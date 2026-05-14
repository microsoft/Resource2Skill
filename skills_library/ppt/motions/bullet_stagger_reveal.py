"""bullet_stagger_reveal — reveal bullets one at a time.

For multi-paragraph text bodies (bullet lists, cards, feature
grids). Each paragraph fades in with an increasing delay so the
audience reads them in order rather than seeing a wall of text.

Applies to:
  - slide_role ∈ {bullet_card_list, feature_grid, agenda, comparison_split}
  - anchor_name matching /bullets?|list|items?/i
"""
from __future__ import annotations

NAME = "bullet_stagger_reveal"
CATEGORY = "entrance"
DESCRIPTION = (
    "Each paragraph fades in sequentially with a 180ms stagger. "
    "Audience reads along top-to-bottom instead of receiving a wall "
    "of text all at once."
)
APPLICABILITY = {
    "roles": ["bullet_card_list", "feature_grid", "agenda",
              "comparison_split", "timeline_horizontal"],
    "anchor_name_regex": r"(bullets?|list|items?|cards?)",
    "max_per_slide": 2,
}
PARAMETERS = {
    "delay_ms":        {"type": "int", "default": 300, "min": 0, "max": 4000},
    "stagger_ms":      {"type": "int", "default": 180, "min": 80, "max": 500},
    "per_duration_ms": {"type": "int", "default": 450, "min": 200, "max": 1200},
}


MOOD = ['editorial']
ARCHETYPE_FIT = ['narrative', 'brand']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_text_stagger
    p = dict(params or {})
    emit_text_stagger(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 300)),
        stagger_ms=int(p.get("stagger_ms", 180)),
        per_duration_ms=int(p.get("per_duration_ms", 450)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['sequential', 'bullets', 'agenda', 'list-reveal', 'staggered']
INTENSITY = 6
EMBEDDING_TEXT = (
    'Each paragraph in a text frame fades in sequentially with 180ms stagger. Audience reads top-to-bottom in the intended order instead of seeing a wall of text. Apply to bullet lists, agendas, timeline step lists, feature grids, metric dashboards.'
)
CONTENT_MATCHERS = {'multi_paragraph': True, 'min_chars': 20}
COMPLEMENTARY_WITH = ['grow_reveal', 'dramatic_zoom']
CONFLICTS_WITH = []
