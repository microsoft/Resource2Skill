"""Thesis Mark Resolve — A compact marker enters with slight rotation and scale, landing like a confident annotation.

Distilled from Material Design Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material Design Motion Overview'

NAME = 'thesis_mark_resolve'
CATEGORY = 'composite'
DESCRIPTION = 'A compact marker enters with slight rotation and scale, landing like a confident annotation.'
APPLICABILITY = {'roles': ['research', 'narrative', 'boardroom'], 'anchor_names': ['badge', 'chip', 'icon', 'section_number', 'kicker'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 60, 'min': 0, 'max': 1200}, 'duration_ms': {'type': 'int', 'default': 360, 'min': 180, 'max': 900}}

TAGS = ['marker', 'annotation', 'thesis', 'settle', 'precise']
INTENSITY = 3
MOOD = ['restrained', 'technical', 'boardroom']
ARCHETYPE_FIT = ['research', 'boardroom', 'narrative']
EMBEDDING_TEXT = 'Best for small thesis markers, numbered dots, or evidence badges. The motion suggests an argument being placed carefully into the document.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['agenda_marker_sweep', 'bullet_stagger_reveal', 'headline_restrike_focus']
CONFLICTS_WITH = ['badge_pinwheel_pop', 'badge_swing_in', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_grow_from_small, emit_rotate_in
    p = dict(params or {})
    d = p.get('delay_ms', 60)
    t = p.get('duration_ms', 360)
    emit_rotate_in(slide, target_shape, delay_ms=d, duration_ms=t, from_deg=-8)
    emit_grow_from_small(slide, target_shape, delay_ms=d, duration_ms=t, scale_from=0.82)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=max(180, int(t * 0.8)))
