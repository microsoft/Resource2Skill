"""margin_note_drop — Short fly-in from top with fade, restrained enough for footnote-like captions..

Short fly-in from top with fade, restrained enough for footnote-like captions. A modest fly-in-from-top for footnote captions. Quiet, late,

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'margin_note_drop'
CATEGORY = 'entrance'
DESCRIPTION = 'Short fly-in from top with fade, restrained enough for footnote-like captions. A modest fly-in-from-top for footnote captions. Quiet, late,'

APPLICABILITY = {'roles': ['section_divider', 'bullet_card_list', 'metric_dashboard', 'agenda'], 'anchor_names': ['footnote', 'caption', 'margin_note', 'source', 'citation'], 'anchor_name_regex': '(footnote|caption|citation|source|margin)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['margin-note', 'research', 'restrained', 'caption', 'editorial']
INTENSITY = 2
MOOD = ['research', 'restrained', 'editorial', 'calm']
ARCHETYPE_FIT = ['research', 'narrative']

EMBEDDING_TEXT = (
    "A modest fly-in-from-top for footnote captions. Quiet, late, deferent — the motion equivalent of a research paper's marginal annotation."
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['row_cascade_settle', 'editorial_ink_bleed']
CONFLICTS_WITH = ['glitch_shear_snap']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fly_in, emit_fade_in
    d = int(p.get('delay_ms',240))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=550)
    emit_fly_in(slide, target_shape, direction='top', delay_ms=d, duration_ms=600)
