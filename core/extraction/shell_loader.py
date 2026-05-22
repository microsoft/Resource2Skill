"""
core/extraction/shell_loader.py

Load Theme JSONs and Shell Python modules from skills_library/ppt/.
This is the bridge between on-disk artifacts and agent/MCP consumers.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

from .schemas import Theme, validate_theme_dict


_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_THEMES_DIR = _PROJECT_ROOT / "skills_library" / "ppt" / "themes"
_SHELLS_DIR = _PROJECT_ROOT / "skills_library" / "ppt" / "shells_seed"
_DISTILLED_DIR = _PROJECT_ROOT / "skills_library" / "ppt" / "shells_distilled"


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def load_theme(theme_id: str) -> dict:
    """Load a theme JSON and return it as a plain dict (shells use dict access)."""
    path = _THEMES_DIR / f"{theme_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Theme '{theme_id}' not found at {path}")
    data = json.loads(path.read_text())
    # Validate via pydantic but return dict (shells don't need model objects)
    validate_theme_dict(data)
    return data


def list_themes() -> list[dict[str, Any]]:
    """Return a list of theme summary cards (for LLM picker).

    Surfaces the LLM-readable `mood` and `archetype_fit` metadata so the
    agent can filter themes by brief without reading the full JSON.
    """
    out = []
    for p in sorted(_THEMES_DIR.glob("*.json")):
        data = json.loads(p.read_text())
        bg_hex = data["palette"]["bg"]
        mode = "dark" if _is_dark_hex(bg_hex) else "light"
        out.append({
            "theme_id": data["theme_id"],
            "name": data["name"],
            "palette_preview": [
                bg_hex, data["palette"]["accent"],
                data["palette"]["accent2"], data["palette"]["text"],
            ],
            "motion_personality": data.get("motion", {}).get("personality", "editorial"),
            "motif": data.get("motif", {}).get("type", "none"),
            "font_primary": list(data.get("typography", {}).values())[0].get("font", "Inter")
                            if data.get("typography") else "Inter",
            "mood": data.get("mood", []),
            "archetype_fit": data.get("archetype_fit", []),
            "mode": mode,
        })
    return out


def _is_dark_hex(hex_str: str) -> bool:
    """True if the hex color is visually dark (luminance < 0.5)."""
    s = hex_str.lstrip("#")
    if len(s) != 6:
        return True
    r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
    return lum < 0.5


# ---------------------------------------------------------------------------
# Shells
# ---------------------------------------------------------------------------


# Ensure the shells_seed directory is importable so shell modules can import
# from `_shell_helpers`.
if str(_SHELLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SHELLS_DIR))


@lru_cache(maxsize=None)
def load_shell(shell_id: str):
    """Load a shell's render() function by id. Searches seed dir first, then distilled."""
    path = _SHELLS_DIR / f"{shell_id}.py"
    if not path.exists():
        # Try distilled shells (each lives at shells_distilled/<id>/render.py)
        cand = _DISTILLED_DIR / shell_id / "render.py"
        if cand.exists():
            path = cand
        else:
            raise FileNotFoundError(f"Shell '{shell_id}' not found in seed or distilled dirs")
    spec = importlib.util.spec_from_file_location(f"shell_{shell_id}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not build import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "render"):
        raise AttributeError(f"Shell '{shell_id}' has no render() function")
    return module


def list_shells(include_distilled: bool = True) -> list[dict[str, Any]]:
    """Return shell summary cards for retrieval/listing."""
    # Load demoted list (seeds that fail the overlap gate)
    demoted_seeds: set[str] = set()
    demoted_file = _PROJECT_ROOT / "skills_library" / "ppt" / "shells_demoted.json"
    if demoted_file.exists():
        try:
            for d in json.loads(demoted_file.read_text()):
                if d.get("source") == "seed":
                    demoted_seeds.add(d["shell_id"])
        except Exception:
            pass

    out = []
    for p in sorted(_SHELLS_DIR.glob("*.py")):
        if p.stem.startswith("_"):
            continue
        try:
            mod = load_shell(p.stem)
        except Exception as e:
            out.append({"shell_id": p.stem, "error": str(e)})
            continue
        slots = getattr(mod, "SLOTS", [])
        doc = (mod.__doc__ or "").strip().split("\n")[0]
        role_tags = _derive_role_tags(p.stem)
        status = "candidate" if p.stem in demoted_seeds else "active"
        ambient_capable = _seed_shell_ambient_capable(p)
        # LLM-readable metadata (added 2026-04-19)
        shell_role = getattr(mod, "ROLE", "") or (role_tags[0] if role_tags else "")
        out.append({
            "shell_id": p.stem,
            "source": "seed",
            "doc": doc,
            "description": getattr(mod, "DESCRIPTION", doc),
            "role": shell_role,
            "archetype": getattr(mod, "ARCHETYPE", ""),
            "mood": list(getattr(mod, "MOOD", []) or []),
            "density": getattr(mod, "DENSITY", "balanced"),
            "style_tags": list(getattr(mod, "STYLE_TAGS", []) or []),
            "slot_names": [s["name"] for s in slots],
            "required_slots": [s["name"] for s in slots if s.get("required")],
            "slots": slots,
            "intent_tags": {"slide_role": role_tags, "compatible_themes": []},
            "status": status,
            "ambient_capable": ambient_capable,
        })
    if include_distilled and _DISTILLED_DIR.exists():
        for d in sorted(_DISTILLED_DIR.iterdir()):
            skill_json = d / "skill.json"
            if not skill_json.exists():
                continue
            try:
                meta = json.loads(skill_json.read_text())
            except Exception as e:
                out.append({"shell_id": d.name, "error": str(e)})
                continue
            tags = meta.get("intent_tags", {}) or {}
            ambient_capable = bool(tags.get("ambient_capable"))
            if not ambient_capable:
                ambient_capable = _distilled_shell_ambient_capable(d)
            # Lift mood from intent_tags; translate distilled mood vocab
            # to the unified vocabulary used by seed shells / motions / themes.
            raw_mood = [m.lower() for m in (tags.get("mood") or [])]
            mood = _translate_mood(raw_mood)
            role_tags = tags.get("slide_role") or []
            role_tags = [_ROLE_ALIAS.get(r, r) for r in role_tags]
            role = role_tags[0] if role_tags else ""
            density_raw = (tags.get("density") or "").lower()
            density = {"low": "sparse", "medium": "balanced",
                        "high": "dense"}.get(density_raw, density_raw or "balanced")
            archetype = _infer_archetype_from_tags(mood, role_tags)
            out.append({
                "shell_id": meta["skill_id"],
                "source": "distilled",
                "doc": meta.get("name", ""),
                "description": meta.get("_distill_reasoning", meta.get("name", "")),
                "role": role,
                "archetype": archetype,
                "mood": mood,
                "density": density,
                "style_tags": tags.get("content_shape", []) or [],
                "slot_names": [s["name"] for s in meta.get("slots", [])],
                "required_slots": [s["name"] for s in meta.get("slots", []) if s.get("required")],
                "slots": meta.get("slots", []),
                "intent_tags": tags,
                "status": meta.get("status", "active"),
                "ambient_capable": ambient_capable,
            })
    return out


# Alias map: distilled-shell role tags -> unified role vocabulary used by
# seed shells and LLM prompts.
_ROLE_ALIAS = {
    "closing": "closing_cta",
    "quote": "hero_quote",
    "editorial_quote": "hero_quote",
    "hero_statement": "hero_giant_metric",
    "bullet_list": "bullet_card_list",
    "card_list": "bullet_card_list",
    "divider": "section_divider",
    "data_dashboard": "metric_dashboard",
    "kpi_dashboard": "metric_dashboard",
    "timeline": "timeline_horizontal",
    "feature": "feature_grid",
    "bento": "feature_grid",
    "comparison": "comparison_split",
}


_MOOD_TRANSLATION = {
    # distilled vocab -> unified vocab
    "corporate": "boardroom",
    "formal": "boardroom",
    "professional": "boardroom",
    "minimal": "restrained",
    "sparse": "restrained",
    "academic": "research",
    "scientific": "research",
    "playful": "playful",
    "friendly": "warm",
    "warm": "warm",
    "bold": "bold",
    "dramatic": "bold",
    "cinematic": "cinematic",
    "elegant": "editorial",
    "editorial": "editorial",
    "sophisticated": "editorial",
    "refined": "editorial",
    "calm": "calm",
    "quiet": "calm",
    "tech": "technical",
    "technical": "technical",
    "digital": "technical",
    "modern": "technical",
    "vibrant": "punchy",
    "punchy": "punchy",
    "energetic": "punchy",
    "restrained": "restrained",
    "boardroom": "boardroom",
    "research": "research",
    "narrative": "narrative",
    "product": "product",
    "brand": "brand",
}


def _translate_mood(raw_mood: list[str]) -> list[str]:
    """Translate distilled-shell mood vocab to unified vocab. Unknown moods
    are dropped (they confuse LLM filtering). Dedup + preserve order."""
    out: list[str] = []
    seen: set[str] = set()
    for m in raw_mood:
        key = m.lower().strip()
        mapped = _MOOD_TRANSLATION.get(key)
        if mapped and mapped not in seen:
            out.append(mapped)
            seen.add(mapped)
    return out


def _infer_archetype_from_tags(mood: list[str], role_tags: list[str]) -> str:
    """Single archetype for a distilled shell. Rough heuristic from mood+role."""
    role_set = {r.lower() for r in role_tags}
    if {"metric_dashboard", "hero_giant_metric", "kpi_card",
        "feature_stat"} & role_set:
        return "data"
    if "closing_cta" in role_set or "product" in mood:
        return "product"
    if "hero_quote" in role_set or "research" in mood:
        return "research"
    if "boardroom" in mood or "restrained" in mood:
        return "boardroom"
    if "brand" in mood:
        return "brand"
    return "narrative"


_AMBIENT_PRIMITIVE_TOKENS = (
    "add_infinite_rotation",
    "add_orbital_motion",
    "add_pulse_loop",
    "add_drift_motion",
)


def _seed_shell_ambient_capable(py_path: Path) -> bool:
    try:
        src = py_path.read_text()
    except Exception:
        return False
    if "AMBIENT_CAPABLE = True" in src:
        return True
    return any(tok in src for tok in _AMBIENT_PRIMITIVE_TOKENS)


def _distilled_shell_ambient_capable(shell_dir: Path) -> bool:
    render_py = shell_dir / "render.py"
    if not render_py.exists():
        return False
    try:
        src = render_py.read_text()
    except Exception:
        return False
    return any(tok in src for tok in _AMBIENT_PRIMITIVE_TOKENS)


def _derive_role_tags(shell_id: str) -> list[str]:
    """Map shell filename stem to slide_role tags. Seed shells follow naming convention."""
    sid = shell_id.lower()
    tags = []
    if "cover" in sid:
        tags.append("cover")
    if "agenda" in sid:
        tags.append("agenda")
    if "section_divider" in sid or "divider" in sid:
        tags.append("section_divider")
    if "bullet" in sid or "card_list" in sid:
        tags.append("bullet_card_list")
    if "metric" in sid or "dashboard" in sid:
        tags.append("metric_dashboard")
    if "timeline" in sid:
        tags.append("timeline_horizontal")
    if "closing" in sid or "cta" in sid:
        tags.append("closing")
    if "comparison" in sid or "split" in sid:
        tags.append("comparison_split")
    if "quote" in sid:
        tags.append("quote")
    if "feature_grid" in sid or "bento" in sid:
        tags.append("feature_grid")
    return tags


def render_shell(slide, shell_id: str, slots: dict, theme_id: str) -> dict:
    """Convenience: load theme + shell and render."""
    theme = load_theme(theme_id)
    mod = load_shell(shell_id)
    mod.render(slide, slots, theme)
    return {"shell_id": shell_id, "theme_id": theme_id, "slots_provided": list(slots.keys())}


__all__ = ["load_theme", "load_shell", "list_themes", "list_shells", "render_shell"]
