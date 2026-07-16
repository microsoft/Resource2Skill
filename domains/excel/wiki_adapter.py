"""Excel WikiAdapter: discovery against ``skills_wiki/excel/`` plus thin
execution-bridge verbs that delegate to the existing ``xlsx_engine``.

The adapter is loaded by the Excel MCP server when ``library_backend: wiki``
is set in ``domain.yaml``. With ``library_backend: legacy`` the server keeps
its existing behaviour and this module is not imported.
"""
from __future__ import annotations

import json
import ast
import sys
from pathlib import Path
from typing import Any

from core.skill_wiki.contract import ExecutionResult, NotExecutableReason, WikiAdapter
from core.skill_wiki.registry import WikiRegistry
from core.skill_wiki.taxonomy import TaxonomyGate

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WIKI_ROOT = PROJECT_ROOT / "skills_wiki" / "excel"
CAPABILITIES_PATH = Path(__file__).parent / "capabilities.json"
_EXPERIMENT_SKIP_SKILL_IDS = {"cfo_scenario_board_workbook_archetype"}


class ExcelWikiAdapter(WikiAdapter):
    DOMAIN = "excel"

    # Legacy tier names (used in agent_prompt.md and older skill catalogs)
    # mapped to the wiki taxonomy. Keeps the prompt working without
    # rewriting every reference.
    _TIER_ALIASES = {
        "token": "T1",
        "snippet": "T2",
        "component": "T3",
        "sheet_shell": "T4",
        "archetype": "T5",
    }

    @classmethod
    def _resolve_tier(cls, tier: str | None) -> str | None:
        if tier is None:
            return None
        return cls._TIER_ALIASES.get(tier, tier)

    def __init__(self, registry_root: Path | str | None = None) -> None:
        super().__init__(capabilities_path=CAPABILITIES_PATH)
        self._explicit_root = Path(registry_root) if registry_root else None
        root = self._resolve_root()
        self._registry = WikiRegistry(root=root, domain="excel")
        self._taxonomy = TaxonomyGate(domain_root=root)
        self._signature_cache: dict[tuple[str, str], set[str]] = {}

    def _resolve_root(self) -> Path:
        """Pick the active registry root: explicit > get_library_dir > default."""
        if self._explicit_root is not None:
            return self._explicit_root
        try:
            from core import get_library_dir
            return get_library_dir("excel")
        except Exception:  # noqa: BLE001
            return DEFAULT_WIKI_ROOT

    # Cache invalidation --------------------------------------------------

    def reload(self) -> None:
        super().reload()
        # Re-resolve the registry root so a backend flip (legacy ↔ wiki)
        # changes the directory served by this adapter without restart.
        new_root = self._resolve_root()
        self._registry = WikiRegistry(root=new_root, domain="excel")
        self._taxonomy = TaxonomyGate(domain_root=new_root)

    # Discovery -----------------------------------------------------------

    def list_tiers(self) -> list[str]:
        return ["T1", "T2", "T3", "T4", "T5"]

    def list_categories(
        self, tier: str | None = None, category_path: str | None = None, depth: int = 2
    ) -> dict[str, Any]:
        tier = self._resolve_tier(tier)
        taxonomy = self._read_taxonomy_tree()
        if tier is not None:
            taxonomy = {tier: taxonomy.get(tier, {})}
        return _truncate_tree(taxonomy, depth=depth)

    def list_skills(
        self, tier: str | None = None, category_path: str | None = None,
        source_type: str | None = None, verified_only: bool = False, limit: int = 50,
    ) -> list[dict[str, Any]]:
        tier = self._resolve_tier(tier)
        path_prefix = tuple(category_path.split("/")) if category_path else None
        out: list[dict[str, Any]] = []
        for entry in self._registry.list_entries():
            if entry.get("skill_id") in _EXPERIMENT_SKIP_SKILL_IDS:
                continue
            if tier is not None and entry.get("tier") != tier:
                continue
            if path_prefix is not None:
                if tuple(entry.get("category_path", []))[: len(path_prefix)] != path_prefix:
                    continue
            if source_type is not None and (entry.get("source") or {}).get("type") != source_type:
                continue
            if verified_only and entry.get("exec_ok") is not True:
                continue
            out.append(_summary_view(entry))
            if len(out) >= limit:
                break
        return out

    def get_skill_text(self, skill_id: str) -> dict[str, Any]:
        entry = self._registry.get(skill_id) or {}
        skill_dir = self._registry.skill_dir(skill_id)
        overview = skill_dir / "text" / "overview.md"
        text_payload: dict[str, Any] = {
            "skill_id": skill_id,
            "name": entry.get("skill_name"),
            "applicability": entry.get("applicability"),
            "tags": entry.get("tags", []),
        }
        if overview.exists():
            text_payload["overview"] = overview.read_text(encoding="utf-8", errors="ignore")
        return text_payload

    def get_skill_code(self, skill_id: str) -> str:
        skill_dir = self._registry.skill_dir(skill_id)
        code_dir = skill_dir / "code"
        if not code_dir.exists():
            return ""
        for candidate in code_dir.glob("*.py"):
            return candidate.read_text(encoding="utf-8", errors="ignore")
        for candidate in code_dir.glob("*.json"):
            return candidate.read_text(encoding="utf-8", errors="ignore")
        return ""

    def get_skill_visual(self, skill_id: str) -> dict[str, Any]:
        skill_dir = self._registry.skill_dir(skill_id)
        visual_dir = skill_dir / "visual"
        if not visual_dir.exists():
            return {"path": None}
        for candidate in visual_dir.iterdir():
            if candidate.is_file():
                return {
                    "path": str(candidate.relative_to(self._registry.root)),
                    "_image_attachment": str(candidate.resolve()),
                }
        return {"path": None}

    def search_skills(
        self, query: str, tier: str | None = None,
        category_path: str | None = None, k: int = 5,
    ) -> list[dict[str, Any]]:
        tier = self._resolve_tier(tier)
        # Two-stage retrieval: Okapi BM25 candidate pool (IDF + length-norm over
        # name+applicability+tags, with a mild multiplicative visual boost) →
        # LLM rerank (Azure GPT-5.5, low reasoning) → top k. The rerank raises
        # LLMRerankError on failure; callers must NOT swallow it.
        from core.skill_wiki.bm25 import bm25_pool
        from core.skill_wiki.llm_rerank import llm_rerank_skills, candidate_pool_size

        pool = bm25_pool(
            self._registry.list_entries(), query, candidate_pool_size(k),
            tier=tier, skip_ids=_EXPERIMENT_SKIP_SKILL_IDS,
            has_visual=_has_visual, summary_view=_summary_view,
        )
        if len(pool) <= k:
            return pool
        candidate_ids = [str(e.get("skill_id")) for e in pool if e.get("skill_id")]
        reranked_ids = llm_rerank_skills(
            query=query,
            candidate_ids=candidate_ids,
            registry_entries=list(self._registry.list_entries()),
            k=k,
            domain="excel",
        )
        by_id = {str(e.get("skill_id")): e for e in pool}
        return [by_id[sid] for sid in reranked_ids if sid in by_id]

    def propose_category(
        self, tier: str, path: list[str], reason: str,
        example_skill_id: str | None = None,
    ) -> dict[str, Any]:
        return self._taxonomy.propose_category(
            tier=tier, path=path, reason=reason, example_skill_id=example_skill_id
        ).to_dict()

    # Execution verbs (thin bridge) --------------------------------------

    def init_workbook(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        """Create a workbook and register it under the caller-provided ``target_id``.

        ``target_id`` is the workbook-id alias the caller wants to reference
        the new workbook by; the engine assigns its own internal id, so we
        record both. ``skill_id`` is informational here (T1 theme tokens may
        seed the workbook theme).
        """
        try:
            xlsx_engine = _xlsx_engine_module()
        except ImportError as exc:
            return ExecutionResult.fail(skill_id, f"xlsx_engine import failed: {exc}", verb="init_workbook")
        name = kwargs.get("name") or target_id
        theme = kwargs.get("theme") or skill_id
        try:
            engine_workbook_id = xlsx_engine.create_workbook(name=name, theme=theme)
        except Exception as exc:  # noqa: BLE001
            return ExecutionResult.fail(skill_id, f"{type(exc).__name__}: {exc}", verb="init_workbook")
        return ExecutionResult.ok(
            skill_id, "init_workbook", target_id,
            detail={"engine_workbook_id": engine_workbook_id, "name": name, "theme": theme},
        )

    def apply_component(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        sheet_name = kwargs.get("sheet_name") or kwargs.get("sheet") or "Sheet1"
        anchor = kwargs.get("anchor") or "A1"
        params = kwargs.get("kwargs") or {k: v for k, v in kwargs.items()
                                           if k not in {"sheet_name", "sheet", "anchor", "kwargs"}}
        # Tier metadata in the wiki is unreliable (380/541 T3-tagged skills
        # are actually shell- or archetype-style). Sniff the skill's code and
        # dispatch to the matching engine verb so apply_skill works regardless
        # of the tier label.
        actual = self._detect_skill_signature(skill_id)
        if actual == "render_workbook":
            params = self._with_required_defaults(skill_id, "render_workbook", params, sheet_name=sheet_name)
            return self._call_engine(
                verb="init_from_archetype",
                skill_id=skill_id,
                target_id=target_id,
                engine_call=lambda eng, skills_dir: eng.render_archetype(
                    skills_dir, target_id, skill_id, params,
                ),
            )
        if actual == "render_sheet":
            params = self._with_required_defaults(skill_id, "render_sheet", params, sheet_name=sheet_name)
            return self._call_engine(
                verb="add_sheet_from_shell",
                skill_id=skill_id,
                target_id=target_id,
                engine_call=lambda eng, skills_dir: eng.render_sheet_shell(
                    skills_dir, target_id, skill_id, sheet_name, params,
                ),
            )
        params = self._with_required_defaults(skill_id, "render", params, sheet_name=sheet_name)
        return self._call_engine(
            verb="apply_component",
            skill_id=skill_id,
            target_id=target_id,
            engine_call=lambda eng, skills_dir: eng.apply_component(
                skills_dir, target_id, sheet_name, anchor, skill_id, params,
            ),
        )

    def add_sheet_from_shell(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        sheet_name = kwargs.get("sheet_name") or kwargs.get("sheet") or "Sheet1"
        params = kwargs.get("kwargs") or {k: v for k, v in kwargs.items()
                                           if k not in {"sheet_name", "sheet", "kwargs"}}
        params = self._with_required_defaults(skill_id, "render_sheet", params, sheet_name=sheet_name)
        return self._call_engine(
            verb="add_sheet_from_shell",
            skill_id=skill_id,
            target_id=target_id,
            engine_call=lambda eng, skills_dir: eng.render_sheet_shell(
                skills_dir, target_id, skill_id, sheet_name, params,
            ),
        )

    def init_from_archetype(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        params = kwargs.get("kwargs") or {k: v for k, v in kwargs.items() if k != "kwargs"}
        params = self._with_required_defaults(skill_id, "render_workbook", params)
        return self._call_engine(
            verb="init_from_archetype",
            skill_id=skill_id,
            target_id=target_id,
            engine_call=lambda eng, skills_dir: eng.render_archetype(
                skills_dir, target_id, skill_id, params,
            ),
        )

    # Internals -----------------------------------------------------------

    def _detect_skill_signature(self, skill_id: str) -> str | None:
        """Sniff which entry-point function a wiki skill exposes.

        Returns "render_workbook" / "render_sheet" / "render" / None.
        Used by apply_component to route to the right engine verb when the
        meta.json tier label is wrong.
        """
        try:
            from core import get_library_dir
            skills_dir = get_library_dir("excel")
            code_path = skills_dir / skill_id / "code" / "skill.py"
            if not code_path.exists():
                return None
            text = code_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None
        # Order matters: render_workbook is most specific, then render_sheet,
        # then bare render(ws, anchor) for true components.
        if "def render_workbook(" in text:
            return "render_workbook"
        if "def render_sheet(" in text:
            return "render_sheet"
        if "def render(" in text:
            return "render"
        return None

    def _with_required_defaults(
        self,
        skill_id: str,
        entrypoint: str,
        params: dict[str, Any],
        *,
        sheet_name: str | None = None,
    ) -> dict[str, Any]:
        """Fill common required kwargs for distilled Excel skills.

        Several wiki skills expose executable code but require presentation
        parameters like ``title`` or ``kpis``. The adapter can supply neutral
        defaults so ``apply_skill`` is a real insertion path; the agent can
        still overwrite task-specific data with grounded follow-up code.
        """
        required = self._required_kwonly_params(skill_id, entrypoint)
        if not required:
            return dict(params)
        out = dict(params)
        defaults = self._default_param_values(skill_id, sheet_name=sheet_name)
        for name in required:
            if name not in out and name in defaults:
                out[name] = defaults[name]
        return out

    def _required_kwonly_params(self, skill_id: str, entrypoint: str) -> set[str]:
        cache_key = (skill_id, entrypoint)
        if cache_key in self._signature_cache:
            return self._signature_cache[cache_key]
        required: set[str] = set()
        try:
            from core import get_library_dir
            code_path = get_library_dir("excel") / skill_id / "code" / "skill.py"
            text = code_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(text)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef) and node.name == entrypoint:
                    for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
                        if default is None:
                            required.add(arg.arg)
                    break
        except Exception:  # noqa: BLE001
            required = set()
        self._signature_cache[cache_key] = required
        return required

    def _default_param_values(self, skill_id: str, *, sheet_name: str | None = None) -> dict[str, Any]:
        entry = self._registry.get(skill_id) or {}
        title = (
            str(entry.get("skill_name") or "").strip()
            or str(sheet_name or "").strip()
            or skill_id.replace("_", " ").title()
        )
        kpis = [
            {"label": "Revenue", "value": 1240000, "delta": 0.12, "status": "Good"},
            {"label": "Margin", "value": 0.64, "delta": 0.03, "status": "Good"},
            {"label": "Risk", "value": 0.18, "delta": -0.02, "status": "Watch"},
        ]
        table_headers = ["Metric", "Current", "Target", "Status"]
        table_rows = [
            ["Pipeline", 1240000, 1100000, "Ahead"],
            ["Efficiency", 0.91, 0.85, "Good"],
            ["Exceptions", 3, 0, "Watch"],
        ]
        return {
            "title": title,
            "subtitle": "Generated workbook section",
            "company_name": "Example Co",
            "kpis": kpis,
            "cards": kpis,
            "table_headers": table_headers,
            "table_data": table_rows,
            "table_rows": table_rows,
            "data": table_rows,
            "main_panel": "Primary performance view",
            "top_right_panel": "Trend view",
            "bottom_right_panel": "Exception view",
            "title_text": title,
            "value": 100,
            "actual": 92,
            "target": 100,
            "prior": 84,
            "actual_value": 92,
            "target_value": 100,
            "primary_value": "92%",
            "secondary_value": "vs 100% target",
            "main_value": "92%",
            "kpi_name": "Performance",
            "kpi_label": "Performance",
            "icon_name": "circle",
            "kpi_value_cell": "B2",
            "data_anchor": "A1",
            "chart_anchor": "E1",
        }

    def _call_engine(
        self, *, verb: str, skill_id: str, target_id: str,
        engine_call: Any,
    ) -> ExecutionResult:
        try:
            xlsx_engine = _xlsx_engine_module()
        except ImportError as exc:
            return ExecutionResult.fail(
                skill_id, f"xlsx_engine import failed: {exc}", verb=verb
            )
        from core import get_library_dir
        skills_dir = get_library_dir("excel")
        try:
            result = engine_call(xlsx_engine, skills_dir)
        except Exception as exc:  # noqa: BLE001
            return ExecutionResult.fail(skill_id, f"{type(exc).__name__}: {exc}", verb=verb)
        if isinstance(result, ExecutionResult):
            return result
        if isinstance(result, dict):
            return ExecutionResult.ok(skill_id, verb, target_id, detail=result)
        return ExecutionResult.ok(skill_id, verb, target_id)

    def _read_taxonomy_tree(self) -> dict[str, Any]:
        path = self._registry.root / "taxonomy.json"
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("tree", {})
        except json.JSONDecodeError:
            return {}


def _xlsx_engine_module():
    """Return the live Excel engine module used by the MCP server.

    ``domains/excel/mcp_server/server.py`` imports the engine as top-level
    ``xlsx_engine`` after putting its directory on ``sys.path``. Importing the
    package-qualified module here creates a second workbook registry, which
    makes ``apply_skill`` fail with ``Unknown workbook_id`` in the real server
    process. Prefer the already-loaded top-level module, then fall back.
    """
    loaded = sys.modules.get("xlsx_engine")
    if loaded is not None and hasattr(loaded, "get_workbook"):
        return loaded
    from domains.excel.mcp_server import xlsx_engine  # type: ignore[import-not-found]
    return xlsx_engine


def _summary_view(entry: dict[str, Any]) -> dict[str, Any]:
    skill_id = entry["skill_id"]
    return {
        "skill_id": skill_id,
        "skill_name": entry.get("skill_name"),
        "tier": entry.get("tier"),
        "category_path": entry.get("category_path"),
        "source": entry.get("source"),
        "license": entry.get("license"),
        "exec_ok": entry.get("exec_ok"),
        "tags": entry.get("tags", []),
        "has_visual": _has_visual(skill_id),
    }


def _has_visual(skill_id: str) -> bool:
    visual_dir = DEFAULT_WIKI_ROOT / skill_id / "visual"
    if not visual_dir.exists():
        return False
    return any(
        p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
        for p in visual_dir.rglob("*")
    )


def _truncate_tree(node: Any, *, depth: int) -> Any:
    if depth <= 0 or not isinstance(node, dict):
        return {}
    return {
        key: _truncate_tree(child, depth=depth - 1) if isinstance(child, dict) else child
        for key, child in node.items()
        if not key.startswith("_")
    }


__all__ = ["ExcelWikiAdapter"]
