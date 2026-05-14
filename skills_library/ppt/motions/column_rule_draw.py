"""column_rule_draw — Vertical line grow from top to bottom, simulating an editorial column rule drawing in..

Vertical line grow from top to bottom, simulating an editorial column rule drawing in. A vertical editorial column rule drawing in top-down over 65

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'column_rule_draw'
CATEGORY = 'entrance'
DESCRIPTION = 'Vertical line grow from top to bottom, simulating an editorial column rule drawing in. A vertical editorial column rule drawing in top-down over 65'

APPLICABILITY = {'roles': ['section_divider', 'agenda', 'bullet_card_list'], 'anchor_names': ['rule', 'divider', 'column_rule', 'border'], 'anchor_name_regex': '(rule|hairline|divider)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['editorial', 'rule-draw', 'thin', 'vertical']
INTENSITY = 2
MOOD = ['editorial', 'restrained', 'research']
ARCHETYPE_FIT = ['narrative', 'research']

EMBEDDING_TEXT = (
    'A vertical editorial column rule drawing in top-down over 650ms. Great on agenda rails and section dividers in restrained, paper-toned themes.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['editorial_ink_bleed']
CONFLICTS_WITH = ['dramatic_zoom', 'bounce_in']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_wipe_in
    emit_wipe_in(slide, target_shape, direction='top', delay_ms=int(p.get('delay_ms',80)), duration_ms=int(p.get('duration_ms',650)))
