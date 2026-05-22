"""Typewriter Line Reveal — Text appears in stepped increments with a restrained left-to-right reveal suited to quotes, findings, and narrative titles.

Distilled from CSS-Tricks Typewriter Effect
Source: https://css-tricks.com/snippets/css/typewriter-effect/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://css-tricks.com/snippets/css/typewriter-effect/'
SOURCE_TITLE = 'CSS-Tricks Typewriter Effect'

NAME = 'typewriter_line_reveal'
CATEGORY = 'text'
DESCRIPTION = 'Text appears in stepped increments with a restrained left-to-right reveal suited to quotes, findings, and narrative titles.'
APPLICABILITY = {'roles': ['headline', 'title', 'quote', 'subtitle'], 'anchor_names': ['headline', 'title', 'quote', 'subtitle', 'hero_headline'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'stagger_ms': {'type': 'int', 'default': 55, 'min': 20, 'max': 150}, 'per_duration_ms': {'type': 'int', 'default': 90, 'min': 40, 'max': 220}, 'wipe_duration_ms': {'type': 'int', 'default': 700, 'min': 300, 'max': 1400}}

TAGS = ['typewriter', 'text', 'stepped', 'editorial', 'reveal']
INTENSITY = 3
MOOD = ['editorial', 'restrained', 'research']
ARCHETYPE_FIT = ['narrative', 'research', 'boardroom']
EMBEDDING_TEXT = 'Inspired by classic CSS typewriter demos, this pattern reveals a line in measured text steps. It works best for research quotes, pull-statements, and deliberate editorial titles.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['hairline_snap_in', 'kicker_tick_up', 'focus_pull_dissolve']
CONFLICTS_WITH = ['glitch_shear_snap', 'confetti_burst', 'dramatic_zoom']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_text_stagger, emit_wipe_in
    p = dict(params or {})
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=p.get('delay_ms', 0), duration_ms=p.get('wipe_duration_ms', 700))
    emit_text_stagger(slide, target_shape, delay_ms=p.get('delay_ms', 0), stagger_ms=p.get('stagger_ms', 55), per_duration_ms=p.get('per_duration_ms', 90))
