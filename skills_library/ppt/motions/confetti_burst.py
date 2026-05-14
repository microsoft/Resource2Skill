"""confetti_burst — Staggered fade-in on the same shape with slight position drift via motion path..

Staggered fade-in on the same shape with slight position drift via motion path. Short 3%-height drift paired with a 600ms fade — reads like 

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'confetti_burst'
CATEGORY = 'entrance'
DESCRIPTION = 'Staggered fade-in on the same shape with slight position drift via motion path. Short 3%-height drift paired with a 600ms fade — reads like '

APPLICABILITY = {'roles': ['closing_cta', 'cover', 'hero_giant_metric'], 'anchor_names': ['badge', 'accent', 'accent_orb', 'icon', 'seal'], 'max_per_slide': 2}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['confetti', 'burst', 'playful', 'warm', 'celebration']
INTENSITY = 6
MOOD = ['playful', 'warm', 'punchy']
ARCHETYPE_FIT = ['brand', 'product', 'narrative']

EMBEDDING_TEXT = (
    'Short 3%-height drift paired with a 600ms fade — reads like a small confetti particle fluttering into place. Works well on festive cover shots.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['bubble_pop_reveal', 'balloon_bob']
CONFLICTS_WITH = ['editorial_ink_bleed', 'cinematic_letterbox_iris']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fade_in, emit_motion_path
    d = int(p.get('delay_ms',200))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=600)
    emit_motion_path(slide, target_shape, svg_path='M 0 0.03 L 0 0', delay_ms=d, duration_ms=700)
