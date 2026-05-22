"""Signal Glitch Burst — A fast, corrupted-looking reveal that snaps a shape into view with brief rotational and scale interference.

Distilled from CSS-Tricks Glitch Effect on Text / Images / SVG
Source: https://css-tricks.com/glitch-effect-text-images-svg/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://css-tricks.com/glitch-effect-text-images-svg/'
SOURCE_TITLE = 'CSS-Tricks Glitch Effect on Text / Images / SVG'

NAME = 'signal_glitch_burst'
CATEGORY = 'composite'
DESCRIPTION = 'A fast, corrupted-looking reveal that snaps a shape into view with brief rotational and scale interference.'
APPLICABILITY = {'roles': ['title', 'section divider', 'hero stat callout'], 'anchor_names': ['headline', 'title', 'hero_headline', 'metric_xl', 'badge', 'icon'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 320, 'min': 180, 'max': 900}}

TAGS = ['glitch', 'signal', 'cyber', 'snap', 'interference']
INTENSITY = 7
MOOD = ['technical', 'bold', 'punchy']
ARCHETYPE_FIT = ['data', 'product', 'research']
EMBEDDING_TEXT = 'Best for security, infra, or debugging slides where a title or metric should feel electronically unstable for a split second before locking in.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['axis_line_draw', 'metric_snap_focus', 'lab_blink_flash']
CONFLICTS_WITH = ['chromatic_stutter', 'glitch_shear_snap', 'headline_prism_stagger']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_pulse, emit_rotate_in
    p = dict(params or {})
    d = int(p.get('delay_ms', 0))
    dur = int(p.get('duration_ms', 320))
    emit_fade_in(slide, target_shape, d, int(dur * 0.35))
    emit_rotate_in(slide, target_shape, d, int(dur * 0.45), from_deg=-8)
    emit_pulse(slide, target_shape, d + int(dur * 0.55), int(dur * 0.18), scale_pct=104, repeats=2)
