"""Material Choreographed Card Cascade — Title, supporting text, and cards animate as a coordinated upward cascade with clear spatial rhythm.

Distilled from Material 3 — Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material 3 — Motion Overview'

NAME = 'material_choreo_card_cascade'
CATEGORY = 'composite'
DESCRIPTION = 'Title, supporting text, and cards animate as a coordinated upward cascade with clear spatial rhythm.'
APPLICABILITY = {'roles': ['feature grid', 'benefits', 'dashboard intro'], 'anchor_names': ['title', 'subtitle', 'cards', 'button', 'icon'], 'max_per_slide': 1}
PARAMETERS = {'delay': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'step': {'type': 'int', 'default': 90, 'min': 30, 'max': 300}, 'duration': {'type': 'int', 'default': 360, 'min': 160, 'max': 1000}}

TAGS = ['material', 'cascade', 'cards', 'stagger', 'ui']
INTENSITY = 5
MOOD = ['technical', 'bold', 'restrained']
ARCHETYPE_FIT = ['product', 'data', 'boardroom']
EMBEDDING_TEXT = 'Inspired by Material choreography, this pattern sequences information by importance while preserving momentum across a card group. It works well for modular UI and feature storytelling.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['chart_bar_grow', 'kpi_status_ping', 'axis_line_draw']
CONFLICTS_WITH = ['hero_spotlight_pull', 'cinematic_letterbox_iris', 'jelly_title_bounce']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_grow_from_small, emit_text_stagger
    p = dict(params or {})
    d=p.get('delay',0); s=p.get('step',90); t=p.get('duration',360); x=target_shape
    emit_fade_in(slide, x.get('title', x), d, 160)
    emit_fly_in(slide, x.get('subtitle', x), direction='bottom', delay_ms=d+s, duration_ms=t)
    emit_text_stagger(slide, x.get('cards', x), d+s*2, s, t)
    emit_grow_from_small(slide, x.get('button', x), d+s*3, 220, scale_from=0.85)
    emit_fade_in(slide, x.get('icon', x), d+s*2, 160)
