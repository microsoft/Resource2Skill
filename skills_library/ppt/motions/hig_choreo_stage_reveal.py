"""HIG Choreographed Stage Reveal — Eyebrow, headline, subtitle, and hero image enter in a calm hierarchy with a soft image settle.

Distilled from Apple Human Interface Guidelines — Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple Human Interface Guidelines — Motion'

NAME = 'hig_choreo_stage_reveal'
CATEGORY = 'composite'
DESCRIPTION = 'Eyebrow, headline, subtitle, and hero image enter in a calm hierarchy with a soft image settle.'
APPLICABILITY = {'roles': ['hero', 'section opener', 'product intro'], 'anchor_names': ['eyebrow', 'headline', 'subtitle', 'hero_image', 'cta'], 'max_per_slide': 1}
PARAMETERS = {'delay': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'step': {'type': 'int', 'default': 120, 'min': 40, 'max': 400}, 'duration': {'type': 'int', 'default': 420, 'min': 180, 'max': 1200}}

TAGS = ['hierarchy', 'staged', 'hero', 'reveal', 'apple-like']
INTENSITY = 4
MOOD = ['calm', 'restrained', 'cinematic']
ARCHETYPE_FIT = ['product', 'brand', 'narrative', 'boardroom']
EMBEDDING_TEXT = 'A layered Apple-style reveal: small context first, headline next, then supporting copy and image settling together. Best for premium product or keynote-style openers.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['glass_crossfade_settle', 'cta_attention_pulse', 'image_ken_burns']
CONFLICTS_WITH = ['dramatic_zoom', 'glitch_shear_snap', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_grow_from_small
    p = dict(params or {})
    d=p.get('delay',0); s=p.get('step',120); t=p.get('duration',420); x=target_shape
    emit_fade_in(slide, x.get('eyebrow', x), d, 180)
    emit_fly_in(slide, x.get('headline', x), direction='bottom', delay_ms=d+s, duration_ms=t)
    emit_fade_in(slide, x.get('subtitle', x), d+s*2, 220)
    emit_grow_from_small(slide, x.get('hero_image', x), d+s, t+120, scale_from=0.92)
    emit_fade_in(slide, x.get('cta', x), d+s*3, 180)
