"""
core/llm_cli.py

CLI LLM backend: drive a locally logged-in agent CLI (Claude Code) as the
model provider instead of API keys. Activated when ``R2S_LLM_BACKEND=cli``;
``core.llm.call_azure_openai`` dispatches here before touching Azure.

Why not ``claude -p`` one-shot per call: the harness agent loop
(``core/agent_executor.py``) is multi-turn — it appends assistant messages
and tool results to a growing conversation. One-shot print mode loses all
prior context. This module instead maps each harness conversation to a
Claude Code session:

  - First call of a conversation  → ``claude -p --output-format json``
    (system prompt via ``--system-prompt``), capture ``session_id``.
  - Subsequent calls              → ``claude -p --resume <session_id>``
    with ONLY the newly appended messages serialized as the next user turn.

Conversations are append-only (verified in ``agent_executor._run_loop``),
so each run uses an explicit conversation id when available, otherwise the
live messages list identity, and ``sent_count`` tracks how much of it has
been forwarded to the CLI.

Function calling is emulated with a text protocol: tool JSON schemas are
injected into the system prompt and the model must reply with a strict
JSON envelope, which is parsed back into the OpenAI assistant-message
shape (``content`` + ``tool_calls``) so no call site changes are needed.

Config:
  R2S_LLM_BACKEND=cli     enable this backend
  R2S_CLI_TOOL=claude     which CLI to use (only "claude" supported in v1)
  R2S_CLI_MODEL=...       optional model override passed to --model
"""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import threading

from core.llm import LLMError

log = logging.getLogger("llm_cli")

# ---------------------------------------------------------------------------
# Conversation/session registry
# ---------------------------------------------------------------------------


class _Session:
    __slots__ = ("session_id", "sent_count")

    def __init__(self, session_id: str, sent_count: int):
        self.session_id = session_id
        self.sent_count = sent_count


_SESSIONS: dict[str, _Session] = {}
_SESSIONS_LOCK = threading.Lock()


def _conversation_key(messages: list[dict], conversation_id: str | None = None) -> str:
    """Identify a conversation run.

    Prefer an explicit run id when the caller has one. Otherwise fall back to
    the live messages list identity so identical prompts from separate runs do
    not share a Claude session.
    """
    if conversation_id:
        return str(conversation_id)
    return f"messages:{id(messages)}"


def reset_sessions() -> None:
    """Drop all session mappings (tests, long-running daemons between tasks)."""
    with _SESSIONS_LOCK:
        _SESSIONS.clear()


# ---------------------------------------------------------------------------
# Message serialization
# ---------------------------------------------------------------------------


def _content_to_text(content) -> str:
    """Flatten OpenAI content (str or parts list) to plain text.

    Image parts cannot be attached through the CLI; they are replaced with an
    explicit placeholder so the model knows material was omitted.
    """
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return str(content or "")
    texts: list[str] = []
    n_images = 0
    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") == "text":
            texts.append(part.get("text", ""))
        elif part.get("type") == "image_url":
            n_images += 1
    if n_images:
        texts.append(f"[{n_images} image(s) omitted: CLI backend cannot attach images]")
    return "\n".join(t for t in texts if t)


def _serialize_new_turns(new_messages: list[dict]) -> str:
    """Serialize newly appended messages into one user-turn text.

    Assistant messages are skipped: they were produced by this backend from
    the CLI's own replies, so the CLI session already contains them.
    """
    blocks: list[str] = []
    for msg in new_messages:
        role = msg.get("role")
        if role == "assistant":
            continue
        if role == "tool":
            name = msg.get("name") or msg.get("tool_call_id") or "unknown"
            blocks.append(
                f"[Tool result for `{name}` "
                f"(call id {msg.get('tool_call_id', '?')})]:\n"
                + _content_to_text(msg.get("content"))
            )
        elif role in ("user", "system"):
            text = _content_to_text(msg.get("content"))
            if text:
                blocks.append(text)
    return "\n\n".join(blocks)


# ---------------------------------------------------------------------------
# Tool-call protocol (text emulation of OpenAI function calling)
# ---------------------------------------------------------------------------

_TOOL_PROTOCOL = """\
TOOL PROTOCOL (mandatory)
You are running inside an automated harness. You do NOT have direct tool \
access; the harness executes tools for you. Available tools (JSON Schema):
{schemas}

Reply with EXACTLY ONE JSON object and nothing else (no markdown fences, \
no prose before or after). Two forms:
1. To call one or more tools:
   {{"content": null, "tool_calls": [{{"id": "call_1", "name": "<tool_name>", "arguments": {{...}}}}]}}
2. When no tool is needed (final answer / status):
   {{"content": "<your full answer>", "tool_calls": []}}
Every reply must be one of these two forms."""


def _build_system_prompt(base: str, tools: list[dict] | None) -> str:
    if not tools:
        return base
    schemas = json.dumps(tools, ensure_ascii=False, indent=1)
    return (base + "\n\n" if base else "") + _TOOL_PROTOCOL.format(schemas=schemas)


def _extract_json_object(text: str) -> dict | None:
    """Parse the first balanced {...} object from model output."""
    text = text.strip()
    # Strip markdown fences if the whole reply is fenced.
    fence = re.fullmatch(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1).strip()
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        pass
    # Balanced-brace scan for the first complete object.
    start = text.find("{")
    while start != -1:
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[start : i + 1])
                        return obj if isinstance(obj, dict) else None
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    return None


