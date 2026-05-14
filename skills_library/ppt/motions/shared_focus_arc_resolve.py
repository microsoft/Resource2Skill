"""Shared Focus Arc Resolve — A focal image surges forward on a soft arc while title and CTA resolve into the new visual state.

Distilled from Motion Layout Animations
Source: https://motion.dev/docs/react-layout-animations
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://motion.dev/docs/react-layout-animations'
SOURCE_TITLE = 'Motion Layout Animations'

NAME = 'shared_focus_arc_resolve'
CATEGORY = 'composite'
DESCRIPTION = 'A focal image surges forward on a soft arc while title and CTA resolve into the new visual state.'
APPLICABILITY = {'roles': ['hero', 'feature handoff', 'product reveal', 'case study opener'], 'anchor_names': ['photo', 'hero_image', 'headline', 'title', 'hero_headline', 'subtitle', 'cta', 'button', 'badge', 'chip'], 'max_per_slide': 1}
PARAMETERS = {'base_delay': {'type': 'int', 'default': 0, 'min': 0, 'max': 1200}}

TAGS = ['shared-element', 'focus', 'arc', 'handoff', 'resolve']
INTENSITY = 6
MOOD = ['cinematic', 'bold', 'product']
ARCHETYPE_FIT = ['product', 'narrative', 'brand']
EMBEDDING_TEXT = 'Best for a product or campaign slide where the image is the shared focal anchor, then the headline and CTA settle around it.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['focus_pull_dissolve', 'hero_spotlight_pull', 'metric_snap_focus']
CONFLICTS_WITH = ['page_turn_drop', 'panel_shutter_unfold', 'chromatic_stutter']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_arc_path, emit_dramatic_zoom, emit_fade_in, emit_grow_from_small, emit_pulse
    p = dict(params or {})
    n = getattr(target_shape, 'name', '').lower(); d = int(p.get('base_delay', 0))
    if any(k in n for k in ('photo', 'hero_image')): emit_dramatic_zoom(slide, target_shape, delay_ms=d, duration_ms=520); emit_arc_path(slide, target_shape, delay_ms=d, duration_ms=520)
    elif any(k in n for k in ('headline', 'title', 'hero_headline')): emit_fade_in(slide, target_shape, delay_ms=d+180, duration_ms=260); emit_grow_from_small(slide, target_shape, delay_ms=d+180, duration_ms=320, scale_from=0.92)
    elif any(k in n for k in ('cta', 'button', 'badge', 'chip')): emit_fade_in(slide, target_shape, delay_ms=d+340, duration_ms=220); emit_pulse(slide, target_shape, delay_ms=d+620, duration_ms=180, scale_pct=108, repeats=1)
    else: emit_fade_in(slide, target_shape, delay_ms=d+240, duration_ms=260)
