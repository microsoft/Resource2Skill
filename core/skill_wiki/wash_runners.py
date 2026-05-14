"""Per-domain wash runners — turn ``skills_library/<d>/`` into ``skills_wiki/<d>/``.

This module wires the wash pipeline. It walks the legacy library
discovering ``skill.json`` payloads and, for python-skill domains, the
matching ``*.py`` next to them. The optional Gemini-style enrichment
overlay (``WASH_USE_GEMINI=1`` + ``AZURE_OPENAI_API_KEY``) is applied
inside ``wash_legacy_skill`` when the env gate is set; until then the
deterministic pass populates the wiki and the enrichment is a no-op.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Iterable, Iterator

from .registry import WikiRegistry, _utc_now
from .wash import WashStats, wash_legacy_skill, write_wash_report
from .budget import BudgetExceeded


# Legacy folder name → tier mapping for the deterministic-input wash.
# Used as a heuristic ONLY when the legacy ``analysis`` markdown does
# not declare a ``**Tier**:`` line (which is the spec's preferred
# source of truth). The Gemini distillation pass overlays both.
_FOLDER_TIER_MAP: dict[str, str] = {
    # T1 — token / preset assets, reference-only.
    "themes": "T1",
    "format_presets": "T1",
    "chart_templates": "T1",
    "color_style": "T1",
    "palettes": "T1",
    "typography": "T1",
    # T2 — formula / snippet assets, reference-only.
    "formulas": "T2",
    "formula": "T2",
    "snippets": "T2",
    "cell_techniques": "T2",
    "validation": "T2",
    "formatting": "T2",
    # T3 — components.
    "components": "T3",
    "chart": "T3",
    "table": "T3",
    "pivot_table": "T3",
    "dashboard": "T3",
    # T4 — sheet shells.
    "sheet_shells_seed": "T4",
    "sheet_shells_distilled": "T4",
    "shells_seed": "T4",
    "shells_distilled": "T4",
    # T5 — workbook archetypes.
    "workbook_archetypes": "T5",
    "archetypes": "T5",
}


# Round-13: structured extraction from the legacy ``analysis`` markdown.
# This is the spec's preferred source for ``tier`` / ``category_path`` /
# ``applicability`` / ``tags`` per docs/skill_wiki_spec_final.md;
# folder-name heuristics are now a fallback rather than the primary
# signal.
_ANALYSIS_TIER_KEYWORD_TO_TIER: dict[str, str] = {
    # T1 — tokens / themes / palettes / formats.
    "theme": "T1", "themes": "T1",
    "format_preset": "T1", "format": "T1",
    "palette": "T1", "palettes": "T1",
    "chart_template": "T1", "chart_templates": "T1",
    "typography": "T1",
    # T2 — formulas / snippets / cell techniques / validations.
    "formula": "T2", "formulas": "T2",
    "snippet": "T2", "snippets": "T2",
    "cell_technique": "T2",
    "validation": "T2",
    # T3 — components.
    "component": "T3", "components": "T3",
    # T4 — sheet shells.
    "sheet_shell": "T4", "shell": "T4", "sheet_shells": "T4",
    # T5 — workbook archetypes / full decks.
    "workbook_archetype": "T5", "archetype": "T5",
    "workbook": "T5",
}


def _extract_from_analysis(analysis_text: str) -> dict[str, Any]:
    """Pull tier / category / applicability / tags out of the legacy
    ``analysis`` markdown.

    The convention used by the existing skills is::

        > **Skill Name**: ...
        * **Tier**: <name>
        * **Core Mechanism**: ...
        * **Applicability**: ...

    Returns a dict with whichever of those fields could be parsed.
    Empty dict when the input is not a string or has no recognisable
    fields.
    """
    if not isinstance(analysis_text, str) or not analysis_text.strip():
        return {}
    out: dict[str, Any] = {}
    import re as _re
    # Tier line — case-insensitive, value can be quoted/colon-bounded.
    tier_match = _re.search(
        r"\*\*\s*Tier\s*\*\*\s*:\s*([A-Za-z0-9_\-]+)",
        analysis_text,
    )
    if tier_match:
        keyword = tier_match.group(1).strip().lower()
        # Direct match first (T1..T5).
        if _re.fullmatch(r"t[1-5]", keyword):
            out["tier"] = keyword.upper()
        elif keyword in _ANALYSIS_TIER_KEYWORD_TO_TIER:
            out["tier"] = _ANALYSIS_TIER_KEYWORD_TO_TIER[keyword]
    # Skill name line.
    name_match = _re.search(
        r"\*\*\s*Skill\s+Name\s*\*\*\s*:\s*([^\n]+)",
        analysis_text,
    )
    if name_match:
        out["skill_name_from_analysis"] = name_match.group(1).strip().rstrip("*").strip()
    # Applicability — capture up to the next blank line or bullet.
    appl_match = _re.search(
        r"\*\*\s*Applicability\s*\*\*\s*:\s*([^\n]+(?:\n(?!\s*[\*\-#]).+)*)",
        analysis_text,
    )
    if appl_match:
        out["applicability"] = appl_match.group(1).strip()
    # Tags / Keywords line (optional).
    tags_match = _re.search(
        r"\*\*\s*(?:Tags|Keywords)\s*\*\*\s*:\s*([^\n]+)",
        analysis_text,
    )
    if tags_match:
        raw = tags_match.group(1).strip()
        tags = [t.strip().strip("`'\"").lower().replace(" ", "_")
                for t in raw.replace(",", " ").split() if t.strip()]
        if tags:
            out["tags"] = tags[:6]
    return out


def _infer_tier_from_path(path: Path, legacy_root: Path) -> str | None:
    """Infer tier from the first folder segment under the legacy domain root."""
    try:
        rel = path.relative_to(legacy_root)
    except ValueError:
        return None
    if not rel.parts:
        return None
    first = rel.parts[0]
    return _FOLDER_TIER_MAP.get(first)


def run_domain_wash(
    *,
    domain: str,
    project_root: Path,
    since: str | None = None,
    frozen_fixtures: str | None = None,
) -> dict[str, Any]:
    legacy_root = project_root / "skills_library" / domain
    if not legacy_root.exists():
        raise FileNotFoundError(legacy_root)
    wiki_root = project_root / "skills_wiki" / domain
    registry = WikiRegistry(root=wiki_root, domain=domain)
    stats = WashStats()
    run_id = f"wash_{int(time.time())}"
    prior_index_ids = {entry["skill_id"] for entry in registry.list_entries()}
    prior_diff: dict[str, dict[str, Any]] = {
        entry["skill_id"]: _canonical_tuple(entry) for entry in registry.list_entries()
    }
    since_ts: float | None = _parse_iso(since) if since else None

    # Round-12: build a real BudgetTracker for the wash command so the
    # optional Gemini/Azure enrichment paths consume the AC-14 cap
    # instead of bypassing it. ``register_pending`` enumerates work at
    # skill-id granularity so ``cap_reached.json`` can list every
    # unprocessed skill, not just source types.
    from .budget import BudgetTracker, load_budget_caps
    cap = load_budget_caps()
    tracker = BudgetTracker(
        cap=cap, domain=domain, run_id=run_id,
        cap_reached_path=wiki_root / f"cap_reached_{run_id}.json",
    )
    # Materialize once so the tracker can register at skill-id
    # granularity and the wash loop can iterate again without re-walking.
    legacy_payloads = list(_iter_legacy_payloads(legacy_root))
    pending_skill_ids = [p["skill_id"] for p in legacy_payloads]
    tracker.register_pending([{"id": sid} for sid in pending_skill_ids])

    fixtures: dict[str, dict[str, Any]] | None = None
    fixture_violations: list[dict[str, Any]] = []
    if frozen_fixtures:
        fixtures = _load_frozen_fixtures(Path(frozen_fixtures))

    cap_reached_payload: dict[str, Any] | None = None
    for legacy in legacy_payloads:
        if since_ts is not None and legacy["mtime"] < since_ts:
            stats.skipped += 1
            continue
        try:
            outcome = wash_legacy_skill(
                registry=registry,
                skill_id=legacy["skill_id"],
                legacy_payload=legacy["payload"],
                code_path=legacy["code_path"],
                text_path=legacy["text_path"],
                visual_path=legacy["visual_path"],
                require_signature_when_code_present=False,
                budget_tracker=tracker,
            )
        except BudgetExceeded as exc:
            # Round-13: cap hit propagates out of wash. Capture the
            # structured payload so the CLI surfaces a non-zero exit
            # plus the remaining-work enumeration. The pending list is
            # still populated at skill-id granularity (see registration
            # above), so payload["remaining"] is accurate.
            cap_reached_payload = exc.payload
            break
        tracker.mark_completed(legacy["skill_id"])
        if outcome["status"] == "quarantined":
            stats.quarantined += 1
            stats.errors.append(outcome)
        elif outcome["status"] == "washed":
            stats.washed += 1
            if fixtures is not None:
                violation = _check_frozen_fixture(
                    skill_id=legacy["skill_id"], fixtures=fixtures, registry=registry
                )
                if violation is not None:
                    fixture_violations.append(violation)

    diff_rows: list[dict[str, Any]] = []
    new_entries = registry.list_entries()
    new_ids = {e["skill_id"] for e in new_entries}
    new_canonical = {e["skill_id"]: _canonical_tuple(e) for e in new_entries}
    for sid, before in prior_diff.items():
        if sid in new_canonical and new_canonical[sid] != before:
            diff_rows.append({"skill_id": sid, "before": before, "after": new_canonical[sid]})
    silently_dropped = sorted(prior_index_ids - new_ids)
    if silently_dropped:
        diff_rows.append({"silently_dropped": silently_dropped})
    if fixture_violations:
        diff_rows.append({"fixture_violations": fixture_violations})
    if diff_rows:
        (wiki_root / "wash_diff.json").write_text(
            json.dumps({"run_id": run_id, "ts": _utc_now(), "rows": diff_rows}, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    write_wash_report(root=wiki_root, stats=stats, run_id=run_id, domain=domain)
    report: dict[str, Any] = {
        "run_id": run_id,
        "stats": stats.to_dict(),
        "wiki_root": str(wiki_root),
        "diff_rows": len(diff_rows),
        "fixture_violations": len(fixture_violations),
        "frozen_fixtures": frozen_fixtures,
    }
    if cap_reached_payload is not None:
        report["cap_reached"] = cap_reached_payload
    return report


def _iter_legacy_payloads(legacy_root: Path) -> Iterator[dict[str, Any]]:
    """Walk the legacy library and yield dicts the wash pipeline understands."""
    for skill_json in sorted(legacy_root.rglob("skill.json")):
        skill_dir = skill_json.parent
        try:
            payload = json.loads(skill_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        skill_id = payload.get("skill_id") or _stable_id_from_dir(skill_dir, legacy_root.name)
        skill_id = _normalise_skill_id(skill_id)
        code_path = _first_match(skill_dir, ("skill.py", "*.py"))
        text_path = _first_match(skill_dir, ("overview.md", "README.md", "analysis.md"))
        visual_path = _first_match(skill_dir, (
            "thumbnail.jpg", "thumbnail.png", "preview.png",
            "frame_00_*.jpg", "frame_*.jpg", "*.jpg", "*.png",
        ))
        forwarded = dict(payload)
        forwarded.setdefault("source", _infer_source(payload, legacy_root.name))
        forwarded["license"] = _infer_license(forwarded, forwarded["source"])
        # Round-13: structured extraction from the legacy analysis
        # markdown is the spec's preferred source for tier / category /
        # applicability / tags. Apply it BEFORE folder heuristics so we
        # respect what the curator put in `**Tier**:` instead of
        # silently overwriting it from a folder name.
        analysis_extract = _extract_from_analysis(payload.get("analysis", ""))
        if analysis_extract.get("tier"):
            forwarded["tier"] = analysis_extract["tier"]
        if analysis_extract.get("applicability") and not forwarded.get("applicability"):
            forwarded["applicability"] = analysis_extract["applicability"]
        if analysis_extract.get("tags") and not forwarded.get("tags"):
            forwarded["tags"] = analysis_extract["tags"]
        if analysis_extract.get("skill_name_from_analysis") and not forwarded.get("skill_name"):
            forwarded["skill_name"] = analysis_extract["skill_name_from_analysis"]
        # Folder-heuristic tier ONLY when no explicit tier survived.
        if not forwarded.get("tier"):
            inferred = _infer_tier_from_path(skill_dir, legacy_root)
            if inferred:
                forwarded["tier"] = inferred
        yield {
            "skill_id": skill_id,
            "payload": forwarded,
            "code_path": code_path,
            "text_path": text_path,
            "visual_path": visual_path,
            "mtime": skill_json.stat().st_mtime,
        }
    # Domains like Excel also keep flat ``*.json`` snippets (formulas/, themes/)
    # that are reference-only. Surface them too so the index picks them up.
    for json_path in sorted(legacy_root.rglob("*.json")):
        if json_path.name == "skill.json":
            continue
        if json_path.name == "index.json":
            continue
        if "_pycache_" in json_path.parts:
            continue
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        if "skill_id" not in payload and "name" not in payload and "skill_name" not in payload:
            continue
        skill_id = _normalise_skill_id(
            payload.get("skill_id") or _stable_id_from_dir(json_path, legacy_root.name)
        )
        rel_parts = json_path.relative_to(legacy_root).parts
        category = rel_parts[0] if rel_parts else "uncategorized"
        forwarded = dict(payload)
        forwarded.setdefault("category_path", [category])
        forwarded.setdefault("source", _infer_source(payload, legacy_root.name))
        forwarded["license"] = _infer_license(forwarded, forwarded["source"])
        if not forwarded.get("tier"):
            inferred = _FOLDER_TIER_MAP.get(category)
            if inferred:
                forwarded["tier"] = inferred
        yield {
            "skill_id": skill_id,
            "payload": forwarded,
            "code_path": None,
            "text_path": None,
            "visual_path": None,
            "mtime": json_path.stat().st_mtime,
        }


def _first_match(skill_dir: Path, patterns: Iterable[str]) -> Path | None:
    for pattern in patterns:
        for hit in sorted(skill_dir.glob(pattern)):
            return hit
    return None


def _normalise_skill_id(value: str) -> str:
    out = value.strip().lower().replace("-", "_").replace(" ", "_")
    out = "".join(ch for ch in out if ch.isalnum() or ch == "_")
    if not out:
        return "skill_anon"
    if out[0].isdigit():
        out = f"s_{out}"
    if out[-1] == "_":
        out = out + "x"
    return out


def _stable_id_from_dir(path: Path, domain: str) -> str:
    try:
        rel = path.relative_to(path.parents[1] if len(path.parents) > 1 else path.parent)
    except ValueError:
        rel = path.name
    h = hashlib.sha1(f"{domain}::{rel}".encode()).hexdigest()[:8]
    return f"{path.stem.lower()}_{h}"


def _infer_source(payload: dict[str, Any], domain: str) -> dict[str, Any]:
    src = payload.get("source")
    if isinstance(src, dict) and "type" in src:
        return src
    if isinstance(src, str):
        return {"type": src}
    if "youtube" in str(payload.get("url", "")).lower():
        return {"type": "youtube", "url": payload.get("url")}
    return {"type": "manual"}


_IN_REPO_PERMISSIVE_SOURCES = {"manual", "distilled"}


def _infer_license(payload: dict[str, Any], source_block: dict[str, Any]) -> str | None:
    """Backfill license metadata for legacy skills that don't carry one.

    Assets imported from ``manual`` or ``distilled`` source live in this
    repository and inherit the project's permissive license; we record
    ``"permissive"`` for those so they pass the AC-10 license filter.
    External-source assets (``youtube``, ``github``, ``article``,
    ``static_artifact``) keep the explicit license the connector
    supplied (if any) — and ``None`` correctly excludes them per AC-10.
    """
    declared = payload.get("license")
    if declared is not None:
        return str(declared)
    source_type = (source_block or {}).get("type")
    if source_type in _IN_REPO_PERMISSIVE_SOURCES:
        return "permissive"
    return None


def _canonical_tuple(entry: dict[str, Any]) -> dict[str, Any]:
    """Canonicalised AC-2 tuple for diff detection."""
    return {
        "tier": entry.get("tier"),
        "category_path": list(entry.get("category_path") or []),
        "source_type": (entry.get("source") or {}).get("type"),
        "exec_ok": entry.get("exec_ok"),
        "schema_version": entry.get("schema_version"),
        "wash_version": entry.get("wash_version"),
    }


def _parse_iso(value: str) -> float | None:
    try:
        return time.mktime(time.strptime(value, "%Y-%m-%dT%H:%M:%SZ"))
    except (TypeError, ValueError):
        return None


# Frozen-fixture replay -----------------------------------------------------


def _load_frozen_fixtures(fixtures_dir: Path) -> dict[str, dict[str, Any]]:
    """Load a frozen-fixtures snapshot for deterministic replay assertions.

    Layout:

        fixtures/wash/<domain>_v1/
            <skill_id>.json   # canonical-tuple of the prior wash run

    Returns an empty dict when the directory is missing so callers can
    treat "no fixtures" as "skip replay assertion" rather than "fail".
    """
    if not fixtures_dir.exists():
        return {}
    out: dict[str, dict[str, Any]] = {}
    for path in fixtures_dir.glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict) or "skill_id" not in payload:
            continue
        out[str(payload["skill_id"])] = payload
    return out


def _check_frozen_fixture(
    *, skill_id: str, fixtures: dict[str, dict[str, Any]], registry: WikiRegistry
) -> dict[str, Any] | None:
    """Compare the freshly-washed entry against its frozen fixture.

    Returns a violation dict on canonical-tuple drift, otherwise None.
    """
    fixture = fixtures.get(skill_id)
    if fixture is None:
        return None
    entry = registry.get(skill_id) or {}
    actual = _canonical_tuple(entry)
    expected = {
        "tier": fixture.get("tier"),
        "category_path": list(fixture.get("category_path") or []),
        "source_type": (fixture.get("source") or {}).get("type"),
        "exec_ok": fixture.get("exec_ok"),
        "schema_version": fixture.get("schema_version"),
        "wash_version": fixture.get("wash_version"),
    }
    if actual != expected:
        return {"skill_id": skill_id, "expected": expected, "actual": actual}
    return None


def write_frozen_fixture(
    *, fixtures_dir: Path, registry: WikiRegistry, skill_ids: Iterable[str] | None = None,
) -> int:
    """Write the current registry's canonical tuples out as fixtures.

    Used to seed a frozen-fixtures snapshot from a known-good run; tests
    use this helper rather than hand-curating files.
    """
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    targets = list(skill_ids) if skill_ids is not None else [e["skill_id"] for e in registry.list_entries()]
    written = 0
    for sid in targets:
        entry = registry.get(sid)
        if entry is None:
            continue
        payload = {
            "skill_id": sid,
            "tier": entry.get("tier"),
            "category_path": list(entry.get("category_path") or []),
            "source": entry.get("source") or {},
            "exec_ok": entry.get("exec_ok"),
            "schema_version": entry.get("schema_version"),
            "wash_version": entry.get("wash_version"),
        }
        (fixtures_dir / f"{sid}.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
        written += 1
    return written
