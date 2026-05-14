"""
core/skill_metadata.py
Auto-tag skills with domain-specific metadata.

Domain-agnostic framework — concrete keyword lists and classification
logic are loaded from domain config or provided as arguments.
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

log = logging.getLogger("skill_metadata")


def _count_matches(text: str, keywords: list[str]) -> int:
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def classify_skill_metadata(
    analysis: str,
    category: str,
    *,
    keyword_rules: dict[str, dict] | None = None,
) -> dict:
    """Classify a skill's metadata based on its analysis text.

    Args:
        analysis: Full analysis text.
        category: Skill category.
        keyword_rules: Domain-specific keyword rules dict, e.g.:
            {
                "difficulty": {
                    "advanced": ["complex", "expert", "advanced"],
                    "intermediate": ["moderate", "some experience"],
                    "beginner": ["simple", "easy", "basic"],
                },
                "scope": {
                    "multi_step": ["multiple steps", "sequence", "series"],
                    "single_action": ["single", "one step", "quick"],
                },
            }
            Each field maps value -> keywords. Highest match wins.

    Returns:
        Dict of metadata tags.
    """
    if not keyword_rules:
        return {}

    text = analysis.lower()
    result = {}

    for field_name, value_keywords in keyword_rules.items():
        scores = {}
        for value, keywords in value_keywords.items():
            score = _count_matches(text, keywords)
            if score:
                scores[value] = score

        if scores:
            result[field_name] = max(scores, key=scores.get)
        else:
            # Default to first value in the dict.
            result[field_name] = next(iter(value_keywords.keys()), "unknown")

    return result


def build_metadata(
    library_dir: Path,
    *,
    keyword_rules: dict[str, dict] | None = None,
) -> dict:
    """Tag all skills in a library and write metadata.json."""
    index_path = library_dir / "index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"No index.json at {index_path}")

    index_data = json.loads(index_path.read_text("utf-8"))
    skills = index_data.get("skills", [])
    log.info(f"Tagging {len(skills)} skills...")

    metadata = {}
    for entry in skills:
        sid = entry["skill_id"]
        detail_path = library_dir / entry["detail_path"]
        if not detail_path.exists():
            log.warning(f"Missing detail: {detail_path}, skip")
            continue

        detail = json.loads(detail_path.read_text("utf-8"))
        analysis = detail.get("analysis", "")
        category = entry.get("category", "other")

        tags = classify_skill_metadata(
            analysis, category, keyword_rules=keyword_rules
        )
        metadata[sid] = {
            "skill_id": sid,
            "skill_name": entry.get("skill_name", ""),
            "category": category,
            **tags,
        }

    output = {
        "total": len(metadata),
        "metadata": metadata,
    }

    out_path = library_dir / "metadata.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), "utf-8")
    log.info(f"Saved {len(metadata)} skill metadata to {out_path}")
    return output


def print_stats(library_dir: Path, fields: list[str] | None = None):
    """Print metadata distribution."""
    meta_path = library_dir / "metadata.json"
    if not meta_path.exists():
        print("No metadata.json found. Run --build first.")
        return

    data = json.loads(meta_path.read_text("utf-8"))
    metadata = data["metadata"]
    total = len(metadata)
    print(f"Total skills: {total}\n")

    # Auto-detect fields if not specified.
    if not fields:
        all_keys = set()
        for m in metadata.values():
            all_keys.update(k for k in m.keys() if k not in ("skill_id", "skill_name", "category"))
        fields = sorted(all_keys)

    for field in fields:
        counts: dict[str, int] = {}
        for m in metadata.values():
            val = str(m.get(field, "unknown"))
            counts[val] = counts.get(val, 0) + 1
        print(f"--- {field} ---")
        for val, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {val:20s}: {cnt:4d} ({cnt/total*100:5.1f}%)")
        print()
