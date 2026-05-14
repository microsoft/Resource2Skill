"""CLI handlers for ``cli.py wiki-*`` and ``budget-status`` commands.

Kept separate from cli.py so the top-level dispatcher stays a thin shim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

from .budget import MissingBudgetConfig, load_budget_caps
from .registry import WikiRegistry
from .taxonomy import TaxonomyGate

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_ROOT = PROJECT_ROOT / "skills_wiki"


def _emit(payload: dict[str, Any], *, json_mode: bool) -> None:
    if json_mode:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    if "summary" in payload:
        print(payload["summary"])
        return
    for key, value in payload.items():
        print(f"{key}: {value}")


def _registry(domain: str) -> WikiRegistry:
    root = WIKI_ROOT / domain
    return WikiRegistry(root=root, domain=domain)


def _registry_load(domain: str) -> tuple[WikiRegistry, dict[str, Any]]:
    reg = _registry(domain)
    reg.replay_wal()  # belt and braces in case a prior run died.
    return reg, reg.load(force=True)


def _git_commit() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(PROJECT_ROOT), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8").strip()
    except Exception:  # noqa: BLE001
        return None


# wiki-wash --------------------------------------------------------------

def cmd_wiki_wash(args: argparse.Namespace) -> int:
    """Wash a domain's legacy library into the wiki.

    Walks ``skills_library/<domain>/`` and imports each entry into
    ``skills_wiki/<domain>/`` via the wash pipeline. The deterministic
    pass populates the registry, runs QA, quarantines structurally
    broken entries, and emits ``wash_report.json``. The optional
    Gemini-style enrichment pass (``WASH_USE_GEMINI=1`` +
    ``AZURE_OPENAI_API_KEY``) refines applicability/tags/category from
    the prose context; on any failure the deterministic meta is
    preserved unchanged.
    """
    json_mode = bool(getattr(args, "json", False))

    if args.dry_run:
        _emit(
            {
                "command": "wiki-wash",
                "domain": args.domain,
                "mode": "dry_run",
                "registry_root": str(_registry(args.domain).root),
                "note": "deterministic wash + optional WASH_USE_GEMINI=1 enrichment overlay",
            },
            json_mode=json_mode,
        )
        return 0

    try:
        load_budget_caps()
    except MissingBudgetConfig as exc:
        _emit({"error": str(exc)}, json_mode=json_mode)
        return 2

    # Round-11: when the operator points --frozen-fixtures at an
    # existing directory, fail loudly if it loads zero fixtures rather
    # than silently reporting fixture_violations=0. The directory may
    # legitimately not exist (replay opt-in); we only fail on the
    # exists-but-empty case.
    if args.frozen_fixtures:
        ff_path = Path(args.frozen_fixtures)
        if ff_path.exists():
            from .wash_runners import _load_frozen_fixtures
            loaded = _load_frozen_fixtures(ff_path)
            if not loaded:
                _emit(
                    {
                        "error": (
                            f"frozen-fixtures directory {ff_path} loaded 0 fixtures. "
                            f"Each fixture must be a top-level <skill_id>.json with at "
                            f"least a 'skill_id' key. Re-emit via "
                            f"`wiki-wash --emit-frozen-fixture-update <dir>` after a "
                            f"known-good run."
                        )
                    },
                    json_mode=json_mode,
                )
                return 2

    # Avoid a hard import at module top so domains without a wash adapter
    # do not pull excel/web modules into every cli call.
    from .wash_runners import run_domain_wash, write_frozen_fixture
    from .run_logs import open_run_log, write_event

    try:
        with open_run_log(command="wash", domain=args.domain) as run_log:
            try:
                report = run_domain_wash(
                    domain=args.domain,
                    project_root=PROJECT_ROOT,
                    since=args.since,
                    frozen_fixtures=args.frozen_fixtures,
                )
            except FileNotFoundError as exc:
                write_event(run_log, "error", {"missing_legacy_library": str(exc)})
                _emit({"error": f"legacy library missing: {exc}"}, json_mode=json_mode)
                return 2
            write_event(run_log, "report", report)
    except Exception:
        # Run-log failure must not mask the actual wash result; fall back
        # to the un-logged path so the operator still sees the report.
        try:
            report = run_domain_wash(
                domain=args.domain,
                project_root=PROJECT_ROOT,
                since=args.since,
                frozen_fixtures=args.frozen_fixtures,
            )
        except FileNotFoundError as exc:
            _emit({"error": f"legacy library missing: {exc}"}, json_mode=json_mode)
            return 2
    _emit(
        {
            "command": "wiki-wash",
            "domain": args.domain,
            "report": report,
        },
        json_mode=json_mode,
    )

    # Round-11: emit canonical-tuple fixtures from the now-current
    # registry for every skill the wash touched. This is the documented
    # "regenerate the frozen fixture" path so README guidance lines up
    # with the CLI surface.
    emit_dir = getattr(args, "emit_frozen_fixture_update", None)
    if emit_dir:
        from .registry import WikiRegistry
        target = Path(emit_dir)
        target.mkdir(parents=True, exist_ok=True)
        reg = WikiRegistry(root=PROJECT_ROOT / "skills_wiki" / args.domain, domain=args.domain)
        written = write_frozen_fixture(fixtures_dir=target, registry=reg)
        _emit({"emit_frozen_fixture_update": {"path": str(target), "written": written}},
              json_mode=json_mode)
    # Round-13: convert a budget cap hit into a non-zero exit so the
    # AC-14 contract holds at the command level. The structured
    # cap_reached payload is already in the report.
    if isinstance(report, dict) and report.get("cap_reached"):
        return 2
    return 0


# wiki-audit -------------------------------------------------------------

def cmd_wiki_audit(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    reg = _registry(args.domain)
    payload = reg.load(force=True)
    issues: list[str] = []
    on_disk_dirs = {
        p.name for p in reg.root.iterdir()
        if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")
    }
    indexed_ids = {entry["skill_id"] for entry in payload.get("entries", [])}
    orphan_dirs = sorted(on_disk_dirs - indexed_ids)
    missing_dirs = sorted(indexed_ids - on_disk_dirs)
    schema_versions: set[str] = set()
    wash_versions: set[str] = set()

    # Per-entry consistency: index ↔ meta.json + every referenced path.
    for entry in payload.get("entries", []):
        sid = entry["skill_id"]
        skill_dir = reg.skill_dir(sid)
        meta_path = skill_dir / "meta.json"
        schema_versions.add(str(entry.get("schema_version", "")))
        wash_versions.add(str(entry.get("wash_version", "")))
        if not meta_path.exists():
            issues.append(f"missing meta.json for {sid}")
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"meta.json unparseable for {sid}: {exc}")
            continue
        for field_name in ("tier", "category_path", "skill_name", "license", "exec_ok",
                           "schema_version", "wash_version"):
            if entry.get(field_name) != meta.get(field_name):
                issues.append(
                    f"index/meta divergence for {sid}: {field_name}="
                    f"{entry.get(field_name)!r} vs {meta.get(field_name)!r}"
                )
        # Validate referenced relative paths.
        for relative in _referenced_relative_paths(entry):
            if not (skill_dir / relative).exists():
                issues.append(f"missing referenced file: {sid}/{relative}")

    # Mixed schema/wash versions across the manifest.
    if len({v for v in schema_versions if v}) > 1:
        issues.append(f"mixed schema_version values present: {sorted(schema_versions)}")
    if len({v for v in wash_versions if v}) > 1:
        issues.append(f"mixed wash_version values present: {sorted(wash_versions)}")

    # Direct taxonomy.json mutation detection: every leaf must have a
    # corresponding ``node_history`` row whose path matches.
    taxonomy_issues = _detect_direct_taxonomy_writes(reg.root / "taxonomy.json")
    issues.extend(taxonomy_issues)

    if args.rebuild:
        rebuilt = reg.rebuild_from_meta()
        _emit(
            {
                "command": "wiki-audit",
                "domain": args.domain,
                "rebuilt_entries": len(rebuilt.get("entries", [])),
                "orphan_dirs": orphan_dirs,
                "missing_dirs": missing_dirs,
                "issues": issues,
            },
            json_mode=json_mode,
        )
        return 0
    _emit(
        {
            "command": "wiki-audit",
            "domain": args.domain,
            "indexed_entries": len(indexed_ids),
            "orphan_dirs": orphan_dirs,
            "missing_dirs": missing_dirs,
            "issues": issues,
        },
        json_mode=json_mode,
    )
    return 1 if issues or orphan_dirs or missing_dirs else 0


def _referenced_relative_paths(entry: dict[str, Any]) -> list[str]:
    relative: list[str] = []
    code = entry.get("code") or {}
    if isinstance(code, dict):
        for key in ("path", "signature"):
            value = code.get(key)
            if isinstance(value, str):
                relative.append(value)
        if "callable" in code and "path" not in code:
            # Code declared but no path → legacy-shape entry that should be repaired.
            pass
    text = entry.get("text") or {}
    if isinstance(text, dict):
        value = text.get("overview_path")
        if isinstance(value, str):
            relative.append(value)
    visual = entry.get("visual") or {}
    if isinstance(visual, dict):
        for key in ("thumbnail", "preview"):
            value = visual.get(key)
            if isinstance(value, str):
                relative.append(value)
    return relative


def _detect_direct_taxonomy_writes(taxonomy_path: Path) -> list[str]:
    if not taxonomy_path.exists():
        return []
    try:
        payload = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"taxonomy.json unparseable: {exc}"]
    tree = payload.get("tree", {}) or {}
    history = payload.get("node_history", []) or []
    audited: set[tuple[str, tuple[str, ...]]] = set()
    for row in history:
        if row.get("action") in (None, "create", "rename"):
            audited.add((row.get("tier", ""), tuple(row.get("path", []))))
    issues: list[str] = []
    for tier, subtree in tree.items():
        for path in _walk_tree_leaves(subtree, prefix=()):
            if (tier, path) not in audited:
                issues.append(
                    f"taxonomy node not in node_history (possible direct write): {tier}/{'/'.join(path)}"
                )
    return issues


def _walk_tree_leaves(node: Any, *, prefix: tuple[str, ...]) -> list[tuple[str, ...]]:
    if not isinstance(node, dict):
        return []
    out: list[tuple[str, ...]] = []
    children = [(k, v) for k, v in node.items() if not k.startswith("_")]
    if not children:
        if prefix:
            out.append(prefix)
        return out
    for k, v in children:
        out.extend(_walk_tree_leaves(v, prefix=prefix + (k,)))
    return out


# taxonomy-merge ---------------------------------------------------------

def cmd_taxonomy_merge(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    gate = TaxonomyGate(domain_root=WIKI_ROOT / args.domain)
    pending = gate.read_queue()
    if args.list:
        _emit({"pending": pending}, json_mode=json_mode)
        return 0
    accepted_ids: list[str]
    if args.all:
        accepted_ids = [row["row_id"] for row in pending]
    elif args.row_ids:
        accepted_ids = list(args.row_ids)
    else:
        _emit({"error": "pass --list / --all / --row-ids <id> ..."}, json_mode=json_mode)
        return 2
    rewriter = _build_path_rewriter(args.domain) if args.rewrite_paths else None
    result = gate.apply_merge(
        accepted_row_ids=accepted_ids,
        approver=args.approver or os.environ.get("USER", "operator"),
        path_rewriter=rewriter,
    )
    _emit({
        "command": "taxonomy-merge",
        "domain": args.domain,
        "applied_count": len(result["applied"]),
        "remaining_pending": result["remaining_pending"],
        "rewritten_entries": result.get("rewritten_entries", 0),
    }, json_mode=json_mode)
    return 0


def _build_path_rewriter(domain: str) -> Any:
    """Closure that rewrites entries whose old category_path now maps elsewhere."""
    reg = _registry(domain)
    def rewriter(rewrites: dict[tuple[str, ...], list[str]]) -> int:
        if not rewrites:
            return 0
        n = 0
        for entry in reg.list_entries():
            tier = entry.get("tier", "")
            current = tuple(entry.get("category_path", []))
            for (rule_tier, old_path), new_path in rewrites.items():
                if rule_tier and rule_tier != tier:
                    continue
                if current[: len(old_path)] == old_path:
                    new_full = list(new_path) + list(current[len(old_path) :])
                    if list(current) == new_full:
                        continue
                    entry["category_path"] = new_full
                    skill_dir = reg.skill_dir(entry["skill_id"])
                    meta_path = skill_dir / "meta.json"
                    if meta_path.exists():
                        meta = json.loads(meta_path.read_text(encoding="utf-8"))
                        meta["category_path"] = new_full
                        reg.commit_meta(entry["skill_id"], meta)
                    reg.put(entry, allow_replace=True)
                    n += 1
                    break
        return n
    return rewriter


# source-stats -----------------------------------------------------------

def cmd_source_stats(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    reg, payload = _registry_load(args.domain)
    entries = payload.get("entries", [])
    by_source: Counter[str] = Counter()
    by_tier: Counter[str] = Counter()
    license_counts: Counter[str] = Counter()
    active_count = 0
    exclusion_counts: Counter[str] = Counter()
    quarantine_dir = reg.quarantine_root
    quarantined = 0
    if quarantine_dir.exists():
        quarantined = sum(1 for _ in quarantine_dir.iterdir() if _.is_dir())
    seen_ids: set[str] = set()
    duplicates = 0
    capabilities = _load_capabilities(args.domain)
    cluster_reps = _read_cluster_reps(reg.root)
    demo_verified = 0
    retrieval_verified = 0
    for entry in entries:
        sid = entry["skill_id"]
        if sid in seen_ids:
            duplicates += 1
            exclusion_counts["duplicate_skill_id"] += 1
            continue
        seen_ids.add(sid)
        by_source[(entry.get("source") or {}).get("type", "unknown")] += 1
        by_tier[entry.get("tier", "unknown")] += 1
        license_counts[str(entry.get("license"))] += 1
        if entry.get("demo_verified"):
            demo_verified += 1
        if entry.get("retrieval_verified"):
            retrieval_verified += 1

        active, reason = _full_active_check(
            entry,
            wiki_root=reg.root,
            capabilities=capabilities,
            cluster_reps=cluster_reps,
        )
        if active:
            active_count += 1
        else:
            exclusion_counts[reason or "unknown"] += 1

    payload_out = {
        "command": "source-stats",
        "domain": args.domain,
        "total_indexed": len(entries),
        "active_count": active_count,
        "demo_verified_count": demo_verified,
        "retrieval_verified_count": retrieval_verified,
        "demo_verified_pct": _pct(demo_verified, active_count),
        "retrieval_verified_pct": _pct(retrieval_verified, active_count),
        "quarantined_dirs": quarantined,
        "duplicates": duplicates,
        "filter_breakdown": {
            "exec_ok_false_excluded": exclusion_counts.get("exec_ok_false", 0),
            "license_excluded": exclusion_counts.get("license", 0),
            "name_excluded": exclusion_counts.get("name", 0),
            "overview_too_short_excluded": exclusion_counts.get("overview_too_short", 0),
            "capability_unsupported_excluded": exclusion_counts.get("capability_unsupported", 0),
            "near_duplicate_excluded": exclusion_counts.get("near_duplicate", 0),
            "duplicate_skill_id_excluded": exclusion_counts.get("duplicate_skill_id", 0),
        },
        "by_source": dict(by_source),
        "by_tier": dict(by_tier),
        "by_license": dict(license_counts),
        "active_filters": {
            "exec_ok_not_false": True,
            "license_present_and_not_blocked": True,
            "skill_id_unique": True,
            "skill_name_meaningful_and_overview_length": True,
            "tier_capability_supported": bool(capabilities),
            "embedding_cluster_representative": bool(cluster_reps),
        },
        "source_mix_compliance": _source_mix_compliance(args.domain, by_source),
    }
    _emit(payload_out, json_mode=json_mode)
    return 0


def _pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(100.0 * numerator / denominator, 2)


def _source_mix_compliance(domain: str, by_source: Counter[str]) -> dict[str, Any]:
    """Compare cumulative source mix to a configured target if present."""
    target_path = PROJECT_ROOT / "domains" / domain / "source_mix_target.json"
    if not target_path.exists():
        return {"target_present": False}
    try:
        target = json.loads(target_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"target_present": False, "error": "target file unparseable"}
    total = sum(by_source.values()) or 1
    actual_pct = {k: round(100.0 * v / total, 2) for k, v in by_source.items()}
    deltas: dict[str, float] = {}
    non_compliant = False
    for source_type, expected_pct in target.items():
        observed = actual_pct.get(source_type, 0.0)
        delta = round(observed - float(expected_pct), 2)
        deltas[source_type] = delta
        if abs(delta) > 15.0:
            non_compliant = True
    return {
        "target_present": True,
        "target_pct": target,
        "actual_pct": actual_pct,
        "deltas_pp": deltas,
        "non_compliant": non_compliant,
    }


def _full_active_check(
    entry: dict[str, Any], *, wiki_root: Path, capabilities: dict[str, Any] | None,
    cluster_reps: dict[str, str] | None,
) -> tuple[bool, str | None]:
    if entry.get("exec_ok") is False:
        return False, "exec_ok_false"
    license_value = entry.get("license")
    if license_value in (None, "blocked"):
        return False, "license"
    name = entry.get("skill_name")
    if name in (None, "", "unknown_skill"):
        return False, "name"
    skill_dir = wiki_root / entry["skill_id"]
    overview = skill_dir / "text" / "overview.md"
    if overview.exists():
        if len(overview.read_text(encoding="utf-8", errors="ignore")) < 200:
            return False, "overview_too_short"
    else:
        # Treat absent overview as too short for "active" purposes; the entry
        # is still in the index but does not count toward the 500 floor.
        return False, "overview_too_short"
    if capabilities is not None:
        tier = entry.get("tier", "")
        verbs = (capabilities.get("tier_to_verbs") or {}).get(tier) or []
        if tier in {"T1", "T2"}:
            if not verbs and not capabilities.get("reference_only_supported", True):
                return False, "capability_unsupported"
        else:
            if not verbs:
                return False, "capability_unsupported"
    if cluster_reps is not None:
        rep = cluster_reps.get(entry["skill_id"])
        if rep is not None and rep != entry["skill_id"]:
            return False, "near_duplicate"
    return True, None


def _load_capabilities(domain: str) -> dict[str, Any] | None:
    path = PROJECT_ROOT / "domains" / domain / "capabilities.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _read_cluster_reps(wiki_root: Path) -> dict[str, str] | None:
    path = wiki_root / "cluster_representatives.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


# wiki-backfill ----------------------------------------------------------

def cmd_wiki_backfill(args: argparse.Namespace) -> int:
    """Backfill ``source.type`` and ``license`` on existing wiki entries
    and route blocked / missing-license entries into ``_quarantine/``.

    The wash pipeline already infers these fields on first import, but
    legacy entries written before the inference logic existed (or
    written with ``license: null``) need a sweep pass. This command
    walks ``skills_wiki/<domain>/*/meta.json`` and:

    * routes any entry with ``license`` in ``{None, "blocked"}`` to
      ``_quarantine/`` with reason ``license_backfill: <value>``,
    * fills ``source.type`` from the URL when the field is missing
      (``youtube`` / ``github`` / ``article`` heuristics) and otherwise
      defaults to ``manual``,
    * leaves entries that already have a permissive license + a
      source.type unchanged.

    A ``--dry-run`` mode classifies but performs no writes; the JSON
    payload reports what *would* have changed so operators can sanity
    check before sweeping.
    """
    json_mode = bool(getattr(args, "json", False))
    dry_run = bool(getattr(args, "dry_run", False))
    reg = _registry(args.domain)
    payload = reg.load(force=True)
    entries = list(payload.get("entries", []))

    quarantined: list[dict[str, Any]] = []
    source_filled: list[dict[str, Any]] = []
    license_unchanged = 0

    for entry in entries:
        sid = entry["skill_id"]
        meta_path = reg.skill_dir(sid) / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        license_value = meta.get("license")
        if license_value in (None, "blocked"):
            quarantined.append({"skill_id": sid, "license": license_value})
            if not dry_run:
                reg.quarantine(
                    sid,
                    reason=f"license_backfill: {license_value!r}",
                    payload=meta,
                )
            continue
        # License OK; check whether source.type needs backfill.
        source_block = meta.get("source") or {}
        if not source_block.get("type"):
            inferred = _infer_source_type_from_url(meta.get("source_url")
                                                   or source_block.get("url") or "")
            source_filled.append({"skill_id": sid, "from": source_block.get("type"),
                                  "to": inferred})
            if not dry_run:
                meta["source"] = {**source_block, "type": inferred}
                reg.commit_meta(sid, meta)
                # Index row also carries source.type as a top-level key
                # in some shapes, so update via put() to keep audit clean.
                from .registry import SkillEntry
                reg.put(SkillEntry(skill_id=sid, data=meta), allow_replace=True)
        else:
            license_unchanged += 1

    report = {
        "command": "wiki-backfill",
        "domain": args.domain,
        "dry_run": dry_run,
        "scanned": len(entries),
        "quarantined": len(quarantined),
        "quarantined_skills": quarantined[:50],
        "source_type_backfilled": len(source_filled),
        "source_type_changes": source_filled[:50],
        "unchanged": license_unchanged,
    }
    _emit(report, json_mode=json_mode)
    return 0


def _infer_source_type_from_url(url: str) -> str:
    """Heuristic-only source.type inference from a URL string."""
    s = (url or "").lower()
    if "youtube.com" in s or "youtu.be" in s:
        return "youtube"
    if "github.com" in s or "raw.githubusercontent.com" in s:
        return "github"
    if s.startswith("http://") or s.startswith("https://"):
        return "article"
    return "manual"


# snapshot ---------------------------------------------------------------

def cmd_snapshot(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    reg = _registry(args.domain)
    if not args.allow_dirty and _git_dirty():
        _emit({"error": "working tree is dirty; pass --allow-dirty to override"}, json_mode=json_mode)
        return 2
    snap_root = PROJECT_ROOT / "snapshots" / args.domain / args.tag
    snap_root.mkdir(parents=True, exist_ok=True)
    digests: dict[str, str | None] = {}
    for name in ("index.json", "taxonomy.json", "embeddings.meta.json"):
        path = reg.root / name
        digests[name] = _digest(path) if path.exists() else None
    manifest = {
        "domain": args.domain,
        "tag": args.tag,
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": _git_commit(),
        "digests": digests,
    }
    (snap_root / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    # Reproducibility artefact: append the snapshot manifest into the
    # per-run log so operators can audit which snapshots came from which
    # run (the plan's logs/<command>_<timestamp>/<domain>.log convention).
    try:
        from .run_logs import open_run_log, write_event
        with open_run_log(command="snapshot", domain=args.domain) as run_log:
            write_event(run_log, "snapshot", manifest)
    except Exception:  # noqa: BLE001
        pass
    _emit({"command": "snapshot", "domain": args.domain, "tag": args.tag, "manifest": manifest}, json_mode=json_mode)
    return 0


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(64 * 1024), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def _git_dirty() -> bool:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(PROJECT_ROOT), "status", "--porcelain"],
            stderr=subprocess.DEVNULL,
        )
        return bool(out.strip())
    except Exception:  # noqa: BLE001
        return False


# budget-status ----------------------------------------------------------

def cmd_budget_status(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    try:
        cap = load_budget_caps()
    except MissingBudgetConfig as exc:
        _emit({"error": str(exc)}, json_mode=json_mode)
        return 2
    reg = _registry(args.domain)
    cap_files = sorted(reg.root.glob("cap_reached_*.json"))
    history: list[dict[str, Any]] = []
    for cap_path in cap_files[-5:]:
        try:
            history.append(json.loads(cap_path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    payload = {
        "command": "budget-status",
        "domain": args.domain,
        "caps": {
            "gemini_call_cap_per_run": cap.gemini_call_cap_per_run,
            "gemini_call_cap_per_domain_per_day": cap.gemini_call_cap_per_domain_per_day,
            "wall_clock_cap_minutes_per_run": cap.wall_clock_cap_minutes_per_run,
        },
        "recent_cap_reached": history,
    }
    _emit(payload, json_mode=json_mode)
    return 0


# Argparse hookup --------------------------------------------------------

def register_subparsers(sub: Any) -> None:
    p = sub.add_parser("wiki-wash", help="Run the wiki wash pipeline (deterministic pass)")
    p.add_argument("--domain", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--frozen-fixtures", default=None,
                   help="Path to a frozen-fixtures dir for deterministic replay (later rounds)")
    p.add_argument("--emit-frozen-fixture-update", default=None,
                   help="After the wash, emit canonical-tuple fixtures for every washed "
                        "skill into this directory (overwrites). Use to refresh "
                        "frozen-fixtures snapshots when wash output legitimately changes.")
    p.add_argument("--since", default=None, help="ISO timestamp; only re-wash entries changed after")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_wiki_wash)

    p = sub.add_parser("wiki-audit", help="Audit and optionally rebuild the wiki index for a domain")
    p.add_argument("--domain", required=True)
    p.add_argument("--rebuild", action="store_true", help="Rebuild index.json from per-skill meta.json")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_wiki_audit)

    p = sub.add_parser("taxonomy-merge", help="Apply approved taxonomy proposals")
    p.add_argument("--domain", required=True)
    p.add_argument("--list", action="store_true", help="List pending proposals")
    p.add_argument("--all", action="store_true", help="Approve all pending proposals")
    p.add_argument("--row-ids", nargs="*", help="Specific proposal row ids to approve")
    p.add_argument("--approver", default=None)
    p.add_argument("--rewrite-paths", action="store_true",
                   help="Also rewrite affected entries' category_path (mandatory for renames/merges)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_taxonomy_merge)

    p = sub.add_parser("source-stats", help="Cumulative source-mix and active-count summary")
    p.add_argument("--domain", required=True)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_source_stats)

    p = sub.add_parser("snapshot", help="Capture a registry snapshot manifest")
    p.add_argument("--domain", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--allow-dirty", action="store_true", help="Allow snapshot under uncommitted changes")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_snapshot)

    p = sub.add_parser("budget-status", help="Show configured caps and recent cap-reached events")
    p.add_argument("--domain", required=True)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_budget_status)

    p = sub.add_parser(
        "wiki-backfill",
        help="Backfill source.type and license on existing entries; "
             "quarantine blocked / missing-license skills",
    )
    p.add_argument("--domain", required=True)
    p.add_argument("--dry-run", action="store_true",
                   help="Report what would change without writing")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_wiki_backfill)


__all__ = ["register_subparsers"]
