"""
core/skill_store.py
Two-level skill storage with domain-driven categorization.

Storage layout per domain:
    skills_library/<domain>/
        index.json                  <- lightweight index
        <category>/
            <skill_id>.json         <- full skill detail
"""
from __future__ import annotations

import json
import os
import re
import time
import hashlib
import logging
import threading
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

log = logging.getLogger("skill_store")
_INDEX_LOCK = threading.Lock()

# Gemini models for classification.
_CLASSIFY_MODELS = [
    "gemini-3.1-pro-preview",
    "gemini-2.5-pro",
    "gemini-2.5-pro-preview-03-25",
    "gemini-2.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite-preview",
]


def _classify_by_keywords(analysis_text: str, category_keywords: dict[str, list[str]]) -> str:
    """Fast zero-API keyword scoring classification."""
    text = analysis_text.lower()
    scores: dict[str, int] = {}
    for cat, keywords in category_keywords.items():
        score = sum(text.count(kw.lower()) for kw in keywords)
        if score:
            scores[cat] = score
    if not scores:
        return "other"
    return max(scores, key=lambda c: scores[c])


def _build_classify_prompt(category_list: list[str], category_keywords: dict[str, list[str]]) -> str:
    """Build a classification prompt from domain categories."""
    lines = ["Based on the skill analysis below, classify this skill into exactly ONE category.\n"]
    lines.append("Available categories:")
    for cat in category_list:
        keywords = category_keywords.get(cat, [])
        examples = ", ".join(keywords[:5]) if keywords else ""
        lines.append(f"- {cat}: {examples}")
    lines.append("\nRespond with ONLY the category name (one word), nothing else.")
    lines.append("\nSkill analysis:\n{analysis}")
    return "\n".join(lines)


def classify_skill(
    analysis_text: str,
    *,
    category_list: list[str],
    category_keywords: dict[str, list[str]],
    model: str = "gemini-2.5-flash",
    api_key: str | None = None,
) -> str:
    """Classify a skill: keyword scoring first, Gemini fallback if 'other'."""
    # Fast keyword pass.
    category = _classify_by_keywords(analysis_text, category_keywords)
    if category != "other":
        return category

    # Gemini fallback.
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return "other"

    client = genai.Client(api_key=key)
    snippet = analysis_text[:2000]
    prompt_template = _build_classify_prompt(category_list, category_keywords)
    prompt = prompt_template.format(analysis=snippet)

    models_to_try = [model] + [m for m in _CLASSIFY_MODELS if m != model]
    for m in models_to_try:
        try:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(model=m, contents=prompt)
                    result = response.text.strip().lower().replace(" ", "_")
                    if result in category_list:
                        return result
                    return "other"
                except Exception as inner:
                    if "429" in str(inner) or "RESOURCE_EXHAUSTED" in str(inner):
                        if attempt == 0:
                            log.warning(f"Rate limited on {m} for classify, trying next model...")
                            break
                    else:
                        raise
        except Exception:
            continue
    return "other"


def _skill_id(skill_name: str, video_url: str) -> str:
    """Generate a stable, unique skill ID."""
    raw = f"{skill_name}::{video_url}"
    short_hash = hashlib.md5(raw.encode()).hexdigest()[:8]
    slug = re.sub(r"[^a-z0-9]+", "_", skill_name.lower()).strip("_")[:40]
    return f"{slug}_{short_hash}"


def _load_index(library_dir: Path) -> dict:
    """Load or create the index file."""
    index_path = library_dir / "index.json"
    if index_path.exists():
        return json.loads(index_path.read_text(encoding="utf-8"))
    return {"updated_at": "", "total": 0, "skills": []}


def _save_index(index: dict, library_dir: Path):
    library_dir.mkdir(parents=True, exist_ok=True)
    index_path = library_dir / "index.json"
    index["updated_at"] = datetime.now().isoformat()
    index["total"] = len(index["skills"])
    index_path.write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def parse_skill_name(analysis_text: str) -> str:
    """Extract the skill name from the Markdown analysis."""
    m = re.search(r"\*\*Skill Name\*\*\s*:\s*(.+)", analysis_text)
    if m:
        name = m.group(1).strip()
        name = re.sub(r"[*`\[\]]+", "", name).strip()
        return name
    return "Unknown Skill"


