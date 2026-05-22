"""typewriter_clack_reveal — Word-by-word fade with fast stagger, like a typewriter snapping out a headline..

Word-by-word fade with fast stagger, like a typewriter snapping out a headline. Typewriter cadence: each word fades in sequentially with a 9

Category: text. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'typewriter_clack_reveal'
CATEGORY = 'text'
DESCRIPTION = 'Word-by-word fade with fast stagger, like a typewriter snapping out a headline. Typewriter cadence: each word fades in sequentially with a 9'

APPLICABILITY = {'roles': ['cover', 'hero_quote', 'section_divider', 'hero_statement'], 'anchor_names': ['headline', 'title', 'title_xl', 'quote', 'hero_headline'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['typewriter', 'editorial', 'letter-clack', 'restrained', 'headline']
INTENSITY = 4
MOOD = ['editorial', 'restrained', 'research', 'calm']
ARCHETYPE_FIT = ['narrative', 'research', 'brand']

EMBEDDING_TEXT = (
    'Typewriter cadence: each word fades in sequentially with a 90ms beat, evoking an editor clack. Best for editorial headlines and research-paper quotes — fast enough to not feel slow, restrained enough to not steal focus from content.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['headline_word_cascade', 'subhead_stagger_fade']
CONFLICTS_WITH = ['headline_prism_stagger', 'dramatic_zoom']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_text_stagger
    emit_text_stagger(slide, target_shape, delay_ms=int(p.get('delay_ms',60)), stagger_ms=int(p.get('stagger_ms',90)), per_duration_ms=int(p.get('per_duration_ms',220)))
