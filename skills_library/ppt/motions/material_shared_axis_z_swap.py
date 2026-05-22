"""Material Shared Axis Z Swap — An incoming zoom-based transition that suggests moving forward to a new surface without a hard cut.

Distilled from Material 3 — Applying transitions
Source: https://m3.material.io/styles/motion/transitions/applying-transitions
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/transitions/applying-transitions'
SOURCE_TITLE = 'Material 3 — Applying transitions'

NAME = 'material_shared_axis_z_swap'
CATEGORY = 'transition'
DESCRIPTION = 'An incoming zoom-based transition that suggests moving forward to a new surface without a hard cut.'
APPLICABILITY = {'roles': ['scene change', 'feature swap', 'hero transition', 'chapter break'], 'anchor_names': ['hero_image', 'photo', 'title_xl', 'cards', 'cta'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 500, 'min': 180, 'max': 1400}}

TAGS = ['shared-axis', 'z-depth', 'zoom', 'swap', 'material']
INTENSITY = 5
MOOD = ['technical', 'bold', 'cinematic']
ARCHETYPE_FIT = ['product', 'brand', 'narrative']
EMBEDDING_TEXT = 'Drawn from Material transition patterns where depth communicates a change of state. It works well as a zoom-cut substitute when you want continuity instead of spectacle.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['headline_arc_settle', 'glass_crossfade_settle', 'cta_arrow_glide']
CONFLICTS_WITH = ['fade_through_zoom_cut', 'dramatic_zoom', 'hero_spotlight_pull']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_zoom_in
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    dur = p.get('duration_ms', 500)
    emit_zoom_in(slide, target_shape, delay_ms=d, duration_ms=dur)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=max(180, int(dur * 0.8)))
