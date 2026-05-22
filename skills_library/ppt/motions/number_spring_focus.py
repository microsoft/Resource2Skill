"""Number Spring Focus — A compact zoom-in with a soft bounce helps a large number steal attention on arrival.

Distilled from Motion Animate Docs
Source: https://motion.dev/docs/animate
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://motion.dev/docs/animate'
SOURCE_TITLE = 'Motion Animate Docs'

NAME = 'number_spring_focus'
CATEGORY = 'emphasis'
DESCRIPTION = 'A compact zoom-in with a soft bounce helps a large number steal attention on arrival.'
APPLICABILITY = {'roles': ['data', 'product', 'boardroom'], 'anchor_names': ['metric_xl', 'value', 'title_xl', 'headline'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'duration_ms': {'type': 'int', 'default': 560, 'min': 260, 'max': 1400}, 'scale_from': {'type': 'int', 'default': 55, 'min': 30, 'max': 80}}

TAGS = ['number', 'zoom', 'bounce', 'arrival', 'attention']
INTENSITY = 7
MOOD = ['bold', 'punchy', 'technical']
ARCHETYPE_FIT = ['data', 'product', 'boardroom']
EMBEDDING_TEXT = 'Use when a top-line number must command the slide the instant it appears. It lands with springy conviction, then settles quickly for reading.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['kicker_tick_up', 'axis_line_draw', 'chart_peak_ping']
CONFLICTS_WITH = ['bounce_in', 'jelly_title_bounce', 'dramatic_zoom']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_bounce_in, emit_grow_from_small
    p = dict(params or {})
    emit_grow_from_small(slide, target_shape, p.get('delay_ms', 0), int(p.get('duration_ms', 560) * 0.55), scale_from=p.get('scale_from', 55) / 100.0)
    emit_bounce_in(slide, target_shape, p.get('delay_ms', 0) + int(p.get('duration_ms', 560) * 0.38), int(p.get('duration_ms', 560) * 0.62))
