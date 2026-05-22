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
from pathlib import Path
from typing import Any

from core.skill_wiki.contract import ExecutionResult, NotExecutableReason, WikiAdapter
from core.skill_wiki.embeddings import IncompatibleEmbeddingIndex, load_compatible
from core.skill_wiki.registry import WikiRegistry
from core.skill_wiki.taxonomy import TaxonomyGate

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WIKI_ROOT = PROJECT_ROOT / "skills_wiki" / "ppt"
CAPABILITIES_PATH = Path(__file__).parent / "capabilities.json"


class PPTWikiAdapter(WikiAdapter):
    DOMAIN = "ppt"

    def __init__(self, registry_root: Path | str | None = None) -> None:
        super().__init__(capabilities_path=CAPABILITIES_PATH)
        self._explicit_root = Path(registry_root) if registry_root else None
        root = self._resolve_root()
        self._registry = WikiRegistry(root=root, domain="ppt")
        self._taxonomy = TaxonomyGate(domain_root=root)
        self._embedding_cache: tuple[list[str], Any, Any] | None = None

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
        self._embedding_cache = None

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
        for candidate in sorted(code_dir.glob("*.py")):
            return candidate.read_text(encoding="utf-8", errors="ignore")
        for candidate in sorted(code_dir.glob("*.json")):
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

    def search_skills(self, query: str, tier: str | None = None,
                      category_path: str | None = None, k: int = 5) -> list[dict[str, Any]]:
        try:
            ids, matrix, _meta = self._load_embeddings()
        except (IncompatibleEmbeddingIndex, FileNotFoundError):
            ids, matrix = [], None
        if matrix is None or not ids:
            return self._substring_search(query, tier=tier, category_path=category_path, k=k)
        return self._substring_search(query, tier=tier, category_path=category_path, k=k)

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

    # Internals -----------------------------------------------------------

    def _read_taxonomy_tree(self) -> dict[str, Any]:
        path = self._registry.root / "taxonomy.json"
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("tree", {})
        except json.JSONDecodeError:
            return {}

    def _load_embeddings(self) -> tuple[list[str], Any, Any]:
        if self._embedding_cache is None:
            from core.skill_wiki.budget import _CONFIG_PATH  # type: ignore[attr-defined]
            payload = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
            ids, matrix, meta = load_compatible(
                npz_path=self._registry.root / "embeddings.npz",
                meta_path=self._registry.root / "embeddings.meta.json",
                expected_model=str(payload.get("embedding_model", "text-embedding-3-large")),
            )
            self._embedding_cache = (ids, matrix, meta)
        return self._embedding_cache

    def _substring_search(self, query: str, *, tier: str | None,
                          category_path: str | None, k: int) -> list[dict[str, Any]]:
        q = query.lower()
        scored: list[tuple[int, dict[str, Any]]] = []
        for entry in self._registry.list_entries():
            if tier is not None and entry.get("tier") != tier:
                continue
            haystack = " ".join([
                str(entry.get("skill_name") or ""),
                str(entry.get("applicability") or ""),
                " ".join(entry.get("tags", []) or []),
            ]).lower()
            score = sum(1 for token in q.split() if token in haystack)
            if _has_visual(entry["skill_id"]):
                score += 2
            if score > 0:
                scored.append((score, _summary_view(entry)))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [entry for _, entry in scored[:k]]


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


__all__ = ["PPTWikiAdapter"]
