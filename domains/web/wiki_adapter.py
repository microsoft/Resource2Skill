"""Web WikiAdapter: discovery + thin executable bridge for the Web domain.

The execution verbs write component files into a workspace dir and update a
``workspace_manifest.json``. The Web MCP server calls into this adapter when
``library_backend: wiki`` is set; with ``legacy`` it falls back to its
existing path.
"""
from __future__ import annotations

import json
import ast
import re
import shutil
from pathlib import Path
from typing import Any

from core.skill_wiki.contract import ExecutionResult, NotExecutableReason, WikiAdapter
from core.skill_wiki.registry import WikiRegistry
from core.skill_wiki.taxonomy import TaxonomyGate

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WIKI_ROOT = PROJECT_ROOT / "skills_wiki" / "web"
CAPABILITIES_PATH = Path(__file__).parent / "capabilities.json"


class WebWikiAdapter(WikiAdapter):
    DOMAIN = "web"

    def __init__(self, registry_root: Path | str | None = None) -> None:
        super().__init__(capabilities_path=CAPABILITIES_PATH)
        self._explicit_root = Path(registry_root) if registry_root else None
        root = self._resolve_root()
        self._registry = WikiRegistry(root=root, domain="web")
        self._taxonomy = TaxonomyGate(domain_root=root)

    def _resolve_root(self) -> Path:
        if self._explicit_root is not None:
            return self._explicit_root
        try:
            from core import get_library_dir
            return get_library_dir("web")
        except Exception:  # noqa: BLE001
            return DEFAULT_WIKI_ROOT

    # Cache invalidation --------------------------------------------------

    def reload(self) -> None:
        super().reload()
        new_root = self._resolve_root()
        self._registry = WikiRegistry(root=new_root, domain="web")
        self._taxonomy = TaxonomyGate(domain_root=new_root)

    # Discovery -----------------------------------------------------------

    def list_tiers(self) -> list[str]:
        return ["T1", "T2", "T3", "T4", "T5"]

    def list_categories(
        self, tier: str | None = None, category_path: str | None = None, depth: int = 2
    ) -> dict[str, Any]:
        taxonomy = self._read_taxonomy_tree()
        if tier is not None:
            taxonomy = {tier: taxonomy.get(tier, {})}
        return _truncate_tree(taxonomy, depth=depth)

    def list_skills(
        self, tier: str | None = None, category_path: str | None = None,
        source_type: str | None = None, verified_only: bool = False, limit: int = 50,
    ) -> list[dict[str, Any]]:
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
        for ext in ("*.html", "*.css", "*.js", "*.tsx", "*.jsx", "*.py", "*.json"):
            for candidate in sorted(code_dir.glob(ext)):
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
            domain="web",
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

    # Execution verbs (workspace bridge) ----------------------------------

    def init_workspace(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        """Create a workspace dir under ``demo/web/<target_id>/`` and seed
        an empty manifest. ``skill_id`` is informational here."""
        workspace = _workspace_dir(target_id)
        workspace.mkdir(parents=True, exist_ok=True)
        manifest_path = workspace / "workspace_manifest.json"
        manifest = {
            "workspace_id": target_id,
            "components": [],
            "archetype": None,
            "seed_skill_id": skill_id,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        return ExecutionResult.ok(
            skill_id, "init_workspace", target_id,
            detail={"workspace": str(workspace), "manifest": str(manifest_path)},
        )

    def write_project_file(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        """Copy a wiki-resident asset into a workspace at the configured path."""
        relative = kwargs.get("relative_path") or "index.html"
        skill_dir = self._registry.skill_dir(skill_id)
        # Pick the first code asset from the wiki entry; callers can override
        # via kwargs["source_file"] when a skill ships multiple files.
        source_name = kwargs.get("source_file")
        source = (skill_dir / "code" / source_name) if source_name else _first_code_asset(skill_dir)
        workspace = _workspace_dir(target_id)
        if source is None or not source.exists():
            generated = self._materialize_overview_component(
                skill_id=skill_id,
                workspace=workspace,
                relative=relative,
                kwargs={k: v for k, v in kwargs.items() if k not in {"relative_path", "source_file"}},
            )
            if generated is not None:
                if generated.get("error"):
                    return ExecutionResult.fail(
                        skill_id,
                        str(generated["error"]),
                        verb="write_project_file",
                    )
                _append_manifest_component(
                    workspace, skill_id=skill_id, relative=generated["entry"]
                )
                return ExecutionResult.ok(
                    skill_id,
                    "write_project_file",
                    target_id,
                    detail=generated,
                )
            return ExecutionResult.fail(
                skill_id, f"no code asset found under {skill_dir}/code", verb="write_project_file"
            )
        target = workspace / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        _append_manifest_component(workspace, skill_id=skill_id, relative=relative)
        return ExecutionResult.ok(
            skill_id, "write_project_file", target_id,
            detail={"wrote": str(target.relative_to(workspace))},
        )

    def apply_component_into_workspace(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        # Componets in the wiki are realised by writing the canonical file
        # plus updating the manifest. The workspace dir must exist (call
        # init_workspace first); we create it lazily otherwise.
        relative = kwargs.get("relative_path") or f"components/{skill_id}.html"
        return self.write_project_file(skill_id=skill_id, target_id=target_id,
                                       relative_path=relative,
                                       source_file=kwargs.get("source_file"))

    def _materialize_overview_component(
        self,
        *,
        skill_id: str,
        workspace: Path,
        relative: str,
        kwargs: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Execute a distilled ``create_component`` block from overview.md.

        Many web wiki skills have text + visual assets plus a fenced Python
        reproducer, but no copied ``code/`` file. Treat that reproducer as the
        executable asset so universal ``apply_skill`` can still mutate the
        target workspace.
        """
        skill_dir = self._registry.skill_dir(skill_id)
        overview = skill_dir / "text" / "overview.md"
        if not overview.exists():
            return None
        code = _extract_create_component_code(
            overview.read_text(encoding="utf-8", errors="ignore")
        )
        if not code:
            return None

        target = workspace / relative
        output_dir = target.parent if target.suffix else target
        output_dir.mkdir(parents=True, exist_ok=True)
        namespace: dict[str, Any] = {"__builtins__": __builtins__}
        try:
            exec(compile(code, f"<web-skill:{skill_id}>", "exec"), namespace, namespace)
            fn = namespace.get("create_component")
            if not callable(fn):
                return None
            call_kwargs = {
                "title_text": kwargs.get("title_text") or kwargs.get("title") or skill_id.replace("_", " ").title(),
                "body_text": kwargs.get("body_text") or kwargs.get("body") or "",
            }
            for key, value in kwargs.items():
                if key not in call_kwargs:
                    call_kwargs[key] = value
            result = fn(str(output_dir), **call_kwargs)
        except Exception as exc:  # noqa: BLE001
            return {
                "generated": False,
                "entry": str(target.relative_to(workspace)),
                "error": f"{type(exc).__name__}: {exc}",
            }

        # Common distilled components write index.html/style.css/script.js.
        generated_files = []
        for p in sorted(output_dir.rglob("*")):
            if p.is_file():
                generated_files.append(str(p.relative_to(workspace)))
        if isinstance(result, dict):
            for name, content in (("index.html", result.get("html")),
                                  ("style.css", result.get("css")),
                                  ("script.js", result.get("js"))):
                if content and not (output_dir / name).exists():
                    (output_dir / name).write_text(str(content), encoding="utf-8")
                    generated_files.append(str((output_dir / name).relative_to(workspace)))

        entry_path = output_dir / "index.html"
        if not entry_path.exists() and target.exists():
            entry_path = target
        if entry_path.name != target.name and target.suffix:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry_path, target)
            entry_path = target
            if str(target.relative_to(workspace)) not in generated_files:
                generated_files.append(str(target.relative_to(workspace)))
        if not entry_path.exists():
            return None
        return {
            "generated": True,
            "entry": str(entry_path.relative_to(workspace)),
            "files": sorted(set(generated_files)),
            "source": "text/overview.md:create_component",
        }

    def init_site_from_archetype(self, *, skill_id: str, target_id: str, **kwargs: Any) -> ExecutionResult:
        outcome = self.init_workspace(skill_id=skill_id, target_id=target_id, **kwargs)
        if not outcome.success:
            return outcome
        # Bring in every code asset shipped with the archetype.
        skill_dir = self._registry.skill_dir(skill_id)
        code_dir = skill_dir / "code"
        if not code_dir.exists():
            return outcome
        workspace = _workspace_dir(target_id)
        copied: list[str] = []
        for asset in sorted(code_dir.iterdir()):
            if not asset.is_file():
                continue
            target = workspace / asset.name
            shutil.copy2(asset, target)
            copied.append(asset.name)
        manifest_path = workspace / "workspace_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["archetype"] = skill_id
        manifest["files"] = copied
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        return ExecutionResult.ok(
            skill_id, "init_site_from_archetype", target_id,
            detail={"workspace": str(workspace), "files": copied},
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


def _workspace_dir(target_id: str) -> Path:
    safe = "".join(ch for ch in target_id if ch.isalnum() or ch in "-_") or "site"
    return PROJECT_ROOT / "demo" / "web" / safe


def _append_manifest_component(workspace: Path, *, skill_id: str, relative: str) -> None:
    manifest_path = workspace / "workspace_manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"workspace_id": workspace.name, "components": [], "archetype": None}
    manifest.setdefault("components", []).append({"skill_id": skill_id, "path": relative})
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def _first_code_asset(skill_dir: Path) -> Path | None:
    code_dir = skill_dir / "code"
    if not code_dir.exists():
        return None
    for ext in ("*.html", "*.css", "*.js", "*.tsx", "*.jsx", "*.json"):
        for candidate in sorted(code_dir.glob(ext)):
            return candidate
    return None


def _extract_create_component_code(markdown: str) -> str | None:
    for block in re.findall(r"```python\s*\n(.*?)(?:```|\Z)", markdown, re.DOTALL | re.IGNORECASE):
        if re.search(r"^def\s+create_component\s*\(", block, re.MULTILINE):
            return _largest_valid_python_prefix(block.strip())
    return None


def _largest_valid_python_prefix(code: str) -> str | None:
    lines = code.splitlines()
    # Fast path for normal, closed code fences.
    try:
        ast.parse(code)
        return code
    except SyntaxError:
        pass
    # Some distilled markdown has an unclosed fence, so prose after the code
    # enters the block. Trim to the largest prefix that still parses.
    for end in range(len(lines), 0, -1):
        candidate = "\n".join(lines[:end]).rstrip()
        if not candidate:
            continue
        try:
            ast.parse(candidate)
        except SyntaxError:
            continue
        if "def create_component" in candidate:
            return candidate
    return None


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


__all__ = ["WebWikiAdapter"]
