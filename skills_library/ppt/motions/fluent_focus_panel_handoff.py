"""Fluent Focus Panel Handoff — Section label, title, and side panel hand off attention with a crisp panel wipe and restrained button finish.

Distilled from Fluent 2 — Motion
Source: https://fluent2.microsoft.design/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://fluent2.microsoft.design/motion'
SOURCE_TITLE = 'Fluent 2 — Motion'

NAME = 'fluent_focus_panel_handoff'
CATEGORY = 'composite'
DESCRIPTION = 'Section label, title, and side panel hand off attention with a crisp panel wipe and restrained button finish.'
APPLICABILITY = {'roles': ['section break', 'comparison panel', 'enterprise product slide'], 'anchor_names': ['section_label', 'title', 'items', 'photo', 'button'], 'max_per_slide': 1}
PARAMETERS = {'delay': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'step': {'type': 'int', 'default': 110, 'min': 40, 'max': 320}, 'duration': {'type': 'int', 'default': 380, 'min': 180, 'max': 1000}}

TAGS = ['fluent', 'panel', 'handoff', 'enterprise', 'wipe']
INTENSITY = 4
MOOD = ['boardroom', 'technical', 'restrained']
ARCHETYPE_FIT = ['boardroom', 'product', 'research']
EMBEDDING_TEXT = 'A Fluent-style handoff uses directional motion to move attention from heading to panel content without excess drama. Strong for enterprise narratives, side-by-side comparisons, and structured reveals.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['audit_pass_glide', 'column_rule_draw', 'metric_bloom_echo']
CONFLICTS_WITH = ['confetti_burst', 'badge_pinwheel_pop', 'chromatic_stutter']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_grow_emphasis, emit_text_stagger, emit_wipe_in
    p = dict(params or {})
    d=p.get('delay',0); s=p.get('step',110); t=p.get('duration',380); x=target_shape
    emit_fade_in(slide, x.get('section_label', x), d, 140)
    emit_fly_in(slide, x.get('title', x), direction='left', delay_ms=d+s, duration_ms=t)
    emit_wipe_in(slide, x.get('photo', x), direction='right', delay_ms=d+s, duration_ms=t+80)
    emit_text_stagger(slide, x.get('items', x), d+s*2, 70, 220)
    emit_grow_emphasis(slide, x.get('button', x), d+s*3, 180, scale_pct=106)
