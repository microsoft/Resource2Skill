"""
core/extraction/schemas.py

Pydantic v2 models for the unified Skill system (v2 refactor).
See docs/ppt_skill_system_v2_refactor.md for the full design.

Three skill kinds live in one store, discriminated by `skill_type`:
  - shell        → parameterized whole-slide layout with named slots
  - snippet      → reusable code primitive (function body)
  - inspiration  → visual reference (frames + palette + composition notes)

Themes and Deck Archetypes are separate top-level artifacts (not skills)
but use the same pydantic toolchain for validation.
"""
from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class SlotKind(str, Enum):
    TEXT = "text"
    BULLET_LIST = "bullet_list"
    IMAGE = "image"
    ICON = "icon"
    CHART = "chart"
    ACCENT_BLOCK = "accent_block"


class SkillStatus(str, Enum):
    ACTIVE = "active"
    CANDIDATE = "candidate"      # failed quality gate, hidden from default retrieval
    DEPRECATED = "deprecated"    # failed on usage, kept read-only
    SUPERSEDED = "superseded"    # merged into another skill


class Density(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MotionPersonality(str, Enum):
    EDITORIAL = "editorial"       # subtle fade / slide — calm
    TECH = "tech"                 # zoom / wipe — crisp, fast
    PLAYFUL = "playful"           # bounce / spin — energetic
    MINIMAL = "minimal"           # fade only — restrained
    BOLD = "bold"                 # zoom + emphasis pulse — loud
    DYNAMIC = "dynamic"           # zoom + wipe mix — product-launch energy
    RESTRAINED = "restrained"     # fade only, boardroom cadence
    CALM = "calm"                 # fade + gentle rise — warm/research
    CINEMATIC = "cinematic"       # long fades + morphs — brand/editorial


# ---------------------------------------------------------------------------
# Shared sub-models
# ---------------------------------------------------------------------------


class Slot(BaseModel):
    """A named placeholder a shell exposes for content injection."""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Slot identifier, used as key in slots dict")
    kind: SlotKind
    required: bool = True
    style: str | None = Field(
        None,
        description="Logical typography/color token from the theme, e.g. 'title_xl', 'accent_dark'",
    )
    max_chars: int | None = Field(None, description="For text slots: max characters before truncation/warning")
    min_chars: int | None = None
    aspect: str | None = Field(None, description="For image slots, e.g. '16:9' or '1:1'")
    bullet_capacity: int | None = Field(None, description="For bullet_list slots: expected item count")
    fallback: str | None = Field(
        None,
        description="If slot not provided, e.g. 'solid_fill:accent_dark' or 'skip'",
    )


class IntentTags(BaseModel):
    """Controlled-vocabulary tags for skill retrieval."""
    model_config = ConfigDict(extra="forbid")

    slide_role: list[str] = Field(
        default_factory=list,
        description="From taxonomy.yaml: cover, agenda, section_divider, bullet_card_list, etc.",
    )
    content_shape: list[str] = Field(
        default_factory=list,
        description="Describes the content layout: 'title+subtitle+image', '3-column', '4-metric', etc.",
    )
    density: Density = Density.MEDIUM
    mood: list[str] = Field(
        default_factory=list,
        description="editorial, bold, playful, minimal, corporate, etc.",
    )
    color_family: list[str] = Field(
        default_factory=list,
        description="dark_neutral, light_warm, saturated_cool, etc.",
    )
    compatible_themes: list[str] = Field(
        default_factory=list,
        description="Theme IDs this shell renders well in. Empty list = theme-agnostic.",
    )


class TaskFit(BaseModel):
    """Hard constraints used by the retrieval filter stage."""
    model_config = ConfigDict(extra="forbid")

    max_text_chars: int | None = None
    min_text_chars: int | None = None
    requires_image: bool = False
    bullet_capacity: int | None = None


class Signature(BaseModel):
    """Hashes used for deduplication at ingest time."""
    model_config = ConfigDict(extra="forbid")

    visual_phash: str | None = Field(None, description="Perceptual hash of rendered thumbnail")
    code_ast_hash: str | None = Field(None, description="SHA-256 of AST-normalized implementation code")
    palette: list[str] = Field(default_factory=list, description="Sampled hex colors from rendered preview")


class Implementation(BaseModel):
    """How to execute this skill to produce slide content."""
    model_config = ConfigDict(extra="forbid")

    entrypoint: str = Field(
        ...,
        description="Function signature, e.g. 'render(slide, slots, theme)' for shell or 'apply(shape, **kwargs)' for snippet",
    )
    code_path: str = Field(..., description="Path relative to the skill directory, e.g. 'code/diagonal_split_hero.py'")
    deps: list[str] = Field(default_factory=list, description="PyPI deps beyond python-pptx/Pillow baseline")


class SourceRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["youtube", "manual", "promoted_legacy"] = "youtube"
    video_id: str | None = None
    video_url: str | None = None
    timestamp: str | None = Field(None, description="HH:MM:SS in source video")


class Provenance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: SourceRef = Field(default_factory=lambda: SourceRef(type="manual"))
    distilled_by: str | None = Field(None, description="e.g. 'gemini-2.5-pro@2026-04' or 'human@<author>'")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class Quality(BaseModel):
    """Post-hoc quality metrics updated by the sweeper."""
    model_config = ConfigDict(extra="forbid")

    exec_ok: bool = False
    render_ok: bool = False
    visual_sim_to_source: float | None = Field(None, ge=0.0, le=1.0)
    rubric_score: float | None = Field(None, ge=0.0, le=1.0)
    usage_count: int = 0
    success_rate: float | None = Field(None, ge=0.0, le=1.0)
    last_checked: str | None = Field(None, description="ISO timestamp of last quality-gate run")


class InspirationFrame(BaseModel):
    """A visual reference frame for inspiration-type skills."""
    model_config = ConfigDict(extra="forbid")

    path: str
    palette: list[str] = Field(default_factory=list)
    composition_notes: str | None = None
    seconds: float | None = None


# ---------------------------------------------------------------------------
# Skill envelope (discriminated union)
# ---------------------------------------------------------------------------


class SkillBase(BaseModel):
    """Shared envelope fields. Never instantiated directly."""
    model_config = ConfigDict(extra="forbid")

    skill_id: str = Field(..., pattern=r"^[a-z0-9_]+_[a-f0-9]{4,8}$")
    version: int = 1
    status: SkillStatus = SkillStatus.ACTIVE
    name: str
    intent_tags: IntentTags = Field(default_factory=IntentTags)
    signature: Signature = Field(default_factory=Signature)
    provenance: Provenance = Field(default_factory=Provenance)
    quality: Quality = Field(default_factory=Quality)
    superseded_by: str | None = Field(None, description="skill_id that replaced this one")


class ShellSkill(SkillBase):
    """A parameterized whole-slide layout with named slots."""
    skill_type: Literal["shell"] = "shell"
    task_fit: TaskFit = Field(default_factory=TaskFit)
    slots: list[Slot] = Field(..., min_length=1)
    implementation: Implementation


class SnippetSkill(SkillBase):
    """A reusable code primitive (function body) with no slot schema."""
    skill_type: Literal["snippet"] = "snippet"
    implementation: Implementation


class InspirationSkill(SkillBase):
    """A visual reference — frames + palette + composition notes, no executable code."""
    skill_type: Literal["inspiration"] = "inspiration"
    frames: list[InspirationFrame] = Field(..., min_length=1)
    palette: list[str] = Field(default_factory=list)
    composition_notes: str | None = None


Skill = Annotated[
    Union[ShellSkill, SnippetSkill, InspirationSkill],
    Field(discriminator="skill_type"),
]


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------


class TypographyStyle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    font: str = Field(..., description="Font family name, e.g. 'Inter' or 'Source Serif Pro'")
    size: float = Field(..., gt=0, description="Point size")
    weight: int = Field(default=400, ge=100, le=900)
    tracking: float = Field(default=0.0, description="Letter-spacing as fraction of em, e.g. -0.02")
    upper: bool = Field(default=False, description="If true, render text in uppercase")
    italic: bool = False


class Palette(BaseModel):
    """Core 6 colors every theme must provide, plus optional extras."""
    model_config = ConfigDict(extra="allow")  # allow extra named colors

    bg: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    panel: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    accent: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    accent2: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    text: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    muted: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")


class Motif(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(
        ...,
        description="e.g. 'serif_number', 'grid_lines', 'gradient_mesh', 'none'",
    )
    description: str


class Spacing(BaseModel):
    model_config = ConfigDict(extra="allow")

    margin: float = Field(default=0.6, description="Slide-edge margin in inches")
    gutter: float = Field(default=0.3, description="Between-element gutter in inches")


class Motion(BaseModel):
    model_config = ConfigDict(extra="allow")

    personality: MotionPersonality = MotionPersonality.EDITORIAL
    preferred_entrance: list[str] = Field(
        default_factory=list,
        description="Filter values in preference order, e.g. ['fade', 'in_bottom']",
    )
    stagger_ms: int = 120
    avoid: list[str] = Field(default_factory=list, description="Effects to suppress, e.g. ['spin', 'bounce']")


class Theme(BaseModel):
    model_config = ConfigDict(extra="allow")

    theme_id: str = Field(..., pattern=r"^[a-z0-9_]+$")
    name: str
    palette: Palette
    typography: dict[str, TypographyStyle] = Field(
        ...,
        description="Keyed by style token: title_xl, title, subtitle, body, caption, etc. "
                    "Shell code references these by name, never by literal font/size.",
    )
    motif: Motif
    spacing: Spacing = Field(default_factory=Spacing)
    motion: Motion = Field(default_factory=Motion)
    # LLM-readable selection metadata (added 2026-04-19)
    mood: list[str] = Field(default_factory=list)
    archetype_fit: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Deck Archetype
# ---------------------------------------------------------------------------


class SlidePlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str = Field(..., description="Matches a slide_role tag in the skill taxonomy")
    content: str = Field(..., description="One-line description of what goes on this slide")
    required: bool = True
    optional_notes: str | None = None


class ArchetypeSection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section: str = Field(..., description="Section label: intro, problem, product, etc.")
    slides: list[SlidePlan]


class DeckArchetype(BaseModel):
    model_config = ConfigDict(extra="forbid")

    archetype_id: str = Field(..., pattern=r"^[a-z0-9_]+$")
    name: str
    description: str = ""
    suggested_slides: int = Field(15, ge=3, le=40)
    sections: list[ArchetypeSection] = Field(..., min_length=1)
    recommended_themes: list[str] = Field(
        default_factory=list,
        description="Theme IDs that pair well with this archetype; empty = any",
    )


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def validate_skill_dict(data: dict) -> Skill:
    """Validate a raw dict as a Skill, routing to the right subtype via discriminator."""
    from pydantic import TypeAdapter

    adapter = TypeAdapter(Skill)
    return adapter.validate_python(data)


def validate_theme_dict(data: dict) -> Theme:
    return Theme.model_validate(data)


def validate_archetype_dict(data: dict) -> DeckArchetype:
    return DeckArchetype.model_validate(data)


__all__ = [
    # Enums
    "SlotKind", "SkillStatus", "Density", "MotionPersonality",
    # Sub-models
    "Slot", "IntentTags", "TaskFit", "Signature", "Implementation",
    "SourceRef", "Provenance", "Quality", "InspirationFrame",
    # Skills
    "SkillBase", "ShellSkill", "SnippetSkill", "InspirationSkill", "Skill",
    # Theme
    "TypographyStyle", "Palette", "Motif", "Spacing", "Motion", "Theme",
    # Archetype
    "SlidePlan", "ArchetypeSection", "DeckArchetype",
    # Validators
    "validate_skill_dict", "validate_theme_dict", "validate_archetype_dict",
]
