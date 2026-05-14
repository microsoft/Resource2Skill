"""Corner Push Reveal — A diagonal-feeling push entrance that combines wipe and lateral movement for directional slide changes.

Distilled from Apple HIG Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://developer.apple.com/design/human-interface-guidelines/motion'
SOURCE_TITLE = 'Apple HIG Motion'

NAME = 'corner_push_reveal'
CATEGORY = 'transition'
DESCRIPTION = 'A diagonal-feeling push entrance that combines wipe and lateral movement for directional slide changes.'
APPLICABILITY = {'roles': ['slide change', 'section handoff', 'panel replacement'], 'anchor_names': ['photo', 'hero_image', 'title', 'headline', 'cards'], 'max_per_slide': 3}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 2000}, 'duration_ms': {'type': 'int', 'default': 460, 'min': 160, 'max': 1600}}

TAGS = ['push', 'corner', 'wipe', 'handoff', 'directional']
INTENSITY = 4
MOOD = ['restrained', 'editorial', 'technical']
ARCHETYPE_FIT = ['boardroom', 'product', 'narrative']
EMBEDDING_TEXT = 'Use this to suggest content being pushed in from an off-corner, especially for full-bleed images or replacing panels. It feels cleaner than a hard slide and more directed than a plain fade.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['lateral_handoff_crossfade', 'editorial_side_nudge', 'panel_unveil_settle']
CONFLICTS_WITH = ['cinematic_lateral_reveal', 'panel_shutter_unfold', 'page_turn_drop']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_fade_in, emit_fly_in, emit_wipe_in
    p = dict(params or {})
    d = int(p.get('duration_ms', 460))
    delay = int(p.get('delay_ms', 0))
    emit_wipe_in(slide, target_shape, direction='left', delay_ms=delay, duration_ms=d)
    emit_fly_in(slide, target_shape, direction='bottom', delay_ms=delay, duration_ms=max(220, d - 40))
    emit_fade_in(slide, target_shape, delay_ms=delay, duration_ms=max(180, d - 120))
