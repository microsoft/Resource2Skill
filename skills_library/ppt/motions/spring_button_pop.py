"""Spring Button Pop — A quick springy pop that makes buttons and chips feel friendly, tactile, and kid-safe.

Distilled from Motion.dev Docs
Source: https://motion.dev/docs
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://motion.dev/docs'
SOURCE_TITLE = 'Motion.dev Docs'

NAME = 'spring_button_pop'
CATEGORY = 'emphasis'
DESCRIPTION = 'A quick springy pop that makes buttons and chips feel friendly, tactile, and kid-safe.'
APPLICABILITY = {'roles': ['cta', 'ui emphasis', 'action cue'], 'anchor_names': ['cta', 'button', 'chip', 'badge', 'icon'], 'max_per_slide': 3}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 420, 'min': 180, 'max': 900}, 'scale_from': {'type': 'int', 'default': 55, 'min': 30, 'max': 80}, 'pulse_pct': {'type': 'int', 'default': 108, 'min': 102, 'max': 120}}

TAGS = ['spring', 'pop', 'button', 'friendly', 'microinteraction']
INTENSITY = 6
MOOD = ['playful', 'warm', 'punchy']
ARCHETYPE_FIT = ['product', 'brand', 'narrative']
EMBEDDING_TEXT = 'A spring-led pop for CTA-sized elements, inspired by modern web motion libraries that use bounce and spring timing to feel tactile and friendly.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['gentle_rise_fade', 'bullet_stagger_reveal', 'cta_attention_pulse']
CONFLICTS_WITH = ['dramatic_zoom', 'glitch_shear_snap', 'chromatic_stutter']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_bounce_in, emit_grow_from_small, emit_pulse
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    t = p.get('duration_ms', 420)
    s = p.get('scale_from', 55) / 100.0
    pp = p.get('pulse_pct', 108)
    emit_grow_from_small(slide, target_shape, d, int(t * 0.72), scale_from=s)
    emit_bounce_in(slide, target_shape, d, t)
    emit_pulse(slide, target_shape, d + int(t * 0.78), int(t * 0.32), scale_pct=pp, repeats=1)
