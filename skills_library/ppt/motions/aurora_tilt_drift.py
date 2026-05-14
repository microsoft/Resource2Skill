"""Aurora Tilt Drift — An ultra-slow rotational drift for abstract color fields or photo backplates, creating soft atmospheric motion behind content.

Distilled from Material Design Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material Design Motion Overview'

NAME = 'aurora_tilt_drift'
CATEGORY = 'ambient'
DESCRIPTION = 'An ultra-slow rotational drift for abstract color fields or photo backplates, creating soft atmospheric motion behind content.'
APPLICABILITY = {'roles': ['background texture', 'hero backdrop', 'section divider'], 'anchor_names': ['photo', 'hero_image', 'section_label', 'title_xl'], 'max_per_slide': 1}
PARAMETERS = {'duration_ms': {'type': 'int', 'default': 18000, 'min': 8000, 'max': 30000}, 'fade_ms': {'type': 'int', 'default': 600, 'min': 0, 'max': 2000}}

TAGS = ['ambient', 'drift', 'background', 'atmospheric', 'slow']
INTENSITY = 2
MOOD = ['calm', 'cinematic', 'warm']
ARCHETYPE_FIT = ['brand', 'narrative', 'product']
EMBEDDING_TEXT = 'Best for blurred gradients, oversized color blobs, and image backplates where you want motion without distracting from text. The effect suggests atmosphere, not spin.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['headline_mist_rise', 'focus_pull_dissolve', 'glass_crossfade_settle']
CONFLICTS_WITH = ['background_parallax_glide', 'image_ken_burns', 'dramatic_zoom']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_ambient_rotation, emit_fade_in
    p = dict(params or {})
    d = p.get('duration_ms', 18000)
    f = p.get('fade_ms', 600)
    emit_fade_in(slide, target_shape, delay_ms=0, duration_ms=f)
    emit_ambient_rotation(slide, target_shape, duration_ms=d)
