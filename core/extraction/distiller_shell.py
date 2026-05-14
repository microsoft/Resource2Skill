"""
core/extraction/distiller_shell.py

Vision-based shell extractor. Input: a slide image (PNG/JPG) showing a
PPT layout. Output: a ShellSkill JSON with slot schema + python-pptx
render code that reads exclusively from the theme dict.

Uses Gemini 3.1 Pro with response_schema=ShellDistillerOutput. Includes
a hand-written seed shell as a few-shot example to constrain the render
code to use _shell_helpers and not fabricate colors or fonts.
"""
from __future__ import annotations

import hashlib
import logging
import os
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .schemas import ShellSkill, Slot, IntentTags, Implementation, Provenance, SourceRef

log = logging.getLogger("ppt.distill.shell")

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SEED_SHELL = _PROJECT_ROOT / "skills_library" / "ppt" / "shells_seed" / "bullet_card_list.py"
_AMBIENT_SEED_SHELL = _PROJECT_ROOT / "skills_library" / "ppt" / "shells_seed" / "cover_ambient_orbit.py"


# ---------------------------------------------------------------------------
# Pydantic response schema for Gemini
# ---------------------------------------------------------------------------


class SlotSpec(BaseModel):
    name: str = Field(..., description="Slot identifier, used as dict key")
    kind: Literal["text", "bullet_list", "image", "icon", "chart", "accent_block"]
    required: bool = True
    style: str | None = Field(None, description="Theme typography token: title_xl, title, subtitle, body, body_bold, caption, metric_xl")
    max_chars: int | None = None
    aspect: str | None = None
    bullet_capacity: int | None = None


class ShellDistillerOutput(BaseModel):
    """What Gemini must return for a shell-extraction request."""
    name: str = Field(..., description="Short human-readable name, e.g. 'Left Hero Split'")
    slide_role: list[str] = Field(
        ...,
        description="Controlled vocabulary: cover, agenda, section_divider, bullet_card_list, metric_dashboard, timeline_horizontal, comparison_split, feature_grid, quote, closing",
    )
    content_shape: str = Field(..., description="Short description, e.g. 'title+3-card-grid', 'metric+bullets'")
    density: Literal["low", "medium", "high"]
    mood: list[str] = Field(default_factory=list, description="Tags: editorial, bold, playful, minimal, corporate, technical, warm, cool")
    slots: list[SlotSpec] = Field(..., min_length=1, max_length=10)
    render_code: str = Field(
        ...,
        description=(
            "Python code defining render(slide, slots, theme). Must import from "
            "_shell_helpers (palette_color, set_textbox_text, add_solid_rect, "
            "add_theme_entrance, get_slot, truncate_to, add_hairline). Must NOT "
            "use hardcoded RGB, hex, or Pt(size) values — read colors and fonts "
            "from the theme parameter. Must call add_theme_entrance() on each "
            "visible shape for motion consistency."
        ),
    )
    reasoning: str = Field(..., description="One-line rationale for the slot schema choice")


# ---------------------------------------------------------------------------
# Few-shot seed
# ---------------------------------------------------------------------------


def _load_seed_example() -> str:
    """Return the bullet_card_list seed shell as a reference implementation."""
    if _SEED_SHELL.exists():
        return _SEED_SHELL.read_text()
    return ""


def _load_ambient_seed_example() -> str:
    """Return the ambient-capable seed shell as a calibration reference."""
    if _AMBIENT_SEED_SHELL.exists():
        return _AMBIENT_SEED_SHELL.read_text()
    return ""


# ---------------------------------------------------------------------------
# Distiller
# ---------------------------------------------------------------------------


