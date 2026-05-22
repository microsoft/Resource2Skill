"""bounce_in — overshoot-and-settle 'pop' entrance.

Scale from 20% up to 120% (overshoot past 100%) then settle back to
100%. Gives a playful 'pop!' arrival feel. Good for badges, CTAs,
callouts that should feel alive.
"""
from __future__ import annotations

NAME = "bounce_in"
CATEGORY = "entrance"
DESCRIPTION = (
    "Shape bounces in: 20% -> 120% -> 100% over 700ms. Playful pop "
    "arrival — pair with CTAs, badges, logos, hero numbers."
)
APPLICABILITY = {
    "roles": ["closing_cta", "kpi_card", "hero_giant_metric",
              "feature_stat", "cover"],
    "anchor_names": ["cta", "badge", "button", "chip", "logo", "seal",
                     "hero_number", "big_number"],
    "max_per_slide": 2,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 400, "min": 0, "max": 4000},
    "duration_ms": {"type": "int", "default": 700, "min": 400, "max": 1500},
}


MOOD = ['punchy', 'bold', 'playful', 'cinematic']
ARCHETYPE_FIT = ['brand', 'product', 'data', 'boardroom']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_bounce_in
    p = dict(params or {})
    emit_bounce_in(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 400)),
        duration_ms=int(p.get("duration_ms", 700)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['dramatic', 'playful', 'overshoot-settle', 'pop-arrival', 'elastic']
INTENSITY = 8
EMBEDDING_TEXT = (
    'Elastic arrival: scale 20 to 120 then settle to 100% over 700ms. Playful pop feel. Use on CTAs, badges, logos, hero numbers, or anywhere you want an audience smile. Avoid on long headlines (text distorts during overshoot).'
)
CONTENT_MATCHERS = {'is_headline': False, 'max_chars': 40}
COMPLEMENTARY_WITH = ['pulse_emphasis', 'breathing_halo']
CONFLICTS_WITH = ['dramatic_zoom', 'grow_reveal', 'zoom_from_center']
