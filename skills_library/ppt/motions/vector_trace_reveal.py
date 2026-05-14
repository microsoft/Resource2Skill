"""Vector Trace Reveal — A directional line-draw style entrance that makes labels, rules, and nodes appear as if being traced live.

Distilled from web.dev Learn CSS Animations
Source: https://web.dev/learn/css/animations/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://web.dev/learn/css/animations/'
SOURCE_TITLE = 'web.dev Learn CSS Animations'

NAME = 'vector_trace_reveal'
CATEGORY = 'entrance'
DESCRIPTION = 'A directional line-draw style entrance that makes labels, rules, and nodes appear as if being traced live.'
APPLICABILITY = {'roles': ['diagram build', 'process slide', 'system architecture'], 'anchor_names': ['section_label', 'timeline_node', 'icon', 'bullet', 'label', 'items'], 'max_per_slide': 3}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'duration_ms': {'type': 'int', 'default': 420, 'min': 200, 'max': 1200}}

TAGS = ['trace', 'draw', 'line', 'vector', 'diagram']
INTENSITY = 4
MOOD = ['technical', 'restrained', 'research']
ARCHETYPE_FIT = ['data', 'research', 'boardroom']
EMBEDDING_TEXT = 'Use on architecture labels, flow nodes, and diagram callouts when you want a precise, plotted feel instead of a generic fade.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['axis_line_draw', 'hairline_snap_in', 'audit_tick_mark']
CONFLICTS_WITH = ['cinematic_veil_reveal', 'confetti_burst', 'dramatic_zoom']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_wipe_in
    p = dict(params or {})
    d = int(p.get('delay_ms', 0))
    dur = int(p.get('duration_ms', 420))
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=d, duration_ms=int(dur * 0.7))
    emit_fade_in(slide, target_shape, d, int(dur * 0.45))
