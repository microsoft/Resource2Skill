"""Wash pipeline: turn a legacy skill payload into a wiki entry.

The wash decomposes into a deterministic pass plus an optional
Gemini-distillation pass. The deterministic pass copies code/text/visual
from a legacy payload into the wiki layout, runs QA against the declared
``signature.json`` entrypoint, and either indexes the result or
quarantines the structurally broken ones. The Gemini pass — gated on
``WASH_USE_GEMINI=1`` and ``GEMINI_API_KEY`` (Round-14: Azure is no
longer accepted as a wash-enrichment backend) — refines
``applicability`` / ``tags`` / ``category_path`` from the prose context.
When the gate is closed or the API call fails, the deterministic output
is preserved unchanged: this is the round-10 fallback contract.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .budget import BudgetExceeded, BudgetTracker, load_budget_caps
from .qa import QAResult, load_domain_smoke_fixture, load_signature, run_qa
from .registry import RegistryError, SchemaValidationError, SkillEntry, WikiRegistry, _utc_now


# Reasons surfaced to ``_quarantine/<skill_id>/quarantine_reason.json``.
QUARANTINE_PARSE_ERROR = "code_parse_error"
QUARANTINE_MISSING_SIGNATURE = "missing_signature_json"
QUARANTINE_MISSING_ENTRYPOINT = "entrypoint_not_callable"
QUARANTINE_SCHEMA_VIOLATION = "meta_schema_violation"
QUARANTINE_REGISTRY_ERROR = "registry_error"


@dataclass
class WashStats:
    washed: int = 0
    skipped: int = 0
    failed: int = 0
    promoted: int = 0
    quarantined: int = 0
    fallbacks: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "washed": self.washed,
            "skipped": self.skipped,
            "failed": self.failed,
            "promoted": self.promoted,
            "quarantined": self.quarantined,
            "fallbacks": self.fallbacks,
            "error_samples": self.errors[:25],
        }


def _stable_skill_id(*, domain: str, source_path: Path) -> str:
    """Deterministic id for legacy skills lacking one of their own."""
    h = hashlib.sha1(f"{domain}::{source_path.name}".encode("utf-8")).hexdigest()[:8]
    base = source_path.stem.lower().replace("-", "_").replace(" ", "_")
    base = "".join(ch for ch in base if ch.isalnum() or ch == "_") or "skill"
    if base[0].isdigit():
        base = f"s_{base}"
    return f"{base}_{h}"


def _classify_modalities(skill_dir: Path) -> list[str]:
    """Detect which of source/visual/text/code subdirs contain real content."""
    present: list[str] = []
    for name in ("source", "visual", "text", "code"):
        sub = skill_dir / name
        if sub.is_dir() and any(sub.iterdir()):
            present.append(name)
    return present


def _seed_meta(
    *, skill_id: str, source_payload: dict[str, Any], domain: str,
    schema_version: str, wash_version: str,
) -> dict[str, Any]:
    name = source_payload.get("skill_name") or source_payload.get("name") or skill_id
    tier = source_payload.get("tier") or "T3"
    category = source_payload.get("category_path") or source_payload.get("category")
    if isinstance(category, str):
        category_path = [category.lower().replace("-", "_")]
    elif isinstance(category, list):
        category_path = [str(c).lower().replace("-", "_") for c in category if c][:3]
    else:
        category_path = ["uncategorized"]
    if not category_path:
        category_path = ["uncategorized"]
    source_block = source_payload.get("source") or {"type": "manual"}
    if isinstance(source_block, str):
        source_block = {"type": source_block}
    license_value = source_payload.get("license")
    return {
        "skill_id": skill_id,
        "skill_name": name,
        "tier": tier,
        "category_path": category_path,
        "applicability": source_payload.get("applicability", ""),
        "tags": list(source_payload.get("tags", []) or []),
        "schema_version": schema_version,
        "wash_version": wash_version,
        "license": license_value,
        "exec_ok": None,
        "source": source_block,
        "wash_run_at": _utc_now(),
    }


def wash_legacy_skill(
    *,
    registry: WikiRegistry,
    skill_id: str,
    legacy_payload: dict[str, Any],
    code_path: Path | None = None,
    text_path: Path | None = None,
    visual_path: Path | None = None,
    smoke_fixture: Path | None = None,
    extra_qa: Callable[[QAResult], None] | None = None,
    require_signature_when_code_present: bool = True,
    budget_tracker: BudgetTracker | None = None,
) -> dict[str, Any]:
    """Wash a single legacy entry.

    Behaviour:

    * If ``code_path`` is provided but ``signature.json`` is missing or
      ``ast.parse`` fails, the skill is **quarantined** rather than indexed.
    * If the declared entrypoint cannot be resolved, the skill is
      quarantined.
    * Schema/registry errors quarantine.
    * Otherwise the entry is committed to the wiki with ``exec_ok``
      reflecting the QA outcome (``true`` / ``false`` / ``null`` per
      ``run_qa`` semantics).
    """
    meta = _seed_meta(
        skill_id=skill_id,
        source_payload=legacy_payload,
        domain=registry.domain,
        schema_version=registry.schema_version,
        wash_version=registry.wash_version,
    )
    skill_dir = registry.skill_dir(skill_id)
    skill_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("source", "visual", "text", "code"):
        (skill_dir / sub).mkdir(exist_ok=True)

    wash_errors: list[str] = []

    if code_path is not None and code_path.exists():
        target = skill_dir / "code" / code_path.name
        try:
            shutil.copy2(code_path, target)
        except Exception as exc:  # noqa: BLE001
            registry.quarantine(skill_id, reason=f"{QUARANTINE_PARSE_ERROR}: copy failed: {exc}", payload=meta)
            return {"status": "quarantined", "skill_id": skill_id, "reason": str(exc)}

        # Locate signature.json next to the legacy code (any caller can
        # override the explicit path by including it in the legacy payload).
        signature_src: Path | None = None
        candidate = code_path.with_name("signature.json")
        if candidate.exists():
            signature_src = candidate
        elif (legacy_payload.get("signature_path")
              and Path(legacy_payload["signature_path"]).exists()):
            signature_src = Path(legacy_payload["signature_path"])

        entrypoint: str | None = None
        signature_payload: dict[str, Any] | None = None
        if signature_src is not None:
            try:
                signature_payload = load_signature(signature_src)
                entrypoint = str(signature_payload.get("entrypoint") or "").strip() or None
                shutil.copy2(signature_src, skill_dir / "code" / "signature.json")
            except Exception as exc:  # noqa: BLE001
                registry.quarantine(
                    skill_id,
                    reason=f"{QUARANTINE_MISSING_SIGNATURE}: invalid signature.json: {exc}",
                    payload=meta,
                )
                return {"status": "quarantined", "skill_id": skill_id, "reason": str(exc)}

        # Fall back to legacy_payload['entrypoint'] only when no signature
        # was declared. Code present without ANY entrypoint declaration is
        # treated as a structural failure when the caller asked for it.
        if entrypoint is None and legacy_payload.get("entrypoint"):
            entrypoint = str(legacy_payload["entrypoint"]).strip() or None

        if entrypoint is None and require_signature_when_code_present:
            registry.quarantine(
                skill_id,
                reason=f"{QUARANTINE_MISSING_SIGNATURE}: code present but entrypoint not declared",
                payload=meta,
            )
            return {"status": "quarantined", "skill_id": skill_id, "reason": "missing entrypoint"}

        if entrypoint is None:
            # Round-11: connector-supplied code with no signature is
            # indexed with exec_ok=None when the caller opted out of the
            # signature requirement. The code blob is preserved on disk
            # so agents can still read it via get_skill_code.
            meta["exec_ok"] = None
            meta.setdefault("code", {})
            meta["code"]["path"] = f"code/{code_path.name}"
        else:
            try:
                resolved_smoke = smoke_fixture
                if resolved_smoke is None:
                    resolved_smoke = load_domain_smoke_fixture(
                        domain=registry.domain, skill_id=skill_id,
                    )
                qa = run_qa(
                    skill_id=skill_id,
                    code_path=target,
                    entrypoint=entrypoint or "",
                    smoke_fixture=resolved_smoke,
                )
            except Exception as exc:  # noqa: BLE001
                registry.quarantine(skill_id, reason=f"{QUARANTINE_PARSE_ERROR}: {exc}", payload=meta)
                return {"status": "quarantined", "skill_id": skill_id, "reason": str(exc)}
            if extra_qa is not None:
                extra_qa(qa)

            # Structural failures = quarantine. Smoke-only failures stay indexed
            # with exec_ok=false so the agent can still see them via verified_only=False.
            if qa.stage_failed in {"ast", "entrypoint"}:
                reason_kind = (
                    QUARANTINE_PARSE_ERROR if qa.stage_failed == "ast"
                    else QUARANTINE_MISSING_ENTRYPOINT
                )
                registry.quarantine(
                    skill_id,
                    reason=f"{reason_kind}: {'; '.join(qa.errors) or qa.stage_failed}",
                    payload=meta,
                )
                return {"status": "quarantined", "skill_id": skill_id, "reason": qa.stage_failed}

            meta["exec_ok"] = qa.exec_ok
            if signature_payload is not None:
                meta.setdefault("code", {})
                meta["code"]["entrypoint"] = entrypoint
                meta["code"]["path"] = f"code/{code_path.name}"
            if qa.errors:
                wash_errors.extend(qa.errors)

    if text_path is not None and text_path.exists():
        try:
            shutil.copy2(text_path, skill_dir / "text" / "overview.md")
        except Exception as exc:  # noqa: BLE001
            wash_errors.append(f"text copy failed: {exc}")
    else:
        # Fall back to whichever free-text fields the legacy payload carries
        # (analysis, description, applicability) so the wiki has overview.md
        # content even when the legacy entry didn't ship one. AC-10's active
        # filter requires overview.md ≥ 200 chars; this populates the file
        # when the legacy payload has anything substantive to say.
        synthesised = _synthesise_overview(legacy_payload)
        if synthesised:
            try:
                (skill_dir / "text" / "overview.md").write_text(synthesised, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                wash_errors.append(f"text synth failed: {exc}")

    if visual_path is not None and visual_path.exists():
        try:
            shutil.copy2(visual_path, skill_dir / "visual" / visual_path.name)
        except Exception as exc:  # noqa: BLE001
            wash_errors.append(f"visual copy failed: {exc}")

    meta["modalities_present"] = _classify_modalities(skill_dir)
    if wash_errors:
        meta["wash_errors"] = wash_errors

    # Optional Gemini-distillation pass. Gated on WASH_USE_GEMINI=1 +
    # GEMINI_API_KEY so deterministic test runs stay deterministic.
    # Round-14: Azure is no longer accepted as a wash-enrichment
    # backend (Codex Round 13 finding 2). On any failure (including the
    # helper returning None) the deterministic meta is preserved AND
    # the diagnostic is written to wash_errors + meta["gemini_distilled"]
    # so the fallback is observable per Codex Round-10 finding 2.
    if _wash_gemini_enabled():
        if budget_tracker is not None:
            # Round-13: a cap hit must propagate out of the wash so
            # the command-level caller can surface a non-zero exit and
            # cap_reached.json. Previously the cap was silently
            # converted to a wash_errors entry, which violated AC-14.
            budget_tracker.check()  # raises BudgetExceeded if cap hit
        enriched: dict[str, Any] | None = None
        try:
            enriched = _enrich_meta_with_gemini(
                meta=meta, skill_dir=skill_dir, domain=registry.domain,
            )
            if budget_tracker is not None:
                budget_tracker.increment_gemini()
        except BudgetExceeded:
            raise
        except Exception as exc:  # noqa: BLE001
            meta.setdefault("wash_errors", []).append(
                f"gemini distill raised: {type(exc).__name__}: {exc}"
            )
            meta["gemini_distilled"] = False
        else:
            if enriched:
                for key in ("applicability", "tags", "category_path", "tier"):
                    if enriched.get(key):
                        meta[key] = enriched[key]
                if enriched.get("name"):
                    meta["skill_name"] = enriched["name"]
                meta["gemini_distilled"] = True
            else:
                # Helper returned None — surface the silent fallback.
                meta.setdefault("wash_errors", []).append(
                    "gemini distill returned None (helper unavailable or empty)"
                )
                meta["gemini_distilled"] = False

    try:
        registry.commit_meta(skill_id, meta)
    except SchemaValidationError as exc:
        registry.quarantine(skill_id, reason=f"{QUARANTINE_SCHEMA_VIOLATION}: {exc}", payload=meta)
        return {"status": "quarantined", "skill_id": skill_id, "reason": str(exc)}

    entry = SkillEntry(skill_id=skill_id, data=meta)
    try:
        registry.put(entry, allow_replace=True)
    except RegistryError as exc:
        registry.quarantine(skill_id, reason=f"{QUARANTINE_REGISTRY_ERROR}: {exc}", payload=meta)
        return {"status": "quarantined", "skill_id": skill_id, "reason": str(exc)}
    return {
        "status": "washed",
        "skill_id": skill_id,
        "exec_ok": meta.get("exec_ok"),
        "errors": wash_errors,
    }


def write_wash_report(*, root: Path, stats: WashStats, run_id: str, domain: str) -> Path:
    payload = {
        "run_id": run_id,
        "domain": domain,
        "ts": _utc_now(),
        "stats": stats.to_dict(),
    }
    out = root / "wash_report.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return out


def assemble_budget_tracker(*, domain: str, root: Path, run_id: str) -> BudgetTracker:
    cap = load_budget_caps()
    cap_reached = root / f"cap_reached_{run_id}.json"
    return BudgetTracker(cap=cap, domain=domain, run_id=run_id, cap_reached_path=cap_reached)


def _synthesise_overview(payload: dict[str, Any]) -> str | None:
    """Build a fallback ``overview.md`` body from legacy free-text fields.

    Round-11: prefers ``text_overview`` (set by source connectors like
    Article, GitHub, StaticArtifact) verbatim when present and ≥ 200
    chars. Falls back to concatenating ``skill_name``, ``applicability``,
    ``description``, ``analysis``, and ``tags``. When the prose is
    shorter than the AC-10 200-character minimum, padding is added by
    serialising structural fields so short reference-only tokens still
    satisfy the active-count gate. Returns ``None`` only if the payload
    is genuinely empty.
    """
    # Prefer the connector-supplied overview verbatim when it is
    # substantial. Otherwise it gets folded in below.
    raw_overview = payload.get("text_overview")
    if isinstance(raw_overview, str) and len(raw_overview.strip()) >= 200:
        return raw_overview

    parts: list[str] = []
    name = payload.get("skill_name") or payload.get("name")
    if name:
        parts.append(f"# {name}")
    if isinstance(raw_overview, str) and raw_overview.strip():
        parts.append(f"\n{raw_overview}")
    applicability = payload.get("applicability")
    if applicability:
        parts.append(f"\n## Applicability\n\n{applicability}")
    description = payload.get("description")
    if description:
        parts.append(f"\n## Description\n\n{description}")
    analysis = payload.get("analysis")
    if isinstance(analysis, str) and analysis.strip():
        parts.append(f"\n## Analysis\n\n{analysis}")
    elif isinstance(analysis, dict):
        analysis_text = "\n".join(f"- {k}: {v}" for k, v in analysis.items())
        if analysis_text:
            parts.append(f"\n## Analysis\n\n{analysis_text}")
    tags = payload.get("tags")
    if tags:
        parts.append("\n## Tags\n\n" + ", ".join(str(t) for t in tags))

    text = "\n".join(parts).strip()
    if len(text) < 200:
        # Pad with a structural snapshot of the payload so reference-only
        # tokens (themes, format presets, formulas) still satisfy AC-10.
        boilerplate_keys = {
            "skill_id", "skill_name", "name", "tier", "category_path",
            "category", "schema_version", "wash_version", "license",
            "exec_ok", "source", "modalities_present", "wash_run_at",
            "wash_errors", "applicability", "description", "analysis",
            "tags", "frames", "thumbnail",
        }
        params = {k: v for k, v in payload.items() if k not in boilerplate_keys}
        if params:
            try:
                rendered = json.dumps(params, indent=2, sort_keys=True, ensure_ascii=False, default=str)
                text = (text + "\n\n## Parameters\n\n```json\n" + rendered + "\n```\n").strip()
            except (TypeError, ValueError):
                pass
    return text if text else None


def _wash_gemini_enabled() -> bool:
    """Gate the model-backed enrichment pass on env vars only.

    Default is OFF so test runs and CI stay deterministic. Round-14:
    enabled only when ``WASH_USE_GEMINI=1`` AND ``GEMINI_API_KEY`` are
    set. Azure-only environments are NOT a valid configuration for the
    wash enrichment path per ``docs/skill_wiki_spec_final.md`` §model
    contract (Codex Round 13 finding 2).
    """
    if os.environ.get("WASH_USE_GEMINI", "").strip() not in {"1", "true", "yes"}:
        return False
    return bool(os.environ.get("GEMINI_API_KEY"))


def _enrich_meta_with_gemini(*, meta: dict[str, Any], skill_dir: Path,
                              domain: str | None = None) -> dict[str, Any] | None:
    """Refine applicability / tags / category_path via the active model.

    Round-12: routes through ``core.skill_wiki.llm_client.call_model_json``
    which prefers Gemini (``GEMINI_API_KEY``) and falls back to Azure
    OpenAI gpt-5.4 (``AZURE_OPENAI_API_KEY``). Returns ``None`` on any
    failure so the caller keeps the deterministic meta. Never raises.
    """
    overview_path = skill_dir / "text" / "overview.md"
    overview = overview_path.read_text(encoding="utf-8", errors="ignore") if overview_path.exists() else ""
    code_dir = skill_dir / "code"
    code_excerpt = ""
    if code_dir.exists():
        for cand in sorted(code_dir.glob("*.py")):
            code_excerpt = cand.read_text(encoding="utf-8", errors="ignore")[:2000]
            break
    domain_label = domain or meta.get("source", {}).get("type", "unknown")
    prompt = (
        f"Refine wiki metadata for skill_id={meta.get('skill_id')!r} in domain "
        f"{domain_label!r}. Emit a JSON object with keys: "
        f"tier (one of T1/T2/T3/T4/T5 — T1=token, T2=snippet, T3=component, "
        f"T4=sheet shell, T5=workbook archetype), "
        f"applicability (1-2 sentences), tags (3-6 short keywords), "
        f"category_path (list of 1-3 lower_snake_case segments), "
        f"name (string), description (<=200 char paraphrase). "
        f"Output JSON only.\n\n"
        f"Current name: {meta.get('skill_name')}\nCurrent tier: {meta.get('tier')}\n"
        f"Current applicability: {meta.get('applicability', '')!r}\n"
        f"Current category_path: {meta.get('category_path', [])}\n\n"
        f"Overview (truncated):\n{overview[:3000]}\n\nCode (truncated):\n{code_excerpt}"
    )
    from .llm_client import call_model_json
    return call_model_json(prompt=prompt)
