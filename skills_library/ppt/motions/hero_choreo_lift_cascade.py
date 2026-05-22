"""Hero Choreography Lift Cascade — Kicker wipes, headline lifts, subtitle fades, and supporting cards rise in a measured cascade.

Distilled from Material 3 Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material 3 Motion Overview'

NAME = 'hero_choreo_lift_cascade'
CATEGORY = 'composite'
DESCRIPTION = 'Kicker wipes, headline lifts, subtitle fades, and supporting cards rise in a measured cascade.'
APPLICABILITY = {'roles': ['hero', 'section opener', 'feature intro', 'agenda'], 'anchor_names': ['eyebrow', 'kicker', 'headline', 'title', 'title_xl', 'subtitle', 'cards', 'cta'], 'max_per_slide': 1}
PARAMETERS = {'base_delay': {'type': 'int', 'default': 0, 'min': 0, 'max': 1200}}

TAGS = ['choreography', 'cascade', 'hero', 'stagger', 'cards']
INTENSITY = 5
MOOD = ['restrained', 'boardroom', 'technical']
ARCHETYPE_FIT = ['product', 'boardroom', 'brand']
EMBEDDING_TEXT = 'Use across a hero stack so small framing text starts the sequence, the main title lifts into focus, and cards or CTA land last.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['hairline_snap_in', 'cta_arrow_glide', 'glass_crossfade_settle']
CONFLICTS_WITH = ['dramatic_zoom', 'glitch_shear_snap', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_grow_emphasis, emit_wipe_in
    p = dict(params or {})
    n = getattr(target_shape, 'name', '').lower(); d = int(p.get('base_delay', 0))
    if any(k in n for k in ('eyebrow', 'kicker', 'section_label')): emit_wipe_in(slide, target_shape, direction='left', delay_ms=d, duration_ms=260)
    elif any(k in n for k in ('headline', 'title', 'hero_headline', 'title_xl')): emit_fly_in(slide, target_shape, direction='bottom', delay_ms=d+120, duration_ms=420); emit_fade_in(slide, target_shape, delay_ms=d+120, duration_ms=320)
    elif any(k in n for k in ('subtitle', 'quote', 'label')): emit_fade_in(slide, target_shape, delay_ms=d+260, duration_ms=300)
    else: emit_fly_in(slide, target_shape, direction='bottom', delay_ms=d+340, duration_ms=360); emit_grow_emphasis(slide, target_shape, delay_ms=d+720, duration_ms=180, scale_pct=104)
