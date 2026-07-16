"""PPT hybrid WikiAdapter.

Discovery flows through the universal wiki contract; execution delegates
to the existing PPT MCP execution layer (python-pptx engine + visual-QA
hooks). The adapter does not own the runtime python-pptx state — it only
resolves a wiki-resident skill into a code blob the caller can execute via
the legacy ``add_slide_from_skill`` / ``replace_slide`` tools.

This satisfies the plan's Milestone 5 hybrid pattern: wiki discovery surface
+ thin executable bridge to the existing domain MCP execution layer, with
``library_backend`` staying on ``legacy`` for runtime asset reads.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from core.skill_wiki.contract import ExecutionResult, NotExecutableReason, WikiAdapter
from core.skill_wiki.registry import WikiRegistry
from core.skill_wiki.taxonomy import TaxonomyGate

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WIKI_ROOT = PROJECT_ROOT / "skills_wiki" / "ppt"
BRAND_WIKI_ROOT = PROJECT_ROOT / "brand_wiki" / "ppt"
CAPABILITIES_PATH = Path(__file__).parent / "capabilities.json"
_ACTIVE_BRAND: str | None = None


def set_active_brand(brand_name: str | None) -> None:
    global _ACTIVE_BRAND
    _ACTIVE_BRAND = brand_name


def _brand_root() -> Path | None:
    brand = _ACTIVE_BRAND or os.environ.get("PPT_ACTIVE_BRAND")
    if not brand:
        return None
    root = BRAND_WIKI_ROOT / brand
    return root if root.is_dir() else None


def _brand_skill_dir(skill_id: str) -> Path | None:
    root = _brand_root()
    if root is None:
        return None
    skill_dir = root / "skills" / skill_id
    return skill_dir if skill_dir.is_dir() else None


def _brand_entry(skill_dir: Path) -> dict[str, Any] | None:
    meta_path = skill_dir / "meta.json"
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _scan_brand_skills() -> list[dict[str, Any]]:
    root = _brand_root()
    if root is None:
        return []
    skills_root = root / "skills"
    if not skills_root.exists():
        return []
    out = []
    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        entry = _brand_entry(skill_dir)
        if entry:
            out.append(_summary_view(entry, root=skills_root))
    return out


class PPTWikiAdapter(WikiAdapter):
    DOMAIN = "ppt"

    def __init__(self, registry_root: Path | str | None = None) -> None:
        super().__init__(capabilities_path=CAPABILITIES_PATH)
        self._explicit_root = Path(registry_root) if registry_root else None
        root = self._resolve_root()
        self._registry = WikiRegistry(root=root, domain="ppt")
        self._taxonomy = TaxonomyGate(domain_root=root)

    def _resolve_root(self) -> Path:
        """PPT runs in hybrid mode: discovery is always rooted at
        ``skills_wiki/ppt`` even though ``library_backend`` stays on
        ``legacy`` so runtime asset reads continue to use the legacy
        python-pptx engine. We deliberately do NOT call
        ``get_library_dir("ppt")`` here because that returns the legacy
        path under hybrid configuration.
        """
        if self._explicit_root is not None:
            return self._explicit_root
        return DEFAULT_WIKI_ROOT

    def reload(self) -> None:
        super().reload()
        new_root = self._resolve_root()
        self._registry = WikiRegistry(root=new_root, domain="ppt")
        self._taxonomy = TaxonomyGate(domain_root=new_root)

    # Discovery -----------------------------------------------------------

    def list_tiers(self) -> list[str]:
        return ["T1", "T2", "T3", "T4", "T5"]

    def list_categories(self, tier: str | None = None, category_path: str | None = None,
                        depth: int = 2) -> dict[str, Any]:
        taxonomy = self._read_taxonomy_tree()
        if tier is not None:
            taxonomy = {tier: taxonomy.get(tier, {})}
        return _truncate_tree(taxonomy, depth=depth)

    def list_skills(self, tier: str | None = None, category_path: str | None = None,
                    source_type: str | None = None, verified_only: bool = False,
                    limit: int = 50) -> list[dict[str, Any]]:
        path_prefix = tuple(category_path.split("/")) if category_path else None
        out: list[dict[str, Any]] = []
        for entry in self._registry.list_entries():
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
        main_ids = {entry["skill_id"] for entry in out}
        for entry in _scan_brand_skills():
            if entry["skill_id"] in main_ids:
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
            out.append(entry)
        return out

    def get_skill_text(self, skill_id: str) -> dict[str, Any]:
        entry = self._registry.get(skill_id) or {}
        skill_dir = self._registry.skill_dir(skill_id)
        brand_dir = _brand_skill_dir(skill_id)
        if not entry and brand_dir is not None:
            entry = _brand_entry(brand_dir) or {}
            skill_dir = brand_dir
        overview = skill_dir / "text" / "overview.md"
        svg_recipe = skill_dir / "svg_recipe.md"
        text_payload: dict[str, Any] = {
            "skill_id": skill_id,
            "name": entry.get("skill_name"),
            "applicability": entry.get("applicability"),
            "tags": entry.get("tags", []),
        }
        if overview.exists():
            text_payload["overview"] = overview.read_text(encoding="utf-8", errors="ignore")
        if svg_recipe.exists():
            # svg_recipe.md is the PRIMARY SVG-construction reference for the
            # PPT Master backend. It distills the skill's visual mechanism
            # into safe-subset SVG (the only subset PPT-Master translates
            # losslessly). When present, the agent should treat it as the
            # primary scaffold for the slide's SVG; get_skill_code (PIL +
            # python-pptx era) is legacy inspiration only.
            text_payload["svg_recipe"] = svg_recipe.read_text(encoding="utf-8", errors="ignore")
        return text_payload

    def get_skill_code(self, skill_id: str) -> str:
        skill_dir = _brand_skill_dir(skill_id) or self._registry.skill_dir(skill_id)
        code_dir = skill_dir / "code"
        if not code_dir.exists():
            return ""
        for candidate in sorted(code_dir.glob("*.py")):
            return candidate.read_text(encoding="utf-8", errors="ignore")
        for candidate in sorted(code_dir.glob("*.json")):
            return candidate.read_text(encoding="utf-8", errors="ignore")
        return ""

    def get_skill_visual(self, skill_id: str) -> dict[str, Any]:
        brand_dir = _brand_skill_dir(skill_id)
        skill_dir = brand_dir or self._registry.skill_dir(skill_id)
        visual_dir = skill_dir / "visual"
        if not visual_dir.exists():
            return {"path": None}
        for candidate in visual_dir.iterdir():
            if candidate.is_file():
                if brand_dir is not None:
                    return {
                        "path": str(candidate.relative_to(brand_dir.parent)),
                        "_image_attachment": str(candidate.resolve()),
                    }
                return {
                    "path": str(candidate.relative_to(self._registry.root)),
                    "_image_attachment": str(candidate.resolve()),
                }
        return {"path": None}

    def search_skills(self, query: str, tier: str | None = None,
                      category_path: str | None = None, k: int = 5) -> list[dict[str, Any]]:
        # Two-stage retrieval: Okapi BM25 candidate pool (IDF + length-norm over
        # name+applicability+tags, with a mild multiplicative visual boost) →
        # LLM rerank (Azure GPT-5.5, low reasoning) → top k. The rerank raises
        # LLMRerankError on failure; callers must NOT swallow it.
        from core.skill_wiki.bm25 import bm25_pool
        from core.skill_wiki.llm_rerank import llm_rerank_skills, candidate_pool_size

        pool = bm25_pool(
            self._registry.list_entries(), query, candidate_pool_size(k),
            tier=tier, has_visual=_has_visual, summary_view=_summary_view,
        )
        if len(pool) <= k:
            return pool
        candidate_ids = [str(e.get("skill_id")) for e in pool if e.get("skill_id")]
        reranked_ids = llm_rerank_skills(
            query=query,
            candidate_ids=candidate_ids,
            registry_entries=list(self._registry.list_entries()),
            k=k,
            domain="ppt",
        )
        by_id = {str(e.get("skill_id")): e for e in pool}
        return [by_id[sid] for sid in reranked_ids if sid in by_id]

    def propose_category(self, tier: str, path: list[str], reason: str,
                         example_skill_id: str | None = None) -> dict[str, Any]:
        return self._taxonomy.propose_category(
            tier=tier, path=path, reason=reason, example_skill_id=example_skill_id
        ).to_dict()

    # Hybrid execution ----------------------------------------------------

    def apply_skill_via_legacy(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        """Resolve the wiki skill's code asset and return a payload that the
        legacy PPT MCP tools can apply.

        The adapter does not import the python-pptx engine itself; it
        returns the resolved code path + entrypoint so the caller can
        invoke ``add_slide_from_skill`` (or any equivalent legacy tool)
        with the right parameters. This keeps the bridge thin and avoids
        coupling the adapter to the legacy engine's lifecycle.
        """
        entry = self._registry.get(skill_id)
        if entry is None:
            return ExecutionResult.not_executable(
                skill_id, NotExecutableReason.SKILL_NOT_FOUND
            )
        skill_dir = self._registry.skill_dir(skill_id)
        code_dir = skill_dir / "code"
        code_files = sorted(code_dir.glob("*.py")) if code_dir.exists() else []
        if not code_files:
            return ExecutionResult.not_executable(
                skill_id, NotExecutableReason.TIER_HAS_NO_CODE,
                message=f"no code asset found under {code_dir}",
            )
        signature_path = code_dir / "signature.json"
        entrypoint: str | None = None
        if signature_path.exists():
            try:
                signature = json.loads(signature_path.read_text(encoding="utf-8"))
                entrypoint = str(signature.get("entrypoint") or "").strip() or None
            except json.JSONDecodeError:
                entrypoint = None
        return ExecutionResult.ok(
            skill_id, "apply_skill_via_legacy", target_id,
            detail={
                "code_path": str(code_files[0]),
                "entrypoint": entrypoint,
                "tier": entry.get("tier"),
                "category_path": entry.get("category_path"),
                "kwargs": kwargs,
            },
        )

    def apply_skill(self, skill_id: str, target_id: str, kwargs_json: str = "{}") -> dict[str, Any]:
        brand_dir = _brand_skill_dir(skill_id)
        if brand_dir is None:
            return super().apply_skill(skill_id=skill_id, target_id=target_id, kwargs_json=kwargs_json)
        try:
            kwargs = json.loads(kwargs_json) if kwargs_json else {}
        except json.JSONDecodeError as exc:
            return ExecutionResult.fail(skill_id, f"invalid kwargs_json: {exc}").to_json()
        code_files = sorted((brand_dir / "code").glob("*.py"))
        if not code_files:
            return ExecutionResult.not_executable(
                skill_id,
                NotExecutableReason.TIER_HAS_NO_CODE,
                message=f"no code asset found under {brand_dir / 'code'}",
            ).to_json()
        entry = _brand_entry(brand_dir) or {}
        return ExecutionResult.ok(
            skill_id,
            "apply_skill_via_legacy",
            target_id,
            detail={
                "code_path": str(code_files[0]),
                "entrypoint": "create_slide",
                "tier": entry.get("tier"),
                "category_path": entry.get("category_path"),
                "kwargs": kwargs,
                "note": "brand overlay skills are exposed for inspection; live deck construction uses brand shell IDs",
            },
        ).to_json()

    # Internals -----------------------------------------------------------

    def _read_taxonomy_tree(self) -> dict[str, Any]:
        path = self._registry.root / "taxonomy.json"
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("tree", {})
        except json.JSONDecodeError:
            return {}


def _summary_view(entry: dict[str, Any], *, root: Path = DEFAULT_WIKI_ROOT) -> dict[str, Any]:
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
        "has_visual": _has_visual(skill_id, root=root),
    }


def _has_visual(skill_id: str, *, root: Path = DEFAULT_WIKI_ROOT) -> bool:
    visual_dir = root / skill_id / "visual"
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


__all__ = ["PPTWikiAdapter", "set_active_brand"]
