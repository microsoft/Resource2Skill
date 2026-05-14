"""thesis_mark_breath — Slow breathing pulse — loops 3x — on a thesis statement or key insight..

Slow breathing pulse — loops 3x — on a thesis statement or key insight. A slow 104% breathing pulse repeating twice over ~2.2s total

Category: emphasis. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'thesis_mark_breath'
CATEGORY = 'emphasis'
DESCRIPTION = 'Slow breathing pulse — loops 3x — on a thesis statement or key insight. A slow 104% breathing pulse repeating twice over ~2.2s total'

APPLICABILITY = {'roles': ['hero_quote', 'section_divider', 'cover', 'hero_statement'], 'anchor_names': ['headline', 'quote', 'tagline', 'thesis'], 'anchor_name_regex': '(headline|quote|tagline|thesis|subhead)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['thesis', 'breath', 'research', 'editorial', 'calm']
INTENSITY = 3
MOOD = ['research', 'calm', 'editorial', 'restrained']
ARCHETYPE_FIT = ['research', 'narrative']

EMBEDDING_TEXT = (
    'A slow 104% breathing pulse repeating twice over ~2.2s total — reads as a thesis catching its breath. Use on research quotes and thesis statements in calm/editorial themes.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['margin_note_drop', 'editorial_ink_bleed']
CONFLICTS_WITH = ['glitch_shear_snap', 'bubble_pop_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    emit_pulse(slide, target_shape, delay_ms=int(p.get('delay_ms',1200)), duration_ms=int(p.get('duration_ms',1100)), scale_pct=104, repeats=2)
