"""
domains/ppt/agent_hooks.py
PPT domain agent hooks — auto-verification + progress tracking.

auto_verify: called after every tool call, can make live MCP calls.
  - After add_slide_from_shell (v2 path): renders slide to PNG, sends to
    GPT-5.4 vision for QA.
  - Legacy v1 tool names (add_slide, add_slide_from_skill, replace_slide)
    are still recognised for back-compat but the user-facing guidance
    always steers back to add_slide_from_shell.
  - Replace cap: zero automatic visual-QA rebuilds in main-bench mode; finish
    the deck and let save-time completion gates decide.
progress_check: called every 10 iterations, reports deck health against
  the archetype's suggested_slides (or deck-plan.json) — no hard-coded
  slide-count target.
"""
import json
import logging
import re

log = logging.getLogger("ppt_hooks")

_used_skills: set[str] = set()
_skill_ref_slides: set[int] = set()  # slides whose add_slide code references a skill via "# from skill:"
_current_theme: str | None = None  # auto-detected from slide background colors
_slide_add_count: int = 0  # track add_slide calls for sampling

# Track per-slide replace count: slide_index -> count. Main-bench PPT uses
# v2 shells as the execution surface, so visual QA must not trigger an
# open-ended rebuild/delete loop. Save-time guards catch true completion
# failures; slide-level visual findings are advisory.
_replace_counts: dict[int, int] = {}
_MAX_REPLACES_PER_SLIDE = 0
# Deck-level cap: total replace budget across the whole deck. After this,
# auto-PASS every QA issue and push agent to keep building forward.
_MAX_REPLACES_PER_DECK = 5

# Track per-category skill failures: category -> [skill_id, ...]
_skill_failures: dict[str, list[str]] = {}

# Layout zone constants (inches) — must match agent_prompt.md Design Spec
_TITLE_ZONE_MAX_Y = 1.10
_CONTENT_ZONE_MIN_Y = 1.20
_CONTENT_ZONE_MAX_Y = 6.60
_FOOTER_ZONE_MIN_Y = 6.70
_LEFT_MARGIN = 0.50
_RIGHT_EDGE = 12.83
_CANVAS_HEIGHT = 7.5


def _infer_target_slide_count(invocations) -> int | None:
    """Find the archetype target from pick_archetype / deck-plan.json output."""
    import json as _json
    import re as _re
    from pathlib import Path as _Path

    # 1. Look at pick_archetype's JSON return — it includes archetype_id; try
    #    to load the archetype's suggested_slides from disk.
    pick_calls = [inv for inv in invocations
                  if inv.tool_name == "pick_archetype" and not inv.error]
    for inv in reversed(pick_calls):
        result = inv.result or ""
        try:
            payload = _json.loads(result)
            target = payload.get("slides_target") or payload.get("requested_slides_target")
            if target:
                return int(target)
        except Exception:
            pass
        m = _re.search(r'"archetype_id"\s*:\s*"([a-z0-9_]+)"', result)
        if not m:
            continue
        archetype_id = m.group(1)
        candidates = list(
            _Path("skills_library/ppt/archetypes").glob(f"{archetype_id}.json")
        )
        for path in candidates:
            try:
                data = _json.loads(path.read_text())
                target = data.get("suggested_slides") or data.get("actual_slide_count")
                if target:
                    return int(target)
            except Exception:
                continue

    # 2. Fall back to deck-plan.json if save_presentation already ran.
    save_calls = [inv for inv in invocations
                  if inv.tool_name == "save_presentation" and not inv.error]
    for inv in reversed(save_calls):
        args = inv.arguments if isinstance(inv.arguments, dict) else {}
        out_path = args.get("output_path") or ""
        if not out_path:
            continue
        plan_path = _Path(out_path).parent / "deck-plan.json"
        if not plan_path.exists():
            continue
        try:
            data = _json.loads(plan_path.read_text())
            target = data.get("slides_target") or data.get("requested_slides_target")
            if target:
                return int(target)
            slides = data.get("slides") or []
            if slides:
                return len(slides)
        except Exception:
            continue
    return None

