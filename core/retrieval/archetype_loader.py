"""
core/retrieval/archetype_loader.py — load deck archetype YAML files.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from core.extraction.schemas import DeckArchetype, validate_archetype_dict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ARCHETYPES_DIR = _PROJECT_ROOT / "skills_library" / "ppt" / "deck_archetypes"


@lru_cache(maxsize=None)
def load_archetype(archetype_id: str) -> dict:
    """Load an archetype YAML and return as dict (validated via pydantic)."""
    path = _ARCHETYPES_DIR / f"{archetype_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Archetype '{archetype_id}' not found at {path}")
    data = yaml.safe_load(path.read_text())
    validate_archetype_dict(data)
    return data


def list_archetypes() -> list[dict[str, Any]]:
    """Return summary cards for all archetypes."""
    out = []
    for p in sorted(_ARCHETYPES_DIR.glob("*.yaml")):
        data = yaml.safe_load(p.read_text())
        try:
            validate_archetype_dict(data)
        except Exception as e:
            out.append({"archetype_id": data.get("archetype_id", p.stem), "error": str(e)})
            continue
        total_slides = sum(len(s.get("slides", [])) for s in data.get("sections", []))
        section_names = [s["section"] for s in data.get("sections", [])]
        out.append({
            "archetype_id": data["archetype_id"],
            "name": data["name"],
            "description": data.get("description", "").strip(),
            "suggested_slides": data.get("suggested_slides", total_slides),
            "actual_slide_count": total_slides,
            "sections": section_names,
            "recommended_themes": data.get("recommended_themes", []),
        })
    return out


__all__ = ["load_archetype", "list_archetypes"]
