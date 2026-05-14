"""lab_blink_flash — Double rapid pulse — reads as a lab indicator LED flashing..

Double rapid pulse — reads as a lab indicator LED flashing. Two rapid 115% pulses — the motion of a lab or dashboard LED

Category: emphasis. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'lab_blink_flash'
CATEGORY = 'emphasis'
DESCRIPTION = 'Double rapid pulse — reads as a lab indicator LED flashing. Two rapid 115% pulses — the motion of a lab or dashboard LED'

APPLICABILITY = {'roles': ['feature_grid', 'hero_giant_metric', 'closing_cta', 'kpi_card'], 'anchor_names': ['indicator', 'badge', 'chip', 'icon', 'accent', 'accent_orb'], 'max_per_slide': 2}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['lab', 'blink', 'led', 'kids', 'science', 'playful']
INTENSITY = 6
MOOD = ['playful', 'technical', 'warm']
ARCHETYPE_FIT = ['narrative', 'data', 'product']

EMBEDDING_TEXT = (
    'Two rapid 115% pulses — the motion of a lab or dashboard LED. Appropriate for science-education decks and simple product indicator graphics.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['bubble_pop_reveal', 'audit_tick_mark']
CONFLICTS_WITH = ['cinematic_letterbox_iris']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    d = int(p.get('delay_ms',400))
    emit_pulse(slide, target_shape, delay_ms=d, duration_ms=220, scale_pct=115, repeats=2)
