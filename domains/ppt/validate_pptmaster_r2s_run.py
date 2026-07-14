#!/usr/bin/env python3
"""Validate PPTMaster x R2S batch outputs for obvious integration failures.

The validator is intentionally structural. It catches policy failures such as:

- every prompt using the same skill reference set
- every deck collapsing to the same slide/shape signature
- Resource2Skill audit labels leaking into visible slide text
- generic skeleton phrases appearing across most prompts

It does not replace human or VLM visual review.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_FORBIDDEN_VISIBLE = (
    "reference-adapted",
    "w/ skill mechanisms rewritten",
    "skill mechanisms rewritten",
    "audience-ready, source evidence rewritten",
    "end presentation",
    "topic 01",
)

DEFAULT_GENERIC_PHRASES = (
    "five decisions for the room",
    "operating signals",
    "path from plan to proof",
    "approve the focused next step",
    "audience need",
    "core offer",
)

DESIGN_REFS_RE = re.compile(r"design_refs\s*:\s*([^>\n-][^>]*)-->", re.I)
TEXT_RE = re.compile(r"<text\b[^>]*>(.*?)</text>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
NULL_REF_TOKENS = {"none", "no-skills-baseline", "no_skills_baseline", "baseline"}


@dataclass
class DeckRecord:
    case: str
    mode: str
    project: Path | None
    refs: set[str] = field(default_factory=set)
    ref_slide_count: int = 0
    visible_text: str = ""
    shape_signature: tuple[int, ...] = field(default_factory=tuple)
    design_ref_pattern: tuple[tuple[str, ...], ...] = field(default_factory=tuple)
    layout_families: tuple[str, ...] = field(default_factory=tuple)


@dataclass
class ValidationResult:
    ok: bool
    failures: list[str]
    warnings: list[str]
    decks: list[DeckRecord]
    metrics: dict[str, Any]

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "failures": self.failures,
            "warnings": self.warnings,
            "metrics": self.metrics,
            "decks": [
                {
                    "case": d.case,
                    "mode": d.mode,
                    "project": str(d.project) if d.project else "",
                    "refs": sorted(d.refs),
                    "ref_slide_count": d.ref_slide_count,
                    "shape_signature": list(d.shape_signature),
                    "design_ref_pattern": [list(x) for x in d.design_ref_pattern],
                    "layout_families": list(d.layout_families),
                }
                for d in self.decks
            ],
        }


def validate_summary(
    summary_path: Path,
    *,
    mode: str = "w",
    min_refs_per_deck: int = 2,
    min_ref_slides_per_deck: int = 2,
    min_distinct_ref_set_ratio: float = 0.5,
    max_ref_set_share: float = 0.6,
    max_shape_signature_share: float = 0.6,
    max_generic_phrase_case_share: float = 0.6,
    forbidden_visible: tuple[str, ...] = DEFAULT_FORBIDDEN_VISIBLE,
    generic_phrases: tuple[str, ...] = DEFAULT_GENERIC_PHRASES,
) -> ValidationResult:
    entries = _load_entries(summary_path)
    decks = [_inspect_entry(entry, summary_path.parent) for entry in entries if _mode_matches(entry, mode)]

    failures: list[str] = []
    warnings: list[str] = []
    n = len(decks)
    if n == 0:
        return ValidationResult(False, [f"no summary entries matched mode={mode!r}"], [], [], {})

    for deck in decks:
        if deck.layout_families and len(set(deck.layout_families)) < min(4, len(deck.layout_families)):
            failures.append(
                f"{deck.case}: only {len(set(deck.layout_families))} layout families in deck; "
                "expected at least 4 for intra-deck PPTMaster flexibility"
            )
        if len(deck.refs) < min_refs_per_deck:
            failures.append(
                f"{deck.case}: only {len(deck.refs)} unique design refs; expected >= {min_refs_per_deck}"
            )
        if deck.ref_slide_count < min_ref_slides_per_deck:
            failures.append(
                f"{deck.case}: design refs recorded on {deck.ref_slide_count} slides; "
                f"expected >= {min_ref_slides_per_deck}"
            )
        lower_text = deck.visible_text.lower()
        leaked = [phrase for phrase in forbidden_visible if phrase in lower_text]
        if leaked:
            failures.append(f"{deck.case}: visible internal/eval label leaked: {', '.join(leaked)}")

    ref_set_counter = Counter(tuple(sorted(deck.refs)) for deck in decks)
    distinct_ref_sets = len(ref_set_counter)
    min_distinct_ref_sets = max(1, math.ceil(n * min_distinct_ref_set_ratio))
    if distinct_ref_sets < min_distinct_ref_sets:
        failures.append(
            f"reference diversity too low: {distinct_ref_sets} distinct ref sets across {n} decks; "
            f"expected >= {min_distinct_ref_sets}"
        )
    most_common_ref_set, most_common_ref_count = ref_set_counter.most_common(1)[0]
    most_common_ref_share = most_common_ref_count / n
    if n > 1 and most_common_ref_share > max_ref_set_share:
        failures.append(
            f"one ref set dominates {most_common_ref_count}/{n} decks "
            f"({most_common_ref_share:.0%}); refs={list(most_common_ref_set)}"
        )

    shape_counter = Counter(deck.shape_signature for deck in decks if deck.shape_signature)
    most_common_shape_share = 0.0
    if shape_counter:
        most_common_shape, most_common_shape_count = shape_counter.most_common(1)[0]
        most_common_shape_share = most_common_shape_count / n
        if n > 1 and most_common_shape_share > max_shape_signature_share:
            failures.append(
                f"one slide/shape signature dominates {most_common_shape_count}/{n} decks "
                f"({most_common_shape_share:.0%}); signature={list(most_common_shape)}"
            )
    else:
        warnings.append("no shape_count signatures available; skipped shape-collapse check")

    phrase_hits: dict[str, list[str]] = {}
    for phrase in generic_phrases:
        cases = [deck.case for deck in decks if phrase in deck.visible_text.lower()]
        if cases:
            phrase_hits[phrase] = cases
            share = len(cases) / n
            if share > max_generic_phrase_case_share:
                failures.append(
                    f"generic skeleton phrase {phrase!r} appears in {len(cases)}/{n} decks ({share:.0%})"
                )

    metrics = {
        "summary_path": str(summary_path),
        "mode": mode,
        "deck_count": n,
        "distinct_ref_sets": distinct_ref_sets,
        "most_common_ref_set_share": most_common_ref_share,
        "most_common_shape_signature_share": most_common_shape_share,
        "generic_phrase_hits": phrase_hits,
    }
    return ValidationResult(not failures, failures, warnings, decks, metrics)


def validate_open_compare(summary_path: Path) -> ValidationResult:
    """Validate a paired open-PPTMaster `wo` vs R2S-enhanced `w` run."""
    entries = _load_entries(summary_path)
    decks = [_inspect_entry(entry, summary_path.parent) for entry in entries]
    failures: list[str] = []
    warnings: list[str] = []
    by_case: dict[str, dict[str, DeckRecord]] = {}
    for deck in decks:
        by_case.setdefault(deck.case, {})[deck.mode] = deck

    wins = 0
    deltas: dict[str, int] = {}
    for case, pair in sorted(by_case.items()):
        wo = pair.get("wo")
        w = pair.get("w")
        if wo is None or w is None:
            failures.append(f"{case}: expected paired modes wo and w")
            continue
        if wo.refs:
            failures.append(f"{case}: wo baseline leaked refs: {sorted(wo.refs)}")
        if len(w.refs) < 2:
            failures.append(f"{case}: w mode has insufficient refs: {sorted(w.refs)}")
        for deck in (wo, w):
            if deck.layout_families and len(set(deck.layout_families)) < min(4, len(deck.layout_families)):
                failures.append(
                    f"{case}/{deck.mode}: only {len(set(deck.layout_families))} layout families; "
                    "open PPTMaster should vary page topology within a deck"
                )
        delta = sum(w.shape_signature) - sum(wo.shape_signature)
        deltas[case] = delta
        if delta > 0:
            wins += 1
        else:
            failures.append(f"{case}: w is not structurally richer than wo (shape delta {delta})")
        lower_text = w.visible_text.lower() + " " + wo.visible_text.lower()
        leaked = [phrase for phrase in DEFAULT_FORBIDDEN_VISIBLE if phrase in lower_text]
        if leaked:
            failures.append(f"{case}: visible internal/eval label leaked: {', '.join(leaked)}")

    metrics = {
        "summary_path": str(summary_path),
        "paired_cases": len(by_case),
        "w_richer_than_wo": wins,
        "shape_delta_by_case": deltas,
    }
    return ValidationResult(not failures, failures, warnings, decks, metrics)


def _load_entries(summary_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("entries", "results", "decks"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    raise ValueError(f"could not find summary entries in {summary_path}")


def _mode_matches(entry: dict[str, Any], mode: str) -> bool:
    if mode == "*":
        return True
    entry_mode = entry.get("mode")
    return entry_mode == mode or entry_mode is None


def _inspect_entry(entry: dict[str, Any], root: Path) -> DeckRecord:
    project = _resolve_project(entry, root)
    deck = DeckRecord(
        case=str(entry.get("case") or entry.get("variant_id") or entry.get("title") or "unknown"),
        mode=str(entry.get("mode") or ""),
        project=project,
        refs=set(_normalize_refs(entry.get("refs"))),
        shape_signature=tuple(int(x) for x in entry.get("shape_counts") or []),
        layout_families=tuple(str(x) for x in entry.get("layout_families") or []),
    )
    if project and project.exists():
        svg_dir = project / "svg_output"
        notes_dir = project / "notes"
        design_ref_pattern: list[tuple[str, ...]] = []
        texts: list[str] = []
        for svg_path in sorted(svg_dir.glob("*.svg")):
            svg = svg_path.read_text(encoding="utf-8", errors="ignore")
            refs = _extract_design_refs(svg)
            design_ref_pattern.append(tuple(refs))
            deck.refs.update(refs)
            if refs:
                deck.ref_slide_count += 1
            texts.extend(_extract_visible_text(svg))
        for note_path in sorted(notes_dir.glob("*.md")):
            note = note_path.read_text(encoding="utf-8", errors="ignore")
            refs = _extract_note_refs(note)
            deck.refs.update(refs)
        deck.design_ref_pattern = tuple(design_ref_pattern)
        deck.visible_text = " | ".join(texts)
        if not deck.shape_signature:
            deck.shape_signature = _shape_signature_from_svgs(svg_dir)
    return deck


def _resolve_project(entry: dict[str, Any], root: Path) -> Path | None:
    raw = entry.get("project") or entry.get("project_path")
    if not raw:
        return None
    path = Path(str(raw))
    return path if path.is_absolute() else (root / path).resolve()


def _normalize_refs(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        pieces = re.split(r"[,;\s]+", value)
    elif isinstance(value, list):
        pieces = []
        for item in value:
            pieces.extend(_normalize_refs(item))
    else:
        pieces = [str(value)]
    return [x.strip() for x in pieces if x and x.strip()]


def _extract_design_refs(svg: str) -> list[str]:
    refs: list[str] = []
    for match in DESIGN_REFS_RE.finditer(svg):
        raw = match.group(1).split("-->", 1)[0].split(";", 1)[0]
        refs.extend(x for x in _normalize_refs(raw) if x.lower() not in NULL_REF_TOKENS)
    return refs


def _extract_note_refs(note: str) -> list[str]:
    refs: list[str] = []
    for line in note.splitlines():
        if "refs=" in line:
            raw = line.split("refs=", 1)[1].split(";", 1)[0]
            refs.extend(x for x in _normalize_refs(raw) if x.lower() not in NULL_REF_TOKENS)
        if "design_refs:" in line:
            raw = line.split("design_refs:", 1)[1].split(";", 1)[0]
            refs.extend(x for x in _normalize_refs(raw) if x.lower() not in NULL_REF_TOKENS)
    return refs


def _extract_visible_text(svg: str) -> list[str]:
    texts: list[str] = []
    for match in TEXT_RE.finditer(svg):
        value = html.unescape(TAG_RE.sub("", match.group(1))).strip()
        if value:
            texts.append(re.sub(r"\s+", " ", value))
    return texts


def _shape_signature_from_svgs(svg_dir: Path) -> tuple[int, ...]:
    counts: list[int] = []
    for svg_path in sorted(svg_dir.glob("*.svg")):
        svg = svg_path.read_text(encoding="utf-8", errors="ignore")
        counts.append(
            sum(
                len(re.findall(fr"<{tag}\b", svg, re.I))
                for tag in ("rect", "circle", "ellipse", "path", "polygon", "polyline", "line", "text", "image")
            )
        )
    return tuple(counts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", type=Path, help="Path to a PPTMaster/R2S batch summary.json")
    parser.add_argument("--mode", default="w", help="Entry mode to validate; use '*' for all entries")
    parser.add_argument("--compare-open", action="store_true", help="Validate paired wo vs w open-PPTMaster comparison")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)

    result = validate_open_compare(args.summary_json) if args.compare_open else validate_summary(args.summary_json, mode=args.mode)
    if args.json:
        print(json.dumps(result.to_jsonable(), indent=2, ensure_ascii=False))
    else:
        status = "PASS" if result.ok else "FAIL"
        print(f"PPTMaster x R2S validation: {status}")
        print(json.dumps(result.metrics, indent=2, ensure_ascii=False))
        if result.failures:
            print("\nFailures:")
            for item in result.failures:
                print(f"- {item}")
        if result.warnings:
            print("\nWarnings:")
            for item in result.warnings:
                print(f"- {item}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
