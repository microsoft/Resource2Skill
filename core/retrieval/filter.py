"""
core/retrieval/filter.py — hard filter stage (local, millisecond).

Filters shells by slide intent before any LLM call. The goal is to cut the
candidate set from "every shell" to "reasonable shells" using cheap
metadata checks, so the picker stage sees 5-20 candidates, not 50+.
"""
from __future__ import annotations

from typing import Any


def filter_shells(
    shells: list[dict],
    *,
    slide_role: str | None = None,
    theme_id: str | None = None,
    requires_image: bool | None = None,
    bullet_capacity_min: int | None = None,
    require_ambient: bool | None = None,
    status_active_only: bool = True,
) -> list[dict]:
    """Apply hard filters. Missing metadata keys are treated as 'unknown'
    (i.e. the shell is kept rather than rejected).

    Args:
        shells: list of shell cards (dicts from list_shells).
        slide_role: if set, shell must have this in its intent_tags.slide_role (or be tagged for any role).
        theme_id: if set, shell must list it in compatible_themes OR have empty compatible_themes.
        requires_image: if True, only shells that accept an image slot.
        bullet_capacity_min: if set, shell's bullet_capacity must be >= N.
        require_ambient: if True, only shells with ambient_capable=True are kept.
        status_active_only: drop shells with status="candidate"/"deprecated" (default True).
    """
    out = []
    for sh in shells:
        # Status check
        if status_active_only and sh.get("status") and sh.get("status") != "active":
            continue

        if require_ambient and not sh.get("ambient_capable"):
            continue

        # Slide role — look at intent_tags.slide_role OR a legacy field
        if slide_role:
            tags = (sh.get("intent_tags") or {}).get("slide_role", [])
            fallback_tags = sh.get("slide_role_tags", [])  # for seed shells without full tags
            all_roles = list(tags) + list(fallback_tags)
            # Heuristic: if shell_id contains the role keyword, accept
            if not all_roles:
                if slide_role.lower() in sh.get("shell_id", "").lower():
                    pass  # accept by name match
                else:
                    # Unknown — keep so agent can still pick (don't starve candidates)
                    pass
            elif slide_role not in all_roles:
                continue

        # Theme compat
        if theme_id:
            compat = (sh.get("intent_tags") or {}).get("compatible_themes", [])
            if compat and theme_id not in compat:
                continue

        # Image requirement
        if requires_image is True:
            slot_names = sh.get("slot_names", [])
            has_image_slot = any("image" in n.lower() or "hero" in n.lower() or "photo" in n.lower()
                                 for n in slot_names)
            if not has_image_slot:
                continue

        # Bullet capacity
        if bullet_capacity_min:
            caps = []
            for slot in sh.get("slots", []):
                if slot.get("kind") == "bullet_list":
                    caps.append(slot.get("bullet_capacity", 0) or 0)
            if caps and max(caps) < bullet_capacity_min:
                continue

        out.append(sh)
    return out


__all__ = ["filter_shells"]
