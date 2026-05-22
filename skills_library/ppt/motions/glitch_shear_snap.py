"""glitch_shear_snap — Two rapid pulses of grow-emphasis with slight overlap, reads as a glitch snap..

Two rapid pulses of grow-emphasis with slight overlap, reads as a glitch snap. Double-beat scale pulse with 60ms overlap — reads as a mild 

Category: emphasis. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'glitch_shear_snap'
CATEGORY = 'emphasis'
DESCRIPTION = 'Two rapid pulses of grow-emphasis with slight overlap, reads as a glitch snap. Double-beat scale pulse with 60ms overlap — reads as a mild '

APPLICABILITY = {'roles': ['hero_giant_metric', 'closing_cta', 'cover', 'feature_stat'], 'anchor_names': ['hero_number', 'value', 'metric_xl', 'cta', 'badge'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['glitch', 'tech', 'snap', 'cyber', 'punchy']
INTENSITY = 7
MOOD = ['technical', 'punchy', 'bold']
ARCHETYPE_FIT = ['product', 'data']

EMBEDDING_TEXT = (
    'Double-beat scale pulse with 60ms overlap — reads as a mild CRT glitch. Good for tech decks announcing a latency number or a product code.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['metric_snap_pop', 'metric_digit_spark']
CONFLICTS_WITH = ['breathing_halo', 'editorial_ink_bleed']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    d = int(p.get('delay_ms',200))
    emit_pulse(slide, target_shape, delay_ms=d, duration_ms=160, scale_pct=108, repeats=1)
    emit_pulse(slide, target_shape, delay_ms=d+220, duration_ms=120, scale_pct=112, repeats=1)
