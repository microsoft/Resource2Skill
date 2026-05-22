"""Fade-Through Zoom Cut — A fast crossfade-style entrance with slight zoom that feels like a modern slide-to-slide cut.

Distilled from Material Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material Motion Overview'

NAME = 'fade_through_zoom_cut'
CATEGORY = 'transition'
DESCRIPTION = 'A fast crossfade-style entrance with slight zoom that feels like a modern slide-to-slide cut.'
APPLICABILITY = {'roles': ['section change', 'hero swap', 'chapter reset'], 'anchor_names': ['hero_image', 'photo', 'headline', 'title', 'hero_headline'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 420, 'min': 120, 'max': 1500}}

TAGS = ['fade-through', 'zoom', 'crossfade', 'cut', 'slide-transition']
INTENSITY = 5
MOOD = ['restrained', 'cinematic', 'boardroom']
ARCHETYPE_FIT = ['narrative', 'product', 'boardroom', 'brand']
EMBEDDING_TEXT = 'Use this when one slide replaces another with minimal spatial travel. It reads like a polished editorial or product crossfade rather than a theatrical entrance.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['focus_pull_dissolve', 'hero_lens_focus', 'gentle_rise_fade']
CONFLICTS_WITH = ['dramatic_zoom', 'glitch_shear_snap', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_dramatic_zoom, emit_fade_in
    p = dict(params or {})
    d = int(p.get('duration_ms', 420))
    delay = int(p.get('delay_ms', 0))
    emit_dramatic_zoom(slide, target_shape, delay_ms=delay, duration_ms=d)
    emit_fade_in(slide, target_shape, delay_ms=delay, duration_ms=max(180, d - 80))
