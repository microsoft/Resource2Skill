"""pulse_emphasis — single-shot attention pulse.

For anchors that are already visible and need a moment-of-emphasis
later in the slide's lifetime (e.g. a CTA button, a warning icon,
a status chip). Single pulse to 112% and back over 600ms.
"""
from __future__ import annotations

NAME = "pulse_emphasis"
CATEGORY = "emphasis"
DESCRIPTION = (
    "Single 600ms pulse to 112% and back. Draws attention to an "
    "already-visible element without re-entrance cost."
)
APPLICABILITY = {
    "roles": ["closing_cta", "kpi_card", "hero_giant_metric",
              "bullet_card_list"],
    "anchor_names": ["cta", "button", "chip", "badge", "warning", "status"],
    "max_per_slide": 2,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 1800, "min": 500, "max": 6000},
    "duration_ms": {"type": "int", "default": 600,  "min": 300, "max": 1500},
    "scale_pct":   {"type": "int", "default": 112,  "min": 104, "max": 135},
    "repeats":     {"type": "int", "default": 1,    "min": 1,   "max": 3},
}


MOOD = ['punchy', 'bold', 'editorial']
ARCHETYPE_FIT = ['product', 'brand', 'data', 'boardroom']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_pulse
    p = dict(params or {})
    emit_pulse(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 1800)),
        duration_ms=int(p.get("duration_ms", 600)),
        scale_pct=int(p.get("scale_pct", 112)),
        repeats=int(p.get("repeats", 1)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['emphasis', 'attention-grab', 'delayed-pulse', 'cta-emphasis']
INTENSITY = 6
EMBEDDING_TEXT = (
    'Single 600ms pulse to 112% and back, fired ~1.8s after slide load. Draws attention to an already-visible element without re-entrance cost. Great on CTA buttons, status chips, KPIs that need a beat of emphasis after the slide settles.'
)
CONTENT_MATCHERS = {'is_headline': False, 'max_chars': 60}
COMPLEMENTARY_WITH = ['count_up_metric', 'bounce_in']
CONFLICTS_WITH = []