_VISUAL_QA_PROMPT = """\
You are a strict PowerPoint slide design critic with high aesthetic standards. Evaluate this slide:

Expected content: {title}
{body}
Theme: {theme}
Shape layout info: {shape_info}

Check these criteria IN ORDER. Stop at the first SERIOUS issue:

1. OVERLAP/CLIPPING (SERIOUS): Any text cut off at slide edges? Shapes covering text? Elements extending beyond canvas?
2. EMPTY/SPARSE (SERIOUS): Cards or panels with >50% empty space? Title-only slide with no content? Content zone mostly blank?
3. CONTENT DENSITY (SERIOUS): Every card/panel must be filled with real content (title + 2-5 lines). Cards with just a title and blank space = ISSUE.
4. TEXT READABILITY (SERIOUS): Text too small (<9pt), low contrast, or obscured?
5. VISUAL FLATNESS (SERIOUS): Are cards just plain white rectangles with thin colored strips? Cards should have VISIBLE gradient header bands (≥0.3in tall with noticeable color shift), drop shadows, and at least one technique (gradient, icon, metric callout). A slide with only white cards + barely-visible 1px accent lines = ISSUE: visually flat.
6. INVISIBLE GRADIENTS (MODERATE): Check if gradient fills are actually visible. A gradient from rgb(248,248,255) to rgb(255,255,255) is invisible — the stop colors must differ by ≥30 RGB units to be perceptible. Near-white-to-white gradients are the same as no gradient.
7. ALIGNMENT (MODERATE): Are similar elements (cards, metrics) aligned on a grid? Equal widths? Consistent spacing? Misaligned elements look amateur.
8. CONTENT-VISUAL FIT (MODERATE): Does the layout match the content type? A comparison should use a grid/table, not a radial diagram. A timeline should be linear, not scattered.

Reply "PASS" if no serious issues and the slide has visible visual richness in its cards/panels.
Reply "ISSUE: [specific problem]" for serious problems.
Reply "SUGGEST: [improvement]" for moderate issues.

Be strict about empty cards AND visually flat slides — both are common AI-generated deck problems."""

_SKILL_CLONE_QA_PROMPT = """\
A slide was generated by cloning a skill template into a presentation deck.
Skill clones commonly produce broken output. Be STRICT — check for these failures:

Expected content: {title}
{body}
Deck theme: {theme}

1. PLACEHOLDER RESIDUE: Does the slide show generic filler text like "Text Here",
   "Title", "Your Text", Chinese placeholder text (标题, 副标题, 会议主题),
   "Lorem ipsum", or any text that clearly does NOT match the expected content?
   → ISSUE: placeholder text not replaced

2. CONTENT MISMATCH: The expected content is shown above. Does the slide actually
   display this content (or a reasonable version of it)? If the slide shows completely
   different text, unrelated content, or is mostly empty with no readable text matching
   the topic → ISSUE: content not injected

3. VISUAL COMPLETENESS: Does the slide look like a finished, polished design?
   Or does it look like a broken template — missing images, half-rendered graphics,
   large empty areas with just a few decorative shapes, or elements obviously clipped
   by the slide edges? → ISSUE: incomplete or broken template

4. THEME MATCH: The deck uses a {theme} theme. Does this slide match?
   A dark slide in a light deck, or vice versa → ISSUE: theme mismatch

Reply "PASS" ONLY if ALL four checks pass.
Otherwise reply "ISSUE: [specific problem]". Be strict.
"""


def _call_vision_llm(b64_png: str, title: str, body: str, theme: str = "dark",
                     skill_clone: bool = False, shape_info: str = "") -> str:
    """Call GPT-5.4 vision to evaluate a rendered slide."""
    try:
        from core.llm import call_azure_openai
    except ImportError:
        return ""

    if skill_clone:
        prompt = _SKILL_CLONE_QA_PROMPT.format(
            title=title[:80], body=body[:200], theme=theme or "unknown"
        )
    else:
        prompt = _VISUAL_QA_PROMPT.format(
            title=title[:60], body=body[:120], theme=theme or "unknown",
            shape_info=shape_info[:500] if shape_info else "(not available)"
        )

    messages = [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_png}"}},
    ]}]

    try:
        resp = call_azure_openai(messages, model="gpt-5.4", reasoning_effort="medium")
        return resp.get("content", "")
    except Exception as e:
        log.warning("Vision QA failed: %s", e)
        return ""


