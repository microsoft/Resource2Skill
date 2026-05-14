"""KPI Status Ping — A quick pulse for a metric tile or number that signals importance like a status ping.

Distilled from web.dev High-performance CSS animations
Source: https://web.dev/articles/animations-guide
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://web.dev/articles/animations-guide'
SOURCE_TITLE = 'web.dev High-performance CSS animations'

NAME = 'kpi_status_ping'
CATEGORY = 'emphasis'
DESCRIPTION = 'A quick pulse for a metric tile or number that signals importance like a status ping.'
APPLICABILITY = {'roles': ['kpi', 'metric highlight', 'dashboard'], 'anchor_names': ['metric_xl', 'value', 'label', 'cards', 'badge'], 'max_per_slide': 3}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'duration_ms': {'type': 'int', 'default': 320, 'min': 160, 'max': 900}, 'scale_pct': {'type': 'int', 'default': 112, 'min': 106, 'max': 120}, 'repeats': {'type': 'int', 'default': 1, 'min': 1, 'max': 2}}

TAGS = ['kpi', 'metric', 'pulse', 'dashboard', 'attention']
INTENSITY = 6
MOOD = ['technical', 'boardroom', 'restrained']
ARCHETYPE_FIT = ['data', 'boardroom', 'product']
EMBEDDING_TEXT = 'Ideal for a single metric, KPI card, or standout number that needs a brief extra beat. It reads cleanly in boardroom dashboards and quarterly business review slides.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['chart_bar_grow', 'count_up_metric', 'metric_bloom_echo']
CONFLICTS_WITH = ['hero_metric_heartbeat_loop', 'confetti_burst', 'badge_pinwheel_pop']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_pulse
    p = dict(params or {})
    emit_pulse(slide, target_shape, p.get('delay_ms', 0), p.get('duration_ms', 320), scale_pct=p.get('scale_pct', 112), repeats=p.get('repeats', 1))
