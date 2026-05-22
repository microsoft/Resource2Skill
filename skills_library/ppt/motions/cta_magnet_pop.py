"""CTA Magnet Pop — A quick oversized pulse makes the button feel tappable without turning into a loop.

Distilled from Animista Pulsate
Source: https://animista.net/play/attention/pulsate
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://animista.net/play/attention/pulsate'
SOURCE_TITLE = 'Animista Pulsate'

NAME = 'cta_magnet_pop'
CATEGORY = 'emphasis'
DESCRIPTION = 'A quick oversized pulse makes the button feel tappable without turning into a loop.'
APPLICABILITY = {'roles': ['product', 'brand', 'boardroom'], 'anchor_names': ['cta', 'button', 'badge', 'chip'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'duration_ms': {'type': 'int', 'default': 420, 'min': 180, 'max': 1200}, 'scale_pct': {'type': 'int', 'default': 114, 'min': 106, 'max': 130}}

TAGS = ['cta', 'pulse', 'attention', 'button', 'tap-target']
INTENSITY = 6
MOOD = ['bold', 'punchy', 'boardroom']
ARCHETYPE_FIT = ['product', 'brand', 'boardroom']
EMBEDDING_TEXT = 'Use on a primary CTA or button after surrounding content settles. It reads like a single magnetic tap cue rather than a decorative bounce.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['bullet_stagger_reveal', 'card_rise_settle', 'hairline_snap_in']
CONFLICTS_WITH = ['cta_attention_pulse', 'confetti_burst', 'glitch_shear_snap']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_grow_emphasis, emit_pulse
    p = dict(params or {})
    emit_grow_emphasis(slide, target_shape, p.get('delay_ms', 0), p.get('duration_ms', 420), scale_pct=p.get('scale_pct', 114))
    emit_pulse(slide, target_shape, p.get('delay_ms', 0) + int(p.get('duration_ms', 420) * 0.45), int(p.get('duration_ms', 420) * 0.55), scale_pct=max(108, p.get('scale_pct', 114) - 2), repeats=1)
