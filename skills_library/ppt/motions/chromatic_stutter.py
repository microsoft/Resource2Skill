"""chromatic_stutter — Three micro pulses in quick succession — reads as RGB channel jitter..

Three micro pulses in quick succession — reads as RGB channel jitter. Three staccato pulses spaced 90ms apart, reading as RGB-chan

Category: emphasis. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'chromatic_stutter'
CATEGORY = 'emphasis'
DESCRIPTION = 'Three micro pulses in quick succession — reads as RGB channel jitter. Three staccato pulses spaced 90ms apart, reading as RGB-chan'

APPLICABILITY = {'roles': ['hero_giant_metric', 'cover', 'closing_cta'], 'anchor_names': ['hero_number', 'value', 'metric_xl', 'badge', 'cta'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['chromatic', 'glitch', 'tech', 'rgb']
INTENSITY = 6
MOOD = ['technical', 'punchy']
ARCHETYPE_FIT = ['product']

EMBEDDING_TEXT = (
    'Three staccato pulses spaced 90ms apart, reading as RGB-channel stutter. Ideal for product-tech decks and gaming/audio launch decks.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['glitch_shear_snap']
CONFLICTS_WITH = ['cinematic_veil_reveal', 'editorial_ink_bleed']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    d = int(p.get('delay_ms',180))
    emit_pulse(slide, target_shape, delay_ms=d, duration_ms=80, scale_pct=104, repeats=1)
    emit_pulse(slide, target_shape, delay_ms=d+90, duration_ms=80, scale_pct=104, repeats=1)
    emit_pulse(slide, target_shape, delay_ms=d+180, duration_ms=100, scale_pct=106, repeats=1)
