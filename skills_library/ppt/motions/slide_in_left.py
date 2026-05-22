"""slide_in_left — content body slides in from the left.

Generic entrance for large content blocks that need directional
emphasis. Good for subheads, sub-section content, feature cards
that land after the headline.
"""
from __future__ import annotations

NAME = "slide_in_left"
CATEGORY = "entrance"
DESCRIPTION = (
    "Shape slides in from the left edge over 700ms. Pair with "
    "grow_reveal on the headline for a natural visual hierarchy."
)
APPLICABILITY = {
    "roles": ["cover", "section_divider", "bullet_card_list",
              "comparison_split"],
    "anchor_names": ["subhead", "tagline", "body", "content_card",
                     "left_column"],
    "max_per_slide": 2,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 400, "min": 0, "max": 4000},
    "duration_ms": {"type": "int", "default": 700, "min": 300, "max": 1500},
}


MOOD = ['editorial']
ARCHETYPE_FIT = ['narrative', 'brand']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fly_in
    p = dict(params or {})
    emit_fly_in(
        slide, target_shape,
        direction="left",
        delay_ms=int(p.get("delay_ms", 400)),
        duration_ms=int(p.get("duration_ms", 700)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['directional', 'subhead', 'body-entrance', 'fly-in']
INTENSITY = 5
EMBEDDING_TEXT = (
    'Shape flies in from off-stage left over 700ms. For subheads, taglines, body copy, left-column content. Pair with grow_reveal on the headline for a natural reading flow (headline lands, then subhead slides in beside it).'
)
CONTENT_MATCHERS = {'is_headline': False}
COMPLEMENTARY_WITH = ['grow_reveal', 'dramatic_zoom']
CONFLICTS_WITH = ['rotate_in']
