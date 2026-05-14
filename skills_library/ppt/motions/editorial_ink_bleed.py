"""editorial_ink_bleed — Soft wipe from center with extra fade, like ink bleeding onto paper..

Soft wipe from center with extra fade, like ink bleeding onto paper. Gentle center-out wipe with a long fade tail. Reads like ink

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'editorial_ink_bleed'
CATEGORY = 'entrance'
DESCRIPTION = 'Soft wipe from center with extra fade, like ink bleeding onto paper. Gentle center-out wipe with a long fade tail. Reads like ink'

APPLICABILITY = {'roles': ['section_divider', 'hero_quote', 'cover', 'editorial_quote'], 'anchor_names': ['headline', 'section_label', 'quote', 'chapter_label'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['editorial', 'ink-bleed', 'soft', 'paper', 'calm']
INTENSITY = 3
MOOD = ['editorial', 'calm', 'warm']
ARCHETYPE_FIT = ['narrative', 'research', 'brand']

EMBEDDING_TEXT = (
    'Gentle center-out wipe with a long fade tail. Reads like ink expanding into thirsty paper. Pair with editorial serif themes for calm chapter opens.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['soft_arc_settle', 'cinematic_veil_reveal']
CONFLICTS_WITH = ['dramatic_zoom', 'bounce_in', 'rotate_in']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_wipe_in, emit_fade_in
    d = int(p.get('delay_ms',0))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=int(p.get('fade_ms',800)))
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=d+40, duration_ms=int(p.get('wipe_ms',900)))
