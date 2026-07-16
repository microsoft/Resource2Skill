"""
core/agent_executor.py
LLM-driven agent loop: GPT-5.4 reasons about a task, issues MCP tool calls
via Azure OpenAI function calling, observes results, and loops until done.

Usage:
    from core.agent_executor import run_agent

    result = run_agent(
        "build a 5x5 cobblestone platform",
        domain_config,
        library_dir,
        model="gpt-5.4",
        reasoning_effort="medium",
    )
    print(result.summary())
"""
from __future__ import annotations

import asyncio
import importlib
import json
import logging
import os
import re
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from core.executor import ToolInvocation, _MCPWrapper, _DryRunMCPWrapper
from core.llm import call_azure_openai, LLMError
from core.mcp_tools_schema import get_tools_from_mcp, load_tools_fallback

log = logging.getLogger("agent_executor")

_TASK_COMPLETE = "TASK_COMPLETE"
_MCP_ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::-([^}]*))?\}")
_REQUESTED_SLIDE_COUNT_PATTERN = re.compile(
    r"\b(?:exactly\s+)?(\d{1,2})\s*[- ]?\s*(?:slide|slides|page|pages)\b",
    re.I,
)


def _declares_task_complete(content: str) -> bool:
    """Return True only for an explicit final completion marker.

    A substring check is too permissive: progress summaries often say things
    like "remaining: save, then return TASK_COMPLETE", which must not terminate
    the agent before the save/render tools actually run.
    """
    for line in (content or "").splitlines():
        marker = line.strip().strip("`").strip()
        if re.match(rf"^{re.escape(_TASK_COMPLETE)}\b", marker):
            return True
    return False


def _requested_slide_count(task: str) -> int | None:
    """Return an explicit deck/page count from the user brief, if present."""
    match = _REQUESTED_SLIDE_COUNT_PATTERN.search(task or "")
    if not match:
        return None
    try:
        count = int(match.group(1))
    except Exception:
        return None
    return count if count > 0 else None


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class AgentResult:
    """Result of an agent loop execution."""
    task: str
    success: bool
    iterations: int
    tool_calls: list[ToolInvocation] = field(default_factory=list)
    conversation: list[dict] = field(default_factory=list)
    final_message: str = ""
    error: str = ""
    note: str = ""

    def summary(self) -> str:
        status = "SUCCESS" if self.success else "INCOMPLETE"
        calls = len(self.tool_calls)
        errs = sum(1 for c in self.tool_calls if not c.success)
        s = f"[{status}] {self.iterations} iterations, {calls} tool calls"
        if errs:
            s += f", {errs} errors"
        if self.error:
            s += f"\n  error: {self.error}"
        if self.note:
            s += f"\n  note:  {self.note}"
        return s


_FLAT_SKILLS_POSTPROCESS_TOOLS = {
    "list_skills", "get_skill_info", "get_skill_text",
}

_SKILL_PATH_GUARD_ERROR = "skill_path_required"
_ARTIFACT_QUALITY_GUARD_ERROR = "artifact_quality_required"

_SKILL_SEARCH_TOOLS = {"list_skills", "search_skills"}
_SKILL_INSPECT_TEXT_TOOLS = {
    "get_skill_info", "get_skill_text", "get_skill_code", "get_skill_recipe",
}
_SKILL_VISUAL_TOOLS = {"get_skill_visual"}
_MIN_VISUAL_SKILL_PAIRS_BY_DOMAIN = {
    "web": 2,
    "ppt": 2,
    "excel": 1,
    "blender": 1,
    "reaper": 1,
}
_MIN_FINAL_SKILL_ATTEMPTS_BY_DOMAIN = {
    "web": 5,       # count internal component skills from init_web_from_schema
    "excel": 3,
    "blender": 3,
    "reaper": 4,
}
_MIN_GROUNDED_SECTIONS_BY_DOMAIN = {
    "ppt": 16,
    "web": 5,
    "blender": 3,
    "reaper": 4,
    "excel": 3,
}

_PRIMARY_SKILL_TOOLS_BY_DOMAIN = {
    # Web schema init composes selected wiki skills internally; direct
    # component insertion is the fallback runtime path.
    "web": {"init_web_from_schema", "add_component_from_skill"},
    # PPT v2 executes through scaffold, but the long-tail wiki skills are
    # mandatory design references and must be threaded into slide metadata.
    "ppt": {"add_slide_from_shell", "add_slide_from_skill"},
    "excel": {
        "apply_skill", "init_from_archetype",
        "add_sheet_from_shell", "apply_component",
    },
    "blender": {
        "apply_skill", "build_scene_from_shell", "add_object_from_skill",
        "apply_lighting_rig", "apply_material_preset",
    },
    "reaper": {"apply_skill"},
}

_TOOLS_REQUIRING_SKILL_INSPECTION = {
    "web": {
        "generate_web_schema", "init_web_from_schema",
        "add_component_from_skill",
    },
    # PPT scaffold (pick_archetype / select_shell / pick_theme) is shared
    # between arms; only the skill-bearing slide call requires inspection.
    "ppt": {"add_slide_from_shell", "add_slide_from_skill"},
    "excel": {
        "apply_skill", "init_from_archetype",
        "add_sheet_from_shell", "apply_component",
    },
    "blender": {
        "apply_skill", "add_object_from_skill",
    },
    "reaper": {"apply_skill"},
}

_MANUAL_TOOLS_REQUIRING_SKILL_ATTEMPT = {
    "web": {"write_file", "save_project"},
    "excel": {"execute_xlsx_code", "save_workbook", "verify_workbook"},
    "blender": {
        "execute_blender_code", "render_scene", "save_scene",
    },
    "reaper": {
        "execute_reaper_code", "create_track", "create_midi_item",
        "add_midi_notes", "add_fx",
    },
}

_FINAL_TOOLS_REQUIRING_SKILL_COUNT = {
    "web": {"save_project"},
    "excel": {"save_workbook", "verify_workbook"},
    "blender": {"render_scene", "save_scene"},
    "reaper": {"render_project", "save_project", "review_audio"},
}

_GROUNDED_PRIMITIVE_TOOLS_BY_DOMAIN = {
    "web": {"write_file"},
    "excel": {"execute_xlsx_code"},
    "blender": {"execute_blender_code"},
    "reaper": {"execute_reaper_code"},
}

_FINAL_TOOLS_REQUIRING_GROUNDED_SECTIONS = {
    "ppt": {"save_presentation"},
    "web": {"save_project"},
    "excel": {"save_workbook", "verify_workbook"},
    "blender": {"render_scene", "save_scene"},
    "reaper": {"render_project", "save_project", "review_audio"},
}

_EXCEL_MUTATION_TOOLS = {
    "create_workbook", "apply_skill", "init_from_archetype",
    "add_sheet_from_shell", "apply_component", "execute_xlsx_code",
}

_WEB_MUTATION_TOOLS = {
    "create_project", "generate_web_schema", "init_web_from_schema",
    "add_component_from_skill", "write_file",
}

_BLENDER_MUTATION_TOOLS = {
    "apply_skill", "build_scene_from_shell", "add_object_from_skill",
    "execute_blender_code", "apply_lighting_rig", "apply_material_preset",
    "apply_scene_polish_pack",
}

_REAPER_FINAL_TOOLS = {"render_project", "review_audio", "save_project"}
_REAPER_MUTATION_TOOLS = {
    "apply_skill", "execute_reaper_code", "create_track", "add_midi_notes",
    "set_tempo",
}


def _flatten_skill_tool_result(tool_name: str, result_text: str) -> str:
    """Strip wiki organization metadata from skill listing/info tool results.

    Used in --flat-skills mode. Goal: agent can still see skill IDs and a
    brief one-line description (so it can pick something to read code for),
    but cannot navigate by category/tag/archetype/theme/applicability.
    Output is shuffled so positional bias from the wiki is gone too.
    """
    if not result_text:
        return result_text
    if tool_name not in _FLAT_SKILLS_POSTPROCESS_TOOLS:
        return result_text

    import random

    # The wiki tools return either JSON (modern wiki path) or plain text
    # (legacy domain MCPs). Handle both.
    text = result_text.strip()
    if text.startswith("{") or text.startswith("["):
        try:
            data = json.loads(text)
        except Exception:
            data = None
        if isinstance(data, dict) and "skills" in data and isinstance(data["skills"], list):
            flat = []
            for s in data["skills"]:
                sid = s.get("skill_id") or s.get("id") or s.get("name") or "?"
                desc = (s.get("description") or s.get("summary")
                        or s.get("skill_name") or "").splitlines()[0][:140]
                flat.append({"skill_id": sid, "description": desc})
            random.shuffle(flat)
            return json.dumps({"skills": flat[:30]}, ensure_ascii=False)
        if isinstance(data, list):
            flat = []
            for s in data:
                if isinstance(s, dict):
                    sid = s.get("skill_id") or s.get("id") or s.get("name") or "?"
                    desc = (s.get("description") or s.get("summary")
                            or s.get("skill_name") or "").splitlines()[0][:140]
                    flat.append({"skill_id": sid, "description": desc})
            random.shuffle(flat)
            return json.dumps(flat[:30], ensure_ascii=False)
        # Unrecognized JSON shape — pass through
        return result_text

    # Plain-text path: most domain MCPs print a category summary or "Found N
    # skills" listing with category/tag info. Strip category info from each
    # line and shuffle. Recognise lines that look like "  <skill_id>  -  ..."
    # or "  <skill_id> [<category>] - <name>".
    lines = text.splitlines()
    skill_lines = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        # Skip header / category-summary lines
        if s.startswith("Skill library:") or s.startswith("Found "):
            continue
        if s.startswith("Categories") or s.startswith("Tier"):
            continue
        # Try to extract skill_id from the start of the line
        head = s.split()[0] if s.split() else ""
        if not head:
            continue
        # Strip [category] markers and trailing tag/applicability annotations
        import re as _re
        cleaned = _re.sub(r"\[[^\]]+\]", "", s)
        cleaned = _re.sub(r"\(category=[^)]+\)", "", cleaned)
        cleaned = _re.sub(r"\s+", " ", cleaned).strip()
        # Truncate to a one-line description
        if " - " in cleaned:
            sid, _, desc = cleaned.partition(" - ")
            skill_lines.append(f"{sid.strip()} — {desc.strip()[:120]}")
        elif ":" in cleaned and " " not in cleaned.split(":", 1)[0]:
            sid, _, desc = cleaned.partition(":")
            skill_lines.append(f"{sid.strip()} — {desc.strip()[:120]}")
        else:
            skill_lines.append(cleaned[:160])
    if not skill_lines:
        return result_text
    random.shuffle(skill_lines)
    skill_lines = skill_lines[:30]
    return f"Found {len(skill_lines)} skills (flat, no wiki organization):\n" + "\n".join(
        f"  {l}" for l in skill_lines
    )


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

    # MCP's default env whitelist excludes Azure/OpenAI creds. Inject them
    # so MCP-side LLM calls (e.g., theme harmonizer, schema generator) work.
    import os as _os
    try:
        from mcp.client.stdio import get_default_environment as _get_default_env
        base_env = _get_default_env()
    except Exception:
        base_env = {}
    cred_keys = (
        "OPENAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY",
        "AZURE_CONFIG_DIR",
    )
    for k, v in _os.environ.items():
        if k.startswith("AZURE_OPENAI_") or k.startswith("VWS_REAPER_") or k in cred_keys:
            if v:
                base_env[k] = v
    if resolved_env is None:
        resolved_env = base_env
    else:
        for k, v in base_env.items():
            resolved_env.setdefault(k, v)

    return StdioServerParameters(
        command=command,
        args=args_list,
        cwd=resolved_cwd,
        env=resolved_env,
        encoding=encoding,
        encoding_error_handler=encoding_error_handler,
    )


