"""
domains/reaper/mcp_server/reaper_engine.py
REAPER skill execution engine — wraps ReaScript code for execution.

Skills are stored as def create_pattern(...) functions. This engine:
  1. Extracts code from skill analysis
  2. Wraps it for execution in REAPER via ReaScript
  3. Returns track/item names created
"""
from __future__ import annotations

import json
import re
from pathlib import Path


def extract_code_from_analysis(analysis: str) -> str:
    """Extract the first Python code block from a skill analysis Markdown."""
    pattern = r"```python\s*\n(.*?)```"
    m = re.search(pattern, analysis, re.DOTALL)
    return m.group(1).strip() if m else ""


def get_skill_detail(
    skills_dir: Path, skill_id: str, index: list[dict]
) -> dict | None:
    """Load full skill detail JSON for a given skill_id."""
    entry = None
    for s in index:
        if s.get("skill_id") == skill_id:
            entry = s
            break
    if entry is None:
        return None

    detail_path = skills_dir / entry["detail_path"]
    if not detail_path.exists():
        return None

    return json.loads(detail_path.read_text(encoding="utf-8"))


def wrap_skill_for_reaper(
    code: str,
    params: dict | None = None,
) -> str:
    """Wrap a skill's create_pattern() code for execution in REAPER.

    Returns a self-contained Python script string that:
    1. Defines the skill's functions
    2. Calls create_pattern() with given params
    3. Prints the names of created tracks for parsing
    """
    params = params or {}

    # Build the param overrides as Python code.
    param_lines = []
    for k, v in params.items():
        param_lines.append(f"    {k}={repr(v)},")
    param_str = "\n".join(param_lines) if param_lines else ""

    wrapper = f"""
# --- Skill code start ---
{code}
# --- Skill code end ---

# Call create_pattern with params.
try:
    result = create_pattern(
{param_str}
    )
    print(f"SKILL_RESULT: {{result}}")
except Exception as e:
    print(f"SKILL_ERROR: {{type(e).__name__}}: {{e}}")
    result = None
"""
    return wrapper


def parse_skill_result(result_text: str) -> tuple[bool, list[str]]:
    """Parse the output from a wrapped skill execution.

    Returns:
        (success: bool, track_names: list[str])
    """
    if "SKILL_ERROR:" in result_text:
        return False, [result_text]

    m = re.search(r"SKILL_CREATED:\s*(.+)", result_text)
    if m:
        names_str = m.group(1).strip()
        if names_str == "(none)":
            return True, []
        return True, [n.strip() for n in names_str.split(",")]

    # Also check for SKILL_RESULT
    m = re.search(r"SKILL_RESULT:\s*(.+)", result_text)
    if m:
        return True, [m.group(1).strip()]

    return True, []
