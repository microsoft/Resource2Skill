"""Research Word-by-Word Reveal — Reveals text in paced word groups for measured editorial and research narratives.

Distilled from Motion stagger docs
Source: https://motion.dev/docs/stagger
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://motion.dev/docs/stagger'
SOURCE_TITLE = 'Motion stagger docs'

NAME = 'research_word_by_word_reveal'
CATEGORY = 'text'
DESCRIPTION = 'Reveals text in paced word groups for measured editorial and research narratives.'
APPLICABILITY = {'roles': ['headline', 'subhead', 'quote', 'key finding'], 'anchor_names': ['headline', 'title', 'title_xl', 'subtitle', 'quote', 'hero_headline'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'stagger_ms': {'type': 'int', 'default': 80, 'min': 20, 'max': 300}, 'per_duration_ms': {'type': 'int', 'default': 320, 'min': 120, 'max': 900}}

TAGS = ['text', 'stagger', 'words', 'editorial', 'research']
INTENSITY = 3
MOOD = ['editorial', 'restrained', 'research']
ARCHETYPE_FIT = ['research', 'narrative', 'boardroom']
EMBEDDING_TEXT = 'A measured text stagger inspired by modern UI choreography docs. Best for headlines, quotes, and findings that should unfold with clarity instead of spectacle.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['axis_line_draw', 'column_rule_draw', 'gentle_rise_fade']
CONFLICTS_WITH = ['headline_prism_stagger', 'glitch_shear_snap', 'jelly_title_bounce']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_text_stagger
    p = dict(params or {})
    emit_text_stagger(slide, target_shape,
        delay_ms=p.get('delay_ms', 0),
        stagger_ms=p.get('stagger_ms', 80),
        per_duration_ms=p.get('per_duration_ms', 320))
