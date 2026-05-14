"""Audit Pass Glide — A restrained confirmation glides in and finishes with a light pulse, signaling checked evidence without celebration.

Distilled from web.dev High-performance CSS animations
Source: https://web.dev/articles/animations-guide
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://web.dev/articles/animations-guide'
SOURCE_TITLE = 'web.dev High-performance CSS animations'

NAME = 'audit_pass_glide'
CATEGORY = 'emphasis'
DESCRIPTION = 'A restrained confirmation glides in and finishes with a light pulse, signaling checked evidence without celebration.'
APPLICABILITY = {'roles': ['research', 'data', 'product'], 'anchor_names': ['icon', 'badge', 'label', 'bullet', 'timeline_node'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 80, 'min': 0, 'max': 1200}, 'duration_ms': {'type': 'int', 'default': 340, 'min': 180, 'max': 900}}

TAGS = ['audit', 'confirm', 'tick', 'glide', 'pulse']
INTENSITY = 3
MOOD = ['restrained', 'research', 'technical']
ARCHETYPE_FIT = ['research', 'data', 'product']
EMBEDDING_TEXT = 'Use on audit checks, status confirmations, or evidence markers. It reads as verified and controlled, with just enough motion to register completion.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['metric_snap_focus', 'bullet_stagger_reveal', 'card_rise_settle']
CONFLICTS_WITH = ['audit_tick_mark', 'kpi_status_ping', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_pulse
    p = dict(params or {})
    d = p.get('delay_ms', 80)
    t = p.get('duration_ms', 340)
    emit_fly_in(slide, target_shape, direction='right', delay_ms=d, duration_ms=t)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=max(180, int(t * 0.7)))
    emit_pulse(slide, target_shape, delay_ms=d + t, duration_ms=220, scale_pct=106, repeats=1)
