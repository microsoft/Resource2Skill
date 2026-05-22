"""Section Divider Breathe — A barely perceptible inhale-exhale scale loop that keeps divider bands and oversized labels gently alive.

Distilled from Apple HIG Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple HIG Motion'

NAME = 'section_divider_breathe'
CATEGORY = 'ambient'
DESCRIPTION = 'A barely perceptible inhale-exhale scale loop that keeps divider bands and oversized labels gently alive.'
APPLICABILITY = {'roles': ['section divider', 'background accent', 'chapter opener'], 'anchor_names': ['section_label', 'section_number', 'kicker', 'badge', 'chip'], 'max_per_slide': 2}
PARAMETERS = {'duration_ms': {'type': 'int', 'default': 5200, 'min': 2400, 'max': 12000}, 'fade_ms': {'type': 'int', 'default': 500, 'min': 0, 'max': 2000}}

TAGS = ['ambient', 'breathing', 'divider', 'subtle', 'loop']
INTENSITY = 2
MOOD = ['calm', 'restrained', 'boardroom']
ARCHETYPE_FIT = ['narrative', 'brand', 'boardroom']
EMBEDDING_TEXT = 'Use on oversized section dividers, chapter labels, or soft color bands to create a polished living-page feel. It reads as calm structure rather than overt animation.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['hairline_snap_in', 'editorial_wipe_rise', 'kicker_tick_up']
CONFLICTS_WITH = ['dramatic_zoom', 'confetti_burst', 'glitch_shear_snap']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_grow_emphasis
    p = dict(params or {})
    d = p.get('duration_ms', 5200)
    f = p.get('fade_ms', 500)
    emit_fade_in(slide, target_shape, delay_ms=0, duration_ms=f)
    emit_grow_emphasis(slide, target_shape, delay_ms=0, duration_ms=d, scale_pct=104)
