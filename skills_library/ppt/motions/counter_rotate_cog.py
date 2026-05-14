"""counter_rotate_cog — continuous reverse rotation ambient.

Pair with orbital_accent on another shape for a cog-like
counter-spinning visual. Continuous indefinite animation.
"""
from __future__ import annotations

NAME = "counter_rotate_cog"
CATEGORY = "ambient"
DESCRIPTION = (
    "Indefinite CCW rotation (8s per revolution). Pair with "
    "orbital_accent or another rotating shape for pm_cogs-style "
    "counter-rotation symmetry."
)
APPLICABILITY = {
    "roles": ["cover", "hero_giant_metric", "section_divider"],
    "anchor_names": ["cog", "ring", "halo", "accent_orb",
                     "background_ring", "secondary_ring"],
    "max_per_slide": 1,
}
PARAMETERS = {
    "duration_ms": {"type": "int", "default": 8000, "min": 3000, "max": 20000},
}


MOOD = ['technical', 'editorial', 'calm']
ARCHETYPE_FIT = ['product', 'brand', 'data', 'boardroom']

def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_counter_rotate
    p = dict(params or {})
    emit_counter_rotate(
        slide, target_shape,
        duration_ms=int(p.get("duration_ms", 8000)),
    )


# ---- Phase-A semantic ranking metadata ----
TAGS = ['ambient-loop', 'rotation', 'cog-pair', 'mechanical']
INTENSITY = 6
EMBEDDING_TEXT = (
    'Continuous CCW rotation, 8 seconds per revolution. Pair with orbital_accent or another rotating shape on the same slide for a pm_cogs-style counter-spinning mechanism. Best on ring, cog, gear, secondary halo shapes.'
)
CONTENT_MATCHERS = {'is_decorative': True}
COMPLEMENTARY_WITH = ['orbital_accent', 'breathing_halo']
CONFLICTS_WITH = []
