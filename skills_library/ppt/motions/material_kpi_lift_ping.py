"""Material KPI Lift Ping — A restrained scale lift followed by one clean pulse gives a metric momentary priority.

Distilled from Material 3 Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material 3 Motion Overview'

NAME = 'material_kpi_lift_ping'
CATEGORY = 'emphasis'
DESCRIPTION = 'A restrained scale lift followed by one clean pulse gives a metric momentary priority.'
APPLICABILITY = {'roles': ['data', 'product', 'boardroom'], 'anchor_names': ['metric_xl', 'value', 'label', 'cards'], 'max_per_slide': 3}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'duration_ms': {'type': 'int', 'default': 520, 'min': 240, 'max': 1400}, 'scale_pct': {'type': 'int', 'default': 110, 'min': 104, 'max': 120}}

TAGS = ['kpi', 'metric', 'priority', 'scale', 'restrained']
INTENSITY = 4
MOOD = ['restrained', 'technical', 'boardroom']
ARCHETYPE_FIT = ['data', 'product', 'boardroom']
EMBEDDING_TEXT = 'Best for a single KPI or highlighted value in a board slide. The effect suggests priority and state change without feeling flashy.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['chart_bar_grow', 'count_up_metric', 'audit_pass_glide']
CONFLICTS_WITH = ['hero_metric_heartbeat_loop', 'dramatic_zoom', 'badge_pinwheel_pop']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_grow_emphasis, emit_pulse
    p = dict(params or {})
    emit_grow_emphasis(slide, target_shape, p.get('delay_ms', 0), int(p.get('duration_ms', 520) * 0.6), scale_pct=p.get('scale_pct', 110))
    emit_pulse(slide, target_shape, p.get('delay_ms', 0) + int(p.get('duration_ms', 520) * 0.52), int(p.get('duration_ms', 520) * 0.48), scale_pct=p.get('scale_pct', 110), repeats=1)