def _envelope_to_message(env: dict) -> dict:
    """Convert the parsed tool-protocol envelope to an OpenAI assistant msg."""
    msg: dict = {"role": "assistant", "content": env.get("content") or ""}
    tool_calls = env.get("tool_calls") or []
    if tool_calls:
        msg["tool_calls"] = [
            {
                "id": str(tc.get("id") or f"call_{i}"),
                "type": "function",
                "function": {
                    "name": tc["name"],
                    "arguments": json.dumps(tc.get("arguments") or {}),
                },
            }
            for i, tc in enumerate(tool_calls)
            if isinstance(tc, dict) and tc.get("name")
        ]
        if not msg["tool_calls"]:
            del msg["tool_calls"]
    return msg


# ---------------------------------------------------------------------------
# Claude CLI invocation
# ---------------------------------------------------------------------------


def _cli_tool() -> str:
    return os.environ.get("R2S_CLI_TOOL", "claude").strip().lower()


def _run_claude(
    prompt: str,
    *,
    system_prompt: str | None,
    resume_id: str | None,
    model: str | None,
    timeout: int,
) -> dict:
    """One claude -p invocation. Returns the parsed --output-format json dict."""
    exe = shutil.which("claude")
    if not exe:
        raise LLMError("R2S_CLI_TOOL=claude but `claude` is not on PATH")
    cmd = [exe, "-p", "--output-format", "json"]
    if system_prompt:
        cmd += ["--system-prompt", system_prompt]
    if resume_id:
        cmd += ["--resume", resume_id]
    if model:
        cmd += ["--model", model]
    log.debug("claude call (resume=%s, prompt=%d chars)", bool(resume_id), len(prompt))
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        raise LLMError(f"claude CLI timed out after {timeout}s") from e
    if proc.returncode != 0:
        raise LLMError(f"claude CLI exit {proc.returncode}: {proc.stderr[:500]}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise LLMError(f"claude CLI returned non-JSON output: {proc.stdout[:300]}") from e
    if data.get("is_error"):
        raise LLMError(f"claude CLI error: {data.get('result', '')[:500]}")
    return data


# ---------------------------------------------------------------------------
# Public entry point (mirrors call_azure_openai's contract)
# ---------------------------------------------------------------------------


def call_cli(
    messages: list[dict],
    *,
    tools: list[dict] | None = None,
    model: str | None = None,
    conversation_id: str | None = None,
    max_completion_tokens: int = 4096,  # noqa: ARG001 - CLI has no token cap knob
    timeout: int = 300,
    max_retries: int = 3,
    tool_choice=None,
    **_: object,
) -> dict:
    """Multi-turn LLM call via a local agent CLI. Drop-in for call_azure_openai.

    Returns an OpenAI-style assistant message dict (``content`` and optional
    ``tool_calls``). Raises LLMError after exhausting retries.
    """
    tool = _cli_tool()
    if tool != "claude":
        raise LLMError(f"R2S_CLI_TOOL={tool!r} not supported yet (v1: claude only)")

    cli_model = os.environ.get("R2S_CLI_MODEL") or None
    timeout = max(60, timeout)
    fp = _conversation_key(messages, conversation_id)

    with _SESSIONS_LOCK:
        session = _SESSIONS.get(fp)

    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            if session is None:
                system_msg = next((m for m in messages if m.get("role") == "system"), None)
                base_system = _content_to_text(system_msg.get("content")) if system_msg else ""
                system_prompt = _build_system_prompt(base_system, tools)
                first_turn = _serialize_new_turns(
                    [m for m in messages if m.get("role") != "system"]
                )
                data = _run_claude(
                    first_turn,
                    system_prompt=system_prompt or None,
                    resume_id=None,
                    model=cli_model,
                    timeout=timeout,
                )
                session = _Session(data["session_id"], len(messages))
                with _SESSIONS_LOCK:
                    _SESSIONS[fp] = session
            else:
                new_tail = messages[session.sent_count :]
                turn_text = _serialize_new_turns(new_tail)
                if tool_choice:
                    # Harness is forcing a tool call this round.
                    if isinstance(tool_choice, dict):
                        fn = tool_choice.get("function", {}).get("name", "?")
                        turn_text += (
                            f"\n\n[HARNESS] You MUST call the tool `{fn}` now "
                            "(form 1 of the protocol)."
                        )
                    else:
                        turn_text += (
                            "\n\n[HARNESS] You MUST call at least one tool now "
                            "(form 1 of the protocol)."
                        )
                # The session already carries the system prompt from the first
                # turn; overriding it on resume would drop domain instructions.
                data = _run_claude(
                    turn_text or "Continue.",
                    system_prompt=None,
                    resume_id=session.session_id,
                    model=cli_model,
                    timeout=timeout,
                )

            result_text = data.get("result") or ""
            if not tools:
                session.sent_count = len(messages)
                return {"role": "assistant", "content": result_text}

            env = _extract_json_object(result_text)
            if env is None:
                raise LLMError(
                    f"CLI reply is not a valid tool-protocol envelope: {result_text[:300]}"
                )
            session.sent_count = len(messages)
            return _envelope_to_message(env)

        except LLMError as e:
            last_error = e
            log.warning("CLI call attempt %d/%d failed: %s", attempt, max_retries, e)

    raise LLMError(f"CLI backend exhausted {max_retries} retries. Last error: {last_error}")
