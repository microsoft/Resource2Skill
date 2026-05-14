"""grow_reveal — cover headline arrives with cinematic weight.

The headline grows from 70% to 100% while fading in. Good for
cover slides and section dividers where the first big text needs
to "land" rather than just appear.
"""
from __future__ import annotations

NAME = "grow_reveal"
CATEGORY = "entrance"
DESCRIPTION = (
    "Shape scales from 70% to 100% while fading in over 700ms. "
    "Cinematic 'arrival' effect for cover headlines."
)
APPLICABILITY = {
    "roles": ["cover", "section_divider", "closing_cta"],
    "anchor_names": ["headline", "hero_headline", "title", "section_label"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 100, "min": 0, "max": 4000},
    "duration_ms": {"type": "int", "default": 700, "min": 300, "max": 2000},
    "from_pct":    {"type": "int", "default": 70,  "min": 30,  "max": 95},
}


MOOD = ['editorial']
ARCHETYPE_FIT = ['brand', 'narrative', 'product']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_grow_from_small
    p = dict(params or {})
    emit_grow_from_small(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 100)),
        duration_ms=int(p.get("duration_ms", 700)),
        from_pct=int(p.get("from_pct", 70)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['subtle', 'cinematic-soft', 'headline-reveal']
INTENSITY = 5
EMBEDDING_TEXT = (
    "Gentle 70% to 100% scale-in with fade over 700ms. Soft cinematic 'settle' for cover headlines, section labels, titles. Less dramatic than dramatic_zoom; use when the moment calls for restraint rather than theatrics."
)
CONTENT_MATCHERS = {'is_headline': True}
COMPLEMENTARY_WITH = ['slide_in_left', 'orbital_accent']
CONFLICTS_WITH = ['dramatic_zoom', 'bounce_in']
