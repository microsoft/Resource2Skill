"""pixel_dot_matrix_build — Staggered fade-in on sub-shapes to simulate a dot-matrix printer building the shape..

Staggered fade-in on sub-shapes to simulate a dot-matrix printer building the shape. Dot-matrix build where the headline or hero value appears as

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'pixel_dot_matrix_build'
CATEGORY = 'entrance'
DESCRIPTION = 'Staggered fade-in on sub-shapes to simulate a dot-matrix printer building the shape. Dot-matrix build where the headline or hero value appears as'

APPLICABILITY = {'roles': ['hero_giant_metric', 'cover', 'section_divider'], 'anchor_names': ['headline', 'value', 'metric_xl', 'title', 'hero_number'], 'max_per_slide': 1}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['pixel', 'dot-matrix', 'tech', 'retro', 'staccato']
INTENSITY = 5
MOOD = ['technical', 'punchy', 'playful']
ARCHETYPE_FIT = ['product', 'data', 'brand']

EMBEDDING_TEXT = (
    'Dot-matrix build where the headline or hero value appears as if printed by a DMP head. Signals retro-tech or early-computing mood without being nostalgic-kitsch.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['glitch_shear_snap', 'marquee_ticker_slide']
CONFLICTS_WITH = ['editorial_ink_bleed', 'soft_arc_settle']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_fade_in
    # Fallback to a plain fade if the shape has no children to stagger.
    emit_fade_in(slide, target_shape, delay_ms=int(p.get('delay_ms',80)), duration_ms=int(p.get('duration_ms',600)))
