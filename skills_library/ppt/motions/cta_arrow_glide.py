"""cta_arrow_glide — Short fly-in-from-left with a late pulse — a CTA button sliding in and tapping once..

Short fly-in-from-left with a late pulse — a CTA button sliding in and tapping once. A CTA button sliding in from the left and tapping once at re

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'cta_arrow_glide'
CATEGORY = 'entrance'
DESCRIPTION = 'Short fly-in-from-left with a late pulse — a CTA button sliding in and tapping once. A CTA button sliding in from the left and tapping once at re'

APPLICABILITY = {'roles': ['closing_cta', 'hero_giant_metric'], 'anchor_names': ['cta', 'button', 'chip', 'badge', 'action'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['cta', 'arrow', 'glide', 'product', 'brand', 'call-to-action']
INTENSITY = 6
MOOD = ['bold', 'punchy', 'cinematic']
ARCHETYPE_FIT = ['product', 'brand']

EMBEDDING_TEXT = (
    'A CTA button sliding in from the left and tapping once at rest. Replaces bland fade-in CTAs with a clear invitation-to-click moment.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['neon_outline_trace', 'hero_spotlight_pull']
CONFLICTS_WITH = ['hairline_snap_in']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fly_in, emit_fade_in, emit_pulse
    d = int(p.get('delay_ms',300))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=450)
    emit_fly_in(slide, target_shape, direction='left', delay_ms=d, duration_ms=550)
    emit_pulse(slide, target_shape, delay_ms=d+700, duration_ms=320, scale_pct=108, repeats=1)
