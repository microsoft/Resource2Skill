"""Plane Counterdrift Loop — A restrained opposing drift for divider ornaments or technical textures that suggests layered depth without obvious travel.

Distilled from Fluent 2 Motion
Source: https://fluent2.microsoft.design/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://fluent2.microsoft.design/motion'
SOURCE_TITLE = 'Fluent 2 Motion'

NAME = 'plane_counterdrift_loop'
CATEGORY = 'ambient'
DESCRIPTION = 'A restrained opposing drift for divider ornaments or technical textures that suggests layered depth without obvious travel.'
APPLICABILITY = {'roles': ['section divider', 'diagram backdrop', 'ornamental accent'], 'anchor_names': ['icon', 'timeline_node', 'badge', 'section_label', 'hero_image'], 'max_per_slide': 2}
PARAMETERS = {'duration_ms': {'type': 'int', 'default': 14000, 'min': 6000, 'max': 24000}, 'fade_ms': {'type': 'int', 'default': 450, 'min': 0, 'max': 2000}}

TAGS = ['ambient', 'layered', 'counterdrift', 'depth', 'technical']
INTENSITY = 3
MOOD = ['technical', 'restrained', 'research']
ARCHETYPE_FIT = ['research', 'product', 'boardroom']
EMBEDDING_TEXT = 'Apply to thin divider motifs, geometric textures, or schematic accents to imply separate visual planes. It works especially well in research and technical decks where motion must stay quiet.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['axis_line_draw', 'column_rule_draw', 'audit_tick_mark']
CONFLICTS_WITH = ['counter_rotate_cog', 'orbital_accent', 'balloon_bob']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_counter_rotate, emit_fade_in
    p = dict(params or {})
    d = p.get('duration_ms', 14000)
    f = p.get('fade_ms', 450)
    emit_fade_in(slide, target_shape, delay_ms=0, duration_ms=f)
    emit_counter_rotate(slide, target_shape, duration_ms=d)
