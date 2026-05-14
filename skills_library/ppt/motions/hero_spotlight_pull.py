"""hero_spotlight_pull — Rotate-in subtle + pulse once — reads as a spotlight settling on the subject..

Rotate-in subtle + pulse once — reads as a spotlight settling on the subject. Fade-in settled by a single emphasis pulse — like a spotligh

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'hero_spotlight_pull'
CATEGORY = 'entrance'
DESCRIPTION = 'Rotate-in subtle + pulse once — reads as a spotlight settling on the subject. Fade-in settled by a single emphasis pulse — like a spotligh'

APPLICABILITY = {'roles': ['cover', 'hero_giant_metric', 'closing_cta'], 'anchor_names': ['headline', 'hero_headline', 'value', 'metric_xl', 'hero_image', 'badge'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['spotlight', 'cinematic', 'brand', 'premium']
INTENSITY = 5
MOOD = ['cinematic', 'bold', 'warm']
ARCHETYPE_FIT = ['brand', 'product']

EMBEDDING_TEXT = (
    'Fade-in settled by a single emphasis pulse — like a spotlight landing and catching its target. Cinematic without being loud.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['cinematic_letterbox_iris', 'breathing_halo']
CONFLICTS_WITH = ['typewriter_clack_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fade_in, emit_pulse
    d = int(p.get('delay_ms',120))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=700)
    emit_pulse(slide, target_shape, delay_ms=d+700, duration_ms=300, scale_pct=106, repeats=1)
