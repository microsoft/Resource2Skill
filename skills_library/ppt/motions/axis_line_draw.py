"""axis_line_draw — Line grow along x-axis — for drawing chart axes, progress bars, timeline rules..

Line grow along x-axis — for drawing chart axes, progress bars, timeline rules. A chart axis drawing across the slide in 900ms — the motion 

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'axis_line_draw'
CATEGORY = 'entrance'
DESCRIPTION = 'Line grow along x-axis — for drawing chart axes, progress bars, timeline rules. A chart axis drawing across the slide in 900ms — the motion '

APPLICABILITY = {'roles': ['metric_dashboard', 'timeline_horizontal', 'comparison_split'], 'anchor_names': ['axis', 'axis_line', 'rule', 'timeline', 'progress_bar', 'baseline'], 'anchor_name_regex': '(axis|rule|timeline|baseline|progress)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['axis', 'line-grow', 'data', 'chart', 'technical']
INTENSITY = 4
MOOD = ['technical', 'boardroom', 'restrained']
ARCHETYPE_FIT = ['data', 'boardroom', 'product']

EMBEDDING_TEXT = (
    'A chart axis drawing across the slide in 900ms — the motion signature of a data-heavy board page. Pair with axis_line anchor names on the rendered slide.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['hairline_snap_in', 'row_cascade_settle']
CONFLICTS_WITH = ['cinematic_letterbox_iris', 'bubble_pop_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_wipe_in
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=int(p.get('delay_ms',120)), duration_ms=int(p.get('duration_ms',900)))
