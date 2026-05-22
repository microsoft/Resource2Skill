"""bubble_pop_reveal — Grow-from-tiny with overshoot followed by a tiny bounce — a playful bubble pop..

Grow-from-tiny with overshoot followed by a tiny bounce — a playful bubble pop. Bubble-pop entrance — 20% to 120% to 100% in 750ms. Better t

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'bubble_pop_reveal'
CATEGORY = 'entrance'
DESCRIPTION = 'Grow-from-tiny with overshoot followed by a tiny bounce — a playful bubble pop. Bubble-pop entrance — 20% to 120% to 100% in 750ms. Better t'

APPLICABILITY = {'roles': ['closing_cta', 'feature_grid', 'cover', 'kpi_card'], 'anchor_names': ['badge', 'chip', 'cta', 'icon', 'seal'], 'max_per_slide': 3}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['bubble', 'pop', 'playful', 'warm', 'kids']
INTENSITY = 7
MOOD = ['playful', 'warm', 'punchy']
ARCHETYPE_FIT = ['brand', 'product', 'narrative']

EMBEDDING_TEXT = (
    "Bubble-pop entrance — 20% to 120% to 100% in 750ms. Better than a plain bounce because it adds a narrative 'popping' feel, perfect for children's and warm-brand decks."
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['balloon_bob']
CONFLICTS_WITH = ['editorial_ink_bleed', 'typewriter_clack_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_bounce_in
    emit_bounce_in(slide, target_shape, delay_ms=int(p.get('delay_ms',200)), duration_ms=int(p.get('duration_ms',750)))
