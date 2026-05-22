"""digit_slot_machine — Rapid grow+fade combo — reads as a slot-machine digit rolling to its final value..

Rapid grow+fade combo — reads as a slot-machine digit rolling to its final value. Combination of a 300ms fade and a 62%->100% grow over 620ms 

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'digit_slot_machine'
CATEGORY = 'entrance'
DESCRIPTION = 'Rapid grow+fade combo — reads as a slot-machine digit rolling to its final value. Combination of a 300ms fade and a 62%->100% grow over 620ms '

APPLICABILITY = {'roles': ['hero_giant_metric', 'metric_dashboard', 'kpi_card', 'feature_stat'], 'anchor_names': ['hero_number', 'value', 'metric_xl', 'digit', 'big_number'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['slot-machine', 'digit', 'roll', 'data', 'hero-metric']
INTENSITY = 6
MOOD = ['technical', 'boardroom', 'punchy']
ARCHETYPE_FIT = ['data', 'boardroom', 'product']

EMBEDDING_TEXT = (
    'Combination of a 300ms fade and a 62%->100% grow over 620ms — reads as a single digit snapping to its final value. Perfect hero-metric motion for data-heavy product and boardroom decks.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['bar_grow_cohort', 'axis_line_draw']
CONFLICTS_WITH = ['typewriter_clack_reveal', 'editorial_ink_bleed']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fade_in, emit_grow_from_small
    d = int(p.get('delay_ms',80))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=300)
    emit_grow_from_small(slide, target_shape, delay_ms=d, duration_ms=620, from_pct=62)
