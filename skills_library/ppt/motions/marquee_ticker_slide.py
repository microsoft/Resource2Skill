"""marquee_ticker_slide — Long horizontal motion path — a news-ticker marquee sliding in from the right..

Long horizontal motion path — a news-ticker marquee sliding in from the right. A short right-to-left translation of ~15% slide width paired

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'marquee_ticker_slide'
CATEGORY = 'entrance'
DESCRIPTION = 'Long horizontal motion path — a news-ticker marquee sliding in from the right. A short right-to-left translation of ~15% slide width paired'

APPLICABILITY = {'roles': ['cover', 'section_divider', 'bullet_card_list', 'timeline_horizontal'], 'anchor_names': ['headline', 'subhead', 'section_label', 'ticker'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['marquee', 'ticker', 'news', 'tech']
INTENSITY = 5
MOOD = ['technical', 'editorial', 'punchy']
ARCHETYPE_FIT = ['product', 'data']

EMBEDDING_TEXT = (
    'A short right-to-left translation of ~15% slide width paired with a 400ms fade. Reads as a ticker sliding into its resting position.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['pixel_dot_matrix_build']
CONFLICTS_WITH = ['breathing_halo']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_motion_path, emit_fade_in
    d = int(p.get('delay_ms',60))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=400)
    emit_motion_path(slide, target_shape, svg_path='M 0.15 0 L 0 0', delay_ms=d, duration_ms=int(p.get('duration_ms',900)))
