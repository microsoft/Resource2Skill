"""
core/retrieval/cards.py — format metadata cards for LLM consumption.

A "card" is a compact human-readable summary of a Skill/Theme/Archetype
that the picker LLM reads. Short enough to fit dozens in one prompt.
"""
from __future__ import annotations


def format_archetype_card(a: dict) -> str:
    """Compact summary for the archetype picker."""
    secs = ", ".join(a.get("sections", []))
    rec = ", ".join(a.get("recommended_themes", [])) or "any"
    return (
        f"[{a['archetype_id']}] {a['name']}  ({a.get('suggested_slides', a.get('actual_slide_count', '?'))} slides)\n"
        f"   sections:  {secs}\n"
        f"   themes:    {rec}\n"
        f"   notes:     {a.get('description', '').replace(chr(10), ' ')[:200]}"
    )


def format_theme_card(t: dict) -> str:
    """Compact summary for the theme picker."""
    palette = " ".join(t.get("palette_preview", []))
    return (
        f"[{t['theme_id']}] {t['name']}\n"
        f"   palette:   {palette}\n"
        f"   motion:    {t.get('motion_personality', '?')}\n"
        f"   motif:     {t.get('motif', '?')}\n"
        f"   font:      {t.get('font_primary', 'Inter')}"
    )


def format_shell_card(s: dict) -> str:
    """Compact summary for the shell picker, with content-capacity hints
    so the agent doesn't pick a metric_dashboard with 12-char cap for a 50-char label."""
    doc = (s.get("doc") or "").strip()
    # Build per-slot capacity summary
    slot_lines = []
    for slot in s.get("slots", []):
        name = slot.get("name", "?")
        kind = slot.get("kind", "?")
        bits = [kind]
        if slot.get("max_chars"):
            bits.append(f"≤{slot['max_chars']}ch")
        if slot.get("bullet_capacity"):
            bits.append(f"×{slot['bullet_capacity']}")
        if slot.get("aspect"):
            bits.append(slot["aspect"])
        if not slot.get("required", True):
            bits.append("opt")
        slot_lines.append(f"{name}({', '.join(bits)})")
    slots_str = ", ".join(slot_lines) if slot_lines else "—"
    ambient_marker = "  [ambient]" if s.get("ambient_capable") else ""
    return (
        f"[{s['shell_id']}]{ambient_marker}  {doc[:120]}\n"
        f"   slots:     {slots_str}"
    )


def format_shell_card_list(shells: list[dict]) -> str:
    """Format multiple shell cards separated by blank lines."""
    return "\n\n".join(format_shell_card(s) for s in shells)


__all__ = [
    "format_archetype_card",
    "format_theme_card",
    "format_shell_card",
    "format_shell_card_list",
]
