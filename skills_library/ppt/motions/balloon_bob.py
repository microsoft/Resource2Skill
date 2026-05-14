"""balloon_bob — Small scale pulse that loops gently — reads as a balloon bobbing..

Small scale pulse that loops gently — reads as a balloon bobbing. Gentle 106% scale pulse repeating 3 times over 900ms each — 

Category: emphasis. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'balloon_bob'
CATEGORY = 'emphasis'
DESCRIPTION = 'Small scale pulse that loops gently — reads as a balloon bobbing. Gentle 106% scale pulse repeating 3 times over 900ms each — '

APPLICABILITY = {'roles': ['cover', 'feature_grid', 'closing_cta', 'kpi_card'], 'anchor_names': ['accent', 'accent_orb', 'badge', 'icon', 'chip'], 'max_per_slide': 2}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['balloon', 'bob', 'playful', 'warm', 'kids']
INTENSITY = 4
MOOD = ['playful', 'warm', 'calm']
ARCHETYPE_FIT = ['brand', 'narrative']

EMBEDDING_TEXT = (
    'Gentle 106% scale pulse repeating 3 times over 900ms each — like a balloon bobbing in a breeze. Signature for kids-education and warm brand themes.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['breathing_halo']
CONFLICTS_WITH = ['glitch_shear_snap', 'cinematic_letterbox_iris']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    emit_pulse(slide, target_shape, delay_ms=int(p.get('delay_ms',500)), duration_ms=int(p.get('duration_ms',900)), scale_pct=int(p.get('scale_pct',106)), repeats=int(p.get('repeats',3)))
