"""rotate_in — dynamic rotating entrance.

Shape rotates from -45deg to 0 while fading in. Much more dynamic
than flat fade — the rotation motion triggers Apple-style
'something is coming at you' feel.
"""
from __future__ import annotations

NAME = "rotate_in"
CATEGORY = "entrance"
DESCRIPTION = (
    "Shape rotates from -45deg to 0 + fade over 800ms. Dynamic "
    "directional arrival for graphics, icons, decorative accents."
)
APPLICABILITY = {
    "roles": ["cover", "hero_giant_metric", "feature_stat",
              "product_showcase"],
    "anchor_names": ["accent", "icon", "badge", "logo", "seal",
                     "accent_orb", "halo"],
    "max_per_slide": 2,
}
PARAMETERS = {
    "delay_ms":    {"type": "int", "default": 200, "min": 0, "max": 3000},
    "duration_ms": {"type": "int", "default": 800, "min": 400, "max": 1500},
    "from_deg":    {"type": "int", "default": -45, "min": -180, "max": 180},
}


MOOD = ['cinematic', 'editorial', 'technical', 'bold']
ARCHETYPE_FIT = ['brand', 'narrative', 'product', 'data']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_rotate_in
    p = dict(params or {})
    emit_rotate_in(
        slide, target_shape,
        delay_ms=int(p.get("delay_ms", 200)),
        duration_ms=int(p.get("duration_ms", 800)),
        from_deg=int(p.get("from_deg", -45)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['dynamic', 'directional', 'spin-arrival', 'cinematic']
INTENSITY = 7
EMBEDDING_TEXT = (
    "Rotate from -45 degrees to 0 while fading in over 800ms. Dynamic directional entrance for decorative icons, logos, accent shapes, badges. Gives a 'something is coming at you' feel. Not recommended for body text."
)
CONTENT_MATCHERS = {'is_headline': False}
COMPLEMENTARY_WITH = ['breathing_halo', 'orbital_accent']
CONFLICTS_WITH = ['slide_in_left', 'fly_in']
