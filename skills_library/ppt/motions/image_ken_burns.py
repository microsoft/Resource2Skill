"""image_ken_burns — subtle zoom/pan on a hero image.

For photographic or illustrative anchors: the image slowly zooms
by ~5% over 10 seconds. Ambient (indefinite) so the slide breathes.
"""
from __future__ import annotations

NAME = "image_ken_burns"
CATEGORY = "ambient"
DESCRIPTION = (
    "Hero image slowly zooms 100% -> 108% -> 100% on a 10s loop. "
    "Apple-product-page style. Plays in PowerPoint; Impress static."
)
APPLICABILITY = {
    "roles": ["cover", "hero_giant_metric", "product_showcase"],
    "anchor_names": ["hero_image", "product_shot", "photo"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "duration_ms": {"type": "int", "default": 10000, "min": 5000, "max": 20000},
    "to_pct":      {"type": "int", "default": 108,   "min": 102,  "max": 120},
}


MOOD = ['editorial', 'calm']
ARCHETYPE_FIT = ['data', 'boardroom', 'narrative', 'brand']

def apply(slide, target_shape, params=None):
    from _shell_helpers import add_pulse_loop
    p = dict(params or {})
    add_pulse_loop(
        slide, target_shape,
        duration_ms=int(p.get("duration_ms", 10000)),
        scale_pct=int(p.get("to_pct", 108)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['ambient-loop', 'photo-pan', 'subtle-breath', 'product-page']
INTENSITY = 4
EMBEDDING_TEXT = (
    "10-second subtle zoom loop (100% to 108% to 100%) on a hero photo or product render. Apple product-page feel. Tight amplitude so text overlays don't drift. For photographic content only, not line art or icons."
)
CONTENT_MATCHERS = {'is_image': True}
COMPLEMENTARY_WITH = ['dramatic_zoom', 'grow_reveal']
CONFLICTS_WITH = []
