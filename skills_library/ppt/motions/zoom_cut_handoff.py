"""Zoom-Cut Handoff — A brisk zoom-in cut that makes incoming content feel snapped into focus between slides.

Distilled from Material Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material Motion Overview'

NAME = 'zoom_cut_handoff'
CATEGORY = 'transition'
DESCRIPTION = 'A brisk zoom-in cut that makes incoming content feel snapped into focus between slides.'
APPLICABILITY = {'roles': ['transition', 'product reveal', 'section jump', 'hero swap'], 'anchor_names': ['hero_image', 'photo', 'title_xl', 'hero_headline', 'cards', 'cta'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 1200}, 'duration_ms': {'type': 'int', 'default': 520, 'min': 180, 'max': 1600}}

TAGS = ['zoom', 'cut', 'focus', 'snap', 'transition']
INTENSITY = 6
MOOD = ['bold', 'technical', 'punchy']
ARCHETYPE_FIT = ['product', 'brand', 'data']
EMBEDDING_TEXT = 'Distilled from Material motion’s focus on spatial continuity, this behaves like a clean zoom-cut between states. Use it when a new slide should feel connected, not merely replaced.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['metric_snap_focus', 'cta_arrow_glide', 'headline_restrike_focus']
CONFLICTS_WITH = ['mist_drift_behind', 'breathing_halo', 'floating_card_drift']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_grow_emphasis, emit_zoom_in
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    dur = p.get('duration_ms', 520)
    emit_zoom_in(slide, target_shape, delay_ms=d, duration_ms=dur)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=max(160, int(dur * 0.6)))
    emit_grow_emphasis(slide, target_shape, delay_ms=d + int(dur * 0.72), duration_ms=max(120, int(dur * 0.28)), scale_pct=104)
