"""Staggered Feature Storyboard — A choreographed feature block where title, copy, cards, and CTA arrive as a readable staged narrative.

Distilled from web.dev CSS Animations
Source: https://web.dev/learn/css/animations/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://web.dev/learn/css/animations/'
SOURCE_TITLE = 'web.dev CSS Animations'

NAME = 'staggered_feature_storyboard'
CATEGORY = 'composite'
DESCRIPTION = 'A choreographed feature block where title, copy, cards, and CTA arrive as a readable staged narrative.'
APPLICABILITY = {'roles': ['feature section', 'capability overview', 'roadmap panel'], 'anchor_names': ['section_label', 'headline', 'items', 'cards', 'cta'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'stagger_ms': {'type': 'int', 'default': 70, 'min': 20, 'max': 300}, 'dur_ms': {'type': 'int', 'default': 420, 'min': 180, 'max': 1200}}

TAGS = ['stagger', 'cascade', 'feature', 'cards', 'readability']
INTENSITY = 5
MOOD = ['technical', 'research', 'warm']
ARCHETYPE_FIT = ['product', 'research', 'data']
EMBEDDING_TEXT = 'Inspired by staggered web animation patterns, this builds a feature story in reading order: label, title, explanatory points, then supporting cards and action.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['axis_line_draw', 'bullet_stagger_reveal', 'metric_bloom_echo']
CONFLICTS_WITH = ['page_turn_drop', 'dramatic_zoom', 'logo_swoop_resolve']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_grow_from_small, emit_text_stagger, emit_wipe_in
    p = dict(params or {})
    d = p.get('delay_ms', 0); s = p.get('stagger_ms', 70); dur = p.get('dur_ms', 420)
    emit_fade_in(slide, target_shape.get('section_label'), delay_ms=d, duration_ms=dur-120)
    emit_fly_in(slide, target_shape.get('headline'), direction='bottom', delay_ms=d+s, duration_ms=dur)
    emit_text_stagger(slide, target_shape.get('items'), delay_ms=d+(2*s), stagger_ms=s, per_duration_ms=dur-80)
    emit_grow_from_small(slide, target_shape.get('cards'), delay_ms=d+(3*s), duration_ms=dur+40, scale_from=0.94)
    emit_wipe_in(slide, target_shape.get('cta'), direction='left', delay_ms=d+(5*s), duration_ms=dur-140)
