"""mist_drift_behind — Slow translation + fade — background mist drifting behind hero content..

Slow translation + fade — background mist drifting behind hero content. Long 4.2s linear drift of 4% slide-width for a background mi

Category: ambient. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'mist_drift_behind'
CATEGORY = 'ambient'
DESCRIPTION = 'Slow translation + fade — background mist drifting behind hero content. Long 4.2s linear drift of 4% slide-width for a background mi'

APPLICABILITY = {'roles': ['cover', 'hero_quote', 'section_divider'], 'anchor_names': ['mist', 'bg_mist', 'ambient', 'fog', 'accent_mist'], 'anchor_name_regex': '(mist|fog|ambient|bg_)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['mist', 'drift', 'ambient', 'calm', 'cinematic']
INTENSITY = 2
MOOD = ['cinematic', 'calm', 'editorial', 'warm']
ARCHETYPE_FIT = ['brand', 'narrative', 'research']

EMBEDDING_TEXT = (
    'Long 4.2s linear drift of 4% slide-width for a background mist layer. A tiny ambient motion that adds atmosphere without stealing focus from the foreground.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['vignette_breath']
CONFLICTS_WITH = ['glitch_shear_snap', 'chromatic_stutter']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_motion_path, emit_fade_in
    d = int(p.get('delay_ms',0))
    emit_fade_in(slide, target_shape, delay_ms=d, duration_ms=1200)
    emit_motion_path(slide, target_shape, svg_path='M 0 0 L 0.04 0.01', delay_ms=d, duration_ms=int(p.get('duration_ms',4200)))
