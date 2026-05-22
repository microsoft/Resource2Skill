"""morph_anchor_arc — decorative accent arcs between morph anchors.

For two-slide sequences with a set_morph_anchor-bound accent shape:
the accent arcs from slide-1 to slide-2 position with a visible
curve, reinforcing the morph transition. Intended to be applied
on slide-2 of the pair; slide-2's transition must be "morph".
"""
from __future__ import annotations

NAME = "morph_anchor_arc"
CATEGORY = "transition"
DESCRIPTION = (
    "Accent anchor arcs across the slide on entry, reinforcing "
    "a PowerPoint Morph between two slides that share the anchor "
    "name (!!sameName* convention)."
)
APPLICABILITY = {
    "roles": ["cover", "section_divider", "hero_giant_metric"],
    "anchor_names": ["accent_orb", "accent_dot", "halo"],
    "requires_morph_pair": True,
    "max_per_slide": 1,
}
PARAMETERS = {
    "delay_ms":    {"type": "int",   "default": 200,  "min": 0,   "max": 2000},
    "duration_ms": {"type": "int",   "default": 1200, "min": 600, "max": 3000},
    "dx_frac":     {"type": "float", "default": 0.35, "min": -1.0, "max": 1.0},
    "dy_frac":     {"type": "float", "default": 0.0,  "min": -0.5, "max": 0.5},
    "bow_frac":    {"type": "float", "default": 0.12, "min": 0.0, "max": 0.35},
}


MOOD = ['cinematic', 'editorial', 'bold', 'punchy']
ARCHETYPE_FIT = ['narrative', 'brand', 'data', 'boardroom']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_arc_path
    p = dict(params or {})
    emit_arc_path(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 200)),
        duration_ms=int(p.get("duration_ms", 1200)),
        dx_frac=float(p.get("dx_frac", 0.35)),
        dy_frac=float(p.get("dy_frac", 0.0)),
        bow_frac=float(p.get("bow_frac", 0.12)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['transition', 'morph-pair', 'anchor-arc', 'cinematic']
INTENSITY = 8
EMBEDDING_TEXT = (
    'Accent anchor shape arcs across the slide on entry of slide B of a morph pair, reinforcing the PowerPoint Morph transition between two slides that share !!sameName* anchors. Requires slide B transition=morph and a named accent anchor present on both slides.'
)
CONTENT_MATCHERS = {'is_decorative': True, 'requires_morph_pair': True}
COMPLEMENTARY_WITH = ['dramatic_zoom']
CONFLICTS_WITH = ['orbital_accent']
