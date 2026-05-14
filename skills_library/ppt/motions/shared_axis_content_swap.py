"""Shared Axis Content Swap — A coordinated headline, visual, and CTA swap that implies continuity while shifting focus across a slide.

Distilled from Material Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material Motion Overview'

NAME = 'shared_axis_content_swap'
CATEGORY = 'composite'
DESCRIPTION = 'A coordinated headline, visual, and CTA swap that implies continuity while shifting focus across a slide.'
APPLICABILITY = {'roles': ['hero swap', 'section transition', 'feature reveal'], 'anchor_names': ['headline', 'subtitle', 'hero_image', 'cta'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'dur_ms': {'type': 'int', 'default': 520, 'min': 180, 'max': 1500}}

TAGS = ['shared-axis', 'transition', 'continuity', 'hero', 'cta']
INTENSITY = 6
MOOD = ['technical', 'boardroom', 'restrained']
ARCHETYPE_FIT = ['product', 'brand', 'boardroom']
EMBEDDING_TEXT = 'A Material-style shared-axis handoff: the headline enters laterally, the hero image resolves with depth, and supporting copy plus CTA follow in a linked sequence.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['hairline_snap_in', 'metric_snap_focus', 'cta_arrow_glide']
CONFLICTS_WITH = ['dramatic_zoom', 'glitch_shear_snap', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_wipe_in, emit_zoom_in
    p = dict(params or {})
    d = p.get('delay_ms', 0); dur = p.get('dur_ms', 520)
    emit_fly_in(slide, target_shape.get('headline'), direction='right', delay_ms=d, duration_ms=dur)
    emit_fade_in(slide, target_shape.get('subtitle'), delay_ms=d+90, duration_ms=dur-80)
    emit_zoom_in(slide, target_shape.get('hero_image'), delay_ms=d+40, duration_ms=dur+80)
    emit_wipe_in(slide, target_shape.get('cta'), direction='left', delay_ms=d+180, duration_ms=dur-120)
