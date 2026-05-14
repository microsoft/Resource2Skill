"""hairline_snap_in — Fast wipe + no flourish. Precise and restrained — boardroom-safe..

Fast wipe + no flourish. Precise and restrained — boardroom-safe. Fast 350ms left-to-right wipe. No bounce, no scale. Delibera

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'hairline_snap_in'
CATEGORY = 'entrance'
DESCRIPTION = 'Fast wipe + no flourish. Precise and restrained — boardroom-safe. Fast 350ms left-to-right wipe. No bounce, no scale. Delibera'

APPLICABILITY = {'roles': ['metric_dashboard', 'bullet_card_list', 'section_divider', 'closing_cta'], 'anchor_names': ['rule', 'divider', 'header_line', 'border', 'panel'], 'anchor_name_regex': '(rule|divider|border|row)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['hairline', 'precise', 'boardroom', 'restrained', 'snap']
INTENSITY = 3
MOOD = ['boardroom', 'restrained', 'technical']
ARCHETYPE_FIT = ['boardroom', 'data']

EMBEDDING_TEXT = (
    'Fast 350ms left-to-right wipe. No bounce, no scale. Deliberately boring — the motion equivalent of a Helvetica rule. Best for board meetings and financial updates.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['column_rule_draw']
CONFLICTS_WITH = ['bubble_pop_reveal', 'neon_outline_trace']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_wipe_in
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=int(p.get('delay_ms',60)), duration_ms=int(p.get('duration_ms',350)))
