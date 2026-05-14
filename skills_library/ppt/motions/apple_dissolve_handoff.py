"""Apple Dissolve Handoff — A restrained crossfade handoff for incoming slide content with a barely perceptible lateral settle.

Distilled from Apple Human Interface Guidelines — Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple Human Interface Guidelines — Motion'

NAME = 'apple_dissolve_handoff'
CATEGORY = 'transition'
DESCRIPTION = 'A restrained crossfade handoff for incoming slide content with a barely perceptible lateral settle.'
APPLICABILITY = {'roles': ['title', 'section transition', 'hero swap', 'content handoff'], 'anchor_names': ['title', 'subtitle', 'photo', 'hero_image', 'cards'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 420, 'min': 150, 'max': 1200}, 'drift_ms': {'type': 'int', 'default': 320, 'min': 120, 'max': 900}}

TAGS = ['dissolve', 'crossfade', 'handoff', 'ios', 'restrained']
INTENSITY = 3
MOOD = ['calm', 'restrained', 'boardroom']
ARCHETYPE_FIT = ['product', 'boardroom', 'narrative']
EMBEDDING_TEXT = 'Based on Apple’s motion guidance favoring continuity and unobtrusive transitions. It reads like a slide-to-slide dissolve with just enough directional drift to imply progression.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['editorial_side_nudge', 'bullet_stagger_reveal', 'metric_snap_focus']
CONFLICTS_WITH = ['dramatic_zoom', 'glitch_shear_snap', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    dur = p.get('duration_ms', 420)
    drift = p.get('drift_ms', 320)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=dur)
    emit_fly_in(slide, target_shape, direction='right', delay_ms=d, duration_ms=drift)
