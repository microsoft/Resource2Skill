"""Rubber Pop Wiggle — A squishy pop-in with a tiny overshoot that feels toy-like, soft, and inviting.

Distilled from Motion animate docs
Source: https://motion.dev/docs/animate
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://motion.dev/docs/animate'
SOURCE_TITLE = 'Motion animate docs'

NAME = 'rubber_pop_wiggle'
CATEGORY = 'composite'
DESCRIPTION = 'A squishy pop-in with a tiny overshoot that feels toy-like, soft, and inviting.'
APPLICABILITY = {'roles': ['highlight', 'cta', 'reaction', 'reward'], 'anchor_names': ['cta', 'button', 'badge', 'chip', 'icon', 'metric_xl'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 520, 'min': 180, 'max': 1500}, 'scale_from': {'type': 'int', 'default': 55, 'min': 30, 'max': 80}, 'pulse_pct': {'type': 'int', 'default': 114, 'min': 105, 'max': 130}}

TAGS = ['rubber', 'pop', 'overshoot', 'organic', 'playful']
INTENSITY = 5
MOOD = ['playful', 'warm']
ARCHETYPE_FIT = ['brand', 'product', 'narrative']
EMBEDDING_TEXT = 'Best for playful CTAs, stickers, or reward states. The shape pops from small, then stretches slightly past final size for a soft rubbery finish.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['gentle_rise_fade', 'hero_metric_heartbeat_loop', 'bullet_stagger_reveal']
CONFLICTS_WITH = ['dramatic_zoom', 'headline_prism_stagger', 'glitch_shear_snap']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_grow_from_small, emit_pulse
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    dur = p.get('duration_ms', 520)
    sf = p.get('scale_from', 55) / 100.0
    pp = p.get('pulse_pct', 114)
    emit_grow_from_small(slide, target_shape, delay_ms=d, duration_ms=int(dur * 0.72), scale_from=sf)
    emit_pulse(slide, target_shape, delay_ms=d + int(dur * 0.58), duration_ms=int(dur * 0.42), scale_pct=pp, repeats=1)
