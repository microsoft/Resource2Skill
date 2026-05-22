"""Flip Card Resolve — A card-like entrance that rotates and settles in, echoing familiar web flip transitions.

Distilled from CSS-Tricks Perspective
Source: https://css-tricks.com/how-css-perspective-works/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://css-tricks.com/how-css-perspective-works/'
SOURCE_TITLE = 'CSS-Tricks Perspective'

NAME = 'flip_card_resolve'
CATEGORY = 'transition'
DESCRIPTION = 'A card-like entrance that rotates and settles in, echoing familiar web flip transitions.'
APPLICABILITY = {'roles': ['card swap', 'detail reveal', 'before-after switch'], 'anchor_names': ['cards', 'photo', 'hero_image', 'badge', 'chip'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 520, 'min': 180, 'max': 1800}, 'from_deg': {'type': 'int', 'default': -12, 'min': -30, 'max': 30}}

TAGS = ['flip', 'card', 'rotate', 'resolve', 'transition']
INTENSITY = 6
MOOD = ['playful', 'technical', 'bold']
ARCHETYPE_FIT = ['product', 'brand', 'research']
EMBEDDING_TEXT = 'Best for replacing one card or panel with another when you want a tactile, UI-like handoff. The rotation suggests a flip without needing true 3D geometry.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['card_rise_settle', 'glass_crossfade_settle', 'badge_pinwheel_pop']
CONFLICTS_WITH = ['page_hinge_drop', 'hinge_pivot_reveal', 'counter_rotate_cog']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_grow_emphasis, emit_rotate_in
    p = dict(params or {})
    d = int(p.get('duration_ms', 520))
    delay = int(p.get('delay_ms', 0))
    ang = int(p.get('from_deg', -12))
    emit_rotate_in(slide, target_shape, delay_ms=delay, duration_ms=d, from_deg=ang)
    emit_fade_in(slide, target_shape, delay_ms=delay, duration_ms=max(200, d - 120))
    emit_grow_emphasis(slide, target_shape, delay_ms=delay + d - 120, duration_ms=120, scale_pct=104)