def _detect_theme_from_code(code: str) -> str | None:
    """Detect light/dark theme from background color in slide code."""
    bg_match = re.search(
        r'(?:background|bg|BG|SLIDE_BG|bg_color|BG_COLOR|slide_bg).*?(?:RGBColor|rgb)\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)',
        code, re.DOTALL | re.IGNORECASE,
    )
    if bg_match:
        r, g, b = int(bg_match.group(1)), int(bg_match.group(2)), int(bg_match.group(3))
        luminance = (r * 0.299 + g * 0.587 + b * 0.114) / 255
        return "light" if luminance > 0.5 else "dark"
    fill_match = re.search(
        r'fore_color\.rgb\s*=\s*(?:RGBColor|rgb)\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)',
        code, re.IGNORECASE,
    )
    if fill_match:
        r, g, b = int(fill_match.group(1)), int(fill_match.group(2)), int(fill_match.group(3))
        luminance = (r * 0.299 + g * 0.587 + b * 0.114) / 255
        if luminance < 0.15 or luminance > 0.75:
            return "light" if luminance > 0.5 else "dark"
    return None


def _check_layout_zones(code: str) -> str | None:
    """Static analysis: check if any shape positions violate layout zone boundaries.

    Returns a warning string if violations found, None otherwise.
    """
    violations = []

    # Match Inches() calls for positioning: left, top, width, height
    # Common patterns:
    #   add_shape(..., Inches(x), Inches(y), Inches(w), Inches(h))
    #   add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    #   .left = Inches(x)  /  .top = Inches(y)

    # Find all textbox/shape additions with 4 Inches args (left, top, width, height)
    shape_pattern = re.compile(
        r'(?:add_(?:shape|textbox))\s*\([^)]*?'
        r'Inches\(\s*([\d.]+)\s*\)\s*,\s*Inches\(\s*([\d.]+)\s*\)\s*,\s*'
        r'Inches\(\s*([\d.]+)\s*\)\s*,\s*Inches\(\s*([\d.]+)\s*\)',
        re.DOTALL,
    )

    for m in shape_pattern.finditer(code):
        try:
            left, top, width, height = (
                float(m.group(1)), float(m.group(2)),
                float(m.group(3)), float(m.group(4)),
            )
        except ValueError:
            continue

        bottom = top + height
        right = left + width

        # Skip full-bleed / full-width shapes:
        # - Background shapes spanning most of the canvas (decorative)
        # - Full-width bars (footers, accent strips, dividers) — width >= 12in
        if width >= 12.0:
            continue

        # Check right edge
        if right > _RIGHT_EDGE + 0.1:  # small tolerance
            violations.append(
                f"Shape at x={left:.1f} w={width:.1f} extends to {right:.1f}in "
                f"(max {_RIGHT_EDGE}in)"
            )

        # Check bottom edge
        if bottom > _CANVAS_HEIGHT + 0.05:
            violations.append(
                f"Shape at y={top:.1f} h={height:.1f} extends to {bottom:.1f}in "
                f"(canvas height {_CANVAS_HEIGHT}in)"
            )

        # Check left margin (except footer bars starting at x=0)
        if left < _LEFT_MARGIN - 0.1 and width < 12.0:
            violations.append(
                f"Shape at x={left:.1f}in violates left margin ({_LEFT_MARGIN}in)"
            )

        # Check negative positions
        if left < -0.01 and width < 12.0:
            violations.append(f"Shape has negative left={left:.2f}in")
        if top < -0.01:
            violations.append(f"Shape has negative top={top:.2f}in")

    # Also check for textboxes with bare 0 as left position (common section divider bug)
    textbox_bare_zero = re.compile(
        r'add_textbox\s*\(\s*(?:Inches\(\s*0(?:\.0*)?\s*\)|0)\s*,',
    )
    if textbox_bare_zero.search(code):
        violations.append(
            "Textbox starts at x=0 — text will be clipped at the left slide edge. "
            "Use x >= Inches(0.7) for all text elements."
        )

    if violations:
        return (
            "LAYOUT ZONE VIOLATIONS detected in code:\n"
            + "\n".join(f"  - {v}" for v in violations[:3])
            + "\nFix: adjust positions to stay within layout zones "
            "(left≥0.5in, right≤12.83in, bottom≤7.5in)."
        )
    return None