# ---------------------------------------------------------------------------
# System prompt builder
# ---------------------------------------------------------------------------

def _build_system_prompt(
    domain_config: dict,
    skill_analyses: list[tuple[str, str, list[dict]]],
) -> str:
    """Build the system prompt for the agent.

    Args:
        domain_config: Domain configuration dict.
        skill_analyses: List of (skill_name, analysis_markdown, frames) tuples.
                        Empty if browse-first mode is active.
    """
    persona = domain_config.get("persona", "You are a helpful expert.")

    # Load domain-specific agent instructions from file
    domain_dir = domain_config.get("_domain_dir")
    prompt_file = domain_config.get("agent_prompt_file", "agent_prompt.md")
    agent_instructions = ""
    if domain_dir:
        prompt_path = Path(domain_dir) / prompt_file
        if prompt_path.exists():
            agent_instructions = prompt_path.read_text(encoding="utf-8")

    parts = [persona]
    if agent_instructions:
        parts.extend(["", agent_instructions])

    # Auto-load skills: any skill_id listed in `auto_load_skills` (domain.yaml
    # or runtime config) gets its `text/overview.md` prepended into the system
    # prompt, BUT ONLY if skill-discovery tools are still enabled. If the
    # caller passed --no-skills (skill-discovery tools disabled), the
    # auto-loaded content is also skipped, so the without-skills baseline
    # really is "LLM with no library access at all".
    auto_load_skills = domain_config.get("auto_load_skills") or []
    disabled_tools = set(domain_config.get("_disabled_tools") or [])
    skill_discovery_disabled = bool(
        disabled_tools & {"list_skills", "get_skill_text", "get_skill_info"}
    )
    # --inline-skills bypass: load primer into system prompt even when tools
    # are disabled. This separates "library-knowledge-in-context" from
    # "library-knowledge-via-tools" as ablation conditions.
    force_auto_load = bool(domain_config.get("_force_auto_load"))
    domain_name = domain_config.get("name") or domain_config.get("domain") or ""
    if auto_load_skills and (force_auto_load or not skill_discovery_disabled) and domain_name:
        try:
            from core import get_wiki_root_override
            wiki_root = get_wiki_root_override(domain_name) or Path(__file__).resolve().parents[1] / "skills_wiki" / domain_name
        except Exception:  # noqa: BLE001
            wiki_root = Path(__file__).resolve().parents[1] / "skills_wiki" / domain_name
        injected_blocks: list[str] = []
        for sid in auto_load_skills:
            overview = wiki_root / sid / "text" / "overview.md"
            if not overview.exists() and domain_config.get("_active_brand"):
                overview = (
                    Path(__file__).resolve().parents[1]
                    / "brand_wiki"
                    / domain_name
                    / str(domain_config["_active_brand"])
                    / "skills"
                    / sid
                    / "text"
                    / "overview.md"
                )
            if not overview.exists():
                continue
            content = overview.read_text(encoding="utf-8", errors="ignore")
            # Truncate to keep prompt reasonable; the primer is dense.
            if len(content) > 12000:
                content = content[:12000] + "\n…(truncated)"
            injected_blocks.append(
                f"### Auto-loaded skill: `{sid}`\n\n"
                f"This content is the `text/overview.md` of the `{sid}` skill, "
                f"injected here at session start because it is configured as a "
                f"foundational primer for this domain. It is already in your "
                f"context, but if the task instructions require an auditable "
                f"`get_skill_text` call, still call that tool so the trace "
                f"records the primer read.\n\n"
                f"{content}"
            )
        if injected_blocks:
            parts.append(
                "\n# AUTO-LOADED FOUNDATIONAL SKILLS\n\n"
                "The following skill content is pre-loaded for you because it is "
                "marked as foundational for this domain. Use it directly; if the "
                "run instructions require a traceable primer read, call "
                "`get_skill_text` as instructed. You can browse other skills via "
                "`list_skills` / `search_skills`.\n"
            )
            parts.extend(injected_blocks)

    if domain_name == "ppt" and domain_config.get("_active_brand"):
        brand = str(domain_config.get("_active_brand"))
        brand_skill_ids = [str(s) for s in (domain_config.get("_brand_skill_ids") or [])]
        role_lines: list[str] = []
        for sid in brand_skill_ids:
            role = "brand slide"
            if sid.startswith("brand_cover"):
                role = "cover slide"
            elif sid.startswith("brand_section"):
                role = "section divider"
            elif sid.startswith("brand_content"):
                role = "content/grid slide"
            elif sid.startswith("brand_data"):
                role = "data/quadrant slide"
            role_lines.append(f"- `{sid}`: primary constructor for {role}")
        parts.append(
            "\n# BRAND SHELL CONSTRUCTION RULES\n\n"
            f"Brand mode is active for `{brand}`. Brand skills are exposed as "
            "PPT shell IDs, so use brand shells as the PRIMARY constructors for "
            "matching slide roles.\n\n"
            + "\n".join(role_lines)
            + "\n\nMandatory workflow:\n"
            "1. For the cover, call `add_slide_from_shell(..., shell_id=\"cover_brand\", ...)`.\n"
            "2. For section dividers, call `section_divider_brand`.\n"
            "3. For body/grid slides, call `content_grid_brand`.\n"
            "4. For metric, quadrant, market, traction, and other data slides, call `data_quadrant_brand`.\n"
            "5. `select_shell` and `list_shells` will surface those brand shells when "
            "a matching role is requested. Prefer them over non-brand shells.\n"
            "6. Do not call `add_slide_from_skill` for slide construction in brand "
            "mode; use `add_slide_from_shell` with the brand shell IDs above.\n"
        )

    skill_selection = domain_config.get("skill_selection", "preselect")

    if domain_config.get("_flat_skills_mode"):
        parts.append(
            "\n# SKILLS MODE: FLAT (no wiki organization)\n\n"
            "Skill code is still accessible via `list_skills`, `get_skill_info`, "
            "`get_skill_code`, and `apply_skill` — but the wiki ORGANIZATION is "
            "hidden: no categories, no tags, no archetypes/themes/palettes, no "
            "semantic search. `list_skills` returns a randomly-shuffled flat "
            "list of (skill_id, brief description) only. You must pick by name "
            "and read code; you cannot browse by structure or get curated "
            "recommendations. Skill discovery tools that depend on the wiki "
            "(search_skills, list_categories, pick_archetype, pick_theme, etc.) "
            "are unavailable.\n"
        )

    if domain_config.get("_require_skill_path"):
        parts.append(
            "\n# AUDITABLE WITH-SKILLS PATH\n\n"
            "This run is part of a with-skills experiment. The trace must show "
            "task-matched skill selection before construction. First call "
            "`search_skills` or `list_skills`, then inspect the selected skill "
            "ids with `get_skill_text`/`get_skill_code`/`get_skill_info` and "
            "`get_skill_visual`. Manual code/write tools are allowed, but every "
            "manual generation call must pass `from_skill_ids` (only ids "
            "inspected in this run), `target_node`/`target_nodes` naming the "
            "section or role being built, and `adaptation_notes` explaining the "
            "borrowed mechanism. Final save/render is blocked until the artifact "
            "has enough grounded sections for this domain.\n"
        )

    if skill_analyses:
        # Preselection mode: inject full skill analyses into system prompt.
        parts.append("\n## Selected Skill — FOLLOW THIS BUILD PLAN")
        parts.append(
            "A skill from the tutorial video library has been selected for this task. "
            "You MUST follow its construction steps, dimensions, materials, and coordinate "
            "patterns as closely as possible. The skill's reproduction code shows the exact "
            "sequence of tool calls — replicate that sequence using your own coordinates "
            "(relative to your starting position).\n"
            "Key rules:\n"
            "- Follow the skill's DIMENSIONS (width, height, depth) exactly\n"
            "- Use the same MATERIALS specified in the skill\n"
            "- Follow the same BUILD ORDER (foundation → walls → features → roof → verify)\n"
            "- Adapt coordinates to your current position but keep relative offsets identical\n"
            "- If the skill uses loops, replicate the same loop pattern\n"
            "- If reference images are provided, use them to verify your build matches visually\n"
        )
        for i, (name, analysis, frames) in enumerate(skill_analyses, 1):
            text = analysis[:8000] if len(analysis) > 8000 else analysis
            parts.append(f"### Skill {i}: {name}")
            parts.append(text)
            if frames:
                parts.append(f"\n**Reference frames**: {len(frames)} images from the tutorial video are attached as visual references. Match your build to these images.")
            parts.append("")
    elif skill_selection == "browse":
        # Browse-first mode: instruct agent to use skill library tools at runtime.
        parts.append(
            "\n## Skill Library — BROWSE AND SELECT AT RUNTIME\n"
            "A skill library is available via MCP tools. You MUST browse it to find "
            "relevant skills before building from scratch.\n"
            "Workflow:\n"
            "1. Call `list-skills` (no args) to see category summary\n"
            "2. Call `list-skills(category=...)` to browse specific categories\n"
            "3. Call `get-skill-info(skill_id=...)` to read metadata and code preview\n"
            "4. Call `get-skill-code(skill_id=...)` to read full implementation code\n"
            "5. Use the skill via the appropriate tool (add-component-from-skill, "
            "add-object-from-skill, etc.) OR write custom code inspired by the skill\n"
            "6. Compose multiple skills to build the complete artifact\n\n"
            "Key rules:\n"
            "- ALWAYS browse skills before writing custom code\n"
            "- Prefer using existing skills over writing from scratch\n"
            "- Compose multiple skills for complex tasks\n"
            "- Verified skills (exec_ok=true) are more reliable\n"
        )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Agent executor
# ---------------------------------------------------------------------------

