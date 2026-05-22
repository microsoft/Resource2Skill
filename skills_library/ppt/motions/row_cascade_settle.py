"""row_cascade_settle — Staggered fade-in on paragraphs inside a list shape — rows appear one by one..

Staggered fade-in on paragraphs inside a list shape — rows appear one by one. List rows fade in top-to-bottom with a 140ms beat. Perfect f

Category: text. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'row_cascade_settle'
CATEGORY = 'text'
DESCRIPTION = 'Staggered fade-in on paragraphs inside a list shape — rows appear one by one. List rows fade in top-to-bottom with a 140ms beat. Perfect f'

APPLICABILITY = {'roles': ['metric_dashboard', 'bullet_card_list', 'agenda', 'timeline_horizontal'], 'anchor_names': ['items', 'bullets', 'rows', 'kpis', 'quarters'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['row-cascade', 'boardroom', 'list', 'staccato', 'precise']
INTENSITY = 4
MOOD = ['boardroom', 'restrained', 'editorial', 'technical']
ARCHETYPE_FIT = ['boardroom', 'data', 'narrative']

EMBEDDING_TEXT = (
    'List rows fade in top-to-bottom with a 140ms beat. Perfect for boardroom KPI tables and meeting agendas. Signals structure, not drama.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['hairline_snap_in']
CONFLICTS_WITH = ['bubble_pop_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_text_stagger
    emit_text_stagger(slide, target_shape, delay_ms=int(p.get('delay_ms',100)), stagger_ms=int(p.get('stagger_ms',140)), per_duration_ms=int(p.get('per_duration_ms',300)))