def _check_title_wrap(code: str) -> str | None:
    """Static lint: detect titles that will wrap badly or contain manual '\\n'.

    Triggers when:
    - A textbox with width W contains large-font text (>=22pt) and the text is
      longer than W * 2.4 chars (rough ratio for bold 28pt), OR
    - A text assignment with font.size >= Pt(22) contains a manual '\\n'.
    """
    warnings = []

    # Find textbox creations, capture the following assignments block up to next blank/shape op.
    # Pattern matches: name=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))...
    tbox_re = re.compile(
        r'([A-Za-z_]\w*)\s*=\s*slide\.shapes\.add_textbox\s*\(\s*'
        r'Inches\([^)]+\)\s*,\s*Inches\([^)]+\)\s*,\s*'
        r'Inches\(\s*([\d.]+)\s*\)\s*,\s*Inches\(\s*[\d.]+\s*\)',
    )
    text_re = re.compile(r"\.text\s*=\s*(['\"])(.*?)\1", re.DOTALL)
    size_re = re.compile(r"font\.size\s*=\s*Pt\(\s*(\d+(?:\.\d+)?)\s*\)")

    for m in tbox_re.finditer(code):
        name = m.group(1)
        try:
            width = float(m.group(2))
        except ValueError:
            continue
        # Look at the next 800 chars for this textbox's config
        segment = code[m.end(): m.end() + 800]
        # Stop at the next textbox/shape definition referencing a different var
        seg_end = re.search(r'\n[A-Za-z_]\w*\s*=\s*slide\.shapes\.add_', segment)
        if seg_end:
            segment = segment[:seg_end.start()]

        texts = [t.group(2) for t in text_re.finditer(segment)]
        sizes = [float(s.group(1)) for s in size_re.finditer(segment)]
        if not texts or not sizes:
            continue
        max_size = max(sizes)
        if max_size < 22:
            continue
        first_text = texts[0]

        # Manual \n in large-font text (only titles usually have \n that way)
        if '\\n' in first_text and max_size >= 24 and len(first_text.replace('\\n', ' ')) <= 80:
            warnings.append(
                f"textbox '{name}' title has manual '\\n' with {max_size:.0f}pt font — "
                f"remove the \\n; let PowerPoint wrap naturally (or widen the box)."
            )

        # Width vs character load. Rough char budget: width_in * (170 / font_pt) bold chars/line
        # (calibrated against python-pptx + LibreOffice rendering, default font families)
        longest_line = max((s for s in first_text.split('\\n')), key=len, default=first_text)
        char_budget = width * (170.0 / max_size)
        if len(longest_line) > char_budget * 1.05:
            warnings.append(
                f"textbox '{name}' width={width:.1f}in too narrow for '{longest_line[:40]}...' "
                f"at {max_size:.0f}pt (fits ~{int(char_budget)} chars/line; "
                f"have {len(longest_line)}). Widen to >= {len(longest_line) * max_size / 170:.1f}in "
                f"or reduce font."
            )

    if warnings:
        return (
            "TEXT WRAP ISSUES (will cause ugly line breaks):\n"
            + "\n".join(f"  - {w}" for w in warnings[:3])
            + "\nFix before the next tool call."
        )
    return None


