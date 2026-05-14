"""Depth Hierarchy Reveal — A layered entrance that establishes information hierarchy with restrained depth, opacity, and timing offsets.

Distilled from Apple HIG Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple HIG Motion'

NAME = 'hig_depth_hierarchy_reveal'
CATEGORY = 'composite'
DESCRIPTION = 'A layered entrance that establishes information hierarchy with restrained depth, opacity, and timing offsets.'
APPLICABILITY = {'roles': ['title slide', 'executive summary', 'product hero'], 'anchor_names': ['eyebrow', 'title_xl', 'subtitle', 'photo', 'button'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'dur_ms': {'type': 'int', 'default': 600, 'min': 240, 'max': 1600}}

TAGS = ['hierarchy', 'depth', 'subtle', 'hero', 'layered']
INTENSITY = 4
MOOD = ['calm', 'editorial', 'restrained']
ARCHETYPE_FIT = ['brand', 'product', 'boardroom']
EMBEDDING_TEXT = 'This follows Apple’s hierarchy-first motion language: primary content settles with minimal scale change, secondary elements lag slightly, and the image adds soft spatial depth.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['editorial_side_nudge', 'focus_pull_dissolve', 'badge_swing_in']
CONFLICTS_WITH = ['bounce_in', 'confetti_burst', 'chromatic_stutter']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_grow_from_small, emit_wipe_in, emit_zoom_in
    p = dict(params or {})
    d = p.get('delay_ms', 0); dur = p.get('dur_ms', 600)
    emit_fade_in(slide, target_shape.get('eyebrow'), delay_ms=d, duration_ms=dur-180)
    emit_grow_from_small(slide, target_shape.get('title_xl'), delay_ms=d+70, duration_ms=dur, scale_from=0.92)
    emit_fly_in(slide, target_shape.get('subtitle'), direction='bottom', delay_ms=d+150, duration_ms=dur-120)
    emit_zoom_in(slide, target_shape.get('photo'), delay_ms=d+40, duration_ms=dur+120)
    emit_wipe_in(slide, target_shape.get('button'), direction='left', delay_ms=d+240, duration_ms=dur-220)
