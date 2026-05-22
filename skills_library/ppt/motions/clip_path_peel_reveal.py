"""Clip-Path Peel Reveal — A page-peel style transition combining edge wipe and slight rotation for editorial image or card swaps.

Distilled from CSS-Tricks — Animating with Clip-Path
Source: https://css-tricks.com/animating-with-clip-path/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://css-tricks.com/animating-with-clip-path/'
SOURCE_TITLE = 'CSS-Tricks — Animating with Clip-Path'

NAME = 'clip_path_peel_reveal'
CATEGORY = 'transition'
DESCRIPTION = 'A page-peel style transition combining edge wipe and slight rotation for editorial image or card swaps.'
APPLICABILITY = {'roles': ['image change', 'card swap', 'section opener', 'editorial transition'], 'anchor_names': ['photo', 'hero_image', 'cards', 'quote', 'section_label'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 620, 'min': 220, 'max': 1600}, 'from_deg': {'type': 'int', 'default': -8, 'min': -20, 'max': 0}}

TAGS = ['peel', 'page-turn', 'wipe', 'editorial', 'reveal']
INTENSITY = 6
MOOD = ['editorial', 'playful', 'warm']
ARCHETYPE_FIT = ['brand', 'narrative', 'research']
EMBEDDING_TEXT = 'Inspired by clip-path reveal demos that mimic peeling and turning surfaces. In slides, it gives photos and cards a tactile editorial transition without requiring true 3D deformation.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['editorial_ink_bleed', 'headline_word_cascade', 'margin_note_drop']
CONFLICTS_WITH = ['curtain_dissolve_reveal', 'flip_card_resolve', 'cinematic_veil_reveal']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_rotate_in, emit_wipe_in
    p = dict(params or {})
    d = p.get('delay_ms', 0)
    dur = p.get('duration_ms', 620)
    fd = p.get('from_deg', -8)
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=d, duration_ms=dur)
    emit_rotate_in(slide, target_shape, delay_ms=d, duration_ms=max(180, int(dur * 0.85)), from_deg=fd)
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=max(180, int(dur * 0.7)))
