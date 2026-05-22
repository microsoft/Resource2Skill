"""page_turn_drop — Fly-in from right + fade — evokes a page turning in a storybook or editorial..

Fly-in from right + fade — evokes a page turning in a storybook or editorial. Right-to-left fly-in coupled with a fade — the animated equi

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'page_turn_drop'
CATEGORY = 'entrance'
DESCRIPTION = 'Fly-in from right + fade — evokes a page turning in a storybook or editorial. Right-to-left fly-in coupled with a fade — the animated equi'

APPLICABILITY = {'roles': ['cover', 'section_divider', 'hero_quote', 'bullet_card_list'], 'anchor_names': ['headline', 'chapter_label', 'quote', 'subhead', 'hero_headline'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['page-turn', 'narrative', 'warm', 'storybook', 'editorial']
INTENSITY = 4
MOOD = ['warm', 'editorial', 'calm']
ARCHETYPE_FIT = ['narrative', 'research', 'brand']

EMBEDDING_TEXT = (
    "Right-to-left fly-in coupled with a fade — the animated equivalent of turning a page in a printed magazine. Signature for warm-narrative and children's books themes."
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['thesis_mark_breath', 'editorial_ink_bleed']
CONFLICTS_WITH = ['glitch_shear_snap', 'chromatic_stutter']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fade_in, emit_fly_in
    d = int(p.get('delay_ms',100))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=700)
    emit_fly_in(slide, target_shape, direction='right', delay_ms=d, duration_ms=800)
