"""explorer_map_pin_drop — Grow-from-small with a dramatic bounce — a map pin dropping onto a location..

Grow-from-small with a dramatic bounce — a map pin dropping onto a location. Classic map-pin drop: a small element grows with overshoot i

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'explorer_map_pin_drop'
CATEGORY = 'entrance'
DESCRIPTION = 'Grow-from-small with a dramatic bounce — a map pin dropping onto a location. Classic map-pin drop: a small element grows with overshoot i'

APPLICABILITY = {'roles': ['feature_grid', 'timeline_horizontal', 'cover', 'closing_cta'], 'anchor_names': ['pin', 'map_pin', 'marker', 'icon', 'badge', 'seal'], 'max_per_slide': 3}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['map-pin', 'drop', 'explorer', 'kids', 'narrative']
INTENSITY = 6
MOOD = ['playful', 'warm', 'punchy']
ARCHETYPE_FIT = ['narrative', 'brand']

EMBEDDING_TEXT = (
    'Classic map-pin drop: a small element grows with overshoot in ~650ms. Signature for exploration/educational narratives.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['lab_blink_flash', 'confetti_burst']
CONFLICTS_WITH = ['hairline_snap_in', 'editorial_ink_bleed']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_bounce_in, emit_fade_in
    d = int(p.get('delay_ms',200))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=400)
    emit_bounce_in(slide, target_shape, delay_ms=d, duration_ms=650)
