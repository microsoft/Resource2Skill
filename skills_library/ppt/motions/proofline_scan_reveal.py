"""Proofline Scan Reveal — A thin measured wipe reveals a rule or divider with quiet analytical pacing.

Distilled from Apple HIG Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple HIG Motion'

NAME = 'proofline_scan_reveal'
CATEGORY = 'entrance'
DESCRIPTION = 'A thin measured wipe reveals a rule or divider with quiet analytical pacing.'
APPLICABILITY = {'roles': ['research', 'boardroom', 'data'], 'anchor_names': ['section_label', 'section_number', 'timeline_node', 'quote'], 'max_per_slide': 3}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 1200}, 'duration_ms': {'type': 'int', 'default': 420, 'min': 180, 'max': 900}}

TAGS = ['hairline', 'rule', 'measured', 'wipe', 'divider']
INTENSITY = 2
MOOD = ['restrained', 'research', 'technical']
ARCHETYPE_FIT = ['research', 'data', 'boardroom']
EMBEDDING_TEXT = 'Use for hairlines, dividers, or subtle thesis separators. It feels like a precise scan across a page rather than a decorative flourish.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['bullet_stagger_reveal', 'metric_snap_focus', 'focus_pull_dissolve']
CONFLICTS_WITH = ['confetti_burst', 'dramatic_zoom', 'jelly_title_bounce']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_wipe_in
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    t = p.get('duration_ms', 420)
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=d, duration_ms=t)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=max(180, int(t * 0.75)))