class AgentExecutor:
    """
    LLM-driven agent loop for executing tasks via MCP tools.

    The agent:
    1. Retrieves relevant skills from the library as reference
    2. Connects to the domain's MCP server
    3. Sends the task + skills + tool schemas to GPT-5.4
    4. Iteratively: GPT-5.4 issues tool calls → execute via MCP → feed results back
    5. Terminates when GPT-5.4 says TASK_COMPLETE or limits are hit
    """

    def __init__(
        self,
        domain_config: dict,
        *,
        model: str = "gpt-5.4",
        reasoning_effort: str = "medium",
        max_iterations: int = 200,
        max_consecutive_errors: int = 5,
        n_skills: int = 5,
        top_k: int = 20,
        dry_run: bool = False,
    ):
        self._config = domain_config
        self._mcp_cfg = domain_config.get("mcp")
        self._model = model
        self._reasoning = reasoning_effort
        self._max_iter = max_iterations
        self._max_errors = max_consecutive_errors
        self._n_skills = n_skills
        self._top_k = top_k
        self._dry_run = dry_run

        # Stuck-loop detection config (domain-agnostic)
        self._failure_patterns = [
            re.compile(p)
            for p in domain_config.get("failure_patterns", [])
        ]
        self._max_repeated = domain_config.get("max_repeated_failures", 4)

        if not self._mcp_cfg and not dry_run:
            raise ValueError(
                f"Domain '{domain_config.get('name', '?')}' has no MCP config. "
                "Use dry_run=True or add MCP config."
            )

    def _is_failure_result(self, text: str) -> bool:
        """Check if a tool result text matches any configured failure pattern."""
        if not self._failure_patterns:
            return False
        return any(p.search(text) for p in self._failure_patterns)

    @staticmethod
    def _extract_image_attachment(text: str) -> str | None:
        """If a tool result is JSON containing `_image_attachment: <abs path>`,
        return the path. Used by get_skill_visual to inline an image as a
        follow-up vision message without bloating the tool result with base64.
        """
        if not text or "_image_attachment" not in text:
            return None
        try:
            data = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return None
        if isinstance(data, dict):
            p = data.get("_image_attachment")
            return p if isinstance(p, str) and p else None
        return None

    async def run(self, task: str, library_dir: Path) -> AgentResult:
        """Run the agent loop for a task."""
        # ------------------------------------------------------------------
        # 1. Retrieve reference skills (skip if browse-first mode)
        # ------------------------------------------------------------------
        skill_selection = self._config.get("skill_selection", "preselect")
        if skill_selection == "browse":
            skill_analyses = []
            log.info("Browse-first mode: skipping preselection (agent uses list-skills at runtime)")
        else:
            skill_analyses = self._retrieve_skills(task, library_dir)
            log.info("Retrieved %d reference skills", len(skill_analyses))

        # ------------------------------------------------------------------
        # 2. Connect to MCP and get tool schemas
        # ------------------------------------------------------------------
        if self._dry_run:
            openai_tools = self._load_fallback_tools()
            return await self._run_loop(
                task, skill_analyses,
                mcp_wrapper=None, openai_tools=openai_tools,
            )
        else:
            return await self._run_with_mcp(task, skill_analyses)

    def _load_fallback_tools(self) -> list[dict]:
        """Load tool schemas for dry-run from domain config."""
        domain_dir = self._config.get("_domain_dir")
        fallback_file = self._config.get("tools_fallback_file")
        if domain_dir and fallback_file:
            path = Path(domain_dir) / fallback_file
            if path.exists():
                return load_tools_fallback(path)
        log.warning("No tools_fallback_file configured; dry-run will have no tools")
        return []

    def _load_hooks_module(self):
        """Load the domain's agent_hooks module, returning it or None.

        Result is cached on self to avoid reloading.
        """
        if hasattr(self, "_hooks_module_cache"):
            return self._hooks_module_cache

        domain_dir = self._config.get("_domain_dir")
        hooks_module = self._config.get("agent_hooks_module")
        self._hooks_module_cache = None

        if not domain_dir or not hooks_module:
            return None
        hooks_path = Path(domain_dir) / f"{hooks_module}.py"
        if not hooks_path.exists():
            return None
        try:
            spec = importlib.util.spec_from_file_location(
                f"domains.{self._config.get('name', 'unknown')}.{hooks_module}",
                hooks_path,
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            log.info("Loaded agent hooks module from %s", hooks_path)
            self._hooks_module_cache = mod
            return mod
        except Exception as e:
            log.warning("Failed to load agent hooks from %s: %s", hooks_path, e)
            return None

    def _load_verify_hook(self):
        """Load the auto_verify hook from the domain's agent_hooks module."""
        mod = self._load_hooks_module()
        return getattr(mod, "auto_verify", None) if mod else None

    def _load_progress_hook(self):
        """Load the progress_check hook from the domain's agent_hooks module."""
        mod = self._load_hooks_module()
        return getattr(mod, "progress_check", None) if mod else None

    @staticmethod
    def _is_skill_path_guard_invocation(inv: ToolInvocation) -> bool:
        return (
            getattr(inv, "error", "") == _SKILL_PATH_GUARD_ERROR
            or str(getattr(inv, "result", "")).startswith("Error: SKILL_PATH_REQUIRED")
        )

    @staticmethod
    def _is_out_of_pool_invocation(inv: ToolInvocation) -> bool:
        result = str(getattr(inv, "result", "") or "")
        return (
            getattr(inv, "error", "") == "out_of_pool"
            or (
                result.startswith("ERROR:")
                and "not in the current skill pool" in result
            )
        )

    @classmethod
    def _effective_invocations(cls, invocations: list[ToolInvocation]) -> list[ToolInvocation]:
        """Return calls that reached the active skill surface and can count."""
        return [
            inv for inv in invocations
            if not cls._is_skill_path_guard_invocation(inv)
            and not cls._is_out_of_pool_invocation(inv)
        ]

    @classmethod
    def _actual_tool_names(cls, invocations: list[ToolInvocation]) -> list[str]:
        """Return tool names that actually reached MCP, excluding guard blocks."""
        return [inv.tool_name for inv in cls._effective_invocations(invocations)]

    @staticmethod
    def _coerce_str_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return []
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [str(v).strip() for v in parsed if str(v).strip()]
            except Exception:
                pass
            return [v.strip() for v in text.split(",") if v.strip()]
        return []

    @classmethod
    def _coerce_target_nodes(cls, value: Any, fallback: str = "") -> list[str]:
        targets = cls._coerce_str_list(value)
        if targets:
            return targets
        fallback = str(fallback or "").strip()
        return [fallback] if fallback else []

    @classmethod
    def _skill_ids_from_payload(cls, payload: Any) -> set[str]:
        ids: set[str] = set()
        if isinstance(payload, dict):
            for key, value in payload.items():
                if key in {"skill_id", "skillId"}:
                    text = str(value or "").strip()
                    if text:
                        ids.add(text)
                elif key == "id":
                    text = str(value or "").strip()
                    if text and not text.startswith("call_"):
                        ids.add(text)
                else:
                    ids.update(cls._skill_ids_from_payload(value))
        elif isinstance(payload, list):
            for item in payload:
                ids.update(cls._skill_ids_from_payload(item))
        return ids

    @classmethod
    def _discovered_skill_ids(cls, invocations: list[ToolInvocation]) -> set[str]:
        """Skill ids surfaced by this run's search/list calls."""
        ids: set[str] = set()
        for inv in cls._effective_invocations(invocations):
            if inv.tool_name not in _SKILL_SEARCH_TOOLS or inv.error:
                continue
            result = str(inv.result or "")
            parsed = cls._parse_json_result(result)
            if parsed is not None:
                ids.update(cls._skill_ids_from_payload(parsed))
            # Legacy list_skills surfaces ids in plain text: "(id: foo_bar)".
            for match in re.finditer(
                r"(?:\bskill_id\b|\bid\b)\s*[:=]\s*['\"]?([A-Za-z0-9_.:-]+)",
                result,
            ):
                sid = match.group(1).strip().rstrip("),.;")
                if sid and not sid.startswith("call_"):
                    ids.add(sid)
        return ids

    @classmethod
    def _inspected_skill_ids(cls, invocations: list[ToolInvocation]) -> set[str]:
        """Skill ids actually inspected in this run via text/code/info/visual."""
        inspect_tools = _SKILL_INSPECT_TEXT_TOOLS | _SKILL_VISUAL_TOOLS
        ids: set[str] = set()
        for inv in cls._effective_invocations(invocations):
            if inv.tool_name not in inspect_tools or inv.error:
                continue
            args = inv.arguments if isinstance(inv.arguments, dict) else {}
            sid = str(args.get("skill_id", "")).strip()
            if sid:
                ids.add(sid)
        return ids

    @classmethod
    def _provenance_skill_ids_from_args(cls, args: dict[str, Any]) -> list[str]:
        return cls._coerce_str_list(
            args.get("from_skill_ids")
            or args.get("from_skill_id")
            or args.get("from_skills")
            or args.get("skill_ids")
        )

    @classmethod
    def _runtime_arg_skill_ids(
        cls,
        domain: str,
        fn_name: str,
        args: dict[str, Any],
    ) -> list[str]:
        """Skill ids named directly by primary skill tools."""
        if domain == "web" and fn_name == "add_component_from_skill":
            sid = str(args.get("skill_id", "")).strip()
            return [sid] if sid else []
        if domain == "ppt":
            if fn_name == "add_slide_from_shell":
                return cls._coerce_str_list(args.get("design_reference_skill_ids"))
            if fn_name == "add_slide_from_skill":
                sid = str(args.get("skill_id", "")).strip()
                return [sid] if sid else []
        if domain == "excel":
            arg_name = {
                "apply_skill": "skill_id",
                "init_from_archetype": "archetype_id",
                "add_sheet_from_shell": "shell_id",
                "apply_component": "component_id",
            }.get(fn_name)
            sid = str(args.get(arg_name, "")).strip() if arg_name else ""
            return [sid] if sid else []
        if domain == "blender":
            arg_name = {
                "apply_skill": "skill_id",
                "add_object_from_skill": "skill_id",
            }.get(fn_name)
            sid = str(args.get(arg_name, "")).strip() if arg_name else ""
            return [sid] if sid else []
        if domain == "reaper" and fn_name == "apply_skill":
            sid = str(args.get("skill_id", "")).strip()
            return [sid] if sid else []
        return []

    @staticmethod
    def _missing_current_run_ids(
        ids: list[str],
        *,
        discovered: set[str],
        inspected: set[str],
    ) -> tuple[list[str], list[str]]:
        unique = sorted(set(ids))
        not_inspected = [sid for sid in unique if sid not in inspected]
        not_discovered = (
            [sid for sid in unique if sid not in discovered]
            if discovered else []
        )
        return not_inspected, not_discovered

    @classmethod
    def _grounding_targets_for_call(
        cls,
        domain: str,
        fn_name: str,
        args: dict[str, Any],
        index: int,
    ) -> list[str]:
        explicit = args.get("target_node") or args.get("target_nodes")
        fallback = ""
        if domain == "web":
            fallback = str(args.get("filename", "")).strip()
        elif domain == "excel":
            fallback = ":".join(
                p for p in [
                    str(args.get("sheet_name", "")).strip(),
                    str(args.get("anchor", "")).strip(),
                ] if p
            )
        elif domain == "blender":
            fallback = (
                str(args.get("object_name", "")).strip()
                or str(args.get("shell_id", "")).strip()
                or str(args.get("output_name", "")).strip()
            )
        elif domain == "reaper":
            fallback = (
                str(args.get("track_name", "")).strip()
                or str(args.get("output_name", "")).strip()
            )
        elif domain == "ppt":
            fallback = str(args.get("slide_role", "")).strip()
        fallback = fallback or f"{fn_name}_{index + 1}"
        return cls._coerce_target_nodes(explicit, fallback=fallback)

    @classmethod
    def _web_schema_groundings(
        cls,
        inv: ToolInvocation,
        index: int,
        inspected: set[str],
    ) -> list[dict[str, Any]]:
        groundings: list[dict[str, Any]] = []
        result = str(inv.result or "")
        for match in re.finditer(
            r"\[(\d+)\]\s+([^(\n]+).*?->\s*([A-Za-z0-9_-]+):\s*",
            result,
        ):
            role = match.group(2).strip() or f"section_{match.group(1)}"
            sid = match.group(3).strip()
            if sid and sid in inspected:
                groundings.append({
                    "tool_name": inv.tool_name,
                    "target_node": role,
                    "from_skill_ids": [sid],
                    "call_index": index,
                })
        return groundings

    @classmethod
    def _grounded_sections(
        cls,
        domain: str,
        invocations: list[ToolInvocation],
    ) -> list[dict[str, Any]]:
        effective = cls._effective_invocations(invocations)
        inspected = cls._inspected_skill_ids(effective)
        groundings: list[dict[str, Any]] = []
        primitive_tools = _GROUNDED_PRIMITIVE_TOOLS_BY_DOMAIN.get(domain, set())

        for index, inv in enumerate(effective):
            if inv.error:
                continue
            name = inv.tool_name
            args = inv.arguments if isinstance(inv.arguments, dict) else {}

            if domain == "web" and name == "init_web_from_schema":
                groundings.extend(cls._web_schema_groundings(inv, index, inspected))
                continue

            ids: list[str] = []
            if name in primitive_tools:
                ids = cls._provenance_skill_ids_from_args(args)
            else:
                ids = cls._runtime_arg_skill_ids(domain, name, args)
            if not ids or any(sid not in inspected for sid in ids):
                continue

            targets = cls._grounding_targets_for_call(domain, name, args, index)
            if domain == "ppt" and name == "add_slide_from_shell":
                targets = [f"slide_{index + 1}:{targets[0]}"]
            for target in targets:
                groundings.append({
                    "tool_name": name,
                    "target_node": target,
                    "from_skill_ids": sorted(set(ids)),
                    "call_index": index,
                })
        return groundings

    @staticmethod
    def _has_nonempty_ppt_reference_ids(fn_args: dict[str, Any]) -> bool:
        found = AgentExecutor._coerce_str_list(
            fn_args.get("design_reference_skill_ids")
        )
        return len(set(found)) >= 2

    @staticmethod
    def _visual_result_has_image(result_text: str) -> bool:
        if not result_text:
            return False
        try:
            payload = json.loads(result_text)
        except Exception:
            return False
        if not isinstance(payload, dict):
            return False
        return bool(payload.get("_image_attachment") or payload.get("path"))

    @staticmethod
    def _web_component_skill_count(invocations: list[ToolInvocation]) -> int:
        """Count component skills actually composed by web schema/runtime tools."""
        skill_ids: set[str] = set()
        for inv in invocations:
            if inv.tool_name == "add_component_from_skill":
                sid = str(inv.arguments.get("skill_id", "")).strip()
                if sid:
                    skill_ids.add(sid)
                continue
            if inv.tool_name != "init_web_from_schema":
                continue
            text = str(inv.result or "")
            for match in re.finditer(r"->\s*([A-Za-z0-9_-]+):\s*Added component from skill", text):
                skill_ids.add(match.group(1))
        return len(skill_ids)

    @classmethod
    def _runtime_skill_ids(
        cls,
        domain: str,
        invocations: list[ToolInvocation],
    ) -> set[str]:
        """Return distinct skill/design-system ids that actually affected build.

        This is stricter than counting calls. Reusing the same skill repeatedly
        should not satisfy the "compose multiple roles" guard.
        """
        ids: set[str] = set()
        for inv in cls._effective_invocations(invocations):
            name = inv.tool_name
            args = inv.arguments if isinstance(inv.arguments, dict) else {}
            if domain == "web":
                if name == "add_component_from_skill":
                    sid = str(args.get("skill_id", "")).strip()
                    if sid:
                        ids.add(sid)
                elif name == "init_web_from_schema":
                    for match in re.finditer(
                        r"->\s*([A-Za-z0-9_-]+):\s*Added component from skill",
                        str(inv.result or ""),
                    ):
                        ids.add(match.group(1))
            elif domain == "ppt":
                if name == "add_slide_from_shell":
                    for sid in cls._coerce_str_list(
                        args.get("design_reference_skill_ids")
                    ):
                        ids.add(sid)
            elif domain == "excel":
                if name == "apply_skill":
                    sid = str(args.get("skill_id", "")).strip()
                elif name == "init_from_archetype":
                    sid = str(args.get("archetype_id", "")).strip()
                elif name == "add_sheet_from_shell":
                    sid = str(args.get("shell_id", "")).strip()
                elif name == "apply_component":
                    sid = str(args.get("component_id", "")).strip()
                else:
                    sid = ""
                if sid:
                    ids.add(sid)
            elif domain == "blender":
                if name in {"apply_skill", "add_object_from_skill"}:
                    sid = str(args.get("skill_id", "")).strip()
                elif name == "build_scene_from_shell":
                    sid = str(args.get("shell_id", "")).strip()
                elif name == "apply_lighting_rig":
                    sid = "lighting:" + str(args.get("rig_name", "")).strip()
                elif name == "apply_material_preset":
                    sid = "material:" + str(args.get("preset_name", "")).strip()
                else:
                    sid = ""
                if sid and not sid.endswith(":"):
                    ids.add(sid)
            elif domain == "reaper":
                if name == "apply_skill":
                    sid = str(args.get("skill_id", "")).strip()
                    if sid:
                        ids.add(sid)
        return ids

    @classmethod
    def _claimed_provenance_skill_ids(
        cls,
        domain: str,
        invocations: list[ToolInvocation],
    ) -> set[str]:
        """Skill ids that the current artifact trace claims as provenance.

        Unlike _runtime_skill_ids, this excludes domain presets/shell ids that
        are not wiki skills, and includes web schema component ids selected
        inside init_web_from_schema after the call returns.
        """
        ids: set[str] = set()
        primitive_tools = _GROUNDED_PRIMITIVE_TOOLS_BY_DOMAIN.get(domain, set())
        for inv in cls._effective_invocations(invocations):
            if inv.error:
                continue
            name = inv.tool_name
            args = inv.arguments if isinstance(inv.arguments, dict) else {}
            if name in primitive_tools:
                ids.update(cls._provenance_skill_ids_from_args(args))
                continue
            if domain == "web" and name == "init_web_from_schema":
                for match in re.finditer(
                    r"->\s*([A-Za-z0-9_-]+):\s*Added component from skill",
                    str(inv.result or ""),
                ):
                    ids.add(match.group(1))
                continue
            ids.update(cls._runtime_arg_skill_ids(domain, name, args))
        return ids

    @staticmethod
    def _parse_json_result(result_text: str) -> Any | None:
        if not result_text:
            return None
        text = str(result_text).strip()
        if not (text.startswith("{") or text.startswith("[")):
            return None
        try:
            return json.loads(text)
        except Exception:
            return None

    @staticmethod
    def _last_invocation_index(
        invocations: list[ToolInvocation],
        tool_names: set[str],
    ) -> tuple[int, ToolInvocation] | tuple[None, None]:
        for i in range(len(invocations) - 1, -1, -1):
            inv = invocations[i]
            if inv.tool_name in tool_names and not inv.error:
                return i, inv
        return None, None

    @classmethod
    def _last_json_result(
        cls,
        invocations: list[ToolInvocation],
        tool_name: str,
    ) -> tuple[int, dict] | tuple[None, None]:
        for i in range(len(invocations) - 1, -1, -1):
            inv = invocations[i]
            if inv.tool_name != tool_name or inv.error:
                continue
            parsed = cls._parse_json_result(str(inv.result or ""))
            if isinstance(parsed, dict):
                return i, parsed
        return None, None

    @staticmethod
    def _task_needs_chart(task: str) -> bool:
        text = (task or "").lower()
        keywords = (
            "dashboard", "chart", "charts", "graph", "trend", "kpi",
            "summary", "executive", "forecast", "comparison", "compare",
            "financial", "report", "visualize", "visualization",
        )
        return any(k in text for k in keywords)

    @staticmethod
    def _parse_web_render_stats(text: str) -> dict[str, int]:
        section_count = 0
        page_w = page_h = 0
        match = re.search(
            r"Rendered:\s*(\d+)x(\d+)px.*?(\d+)\s+top-level sections",
            text or "",
            re.I,
        )
        if match:
            page_w = int(match.group(1))
            page_h = int(match.group(2))
            section_count = int(match.group(3))
        return {"page_w": page_w, "page_h": page_h, "sections": section_count}

    @staticmethod
    def _parse_web_dom_stats(text: str) -> dict[str, int]:
        elements = errors = 0
        match = re.search(r"DOM:\s*(\d+)\s+elements", text or "", re.I)
        if match:
            elements = int(match.group(1))
        err_match = re.search(r"Console errors:\s*(\d+)", text or "", re.I)
        if err_match:
            errors = int(err_match.group(1))
        return {"elements": elements, "console_errors": errors}

    @classmethod
    def _web_quality_guard_message(
        cls,
        fn_name: str,
        invocations: list[ToolInvocation],
    ) -> str | None:
        if fn_name != "save_project":
            return None
        effective = cls._effective_invocations(invocations)
        init_idx, _ = cls._last_invocation_index(
            effective, {"init_web_from_schema"}
        )
        render_idx, render_inv = cls._last_invocation_index(effective, {"render_page"})
        dom_idx, dom_inv = cls._last_invocation_index(effective, {"inspect_dom"})
        if render_inv is None or render_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: before save_project, call "
                "`render_page` so the composed skill page is visible and can be "
                "checked for full-page layout quality."
            )
        if dom_inv is None or dom_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: before save_project, call "
                "`inspect_dom` after rendering to confirm section density and "
                "console health."
            )
        # Schema output is a draft; only require schema-specific refinement
        # when the agent chose the schema composer. Manual component assembly
        # remains a valid runtime-skill path.
        if init_idx is not None and not any(
            i > init_idx and inv.tool_name in {"reflect_and_swap", "write_file"}
            for i, inv in enumerate(effective)
        ):
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: schema output is a draft "
                "only. After `init_web_from_schema`, refine the page with "
                "`reflect_and_swap` (or `write_file` to fix layout/content) "
                "and then re-render before saving."
            )
        last_mutation = -1
        for i, inv in enumerate(effective):
            if inv.tool_name in _WEB_MUTATION_TOOLS:
                last_mutation = i
        if last_mutation > render_idx or last_mutation > dom_idx:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: the web project changed after "
                "the last render/DOM inspection. Run `render_page` and "
                "`inspect_dom` again before saving."
            )
        render_stats = cls._parse_web_render_stats(str(render_inv.result or ""))
        dom_stats = cls._parse_web_dom_stats(str(dom_inv.result or ""))
        blockers: list[str] = []
        if render_stats["sections"] and render_stats["sections"] < 7:
            blockers.append(f"only {render_stats['sections']} top-level sections; add FAQ/proof/CTA/footer density")
        if dom_stats["elements"] and dom_stats["elements"] < 80:
            blockers.append(f"only {dom_stats['elements']} DOM elements; page is too sparse for a scored landing page")
        if dom_stats["console_errors"] > 0:
            blockers.append(f"{dom_stats['console_errors']} console error(s) present")
        if blockers:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: Web quality check found "
                + "; ".join(blockers)
                + ". Use the skill path or write_file repair, then rerender and "
                "inspect before saving."
            )
        return None

    @classmethod
    def _excel_quality_guard_message(
        cls,
        fn_name: str,
        invocations: list[ToolInvocation],
        task: str,
    ) -> str | None:
        if fn_name not in {"save_workbook", "verify_workbook"}:
            return None
        effective = cls._effective_invocations(invocations)
        reflect_idx, reflect = cls._last_json_result(effective, "workbook_reflect")
        if not isinstance(reflect, dict) or reflect_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: before saving/verifying a "
                "with-skills Excel artifact, call `workbook_reflect(workbook_id)`, "
                "read its warnings, fix weak data/chart/sheet issues, then save."
            )

        last_mutation = -1
        for i, inv in enumerate(effective):
            if inv.tool_name in _EXCEL_MUTATION_TOOLS:
                last_mutation = i
        if last_mutation > reflect_idx:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: the workbook changed after "
                "the last `workbook_reflect`. Run `workbook_reflect` again and "
                "fix any remaining warnings before save/verify."
            )

        totals = reflect.get("totals") or {}
        warnings = [str(w) for w in (reflect.get("warnings") or [])]
        blockers: list[str] = []
        total_rows = int(totals.get("total_data_rows") or 0)
        total_charts = int(totals.get("total_charts") or 0)
        total_placeholders = int(totals.get("total_placeholders") or 0)
        empty_sheets = int(totals.get("empty_sheets") or 0)

        if total_rows < 60:
            blockers.append(f"only {total_rows} total data rows; add >=60 realistic rows")
        if total_placeholders > 0:
            blockers.append(f"{total_placeholders} placeholder strings remain")
        if empty_sheets > 0:
            blockers.append(f"{empty_sheets} empty sheet(s) remain")
        if cls._task_needs_chart(task) and total_charts < 1:
            blockers.append("brief needs dashboard/chart/report polish but workbook has no chart")

        for warning in warnings:
            low = warning.lower()
            if "placeholder" in low or "empty" in low or "default 'sheet'" in low:
                blockers.append(warning)
            elif "data rows" in low and ("only" in low or "<60" in low):
                blockers.append(warning)
            elif "no charts" in low and cls._task_needs_chart(task):
                blockers.append(warning)

        if blockers:
            unique = []
            for item in blockers:
                if item not in unique:
                    unique.append(item)
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: Excel reflection found "
                "issues that will hurt the artifact score: "
                + "; ".join(unique[:5])
                + ". Fix with `execute_xlsx_code` or another matched skill, "
                "then run `workbook_reflect` again before saving."
            )
        return None

    @staticmethod
    def _parse_blender_scene_info(text: str) -> dict[str, int]:
        obj_match = re.search(r"Objects\s*\((\d+)\)", text or "")
        if not obj_match:
            obj_match = re.search(r"Objects:\s*(\d+)", text or "")
        object_count = int(obj_match.group(1)) if obj_match else 0
        light_count = len(re.findall(r"\[LIGHT\]", text or ""))
        mesh_count = len(re.findall(r"\[MESH\]", text or ""))
        materials = {
            m.group(1).strip()
            for m in re.finditer(r"material:\s*(.+)", text or "")
            if m.group(1).strip()
        }
        return {
            "objects": object_count,
            "meshes": mesh_count,
            "lights": light_count,
            "materials": len(materials),
        }

    @classmethod
    def _blender_quality_guard_message(
        cls,
        fn_name: str,
        invocations: list[ToolInvocation],
        require_skill_path: bool = True,
    ) -> str | None:
        if fn_name not in {"render_scene", "save_scene"}:
            return None
        effective = cls._effective_invocations(invocations)
        render_idx, _ = cls._last_invocation_index(effective, {"render_scene"})

        if fn_name == "save_scene" and render_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: save_scene is locked until "
                "a successful final `render_scene` has produced the scored PNG."
            )
        if not require_skill_path:
            return None

        scene_idx, scene_inv = cls._last_invocation_index(effective, {"get_scene_info"})
        screenshot_idx, _ = cls._last_invocation_index(
            effective, {"get_viewport_screenshot"}
        )
        polish_idx, _ = cls._last_invocation_index(
            effective, {"apply_scene_polish_pack"}
        )
        if polish_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: call "
                "`apply_scene_polish_pack(scene_type=\"auto\")` before final "
                "render/save so shell/skill output gets set dressing, material, "
                "lighting, and camera polish."
            )
        if scene_inv is None or scene_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: call `get_scene_info` before "
                "final render/save so the scene can be checked for object, "
                "material, and lighting density."
            )
        if screenshot_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: call `get_viewport_screenshot`, "
                "inspect the preview, and fix framing/lighting before final render."
            )
        last_mutation = -1
        last_non_polish_mutation = -1
        for i, inv in enumerate(effective):
            if inv.tool_name in _BLENDER_MUTATION_TOOLS:
                last_mutation = i
                if inv.tool_name != "apply_scene_polish_pack":
                    last_non_polish_mutation = i
        if polish_idx < last_non_polish_mutation:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: the scene changed after the "
                "last `apply_scene_polish_pack`. Run the polish pack again, then "
                "`get_scene_info` and `get_viewport_screenshot` before final render. "
                "Exact required sequence: `apply_scene_polish_pack` -> "
                "`get_scene_info` -> `get_viewport_screenshot` -> `render_scene`."
            )
        if scene_idx < last_mutation or screenshot_idx < last_mutation:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: the scene changed after the "
                "last scene info or viewport screenshot. Re-check with "
                "`get_scene_info` and `get_viewport_screenshot` before final render. "
                "Exact required sequence: `apply_scene_polish_pack` -> "
                "`get_scene_info` -> `get_viewport_screenshot` -> `render_scene`; "
                "do not call any mutating tool, including another polish pack, "
                "between the screenshot and render."
            )
        if fn_name == "save_scene" and render_idx is not None and last_mutation > render_idx:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: the scene changed after the "
                "last render. Run `render_scene` again before `save_scene`."
            )
        stats = cls._parse_blender_scene_info(str(scene_inv.result or ""))
        blockers: list[str] = []
        if stats["objects"] < 18:
            blockers.append(f"scene has {stats['objects']} objects; add set dressing/detail to reach >=18")
        if stats["materials"] < 5:
            blockers.append(f"scene has {stats['materials']} distinct materials; apply richer material presets/procedurals")
        if stats["lights"] < 3:
            blockers.append(f"scene has {stats['lights']} lights; add key/fill/rim or a lighting rig")
        if stats["meshes"] < 12:
            blockers.append(f"scene has {stats['meshes']} mesh objects; add layered geometry, props, or repeated motifs")
        if blockers:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: Blender scene is still a "
                "weak blockout: "
                + "; ".join(blockers[:5])
                + ". Use matched skills/materials/lighting plus `execute_blender_code`, "
                "then re-check with `get_scene_info` and screenshot."
            )
        return None

    @staticmethod
    def _parse_reaper_project_info(text: str) -> dict[str, int]:
        track_match = re.search(r"Tracks\s*\((\d+)\)", text or "")
        if not track_match:
            track_match = re.search(r"Tracks:\s*(\d+)", text or "")
        notes_match = re.search(r"Total notes:\s*(\d+)", text or "")
        return {
            "tracks": int(track_match.group(1)) if track_match else 0,
            "notes": int(notes_match.group(1)) if notes_match else 0,
        }

    @staticmethod
    def _parse_reaper_review_overall(text: str) -> float | None:
        match = re.search(r"OVERALL:\s*([0-9.]+)\s*/\s*10", text or "", re.I)
        if not match:
            return None
        try:
            return float(match.group(1))
        except Exception:
            return None

    @staticmethod
    def _parse_reaper_review_dimension(text: str, label: str) -> float | None:
        match = re.search(
            rf"{re.escape(label)}:\s*([0-9.]+)\s*/\s*10",
            text or "",
            re.I,
        )
        if not match:
            return None
        try:
            return float(match.group(1))
        except Exception:
            return None

    @classmethod
    def _reaper_quality_guard_message(
        cls,
        fn_name: str,
        invocations: list[ToolInvocation],
    ) -> str | None:
        if fn_name not in _REAPER_FINAL_TOOLS:
            return None
        effective = cls._effective_invocations(invocations)
        info_idx, info_inv = cls._last_invocation_index(effective, {"get_project_info"})
        arrange_idx, _ = cls._last_invocation_index(effective, {"arrange_project_sections"})
        render_idx, _ = cls._last_invocation_index(effective, {"render_project"})
        review_idx, review_inv = cls._last_invocation_index(effective, {"review_audio"})

        if arrange_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: call "
                "`arrange_project_sections(total_bars=<brief bars>, pattern_bars=8, style=<genre>)` "
                "before final render/review/save so skill loops become a full "
                "intro/main/breakdown/final arrangement."
            )
        last_music_mutation = -1
        for i, inv in enumerate(effective):
            if inv.tool_name in _REAPER_MUTATION_TOOLS:
                last_music_mutation = i
        if last_music_mutation > arrange_idx:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: music changed after the last "
                "`arrange_project_sections` call. Arrange the final track form "
                "again before render/review/save."
            )

        if info_inv is None or info_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: call `get_project_info` once "
                "before final render/review/save so track count and note density "
                "can be checked."
            )
        stats = cls._parse_reaper_project_info(str(info_inv.result or ""))
        blockers: list[str] = []
        if stats["tracks"] < 5:
            blockers.append(f"only {stats['tracks']} tracks; add drums, bass, harmony, lead/pad, and arrangement role tracks")
        if stats["notes"] < 200:
            blockers.append(f"only {stats['notes']} notes; extend patterns across the full requested form")
        if blockers:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: REAPER project is too sparse "
                "for final render/review/save: "
                + "; ".join(blockers)
                + ". Use more role skills or add MIDI notes before proceeding."
            )

        if fn_name in {"review_audio", "save_project"} and render_idx is None:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: run `render_project` before "
                "`review_audio` or `save_project`."
            )
        if fn_name == "save_project":
            if review_inv is None or review_idx is None:
                return (
                    "Error: ARTIFACT_QUALITY_REQUIRED: run `review_audio` after "
                    "rendering, read the top fixes, and improve the project before save."
                )
            review_text = str(review_inv.result or "")
            if review_text.lower().startswith("error"):
                return (
                    "Error: ARTIFACT_QUALITY_REQUIRED: `review_audio` failed. "
                    "Fix the render path/review issue and rerun it before save."
                )
            overall = cls._parse_reaper_review_overall(review_text)
            if overall is not None and overall < 6.0:
                return (
                    f"Error: ARTIFACT_QUALITY_REQUIRED: `review_audio` overall "
                    f"is {overall:.1f}/10. Apply the listed fixes, re-render, "
                    "and review again before save."
                )
            arrangement = cls._parse_reaper_review_dimension(review_text, "Arrangement")
            if arrangement is not None and arrangement < 6.0:
                return (
                    f"Error: ARTIFACT_QUALITY_REQUIRED: `review_audio` Arrangement "
                    f"is {arrangement:.1f}/10. Call `arrange_project_sections` "
                    "or add section fills/drops, re-render, and review again before save."
                )
        return None

    def _artifact_quality_guard_message(
        self,
        fn_name: str,
        invocations: list[ToolInvocation],
        task: str,
    ) -> str | None:
        """Block final artifacts that are trace-valid but visibly too shallow.

        This guard is enabled only for with-skills runs. It does not reward tool
        calls directly; it forces the agent to use the skill path to produce
        artifact properties the evaluator can actually see/hear.
        """
        require_skill_path = bool(self._config.get("_require_skill_path"))
        domain = str(self._config.get("name") or self._config.get("domain") or "")
        if domain == "blender":
            return self._blender_quality_guard_message(
                fn_name,
                invocations,
                require_skill_path=require_skill_path,
            )
        if not require_skill_path:
            return None
        if domain == "web":
            return self._web_quality_guard_message(fn_name, invocations)
        if domain == "excel":
            return self._excel_quality_guard_message(fn_name, invocations, task)
        if domain == "reaper":
            return self._reaper_quality_guard_message(fn_name, invocations)
        return None

    def _skill_path_guard_message(
        self,
        fn_name: str,
        fn_args: dict[str, Any],
        invocations: list[ToolInvocation],
        task: str = "",
    ) -> str | None:
        """Return a corrective tool result if with-skills trace rules are unmet.

        This is deliberately runtime-enforced rather than prompt-only: old
        web/PPT traces looked like with-skills runs but bypassed the wiki path.
        The guard is enabled only when callers set `_require_skill_path`.
        """
        if not self._config.get("_require_skill_path"):
            return None

        domain = str(self._config.get("name") or self._config.get("domain") or "")
        if not domain:
            return None

        effective_invocations = self._effective_invocations(invocations)
        actual_tools = [inv.tool_name for inv in effective_invocations]
        actual_set = set(actual_tools)
        searched = bool(_SKILL_SEARCH_TOOLS & actual_set)
        current_run_discovered_ids = self._discovered_skill_ids(effective_invocations)
        current_run_inspected_ids = self._inspected_skill_ids(effective_invocations)
        current_run_selected_ids = (
            current_run_discovered_ids
            | self._claimed_provenance_skill_ids(domain, effective_invocations)
        )
        text_skill_ids = {
            str(inv.arguments.get("skill_id", "")).strip()
            for inv in effective_invocations
            if inv.tool_name in _SKILL_INSPECT_TEXT_TOOLS
            and isinstance(inv.arguments, dict)
            and str(inv.arguments.get("skill_id", "")).strip()
        }
        visual_skill_ids = {
            str(inv.arguments.get("skill_id", "")).strip()
            for inv in effective_invocations
            if inv.tool_name in _SKILL_VISUAL_TOOLS
            and self._visual_result_has_image(str(inv.result or ""))
            and isinstance(inv.arguments, dict)
            and str(inv.arguments.get("skill_id", "")).strip()
        }
        inspected_text = bool(text_skill_ids)
        inspected_visual = bool(visual_skill_ids)
        visual_pair_count = len(text_skill_ids & visual_skill_ids)
        min_visual_pairs = _MIN_VISUAL_SKILL_PAIRS_BY_DOMAIN.get(domain, 1)
        inspected_same_skill = visual_pair_count >= min_visual_pairs
        inspected = searched and inspected_same_skill

        primary_tools = _PRIMARY_SKILL_TOOLS_BY_DOMAIN.get(domain, set())
        primary_count = sum(1 for name in actual_tools if name in primary_tools)
        effective_skill_attempt_count = len(
            self._runtime_skill_ids(domain, effective_invocations)
        )

        inspection_tools = _TOOLS_REQUIRING_SKILL_INSPECTION.get(domain, set())
        if fn_name in inspection_tools and not inspected:
            if domain == "reaper" and fn_name == "apply_skill":
                skill_id = str(fn_args.get("skill_id", "")).strip()
                has_text_for_target = bool(skill_id and skill_id in text_skill_ids)
                if searched and has_text_for_target:
                    return None
            missing = []
            if not searched:
                missing.append("search_skills/list_skills")
            if not inspected_text:
                missing.append("get_skill_info/get_skill_text/get_skill_code")
            if not inspected_visual:
                missing.append("get_skill_visual")
            if inspected_text and inspected_visual and not inspected_same_skill:
                missing.append(
                    f"text/code/info and real visual image for at least "
                    f"{min_visual_pairs} same skill_id candidate(s) "
                    f"(current={visual_pair_count})"
                )
            return (
                "Error: SKILL_PATH_REQUIRED: with_skills must show task-matched "
                f"skill selection before `{fn_name}`. Missing: "
                f"{', '.join(missing)}. First browse for task-relevant skills, "
                "inspect the selected candidate's text/code/info and visual, then "
                f"retry `{fn_name}`."
            )

        runtime_ids = self._runtime_arg_skill_ids(domain, fn_name, fn_args)
        if runtime_ids:
            not_inspected, not_discovered = self._missing_current_run_ids(
                runtime_ids,
                discovered=current_run_discovered_ids,
                inspected=current_run_inspected_ids,
            )
            if not_inspected or not_discovered:
                missing_parts = []
                if not_discovered:
                    missing_parts.append(
                        "not returned by this run's search/list trace: "
                        + ", ".join(not_discovered)
                    )
                if not_inspected:
                    missing_parts.append(
                        "never inspected this run: " + ", ".join(not_inspected)
                    )
                return (
                    "Error: SKILL_PATH_REQUIRED: fabricated_provenance: "
                    f"`{fn_name}` names skill id(s) that were not selected and "
                    "inspected in the current run. "
                    + "; ".join(missing_parts)
                    + ". Search/list the task-relevant skill, inspect it with "
                    "get_skill_text/get_skill_code/get_skill_visual/get_skill_info, "
                    f"then retry `{fn_name}`."
                )

        if domain == "ppt" and fn_name == "add_slide_from_shell":
            if not self._has_nonempty_ppt_reference_ids(fn_args):
                return (
                    "Error: SKILL_PATH_REQUIRED: add_slide_from_shell must include "
                    "`design_reference_skill_ids` containing at least 2 distinct "
                    "long-tail wiki skills inspected with get_skill_text/"
                    "get_skill_code/get_skill_visual. Retry with those ids so "
                    "deck-plan.json and slide notes preserve the audit trace."
                )

        primitive_tools = _GROUNDED_PRIMITIVE_TOOLS_BY_DOMAIN.get(domain, set())
        if fn_name in primitive_tools:
            from_skill_ids = self._provenance_skill_ids_from_args(fn_args)
            target_nodes = self._grounding_targets_for_call(
                domain, fn_name, fn_args, len(effective_invocations)
            )
            explicit_target = bool(
                self._coerce_target_nodes(
                    fn_args.get("target_node") or fn_args.get("target_nodes")
                )
            )
            adaptation_notes = str(fn_args.get("adaptation_notes", "") or "").strip()
            if not from_skill_ids:
                return (
                    "Error: SKILL_PATH_REQUIRED: manual generation tool "
                    f"`{fn_name}` must include non-empty `from_skill_ids` naming "
                    "the inspected wiki skill(s) whose text/code/visual patterns "
                    "the generated code adapts."
                )
            not_inspected, not_discovered = self._missing_current_run_ids(
                from_skill_ids,
                discovered=current_run_selected_ids,
                inspected=current_run_inspected_ids,
            )
            if not_inspected or not_discovered:
                missing_parts = []
                if not_discovered:
                    missing_parts.append(
                        "not returned by this run's search/list trace or "
                        "prior runtime selection trace: "
                        + ", ".join(not_discovered)
                    )
                if not_inspected:
                    missing_parts.append(
                        "never inspected this run: " + ", ".join(not_inspected)
                    )
                return (
                    "Error: SKILL_PATH_REQUIRED: fabricated_provenance: "
                    f"`from_skill_ids` on `{fn_name}` must be a subset of skills "
                    "selected and inspected in this run. "
                    + "; ".join(missing_parts)
                )
            if not explicit_target or not target_nodes:
                return (
                    "Error: SKILL_PATH_REQUIRED: manual generation tool "
                    f"`{fn_name}` must include `target_node` (or JSON/list "
                    "`target_nodes`) naming the concrete section/role being "
                    "adapted, e.g. nav, hero, dashboard_layout, lighting, bass."
                )
            if not adaptation_notes:
                return (
                    "Error: SKILL_PATH_REQUIRED: manual generation tool "
                    f"`{fn_name}` must include `adaptation_notes` explaining the "
                    "specific mechanisms borrowed from `from_skill_ids`."
                )

        manual_tools = _MANUAL_TOOLS_REQUIRING_SKILL_ATTEMPT.get(domain, set())
        final_ground_tools = _FINAL_TOOLS_REQUIRING_GROUNDED_SECTIONS.get(domain, set())
        if (
            fn_name in manual_tools
            and fn_name not in primitive_tools
            and fn_name not in final_ground_tools
            and primary_count < 1
        ):
            return (
                "Error: SKILL_PATH_REQUIRED: manual construction/repair tools are "
                f"locked in with_skills until after one real domain skill attempt. "
                f"Call a task-matched runtime skill tool first: "
                f"{', '.join(sorted(primary_tools)) or 'apply_skill'}, then retry "
                f"`{fn_name}` if repair is still needed."
            )

        final_tools = _FINAL_TOOLS_REQUIRING_GROUNDED_SECTIONS.get(domain, set())
        if fn_name in final_tools:
            if domain == "reaper" and not inspected_visual:
                return (
                    "Error: SKILL_PATH_REQUIRED: before final render/review/save, "
                    "inspect at least one task-relevant audio skill with "
                    "`get_skill_visual` that returns an image. REAPER skills may "
                    "be applied from text/code even when a specific skill has no "
                    "visual, but the with_skills trace must still include one "
                    "multimodal reference."
                )
            claimed_ids = sorted(
                self._claimed_provenance_skill_ids(domain, effective_invocations)
            )
            if claimed_ids:
                # Composer/runtime tools can select ids internally after the
                # model has already performed its task-level search. Treat the
                # tool result itself as the current-run selection trace, but
                # still require every claimed wiki id to be inspected before
                # final save/render.
                not_inspected = [
                    sid for sid in claimed_ids
                    if sid not in current_run_inspected_ids
                ]
                if not_inspected:
                    return (
                        "Error: SKILL_PATH_REQUIRED: fabricated_provenance: "
                        "the current artifact trace claims wiki skill id(s) "
                        "that were never inspected in this run: "
                        + ", ".join(not_inspected)
                        + ". For schema/composer-selected ids, inspect each "
                        "exact id with get_skill_text/get_skill_code/"
                        "get_skill_info and get_skill_visual, "
                        f"then retry `{fn_name}`."
                    )
            min_count = _MIN_GROUNDED_SECTIONS_BY_DOMAIN.get(
                domain,
                _MIN_FINAL_SKILL_ATTEMPTS_BY_DOMAIN.get(domain, 1),
            )
            if domain == "ppt":
                requested_slides = _requested_slide_count(task)
                if requested_slides:
                    # Do not force a deck to add appendix slides only to satisfy
                    # the global 16-section target when the brief explicitly
                    # requests a smaller deck. In that case every requested
                    # slide must still carry inspected skill provenance.
                    min_count = min(min_count, requested_slides)
            grounded_sections = self._grounded_sections(domain, effective_invocations)
            grounded_count = len(grounded_sections)
            if grounded_count < min_count:
                return (
                    "Error: SKILL_PATH_REQUIRED: this final/review tool is locked "
                    f"until at least {min_count} grounded section(s)/role(s) "
                    "have traceable skill provenance. Current grounded count: "
                    f"{grounded_count}. For manual code/write tools, pass "
                    "`from_skill_ids`, `target_node`, and `adaptation_notes`; "
                    "for runtime skill tools, inspect the exact skill ids first."
                )

        return None

    def _retrieve_skills(
        self, task: str, library_dir: Path
    ) -> list[tuple[str, str, list[dict]]]:
        """Select skills from library index via LLM, then load full details.

        Returns list of (skill_name, analysis_markdown, frames) tuples.
        """
        try:
            from core.skill_store import get_skill
            from core.skill_retriever import extract_summary

            index_path = library_dir / "index.json"
            if not index_path.exists():
                log.warning("No skill index at %s", index_path)
                return []

            index_data = json.loads(index_path.read_text("utf-8"))
            skills_list = index_data.get("skills", [])
            if not skills_list:
                return []

            # Build a concise menu of available skills for LLM selection
            menu_lines = []
            for i, s in enumerate(skills_list, 1):
                sid = s["skill_id"]
                name = s.get("skill_name", sid)
                cat = s.get("category", "?")
                title = s.get("source_title", "")
                # Load a short summary if available
                full = get_skill(library_dir, sid)
                summary = ""
                if full and full.get("analysis"):
                    summary = extract_summary(
                        full["analysis"],
                        skill_name=name,
                    )[:200]
                menu_lines.append(
                    f"{i}. [{cat}] {name} (id: {sid})"
                    + (f"\n   Source: {title}" if title else "")
                    + (f"\n   Summary: {summary}" if summary else "")
                )

            menu = "\n".join(menu_lines)
            n = min(self._n_skills, len(skills_list))

            # Ask LLM to select
            select_prompt = (
                f"Task: {task}\n\n"
                f"Available skills ({len(skills_list)} total):\n{menu}\n\n"
                f"Pick the {n} most relevant skill(s) for this task. "
                f"Output ONLY a JSON array of skill_id strings, e.g. "
                f'["skill_id_1", "skill_id_2"]. If none are relevant, output [].'
            )

            try:
                resp = call_azure_openai(
                    [{"role": "user", "content": select_prompt}],
                    model=self._model,
                    reasoning_effort="low",
                )
                import re as _re
                text = resp.get("content", "")
                m = _re.search(r"\[.*?\]", text, _re.DOTALL)
                if m:
                    selected_ids = json.loads(m.group())
                else:
                    selected_ids = []
            except Exception as e:
                log.warning("LLM skill selection failed: %s, falling back to first %d", e, n)
                selected_ids = [s["skill_id"] for s in skills_list[:n]]

            if not selected_ids:
                log.info("LLM selected no skills for task: %s", task)
                return []

            # Load full analyses for selected skills
            analyses = []
            for sid in selected_ids[:n]:
                full = get_skill(library_dir, sid)
                if full and full.get("analysis"):
                    # Resolve frame paths from the skill's directory
                    frames = full.get("frames", [])
                    skill_dir = Path(full.get("_skill_dir", ""))
                    resolved_frames = []
                    for f in frames:
                        frame_path = skill_dir / f["path"]
                        if frame_path.exists():
                            resolved_frames.append({
                                **f,
                                "abs_path": str(frame_path),
                            })
                    analyses.append((
                        full.get("skill_name", sid),
                        full["analysis"],
                        resolved_frames,
                    ))

            log.info(
                "LLM selected %d skill(s): %s",
                len(analyses),
                [a[0] for a in analyses],
            )
            return analyses

        except Exception as e:
            log.warning("Skill selection failed (continuing without skills): %s", e)
            return []

    async def _run_with_mcp(
        self,
        task: str,
        skill_analyses: list[tuple[str, str]],
    ) -> AgentResult:
        """Run with a live MCP connection."""
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
        except ImportError:
            return AgentResult(
                task=task, success=False, iterations=0,
                error="mcp package not installed. Run: pip install mcp",
            )

        server_params = _build_server_params(StdioServerParameters, self._mcp_cfg)
        completed_result: AgentResult | None = None

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    log.info("MCP server connected")

                    spawn_wait = self._mcp_cfg.get("spawn_wait", 6)
                    if spawn_wait > 0:
                        log.info("Waiting %ds for bot to spawn...", spawn_wait)
                        await asyncio.sleep(spawn_wait)

                    # Get tool schemas dynamically
                    openai_tools = await get_tools_from_mcp(session)

                    # Filter out disabled tools (for benchmark conditions)
                    disabled = self._config.get("_disabled_tools")
                    if disabled:
                        before = len(openai_tools)
                        openai_tools = [
                            t for t in openai_tools
                            if t["function"]["name"] not in disabled
                        ]
                        log.info(
                            "Filtered tools: %d → %d (disabled: %s)",
                            before, len(openai_tools), disabled,
                        )

                    invocations: list[ToolInvocation] = []
                    mcp = _MCPWrapper(session, invocations)

                    completed_result = await self._run_loop(
                        task, skill_analyses,
                        mcp_wrapper=mcp,
                        openai_tools=openai_tools,
                        invocations=invocations,
                    )
                    return completed_result

        except Exception as exc:
            if completed_result is not None:
                cleanup_note = (
                    f"MCP connection emitted a cleanup/stdio warning after "
                    f"agent loop completion: {exc}"
                )
                completed_result.note = (
                    f"{completed_result.note}\n{cleanup_note}"
                    if completed_result.note else cleanup_note
                )
                log.warning(cleanup_note)
                return completed_result
            log.exception("MCP connection failed before agent loop completion")
            return AgentResult(
                task=task, success=False, iterations=0,
                error=f"MCP connection failed: {exc}",
            )

    async def _run_loop(
        self,
        task: str,
        skill_analyses: list[tuple[str, str]],
        *,
        mcp_wrapper,
        openai_tools: list[dict],
        invocations: list[ToolInvocation] | None = None,
    ) -> AgentResult:
        """The core agent loop."""
        if invocations is None:
            invocations = []

        # For dry-run, create a mock wrapper
        if mcp_wrapper is None:
            mcp_wrapper = _DryRunMCPWrapper(
                invocations,
                placeholders=self._config.get("dry_run_placeholders", {}),
            )

        # Load domain-specific hooks (if any)
        verify_hook = self._load_verify_hook()
        progress_hook = self._load_progress_hook()

        # Build system prompt
        system_prompt = _build_system_prompt(self._config, skill_analyses)

        # Initial user message from domain config
        initial_prompt = self._config.get(
            "agent_initial_prompt",
            "Execute the task step by step.",
        )

        messages: list[dict] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {task}\n\n{initial_prompt}"},
        ]

        # Inject reference frames as a vision message if available
        all_frames = []
        for _, _, frames in skill_analyses:
            all_frames.extend(frames)
        if all_frames:
            import base64
            vision_content: list[dict] = [
                {"type": "text", "text": (
                    "Reference images from the tutorial video. These show what the "
                    "build should look like at each stage. Match your build to these:"
                )},
            ]
            for f in all_frames[:8]:
                abs_path = f.get("abs_path", "")
                if abs_path and Path(abs_path).exists():
                    img_data = Path(abs_path).read_bytes()
                    b64 = base64.b64encode(img_data).decode()
                    vision_content.append({
                        "type": "text",
                        "text": f"Stage: {f.get('description', '?')} (t={f.get('seconds', '?')}s)",
                    })
                    vision_content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    })
            if len(vision_content) > 1:
                messages.append({"role": "user", "content": vision_content})
                log.info("Injected %d reference frame(s) as vision", len(all_frames))

        consecutive_no_tool = 0
        consecutive_errors = 0
        iteration = 0

        # Stuck-loop detection state
        recent_calls: deque[tuple] = deque(maxlen=10)
        stuck_count = 0
        consecutive_soft_errors = 0
        deadline_nudge_sent = False

        for iteration in range(1, self._max_iter + 1):
            log.info("=== Iteration %d/%d ===", iteration, self._max_iter)

            deadline_nudge = self._config.get("deadline_nudge")
            if deadline_nudge and not deadline_nudge_sent:
                try:
                    remaining_threshold = int(
                        self._config.get("deadline_nudge_remaining", 5)
                    )
                except Exception:
                    remaining_threshold = 5
                remaining = self._max_iter - iteration + 1
                if remaining <= max(1, remaining_threshold):
                    try:
                        nudge_text = str(deadline_nudge).format(
                            iteration=iteration,
                            max_iter=self._max_iter,
                            remaining=remaining,
                        )
                    except Exception:
                        nudge_text = str(deadline_nudge)
                    messages.append({"role": "user", "content": nudge_text})
                    deadline_nudge_sent = True

            # Call GPT-5.4
            try:
                tool_choice = None
                if (
                    openai_tools
                    and self._config.get("force_tool_after_no_tool")
                    and consecutive_no_tool > 0
                ):
                    tool_choice = "required"
                    forced_sequence = self._config.get("force_tool_sequence_after_no_tool") or []
                    if forced_sequence:
                        used_ok = {
                            inv.tool_name
                            for inv in invocations
                            if not inv.error
                        }
                        for tool_name in forced_sequence:
                            if tool_name not in used_ok:
                                tool_choice = {
                                    "type": "function",
                                    "function": {"name": tool_name},
                                }
                                break
                response_msg = call_azure_openai(
                    messages,
                    tools=openai_tools,
                    model=self._model,
                    reasoning_effort=self._reasoning,
                    max_completion_tokens=16384,
                    max_retries=10,
                    retry_delay=20.0,
                    timeout=300,
                    tool_choice=tool_choice,
                )
            except LLMError as e:
                return AgentResult(
                    task=task, success=False, iterations=iteration,
                    tool_calls=invocations, conversation=messages,
                    error=f"LLM call failed: {e}",
                )

            # Append assistant response to conversation
            messages.append(response_msg)

            content = response_msg.get("content") or ""
            tool_calls_list = response_msg.get("tool_calls") or []

            # Check for an explicit TASK_COMPLETE marker. Do not terminate on
            # planning prose that merely mentions the marker as a future step.
            if _declares_task_complete(content) and not tool_calls_list:
                log.info("Agent declared TASK_COMPLETE at iteration %d", iteration)
                return AgentResult(
                    task=task, success=True, iterations=iteration,
                    tool_calls=invocations, conversation=messages,
                    final_message=content,
                    note=f"Completed in {iteration} iterations, {len(invocations)} tool calls",
                )

            # No tool calls and no TASK_COMPLETE — model might be stuck
            if not tool_calls_list:
                consecutive_no_tool += 1
                log.warning("No tool calls in response (consecutive: %d)", consecutive_no_tool)
                if consecutive_no_tool >= 8:
                    return AgentResult(
                        task=task, success=False, iterations=iteration,
                        tool_calls=invocations, conversation=messages,
                        final_message=content,
                        error="Agent stuck: 8 consecutive responses without tool calls",
                    )
                # Escalating, domain-aware nudges to unstick the model.
                # Domains can override `stuck_nudge` and `stuck_nudge_late`
                # via domain.yaml; otherwise generic instructions apply.
                domain_name = self._config.get("name", "")
                if consecutive_no_tool <= 2:
                    nudge = self._config.get(
                        "stuck_nudge",
                        "Continue with your next tool call, or say TASK_COMPLETE if done.",
                    )
                else:
                    domain_late_hints = {
                        "ppt": (
                            "Call add_slide_from_shell for the next planned slide, "
                            "or save_presentation if all target slides are built. "
                            "IGNORE visual QA suggestions — finishing the deck "
                            "matters more than perfecting any one slide."
                        ),
                        "excel": (
                            "Call execute_xlsx_code with from_skill_ids, target_node, "
                            "and adaptation_notes to populate the next sheet, "
                            "or save_workbook + verify_workbook if all sheets are built. "
                            "If you don't have a workbook_id yet, call create_workbook first."
                        ),
                        "web": (
                            "Call write_file with from_skill_ids, target_node, and "
                            "adaptation_notes to add the next section/style, "
                            "or save_project if the page is complete. "
                            "DO NOT skip save_project — files in /tmp will be lost."
                        ),
                        "blender": (
                            "Call execute_blender_code with from_skill_ids, target_node, "
                            "and adaptation_notes to add the next object/light/material, "
                            "or render_scene if the scene is set up."
                        ),
                        "reaper": (
                            "Call execute_reaper_code with from_skill_ids, target_node, "
                            "and adaptation_notes for the next grounded musical role, "
                            "or render_project if all tracks are arranged. "
                            "STOP calling get_project_info — render now."
                        ),
                    }
                    nudge = self._config.get(
                        "stuck_nudge_late",
                        domain_late_hints.get(
                            domain_name,
                            "You must make a tool call now. If the artifact is "
                            "in a savable state, call the save tool. Otherwise "
                            "call the next building tool.",
                        ),
                    )
                messages.append({"role": "user", "content": nudge})
                continue

            consecutive_no_tool = 0

            # Execute each tool call
            pending_image_messages: list[dict] = []
            for tc in tool_calls_list:
                fn_name = tc["function"]["name"]
                try:
                    fn_args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError:
                    fn_args = {}

                log.info("Tool call: %s(%s)", fn_name, fn_args)

                guard_blocked = False
                try:
                    guard_msg = self._skill_path_guard_message(
                        fn_name, fn_args, invocations, task
                    )
                    guard_error = _SKILL_PATH_GUARD_ERROR
                    if not guard_msg:
                        guard_msg = self._artifact_quality_guard_message(
                            fn_name, invocations, task
                        )
                        guard_error = _ARTIFACT_QUALITY_GUARD_ERROR
                    if guard_msg:
                        guard_blocked = True
                        result_text = guard_msg
                        consecutive_errors = 0
                        invocations.append(ToolInvocation(
                            tool_name=fn_name,
                            arguments=fn_args,
                            result=result_text,
                            error=guard_error,
                        ))
                        log.info("Guard %s blocked %s", guard_error, fn_name)
                    else:
                        result_text = await mcp_wrapper.call_tool(fn_name, fn_args)
                        consecutive_errors = 0
                except Exception as e:
                    result_text = f"Error: {e}"
                    consecutive_errors += 1
                    log.warning("Tool call error (%d consecutive): %s", consecutive_errors, e)

                # --flat-skills: strip wiki organization metadata (categories,
                # tags, archetypes) from skill listing/info results so the
                # agent can only see skill_id + brief description.
                if self._config.get("_flat_skills_mode") and result_text:
                    try:
                        result_text = _flatten_skill_tool_result(fn_name, result_text)
                    except Exception as e:
                        log.warning("flat-skills postprocess failed for %s: %s", fn_name, e)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result_text or "ok",
                })

                # If the tool result advertises an image (e.g. get_skill_visual
                # returns {"_image_attachment": "<abs path>"}), follow up with a
                # vision message so the LLM actually SEES the image. Plumbing
                # the base64 directly into the tool result would bloat context
                # by ~130KB per call; this side-channel keeps the tool message
                # compact and only attaches the image once.
                _attach_path = self._extract_image_attachment(result_text or "")
                if _attach_path is not None:
                    try:
                        from pathlib import Path as _Path
                        import base64 as _b64
                        p = _Path(_attach_path)
                        if p.is_file() and p.stat().st_size < 5 * 1024 * 1024:
                            ext = p.suffix.lstrip(".").lower()
                            mime = {"jpg": "jpeg", "jpeg": "jpeg",
                                    "png": "png", "webp": "webp",
                                    "gif": "gif"}.get(ext, "jpeg")
                            b64 = _b64.b64encode(p.read_bytes()).decode("ascii")
                            pending_image_messages.append({
                                "role": "user",
                                "content": [
                                    {"type": "text", "text":
                                     f"[image attachment from {fn_name}: {p.name}]"},
                                    {"type": "image_url",
                                     "image_url": {"url": f"data:image/{mime};base64,{b64}"}},
                                ],
                            })
                            log.info("Attached image %s (%d bytes) from %s",
                                     p.name, p.stat().st_size, fn_name)
                    except Exception as _ae:
                        log.warning("image attach failed: %s", _ae)

                # --- Stuck-loop detection ---
                call_sig = (
                    fn_name,
                    hash(json.dumps(fn_args, sort_keys=True)),
                    hash(result_text or ""),
                )
                recent_calls.append(call_sig)

                # Track soft failures (tool returns failure text, not exception)
                if self._is_failure_result(result_text or ""):
                    consecutive_soft_errors += 1
                elif "Error:" not in (result_text or ""):
                    consecutive_soft_errors = 0

                # Detect repeated identical failing calls
                k = self._max_repeated
                if len(recent_calls) >= k:
                    last_k = list(recent_calls)[-k:]
                    if all(c == last_k[0] for c in last_k):
                        is_failing = self._is_failure_result(result_text or "")
                        # If failure_patterns configured, require match; else flag any duplicate
                        if is_failing or not self._failure_patterns:
                            stuck_count += 1
                            log.warning(
                                "Stuck-loop detected (%d): %s repeated %d times",
                                stuck_count, fn_name, k,
                            )
                            messages.append({
                                "role": "user",
                                "content": (
                                    f"STUCK DETECTED: You called {fn_name} with the same "
                                    f"arguments {k} times and it keeps returning: "
                                    f"'{(result_text or '')[:200]}'. "
                                    "You MUST try a different approach. "
                                    "Do NOT repeat the same call."
                                ),
                            })
                            if stuck_count >= 3:
                                return AgentResult(
                                    task=task, success=False, iterations=iteration,
                                    tool_calls=invocations, conversation=messages,
                                    error=f"Agent stuck in failure loop (ignored {stuck_count} warnings)",
                                )

                # Auto-reflection via domain hook
                if verify_hook and not guard_blocked:
                    verify_msg = await verify_hook(
                        fn_name, fn_args, result_text, mcp_wrapper
                    )
                    if verify_msg:
                        log.info("Auto-verify: %s", verify_msg)
                        # Record feedback on the tool invocation for logging
                        if invocations:
                            invocations[-1].verify_feedback = verify_msg
                        messages.append({
                            "role": "user",
                            "content": verify_msg,
                        })

            # Keep function-call protocol valid: all tool_call responses for
            # the assistant turn must appear before any non-tool follow-up
            # messages. Vision attachments are therefore appended after the
            # whole tool-call batch, not interleaved between tool results.
            if pending_image_messages:
                messages.extend(pending_image_messages)

            if consecutive_errors >= self._max_errors:
                return AgentResult(
                    task=task, success=False, iterations=iteration,
                    tool_calls=invocations, conversation=messages,
                    error=f"Too many consecutive errors ({consecutive_errors})",
                )

            if consecutive_soft_errors >= self._max_errors * 2:
                return AgentResult(
                    task=task, success=False, iterations=iteration,
                    tool_calls=invocations, conversation=messages,
                    error=f"Too many consecutive tool failures ({consecutive_soft_errors})",
                )

            # Progress check every 10 iterations
            if iteration > 0 and iteration % 10 == 0:
                recent_invocations = invocations[-20:]
                recent_failures = sum(
                    1 for inv in recent_invocations
                    if self._is_failure_result(inv.result) or inv.error
                )

                progress_parts = [
                    f"Progress check at iteration {iteration}/{self._max_iter}:",
                    f"- {len(invocations)} tool calls total, "
                    f"{recent_failures} failures in last {len(recent_invocations)} calls.",
                ]

                # Call domain-specific progress hook if available
                if progress_hook:
                    try:
                        extra = await progress_hook(
                            mcp_wrapper, invocations, iteration
                        )
                        if extra:
                            progress_parts.append(extra)
                    except Exception as e:
                        log.warning("progress_check hook failed: %s", e)

                progress_parts.append(
                    "Assess what you have accomplished so far, what remains, "
                    "and whether your current approach is working. "
                    "If stuck or making no progress, change strategy. "
                    "Say TASK_COMPLETE if the task is done."
                )

                messages.append({
                    "role": "user",
                    "content": "\n".join(progress_parts),
                })

        # Max iterations reached
        return AgentResult(
            task=task, success=False, iterations=iteration,
            tool_calls=invocations, conversation=messages,
            final_message=content if 'content' in dir() else "",
            note=f"Max iterations ({self._max_iter}) reached",
        )


# ---------------------------------------------------------------------------
# Synchronous convenience wrapper
# ---------------------------------------------------------------------------

def run_agent(
    task: str,
    domain_config: dict,
    library_dir: Path,
    brand: str | None = None,
    **kwargs,
) -> AgentResult:
    """
    Synchronous entry point for the agent loop.

    Args:
        task: Natural language task description.
        domain_config: Loaded domain config (from core.load_domain).
        library_dir: Path to skill library directory.
        **kwargs: Passed to AgentExecutor (model, reasoning_effort, etc.).

    Returns:
        AgentResult with conversation log and tool call history.
    """
    if brand:
        log.info("brand active: %s", brand)
        domain_config = dict(domain_config)
        domain_config.setdefault("_active_brand", brand)
    executor = AgentExecutor(domain_config, **kwargs)
    return asyncio.run(executor.run(task, library_dir))
