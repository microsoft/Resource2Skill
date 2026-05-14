"""bar_grow_cohort — Staggered grow-from-small on each bar-like shape in a cohort chart..

Staggered grow-from-small on each bar-like shape in a cohort chart. Each bar grows from ~18% to 100% over 750ms. Designed to ani

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'bar_grow_cohort'
CATEGORY = 'entrance'
DESCRIPTION = 'Staggered grow-from-small on each bar-like shape in a cohort chart. Each bar grows from ~18% to 100% over 750ms. Designed to ani'

APPLICABILITY = {'roles': ['metric_dashboard', 'comparison_split', 'feature_grid'], 'anchor_names': ['bar', 'col', 'chart_bar', 'series', 'column'], 'anchor_name_regex': '(bar|col|chart|series|column)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['bar-grow', 'chart', 'data', 'cohort', 'staccato']
INTENSITY = 5
MOOD = ['technical', 'boardroom', 'bold']
ARCHETYPE_FIT = ['data', 'boardroom']

EMBEDDING_TEXT = (
    'Each bar grows from ~18% to 100% over 750ms. Designed to animate an implicit cohort chart where each shape is one bar in a series.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['axis_line_draw']
CONFLICTS_WITH = ['cinematic_letterbox_iris']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_grow_from_small
    emit_grow_from_small(slide, target_shape, delay_ms=int(p.get('delay_ms',220)), duration_ms=int(p.get('duration_ms',750)), from_pct=int(p.get('from_pct',18)))
