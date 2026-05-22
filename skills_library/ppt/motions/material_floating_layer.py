"""Material Floating Layer — A supporting layer fades up and glides on a soft arc to imply depth without calling attention.

Distilled from Material 3 Motion overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material 3 Motion overview'

NAME = 'material_floating_layer'
CATEGORY = 'ambient'
DESCRIPTION = 'A supporting layer fades up and glides on a soft arc to imply depth without calling attention.'
APPLICABILITY = {'roles': ['supporting illustration', 'background card', 'section divider'], 'anchor_names': ['cards', 'photo', 'hero_image', 'icon'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 4000}, 'fade_ms': {'type': 'int', 'default': 450, 'min': 100, 'max': 1200}, 'duration_ms': {'type': 'int', 'default': 6000, 'min': 2000, 'max': 12000}}

TAGS = ['depth', 'float', 'arc', 'layer', 'ambient']
INTENSITY = 2
MOOD = ['calm', 'technical', 'boardroom']
ARCHETYPE_FIT = ['product', 'research', 'boardroom']
EMBEDDING_TEXT = 'Use this for secondary layers that should feel lightly suspended in space. The slow arc gives enough dimensionality for dividers, diagrams, and supporting imagery.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['material_choreo_card_cascade', 'glyph_focus_resolve', 'hairline_snap_in']
CONFLICTS_WITH = ['floating_card_drift', 'arc_balloon_arrival', 'bounce_in']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_arc_path, emit_fade_in
    p = dict(params or {})
    d = int(p.get('delay_ms', 0))
    fade = int(p.get('fade_ms', 450))
    dur = int(p.get('duration_ms', 6000))
    emit_fade_in(slide, target_shape, d, fade)
    emit_arc_path(slide, target_shape, d, dur)
