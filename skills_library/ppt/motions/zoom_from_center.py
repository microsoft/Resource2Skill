"""zoom_from_center — element zooms in from 30% to 100%.

Good for icons, badges, or single-focus visuals that should
"pop" into existence without directional bias. Distinct from
grow_reveal in that zoom_from_center starts much smaller (30%
vs 70%) and has a quick snap feel instead of a cinematic settle.
"""
from __future__ import annotations

NAME = "zoom_from_center"
CATEGORY = "entrance"
DESCRIPTION = (
    "Shape zooms from 30% to 100% over 500ms with fade. Snappy "
    "entrance for icons, badges, callouts."
)
APPLICABILITY = {
    "roles": ["kpi_card", "feature_stat", "closing_cta", "cover"],
    "anchor_names": ["icon", "badge", "callout", "logo", "seal"],
    "max_per_slide": 3,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 300, "min": 0, "max": 4000},
    "duration_ms": {"type": "int", "default": 500, "min": 200, "max": 1200},
    "from_pct":    {"type": "int", "default": 30,  "min": 10,  "max": 60},
}


MOOD = ['bold', 'cinematic', 'editorial']
ARCHETYPE_FIT = ['brand', 'product', 'data', 'boardroom']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_zoom_in
    p = dict(params or {})
    emit_zoom_in(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 300)),
        duration_ms=int(p.get("duration_ms", 500)),
        from_pct=int(p.get("from_pct", 30)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['snappy', 'icon-pop', 'center-scale']
INTENSITY = 6
EMBEDDING_TEXT = (
    'Snappy 30% to 100% center zoom over 500ms. For small focal elements: icons, seals, chips, callout badges. Direction-agnostic. Faster and crisper than grow_reveal; use when you want several icons to arrive together.'
)
CONTENT_MATCHERS = {'is_headline': False, 'max_chars': 20}
COMPLEMENTARY_WITH = ['pulse_emphasis']
CONFLICTS_WITH = ['dramatic_zoom', 'grow_reveal', 'bounce_in']
