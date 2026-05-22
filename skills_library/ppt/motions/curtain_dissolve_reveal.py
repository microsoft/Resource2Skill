"""Curtain Dissolve Reveal — A soft curtain-like wipe layered with dissolve to introduce the next slide with restrained theatricality.

Distilled from Apple HIG Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple HIG Motion'

NAME = 'curtain_dissolve_reveal'
CATEGORY = 'transition'
DESCRIPTION = 'A soft curtain-like wipe layered with dissolve to introduce the next slide with restrained theatricality.'
APPLICABILITY = {'roles': ['transition', 'section break', 'image handoff', 'chapter opener'], 'anchor_names': ['hero_image', 'photo', 'title', 'hero_headline', 'cards'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 1200}, 'duration_ms': {'type': 'int', 'default': 700, 'min': 200, 'max': 2000}}

TAGS = ['curtain', 'wipe', 'dissolve', 'handoff', 'soft transition']
INTENSITY = 4
MOOD = ['cinematic', 'restrained', 'editorial']
ARCHETYPE_FIT = ['narrative', 'brand', 'boardroom']
EMBEDDING_TEXT = 'Inspired by Apple’s motion guidance, this reads like a stage curtain opening while the content dissolves in. It suits hero images, photos, and chapter-title handoffs.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['headline_arc_settle', 'glass_crossfade_settle', 'hero_spotlight_pull']
CONFLICTS_WITH = ['glitch_shear_snap', 'confetti_burst', 'badge_pinwheel_pop']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_wipe_in
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    dur = p.get('duration_ms', 700)
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=d, duration_ms=dur)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=max(180, int(dur * 0.75)))
