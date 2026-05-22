"""Arc Balloon Arrival — An object glides in on a soft curved path and settles with a buoyant, balloon-like feel.

Distilled from Material Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material Motion Overview'

NAME = 'arc_balloon_arrival'
CATEGORY = 'composite'
DESCRIPTION = 'An object glides in on a soft curved path and settles with a buoyant, balloon-like feel.'
APPLICABILITY = {'roles': ['hero reveal', 'illustration entrance', 'playful product intro'], 'anchor_names': ['photo', 'hero_image', 'icon', 'badge', 'cards'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 900, 'min': 400, 'max': 1800}, 'pulse_pct': {'type': 'int', 'default': 105, 'min': 102, 'max': 112}}

TAGS = ['arc', 'float', 'balloon', 'organic', 'arrival']
INTENSITY = 5
MOOD = ['playful', 'warm', 'calm']
ARCHETYPE_FIT = ['brand', 'product', 'narrative']
EMBEDDING_TEXT = 'A warm curved entrance for illustrations or hero objects, borrowing from Material’s emphasis on arcs and spatial continuity rather than rigid straight-line movement.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['headline_arc_settle', 'gentle_rise_fade', 'hero_arc_glide']
CONFLICTS_WITH = ['background_parallax_glide', 'dramatic_zoom', 'cinematic_lateral_reveal']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_arc_path, emit_fade_in, emit_pulse
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    t = p.get('duration_ms', 900)
    pp = p.get('pulse_pct', 105)
    emit_fade_in(slide, target_shape, d, int(t * 0.45))
    emit_arc_path(slide, target_shape, d, t)
    emit_pulse(slide, target_shape, d + int(t * 0.76), int(t * 0.24), scale_pct=pp, repeats=1)