_DISTILL_SYSTEM = """You are a slide-layout distiller. You receive ONE slide image (a screenshot from a PowerPoint tutorial or template) and must extract it into a reusable "shell" — a parameterized layout function with named slots.

RULES:

1. Identify the slide's ROLE (cover / agenda / section_divider / bullet_card_list / metric_dashboard / timeline_horizontal / comparison_split / feature_grid / quote / closing).

2. Declare SLOTS — named placeholders for the variable parts (text strings, bullet items, images). Every slot gets: name, kind, required, style (a theme typography token), and optional constraints (max_chars, aspect, bullet_capacity). Example: for a cover slide the slots might be [eyebrow, headline, subhead, hero_image].
   - Set max_chars REALISTICALLY based on the visible space. A KPI value box that holds "$148M" needs max_chars ≥ 8. A 3-card grid label that fits "Sustain growth quality" needs ≥ 25.
   - Set bullet_capacity to the visible count.

3. Write render(slide, slots, theme) code that reproduces the layout. MANDATORY:
   - Import helpers from _shell_helpers (palette_color, set_textbox_text, add_solid_rect, add_theme_entrance, add_emphasis_pulse, add_sequential_reveal, get_slot, truncate_to, add_hairline).
   - ALL colors come from palette_color(theme, "<palette_key>") — never RGBColor(...) with hardcoded values.
   - ALL fonts/sizes come from theme["typography"]["<style_token>"] via apply_type_style / set_textbox_text — never Pt(42) etc.
   - Always call set_textbox_text(...) for text — it auto-shrinks to fit. Do NOT manually create text frames with hardcoded font sizes.
   - **Motion**: call add_theme_entrance(slide, shape, theme, delay_ms=..., index=i) on each visible shape. For emphasis on key shapes (KPI numbers, CTA buttons, hero shapes), additionally call add_emphasis_pulse(slide, shape, theme, delay_ms=2000) so they pulse after entrance. Use add_sequential_reveal(slide, [shape1, shape2, shape3], theme) for ordered groups (timeline steps, list items).
   - **Spacing**: stay within slide bounds — Inches(0.6) ≤ x ≤ Inches(12.7), Inches(0.3) ≤ y ≤ Inches(7.2). Leave at least Inches(0.1) gap between any two non-overlapping shapes.
   - **Text colors**: dark text ("text") goes on light fills; light text ("bg" or "text" if light theme) goes on dark accent fills. NEVER put "text" color on a "panel" fill if both are dark.

4. The render code must work even if optional slots are missing (use get_slot(slots, name, default=None)).

5. Your output MUST match the response_schema exactly — structured JSON only.

6. AMBIENT MOTION VOCABULARY. If the source frames show *continuous* or *looping* motion (a rotating cog mechanism, planets orbiting, a pulsing highlight, a drifting decorative shape), you MUST emit code that calls one of these primitives exported from `_shell_helpers`:
   - `add_infinite_rotation(slide, shape, duration_ms=..., direction="cw"|"ccw")` — continuous rotation, backed by `<p:animRot>` + `repeatCount="indefinite"`.
   - `add_orbital_motion(slide, shape, center_xy=(cx_in, cy_in), radius_in=..., duration_ms=..., direction="cw"|"ccw")` — circular path around a center point, backed by `<p:animMotion>` + `repeatCount="indefinite"`.
   - `add_pulse_loop(slide, shape, duration_ms=..., scale_pct=...)` — scale between 100% and `scale_pct` forever (auto-reversed).
   - `add_drift_motion(slide, shape, dx_in=..., dy_in=..., duration_ms=..., pingpong=True)` — gentle back-and-forth translation.
   These are the only approved way to emit continuous motion. Do NOT write custom `<p:anim>` / `<p:animRot>` XML when one of these fits; do NOT emit `repeatCount="indefinite"` by hand. When you emit a shell that uses any of these primitives, also set the module-level constant `AMBIENT_CAPABLE = True` at the top of the file (above the `SLOTS = [...]` declaration) so the retrieval layer marks the shell as ambient-capable. Use these primitives ONLY when the source frames actually depict continuous motion — do not sprinkle them on static tutorials.

7. MORPH ANCHOR NAMING. When a tutorial shows an element morphing across a slide boundary (a logo moving, a number resizing, a section chip sliding across), tag the morphable shape with `set_morph_anchor(shape, role)` from `_shell_helpers`. `role` MUST be one of `brand_mark`, `accent_orb`, `hero_number`, `hero_headline`, `section_chip` per the contract at `docs/ppt_morph_continuity_contract.md`. This writes the PowerPoint `!!sameName` force-match name so the same role can morph across adjacent slides. Do not invent additional role names.
"""


