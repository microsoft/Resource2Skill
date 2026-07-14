from pathlib import Path
import importlib.util


def _helpers():
    path = Path(__file__).resolve().parents[2] / "_codex_workbook_helpers.py"
    spec = importlib.util.spec_from_file_location("codex_workbook_helpers", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render_workbook(wb, *, title: str = "AI Infrastructure Board Scenario Model", **kwargs) -> None:
    _helpers().render_cfo(wb, title_text=title)
