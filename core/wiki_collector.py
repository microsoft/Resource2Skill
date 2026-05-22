"""Connector-driven collection cycle that writes into ``skills_wiki/<d>/``.

This is the new path the Skill Wiki spec requires. ``run_connector_cycle``
takes a list of ``SourceConnector`` instances, a per-cycle quota, and a
source-mix policy. Per-source quotas are computed from the mix; YouTube
quotas hard-fail when unmet, the rest soft-fail. Every candidate the
connectors return is washed through the wiki pipeline; ``license is None``
or ``license == "blocked"`` routes to ``_quarantine/``.

Round-11: connector-supplied ``code_text`` / ``text_overview`` /
``visual_path`` are materialized into temp files and threaded through
``wash_legacy_skill`` as ``code_path`` / ``text_path`` / ``visual_path``
so the connector content lands inside the washed skill directory
instead of being silently dropped.

Legacy ``core/auto_collect.py`` still drives the old per-domain
YouTube-only path; this module is the new path that ``cli.py collect``
calls when ``library_backend: wiki`` is set.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from core.skill_wiki.budget import BudgetExceeded, BudgetTracker, load_budget_caps
from core.skill_wiki.registry import WikiRegistry, _utc_now
from core.skill_wiki.wash import wash_legacy_skill, write_wash_report, WashStats
from core.sources import CandidateSkill, SourceConnector


@dataclass
class CycleReport:
    domain: str
    cycle_quota: int
    source_mix: dict[str, int]
    acquired: dict[str, int] = field(default_factory=dict)
    fill_rate: dict[str, float] = field(default_factory=dict)
    failed_hard: list[str] = field(default_factory=list)
    quarantined: int = 0
    washed: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)
    cap_reached: dict[str, Any] | None = None
    ts: str = field(default_factory=_utc_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "cycle_quota": self.cycle_quota,
            "source_mix_target": self.source_mix,
            "acquired": dict(self.acquired),
            "fill_rate": dict(self.fill_rate),
            "failed_hard": list(self.failed_hard),
            "quarantined": self.quarantined,
            "washed": self.washed,
            "errors": self.errors[:25],
            "cap_reached": self.cap_reached,
            "ts": self.ts,
        }


def parse_source_mix(mix_string: str) -> dict[str, int]:
    """Parse ``"youtube=80,github=5,article=5,static=10"`` into a dict.

    The canonical key for the static-artifact connector is
    ``static_artifact``; ``static`` is accepted as an alias because the
    spec command line uses it.
    """
    aliases = {"static": "static_artifact"}
    out: dict[str, int] = {}
    for chunk in mix_string.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise ValueError(f"invalid source-mix entry: {chunk!r}")
        key, val = chunk.split("=", 1)
        key = aliases.get(key.strip(), key.strip())
        try:
            out[key] = int(val.strip())
        except ValueError as exc:
            raise ValueError(f"invalid source-mix percentage: {chunk!r}") from exc
    if sum(out.values()) <= 0:
        raise ValueError("source-mix must declare at least one positive quota")
    return out


def run_connector_cycle(
    *,
    domain: str,
    connectors: list[SourceConnector],
    cycle_quota: int,
    source_mix: dict[str, int],
    project_root: Path,
    extras: dict[str, Any] | None = None,
) -> CycleReport:
    """Run one collection cycle against ``connectors``.

    The function:
      1. Loads + enforces the per-run budget cap precondition.
      2. Computes per-source quotas from ``source_mix`` proportions.
      3. Calls each connector's ``acquire``; YouTube hard-fails on zero,
         others log a warning.
      4. Washes every candidate into ``skills_wiki/<domain>/``; entries
         with ``license is None`` or ``"blocked"`` quarantine.
      5. Returns a structured ``CycleReport``.
    """
    extras = extras or {}
    cap = load_budget_caps()
    wiki_root = project_root / "skills_wiki" / domain
    registry = WikiRegistry(root=wiki_root, domain=domain)
    cycle_id = f"cycle_{int(time.time())}"
    tracker = BudgetTracker(
        cap=cap, domain=domain, run_id=cycle_id,
        cap_reached_path=wiki_root / f"cap_reached_{cycle_id}.json",
    )

    by_type = {c.source_type: c for c in connectors}
    quotas = _allocate_quotas(cycle_quota=cycle_quota, source_mix=source_mix)
    report = CycleReport(domain=domain, cycle_quota=cycle_quota, source_mix=quotas)
    # Round-13: register pending at SOURCE-type granularity for the
    # acquire phase only. Once candidates are gathered we re-register
    # at skill-id granularity below so cap_reached.remaining lists
    # actual skill ids rather than source labels (Codex finding 2).
    tracker.register_pending([{"id": st} for st in quotas])

    candidates: list[CandidateSkill] = []
    cap_reached_during_acquire = False
    cap_source_idx: int | None = None
    quota_keys = list(quotas.keys())
    for idx, source_type in enumerate(quota_keys):
        quota = quotas[source_type]
        if quota <= 0:
            report.acquired[source_type] = 0
            report.fill_rate[source_type] = 0.0
            continue
        connector = by_type.get(source_type)
        if connector is None:
            report.acquired[source_type] = 0
            report.fill_rate[source_type] = 0.0
            if source_type == "youtube":
                report.failed_hard.append(f"no connector available for required source: {source_type}")
            continue
        try:
            # Round-12: thread the cycle BudgetTracker into every
            # connector via kwargs so model-backed connectors can
            # consume the per-run budget cap. Connectors that don't
            # use it silently ignore the kwarg.
            acquired = connector.acquire(
                domain=domain, quota=quota, budget_tracker=tracker, **extras,
            )
        except BudgetExceeded as exc:
            # A cap-reached BudgetExceeded raised by a connector
            # during acquire is a real cap event, not a generic
            # connector error. Capture the structured payload, stop
            # the cycle, and persist the cap_reached file so
            # cli.py collect returns exit code 2.
            report.cap_reached = dict(exc.payload)
            report.acquired[source_type] = 0
            report.fill_rate[source_type] = 0.0
            cap_reached_during_acquire = True
            cap_source_idx = idx
            break
        except Exception as exc:  # noqa: BLE001
            report.errors.append({"source_type": source_type, "error": f"{type(exc).__name__}: {exc}"})
            acquired = []
        report.acquired[source_type] = len(acquired)
        report.fill_rate[source_type] = round(len(acquired) / quota, 3) if quota else 0.0
        if source_type == "youtube" and len(acquired) == 0 and quota > 0:
            report.failed_hard.append("youtube quota unmet (hard-fail policy)")
        candidates.extend(acquired)
        tracker.mark_completed(source_type)

    if cap_reached_during_acquire:
        # Build the unified remaining-work payload: every already
        # acquired-but-unwashed candidate skill_id plus the
        # not-yet-run acquire units (the source type that tripped
        # the cap and any subsequent ones). This gives operators a
        # single enumerable list of unprocessed work in
        # cap_reached_<run_id>.json, regardless of whether the cap
        # fired during a connector that already had earlier siblings
        # succeed.
        unified_remaining: list[dict[str, Any]] = []
        for cand in candidates:
            unified_remaining.append({"id": cand.skill_id, "kind": "candidate",
                                      "source_type": cand.source_type})
        if cap_source_idx is not None:
            for st in quota_keys[cap_source_idx:]:
                # Skip later sources that rounded down to quota 0:
                # they were never going to do work, so listing them
                # in remaining overstates the cap payload (Codex
                # Round 16 small-cycle reproducer: cycle_quota=1,
                # mix={youtube:80, github:5, article:5,
                # static_artifact:10} → only youtube has positive
                # quota, the other three round down to 0).
                if quotas.get(st, 0) <= 0:
                    continue
                unified_remaining.append({"id": st, "kind": "source_type"})
        report.cap_reached["remaining"] = unified_remaining
        report.cap_reached.setdefault("domain", domain)
        report.cap_reached.setdefault("run_id", cycle_id)
        # Some connectors raise BudgetExceeded directly without
        # going through BudgetTracker._raise(), which means
        # cap_reached_<run_id>.json may not have been written. Make
        # the artifact unconditional here so downstream tooling can
        # always find it after a cap event.
        cap_reached_path = wiki_root / f"cap_reached_{cycle_id}.json"
        cap_reached_path.parent.mkdir(parents=True, exist_ok=True)
        cap_reached_path.write_text(
            json.dumps(report.cap_reached, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        write_wash_report(root=wiki_root, stats=WashStats(), run_id=cycle_id, domain=domain)
        report_path = wiki_root / f"cycle_report_{cycle_id}.json"
        report_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        try:
            from core.skill_wiki.run_logs import open_run_log, write_event
            with open_run_log(command="collect", domain=domain, project_root=project_root) as run_log:
                write_event(run_log, "cycle_report", report.to_dict())
        except Exception:  # noqa: BLE001
            pass
        return report

    # Round-13: re-register pending at candidate granularity so a
    # mid-cycle cap hit emits cap_reached.remaining = [skill_id, ...]
    # rather than [source_type, ...].
    tracker.register_pending([{"id": cand.skill_id} for cand in candidates])

    # Round-13: re-register pending at candidate granularity so a
    # mid-cycle cap hit emits cap_reached.remaining = [skill_id, ...]
    # rather than [source_type, ...].
    tracker.register_pending([{"id": cand.skill_id} for cand in candidates])

    # Wash each candidate; license==null or blocked quarantines without
    # entering the index.
    stats = WashStats()
    for cand in candidates:
        try:
            tracker.check()
        except BudgetExceeded as exc:
            report.cap_reached = exc.payload
            break
        license_value = cand.license
        if license_value in (None, "blocked"):
            registry.quarantine(
                cand.skill_id,
                reason=f"license_excluded: {license_value!r}",
                payload=cand.to_legacy_payload(),
            )
            report.quarantined += 1
            tracker.mark_completed(cand.skill_id)
            continue
        try:
            outcome = _wash_candidate(cand, registry=registry, budget_tracker=tracker)
        except BudgetExceeded as exc:
            report.cap_reached = exc.payload
            break
        tracker.mark_completed(cand.skill_id)
        if outcome["status"] == "quarantined":
            report.quarantined += 1
            stats.quarantined += 1
            stats.errors.append(outcome)
        else:
            report.washed += 1
            stats.washed += 1

    # Persist artefacts.
    write_wash_report(root=wiki_root, stats=stats, run_id=cycle_id, domain=domain)
    report_path = wiki_root / f"cycle_report_{cycle_id}.json"
    report_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    # Per-run reproducibility log under logs/collect_<ts>/<domain>.log.
    try:
        from core.skill_wiki.run_logs import open_run_log, write_event
        with open_run_log(command="collect", domain=domain, project_root=project_root) as run_log:
            write_event(run_log, "cycle_report", report.to_dict())
    except Exception:  # noqa: BLE001
        pass
    return report


def _allocate_quotas(*, cycle_quota: int, source_mix: dict[str, int]) -> dict[str, int]:
    total = sum(source_mix.values())
    if total <= 0:
        return {k: 0 for k in source_mix}
    out: dict[str, int] = {}
    allocated = 0
    keys = list(source_mix.keys())
    for key in keys[:-1]:
        share = int(round(cycle_quota * (source_mix[key] / total)))
        out[key] = share
        allocated += share
    out[keys[-1]] = max(0, cycle_quota - allocated)
    return out


__all__ = [
    "CandidateSkill",
    "CycleReport",
    "parse_source_mix",
    "run_connector_cycle",
]


def _resolve_temp_root() -> str | None:
    """Return a writable directory for connector materialization scratch.

    Order of preference: ``/data/tmp`` (the project convention from
    CLAUDE.md) when it exists AND is writable; otherwise None so
    ``tempfile.mkdtemp`` falls back to the system default. Round-12
    fix: previous version returned ``"/data/tmp"`` whenever the
    directory existed, which broke in environments where the path was
    read-only (Codex's reproducer)."""
    candidate = Path("/data/tmp")
    if candidate.exists():
        try:
            probe = candidate / f"._wash_candidate_probe_{os.getpid()}"
            probe.write_text("x")
            probe.unlink()
            return str(candidate)
        except OSError:
            return None
    return None


def _wash_candidate(cand: CandidateSkill, *, registry: WikiRegistry,
                    budget_tracker: "BudgetTracker | None" = None) -> dict[str, Any]:
    """Materialize candidate.code_text / text_overview / visual_path into a
    temp dir then call ``wash_legacy_skill`` with real ``code_path`` /
    ``text_path`` / ``visual_path``.

    Round-11: closes the connector→wash content drop.
    Round-12: temp-root robust to read-only ``/data/tmp`` environments;
    threads the cycle BudgetTracker into ``wash_legacy_skill`` so the
    enrichment path consumes the real cap.
    """
    tmp = Path(tempfile.mkdtemp(prefix="wash_cand_", dir=_resolve_temp_root()))
    code_path: Path | None = None
    text_path: Path | None = None
    visual_path: Path | None = None
    try:
        if cand.code_text is not None:
            filename = cand.code_filename or "skill.py"
            cp = tmp / filename
            cp.write_text(cand.code_text, encoding="utf-8")
            code_path = cp
        if cand.text_overview:
            tp = tmp / "overview.md"
            tp.write_text(cand.text_overview, encoding="utf-8")
            text_path = tp
        if cand.visual_path and Path(cand.visual_path).exists():
            visual_path = Path(cand.visual_path)
        return wash_legacy_skill(
            registry=registry,
            skill_id=cand.skill_id,
            legacy_payload=cand.to_legacy_payload(),
            code_path=code_path,
            text_path=text_path,
            visual_path=visual_path,
            require_signature_when_code_present=False,
            budget_tracker=budget_tracker,
        )
    finally:
        try:
            shutil.rmtree(tmp, ignore_errors=True)
        except Exception:  # noqa: BLE001
            pass
