"""Tracking Word Settle — Words enter in a paced sequence with a softened fade, echoing editorial tracking-in treatments without feeling theatrical.

Distilled from Animista Text Entrances
Source: https://animista.net/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://animista.net/'
SOURCE_TITLE = 'Animista Text Entrances'

NAME = 'tracking_word_settle'
CATEGORY = 'text'
DESCRIPTION = 'Words enter in a paced sequence with a softened fade, echoing editorial tracking-in treatments without feeling theatrical.'
APPLICABILITY = {'roles': ['title', 'subtitle', 'headline', 'bullet'], 'anchor_names': ['title', 'subtitle', 'headline', 'bullet', 'items'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'stagger_ms': {'type': 'int', 'default': 90, 'min': 30, 'max': 180}, 'per_duration_ms': {'type': 'int', 'default': 160, 'min': 80, 'max': 280}, 'fade_duration_ms': {'type': 'int', 'default': 520, 'min': 200, 'max': 1000}}

TAGS = ['word-by-word', 'tracking-in', 'fade', 'editorial', 'stagger']
INTENSITY = 4
MOOD = ['editorial', 'calm', 'research']
ARCHETYPE_FIT = ['narrative', 'research', 'brand']
EMBEDDING_TEXT = 'Based on popular Animista text entrance treatments, this pattern reveals language by word groups rather than flashy character effects. It suits editorial titles, summaries, and evidence-led bullets.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['editorial_wipe_rise', 'margin_note_drop', 'gentle_rise_fade']
CONFLICTS_WITH = ['bounce_in', 'badge_pinwheel_pop', 'hero_metric_surge_settle']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_text_stagger
    p = dict(params or {})
    emit_fade_in(slide, target_shape, delay_ms=p.get('delay_ms', 0), duration_ms=p.get('fade_duration_ms', 520))
    emit_text_stagger(slide, target_shape, delay_ms=p.get('delay_ms', 0), stagger_ms=p.get('stagger_ms', 90), per_duration_ms=p.get('per_duration_ms', 160))