def _record_skill_failure(skill_id: str, category: str) -> str:
    """Record a skill failure and suggest an alternative if available."""
    if category not in _skill_failures:
        _skill_failures[category] = []
    if skill_id not in _skill_failures[category]:
        _skill_failures[category].append(skill_id)

    n_failures = len(_skill_failures[category])
    failed_ids = ", ".join(_skill_failures[category])

    if n_failures >= 2:
        return (
            f"2+ skills from category '{category}' have failed ({failed_ids}). "
            f"Try listing OTHER skills from this category with "
            f"`list-skills category={category}` and pick one you haven't tried. "
            f"Avoid these failed IDs: {failed_ids}"
        )
    return ""


async def progress_check(mcp, invocations, iteration):
    """Block premature TASK_COMPLETE and check visual quality.

    Target slide count is read from ``demo/<deck>/deck-plan.json`` (written by
    ``save_presentation``) or from the archetype's ``suggested_slides`` when
    available. There is no hard-coded 15-slide target — a 6-page deck on a
    6-page archetype completes cleanly.
    """
    save_calls = [inv for inv in invocations if inv.tool_name == "save_presentation"]
    successful_saves = [inv for inv in save_calls
                        if inv.result and "Saved" in inv.result and not inv.error]

    slide_adds = [inv for inv in invocations
                  if inv.tool_name in ("add_slide_from_shell", "add_slide",
                                       "add_slide_from_skill", "replace_slide")
                  and not inv.error]
    slide_deletes = [inv for inv in invocations
                     if inv.tool_name == "delete_slide" and not inv.error]
    effective_slide_count = max(0, len(slide_adds) - len(slide_deletes))

    target_slides = _infer_target_slide_count(invocations)

    if successful_saves:
        import re as _re
        last_save = successful_saves[-1].result or ""
        m = _re.search(r"Saved (\d+)-slide", last_save)
        actual_slides = int(m.group(1)) if m else effective_slide_count
        if target_slides and actual_slides < target_slides:
            return (
                f"BLOCKING: Presentation has only {actual_slides} slides — "
                f"archetype target is {target_slides}. You MUST NOT say "
                f"TASK_COMPLETE. Add {target_slides - actual_slides} more "
                "slides and call save_presentation again."
            )
        return (
            f"Presentation saved successfully ({actual_slides} slides). "
            "You may say TASK_COMPLETE."
        )

    if not slide_adds:
        return (
            "WARNING: NO slides added yet — you are still in the planning "
            "phase. Do NOT say TASK_COMPLETE. Proceed to building slides "
            "with add_slide_from_shell (v2 path)."
        )

    # V1-only quality checks have been retired. The v2 pipeline enforces
    # motion-budget, morph-lint, contrast, and overlap gates at save time
    # (see core/extraction/quality_gate.py and
    # domains/ppt/mcp_server/server.py:save_presentation), so we no longer
    # emit add_slide-centric heuristic warnings. Back-compat: if a
    # long-running session somehow still uses v1 tools, it will just skip
    # the below and fall through to the base warning.
    quality_warning = ""
    _ = iteration  # retained for signature stability; no longer used here.

    return (
        f"WARNING: save_presentation has NOT been called yet. "
            f"{effective_slide_count} current slides estimated "
            f"({len(slide_adds)} added, {len(slide_deletes)} deleted)"
        + (f" (archetype target: {target_slides})." if target_slides
           else " — no archetype target yet.")
        + " Do NOT say TASK_COMPLETE. Keep building with add_slide_from_shell, "
        "then call save_presentation."
        + quality_warning
    )


