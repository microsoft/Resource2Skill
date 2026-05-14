"""Playful Drop Bounce — A cheerful top-down arrival that lands with a soft bounce for kid-friendly callouts and badges.

Distilled from Animate.css
Source: https://animate.style/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://animate.style/'
SOURCE_TITLE = 'Animate.css'

NAME = 'playful_drop_bounce'
CATEGORY = 'entrance'
DESCRIPTION = 'A cheerful top-down arrival that lands with a soft bounce for kid-friendly callouts and badges.'
APPLICABILITY = {'roles': ['intro', 'callout', 'feature', 'celebration'], 'anchor_names': ['badge', 'chip', 'icon', 'cta', 'button', 'section_label'], 'max_per_slide': 3}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 700, 'min': 200, 'max': 2000}, 'pulse_pct': {'type': 'int', 'default': 108, 'min': 102, 'max': 125}}

TAGS = ['bounce', 'drop', 'playful', 'kid-friendly', 'arrival']
INTENSITY = 6
MOOD = ['playful', 'warm', 'punchy']
ARCHETYPE_FIT = ['brand', 'product', 'narrative']
EMBEDDING_TEXT = 'Use for badges, icons, and buttons that should feel friendly and energetic. It drops in from above, rebounds once, then gives a tiny settling pop.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['bullet_stagger_reveal', 'cta_attention_pulse', 'badge_pinwheel_pop']
CONFLICTS_WITH = ['dramatic_zoom', 'glitch_shear_snap', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_bounce_in, emit_fly_in, emit_grow_emphasis
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    dur = p.get('duration_ms', 700)
    pulse = p.get('pulse_pct', 108)
    emit_fly_in(slide, target_shape, direction='top', delay_ms=d, duration_ms=int(dur * 0.78))
    emit_bounce_in(slide, target_shape, delay_ms=d, duration_ms=dur)
    emit_grow_emphasis(slide, target_shape, delay_ms=d + dur, duration_ms=180, scale_pct=pulse)
