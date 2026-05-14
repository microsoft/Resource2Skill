"""
domains/blender/mcp_server/blender_engine.py
Blender skill execution engine — wraps bpy code for execution via BlenderMCP.

Skills are stored as def create_object(...) functions. This engine:
  1. Extracts code from skill analysis
  2. Wraps it for execution via BlenderMCP's execute_blender_code
  3. Returns object names created
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

    data = json.loads(detail_path.read_text(encoding="utf-8"))
    data["_skill_dir"] = str(detail_path.parent)
    return data


def wrap_skill_for_blender(
    code: str,
    params: dict | None = None,
) -> str:
    """Wrap a skill's create_object() code for execution in Blender.

    Returns a self-contained bpy script string that:
    1. Defines the skill's functions
    2. Calls create_object() with given params
    3. Prints the names of created objects for parsing
    """
    params = params or {}

    # Patch known bpy 5.x API breakages in distilled code.
    # Older skills used `in_out="OUT"`/"IN" — Blender 5.x renamed these to
    # "OUTPUT"/"INPUT" on NodeTreeInterface.new_socket().
    code = re.sub(r"""in_out\s*=\s*["']OUT["']""", 'in_out="OUTPUT"', code)
    code = re.sub(r"""in_out\s*=\s*["']IN["']""", 'in_out="INPUT"', code)

    # Build the param overrides as Python code.
    param_lines = []
    for k, v in params.items():
        param_lines.append(f"    {k}={repr(v)},")
    param_str = "\n".join(param_lines) if param_lines else ""

    wrapper = f"""
import bpy

# Record objects before execution.
_before = set(obj.name for obj in bpy.data.objects)

# --- Skill code start ---
{code}
# --- Skill code end ---

# Call create_object with params.
_skill_failed = False
try:
    result = create_object(
{param_str}
    )
except Exception as e:
    print(f"SKILL_ERROR: {{type(e).__name__}}: {{e}}")
    result = None
    _skill_failed = True

# Report new objects (skip on failure to avoid misleading the agent).
if not _skill_failed:
    _after = set(obj.name for obj in bpy.data.objects)
    _new = _after - _before
    if _new:
        print(f"SKILL_CREATED: {{','.join(sorted(_new))}}")
    else:
        print("SKILL_CREATED: (none)")
"""
    return wrapper


def parse_skill_result(result_text: str) -> tuple[bool, list[str]]:
    """Parse the output from a wrapped skill execution.

    Returns:
        (success: bool, object_names: list[str])
    """
    if "SKILL_ERROR:" in result_text:
        return False, [result_text]

    m = re.search(r"SKILL_CREATED:\s*(.+)", result_text)
    if m:
        names_str = m.group(1).strip()
        if names_str == "(none)":
            return True, []
        return True, [n.strip() for n in names_str.split(",")]

    return True, []
