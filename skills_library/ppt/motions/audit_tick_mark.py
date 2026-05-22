"""audit_tick_mark — Small pulse once a shape has landed — reads as a checkbox tick after a line-item review..

Small pulse once a shape has landed — reads as a checkbox tick after a line-item review. A single late-arrival pulse on a delta indicator — the motio

Category: emphasis. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'audit_tick_mark'
CATEGORY = 'emphasis'
DESCRIPTION = 'Small pulse once a shape has landed — reads as a checkbox tick after a line-item review. A single late-arrival pulse on a delta indicator — the motio'

APPLICABILITY = {'roles': ['metric_dashboard', 'bullet_card_list', 'closing_cta', 'comparison_split'], 'anchor_names': ['delta', 'check', 'tick', 'success', 'indicator'], 'anchor_name_regex': '(delta|tick|check|success|indicator)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['audit', 'tick', 'boardroom', 'precise', 'confirmation']
INTENSITY = 4
MOOD = ['boardroom', 'restrained', 'technical']
ARCHETYPE_FIT = ['boardroom', 'data']

EMBEDDING_TEXT = (
    'A single late-arrival pulse on a delta indicator — the motion version of stamping APPROVED on a financial ledger row.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['hairline_snap_in']
CONFLICTS_WITH = ['breathing_halo']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    emit_pulse(slide, target_shape, delay_ms=int(p.get('delay_ms',800)), duration_ms=320, scale_pct=112, repeats=1)
