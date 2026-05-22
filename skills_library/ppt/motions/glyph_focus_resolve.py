"""Glyph Focus Resolve — Letters resolve one by one with a subtle zoomed clarity, giving headlines a precise, technical reading rhythm.

Distilled from web.dev Split Text Animations
Source: https://web.dev/articles/building/split-text-animations
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://web.dev/articles/building/split-text-animations'
SOURCE_TITLE = 'web.dev Split Text Animations'

NAME = 'glyph_focus_resolve'
CATEGORY = 'text'
DESCRIPTION = 'Letters resolve one by one with a subtle zoomed clarity, giving headlines a precise, technical reading rhythm.'
APPLICABILITY = {'roles': ['headline', 'title', 'section_label', 'metric_xl'], 'anchor_names': ['headline', 'title', 'section_label', 'metric_xl', 'label'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'stagger_ms': {'type': 'int', 'default': 32, 'min': 10, 'max': 100}, 'per_duration_ms': {'type': 'int', 'default': 140, 'min': 60, 'max': 260}, 'zoom_duration_ms': {'type': 'int', 'default': 420, 'min': 180, 'max': 900}}

TAGS = ['letter-by-letter', 'split-text', 'technical', 'resolve', 'headline']
INTENSITY = 4
MOOD = ['technical', 'research', 'restrained']
ARCHETYPE_FIT = ['research', 'data', 'product']
EMBEDDING_TEXT = 'Drawn from split-text techniques on web.dev, this motion treats each glyph as a small unit of focus. Use it for precise titles, section labels, and analytical callouts.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['axis_line_draw', 'column_rule_draw', 'metric_snap_focus']
CONFLICTS_WITH = ['headline_prism_stagger', 'chromatic_stutter', 'neon_outline_trace']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_text_stagger, emit_zoom_in
    p = dict(params or {})
    emit_zoom_in(slide, target_shape, delay_ms=p.get('delay_ms', 0), duration_ms=p.get('zoom_duration_ms', 420))
    emit_text_stagger(slide, target_shape, delay_ms=p.get('delay_ms', 0), stagger_ms=p.get('stagger_ms', 32), per_duration_ms=p.get('per_duration_ms', 140))
