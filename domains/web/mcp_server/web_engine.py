"""
domains/web/mcp_server/web_engine.py
Web skill execution engine — exec's create_component() from distilled skill code.

Mirrors the PPT pptx_engine.py pattern:
  1. exec() skill code in isolated namespace
  2. Call create_component(output_dir, **params)
  3. Return (success, file_list)
"""
from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

# Common imports prepended to every skill code before exec.
_SKILL_EXEC_PREAMBLE = """\
import os, json, math, re
from pathlib import Path
"""


def _skill_worker(full_code: str, output_dir: str, params: dict, queue) -> None:
    """Run untrusted-ish skill code in a child process.

    Some scraped web skills contain accidental infinite loops or long asset
    generation. Running them in the MCP process can wedge the whole agent
    turn, so the parent enforces a wall-clock timeout around this worker.
    """
    try:
        namespace: dict = {}
        exec(full_code, namespace)

        func = namespace.get("create_component")
        if func is None:
            queue.put({"ok": False, "error_type": "MissingFunction", "error": "no create_component() found"})
            return

        sig = inspect.signature(func)
        filtered = {k: v for k, v in params.items() if k in sig.parameters}

        old_cwd = os.getcwd()
        work_dir = tempfile.mkdtemp(prefix="web_skill_")
        try:
            os.chdir(work_dir)
            func(output_dir, **filtered)
        finally:
            os.chdir(old_cwd)
            import shutil
            shutil.rmtree(work_dir, ignore_errors=True)

        file_list = []
        for f in Path(output_dir).iterdir():
            if f.is_file():
                file_list.append(f.name)
        queue.put({"ok": True, "files": sorted(file_list)})
    except Exception as e:  # noqa: BLE001
        queue.put({
            "ok": False,
            "error_type": type(e).__name__,
            "error": str(e),
            "trace": traceback.format_exc()[-500:],
        })


def _run_skill_with_timeout(
    full_code: str,
    output_dir: str,
    params: dict,
    timeout_sec: float,
) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    runner = r'''
import inspect, json, os, shutil, sys, tempfile, traceback
from pathlib import Path

code_path, output_dir, params_path, result_path = sys.argv[1:5]
try:
    full_code = Path(code_path).read_text(encoding="utf-8")
    params = json.loads(Path(params_path).read_text(encoding="utf-8"))
    namespace = {}
    exec(full_code, namespace)

    func = namespace.get("create_component")
    if func is None:
        result = {"ok": False, "error_type": "MissingFunction", "error": "no create_component() found"}
    else:
        sig = inspect.signature(func)
        filtered = {k: v for k, v in params.items() if k in sig.parameters}
        old_cwd = os.getcwd()
        work_dir = tempfile.mkdtemp(prefix="web_skill_")
        try:
            os.chdir(work_dir)
            func(output_dir, **filtered)
        finally:
            os.chdir(old_cwd)
            shutil.rmtree(work_dir, ignore_errors=True)
        files = sorted(f.name for f in Path(output_dir).iterdir() if f.is_file())
        result = {"ok": True, "files": files}
except Exception as e:
    result = {
        "ok": False,
        "error_type": type(e).__name__,
        "error": str(e),
        "trace": traceback.format_exc()[-500:],
    }
Path(result_path).write_text(json.dumps(result), encoding="utf-8")
'''
    with tempfile.TemporaryDirectory(prefix="web_skill_runner_") as tmp:
        tmp_path = Path(tmp)
        code_path = tmp_path / "skill_code.py"
        params_path = tmp_path / "params.json"
        result_path = tmp_path / "result.json"
        code_path.write_text(full_code, encoding="utf-8")
        params_path.write_text(json.dumps(params), encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-c", runner, str(code_path), output_dir, str(params_path), str(result_path)],
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "error_type": "TimeoutError",
                "error": f"skill execution exceeded {timeout_sec:.0f}s",
            }
        if result_path.exists():
            try:
                return json.loads(result_path.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                return {"ok": False, "error_type": type(e).__name__, "error": str(e)}
        return {
            "ok": False,
            "error_type": "ProcessExit",
            "error": (proc.stderr or proc.stdout or f"skill process exited with code {proc.returncode}")[-500:],
        }


def exec_skill_code(
    code: str,
    output_dir: str,
    params: dict | None = None,
    max_retries: int = 2,
    timeout_sec: float = 12.0,
) -> tuple[bool, list[str]]:
    """Execute a web skill's create_component() function.

    Args:
        code: Python source code containing def create_component(output_dir, ...).
        output_dir: Directory to write HTML/CSS/JS files into.
        params: Optional keyword arguments for create_component().
        max_retries: Number of auto-repair retries on common errors.
        timeout_sec: Wall-clock timeout for each execution attempt.

    Returns:
        (success: bool, file_list: list of created filenames)
    """
    params = params or {}
    os.makedirs(output_dir, exist_ok=True)

    full_code = _SKILL_EXEC_PREAMBLE + "\n" + code

    for attempt in range(1 + max_retries):
        result = _run_skill_with_timeout(full_code, output_dir, params, timeout_sec)
        if result.get("ok"):
            return True, list(result.get("files") or [])

        error_type = str(result.get("error_type") or "Error")
        error = str(result.get("error") or "")
        if error_type in {"ImportError", "NameError", "AttributeError"}:
            if attempt < max_retries:
                # Try to auto-fix common import issues.
                full_code = _auto_fix(full_code, RuntimeError(error))
                continue
            return False, [f"Error after {attempt + 1} attempts: {error_type}: {error}"]
        trace = str(result.get("trace") or "")
        if trace:
            return False, [f"Error: {error_type}: {error}\n{trace}"]
        return False, [f"Error: {error_type}: {error}"]

    return False, ["Error: max retries exceeded"]


def _auto_fix(code: str, error: Exception) -> str:
    """Try to auto-fix common skill code errors."""
    msg = str(error)

    # Missing import fixes.
    if "colorsys" in msg:
        code = "import colorsys\n" + code
    elif "textwrap" in msg:
        code = "import textwrap\n" + code
    elif "base64" in msg:
        code = "import base64\n" + code
    elif "urllib" in msg:
        code = "import urllib.request\n" + code

    return code


def extract_code_from_analysis(analysis: str) -> str:
    """Extract the first Python code block from a skill analysis Markdown."""
    import re
    pattern = r"```python\s*\n(.*?)```"
    m = re.search(pattern, analysis, re.DOTALL)
    return m.group(1).strip() if m else ""


def get_skill_detail(
    skills_dir: Path, skill_id: str, index: list[dict]
) -> dict | None:
    """Load full skill detail JSON for a given skill_id.

    Returns None when the entry exists in the index but has no
    ``detail_path`` (e.g. wiki-format entries). The caller is expected
    to fall back to the wiki overview.md path in that case.
    """
    entry = None
    for s in index:
        if s.get("skill_id") == skill_id:
            entry = s
            break
    if entry is None:
        return None

    detail_path_str = entry.get("detail_path")
    if not detail_path_str:
        return None
    detail_path = skills_dir / detail_path_str
    if not detail_path.exists():
        return None

    import json
    return json.loads(detail_path.read_text(encoding="utf-8"))
