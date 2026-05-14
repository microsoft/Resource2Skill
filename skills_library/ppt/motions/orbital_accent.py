"""orbital_accent — ambient orbital motion on a decorative shape.

Binds the ambient-primitive orbital motion to an accent shape
(accent_orb, decorative dot, halo). Continuous motion — not
content-triggered — so best paired with cover/hero slides that
stay on screen for several seconds.
"""
from __future__ import annotations

NAME = "orbital_accent"
CATEGORY = "ambient"
DESCRIPTION = (
    "Accent shape travels a continuous elliptical orbit while the "
    "slide is visible. Plays in PowerPoint; Impress renders static."
)
APPLICABILITY = {
    "roles": ["cover", "hero_giant_metric", "section_divider"],
    "anchor_names": ["accent_orb", "accent_dot", "halo", "orb"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "orbit_radius_in": {"type": "float", "default": 0.8, "min": 0.2, "max": 2.5},
    "duration_ms":     {"type": "int",   "default": 8000, "min": 4000, "max": 20000},
    "direction":       {"type": "str",   "default": "cw", "enum": ["cw", "ccw"]},
}


MOOD = ['editorial', 'cinematic', 'bold', 'punchy']
ARCHETYPE_FIT = ['brand', 'narrative', 'data', 'boardroom']

def apply(slide, target_shape, params=None):
    # Reuse the ambient primitive from shells_seed.
    from _shell_helpers import add_orbital_motion
    p = dict(params or {})
    # Orbit center = shape's current position (so the shape orbits
    # around where it started).
    try:
        cx = (target_shape.left + target_shape.width / 2) / 914400.0
        cy = (target_shape.top + target_shape.height / 2) / 914400.0
    except Exception:
        cx, cy = 6.0, 3.5
    add_orbital_motion(
        slide, target_shape,
        center_xy=(cx, cy),
        radius_in=float(p.get("orbit_radius_in", 0.8)),
        duration_ms=int(p.get("duration_ms", 8000)),
        direction=p.get("direction", "cw"),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['ambient-loop', 'orbital', 'decorative', 'cover-polish']
INTENSITY = 7
EMBEDDING_TEXT = (
    'Continuous elliptical orbit motion on a decorative shape (accent orb, halo, dot). Indefinite loop — plays for the entire slide lifetime. Great for cover slides, hero slides, section dividers that sit on screen for several seconds. PowerPoint only (Impress renders static).'
)
CONTENT_MATCHERS = {'is_headline': False, 'is_decorative': True}
COMPLEMENTARY_WITH = ['breathing_halo', 'counter_rotate_cog', 'dramatic_zoom']
CONFLICTS_WITH = ['morph_anchor_arc']
