"""Code QA gates: ast parse, import resolution, declared entrypoint, smoke fixture.

The wash pipeline only marks a skill ``exec_ok=true`` when every gate passes.
A skill that lacks a smoke fixture is recorded as ``exec_ok=null`` (unknown),
not ``False``, so it remains visible to the agent.
"""
from __future__ import annotations

import ast
import importlib
import importlib.util
import json
import multiprocessing
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class QAResult:
    skill_id: str
    exec_ok: bool | None
    errors: list[str] = field(default_factory=list)
    stage_failed: str | None = None
    stage_completed: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "exec_ok": self.exec_ok,
            "errors": list(self.errors),
            "stage_failed": self.stage_failed,
            "stage_completed": list(self.stage_completed),
        }


def _ast_parse(source: str) -> list[str]:
    try:
        ast.parse(source)
    except SyntaxError as exc:
        return [f"syntax error at line {exc.lineno}: {exc.msg}"]
    return []


def _resolve_imports(source: str, *, allowed_missing: set[str] | None = None) -> list[str]:
    """Return a list of error strings for unresolvable top-level imports."""
    allowed_missing = allowed_missing or set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["could not parse for import resolution"]
    errors: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                # Relative import — skip; engine context resolves these.
                continue
            module = node.module or ""
            names = [module] if module else []
        else:
            continue
        for name in names:
            top = name.split(".")[0]
            if not top or top in allowed_missing:
                continue
            try:
                spec = importlib.util.find_spec(top)
                if spec is None:
                    errors.append(f"unresolved import: {name}")
            except (ImportError, ValueError) as exc:
                errors.append(f"import probe failed for {name}: {exc}")
    return errors


def _check_entrypoint(source: str, entrypoint: str) -> list[str]:
    """Statically check that ``entrypoint`` is a top-level callable name."""
    if not entrypoint:
        return ["signature.entrypoint is empty"]
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["could not parse for entrypoint check"]
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == entrypoint:
            return []
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == entrypoint:
                    return []
        if isinstance(node, ast.ClassDef) and node.name == entrypoint:
            return []
    return [f"entrypoint {entrypoint!r} not defined at module top level"]


def _run_smoke_in_subprocess(
    fixture_path: str, code_path: str, entrypoint: str, conn: Any, timeout: float
) -> None:  # pragma: no cover - exercised via multiprocessing
    try:
        spec = importlib.util.spec_from_file_location("_skill_under_qa", code_path)
        if spec is None or spec.loader is None:
            conn.send(("error", "failed to load skill module"))
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules["_skill_under_qa"] = module
        spec.loader.exec_module(module)
        fn = getattr(module, entrypoint, None)
        if fn is None or not callable(fn):
            conn.send(("error", f"entrypoint {entrypoint!r} not callable"))
            return
        with open(fixture_path, "r", encoding="utf-8") as fh:
            fixture = json.load(fh)
        kwargs = fixture.get("kwargs", {})
        fn(**kwargs)
        conn.send(("ok", None))
    except Exception as exc:  # noqa: BLE001
        conn.send(("error", f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"))


def run_qa(
    *,
    skill_id: str,
    code_path: Path | str,
    entrypoint: str,
    smoke_fixture: Path | str | None = None,
    smoke_timeout_seconds: float = 30.0,
    allowed_missing_imports: set[str] | None = None,
) -> QAResult:
    """Run the QA gates for a single skill and return a structured result.

    Stage order: ``ast``, ``imports``, ``entrypoint``, ``smoke``. The first
    failure short-circuits and yields ``exec_ok=False``. Missing smoke fixture
    yields ``exec_ok=None`` (unknown), not ``False``, so the skill stays
    visible to discovery.
    """
    code_path = Path(code_path)
    if not code_path.exists():
        return QAResult(
            skill_id=skill_id,
            exec_ok=False,
            errors=[f"code path missing: {code_path}"],
            stage_failed="code_present",
        )

    source = code_path.read_text(encoding="utf-8")
    completed: list[str] = []

    ast_errors = _ast_parse(source)
    if ast_errors:
        return QAResult(skill_id, False, ast_errors, "ast", completed)
    completed.append("ast")

    import_errors = _resolve_imports(source, allowed_missing=allowed_missing_imports)
    if import_errors:
        return QAResult(skill_id, False, import_errors, "imports", completed)
    completed.append("imports")

    entry_errors = _check_entrypoint(source, entrypoint)
    if entry_errors:
        return QAResult(skill_id, False, entry_errors, "entrypoint", completed)
    completed.append("entrypoint")

    if smoke_fixture is None:
        return QAResult(skill_id, None, [], None, completed)

    smoke_fixture = Path(smoke_fixture)
    if not smoke_fixture.exists():
        return QAResult(skill_id, None, [f"smoke fixture absent: {smoke_fixture}"], None, completed)

    parent_conn, child_conn = multiprocessing.Pipe(duplex=False)
    proc = multiprocessing.Process(
        target=_run_smoke_in_subprocess,
        args=(str(smoke_fixture), str(code_path), entrypoint, child_conn, smoke_timeout_seconds),
        daemon=True,
    )
    proc.start()
    proc.join(timeout=smoke_timeout_seconds)
    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=5)
        return QAResult(
            skill_id,
            False,
            [f"smoke timed out after {smoke_timeout_seconds}s"],
            "smoke",
            completed,
        )
    try:
        status, payload = parent_conn.recv()
    except EOFError:
        status, payload = "error", "subprocess crashed without sending status"
    if status == "ok":
        completed.append("smoke")
        return QAResult(skill_id, True, [], None, completed)
    return QAResult(skill_id, False, [str(payload)], "smoke", completed)


def load_signature(signature_path: Path | str) -> dict[str, Any]:
    payload = json.loads(Path(signature_path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("signature.json must decode to a JSON object")
    return payload


def load_domain_smoke_fixture(*, domain: str, skill_id: str, project_root: Path | None = None) -> Path | None:
    """Resolve a smoke fixture for ``skill_id`` within a domain.

    Looks under ``domains/<domain>/smoke_fixtures/<skill_id>.json`` first,
    then falls back to ``domains/<domain>/smoke_fixtures/_default.json``.
    Returns ``None`` if neither file exists; ``run_qa`` then yields
    ``exec_ok=null`` (visible but unknown) per AC-3.
    """
    root = project_root if project_root is not None else Path(__file__).resolve().parents[2]
    fixtures_dir = root / "domains" / domain / "smoke_fixtures"
    candidate = fixtures_dir / f"{skill_id}.json"
    if candidate.exists():
        return candidate
    fallback = fixtures_dir / "_default.json"
    if fallback.exists():
        return fallback
    return None


def derive_qa_callable(adapter: Any) -> Callable[..., QAResult] | None:
    """Optional hook for adapters that want to add domain-specific gates."""
    fn = getattr(adapter, "extra_qa", None)
    return fn if callable(fn) else None
