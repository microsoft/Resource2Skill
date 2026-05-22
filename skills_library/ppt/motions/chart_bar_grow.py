"""chart_bar_grow — bars grow from their baseline.

For chart anchors: each bar should appear to grow from its
baseline to full height, stagger across series. python-pptx
doesn't give us a clean per-bar animation anchor, so we apply
a wipe_in(direction="bottom") to the chart frame, which is
what PowerPoint does under the "Grow" chart animation preset.
"""
from __future__ import annotations

NAME = "chart_bar_grow"
CATEGORY = "entrance"
DESCRIPTION = (
    "Chart bars grow from their baseline via a bottom-up wipe. "
    "450ms duration, matches Apple Keynote 'Build from Bottom'."
)
APPLICABILITY = {
    "roles": ["metric_dashboard", "comparison_split"],
    "anchor_names": ["chart", "bar_chart", "metric_chart"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 400, "min": 0, "max": 4000},
    "duration_ms": {"type": "int", "default": 700, "min": 300, "max": 2000},
}


MOOD = ['editorial']
ARCHETYPE_FIT = ['data', 'boardroom']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_wipe_in
    p = dict(params or {})
    emit_wipe_in(
        slide, target_shape,
        direction="bottom",
        delay_ms=int(p.get("delay_ms", 400)),
        duration_ms=int(p.get("duration_ms", 700)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['chart-entrance', 'wipe-bottom', 'data-reveal']
INTENSITY = 6
EMBEDDING_TEXT = (
    "Chart or bar graph grows from baseline via a bottom-up wipe over 700ms. Matches the Keynote 'Build From Bottom' chart animation. Apply to chart frames, data visualisations."
)
CONTENT_MATCHERS = {'is_chart': True}
COMPLEMENTARY_WITH = ['bullet_stagger_reveal']
CONFLICTS_WITH = []
