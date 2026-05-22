"""breathing_halo — continuous strong-amplitude pulse.

For decorative rings / halos / accents on hero slides. Oscillates
between 100% and 130% over 3s, much stronger than the default
pulse_loop (110-120%). Makes the slide feel alive.
"""
from __future__ import annotations

NAME = "breathing_halo"
CATEGORY = "ambient"
DESCRIPTION = (
    "Indefinite 100%<->130% breathing pulse on a decorative shape "
    "(halo, ring, orb). 3s cycle. Stronger amplitude than the "
    "default ambient pulse for hero visibility."
)
APPLICABILITY = {
    "roles": ["cover", "hero_giant_metric", "section_divider",
              "closing_cta"],
    "anchor_names": ["halo", "ring", "accent_orb", "glow",
                     "background_ring"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "duration_ms": {"type": "int", "default": 3000, "min": 1500, "max": 8000},
    "scale_pct":   {"type": "int", "default": 130,  "min": 115,  "max": 160},
}


MOOD = ['calm', 'editorial', 'bold', 'punchy']
ARCHETYPE_FIT = ['brand', 'data', 'boardroom', 'narrative']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_breathing_halo
    p = dict(params or {})
    emit_breathing_halo(
        slide, target_shape,
        duration_ms=int(p.get("duration_ms", 3000)),
        scale_pct=int(p.get("scale_pct", 130)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['ambient-loop', 'breathing', 'halo', 'high-amplitude']
INTENSITY = 7
EMBEDDING_TEXT = (
    'High-amplitude 100% to 130% indefinite breathing pulse on a decorative ring/halo/orb shape. 3-second cycle. Stronger than the default ambient pulse — meant to be visible at distance. Best on cover/hero accent shapes.'
)
CONTENT_MATCHERS = {'is_decorative': True}
COMPLEMENTARY_WITH = ['orbital_accent', 'counter_rotate_cog']
CONFLICTS_WITH = []
