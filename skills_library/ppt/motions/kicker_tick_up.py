"""kicker_tick_up — Tiny fly-in-from-bottom on an eyebrow/kicker — ~200ms, barely-there..

Tiny fly-in-from-bottom on an eyebrow/kicker — ~200ms, barely-there. An eyebrow/kicker tick-up in 300ms. Barely-there motion — me

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'kicker_tick_up'
CATEGORY = 'entrance'
DESCRIPTION = 'Tiny fly-in-from-bottom on an eyebrow/kicker — ~200ms, barely-there. An eyebrow/kicker tick-up in 300ms. Barely-there motion — me'

APPLICABILITY = {'roles': ['cover', 'section_divider', 'metric_dashboard', 'agenda', 'bullet_card_list'], 'anchor_names': ['eyebrow', 'kicker', 'overline', 'section_label', 'context'], 'anchor_name_regex': '(eyebrow|kicker|overline|section_label|context)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['kicker', 'tick-up', 'eyebrow', 'editorial', 'restrained']
INTENSITY = 2
MOOD = ['editorial', 'restrained', 'research', 'boardroom']
ARCHETYPE_FIT = ['narrative', 'research', 'boardroom']

EMBEDDING_TEXT = (
    'An eyebrow/kicker tick-up in 300ms. Barely-there motion — meant to prime the reader before the headline, never to compete with it.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['typewriter_clack_reveal', 'column_rule_draw']
CONFLICTS_WITH = ['bubble_pop_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fly_in, emit_fade_in
    d = int(p.get('delay_ms',60))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=260)
    emit_fly_in(slide, target_shape, direction='bottom', delay_ms=d, duration_ms=300)
