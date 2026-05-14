"""Jelly Title Bounce — Text lands with a soft bouncy stagger, like playful sticker lettering in a kid-friendly interface.

Distilled from Animista
Source: https://animista.net/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://animista.net/'
SOURCE_TITLE = 'Animista'

NAME = 'jelly_title_bounce'
CATEGORY = 'text'
DESCRIPTION = 'Text lands with a soft bouncy stagger, like playful sticker lettering in a kid-friendly interface.'
APPLICABILITY = {'roles': ['headline reveal', 'playful section intro', 'youthful brand moment'], 'anchor_names': ['headline', 'title', 'title_xl', 'hero_headline', 'kicker'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'stagger_ms': {'type': 'int', 'default': 45, 'min': 20, 'max': 120}, 'per_duration_ms': {'type': 'int', 'default': 240, 'min': 120, 'max': 500}, 'pulse_pct': {'type': 'int', 'default': 106, 'min': 102, 'max': 112}}

TAGS = ['text', 'bounce', 'jelly', 'stagger', 'sticker']
INTENSITY = 7
MOOD = ['playful', 'warm', 'bold']
ARCHETYPE_FIT = ['brand', 'narrative', 'product']
EMBEDDING_TEXT = 'A staggered title treatment with a soft jelly-like bounce, echoing the playful text entrances popular in CSS animation galleries and kid-friendly web branding.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['eyebrow_tick_in', 'metric_digit_pop_stagger', 'bubble_pop_reveal']
CONFLICTS_WITH = ['headline_letterpress_stagger', 'headline_prism_stagger', 'editorial_ink_bleed']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_pulse, emit_text_stagger
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    st = p.get('stagger_ms', 45)
    pd = p.get('per_duration_ms', 240)
    pp = p.get('pulse_pct', 106)
    emit_text_stagger(slide, target_shape, d, st, pd)
    emit_pulse(slide, target_shape, d + st, int(pd * 0.9), scale_pct=pp, repeats=1)