def store_skill(
    analysis_text: str,
    *,
    domain: str,
    library_dir: Path,
    category_list: list[str],
    category_keywords: dict[str, list[str]],
    video_url: str,
    video_title: str = "",
    video_id: str = "",
    channel: str = "",
    duration_sec: int = 0,
    views: int = 0,
    category: str | None = None,
    frames: list[dict] | None = None,
    model: str = "gemini-2.5-flash",
    api_key: str | None = None,
) -> dict:
    """Parse, categorize, and store a skill analysis.

    Returns:
        The index entry dict for this skill.
    """
    skill_name = parse_skill_name(analysis_text)

    if not category:
        category = classify_skill(
            analysis_text,
            category_list=category_list,
            category_keywords=category_keywords,
            model=model,
            api_key=api_key,
        )

    sid = _skill_id(skill_name, video_url)

    source = {
        "type": "youtube",
        "video_url": video_url,
        "video_id": video_id,
        "video_title": video_title,
        "channel": channel,
        "duration_sec": duration_sec,
        "views": views,
    }

    detail = {
        "skill_id": sid,
        "skill_name": skill_name,
        "domain": domain,
        "category": category,
        "source": source,
        "extracted_at": datetime.now().isoformat(),
        "analysis": analysis_text,
        "frames": frames or [],
    }

    cat_dir = library_dir / category / sid
    cat_dir.mkdir(parents=True, exist_ok=True)
    detail_path = cat_dir / "skill.json"
    detail_path.write_text(
        json.dumps(detail, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    with _INDEX_LOCK:
        index = _load_index(library_dir)
        existing_ids = {s["skill_id"] for s in index["skills"]}
        if sid not in existing_ids:
            index_entry = {
                "skill_id": sid,
                "skill_name": skill_name,
                "category": category,
                "source_video": video_url,
                "source_title": video_title,
                "channel": channel,
                "detail_path": str(detail_path.relative_to(library_dir)),
            }
            index["skills"].append(index_entry)
            _save_index(index, library_dir)

    return {
        "skill_id": sid,
        "skill_name": skill_name,
        "category": category,
        "detail_path": str(detail_path),
    }


def list_skills(library_dir: Path, category: str | None = None) -> list[dict]:
    """List skills from the index, optionally filtered by category."""
    index = _load_index(library_dir)
    skills = index.get("skills", [])
    if category:
        skills = [s for s in skills if s.get("category") == category]
    return skills


def get_skill(library_dir: Path, skill_id: str) -> dict | None:
    """Load a full skill detail by ID.

    Supports both layouts:
      - New: <category>/<skill_id>/skill.json
      - Legacy: <category>/<skill_id>.json
    """
    index = _load_index(library_dir)
    for entry in index.get("skills", []):
        if entry["skill_id"] == skill_id:
            detail_path = library_dir / entry["detail_path"]
            if detail_path.exists():
                data = json.loads(detail_path.read_text(encoding="utf-8"))
                # Attach the skill directory for frame resolution
                data["_skill_dir"] = str(detail_path.parent)
                return data
    return None


def print_index(library_dir: Path, category_list: list[str] | None = None):
    """Pretty-print the skill index grouped by category."""
    index = _load_index(library_dir)
    by_cat: dict[str, list] = {}
    for s in index.get("skills", []):
        cat = s.get("category", "other")
        by_cat.setdefault(cat, []).append(s)

    print(f"Total skills: {index.get('total', 0)}")
    print(f"Last updated: {index.get('updated_at', 'never')}")
    print("=" * 60)

    cats = category_list or sorted(by_cat.keys())
    for cat in cats:
        skills = by_cat.get(cat, [])
        if not skills:
            continue
        print(f"\n[{cat}] ({len(skills)} skills)")
        for s in skills:
            src = s.get("source_title") or s.get("source_video", "")
            print(f"  - {s['skill_name']}")
            print(f"    source: {src}")
