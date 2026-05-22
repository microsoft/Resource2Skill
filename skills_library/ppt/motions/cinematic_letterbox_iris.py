"""cinematic_letterbox_iris — Long zoom-in from 85% combined with a fade, mimicking a cinematic iris open..

Long zoom-in from 85% combined with a fade, mimicking a cinematic iris open. Cinematic iris open: a gentle 85%->100% zoom over 1.1s timed

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'cinematic_letterbox_iris'
CATEGORY = 'entrance'
DESCRIPTION = 'Long zoom-in from 85% combined with a fade, mimicking a cinematic iris open. Cinematic iris open: a gentle 85%->100% zoom over 1.1s timed'

APPLICABILITY = {'roles': ['cover', 'hero_quote', 'hero_giant_metric', 'section_divider'], 'anchor_names': ['headline', 'hero_headline', 'quote', 'value', 'metric_xl'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['cinematic', 'iris', 'letterbox', 'premium', 'brand']
INTENSITY = 5
MOOD = ['cinematic', 'editorial', 'bold']
ARCHETYPE_FIT = ['brand', 'narrative']

EMBEDDING_TEXT = (
    'Cinematic iris open: a gentle 85%->100% zoom over 1.1s timed with a 900ms fade. Best as the FIRST frame of a deck or the opening of a new chapter in brand/cinematic themes.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['cinematic_veil_reveal', 'soft_arc_settle']
CONFLICTS_WITH = ['glitch_shear_snap', 'typewriter_clack_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fade_in, emit_grow_from_small
    d = int(p.get('delay_ms',100))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=int(p.get('fade_ms',900)))
    emit_grow_from_small(slide, target_shape, delay_ms=d, duration_ms=int(p.get('grow_ms',1100)), from_pct=int(p.get('from_pct',85)))
