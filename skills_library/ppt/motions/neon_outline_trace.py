"""neon_outline_trace — Wipe right-to-left quickly followed by a pulse — reads as a neon sign tracing its outline..

Wipe right-to-left quickly followed by a pulse — reads as a neon sign tracing its outline. Right-to-left wipe in 600ms + a 280ms emphasis bump. Reads l

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'neon_outline_trace'
CATEGORY = 'entrance'
DESCRIPTION = 'Wipe right-to-left quickly followed by a pulse — reads as a neon sign tracing its outline. Right-to-left wipe in 600ms + a 280ms emphasis bump. Reads l'

APPLICABILITY = {'roles': ['cover', 'closing_cta', 'hero_giant_metric'], 'anchor_names': ['headline', 'hero_headline', 'cta', 'badge', 'value'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['neon', 'outline-trace', 'brand', 'retro', '80s']
INTENSITY = 6
MOOD = ['cinematic', 'bold', 'punchy', 'playful']
ARCHETYPE_FIT = ['brand', 'product']

EMBEDDING_TEXT = (
    'Right-to-left wipe in 600ms + a 280ms emphasis bump. Reads like a neon tube tracing its outline and then settling. Perfect for retro-neon and synthwave brand moments.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['cinematic_letterbox_iris', 'chromatic_stutter']
CONFLICTS_WITH = ['editorial_ink_bleed']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_wipe_in, emit_pulse
    d = int(p.get('delay_ms',80))
    emit_wipe_in(slide, target_shape, direction='right', delay_ms=d, duration_ms=600)
    emit_pulse(slide, target_shape, delay_ms=d+700, duration_ms=280, scale_pct=104, repeats=1)
