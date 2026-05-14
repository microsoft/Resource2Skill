"""dramatic_zoom — cinematic 10%→100% zoom-in.

For hero shots: product reveals, big numbers, section dividers,
opening headlines. Much more dramatic than grow_reveal (which only
scales 70→100%). 900ms duration lets the audience SEE the arrival.
"""
from __future__ import annotations

NAME = "dramatic_zoom"
CATEGORY = "entrance"
DESCRIPTION = (
    "Shape arrives from 10% to 100% scale over 900ms. "
    "Apple-keynote-reveal feel for headlines, hero metrics, and "
    "section dividers."
)
APPLICABILITY = {
    "roles": ["cover", "section_divider", "hero_giant_metric",
              "closing_cta", "kpi_card"],
    "anchor_names": ["headline", "hero_headline", "section_label",
                     "hero_number", "title", "big_number"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 200, "min": 0, "max": 4000},
    "duration_ms": {"type": "int", "default": 900, "min": 500, "max": 2000},
    "from_pct":    {"type": "int", "default": 10,  "min": 5,   "max": 40},
}


MOOD = ['bold', 'cinematic', 'editorial', 'punchy']
ARCHETYPE_FIT = ['brand', 'product', 'narrative', 'data']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_dramatic_zoom
    p = dict(params or {})
    emit_dramatic_zoom(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 200)),
        duration_ms=int(p.get("duration_ms", 900)),
        from_pct=int(p.get("from_pct", 10)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['dramatic', 'cinematic', 'hero-reveal', 'apple-keynote', 'scale-up', 'headline-arrival']
INTENSITY = 9
EMBEDDING_TEXT = (
    'Cinematic 10% to 100% scale-in over 900ms. Best for hero numbers, section dividers, and cover headlines that need to feel like they arrive with authority. Produces an Apple-keynote product-reveal sensation. Stronger than grow_reveal which only scales 70 to 100%.'
)
CONTENT_MATCHERS = {'is_headline': True, 'min_chars': 1, 'max_chars': 120}
COMPLEMENTARY_WITH = ['breathing_halo', 'orbital_accent', 'slide_in_left']
CONFLICTS_WITH = ['grow_reveal', 'zoom_from_center', 'bounce_in']