_USER_TEMPLATE = """Here is a slide image. Extract it into a shell.

REFERENCE IMPLEMENTATION — this is a hand-written seed shell (bullet_card_list). Match its style, helper usage, and theme-token discipline:

```python
{seed_code}
```

AMBIENT-MOTION REFERENCE — when the source frame depicts continuous motion (rotation, orbit, pulse, drift), match THIS shell's use of `add_infinite_rotation` / `add_orbital_motion` / `add_pulse_loop` / `add_drift_motion` and remember to set `AMBIENT_CAPABLE = True` at module top:

```python
{ambient_seed_code}
```

Now extract the shell from the provided image. Output ShellDistillerOutput JSON. {motion_hint}"""


def distill_shell_from_image(
    image_path: str | Path,
    model: str = "gemini-3.1-pro-preview",
    api_key: str | None = None,
    source_video_id: str | None = None,
    source_timestamp: str | None = None,
    max_retries: int = 3,
) -> dict:
    """Extract a shell from a slide image via Gemini 3.1 Pro.

    Retries up to max_retries with lint feedback if the generated code
    fails the helper/theme-token checks.
    """
    from google import genai
    from google.genai import types

    img = Path(image_path)
    if not img.exists():
        return {"error": f"image not found: {img}"}

    seed_code = _load_seed_example()
    ambient_seed_code = _load_ambient_seed_example()

    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        return {"error": "GEMINI_API_KEY / GOOGLE_API_KEY not set"}

    client = genai.Client(api_key=key)

    img_part = types.Part.from_bytes(
        data=img.read_bytes(),
        mime_type="image/jpeg" if img.suffix.lower() in (".jpg", ".jpeg") else "image/png",
    )

    config = types.GenerateContentConfig(
        system_instruction=_DISTILL_SYSTEM,
        response_mime_type="application/json",
        response_schema=ShellDistillerOutput,
        temperature=0.2,
    )

    user_prompt = _USER_TEMPLATE.format(
        seed_code=seed_code,
        ambient_seed_code=ambient_seed_code,
        motion_hint=_motion_hint(image_path, source_video_id),
    )

    last_errors: list[str] = []
    for attempt in range(max_retries):
        if attempt > 0 and last_errors:
            retry_note = (
                f"\n\nPREVIOUS ATTEMPT FAILED with these errors:\n"
                + "\n".join(f"  - {e}" for e in last_errors)
                + "\n\nFix these specifically. In particular, colors MUST go through "
                  "palette_color(theme, 'bg'|'panel'|'accent'|'accent2'|'text'|'muted') "
                  "and text styling MUST go through set_textbox_text(...) or "
                  "apply_type_style(run, theme, 'title'|'body'|...). Do NOT use "
                  "RGBColor(...) directly anywhere except as receiver for the result of palette_color()."
            )
            prompt_this_attempt = user_prompt + retry_note
        else:
            prompt_this_attempt = user_prompt

        text_part = types.Part(text=prompt_this_attempt)
        try:
            resp = client.models.generate_content(
                model=model,
                contents=[types.Content(parts=[img_part, text_part])],
                config=config,
            )
        except Exception as e:
            log.warning("Gemini distill failed for %s (attempt %d): %s",
                        img.name, attempt + 1, e)
            last_errors = [f"gemini call failed: {e}"]
            continue

        try:
            parsed = resp.parsed
            if parsed is None:
                import json as _json
                parsed = ShellDistillerOutput.model_validate(_json.loads(resp.text))
        except Exception as e:
            last_errors = [f"response parse failed: {e}"]
            continue

        code = parsed.render_code
        lint_errors = _lint_render_code(code)
        if not lint_errors:
            # Success — build and return
            skill_id = _make_skill_id(parsed.name)
            return {
                "skill_id": skill_id,
                "skill_type": "shell",
                "name": parsed.name,
                "status": "candidate",
                "intent_tags": {
                    "slide_role": parsed.slide_role,
                    "content_shape": [parsed.content_shape],
                    "density": parsed.density,
                    "mood": parsed.mood,
                    "compatible_themes": [],
                },
                "slots": [s.model_dump() for s in parsed.slots],
                "implementation": {
                    "entrypoint": "render(slide, slots, theme)",
                    "code_path": f"code/{skill_id}.py",
                },
                "provenance": {
                    "source": {
                        "type": "youtube" if source_video_id else "manual",
                        "video_id": source_video_id,
                        "timestamp": source_timestamp,
                    },
                    "distilled_by": f"{model}@distill_shell",
                    "confidence": max(0.5, 0.85 - 0.1 * attempt),
                },
                "_render_code": code,
                "_reasoning": parsed.reasoning,
                "_attempts": attempt + 1,
            }
        # Lint failed — log and retry with feedback
        last_errors = lint_errors
        log.info("distill attempt %d/%d lint failed for %s: %s",
                 attempt + 1, max_retries, img.name, lint_errors)

    return {
        "error": f"lint failed after {max_retries} attempts: {'; '.join(last_errors)}",
    }


