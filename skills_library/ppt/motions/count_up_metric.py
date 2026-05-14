"""count_up_metric — draw attention to a single hero number.

Best for: slides whose primary anchor is a large headline number
(e.g. hero_giant_metric). The number shape fades in, grows slightly
past 100%, then settles. Total visual effect is "the number
arrives with authority".

Applies to:
  - slide_role ∈ {hero_giant_metric, kpi_card, feature_stat}
  - anchor_name ∈ {hero_number, big_number, metric_value}
"""
from __future__ import annotations

NAME = "count_up_metric"
CATEGORY = "emphasis"
DESCRIPTION = (
    "Hero number arrives: fade-in over 600ms, then a 400ms grow-pulse "
    "to 115% and back so the eye anchors on the number."
)
APPLICABILITY = {
    "roles": ["hero_giant_metric", "kpi_card", "feature_stat"],
    "anchor_names": ["hero_number", "big_number", "metric_value"],
    "content_hints": ["digit", "%", "$", "x", "K", "M", "B"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 200, "min": 0, "max": 4000},
    "fade_ms":     {"type": "int", "default": 600, "min": 200, "max": 2000},
    "pulse_ms":    {"type": "int", "default": 500, "min": 200, "max": 1500},
    "pulse_scale": {"type": "int", "default": 115, "min": 105, "max": 140},
}


MOOD = ['boardroom', 'punchy', 'technical', 'bold']
ARCHETYPE_FIT = ['data', 'boardroom']

def apply(slide, target_shape, params=None):
    """Apply the count-up emphasis to target_shape on slide."""
    from _motion_helpers import emit_fade_in, emit_pulse
    p = dict(params or {})
    delay = int(p.get("delay_ms", 200))
    fade  = int(p.get("fade_ms", 600))
    pulse_dur   = int(p.get("pulse_ms", 500))
    pulse_scale = int(p.get("pulse_scale", 115))
    emit_fade_in(slide, target_shape, delay_ms=delay, duration_ms=fade)
    emit_pulse(
        slide, target_shape,
        delay_ms=delay + fade,
        duration_ms=pulse_dur,
        scale_pct=pulse_scale,
        repeats=1,
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['metric-focus', 'hero-number', 'digits', 'emphasis-composite']
INTENSITY = 8
EMBEDDING_TEXT = (
    "Composite hero-number arrival: 600ms fade-in then a 400ms 115% pulse. The eye locks on the digit. For '142', '99%', '$4.2B', KPI cards. Target must be a text frame containing digits or a unit symbol."
)
CONTENT_MATCHERS = {'digits': True, 'is_headline': False, 'max_chars': 20}
COMPLEMENTARY_WITH = ['breathing_halo', 'pulse_emphasis']
CONFLICTS_WITH = ['dramatic_zoom', 'bounce_in']
