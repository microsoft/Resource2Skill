"""Section Divider Slow Pan — A background divider eases into view and drifts horizontally for understated parallax-like depth.

Distilled from web.dev Parallax performance
Source: https://web.dev/articles/speed-parallax
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://web.dev/articles/speed-parallax'
SOURCE_TITLE = 'web.dev Parallax performance'

NAME = 'section_divider_slow_pan'
CATEGORY = 'ambient'
DESCRIPTION = 'A background divider eases into view and drifts horizontally for understated parallax-like depth.'
APPLICABILITY = {'roles': ['section divider', 'background texture', 'chapter break'], 'anchor_names': ['photo', 'hero_image', 'section_label', 'section_number'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 4000}, 'fade_ms': {'type': 'int', 'default': 500, 'min': 100, 'max': 1500}, 'duration_ms': {'type': 'int', 'default': 9000, 'min': 3000, 'max': 20000}}

TAGS = ['parallax', 'drift', 'divider', 'background', 'slow']
INTENSITY = 2
MOOD = ['calm', 'restrained', 'editorial']
ARCHETYPE_FIT = ['narrative', 'brand', 'boardroom']
EMBEDDING_TEXT = 'Inspired by web parallax guidance, this creates a restrained divider drift rather than a full scrolling effect. Best for section bands, washes, or wide image crops.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['headline_mist_rise', 'kicker_tick_up', 'gentle_rise_fade']
CONFLICTS_WITH = ['background_parallax_glide', 'dramatic_zoom', 'confetti_burst']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_motion_path
    p = dict(params or {})
    d = int(p.get('delay_ms', 0))
    fade = int(p.get('fade_ms', 500))
    dur = int(p.get('duration_ms', 9000))
    emit_fade_in(slide, target_shape, d, fade)
    emit_motion_path(slide, target_shape, 'M0,0 C20,-6 40,6 64,0', d, dur)
