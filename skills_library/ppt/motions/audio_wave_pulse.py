"""audio_wave_pulse — Breathing pulse scaled at 108% looped 4x — a waveform or audio envelope pulsing..

Breathing pulse scaled at 108% looped 4x — a waveform or audio envelope pulsing. A 108% scale pulse repeating 4 times at 700ms — reads as an 

Category: ambient. Auto-authored by scripts/distill_more_motions.py on 2026-04-19.
"""
from __future__ import annotations

NAME = 'audio_wave_pulse'
CATEGORY = 'ambient'
DESCRIPTION = 'Breathing pulse scaled at 108% looped 4x — a waveform or audio envelope pulsing. A 108% scale pulse repeating 4 times at 700ms — reads as an '

APPLICABILITY = {'roles': ['hero_giant_metric', 'cover', 'section_divider'], 'anchor_names': ['wave', 'audio', 'equalizer', 'pulse_bar', 'sonic'], 'anchor_name_regex': '(wave|audio|equalizer|sonic|pulse_bar)'}

PARAMETERS = {
    "delay_ms":     {"type": "int", "default": 100, "min": 0,   "max": 6000},
    "duration_ms":  {"type": "int", "default": 700, "min": 200, "max": 4000},
}

TAGS = ['audio-wave', 'pulse', 'media', 'music', 'brand']
INTENSITY = 5
MOOD = ['cinematic', 'playful', 'bold', 'punchy']
ARCHETYPE_FIT = ['product', 'brand']

EMBEDDING_TEXT = (
    'A 108% scale pulse repeating 4 times at 700ms — reads as an audio waveform breathing. Perfect for music-tech and podcast product decks.'
)
CONTENT_MATCHERS = {"is_headline": False}
COMPLEMENTARY_WITH = ['neon_outline_trace', 'chromatic_stutter']
CONFLICTS_WITH = ['hairline_snap_in', 'editorial_ink_bleed']


def apply(slide, target_shape, params=None):
    p = dict(params or {})
    from _motion_helpers import emit_pulse
    emit_pulse(slide, target_shape, delay_ms=int(p.get('delay_ms',200)), duration_ms=int(p.get('duration_ms',700)), scale_pct=108, repeats=4)