# ---------------------------------------------------------------------------
# Lint
# ---------------------------------------------------------------------------


_FORBIDDEN_PATTERNS = [
    (r"RGBColor\(\s*\d+", "hardcoded RGBColor(r,g,b) — must use palette_color(theme, ...)"),
    (r"#[0-9A-Fa-f]{6}", "hardcoded hex color — must use theme"),
    (r"\bPt\(\s*\d{2,}\s*\)", "hardcoded Pt(N) >= 10 — font sizes must come from theme typography"),
]

_REQUIRED_PATTERNS = [
    (r"from _shell_helpers import", "must import from _shell_helpers"),
    (r"def render\s*\(\s*slide[^,]*,\s*slots[^,]*,\s*theme", "render(slide, slots, theme) signature required"),
    (r"palette_color\s*\(\s*theme", "must read colors via palette_color(theme, ...)"),
]


def _lint_render_code(code: str) -> list[str]:
    errors = []
    # Forbidden
    for pat, msg in _FORBIDDEN_PATTERNS:
        if re.search(pat, code):
            # Allow Pt() inside line widths / tracking if small number
            if "Pt(" in pat:
                # gather all Pt(N) and only flag large ones that are clearly font sizes
                for m in re.finditer(r"Pt\(\s*(\d+(?:\.\d+)?)\s*\)", code):
                    if float(m.group(1)) >= 10:
                        errors.append(msg)
                        break
            else:
                errors.append(msg)
    # Required
    for pat, msg in _REQUIRED_PATTERNS:
        if not re.search(pat, code):
            errors.append(f"missing: {msg}")
    # Basic syntax
    try:
        import ast
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"syntax error: {e}")
    return errors


def _make_skill_id(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")[:40]
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:6]
    return f"{slug}_{h}"


_MOTION_HINT_KEYWORDS = (
    "rotat", "orbit", "spin", "pulse", "loop", "indefinite",
    "ambient", "motion_path", "anim", "morph",
)


def _motion_hint(image_path, video_id) -> str:
    """Return a one-line nudge appended to the user prompt when the image
    path or source video id suggests continuous motion. The nudge tells the
    distiller to consider the ambient primitives explicitly; it does NOT
    force their use when the frame is genuinely static.
    """
    haystack = " ".join(filter(None, [str(image_path or ""), str(video_id or "")])).lower()
    if any(tok in haystack for tok in _MOTION_HINT_KEYWORDS):
        return (
            "If the slide visibly depicts continuous motion (an orbiting "
            "element, a rotating wheel, a pulsing highlight, a drifting "
            "decoration), prefer the ambient primitives shown in the "
            "ambient-motion reference and set AMBIENT_CAPABLE = True."
        )
    return ""


__all__ = ["distill_shell_from_image", "ShellDistillerOutput", "_lint_render_code"]
