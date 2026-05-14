"""
domains/excel/agent_hooks.py

Hooks invoked by core/agent_executor.py during the agent loop.

- auto_verify(tool_name, tool_args, result_text, mcp)
    Called after every successful tool call. Returns either None (no
    correction needed) or a short string the agent should treat as a
    correction nudge appended to its next user turn.

- progress_check(mcp, invocations, iteration)
    Called every 10 iterations. Returns a one-paragraph status report
    summarizing the workbook (sheets, charts, recent failures).
"""
from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path safety helper (mirrors xlsx_engine.safe_demo_path but standalone so
# hooks have no import dependency on the MCP server)
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEMO_ROOT = (_PROJECT_ROOT / "demo" / "excel").resolve()
_SHELL_METACHARS = re.compile(r"[;|&$`<>]")


def _is_path_safe(filepath: str) -> tuple[bool, str]:
    """Return (ok, reason) for a filepath argument."""
    if not filepath:
        return True, ""
    if _SHELL_METACHARS.search(filepath):
        return False, "shell metacharacters"
    candidate = Path(filepath)
    if not candidate.is_absolute():
        candidate = _DEMO_ROOT / candidate.name
    try:
        resolved = Path(os.path.realpath(candidate))
        resolved.relative_to(_DEMO_ROOT)
    except Exception:
        return False, f"resolves outside {_DEMO_ROOT}"
    return True, ""


# ---------------------------------------------------------------------------
# Result parsing (tools return JSON-encoded payloads or "Error: ..." strings)
# ---------------------------------------------------------------------------

def _parse_result(result_text: str) -> dict | None:
    """Try to parse the tool result as JSON. Returns dict or None."""
    if not isinstance(result_text, str):
        return None
    s = result_text.strip()
    if not s.startswith("{") and not s.startswith("["):
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def _is_error_result(result_text: str) -> bool:
    if not isinstance(result_text, str):
        return False
    if result_text.startswith("Error:"):
        return True
    parsed = _parse_result(result_text)
    if isinstance(parsed, dict) and parsed.get("ok") is False:
        return True
    return False


# ---------------------------------------------------------------------------
# auto_verify
# ---------------------------------------------------------------------------

_VERIFY_TOOLS = {
    "create_workbook", "save_workbook", "init_from_archetype",
    "add_sheet_from_shell", "apply_component", "execute_xlsx_code",
    "verify_workbook",
}


async def auto_verify(tool_name: str, tool_args: dict, result_text: str, mcp):
    """Inspect the tool call and return a correction string if something
    looks off, otherwise None.

    The hook is fast and stateless: it does not call back into the MCP
    except in the verify_workbook branch where the agent's own follow-up
    will already have done so.
    """
    if tool_name not in _VERIFY_TOOLS:
        return None

    # 1. Path safety on every argument named filepath
    fp = tool_args.get("filepath") if isinstance(tool_args, dict) else None
    if fp:
        ok, reason = _is_path_safe(str(fp))
        if not ok:
            return (
                f"Path safety: {tool_name} was called with filepath={fp!r} "
                f"({reason}). All Excel outputs must live under "
                f"demo/excel/. Choose a path like demo/excel/<task_name>.xlsx."
            )

    # 2. Generic error detection
    if _is_error_result(result_text):
        if tool_name == "execute_xlsx_code":
            return (
                "execute_xlsx_code returned an error. Read the traceback in "
                "the result, fix the openpyxl call, and retry. Common causes: "
                "missing import (use the pre-injected names), wrong attribute "
                "(e.g. PatternFill needs fgColor= and fill_type='solid' or pass "
                "type 'solid' positionally), out-of-range cell reference."
            )
        if tool_name == "init_from_archetype":
            archetype = tool_args.get("archetype_id", "?") if isinstance(tool_args, dict) else "?"
            return (
                f"init_from_archetype failed for {archetype!r}. "
                "Confirm the archetype_id with list_skills(tier='archetype'), "
                "then retry with kwargs_json that matches the archetype's expected "
                "keys (title, period, theme, etc.)."
            )
        if tool_name == "add_sheet_from_shell":
            shell = tool_args.get("shell_id", "?") if isinstance(tool_args, dict) else "?"
            return (
                f"add_sheet_from_shell failed for shell {shell!r}. "
                "Use list_skills(tier='sheet_shell') to see valid shell_ids "
                "and get_skill_code(<shell_id>) to inspect required kwargs."
            )
        if tool_name == "apply_component":
            comp = tool_args.get("component_id", "?") if isinstance(tool_args, dict) else "?"
            return (
                f"apply_component failed for component {comp!r}. "
                "Check list_skills(tier='component') for valid IDs and "
                "get_skill_code(<component_id>) for the kwargs the render() "
                "function expects."
            )
        return f"{tool_name} returned an error. Inspect the message and retry with corrected arguments."

    # 3. verify_workbook structural checks
    if tool_name == "verify_workbook":
        parsed = _parse_result(result_text)
        if not isinstance(parsed, dict):
            return None
        if not parsed.get("ok"):
            return f"verify_workbook reports ok=false: {parsed.get('error', 'unknown error')}."
        warnings = parsed.get("warnings", []) or []
        sheets = parsed.get("sheets", []) or []
        empty_sheets = [s["name"] for s in sheets
                        if s.get("non_empty_rows", 0) == 0]
        no_chart = all((s.get("charts", 0) == 0) for s in sheets)
        msgs = []
        if warnings:
            msgs.append("warnings: " + "; ".join(warnings))
        if empty_sheets:
            msgs.append(f"empty sheets: {empty_sheets}")
        if no_chart and len(sheets) > 1:
            msgs.append("no charts on any sheet — consider adding compare_chart")
        if msgs:
            return ("verify_workbook surfaced issues — "
                    + "; ".join(msgs)
                    + ". Fix these before saying TASK_COMPLETE.")

    # 4. save_workbook sanity: filepath should end in .xlsx
    if tool_name == "save_workbook":
        parsed = _parse_result(result_text)
        if isinstance(parsed, dict):
            saved_fp = parsed.get("filepath", "")
            if saved_fp and not saved_fp.endswith(".xlsx"):
                return (
                    f"save_workbook produced {saved_fp!r} which is not an "
                    ".xlsx file. Re-save with a .xlsx extension."
                )
            sheets = parsed.get("sheets", [])
            if not sheets:
                return "save_workbook returned 0 sheets — the workbook has no content. Add a shell or run init_from_archetype before saving."

    return None


# ---------------------------------------------------------------------------
# progress_check
# ---------------------------------------------------------------------------

async def progress_check(mcp, invocations, iteration):
    """Return a short status string describing workbook health."""
    invocations = invocations or []
    by_tool = Counter(inv.tool_name for inv in invocations)
    failures = [inv for inv in invocations if not getattr(inv, "success", True)]

    create_calls = [inv for inv in invocations
                    if inv.tool_name == "create_workbook" and getattr(inv, "success", True)]
    save_calls = [inv for inv in invocations
                  if inv.tool_name == "save_workbook" and getattr(inv, "success", True)]
    archetype_calls = [inv for inv in invocations
                       if inv.tool_name == "init_from_archetype" and getattr(inv, "success", True)]
    shell_calls = [inv for inv in invocations
                   if inv.tool_name == "add_sheet_from_shell" and getattr(inv, "success", True)]
    component_calls = [inv for inv in invocations
                       if inv.tool_name == "apply_component" and getattr(inv, "success", True)]
    code_calls = [inv for inv in invocations
                  if inv.tool_name == "execute_xlsx_code" and getattr(inv, "success", True)]

    parts = [
        f"iteration {iteration}",
        f"workbooks created: {len(create_calls)}",
        f"saves: {len(save_calls)}",
    ]
    if archetype_calls:
        parts.append(f"archetype calls: {len(archetype_calls)}")
    if shell_calls:
        parts.append(f"shell calls: {len(shell_calls)}")
    if component_calls:
        parts.append(f"component calls: {len(component_calls)}")
    if code_calls:
        parts.append(f"execute_xlsx_code calls: {len(code_calls)}")
    if failures:
        recent_failures = failures[-3:]
        parts.append(
            "recent failures: "
            + "; ".join(f"{f.tool_name}({getattr(f, 'error', '?')[:60]})"
                        for f in recent_failures)
        )

    if save_calls and not any(inv.tool_name == "verify_workbook"
                              for inv in invocations):
        parts.append("WARNING: workbook was saved but never verified — "
                     "call verify_workbook before TASK_COMPLETE.")

    return " | ".join(parts)