async def auto_verify(tool_name, tool_args, result_text, mcp):
    """Auto-verify after slide operations with visual QA."""
    global _current_theme

    if tool_name not in ("add_slide", "add_slide_from_skill", "replace_slide",
                         "add_slide_from_shell"):
        return None

    if "Error" in result_text:
        # Track skill failures by category for fallback suggestions
        if tool_name == "add_slide_from_skill":
            skill_id = tool_args.get("skill_id", "")
            category = tool_args.get("style_hints", "").split()[0] if tool_args.get("style_hints") else ""
            if skill_id and category:
                extra = _record_skill_failure(skill_id, category)
                if extra:
                    return f"The last {tool_name} call failed. {extra}"
        return f"The last {tool_name} call failed. Try a different approach."

    if re.search(r"\b0 shapes\b", result_text):
        return (
            "Warning: slide has 0 shapes (empty). Delete it and re-add with "
            "add_slide_from_shell passing the correct slots."
        )

    # --- Replace cap: max N replaces per slide ---
    match = re.search(r"(?:Added|Replaced) slide (\d+)", result_text)
    if not match:
        return None
    slide_idx = int(match.group(1))

    if tool_name == "replace_slide":
        _replace_counts[slide_idx] = _replace_counts.get(slide_idx, 0) + 1
        total_replaces = sum(_replace_counts.values())
        if total_replaces > _MAX_REPLACES_PER_DECK:
            log.info("Deck replace budget reached (%d total), auto-PASS",
                     total_replaces)
            return (
                f"Deck-level replace budget reached ({total_replaces}/{_MAX_REPLACES_PER_DECK}). "
                "Stop replacing and build remaining slides via add_slide_from_shell. "
                "Visual imperfections are acceptable; finishing the deck is not."
            )
        if _replace_counts[slide_idx] > _MAX_REPLACES_PER_SLIDE:
            log.info("Replace cap reached for slide %d (%d replaces), auto-PASS",
                     slide_idx, _replace_counts[slide_idx])
            return (
                f"Slide {slide_idx} has been replaced {_replace_counts[slide_idx]} times "
                f"(max {_MAX_REPLACES_PER_SLIDE}). MOVE ON to the next slide. "
                "Do not replace this slide again."
            )

    prs_id = tool_args.get("prs_id")
    if not prs_id:
        return None

    if _MAX_REPLACES_PER_SLIDE <= 0 and tool_name == "add_slide_from_shell":
        # Main experiment mode: do not spend extra render/VLM cycles on
        # advisory slide critique when no automatic rebuild is allowed.
        return None

    # --- Layout zone static check (for add_slide / replace_slide code) ---
    if tool_name in ("add_slide", "replace_slide"):
        code = tool_args.get("code", "")
        zone_warning = _check_layout_zones(code)
        if zone_warning:
            log.warning("Layout zone violation on slide %d: %s", slide_idx, zone_warning[:200])
            return (
                f"LAYOUT VIOLATION on slide {slide_idx}:\n{zone_warning}\n"
                "Regenerate the slide via add_slide_from_shell with corrected slot values positions within the layout zones."
            )
        wrap_warning = _check_title_wrap(code)
        if wrap_warning:
            current_replaces = _replace_counts.get(slide_idx, 0)
            if current_replaces < _MAX_REPLACES_PER_SLIDE:
                log.warning("Title wrap issue on slide %d: %s", slide_idx, wrap_warning[:200])
                return (
                    f"Slide {slide_idx} — {wrap_warning}\n"
                    f"Rebuild the slide via add_slide_from_shell with adjusted slot values to widen the textbox or shrink the font. "
                    f"You have {_MAX_REPLACES_PER_SLIDE - current_replaces} replace(s) left."
                )

    # Detect server-side WARNING from skill clone quality check
    is_skill_clone = tool_name == "add_slide_from_skill"
    has_server_warning = "WARNING:" in result_text

    if is_skill_clone and has_server_warning:
        skill_id = tool_args.get("skill_id", "")
        category = tool_args.get("style_hints", "").split()[0] if tool_args.get("style_hints") else ""

        fallback_msg = ""
        if skill_id and category:
            fallback_msg = _record_skill_failure(skill_id, category)

        warning_detail = result_text.split("WARNING:")[-1].strip()
        msg = (
            f"Skill clone produced a BROKEN slide {slide_idx}: {warning_detail}\n"
            f"You MUST rebuild this slide via add_slide_from_shell using custom python-pptx code."
        )
        if fallback_msg:
            msg += f"\n{fallback_msg}"
        log.warning("Skill clone WARNING for slide %d: %s", slide_idx, warning_detail[:200])
        return msg

    # Auto-detect theme from code
    if tool_name == "add_slide":
        code = tool_args.get("code", "")
        detected = _detect_theme_from_code(code)
        if detected:
            _current_theme = detected
        # Track skill provenance — agent is instructed to add `# from skill: <id>`
        # comments when borrowing helpers. Count how many slides actually do so.
        if re.search(r"#\s*from\s+skill\s*:", code, re.IGNORECASE):
            _skill_ref_slides.add(slide_idx)

    # Detect theme from palette parameter
    if is_skill_clone:
        palette_arg = tool_args.get("palette", "")
        if palette_arg and palette_arg != "none":
            try:
                pal = json.loads(palette_arg)
                bg = pal.get("dark_bg", [0, 0, 0])
                lum = (bg[0] * 0.299 + bg[1] * 0.587 + bg[2] * 0.114) / 255
                _current_theme = "light" if lum > 0.5 else "dark"
            except (ValueError, TypeError, KeyError):
                pass

    # Skill diversity
    if is_skill_clone:
        skill_id = tool_args.get("skill_id", "")
        if skill_id and skill_id in _used_skills:
            return f"Note: skill '{skill_id}' already used. Pick a different one."
        if skill_id:
            _used_skills.add(skill_id)

    # Shape count check + collect shape info for VLM
    shapes = 0
    shape_info_text = ""
    overlap_lines = []
    try:
        info = await mcp.call_tool("get_slide_info", {"prs_id": prs_id, "slide_index": slide_idx})
        shape_info_text = info or ""
        shape_match = re.search(r"(\d+) shapes", info)
        shapes = int(shape_match.group(1)) if shape_match else 0
        if shapes == 0:
            return (
                f"Warning: slide {slide_idx} appears empty. Do not delete or "
                "rebuild the deck loop; continue building the remaining slides "
                "and rely on save_presentation to enforce completion."
            )
        # Parse OVERLAPS section from get_slide_info
        if "OVERLAPS:" in info:
            tail = info.split("OVERLAPS:", 1)[1]
            overlap_lines = [ln.strip() for ln in tail.splitlines() if ln.strip()]
    except Exception:
        pass

    # Deterministic overlap gate — if bbox collisions detected, return fix directive
    # before spending a vision call. Agent sees exact coordinates, not vague prose.
    if overlap_lines:
        current_replaces = _replace_counts.get(slide_idx, 0)
        if current_replaces < _MAX_REPLACES_PER_SLIDE:
            log.warning("BBox overlap detected on slide %d: %d issue(s)", slide_idx, len(overlap_lines))
            issue_block = "\n  ".join(overlap_lines[:6])
            return (
                f"Slide {slide_idx} has geometric overlaps (deterministic bbox check):\n"
                f"  {issue_block}\n"
                f"FIX by rebuilding via add_slide_from_shell. Keep content identical but adjust coordinates:\n"
                f"  - Shrink or move the listed shapes so intersection < 25% of the smaller shape\n"
                f"  - Text shapes must not overlap other text shapes or accent bands\n"
                f"  - Out-of-bounds shapes: clamp to 0.4 <= x, x+w <= 12.9, 0.3 <= y, y+h <= 7.2\n"
                f"You have {_MAX_REPLACES_PER_SLIDE - current_replaces} replace(s) left for this slide."
            )

    # Detect complex layouts that MUST be rendered (never skip)
    code = tool_args.get("code", "") if tool_name in ("add_slide", "replace_slide") else ""
    is_complex_layout = any(kw in code.lower() for kw in [
        "math.cos", "math.sin", "freeformbuilder", "freeform", "begin(",
        "add_picture", "add_connector",
    ])

    # Visual QA via render — sampling strategy to save iterations:
    # ALWAYS render: skill clones, replace_slide, complex layouts (high-risk)
    # Sample every other: simple add_slide with >8 shapes (low-risk)
    global _slide_add_count
    skip_render = False
    if tool_name == "add_slide" and shapes >= 8 and not is_complex_layout:
        _slide_add_count += 1
        if _slide_add_count % 2 == 0:
            skip_render = True
            log.info("Skipping render QA for slide %d (sampling: %d shapes, low risk)",
                     slide_idx, shapes)

    if skip_render:
        return None

    # Visual QA via render
    try:
        render_result = await mcp.call_tool("render_slide", {"prs_id": prs_id, "slide_index": slide_idx})
        if not render_result or "Error" in render_result:
            return None

        b64_match = re.search(r"base64,(.+)", render_result)
        if not b64_match:
            return None

        # Extract expected content — ONLY from content_brief, never from code
        content_brief = tool_args.get("content_brief", "")
        if not content_brief and tool_name in ("add_slide", "replace_slide"):
            code = tool_args.get("code", "")
            title_match = re.search(r"\.text\s*=\s*['\"]([^'\"]{3,50})['\"]", code)
            content_brief = title_match.group(1) if title_match else ""
        lines = content_brief.strip().split("\n") if content_brief else []
        title = lines[0] if lines else "(slide content)"
        body = "\n".join(lines[1:3]) if len(lines) > 1 else ""

        # Use stricter QA prompt for skill clones
        qa_result = _call_vision_llm(
            b64_match.group(1), title, body,
            theme=_current_theme,
            skill_clone=is_skill_clone,
            shape_info=shape_info_text,
        )
        if not qa_result:
            return None

        if "pass" in qa_result.lower()[:15]:
            log.info("Visual QA PASS for slide %d", slide_idx)
            return None

        # For skill clones, any non-PASS is treated as failure
        if is_skill_clone:
            skill_id = tool_args.get("skill_id", "")
            category = tool_args.get("style_hints", "").split()[0] if tool_args.get("style_hints") else ""
            fallback_msg = ""
            if skill_id and category:
                fallback_msg = _record_skill_failure(skill_id, category)

            msg = (
                f"Visual QA FAILED for skill-cloned slide {slide_idx}: {qa_result}\n"
                f"You MUST rebuild this slide via add_slide_from_shell using custom python-pptx code."
            )
            if fallback_msg:
                msg += f"\nAlternatively: {fallback_msg}"
            log.warning("Skill clone QA ISSUE for slide %d: %s", slide_idx, qa_result[:200])
            return msg

        # Check replace budget before suggesting a fix
        current_replaces = _replace_counts.get(slide_idx, 0)
        if current_replaces >= _MAX_REPLACES_PER_SLIDE:
            log.info("Visual QA found issue on slide %d but replace cap reached, skipping",
                     slide_idx)
            return None  # Don't suggest more replaces — move on

        # Handle both ISSUE and SUGGEST for non-skill slides
        if "suggest" in qa_result.lower()[:15]:
            log.info("Visual QA SUGGEST for slide %d: %s", slide_idx, qa_result[:200])
            return f"Visual QA suggestion for slide {slide_idx}: {qa_result}\nConsider improving by rebuilding via add_slide_from_shell (you have {_MAX_REPLACES_PER_SLIDE - current_replaces} replace(s) left for this slide)."

        log.warning("Visual QA ISSUE for slide %d: %s", slide_idx, qa_result[:200])
        # Give specific fix guidance for overlap issues
        qa_lower = qa_result.lower()
        if "overlap" in qa_lower or "clipping" in qa_lower or "edge" in qa_lower or "cropped" in qa_lower:
            return (
                f"Visual QA OVERLAP issue on slide {slide_idx}: {qa_result}\n"
                "FIX: rebuild via add_slide_from_shell — keep the same layout but:\n"
                "  1. Shorten any long text (truncate or use fewer words)\n"
                "  2. Reduce font size by 2-4pt on crowded elements\n"
                "  3. Move shapes inward (margin >= 0.5in from all edges)\n"
                "  4. Ensure all shapes stay within layout zones (content y: 1.2-6.6in)\n"
                f"You have {_MAX_REPLACES_PER_SLIDE - current_replaces} replace(s) left for this slide."
            )
        return (
            f"Visual QA for slide {slide_idx}: {qa_result}\n"
            f"Regenerate the slide via add_slide_from_shell with corrected slot values ({_MAX_REPLACES_PER_SLIDE - current_replaces} replace(s) left)."
        )
    except Exception as e:
        log.warning("Visual QA error: %s", e)
        return None
