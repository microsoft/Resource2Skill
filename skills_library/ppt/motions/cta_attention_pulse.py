"""CTA Attention Pulse — A restrained button pulse that briefly enlarges to draw focus without feeling noisy.

Distilled from Material 3 Motion Overview
Source: https://m3.material.io/styles/motion/overview
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://m3.material.io/styles/motion/overview'
SOURCE_TITLE = 'Material 3 Motion Overview'

NAME = 'cta_attention_pulse'
CATEGORY = 'emphasis'
DESCRIPTION = 'A restrained button pulse that briefly enlarges to draw focus without feeling noisy.'
APPLICABILITY = {'roles': ['cta', 'button', 'product highlight'], 'anchor_names': ['cta', 'button', 'badge', 'chip'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'duration_ms': {'type': 'int', 'default': 420, 'min': 180, 'max': 1200}, 'scale_pct': {'type': 'int', 'default': 110, 'min': 104, 'max': 118}}

TAGS = ['cta', 'pulse', 'attention', 'material', 'microinteraction']
INTENSITY = 5
MOOD = ['restrained', 'product', 'boardroom']
ARCHETYPE_FIT = ['product', 'boardroom', 'brand']
EMBEDDING_TEXT = 'Use on a primary CTA or key decision button when you want a subtle call-to-action emphasis. Best for product demos, pricing slides, and executive recommendation moments.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['gentle_rise_fade', 'hairline_snap_in', 'cta_arrow_glide']
CONFLICTS_WITH = ['confetti_burst', 'glitch_shear_snap', 'dramatic_zoom']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_grow_emphasis
    p = dict(params or {})
    emit_grow_emphasis(slide, target_shape, p.get('delay_ms', 0), p.get('duration_ms', 420), scale_pct=p.get('scale_pct', 110))
