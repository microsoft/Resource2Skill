"""tag_pill_arrive — Small scale grow + fade — a badge/pill arriving. Faster than bounce, quieter than zoom..

Small scale grow + fade — a badge/pill arriving. Faster than bounce, quieter than zoom. An 80%->100% grow with a 400ms fade — a clean pill/badge arr

Category: entrance. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'tag_pill_arrive'
CATEGORY = 'entrance'
DESCRIPTION = 'Small scale grow + fade — a badge/pill arriving. Faster than bounce, quieter than zoom. An 80%->100% grow with a 400ms fade — a clean pill/badge arr'

APPLICABILITY = {'roles': ['cover', 'closing_cta', 'feature_grid', 'hero_giant_metric'], 'anchor_names': ['badge', 'chip', 'pill', 'tag', 'label', 'accent'], 'max_per_slide': 3}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['pill', 'badge', 'arrival', 'brand', 'product']
INTENSITY = 4
MOOD = ['bold', 'punchy', 'editorial']
ARCHETYPE_FIT = ['product', 'brand']

EMBEDDING_TEXT = (
    'An 80%->100% grow with a 400ms fade — a clean pill/badge arrival with no overshoot. Works across almost any theme that has badges or tags.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['cta_arrow_glide', 'neon_outline_trace']
CONFLICTS_WITH = ['typewriter_clack_reveal']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_grow_from_small, emit_fade_in
    d = int(p.get('delay_ms',150))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=400)
    emit_grow_from_small(slide, target_shape, delay_ms=d, duration_ms=500, from_pct=80)
