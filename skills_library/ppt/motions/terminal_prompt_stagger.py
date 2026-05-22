"""Terminal Prompt Stagger — A stepped text reveal that mimics command-line output appearing line by line with a subtle prompt settle.

Distilled from Fluent 2 Motion
Source: https://fluent2.microsoft.design/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://fluent2.microsoft.design/motion'
SOURCE_TITLE = 'Fluent 2 Motion'

NAME = 'terminal_prompt_stagger'
CATEGORY = 'text'
DESCRIPTION = 'A stepped text reveal that mimics command-line output appearing line by line with a subtle prompt settle.'
APPLICABILITY = {'roles': ['code slide', 'CLI demo', 'log output', 'technical recap'], 'anchor_names': ['title', 'subtitle', 'quote', 'items', 'bullet', 'label', 'cta'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'stagger_ms': {'type': 'int', 'default': 55, 'min': 20, 'max': 200}, 'per_duration_ms': {'type': 'int', 'default': 140, 'min': 60, 'max': 400}}

TAGS = ['terminal', 'type', 'stagger', 'command-line', 'output']
INTENSITY = 3
MOOD = ['technical', 'restrained', 'boardroom']
ARCHETYPE_FIT = ['product', 'data', 'research', 'boardroom']
EMBEDDING_TEXT = 'Ideal for shell commands, SQL snippets, and progressive findings where the audience should read output in controlled, sequential beats.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['bullet_stagger_reveal', 'column_rule_draw', 'metric_snap_focus']
CONFLICTS_WITH = ['marquee_ticker_slide', 'jelly_title_bounce', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_grow_emphasis, emit_text_stagger
    p = dict(params or {})
    d = int(p.get('delay_ms', 0))
    st = int(p.get('stagger_ms', 55))
    per = int(p.get('per_duration_ms', 140))
    emit_text_stagger(slide, target_shape, d, st, per)
    emit_grow_emphasis(slide, target_shape, d + st * 4, 140, scale_pct=102)
