"""polaroid_drop_tilt — Fly-in from top with rotate, like a Polaroid landing slightly askew..

Fly-in from top with rotate, like a Polaroid landing slightly askew. Fly-in from top + small rotate in — reads as a Polaroid snap

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'polaroid_drop_tilt'
CATEGORY = 'entrance'
DESCRIPTION = 'Fly-in from top with rotate, like a Polaroid landing slightly askew. Fly-in from top + small rotate in — reads as a Polaroid snap'

APPLICABILITY = {'roles': ['cover', 'feature_grid', 'hero_quote', 'closing_cta'], 'anchor_names': ['hero_image', 'photo', 'polaroid', 'card', 'accent'], 'max_per_slide': 2}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['polaroid', 'drop', 'tilt', 'playful', 'warm', 'narrative']
INTENSITY = 6
MOOD = ['playful', 'warm', 'cinematic']
ARCHETYPE_FIT = ['brand', 'narrative', 'product']

EMBEDDING_TEXT = (
    'Fly-in from top + small rotate in — reads as a Polaroid snapshot dropping and settling tilted. Perfect for moodboards, feature grids, and warm brand decks.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['confetti_burst', 'bubble_pop_reveal']
CONFLICTS_WITH = ['hairline_snap_in', 'row_cascade_settle']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fly_in, emit_fade_in, emit_rotate_in
    d = int(p.get('delay_ms',120))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=700)
    emit_fly_in(slide, target_shape, direction='top', delay_ms=d, duration_ms=750)
    emit_rotate_in(slide, target_shape, delay_ms=d, duration_ms=700)
