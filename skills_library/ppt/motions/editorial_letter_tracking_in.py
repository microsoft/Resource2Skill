"""Editorial Letter Tracking In — Letters appear sequentially with a subtle settle, echoing kinetic typography intros.

Distilled from Animista tracking-in-expand
Source: https://animista.net/play/text/tracking-in/tracking-in-expand
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://animista.net/play/text/tracking-in/tracking-in-expand'
SOURCE_TITLE = 'Animista tracking-in-expand'

NAME = 'editorial_letter_tracking_in'
CATEGORY = 'text'
DESCRIPTION = 'Letters appear sequentially with a subtle settle, echoing kinetic typography intros.'
APPLICABILITY = {'roles': ['title', 'section opener', 'pull quote'], 'anchor_names': ['headline', 'title', 'title_xl', 'kicker', 'eyebrow', 'section_label', 'section_number'], 'max_per_slide': 1}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'stagger_ms': {'type': 'int', 'default': 34, 'min': 10, 'max': 120}, 'per_duration_ms': {'type': 'int', 'default': 220, 'min': 100, 'max': 700}, 'settle_pct': {'type': 'int', 'default': 104, 'min': 101, 'max': 115}}

TAGS = ['text', 'letters', 'tracking', 'kinetic-type', 'editorial']
INTENSITY = 4
MOOD = ['editorial', 'cinematic', 'restrained']
ARCHETYPE_FIT = ['brand', 'narrative', 'research']
EMBEDDING_TEXT = 'A letter-driven editorial entrance that feels deliberate and typographic. Use it on short titles, section numbers, or sharply set pull quotes.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['cinematic_veil_reveal', 'hairline_snap_in', 'eyebrow_tick_in']
CONFLICTS_WITH = ['headline_letterpress_stagger', 'headline_restrike_focus', 'chromatic_stutter']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_grow_emphasis, emit_text_stagger
    p = dict(params or {})
    emit_text_stagger(slide, target_shape,
        delay_ms=p.get('delay_ms', 0),
        stagger_ms=p.get('stagger_ms', 34),
        per_duration_ms=p.get('per_duration_ms', 220))
    emit_grow_emphasis(slide, target_shape,
        delay_ms=p.get('delay_ms', 0) + p.get('stagger_ms', 34) * 6,
        duration_ms=180, scale_pct=p.get('settle_pct', 104))
