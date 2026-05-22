"""Apple Soft Breathe — A large background shape gently settles in and performs a near-imperceptible breathing scale.

Distilled from Apple HIG Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple HIG Motion'

NAME = 'apple_soft_breathe'
CATEGORY = 'ambient'
DESCRIPTION = 'A large background shape gently settles in and performs a near-imperceptible breathing scale.'
APPLICABILITY = {'roles': ['background texture', 'hero backdrop', 'quiet emphasis'], 'anchor_names': ['photo', 'hero_image', 'badge', 'chip'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'intro_ms': {'type': 'int', 'default': 700, 'min': 200, 'max': 2000}, 'pulse_ms': {'type': 'int', 'default': 5000, 'min': 1200, 'max': 12000}, 'scale_pct': {'type': 'int', 'default': 103, 'min': 101, 'max': 108}}

TAGS = ['breathing', 'settle', 'soft', 'background', 'minimal']
INTENSITY = 1
MOOD = ['calm', 'restrained', 'warm']
ARCHETYPE_FIT = ['brand', 'product', 'narrative']
EMBEDDING_TEXT = 'This is a subtle, premium-feeling inhale-exhale for oversized backdrops or blurred color fields. It should read as atmosphere, not attention-seeking animation.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['apple_dissolve_handoff', 'focus_pull_dissolve', 'editorial_wipe_rise']
CONFLICTS_WITH = ['breathing_halo', 'hero_metric_heartbeat_loop', 'jelly_title_bounce']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_pulse
    p = dict(params or {})
    d = int(p.get('delay_ms', 0))
    intro = int(p.get('intro_ms', 700))
    pulse = int(p.get('pulse_ms', 5000))
    scale = int(p.get('scale_pct', 103))
    emit_fade_in(slide, target_shape, d, intro)
    emit_pulse(slide, target_shape, d + intro, pulse, scale_pct=scale, repeats=2)
