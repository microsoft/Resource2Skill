"""core/extraction — Skill extraction pipeline (v2).

See docs/ppt_skill_system_v2_refactor.md for the design.
"""
from .schemas import (
    Skill, ShellSkill, SnippetSkill, InspirationSkill,
    Theme, DeckArchetype,
    Slot, IntentTags, TaskFit, Implementation, Provenance, Quality,
    SkillStatus, SlotKind, Density, MotionPersonality,
    validate_skill_dict, validate_theme_dict, validate_archetype_dict,
)

__all__ = [
    "Skill", "ShellSkill", "SnippetSkill", "InspirationSkill",
    "Theme", "DeckArchetype",
    "Slot", "IntentTags", "TaskFit", "Implementation", "Provenance", "Quality",
    "SkillStatus", "SlotKind", "Density", "MotionPersonality",
    "validate_skill_dict", "validate_theme_dict", "validate_archetype_dict",
]
