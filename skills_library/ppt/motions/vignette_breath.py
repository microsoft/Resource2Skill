"""vignette_breath — Very slow, subtle pulse — ambient frame around hero content..

Very slow, subtle pulse — ambient frame around hero content. A barely-there 103% breathing pulse on a vignette frame. Mea

Category: ambient. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'vignette_breath'
CATEGORY = 'ambient'
DESCRIPTION = 'Very slow, subtle pulse — ambient frame around hero content. A barely-there 103% breathing pulse on a vignette frame. Mea'

APPLICABILITY = {'roles': ['cover', 'hero_giant_metric', 'closing_cta', 'section_divider'], 'anchor_names': ['vignette', 'frame', 'border', 'bg_accent', 'ambient'], 'anchor_name_regex': '(vignette|frame|ambient|bg_accent)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['vignette', 'ambient', 'breath', 'calm', 'cinematic']
INTENSITY = 2
MOOD = ['cinematic', 'calm', 'editorial']
ARCHETYPE_FIT = ['brand', 'narrative', 'research']

EMBEDDING_TEXT = (
    'A barely-there 103% breathing pulse on a vignette frame. Meant to be ambient — not the focal motion of the slide. Pair with a bolder entrance motion on the hero content.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['cinematic_letterbox_iris']
CONFLICTS_WITH = ['glitch_shear_snap']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    emit_pulse(slide, target_shape, delay_ms=int(p.get('delay_ms',0)), duration_ms=int(p.get('duration_ms',2600)), scale_pct=103, repeats=3)
