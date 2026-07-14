"""
core/executor.py
Generic MCP-based skill executor.

Design:
  - Skills store reproduction code as a Python async function that calls
    mcp.call_tool(name, args) — the only available API.
  - The executor extracts that function from the skill's analysis Markdown,
    connects to the domain's MCP server via stdio, and executes the function.
  - Fully domain-agnostic: all domain specifics come from domain_config["mcp"].

Usage:
    from core.executor import run_skill

    result = run_skill(skill_dict, domain_config)
    # or async:
    result = await SkillExecutor(domain_config).execute(skill_dict)
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import textwrap
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger("executor")


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class ToolInvocation:
    """Record of a single MCP tool call."""
    tool_name: str
    arguments: dict
    result: str
    error: str = ""
    verify_feedback: str = ""  # auto_verify hook response, if any

    @property
    def success(self) -> bool:
        return not self.error


@dataclass
class ExecutionResult:
    """Result of executing a skill."""
    skill_id: str
    skill_name: str
    success: bool
    tool_calls: list[ToolInvocation] = field(default_factory=list)
    error: str = ""
    note: str = ""  # human-readable summary

    def summary(self) -> str:
        status = "OK" if self.success else "FAILED"
        calls = len(self.tool_calls)
        errs = sum(1 for c in self.tool_calls if not c.success)
        s = f"[{status}] {self.skill_name}  ({calls} tool calls"
        if errs:
            s += f", {errs} errors"
        s += ")"
        if self.error:
            s += f"\n  error: {self.error}"
        if self.note:
            s += f"\n  note:  {self.note}"
        return s


# ---------------------------------------------------------------------------
# MCP wrapper — the object injected into skill code
# ---------------------------------------------------------------------------

class _MCPWrapper:
    """
    Thin async wrapper around an MCP ClientSession.
    Exposes a single method: call_tool(name, arguments) -> str.

    This is the only API available to skill code.
    """

    def __init__(self, session, record: list[ToolInvocation], auto_verify_fn=None):
        self._session = session
        self._record = record
        self._auto_verify = auto_verify_fn

    async def call_tool(self, name: str, arguments: dict | None = None) -> str:
        """Call an MCP tool and return its text result."""
        args = arguments or {}
        log.debug("call_tool: %s %s", name, args)
        try:
            result = await self._session.call_tool(name, args)
            # MCP SDK returns a CallToolResult with .content list
            text = _extract_text(result)
            self._record.append(ToolInvocation(
                tool_name=name, arguments=args, result=text
            ))

            # Run auto_verify hook if available
            if self._auto_verify:
                try:
                    feedback = await self._auto_verify(name, args, text, self)
                    if feedback:
                        log.warning("auto_verify: %s", feedback)
                except Exception as ve:
                    log.debug("auto_verify error (ignored): %s", ve)

            return text
        except Exception as exc:
            err = str(exc)
            log.warning("call_tool %s failed: %s", name, err)
            self._record.append(ToolInvocation(
                tool_name=name, arguments=args, result="", error=err
            ))
            raise


class _DryRunMCPWrapper:
    """
    Dry-run wrapper: logs tool calls but never connects to a real server.
    Returns placeholder responses from domain config so skill code can continue.
    """

    def __init__(self, record: list[ToolInvocation], placeholders: dict[str, str] | None = None):
        self._record = record
        self._placeholders = placeholders or {}

    async def call_tool(self, name: str, arguments: dict | None = None) -> str:
        args = arguments or {}
        placeholder = self._placeholders.get(name, "ok")
        log.info("[dry-run] %s(%s) -> %s", name, args, placeholder)
        self._record.append(ToolInvocation(
            tool_name=name, arguments=args, result=placeholder
        ))
        return placeholder


def _extract_text(call_result) -> str:
    """Extract text content from an MCP CallToolResult.

    FastMCP serializes a `list[dict]` tool return as a `content` list with
    one `TextContent` per element. The previous version of this function
    returned only the first item — silently dropping the rest. That bug made
    every multi-result tool (search_skills returning k=5 → 1 visible result,
    list_skills returning N → 1) behave as if it returned a single item.

    Behavior now:
      - 0 items → str(call_result) fallback
      - 1 item  → that item's text (covers scalar-returning tools)
      - 2+ items, each JSON-parseable → wrap as a single JSON array literal
      - 2+ items, not all JSON → newline-join the texts
    """
    if not hasattr(call_result, "content"):
        return str(call_result)
    texts: list[str] = []
    for item in call_result.content:
        if hasattr(item, "text"):
            texts.append(item.text)
    if not texts:
        return str(call_result)
    if len(texts) == 1:
        return texts[0]
    # Multi-item: try JSON-array packaging so the agent sees a normal list.
    parsed: list[Any] = []
    all_json = True
    for t in texts:
        try:
            parsed.append(json.loads(t))
        except (json.JSONDecodeError, TypeError):
            all_json = False
            break
    if all_json:
        try:
            return json.dumps(parsed, ensure_ascii=False, indent=2)
        except (TypeError, ValueError):
            pass
    return "\n".join(texts)


_MCP_ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::-([^}]*))?\}")


def _expand_mcp_value(value: str) -> str:
    """Expand `${VAR}` and `${VAR:-default}` expressions using the local environment."""
    def repl(match: re.Match[str]) -> str:
        var_name = match.group(1)
        default = match.group(2)
        env_value = os.environ.get(var_name)
        if env_value not in (None, ""):
            return env_value
        return default or ""

    return _MCP_ENV_PATTERN.sub(repl, value)


def _build_server_params(StdioServerParameters, mcp_cfg: dict[str, Any]):
    """Build stdio server parameters from domain MCP config."""
    command = _expand_mcp_value(str(mcp_cfg["command"]))
    args_list = [_expand_mcp_value(str(a)) for a in mcp_cfg.get("args", [])]
    cwd = mcp_cfg.get("cwd")
    env = mcp_cfg.get("env")
    encoding = mcp_cfg.get("encoding", "utf-8")
    encoding_error_handler = mcp_cfg.get("encoding_error_handler", "strict")

    resolved_cwd = _expand_mcp_value(str(cwd)) if cwd else None
    resolved_env = None
    if env:
        resolved_env = {
            str(k): _expand_mcp_value(str(v))
            for k, v in env.items()
        }

    return StdioServerParameters(
        command=command,
        args=args_list,
        cwd=resolved_cwd,
        env=resolved_env,
        encoding=encoding,
        encoding_error_handler=encoding_error_handler,
    )


# ---------------------------------------------------------------------------
# Code extraction
# ---------------------------------------------------------------------------

def extract_code(analysis: str) -> str:
    """
    Extract the first ```python ... ``` block from a skill's Markdown analysis.

    Returns the raw Python source string (not dedented).
    Raises ValueError if no Python block is found.
    """
    # Match fenced code blocks tagged as python
    pattern = re.compile(
        r"```python\s*\n(.*?)```",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(analysis)
    if not m:
        raise ValueError("No ```python code block found in skill analysis")
    return textwrap.dedent(m.group(1))


def extract_function_name(code: str) -> str | None:
    """Extract the name of the first async def in the code block."""
    m = re.search(r"^async\s+def\s+(\w+)", code, re.MULTILINE)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Main executor
# ---------------------------------------------------------------------------

class SkillExecutor:
    """
    Execute a skill via a domain's MCP server.

    Args:
        domain_config: Loaded domain config dict (from core.load_domain).
                       Must have domain_config["mcp"] with "command" and "args".
        dry_run:       If True, trace tool calls without connecting to a server.
    """

    def __init__(self, domain_config: dict, *, dry_run: bool = False):
        self._config = domain_config
        self._mcp_cfg = domain_config.get("mcp")
        self._dry_run = dry_run
        self._auto_verify_fn = None

        if not self._mcp_cfg and not dry_run:
            raise ValueError(
                f"Domain '{domain_config.get('name', '?')}' has no MCP config. "
                "Cannot execute. Set dry_run=True to trace without connecting."
            )

        # Load domain auto_verify hook if configured
        hooks_module = domain_config.get("agent_hooks_module")
        if hooks_module:
            domain_name = domain_config.get("name", "")
            try:
                import importlib
                mod = importlib.import_module(f"domains.{domain_name}.{hooks_module}")
                self._auto_verify_fn = getattr(mod, "auto_verify", None)
            except Exception as exc:
                log.debug("Could not load auto_verify from %s: %s", hooks_module, exc)

    async def execute(self, skill: dict, **kwargs) -> ExecutionResult:
        """
        Execute a skill.

        Args:
            skill:   Full skill detail dict (from skill_store.get_skill).
            **kwargs: Passed through to the skill function as overrides
                      (e.g., width=10, material="oak_log").

        Returns:
            ExecutionResult with tool_calls log and success flag.
        """
        sid = skill.get("skill_id", "unknown")
        name = skill.get("skill_name", "Unknown Skill")

        # Extract code
        analysis = skill.get("analysis", "")
        try:
            code = extract_code(analysis)
        except ValueError as exc:
            return ExecutionResult(
                skill_id=sid, skill_name=name,
                success=False, error=str(exc),
            )

        func_name = extract_function_name(code)
        if not func_name:
            return ExecutionResult(
                skill_id=sid, skill_name=name,
                success=False, error="No 'async def' found in code block",
            )

        log.info("Executing skill '%s' (func=%s, dry_run=%s)", name, func_name, self._dry_run)

        invocations: list[ToolInvocation] = []

        if self._dry_run:
            return await self._exec_dry_run(
                sid, name, code, func_name, invocations, kwargs
            )
        else:
            return await self._exec_live(
                sid, name, code, func_name, invocations, kwargs
            )

    async def _exec_dry_run(
        self, sid, name, code, func_name, invocations, kwargs
    ) -> ExecutionResult:
        placeholders = self._config.get("dry_run_placeholders", {})
        mcp = _DryRunMCPWrapper(invocations, placeholders=placeholders)
        try:
            ns: dict[str, Any] = {}
            exec(compile(code, "<skill>", "exec"), ns)  # noqa: S102
            func = ns.get(func_name)
            if func is None:
                return ExecutionResult(
                    skill_id=sid, skill_name=name,
                    success=False,
                    error=f"Function '{func_name}' not found after exec",
                )
            await func(mcp, **kwargs)
            return ExecutionResult(
                skill_id=sid, skill_name=name,
                success=True, tool_calls=invocations,
                note=f"Dry-run complete: {len(invocations)} tool calls traced",
            )
        except Exception as exc:
            return ExecutionResult(
                skill_id=sid, skill_name=name,
                success=False, tool_calls=invocations, error=str(exc),
            )

    async def _exec_live(
        self, sid, name, code, func_name, invocations, kwargs
    ) -> ExecutionResult:
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
        except ImportError:
            return ExecutionResult(
                skill_id=sid, skill_name=name,
                success=False,
                error="mcp package not installed. Run: pip install mcp",
            )

        server_params = _build_server_params(StdioServerParameters, self._mcp_cfg)

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    log.info("MCP server connected")

                    # Wait for bot to spawn (some MCP servers need time)
                    spawn_wait = self._mcp_cfg.get("spawn_wait", 6)
                    if spawn_wait > 0:
                        log.info("Waiting %ds for bot to spawn...", spawn_wait)
                        await asyncio.sleep(spawn_wait)

                    mcp = _MCPWrapper(session, invocations, auto_verify_fn=self._auto_verify_fn)

                    ns: dict[str, Any] = {}
                    exec(compile(code, "<skill>", "exec"), ns)  # noqa: S102
                    func = ns.get(func_name)
                    if func is None:
                        return ExecutionResult(
                            skill_id=sid, skill_name=name,
                            success=False,
                            error=f"Function '{func_name}' not found after exec",
                        )
                    await func(mcp, **kwargs)
                    return ExecutionResult(
                        skill_id=sid, skill_name=name,
                        success=True, tool_calls=invocations,
                        note=f"{len(invocations)} tool calls executed",
                    )

        except Exception as exc:
            return ExecutionResult(
                skill_id=sid, skill_name=name,
                success=False, tool_calls=invocations, error=str(exc),
            )


# ---------------------------------------------------------------------------
# Convenience synchronous wrapper (for CLI)
# ---------------------------------------------------------------------------

def run_skill(
    skill: dict,
    domain_config: dict,
    *,
    dry_run: bool = False,
    **kwargs,
) -> ExecutionResult:
    """
    Synchronous entry point for executing a skill.

    Args:
        skill:         Full skill dict from skill_store.get_skill().
        domain_config: Loaded domain config (must have "mcp" key).
        dry_run:       If True, trace without connecting.
        **kwargs:      Passed through to the skill function as parameter overrides.

    Returns:
        ExecutionResult.
    """
    executor = SkillExecutor(domain_config, dry_run=dry_run)
    return asyncio.run(executor.execute(skill, **kwargs))
