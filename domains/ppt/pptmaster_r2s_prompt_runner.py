#!/usr/bin/env python3
"""Prompt-specific PPTMaster x Resource2Skill reference runner.

This is a small executable reference path for the integration contract:

- PPTMaster remains the SVG-first/export backend and open visual planner.
- Without R2S, prompts still produce domain-specific SVG decks.
- With R2S, selected skill IDs add extra visual mechanisms on top of the open
  PPTMaster plan rather than replacing it with a fixed skeleton.

The runner is deterministic and deliberately lightweight. It is not a
replacement for the LLM agent path; it is a regression harness that proves the
PPTMaster backend can be guided by prompt-specific R2S references without
collapsing into a single template.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

UTC = timezone.utc  # py3.10 compatibility (datetime.UTC is 3.11+)


ROOT = Path(__file__).resolve().parents[2]
SERVER_DIR = Path(__file__).resolve().parent / "mcp_server"
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

import pptmaster_engine  # noqa: E402


SVG_W = 1280
SVG_H = 720


@dataclass(frozen=True)
class Palette:
    bg: str
    ink: str
    muted: str
    primary: str
    accent: str
    surface: str


PALETTES: dict[str, Palette] = {
    "kids": Palette("#FFF7ED", "#24120A", "#7C4A22", "#EA580C", "#22C55E", "#FFFFFF"),
    "restaurant": Palette("#FFFBEB", "#23180D", "#7A4B16", "#D97706", "#84CC16", "#FFF7D6"),
    "real_estate": Palette("#FFF7ED", "#21170F", "#7C4A22", "#B45309", "#0F766E", "#FFFFFF"),
    "financial": Palette("#0F172A", "#F8FAFC", "#CBD5E1", "#FBBF24", "#64748B", "#1E293B"),
    "legal": Palette("#F8F5F0", "#111111", "#4B5563", "#B45309", "#374151", "#FFFFFF"),
    "research": Palette("#111022", "#F8FAFC", "#CBD5E1", "#7C3AED", "#22D3EE", "#1F1B3D"),
    "fintech": Palette("#071923", "#F8FAFC", "#BFE9F2", "#0891B2", "#A855F7", "#0B2A34"),
    "esports": Palette("#100A1C", "#F8FAFC", "#FBCFE8", "#DB2777", "#06B6D4", "#24113A"),
    "nonprofit": Palette("#F5FAF9", "#0F1D1C", "#356B67", "#0F766E", "#F97316", "#FFFFFF"),
    "healthtech": Palette("#F5FAF9", "#0F1D1C", "#46615E", "#0F766E", "#E11D48", "#FFFFFF"),
    "creative": Palette("#111827", "#F8FAFC", "#CBD5E1", "#2563EB", "#F59E0B", "#1F2937"),
    "product": Palette("#0B1220", "#F8FAFC", "#DDE7F0", "#2563EB", "#F59E0B", "#111827"),
    "generic": Palette("#F8FAFC", "#0F172A", "#475569", "#2563EB", "#F59E0B", "#FFFFFF"),
}


DOMAIN_QUERY_HINTS: dict[str, str] = {
    "kids": "playful diagram classroom lesson illustrated process",
    "restaurant": "restaurant food menu editorial warm map pitch",
    "real_estate": "property real estate gallery map cinematic editorial",
    "financial": "financial boardroom data dashboard table risk executive",
    "legal": "legal boardroom risk matrix table restrained executive",
    "research": "research academic method pipeline evidence architecture",
    "fintech": "fintech investor data dashboard technical network",
    "esports": "esports roster neon cinematic team bold metric",
    "nonprofit": "nonprofit donor impact story warm editorial metrics",
    "healthtech": "clinical medical device dashboard evidence timeline",
    "creative": "creative agency brand editorial cinematic collage",
    "product": "product launch SaaS feature grid comparison hero metric cinematic",
    "generic": "presentation layout visual infographic dashboard",
}


ROLE_SEQUENCES: dict[str, list[str]] = {
    "kids": [
        "playful_cover",
        "labeled_diagram",
        "sideways_process",
        "giant_fun_metric",
        "comparison_lab",
        "sensor_cards",
        "safety_checklist",
        "draw_activity",
        "memory_close",
    ],
    "restaurant": [
        "editorial_cover",
        "menu_board",
        "neighborhood_scene",
        "sourcing_map",
        "unit_economics",
        "buildout_timeline",
        "risk_matrix",
        "launch_calendar",
        "founder_cards",
        "ask_close",
    ],
    "real_estate": [
        "property_cover",
        "gallery_wall",
        "factsheet",
        "site_map",
        "materials_grid",
        "systems_table",
        "comps_chart",
        "pricing_strategy",
        "showing_timeline",
        "agent_close",
    ],
    "financial": [
        "board_cover",
        "executive_snapshot",
        "kpi_dashboard",
        "variance_table",
        "cohort_flow",
        "risk_register",
        "decision_matrix",
        "q4_roadmap",
        "approval_close",
    ],
    "legal": [
        "board_cover",
        "practice_mix_table",
        "partner_metrics",
        "originations_matrix",
        "risk_register",
        "talent_pipeline",
        "vote_matrix",
        "strategic_roadmap",
        "decision_close",
    ],
    "research": [
        "research_cover",
        "motivation_split",
        "method_pipeline",
        "system_architecture",
        "evidence_matrix",
        "results_dashboard",
        "limitations",
        "related_work_map",
        "future_work",
        "research_close",
    ],
    "fintech": [
        "investor_cover",
        "market_gap_split",
        "network_architecture",
        "settlement_dashboard",
        "customer_win",
        "moat_comparison",
        "business_model_table",
        "roadmap",
        "capital_ask",
    ],
    "esports": [
        "cinematic_cover",
        "roster_wheel",
        "game_portfolio",
        "audience_dashboard",
        "sponsor_ladder",
        "facility_map",
        "academy_pipeline",
        "unit_economics",
        "series_close",
    ],
    "nonprofit": [
        "impact_cover",
        "story_quote",
        "reach_dashboard",
        "program_map",
        "dollar_flow",
        "volunteer_wall",
        "partnership_timeline",
        "next_year_goals",
        "donor_close",
    ],
    "healthtech": [
        "clinical_cover",
        "device_profile",
        "study_dashboard",
        "predicate_comparison",
        "adverse_events_table",
        "manufacturing_readiness",
        "cybersecurity_stack",
        "regulatory_timeline",
        "board_ask",
    ],
    "creative": [
        "brand_cover",
        "diagnosis_collage",
        "customer_voice",
        "territory_moodboard",
        "competitive_map",
        "packaging_gallery",
        "digital_experience",
        "rollout_plan",
        "pricing_close",
    ],
    "product": [
        "product_cover",
        "hero_metric",
        "problem_solution_split",
        "feature_grid",
        "before_after",
        "pricing_matrix",
        "customer_logo_wall",
        "security_stack",
        "install_cta",
        "launch_close",
    ],
    "generic": [
        "cover",
        "snapshot",
        "cards",
        "dashboard",
        "comparison",
        "timeline",
        "close",
    ],
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("briefs", nargs="*", type=Path, help="Brief JSON files to run")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("demo/pptmaster_r2s_prompt_specific") / datetime.now(UTC).strftime("%Y%m%d_%H%M%S"),
        help="Output root",
    )
    parser.add_argument("--mode", default="both", choices=["w", "wo", "both"], help="Run with R2S, without R2S, or both")
    parser.add_argument("--max-slides", type=int, default=12, help="Safety cap for generated slides")
    parser.add_argument("--no-export", action="store_true", help="Skip PPTX export and only write SVG projects")
    args = parser.parse_args(argv)

    brief_paths = args.briefs or _default_briefs()
    skill_entries = _load_skill_entries()
    args.out.mkdir(parents=True, exist_ok=True)

    summary: list[dict[str, Any]] = []
    for brief_path in brief_paths:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
        modes = ["wo", "w"] if args.mode == "both" else [args.mode]
        for mode in modes:
            entry = build_deck(
                brief=brief,
                brief_path=brief_path,
                out_root=args.out,
                mode=mode,
                skill_entries=skill_entries,
                max_slides=args.max_slides,
                export=not args.no_export,
            )
            summary.append(entry)

    summary_path = args.out / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    report_path = args.out / "README.md"
    report_path.write_text(_summary_markdown(args.out, summary), encoding="utf-8")
    print(summary_path)
    return 0


# ---- Resource2Skill svg_recipe -> real slide rendering -------------------
# A selected PPT skill is *applied* by rendering its svg_recipe.md SVG as one
# slide (with this deck's text substituted in), not by a generic hash overlay.
# Body slides rendered directly from a skill svg_recipe under R2S (one distinct
# skill each). Cover (1) and close (last) stay the genuine PPT Master template, so
# the baseline is a real PPT Master deck — the with/without difference comes from
# R2S genuinely redesigning the content slides, not from degrading the baseline.
RECIPE_SLIDE_INDICES = (2, 3, 4, 5)


def _load_recipe_svg(skill_id: str) -> str | None:
    p = Path("skills_wiki/ppt") / skill_id / "svg_recipe.md"
    if not p.exists():
        return None
    m = re.search(r"```svg\s*(.*?)```", p.read_text(encoding="utf-8", errors="ignore"), re.S)
    if not m:
        return None
    svg = m.group(1).strip()
    if "<svg" not in svg or "</svg>" not in svg:
        return None
    return svg


def _recipe_distinctiveness(skill_id: str) -> int:
    svg = _load_recipe_svg(skill_id) or ""
    return sum(svg.count(tok) for tok in ("<filter", "clipPath", "<mask", "feGaussianBlur"))


def _recipe_svg_slide(skill_id: str, headline: str, supports: list[str]) -> str | None:
    """Render a skill's svg_recipe SVG as a full slide, substituting this deck's
    text into the recipe's most prominent <text> nodes. Returns None on failure so
    the caller can fall back to the open-plan template."""
    svg = _load_recipe_svg(skill_id)
    if not svg:
        return None
    # Recipes use placeholder <image href="https://images.example.com/..."> photos;
    # those can't load and break the SVG->PPTX export, so drop them (the skill's
    # actual mechanism — gradients, masks, filters, shapes, text — stays intact).
    svg = re.sub(r"<image\b[^>]*?/>", "", svg, flags=re.S)
    svg = re.sub(r"<image\b.*?</image>", "", svg, flags=re.S)
    texts = list(re.finditer(r"<text\b[^>]*>(.*?)</text>", svg, re.S))

    def _fsize(tag: str) -> float:
        m = re.search(r'font-size="?(\d+(?:\.\d+)?)', tag)
        return float(m.group(1)) if m else 0.0

    def _clean(inner: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", inner)).strip()

    def _fit(new: str, placeholder: str) -> str:
        # The recipe's placeholder text fit its box at this font-size, so use its
        # character count as the box capacity — keeps substituted copy from
        # overflowing the box and clipping (looks broken at showcase size).
        cap = max(len(placeholder) + 4, 18)
        new = new.strip()
        if len(new) <= cap:
            return new
        return new[: cap - 1].rstrip(" ,.;:-") + "…"

    repl: dict[int, str] = {}
    if texts:
        order = sorted(range(len(texts)), key=lambda i: _fsize(texts[i].group(0)), reverse=True)
        contents = [headline] + [s for s in (supports or []) if s]
        for rank, ti in enumerate(order):
            if rank < len(contents):
                repl[ti] = escape(_fit(contents[rank], _clean(texts[ti].group(1))))
    out: list[str] = []
    last = 0
    for i, m in enumerate(texts):
        out.append(svg[last:m.start(1)])
        out.append(repl[i] if i in repl else m.group(1))
        last = m.end(1)
    out.append(svg[last:])
    result = "".join(out)
    # Some authored recipes contain bare ampersands ("R&D", "Q&A") that aren't
    # valid XML; repair them so the SVG validator/exporter doesn't choke.
    result = re.sub(r"&(?!(?:#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);)", "&amp;", result)
    # Final guard: if a recipe is still malformed, fall back to the template slide
    # (return None) rather than crash the whole deck.
    try:
        ET.fromstring(result.encode("utf-8"))
    except ET.ParseError:
        return None
    return result


# Model used to author skill slides. SVG layout authoring needs more than the
# CLAUDE.md default "low"; medium is a justified override for layout quality.
LLM_SLIDE_MODEL = "gpt-5.4"
LLM_SLIDE_REASONING = "medium"


def _clean_llm_svg(text: str) -> str | None:
    """Extract + sanitise an SVG returned by the LLM. Returns None if unusable."""
    if not text:
        return None
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:svg|xml)?\s*", "", t)
        t = re.sub(r"\s*```$", "", t.strip())
    m = re.search(r"<svg\b.*?</svg>", t, re.S)
    if not m:
        return None
    svg = m.group(0)
    # Safety: no external images / foreignObject; repair bare ampersands.
    svg = re.sub(r"<image\b[^>]*?/>", "", svg, flags=re.S)
    svg = re.sub(r"<image\b.*?</image>", "", svg, flags=re.S)
    svg = re.sub(r"<foreignObject\b.*?</foreignObject>", "", svg, flags=re.S)
    svg = re.sub(r"&(?!(?:#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);)", "&amp;", svg)
    # Force the canvas to our size so the export lands at 1280x720.
    svg = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r"\1", svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\sheight="[^"]*"', r"\1", svg, count=1)
    if "viewBox" not in svg.split(">", 1)[0]:
        svg = svg.replace("<svg", f'<svg viewBox="0 0 {SVG_W} {SVG_H}"', 1)
    svg = svg.replace("<svg", f'<svg width="{SVG_W}" height="{SVG_H}"', 1)
    try:
        root = ET.fromstring(svg.encode("utf-8"))
    except ET.ParseError:
        return None
    if root.tag.split("}", 1)[-1].lower() != "svg":
        return None
    return svg


def _llm_skill_slide(
    *,
    skill_id: str,
    skill_name: str,
    applicability: str,
    headline: str,
    bullets: list[str],
    domain: str,
    palette: Palette,
    tone: str,
) -> str | None:
    """Author a slide that genuinely APPLIES a skill to this deck's content.

    The skill's `svg_recipe` is given to the model as a *design reference* (the
    visual approach: layout structure, palette, shapes, signature mechanism). The
    model must re-author a fresh 1280x720 SVG that lays out THIS slide's real
    content in that style — using only the provided text (no leaked example names/
    labels from the reference). Returns None on any failure so the caller can fall
    back to the deterministic recipe-fill / template path."""
    reference = _load_recipe_svg(skill_id)
    if not reference:
        return None
    if len(reference) > 6500:  # keep the prompt bounded; the head conveys structure
        reference = reference[:6500] + "\n<!-- …reference truncated… -->"

    import os
    import sys
    project_root = (
        os.environ.get("VWS_PROJECT_ROOT")
        or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        from core.llm import call_azure_openai  # type: ignore
    except Exception:
        return None
    os.environ.setdefault("AZURE_OPENAI_USE_AAD", "1")

    points = "\n".join(f"- {b.strip()}" for b in (bullets or []) if b and b.strip())
    system = (
        "You are an expert presentation designer who outputs RAW SVG only. "
        "You receive (1) a DESIGN REFERENCE — an example slide SVG demonstrating a "
        "distilled design skill — and (2) the ACTUAL CONTENT for one new slide. "
        "Produce a NEW 1280x720 SVG that applies the reference skill's visual "
        "APPROACH (its layout structure, composition, color treatment, shapes, and "
        "signature mechanism) to the ACTUAL CONTENT. "
        "CRITICAL: use ONLY the actual content's words. The reference's names, "
        "labels, numbers and captions are placeholders — never copy them. "
        "Every element must sit inside the 1280x720 canvas with >=56px margins and "
        "no text overflow (wrap or shorten). Output ONLY the SVG markup."
    )
    user = (
        f"SKILL: {skill_name or skill_id}\n"
        f"WHAT IT DOES: {(applicability or '').strip()[:400]}\n\n"
        f"DESIGN REFERENCE SVG (emulate the visual approach, NOT the text):\n"
        f"{reference}\n\n"
        f"ACTUAL CONTENT FOR THIS SLIDE:\n"
        f"  Headline: {headline.strip()}\n"
        f"  Supporting points:\n{points or '  (none)'}\n"
        f"  Domain/tone: {domain}; {tone}\n\n"
        f"HARD REQUIREMENTS:\n"
        f'- Root exactly: <svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" '
        f'height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}">\n'
        f"- Allowed elements: rect, circle, ellipse, line, polyline, polygon, path, "
        f"text, tspan, g, defs, linearGradient, radialGradient, stop, filter, "
        f"feGaussianBlur, feOffset, feMerge, feMergeNode, clipPath, mask.\n"
        f"- NO <image>, NO external URLs, NO foreignObject. Fonts: font-family=\"Arial\".\n"
        f"- Render the headline prominently and lay out the supporting points using "
        f"the skill's mechanism (e.g. hub / split-grid / dashboard / diagonal cards / "
        f"timeline). Keep all text inside its shapes.\n"
        f"- LAYOUT SAFETY (most important): shapes and their text must NOT overlap or "
        f"collide — leave clear spacing between every element. Do NOT place a large "
        f"central text block on top of other shapes. If the skill uses a central "
        f"hub/focus, the centre holds only a SHORT label (<=5 words, e.g. a title or "
        f"metric); the detailed points go in the surrounding elements.\n"
        f"- Be concise per element: trim each supporting point to a short phrase that "
        f"fits its box; never let a sentence spill outside its shape or off-canvas.\n"
        f"- The reference may show image/photo/mockup placeholders — you CANNOT use "
        f"images. Do NOT leave empty boxes or 'mockup'/'photo'/'image' labels: fill "
        f"every region with real content from this slide, or make it a solid "
        f"decorative colour block / shape. Replace any photo area with a bold colour "
        f"panel, an icon drawn from shapes, or a text card.\n"
        f"- Titles and headlines must fit FULLY inside their container — shrink the "
        f"font size so the whole title shows; never truncate or let text run past a "
        f"box edge. Do not duplicate the headline.\n"
        f"- Cohesive palette fitting a {domain} deck (you may reuse the reference's).\n"
        f"Output ONLY the SVG."
    )
    try:
        resp = call_azure_openai(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            model=LLM_SLIDE_MODEL,
            reasoning_effort=LLM_SLIDE_REASONING,
            max_completion_tokens=20000,
            timeout=240,
            max_retries=2,
            retry_delay=4.0,
        )
    except Exception:
        return None
    return _clean_llm_svg(resp.get("content") or "")


def build_deck(
    *,
    brief: dict[str, Any],
    brief_path: Path,
    out_root: Path,
    mode: str,
    skill_entries: list[dict[str, Any]],
    max_slides: int,
    export: bool,
) -> dict[str, Any]:
    case = str(brief.get("variant_id") or brief.get("out_dirname") or brief_path.stem)
    title = str(brief.get("title") or case.replace("_", " ").title())
    domain = infer_domain(brief)
    palette = PALETTES.get(domain, PALETTES["generic"])
    use_r2s = mode == "w"
    refs = select_skill_refs(brief, skill_entries, k=4) if use_r2s else []
    ref_details = _ref_details(refs, skill_entries)
    roles = _role_sequence(domain, brief, max_slides=max_slides)

    base_dir = out_root / case / mode
    project_meta = pptmaster_engine.create_project(f"{case}_{mode}", canvas_format="ppt169", base_dir=str(base_dir))
    project_path = Path(project_meta["project_path"])

    warnings: list[dict[str, Any]] = []
    shape_counts: list[int] = []
    layout_families: list[str] = []
    core_points = [str(x) for x in brief.get("core_points") or []]
    audience = str(brief.get("audience") or "")

    # Under R2S, the most distinctive selected skills are rendered as real slides
    # directly from their svg_recipe (the actual mechanism), not the open template.
    recipe_assign: dict[int, str] = {}
    if use_r2s and refs:
        distinct = sorted(refs, key=_recipe_distinctiveness, reverse=True)
        for j, sidx in enumerate(RECIPE_SLIDE_INDICES):
            recipe_assign[sidx] = distinct[j % len(distinct)]

    for idx, role in enumerate(roles, start=1):
        slide_ref = recipe_assign.get(idx) or (refs[(idx - 1) % len(refs)] if refs else "")
        point = core_points[(idx - 1) % len(core_points)] if core_points else title
        bullets = _points_for_slide(core_points, idx, count=4)
        layout_family = _layout_family(role, idx, len(roles))
        svg = None
        if idx in recipe_assign:
            sref = recipe_assign[idx]
            rd = ref_details.get(sref, {})
            # Primary: let the LLM genuinely APPLY the skill to this slide's real
            # content (authors a fresh SVG in the skill's style). Fallbacks:
            # deterministic recipe-fill, then the open template.
            if os.environ.get("PPT_LLM_SLIDES", "1") != "0":
                svg = _llm_skill_slide(
                    skill_id=sref,
                    skill_name=str(rd.get("name", "")),
                    applicability=str(rd.get("applicability", "")),
                    headline=point or title,
                    bullets=bullets,
                    domain=domain,
                    palette=palette,
                    tone=", ".join(str(t) for t in (brief.get("tone_words") or [])),
                )
                if svg is not None:
                    layout_family = "skill_llm"
            if svg is None:
                svg = _recipe_svg_slide(sref, point or title, bullets)
                if svg is not None:
                    layout_family = "skill_recipe"
        if svg is None:
            svg = render_slide(
                idx=idx,
                total=len(roles),
                role=role,
                title=title,
                audience=audience,
                point=point,
                bullets=bullets,
                domain=domain,
                palette=palette,
                ref=slide_ref,
                use_r2s=use_r2s,
            )
        note_lines = [
            f"case={case}",
            f"domain={domain}",
            f"mode={mode}",
            f"role={role}",
            f"layout_family={layout_family}",
            f"brief={brief_path}",
        ]
        if slide_ref:
            note_lines.extend(
                [
                    f"design_refs: {slide_ref}",
                    f"design_ref_name={ref_details.get(slide_ref, {}).get('name', '')}",
                    f"design_ref_category={ref_details.get(slide_ref, {}).get('category', '')}",
                ]
            )
        result = pptmaster_engine.write_svg_slide(
            project_path=str(project_path),
            svg=svg,
            slide_name=f"{idx:02d}_{_slug(role)}",
            notes="\n".join(note_lines),
        )
        if result.get("warnings"):
            warnings.append({"slide": idx, "role": role, "warnings": result["warnings"]})
        shape_counts.append(_svg_shape_count(svg))
        layout_families.append(layout_family)

    pptx_path = ""
    if export:
        export_result = pptmaster_engine.export_project(
            project_path=str(project_path),
            output_path=str(project_path / "exports" / f"{case}_{mode}.pptx"),
            compat=False,
            finalize=False,
        )
        pptx_path = export_result.get("pptx_path", "")

    return {
        "case": case,
        "title": title,
        "brief": str(brief_path),
        "mode": mode,
        "domain": domain,
        "pptx": pptx_path,
        "project": str(project_path),
        "slides": len(roles),
        "roles": roles,
        "layout_families": layout_families,
        "shape_counts": shape_counts,
        "refs": refs,
        "ref_details": ref_details,
        "visual_family": visual_family(domain),
        "warnings": warnings,
    }


def infer_domain(brief: dict[str, Any]) -> str:
    text = _brief_text(brief)
    checks = [
        ("nonprofit", ("nonprofit", "donor", "literacy", "volunteer", "annual impact", "community partners")),
        ("esports", ("esports", "gaming", "roster", "twitch", "series a", "competitive esports")),
        ("restaurant", ("restaurant", "menu", "chef", "counter", "lunch", "food")),
        ("real_estate", ("real estate", "property", "listing", "bedrooms", "acres", "sqft", "open houses")),
        ("research", ("videoworldskills", "academic research", "method pipeline", "ml systems", "paper", "limitations")),
        ("fintech", ("fintech", "ledger", "settlement", "series b", "institutional investors", "merchant")),
        ("healthtech", ("medical", "clinical", "device", "fda", "510(k)", "patients")),
        ("creative", ("agency", "rebrand", "brand", "coffee", "creative")),
        ("kids", ("classroom", "lesson", "volcano", "rockets", "4th-grade", "8-year-old", "earth science")),
        ("legal", ("law firm", "partnership", "legal", "malpractice", "associate", "partner")),
        ("financial", ("board review", "q3", "revenue", "retention", "gross margin", "quarterly board")),
        ("product", ("product launch", "second brain", "saas", "semantic search", "install this week")),
    ]
    for domain, needles in checks:
        if any(n in text for n in needles):
            return domain
    archetype = str(brief.get("archetype_preference") or "").lower()
    if archetype in PALETTES:
        return archetype
    return "generic"


def select_skill_refs(brief: dict[str, Any], entries: list[dict[str, Any]], k: int = 3) -> list[str]:
    """Select k skill references most appropriate for the brief.

    Two-stage pipeline:
      1. Keyword + category overlap to pick top ~25 candidates (cheap, deterministic).
      2. LLM rerank (GPT-5.5 low reasoning) reads the brief + candidate metadata
         and picks the k that best match the brief's visual TONE, not just
         keyword surface — keyword scoring alone biases toward dashboard/gauge
         skills for any brief that mentions "metrics" or "telemetry", even
         when the brief is a cinematic executive keynote.

    Falls back to the keyword-only top-k on any LLM error.
    """
    candidates = _select_skill_refs_keyword(brief, entries, k=max(k, 25))
    if not candidates:
        return []
    if len(candidates) <= k:
        return candidates[:k]

    try:
        reranked = _llm_rerank_skills(brief, candidates, entries, k=k)
        if reranked:
            return reranked
    except Exception as exc:  # noqa: BLE001
        import logging
        logging.getLogger(__name__).warning(
            "LLM skill rerank failed (%s); falling back to keyword top-%d",
            type(exc).__name__, k,
        )
    return candidates[:k]


def _select_skill_refs_keyword(brief: dict[str, Any], entries: list[dict[str, Any]],
                                 k: int = 3) -> list[str]:
    """Original term-overlap + category bonus + diversity ranking.

    Used as pre-filter for the LLM rerank path; also used standalone as the
    fallback when LLM rerank is unavailable.
    """
    domain = infer_domain(brief)
    query = _brief_text(brief) + " " + DOMAIN_QUERY_HINTS.get(domain, "")
    tokens = _tokens(query)
    preferred_categories = _preferred_categories(domain)
    scored: list[tuple[float, str, str]] = []
    for entry in entries:
        sid = str(entry.get("skill_id") or "")
        if not sid:
            continue
        haystack = _skill_text(entry)
        score = sum(1.0 for token in tokens if token in haystack)
        category_path = " ".join(str(x).lower() for x in entry.get("category_path") or [])
        skill_name = str(entry.get("skill_name") or "").lower()
        for category in preferred_categories:
            if category in category_path or category in skill_name:
                score += 2.0
        if "template" in skill_name and score < 8:
            score -= 2.0
        if score > 0:
            scored.append((score, sid, category_path))

    selected: list[str] = []
    seen_categories: set[str] = set()
    for _, sid, category_path in sorted(scored, reverse=True):
        primary_category = category_path.split()[0] if category_path else ""
        if sid in selected:
            continue
        if primary_category and primary_category in seen_categories and len(selected) < k - 1:
            continue
        selected.append(sid)
        if primary_category:
            seen_categories.add(primary_category)
        if len(selected) >= k:
            break

    fallback = _fallback_refs(domain)
    for sid in fallback:
        if len(selected) >= k:
            break
        if sid not in selected:
            selected.append(sid)
    return selected[:k]


def _llm_rerank_skills(brief: dict[str, Any], candidate_ids: list[str],
                        entries: list[dict[str, Any]], k: int) -> list[str]:
    """Ask GPT-5.5 to pick the k best skill refs for the brief.

    Reads candidates' metadata only (name, category, applicability, tags) —
    not full overview/code/visual — to keep prompt under ~6K tokens.
    Returns list of skill_ids in priority order, or empty list on failure
    (caller falls back to the candidates list passed in).
    """
    import json as _json
    import os
    import sys
    project_root = (
        os.environ.get("VWS_PROJECT_ROOT")
        or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        from core.llm import call_azure_openai  # type: ignore
    except Exception:
        return []

    os.environ.setdefault("AZURE_OPENAI_USE_AAD", "1")

    by_id = {str(e.get("skill_id")): e for e in entries}
    catalog_lines: list[str] = []
    for cid in candidate_ids:
        e = by_id.get(cid) or {}
        cat = " / ".join(str(x) for x in e.get("category_path") or []) or "(uncat)"
        applic = (e.get("applicability") or "").strip().replace("\n", " ")
        if len(applic) > 200:
            applic = applic[:200] + "…"
        tags = ", ".join(str(t) for t in (e.get("tags") or [])[:6])
        catalog_lines.append(
            f"- id: {cid}\n  name: {e.get('skill_name', '?')}\n"
            f"  category: {cat}\n  applicability: {applic}\n"
            f"  tags: {tags}"
        )
    catalog = "\n".join(catalog_lines)

    brief_summary = {
        "title": brief.get("title", ""),
        "audience": brief.get("audience", ""),
        "tone_words": brief.get("tone_words") or [],
        "mood_preference": brief.get("mood_preference") or [],
        "archetype_preference": brief.get("archetype_preference", ""),
        "core_points": (brief.get("core_points") or [])[:8],
        "n_slides": brief.get("n_slides", 0),
    }
    brief_text = _json.dumps(brief_summary, indent=2, ensure_ascii=False)

    system = (
        "You pick PPT skill references for an SVG-first deck generator. "
        "Each skill is a documented visual technique distilled from a "
        "real designer's tutorial. Pick the k skills whose visual style "
        "BEST matches the brief's TONE and AUDIENCE — not just keyword "
        "overlap. A 'corporate executive keynote' should NOT use a "
        "dashboard-gauge skill just because the brief mentions 'metrics'. "
        "Prefer cinematic / editorial / architectural / poster / hero "
        "skills for keynotes; prefer dashboard / chart / data-viz skills "
        "for analytical reviews; prefer playful / illustrated / kinetic "
        "skills for educational content. Avoid stacking similar techniques "
        "(don't pick 3 gauges or 3 card-grid layouts)."
    )
    user = (
        f"Brief:\n{brief_text}\n\n"
        f"Candidates ({len(candidate_ids)}):\n{catalog}\n\n"
        f"Pick the {k} best skill_ids in priority order. "
        f"Output ONLY a JSON object: "
        f'{{"picks": ["id1", "id2", ...], "why": "one sentence rationale"}}. '
        f"No prose outside the JSON."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    resp = call_azure_openai(
        messages,
        model="gpt-5.5",
        reasoning_effort="low",
        max_completion_tokens=600,
        timeout=60,
        max_retries=2,
        retry_delay=4.0,
    )
    text = (resp.get("content") or "").strip()
    # Strip optional ```json fence
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = _json.loads(text)
    except _json.JSONDecodeError:
        return []
    picks = data.get("picks") if isinstance(data, dict) else None
    if not isinstance(picks, list):
        return []
    candidate_set = set(candidate_ids)
    out: list[str] = []
    for p in picks:
        sid = str(p).strip()
        if sid and sid in candidate_set and sid not in out:
            out.append(sid)
        if len(out) >= k:
            break
    return out


def render_slide(
    *,
    idx: int,
    total: int,
    role: str,
    title: str,
    audience: str,
    point: str,
    bullets: list[str],
    domain: str,
    palette: Palette,
    ref: str,
    use_r2s: bool,
) -> str:
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}">'
    parts = [head]
    if ref:
        parts.append(f"<!-- design_refs: {escape(ref)} -->")
    parts.append(f'<rect width="{SVG_W}" height="{SVG_H}" fill="{palette.bg}"/>')
    parts.extend(_open_pptmaster_slide(
        idx=idx,
        total=total,
        role=role,
        title=title,
        audience=audience,
        point=point,
        bullets=bullets,
        domain=domain,
        p=palette,
    ))
    parts.append("</svg>")
    return "".join(parts)


def visual_family(domain: str) -> str:
    return {
        "kids": "illustrated classroom diagram",
        "restaurant": "editorial menu and neighborhood board",
        "real_estate": "property gallery and location packet",
        "financial": "dense boardroom KPI memo",
        "legal": "practice-review dossier",
        "research": "academic method architecture",
        "fintech": "networked dark product dashboard",
        "esports": "neon arena roster",
        "nonprofit": "warm impact story",
        "healthtech": "clinical evidence packet",
        "creative": "agency collage moodboard",
        "product": "product UI launch system",
    }.get(domain, "open PPTMaster editorial system")


def design_opportunities(domain: str) -> list[str]:
    """Return non-binding opportunities for adapting selected R2S refs.

    These are not slide roles and not a required deck skeleton. They describe
    where skill mechanisms may enrich PPTMaster's own open-ended plan.
    """
    return {
        "kids": [
            "Use diagrammatic labels, playful arrows, and draw-along activity surfaces.",
            "Prefer visual analogies over boardroom agenda or decision pages.",
            "R2S process/diagram skills can enrich explanation slides without fixing slide order.",
        ],
        "restaurant": [
            "Use menu-board, neighborhood-scene, sourcing-map, and unit-economics surfaces as needed.",
            "R2S editorial/photo treatment skills should add appetite and locality, not generic investor templates.",
        ],
        "real_estate": [
            "Use gallery, map, factsheet, material, and comparable-sales surfaces according to content.",
            "R2S image/collage skills should stage property inspection and location logic.",
        ],
        "financial": [
            "Use dense KPI, variance, risk, and decision-table surfaces where the content demands them.",
            "R2S dashboard/table skills should improve data hierarchy without forcing all pages to dashboards.",
        ],
        "legal": [
            "Use dossier, practice-mix, risk register, talent pipeline, and vote surfaces as appropriate.",
            "R2S table/matrix skills should preserve restrained partnership-review tone.",
        ],
        "research": [
            "Use method pipeline, architecture, evidence matrix, results, and limitation surfaces as needed.",
            "R2S process/architecture skills should make the research logic more traceable.",
        ],
        "fintech": [
            "Use network, settlement, dashboard, moat comparison, and business-model surfaces as needed.",
            "R2S technical/dashboard skills should express rails, reconciliation, and flow.",
        ],
        "esports": [
            "Use roster, game portfolio, sponsor ladder, arena/media, and audience surfaces as needed.",
            "R2S neon/team/gallery skills should heighten identity and team momentum.",
        ],
        "nonprofit": [
            "Use story, impact dashboard, program map, volunteer, and donor ask surfaces as needed.",
            "R2S storytelling/dashboard skills should emphasize impact and warmth.",
        ],
        "product": [
            "Use product UI, hero metric, feature grid, before/after, pricing, and security surfaces as needed.",
            "R2S comparison/product skills should clarify capability and adoption path.",
        ],
    }.get(domain, ["Use selected R2S refs as optional mechanism evidence while preserving open PPTMaster page planning."])


def _open_pptmaster_slide(
    *,
    idx: int,
    total: int,
    role: str,
    title: str,
    audience: str,
    point: str,
    bullets: list[str],
    domain: str,
    p: Palette,
) -> list[str]:
    layout = _layout_family(role, idx, total)
    parts = _domain_stage(domain, p, idx)
    if layout == "cover":
        parts.extend(_layout_cover(title, audience, domain, p))
    elif layout == "hero_metric":
        parts.extend(_layout_hero_metric(role, point, bullets, domain, p))
    elif layout == "split":
        parts.extend(_layout_split(role, point, bullets, domain, p))
    elif layout == "diagram":
        parts.extend(_layout_diagram(role, point, bullets, domain, p))
    elif layout == "dashboard":
        parts.extend(_layout_dashboard(role, point, bullets, domain, p))
    elif layout == "matrix":
        parts.extend(_layout_matrix(role, point, bullets, domain, p))
    elif layout == "process":
        parts.extend(_layout_process(role, point, bullets, domain, p))
    elif layout == "gallery":
        parts.extend(_layout_gallery(role, point, bullets, domain, p))
    elif layout == "quote":
        parts.extend(_layout_quote(role, point, bullets, domain, p))
    elif layout == "close":
        parts.extend(_layout_close(role, point, bullets, domain, p))
    else:
        parts.extend(_layout_cards(role, point, bullets, domain, p))
    return parts


def _layout_family(role: str, idx: int, total: int) -> str:
    role = role.lower()
    if idx == 1:
        return "cover"
    if idx == total or "close" in role or "ask" in role or "cta" in role:
        return "close"
    if any(k in role for k in ("hero", "giant", "metric")):
        return "hero_metric"
    if any(k in role for k in ("split", "before_after", "market_gap", "motivation")):
        return "split"
    if any(k in role for k in ("diagram", "architecture", "network", "stack", "site_map", "program_map")):
        return "diagram"
    if any(k in role for k in ("dashboard", "snapshot", "economics", "reach", "results")):
        return "dashboard"
    if any(k in role for k in ("matrix", "table", "register", "comparison", "pricing", "vote", "risk")):
        return "matrix"
    if any(k in role for k in ("timeline", "calendar", "roadmap", "pipeline", "process", "flow", "buildout")):
        return "process"
    if any(k in role for k in ("gallery", "moodboard", "collage", "scene", "wall", "roster", "portfolio")):
        return "gallery"
    if any(k in role for k in ("quote", "story", "voice")):
        return "quote"
    return ["cards", "split", "matrix", "process", "gallery"][(idx - 2) % 5]


def _domain_stage(domain: str, p: Palette, idx: int) -> list[str]:
    label = {
        "kids": "CLASSROOM",
        "restaurant": "MENU BOARD",
        "real_estate": "PROPERTY PACKET",
        "financial": "BOARD PACKET",
        "legal": "PARTNERSHIP DOSSIER",
        "research": "METHOD TRACE",
        "fintech": "RAIL NETWORK",
        "esports": "ARENA",
        "nonprofit": "IMPACT STORY",
        "product": "PRODUCT SYSTEM",
    }.get(domain, "OPEN PPTMASTER")
    parts = [
        f'<text x="70" y="82" font-family="Arial" font-size="16" font-weight="900" fill="{p.primary}">{escape(label)} / {idx:02d}</text>',
    ]
    if domain in {"fintech", "research", "esports", "financial"}:
        parts.append(f'<circle cx="1115" cy="120" r="180" fill="{p.primary}" opacity="0.10"/>')
        parts.append(f'<path d="M0 655 C320 600 540 725 850 640 S1110 590 1280 630 L1280 720 L0 720 Z" fill="{p.primary}" opacity="0.07"/>')
    elif domain == "kids":
        parts.append(f'<circle cx="1110" cy="115" r="110" fill="{p.accent}" opacity="0.17"/>')
        parts.append(f'<path d="M986 654 q70 -76 140 0" fill="none" stroke="{p.primary}" stroke-width="10" opacity="0.16"/>')
    elif domain == "restaurant":
        parts.append(f'<rect x="42" y="48" width="1196" height="626" rx="36" fill="none" stroke="{p.primary}" stroke-width="3" opacity="0.55"/>')
        parts.append(f'<circle cx="1090" cy="146" r="70" fill="{p.accent}" opacity="0.22"/>')
    elif domain == "real_estate":
        parts.append(f'<rect x="58" y="96" width="360" height="520" rx="28" fill="{p.surface}" opacity="0.62"/>')
        parts.append(f'<rect x="900" y="98" width="250" height="250" rx="28" fill="{p.primary}" opacity="0.12"/>')
    else:
        parts.append(f'<circle cx="1110" cy="120" r="130" fill="{p.accent}" opacity="0.12"/>')
    return parts


def _layout_cover(title: str, audience: str, domain: str, p: Palette) -> list[str]:
    return [
        *_wrap(title, 74, 180, 32, 58, p.ink, weight=900, max_lines=3),
        *_wrap(audience, 78, 424, 48, 24, p.muted, max_lines=2),
        f'<rect x="770" y="146" width="365" height="390" rx="42" fill="{p.surface}" stroke="{p.primary}" stroke-width="4" opacity="0.86"/>',
        f'<circle cx="950" cy="305" r="118" fill="{p.accent}" opacity="0.24"/>',
        f'<rect x="840" y="430" width="220" height="42" rx="21" fill="{p.primary}" opacity="0.30"/>',
    ]


def _layout_hero_metric(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    value = _numeric_values(point, bullets)[0]
    return [
        *_eyebrow_and_title(role, point, p),
        f'<text x="90" y="476" font-family="Arial" font-size="150" font-weight="900" fill="{p.primary}">{escape(value)}</text>',
        f'<rect x="760" y="210" width="340" height="260" rx="38" fill="{p.surface}" stroke="{p.accent}" stroke-width="3" opacity="0.88"/>',
        *_wrap(point, 800, 310, 25, 25, p.ink, weight=800, max_lines=4),
    ]


def _layout_split(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    items = bullets or [point]
    return [
        *_eyebrow_and_title(role, point, p),
        f'<rect x="86" y="260" width="510" height="310" rx="30" fill="{p.surface}" stroke="{p.muted}" stroke-width="2"/>',
        f'<rect x="684" y="220" width="500" height="390" rx="30" fill="{p.primary}" opacity="0.16" stroke="{p.primary}" stroke-width="3"/>',
        f'<text x="126" y="326" font-family="Arial" font-size="20" font-weight="900" fill="{p.accent}">BEFORE</text>',
        f'<text x="724" y="286" font-family="Arial" font-size="20" font-weight="900" fill="{p.primary}">AFTER</text>',
        *_wrap(items[0], 126, 390, 35, 23, p.ink, weight=800, max_lines=3),
        *_wrap(items[min(1, len(items)-1)], 724, 354, 33, 25, p.ink, weight=900, max_lines=4),
        f'<path d="M610 405 L664 405" stroke="{p.accent}" stroke-width="7" stroke-linecap="round"/>',
        f'<path d="M650 385 L674 405 L650 425" fill="none" stroke="{p.accent}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
    ]


def _layout_diagram(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    cx, cy = 640, 378
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="96" fill="{p.primary}" opacity="0.22" stroke="{p.primary}" stroke-width="4"/>')
    parts.extend(_wrap(_short_label(point), cx - 82, cy - 8, 15, 21, p.ink, weight=900, max_lines=2))
    positions = [(260, 280), (1010, 280), (320, 550), (960, 550), (640, 585)]
    for i, item in enumerate((bullets or [point])[:5]):
        x, y = positions[i]
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{p.muted}" stroke-width="3" opacity="0.35"/>')
        parts.append(f'<rect x="{x-116}" y="{y-48}" width="232" height="96" rx="22" fill="{p.surface}" stroke="{p.accent if i%2 else p.primary}" stroke-width="2"/>')
        parts.extend(_wrap(item, x - 92, y - 5, 23, 17, p.ink, weight=760, max_lines=2))
    return parts


def _layout_dashboard(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    values = _numeric_values(point, bullets)
    labels = bullets[:4] or [point]
    for i in range(4):
        x = 88 + (i % 4) * 292
        h = 118 + (i % 3) * 36
        y = 562 - h
        parts.append(f'<rect x="{x}" y="{y}" width="230" height="{h}" rx="24" fill="{p.surface}" stroke="{p.primary}" stroke-width="2"/>')
        parts.append(f'<text x="{x+26}" y="{y+58}" font-family="Arial" font-size="38" font-weight="900" fill="{p.primary}">{escape(values[i % len(values)])}</text>')
        parts.extend(_wrap(labels[i % len(labels)], x + 26, y + 96, 20, 16, p.muted, weight=700, max_lines=2))
    return parts


def _layout_matrix(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    items = (bullets or [point])[:6]
    for i, item in enumerate(items):
        col = i % 3
        row = i // 3
        x = 82 + col * 382
        y = 244 + row * 165
        parts.append(f'<rect x="{x}" y="{y}" width="326" height="124" rx="18" fill="{p.surface}" stroke="{p.muted}" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="326" height="34" rx="17" fill="{p.primary}" opacity="0.18"/>')
        parts.append(f'<text x="{x+22}" y="{y+25}" font-family="Arial" font-size="15" font-weight="900" fill="{p.primary}">{escape(str(i+1).zfill(2))}</text>')
        parts.extend(_wrap(item, x + 22, y + 72, 28, 17, p.ink, weight=760, max_lines=2))
    return parts


def _layout_process(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    items = (bullets or [point])[:5]
    for i, item in enumerate(items):
        x = 122 + i * 218
        y = 360 + (i % 2) * 90
        parts.append(f'<path d="M{x} {y-46} L{x+128} {y-46} L{x+164} {y} L{x+128} {y+46} L{x} {y+46} L{x+36} {y} Z" fill="{p.primary if i%2 else p.accent}" opacity="0.80"/>')
        parts.append(f'<text x="{x+58}" y="{y+9}" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">{i+1}</text>')
        parts.extend(_wrap(item, x - 8, 250 if i % 2 == 0 else 562, 22, 16, p.ink, weight=760, max_lines=2))
    return parts


def _layout_gallery(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    rects = [(80, 238, 420, 330), (530, 238, 250, 150), (810, 238, 360, 150), (530, 418, 310, 150), (870, 418, 300, 150)]
    for i, (x, y, w, h) in enumerate(rects):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{p.primary if i%2 else p.accent}" opacity="{0.18 + i*0.06:.2f}"/>')
        item = (bullets or [point])[i % len(bullets or [point])]
        parts.extend(_wrap(item, x + 24, y + h - 42, max(14, w // 17), 17, p.ink, weight=800, max_lines=1))
    return parts


def _layout_quote(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    quote = bullets[0] if bullets else point
    return [
        f'<text x="88" y="156" font-family="Arial" font-size="96" font-weight="900" fill="{p.primary}" opacity="0.30">“</text>',
        *_wrap(quote, 150, 220, 38, 46, p.ink, weight=900, max_lines=4),
        f'<line x1="158" y1="560" x2="560" y2="560" stroke="{p.accent}" stroke-width="6"/>',
        f'<circle cx="980" cy="360" r="170" fill="{p.surface}" stroke="{p.primary}" stroke-width="3" opacity="0.74"/>',
    ]


def _layout_close(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    ask = bullets[-1] if bullets else point
    return [
        f'<rect x="0" y="0" width="1280" height="720" fill="{p.primary}" opacity="0.16"/>',
        # decorative accent tucked into the bottom-right corner, clear of all text
        f'<circle cx="1240" cy="690" r="210" fill="{p.accent}" opacity="0.18"/>',
        f'<circle cx="1240" cy="690" r="120" fill="{p.primary}" opacity="0.30"/>',
        f'<text x="84" y="122" font-family="Arial" font-size="18" font-weight="900" fill="{p.accent}">{escape(domain.upper())} NEXT STEP</text>',
        *_wrap(ask, 84, 250, 27, 54, p.ink, weight=900, max_lines=3),
        f'<rect x="88" y="520" width="480" height="72" rx="36" fill="{p.primary}"/>',
        f'<text x="126" y="567" font-family="Arial" font-size="24" font-weight="900" fill="#FFFFFF">{escape(_close_label(domain))}</text>',
    ]


def _layout_cards(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    items = (bullets or [point])[:4]
    for i, item in enumerate(items):
        x = 92 + i * 286
        y = 272 + (i % 2) * 34
        parts.append(f'<rect x="{x}" y="{y}" width="238" height="260" rx="24" fill="{p.surface}" stroke="{p.primary if i%2 else p.accent}" stroke-width="2"/>')
        parts.append(f'<circle cx="{x+54}" cy="{y+58}" r="22" fill="{p.primary if i%2 else p.accent}"/>')
        parts.extend(_wrap(item, x + 28, y + 126, 22, 19, p.ink, weight=760, max_lines=4))
    return parts


def _family_kids(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<circle cx="1090" cy="120" r="132" fill="{p.accent}" opacity="0.18"/>',
        f'<path d="M760 575 L900 260 L1040 575 Z" fill="{p.primary}" opacity="0.28"/>',
        f'<path d="M900 260 L945 575 L862 575 Z" fill="{p.accent}" opacity="0.75"/>',
        f'<text x="64" y="82" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">CLASSROOM EXPLAINER {idx}/{total}</text>',
    ]
    if idx == 1:
        parts.extend(_wrap(title, 72, 190, 28, 58, p.ink, weight=900, max_lines=3))
        parts.extend(_wrap(audience, 76, 420, 46, 24, p.muted, max_lines=2))
        return parts
    if "diagram" in role:
        parts.extend(_wrap("Label the volcano", 72, 140, 30, 42, p.ink, weight=900, max_lines=1))
        labels = ["crater", "pipe", "magma", "lava"]
        coords = [(760, 250), (900, 400), (800, 560), (980, 470)]
        for label, (x, y) in zip(labels, coords):
            parts.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{p.accent}"/>')
            parts.append(f'<line x1="{x}" y1="{y}" x2="{x-190}" y2="{y-40}" stroke="{p.ink}" stroke-width="3"/>')
            parts.append(f'<text x="{x-330}" y="{y-48}" font-family="Arial" font-size="24" font-weight="900" fill="{p.ink}">{escape(label)}</text>')
    elif "activity" in role or idx == total:
        parts.extend(_wrap("Draw it, then explain it", 72, 150, 34, 46, p.ink, weight=900, max_lines=2))
        for i, item in enumerate((bullets or [point])[:3]):
            x = 90 + i * 330
            parts.append(f'<rect x="{x}" y="330" width="270" height="170" rx="26" fill="{p.surface}" stroke="{p.accent}" stroke-width="4"/>')
            parts.extend(_wrap(item, x + 24, 390, 24, 20, p.ink, weight=800, max_lines=3))
    else:
        parts.extend(_wrap(point, 72, 140, 38, 42, p.ink, weight=900, max_lines=2))
        for i, item in enumerate((bullets or [point])[:4]):
            x = 82 + (i % 2) * 430
            y = 280 + (i // 2) * 150
            parts.append(f'<path d="M{x} {y} q20 -30 50 0 t50 0 t50 0 q24 34 -14 72 h-136 q-44 -28 0 -72" fill="{p.surface}" stroke="{p.primary if i%2 else p.accent}" stroke-width="3"/>')
            parts.extend(_wrap(item, x + 22, y + 48, 34, 18, p.ink, weight=800, max_lines=2))
    return parts


def _family_restaurant(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<rect x="48" y="54" width="1184" height="612" rx="34" fill="{p.surface}" stroke="{p.primary}" stroke-width="3"/>',
        f'<line x1="662" y1="86" x2="662" y2="632" stroke="{p.primary}" stroke-width="3" opacity="0.35"/>',
        f'<circle cx="1035" cy="170" r="76" fill="{p.accent}" opacity="0.26"/>',
        f'<text x="82" y="112" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">NOON MENU BOARD {idx}/{total}</text>',
    ]
    if idx == 1:
        parts.extend(_wrap(title, 82, 210, 28, 50, p.ink, weight=900, max_lines=4))
        parts.extend(_wrap(audience, 720, 250, 32, 26, p.muted, weight=700, max_lines=4))
    elif "menu" in role:
        parts.extend(_wrap("The offer is small on purpose", 82, 170, 30, 42, p.ink, weight=900, max_lines=2))
        menu = ["hot bowl", "salad trio", "two sandwiches", "one dessert"]
        for i, item in enumerate(menu):
            parts.append(f'<text x="740" y="{190+i*86}" font-family="Arial" font-size="34" font-weight="900" fill="{p.ink}">{escape(item)}</text>')
            parts.append(f'<text x="1080" y="{190+i*86}" font-family="Arial" font-size="26" font-weight="900" fill="{p.primary}">${18+i*2}</text>')
    else:
        parts.extend(_wrap(point, 82, 170, 31, 40, p.ink, weight=900, max_lines=2))
        for i, item in enumerate((bullets or [point])[:5]):
            y = 260 + i * 62
            parts.append(f'<circle cx="730" cy="{y-8}" r="11" fill="{p.accent}"/>')
            parts.extend(_wrap(item, 760, y, 35, 20, p.ink, weight=760, max_lines=1))
    return parts


def _family_real_estate(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<rect x="64" y="70" width="506" height="560" rx="28" fill="{p.surface}" stroke="{p.primary}" stroke-width="3"/>',
        f'<rect x="610" y="70" width="596" height="255" rx="28" fill="{p.primary}" opacity="0.16"/>',
        f'<rect x="610" y="360" width="280" height="270" rx="28" fill="{p.accent}" opacity="0.18"/>',
        f'<rect x="926" y="360" width="280" height="270" rx="28" fill="{p.primary}" opacity="0.12"/>',
        f'<text x="90" y="112" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">PROPERTY PACKET {idx}/{total}</text>',
    ]
    if idx == 1:
        parts.extend(_wrap(title, 90, 210, 27, 48, p.ink, weight=900, max_lines=4))
        parts.extend(_wrap(audience, 650, 188, 38, 24, p.muted, weight=700, max_lines=3))
    elif "map" in role or "site" in role:
        parts.extend(_wrap("Location logic", 90, 170, 27, 44, p.ink, weight=900, max_lines=2))
        pts = [(710, 455), (790, 410), (875, 495), (1010, 420), (1110, 520)]
        for a, b in zip(pts, pts[1:]):
            parts.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{p.primary}" stroke-width="5" opacity="0.55"/>')
        for x, y in pts:
            parts.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{p.accent}"/>')
    else:
        parts.extend(_wrap(point, 90, 170, 27, 42, p.ink, weight=900, max_lines=3))
        for i, item in enumerate((bullets or [point])[:4]):
            x = 645 + (i % 2) * 285
            y = 390 + (i // 2) * 112
            parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">FACT {i+1}</text>')
            parts.extend(_wrap(item, x, y + 38, 25, 18, p.ink, weight=760, max_lines=2))
    return parts


def _family_boardroom(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette, *, legal: bool = False) -> list[str]:
    label = "PARTNERSHIP DOSSIER" if legal else "BOARD PACKET"
    parts = [
        f'<rect x="0" y="0" width="1280" height="92" fill="{p.surface}"/>',
        f'<text x="72" y="58" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">{label} {idx}/{total}</text>',
        f'<line x1="72" y1="150" x2="1180" y2="150" stroke="{p.primary}" stroke-width="3"/>',
    ]
    parts.extend(_wrap(title if idx == 1 else point, 72, 128, 52, 34, p.ink, weight=900, max_lines=2))
    rows = (bullets or [point])[:6]
    for i, item in enumerate(rows):
        y = 250 + i * 58
        fill = p.surface if i % 2 == 0 else p.bg
        parts.append(f'<rect x="82" y="{y-34}" width="1070" height="48" fill="{fill}" stroke="{p.muted}" stroke-width="1" opacity="0.95"/>')
        parts.append(f'<text x="108" y="{y}" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">{escape(str(i+1).zfill(2))}</text>')
        parts.extend(_wrap(item, 170, y, 74, 18, p.ink, weight=700, max_lines=1))
    if any(k in role for k in ["dashboard", "metric", "partner"]):
        values = _numeric_values(point, rows)
        for i, value in enumerate(values[:4]):
            x = 740 + (i % 2) * 210
            y = 250 + (i // 2) * 122
            parts.append(f'<rect x="{x}" y="{y}" width="172" height="88" rx="12" fill="{p.primary}" opacity="0.22"/>')
            parts.append(f'<text x="{x+20}" y="{y+54}" font-family="Arial" font-size="28" font-weight="900" fill="{p.ink}">{escape(value)}</text>')
    return parts


def _family_research(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<rect x="54" y="62" width="1172" height="596" rx="18" fill="{p.surface}" opacity="0.70"/>',
        f'<text x="82" y="108" font-family="Arial" font-size="18" font-weight="900" fill="{p.accent}">METHOD TRACE {idx}/{total}</text>',
    ]
    parts.extend(_wrap(title if idx == 1 else point, 82, 170, 45, 40, p.ink, weight=900, max_lines=2))
    nodes = ["Input", "Distill", "Index", "Compose", "Audit"]
    for i, node in enumerate(nodes):
        x = 110 + i * 220
        y = 430 if i % 2 else 360
        parts.append(f'<rect x="{x}" y="{y}" width="150" height="74" rx="14" fill="{p.primary if i%2 else p.accent}" opacity="0.82"/>')
        parts.append(f'<text x="{x+22}" y="{y+46}" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">{node}</text>')
        if i:
            parts.append(f'<path d="M{x-68} {y+37} L{x-12} {y+37}" stroke="{p.muted}" stroke-width="4"/>')
    for i, item in enumerate((bullets or [point])[:3]):
        parts.extend(_wrap(item, 740, 275 + i * 70, 32, 18, p.muted, weight=700, max_lines=2))
    return parts


def _family_fintech(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<text x="70" y="92" font-family="Arial" font-size="18" font-weight="900" fill="{p.accent}">RAIL NETWORK {idx}/{total}</text>',
        *_wrap(title if idx == 1 else point, 70, 150, 40, 42, p.ink, weight=900, max_lines=2),
    ]
    hub = (650, 390)
    parts.append(f'<circle cx="{hub[0]}" cy="{hub[1]}" r="72" fill="{p.primary}" opacity="0.82"/>')
    for i, item in enumerate((bullets or [point])[:6]):
        x = 210 + (i % 3) * 430
        y = 290 + (i // 3) * 190
        parts.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="{p.primary}" stroke-width="3" opacity="0.42"/>')
        parts.append(f'<rect x="{x-95}" y="{y-42}" width="190" height="84" rx="18" fill="{p.surface}" stroke="{p.accent}" stroke-width="2"/>')
        parts.extend(_wrap(item, x - 72, y - 4, 18, 16, p.ink, weight=760, max_lines=2))
    return parts


def _family_esports(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<path d="M0 0 L1280 0 L1120 720 L0 720 Z" fill="{p.surface}" opacity="0.75"/>',
        f'<text x="76" y="96" font-family="Arial" font-size="18" font-weight="900" fill="{p.accent}">ARENA ROSTER {idx}/{total}</text>',
        *_wrap(title if idx == 1 else point, 76, 170, 34, 44, p.ink, weight=900, max_lines=2),
    ]
    for i, item in enumerate((bullets or [point])[:5]):
        x = 90 + i * 225
        y = 420 + (i % 2) * 36
        parts.append(f'<path d="M{x} {y-120} L{x+150} {y-150} L{x+190} {y+50} L{x+20} {y+80} Z" fill="{p.primary if i%2 else p.accent}" opacity="0.32" stroke="{p.accent}" stroke-width="2"/>')
        parts.extend(_wrap(item, x + 22, y + 6, 18, 17, p.ink, weight=800, max_lines=2))
    return parts


def _family_nonprofit(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<circle cx="210" cy="360" r="185" fill="{p.primary}" opacity="0.15"/>',
        f'<text x="78" y="98" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">IMPACT STORY {idx}/{total}</text>',
        *_wrap(title if idx == 1 else point, 78, 170, 38, 42, p.ink, weight=900, max_lines=2),
        f'<path d="M650 170 C850 120 1070 230 1110 420 C930 520 720 520 610 390 C570 300 590 220 650 170 Z" fill="{p.surface}" stroke="{p.accent}" stroke-width="3"/>',
    ]
    for i, item in enumerate((bullets or [point])[:4]):
        y = 260 + i * 72
        parts.append(f'<circle cx="690" cy="{y-8}" r="16" fill="{p.accent}" opacity="0.72"/>')
        parts.extend(_wrap(item, 725, y, 36, 19, p.ink, weight=760, max_lines=2))
    return parts


def _family_product(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<rect x="710" y="86" width="430" height="548" rx="46" fill="{p.surface}" stroke="{p.primary}" stroke-width="4"/>',
        f'<rect x="750" y="148" width="350" height="72" rx="18" fill="{p.primary}" opacity="0.20"/>',
        f'<text x="78" y="100" font-family="Arial" font-size="18" font-weight="900" fill="{p.accent}">PRODUCT SYSTEM {idx}/{total}</text>',
        *_wrap(title if idx == 1 else point, 78, 176, 32, 48, p.ink, weight=900, max_lines=3),
    ]
    for i, item in enumerate((bullets or [point])[:4]):
        y = 270 + i * 78
        parts.append(f'<rect x="760" y="{y}" width="320" height="52" rx="16" fill="{p.primary if i%2 else p.accent}" opacity="0.22"/>')
        parts.extend(_wrap(item, 790, y + 34, 28, 16, p.ink, weight=760, max_lines=1))
    return parts


def _family_open_editorial(idx: int, total: int, role: str, title: str, audience: str, point: str, bullets: list[str], p: Palette) -> list[str]:
    parts = [
        f'<text x="76" y="96" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">OPEN PPTMASTER {idx}/{total}</text>',
        *_wrap(title if idx == 1 else point, 76, 170, 42, 44, p.ink, weight=900, max_lines=2),
    ]
    for i, item in enumerate((bullets or [point])[:4]):
        x = 90 + i * 280
        parts.append(f'<rect x="{x}" y="360" width="230" height="170" rx="18" fill="{p.surface}" stroke="{p.primary}" stroke-width="2"/>')
        parts.extend(_wrap(item, x + 24, 420, 22, 18, p.ink, weight=760, max_lines=3))
    return parts


def _r2s_mechanism_overlay(ref: str, role: str, domain: str, p: Palette, idx: int) -> list[str]:
    """Add visible mechanism cues while leaving the open PPTMaster plan intact."""
    seed = sum(ord(ch) for ch in ref) % 5
    parts: list[str] = []
    if seed == 0:
        # Split-panel / masked-window mechanism.
        parts.append(f'<path d="M940 0 L1280 0 L1180 720 L820 720 Z" fill="{p.primary}" opacity="0.10"/>')
        parts.append(f'<path d="M1030 0 L1280 0 L1225 720 L980 720 Z" fill="{p.accent}" opacity="0.13"/>')
        for i in range(4):
            parts.append(f'<rect x="{870+i*72}" y="{98+i*22}" width="54" height="118" rx="18" fill="{p.surface}" stroke="{p.accent}" stroke-width="2" opacity="0.40"/>')
    elif seed == 1:
        # Glass/card-depth mechanism.
        parts.append(f'<rect x="812" y="82" width="360" height="168" rx="34" fill="{p.surface}" stroke="{p.primary}" stroke-width="3" opacity="0.50"/>')
        for i in range(3):
            parts.append(f'<rect x="{848+i*92}" y="{120+i*18}" width="74" height="74" rx="20" fill="{p.primary if i%2 else p.accent}" opacity="{0.24+i*0.08:.2f}"/>')
        parts.append(f'<circle cx="1130" cy="104" r="72" fill="{p.accent}" opacity="0.16"/>')
    elif seed == 2:
        # Ribbon flow / kinetic path mechanism.
        parts.append(f'<path d="M810 118 C900 24 1015 205 1195 82 L1195 138 C1020 260 910 96 810 188 Z" fill="{p.accent}" opacity="0.24"/>')
        parts.append(f'<path d="M820 196 C930 105 1022 294 1178 206" fill="none" stroke="{p.primary}" stroke-width="8" opacity="0.42"/>')
        for i in range(4):
            parts.append(f'<circle cx="{860+i*90}" cy="{154+(i%2)*48}" r="{10+i*2}" fill="{p.primary if i%2 else p.accent}" opacity="0.75"/>')
    elif seed == 3:
        # Hub/network mechanism.
        parts.append(f'<circle cx="1010" cy="156" r="58" fill="{p.primary}" opacity="0.28"/>')
        for i, (x, y) in enumerate([(850, 96), (910, 220), (1110, 96), (1160, 224), (1010, 292)]):
            parts.append(f'<line x1="1010" y1="156" x2="{x}" y2="{y}" stroke="{p.accent}" stroke-width="3" opacity="0.34"/>')
            parts.append(f'<circle cx="{x}" cy="{y}" r="{18+i}" fill="{p.accent if i%2 else p.primary}" opacity="0.54"/>')
    else:
        # Spotlight / macro-typographic stage mechanism.
        parts.append(f'<circle cx="1035" cy="162" r="150" fill="{p.accent}" opacity="0.15"/>')
        parts.append(f'<circle cx="1035" cy="162" r="88" fill="{p.primary}" opacity="0.22"/>')
        parts.append(f'<rect x="810" y="95" width="420" height="132" rx="66" fill="{p.surface}" stroke="{p.accent}" stroke-width="3" opacity="0.46"/>')
        parts.append(f'<line x1="860" y1="162" x2="1180" y2="162" stroke="{p.primary}" stroke-width="6" opacity="0.36"/>')
    return parts


def _slide_cover(title: str, audience: str, domain: str, p: Palette) -> list[str]:
    parts = [
        f'<text x="72" y="104" font-family="Arial" font-size="20" font-weight="900" fill="{p.primary}">{escape(domain.upper())}</text>',
        *_wrap(title, 72, 188, 34, 54, p.ink, weight=900, max_lines=3),
        *_wrap(audience, 76, 420, 52, 24, p.muted, max_lines=2),
        f'<rect x="760" y="118" width="360" height="450" rx="38" fill="{p.surface}" opacity="0.92" stroke="{p.primary}" stroke-width="4"/>',
        f'<circle cx="940" cy="276" r="112" fill="{p.accent}" opacity="0.25"/>',
        f'<circle cx="1012" cy="356" r="145" fill="{p.primary}" opacity="0.18"/>',
    ]
    for i in range(4):
        parts.append(f'<rect x="{820+i*54}" y="{460-i*28}" width="38" height="{62+i*34}" rx="10" fill="{p.primary if i%2 else p.accent}" opacity="0.85"/>')
    return parts


def _slide_diagram(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    cx, cy = 640, 350
    parts = [
        *_eyebrow_and_title(role, point, p),
        f'<circle cx="{cx}" cy="{cy}" r="116" fill="{p.primary}" opacity="0.18" stroke="{p.primary}" stroke-width="4"/>',
        *_wrap(_short_label(point), cx - 94, cy - 12, 16, 22, p.ink, weight=900, max_lines=2),
    ]
    positions = [(290, 260), (990, 260), (320, 500), (960, 500)]
    for i, item in enumerate((bullets or [point])[:4]):
        x, y = positions[i]
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{p.muted}" stroke-width="3" opacity="0.35"/>')
        parts.append(f'<rect x="{x-118}" y="{y-52}" width="236" height="104" rx="22" fill="{p.surface}" stroke="{p.primary if i%2 else p.accent}" stroke-width="2"/>')
        parts.extend(_wrap(item, x - 92, y - 8, 24, 18, p.ink, max_lines=2, weight=760))
    return parts


def _slide_dashboard(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    values = _numeric_values(point, bullets)
    labels = bullets[:4] or [point]
    for i in range(4):
        x = 86 + (i % 2) * 548
        y = 222 + (i // 2) * 190
        value = values[i % len(values)]
        parts.append(f'<rect x="{x}" y="{y}" width="488" height="146" rx="24" fill="{p.surface}" stroke="{p.primary}" stroke-width="2"/>')
        parts.append(f'<text x="{x+34}" y="{y+68}" font-family="Arial" font-size="44" font-weight="900" fill="{p.primary}">{escape(value)}</text>')
        parts.extend(_wrap(labels[i % len(labels)], x + 34, y + 108, 34, 18, p.muted, max_lines=1, weight=700))
        parts.append(f'<rect x="{x+386}" y="{y+42}" width="58" height="58" rx="14" fill="{p.accent}" opacity="0.78"/>')
    return parts


def _slide_matrix(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    items = (bullets or [point])[:6]
    for i, item in enumerate(items):
        col = i % 3
        row = i // 3
        x = 82 + col * 390
        y = 220 + row * 178
        parts.append(f'<rect x="{x}" y="{y}" width="335" height="132" rx="20" fill="{p.surface}" stroke="{p.muted}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+24}" y="{y+42}" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">{escape(str(i+1).zfill(2))}</text>')
        parts.extend(_wrap(item, x + 24, y + 78, 27, 18, p.ink, max_lines=2, weight=760))
    return parts


def _slide_process(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    items = (bullets or [point])[:5]
    parts.append(f'<line x1="142" y1="386" x2="1120" y2="386" stroke="{p.muted}" stroke-width="4" opacity="0.25"/>')
    for i, item in enumerate(items):
        x = 160 + i * 225
        y = 330 if i % 2 == 0 else 430
        fill = p.primary if i % 2 == 0 else p.accent
        parts.append(f'<path d="M{x} {y-42} L{x+128} {y-42} L{x+162} {y} L{x+128} {y+42} L{x} {y+42} Z" fill="{fill}"/>')
        parts.append(f'<text x="{x+42}" y="{y+9}" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">{escape(str(i+1))}</text>')
        parts.extend(_wrap(item, x - 20, 250 if i % 2 == 0 else 545, 22, 17, p.ink, max_lines=2, weight=760))
    return parts


def _slide_gallery(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    rects = [(82, 222, 330, 360), (442, 222, 250, 170), (720, 222, 410, 170), (442, 414, 330, 168), (800, 414, 330, 168)]
    for i, (x, y, w, h) in enumerate(rects):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{p.primary if i%2 else p.accent}" opacity="{0.18 + i*0.07:.2f}"/>')
        label = (bullets or [point])[i % len(bullets or [point])]
        parts.extend(_wrap(label, x + 26, y + h - 46, max(14, w // 17), 18, p.ink, max_lines=1, weight=800))
    return parts


def _slide_cards(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    parts = [*_eyebrow_and_title(role, point, p)]
    items = (bullets or [point])[:4]
    for i, item in enumerate(items):
        x = 92 + i * 286
        parts.append(f'<rect x="{x}" y="254" width="238" height="270" rx="24" fill="{p.surface}" stroke="{p.primary if i%2 else p.accent}" stroke-width="2"/>')
        parts.append(f'<circle cx="{x+54}" cy="314" r="22" fill="{p.primary if i%2 else p.accent}"/>')
        parts.extend(_wrap(item, x + 28, 382, 22, 20, p.ink, max_lines=4, weight=760))
    return parts


def _slide_close(role: str, point: str, bullets: list[str], domain: str, p: Palette) -> list[str]:
    ask = point
    if bullets:
        ask = bullets[-1]
    parts = [
        f'<text x="84" y="122" font-family="Arial" font-size="20" font-weight="900" fill="{p.accent}">{escape(domain.upper())} NEXT STEP</text>',
        *_wrap(ask, 82, 250, 34, 58, p.ink, weight=900, max_lines=3),
        f'<rect x="88" y="512" width="480" height="70" rx="35" fill="{p.primary}"/>',
        f'<text x="126" y="557" font-family="Arial" font-size="24" font-weight="900" fill="#FFFFFF">{escape(_close_label(domain))}</text>',
        f'<circle cx="1032" cy="332" r="168" fill="{p.accent}" opacity="0.24"/>',
        f'<circle cx="1032" cy="332" r="92" fill="{p.primary}" opacity="0.84"/>',
    ]
    return parts


def _background_motif(domain: str, p: Palette, idx: int) -> list[str]:
    if domain in {"financial", "research", "fintech", "esports", "creative"}:
        return [
            f'<circle cx="{1080 - idx * 8}" cy="{118 + idx * 6}" r="190" fill="{p.primary}" opacity="0.12"/>',
            f'<path d="M0 650 C280 610 460 710 740 660 S1040 580 1280 630 L1280 720 L0 720 Z" fill="{p.primary}" opacity="0.08"/>',
        ]
    return [
        f'<circle cx="{1120 - idx * 7}" cy="{126 + idx * 3}" r="150" fill="{p.accent}" opacity="0.16"/>',
        f'<rect x="-80" y="628" width="520" height="180" rx="90" fill="{p.primary}" opacity="0.08"/>',
    ]


def _eyebrow_and_title(role: str, point: str, p: Palette) -> list[str]:
    return [
        f'<text x="76" y="92" font-family="Arial" font-size="18" font-weight="900" fill="{p.primary}">{escape(role.replace("_", " ").upper())}</text>',
        *_wrap(point, 76, 154, 48, 42, p.ink, weight=900, max_lines=2),
    ]


def _wrap(text: str, x: int, y: int, width_chars: int, size: int, fill: str, *, weight: int = 500, max_lines: int = 3) -> list[str]:
    words = str(text).replace("—", "-").split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if len(candidate) > width_chars and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
        if len(lines) >= max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = lines[-1].rstrip(".,;:") + "..."
    return [
        f'<text x="{x}" y="{y + i * int(size * 1.18)}" font-family="Arial" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(line)}</text>'
        for i, line in enumerate(lines)
    ]


def _points_for_slide(points: list[str], idx: int, count: int) -> list[str]:
    if not points:
        return []
    start = max(0, idx - 1)
    return [points[(start + j) % len(points)] for j in range(min(count, len(points)))]


def _role_sequence(domain: str, brief: dict[str, Any], max_slides: int) -> list[str]:
    base = ROLE_SEQUENCES.get(domain, ROLE_SEQUENCES["generic"])
    requested = int(brief.get("n_slides") or min(len(base), max_slides))
    requested = max(3, min(requested, max_slides))
    roles = list(base)
    prefer = [str(x) for x in brief.get("role_prefer") or []]
    for role in prefer:
        mapped = _normalize_role(role)
        if mapped in {"cover", "ask_close", "close", "closing_cta"}:
            continue
        if mapped and mapped not in roles:
            insert_at = max(1, min(len(roles) - 1, len(roles) // 2))
            roles.insert(insert_at, mapped)
    while len(roles) < requested:
        roles.append(f"domain_detail_{len(roles)+1}")
    return roles[:requested]


def _normalize_role(role: str) -> str:
    mapping = {
        "hero_giant_metric": "giant_fun_metric",
        "metric_dashboard": "kpi_dashboard",
        "comparison_split": "comparison_matrix",
        "timeline_horizontal": "roadmap",
        "bullet_card_list": "insight_cards",
        "feature_grid": "feature_grid",
        "closing_cta": "ask_close",
        "hero_quote": "story_quote",
        "cover": "cover",
    }
    return mapping.get(role, role.replace("-", "_"))


def _preferred_categories(domain: str) -> list[str]:
    return {
        "kids": ["diagram", "infographic", "process", "playful"],
        "restaurant": ["layout", "map", "editorial", "infographic"],
        "real_estate": ["gallery", "map", "image", "layout"],
        "financial": ["dashboard", "data", "table", "chart"],
        "legal": ["table", "matrix", "dashboard", "timeline"],
        "research": ["architecture", "process", "academic", "layout"],
        "fintech": ["dashboard", "technical", "network", "data"],
        "esports": ["team", "roster", "neon", "cinematic"],
        "nonprofit": ["story", "impact", "dashboard", "editorial"],
        "healthtech": ["dashboard", "timeline", "comparison", "clinical"],
        "creative": ["collage", "brand", "editorial", "gallery"],
        "product": ["product", "feature", "comparison", "dashboard", "layout"],
    }.get(domain, ["layout", "infographic", "dashboard"])


def _fallback_refs(domain: str) -> list[str]:
    return {
        "kids": ["systematic_logical_flowcharting_85abee35", "whimsical_illustrated_map_infographic_4fffa4cd", "wheel_and_cta_e8f788"],
        "restaurant": ["whimsical_illustrated_map_infographic_4fffa4cd", "vintage_editorial_master_layout_renaissa_6960383b", "thematic_collage_hero_slide_e375482c"],
        "real_estate": ["cinematic_horizontal_gallery_morph_419f9fc2", "whimsical_illustrated_map_infographic_4fffa4cd", "cinematic_spatial_morph_timeline_e51d782d"],
        "financial": ["bi_style_executive_dashboard_kpi_grid_696779ba", "structured_data_clarity_formula_e502a2b7", "odometer_morph_reveal_b7b6b050"],
        "legal": ["tiered_feature_comparison_grid_e76c247e", "one_page_executive_project_status_dashbo_268345ed", "proportional_date_scaled_timeline_af8f3dcf"],
        "research": ["classic_academic_split_layout_399fdc67", "modular_technical_architecture_layout_d133f366", "modern_minimalist_process_funnel_napkin__f5869489"],
        "fintech": ["technical_blueprint_calibration_pattern_7a140774", "tech_dashboard_network_topology_9add4e09", "vertical_metric_stack_c5720e"],
        "esports": ["neon_circular_hub_team_roster_097a0986", "vertical_roster_morph_2b28e4e0", "vibrant_geometric_framed_overlay_8a0c8ef3"],
        "nonprofit": ["testimonial_split_d0fccc", "whimsical_illustrated_map_infographic_4fffa4cd", "vertical_metric_stack_c5720e"],
        "healthtech": ["bi_style_executive_dashboard_kpi_grid_696779ba", "structured_data_clarity_formula_e502a2b7", "proportional_date_scaled_timeline_af8f3dcf"],
        "creative": ["magazine_cut_out_collage_effect_84c8b741", "editorial_grid_layered_composition_26713b2e", "thematic_collage_hero_slide_e375482c"],
        "product": ["dynamic_product_variant_showcase_b6eb2eb7", "tiered_feature_comparison_grid_e76c247e", "hero_metric_infographic_layout_4bc1df4b"],
    }.get(domain, ["editorial_grid_layered_composition_26713b2e", "symmetrical_ribbon_flow_infographic_dcd967ea", "vertical_metric_stack_c5720e"])


def _ref_details(refs: list[str], entries: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    by_id = {str(entry.get("skill_id")): entry for entry in entries}
    details: dict[str, dict[str, str]] = {}
    for ref in refs:
        entry = by_id.get(ref, {})
        category_path = entry.get("category_path") or []
        if isinstance(category_path, list):
            category = " / ".join(str(x) for x in category_path)
        else:
            category = str(category_path)
        details[ref] = {
            "name": str(entry.get("skill_name") or ref),
            "category": category,
            "applicability": str(entry.get("applicability") or "")[:240],
        }
    return details


def _load_skill_entries() -> list[dict[str, Any]]:
    path = ROOT / "skills_wiki" / "ppt" / "index.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        entries = data.get("entries")
        if isinstance(entries, list):
            return entries
    path = ROOT / "skills_library" / "ppt" / "index.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("skills") or []


def _default_briefs() -> list[Path]:
    candidates = [
        "briefs/product_launch.json",
        "briefs/kids_volcano.json",
        "briefs/financial.json",
        "briefs/research.json",
        "briefs_showcase/nonprofit_annual.json",
        "briefs_showcase/legal_partnership_review.json",
        "briefs_showcase/esports_team_intro.json",
        "briefs_showcase/real_estate_listing.json",
        "briefs_showcase/restaurant_launch.json",
        "briefs_showcase/fintech_series_b.json",
    ]
    return [ROOT / p for p in candidates if (ROOT / p).exists()]


def _brief_text(brief: dict[str, Any]) -> str:
    values = [
        brief.get("title", ""),
        brief.get("audience", ""),
        brief.get("archetype_preference", ""),
        " ".join(brief.get("tone_words") or []),
        " ".join(brief.get("mood_preference") or []),
        " ".join(brief.get("role_prefer") or []),
        " ".join(brief.get("role_avoid") or []),
        " ".join(str(x) for x in brief.get("core_points") or []),
    ]
    return " ".join(str(v).lower() for v in values)


def _skill_text(entry: dict[str, Any]) -> str:
    values = [
        entry.get("skill_id", ""),
        entry.get("skill_name", ""),
        entry.get("applicability", ""),
        " ".join(str(x) for x in entry.get("tags") or []),
        " ".join(str(x) for x in entry.get("category_path") or []),
    ]
    source = entry.get("source") or {}
    if isinstance(source, dict):
        values.append(str(source.get("video_title", "")))
    return " ".join(str(v).lower() for v in values)


def _tokens(text: str) -> set[str]:
    stop = {
        "the", "and", "for", "with", "that", "this", "from", "into", "your", "their",
        "slide", "slides", "deck", "presentation", "review", "pitch", "audience",
    }
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 2 and t not in stop}


def _numeric_values(point: str, bullets: list[str]) -> list[str]:
    text = " ".join([point] + bullets)
    found = re.findall(r"[$+]?\d[\d,.]*(?:%|x|K|M|B|bps| wk| mo| sec| min)?", text)
    return (found or ["3", "7", "12", "90%"])[:4]


def _short_label(text: str) -> str:
    words = str(text).split()
    return " ".join(words[:4]) if words else "Core idea"


def _close_label(domain: str) -> str:
    return {
        "kids": "Try the activity",
        "restaurant": "Open the round",
        "real_estate": "Schedule the preview",
        "financial": "Approve the plan",
        "legal": "Record the vote",
        "research": "Discuss the evidence",
        "fintech": "Lead the Series B",
        "esports": "Back the roster",
        "nonprofit": "Become a sustainer",
        "healthtech": "Submit the package",
        "creative": "Choose the direction",
        "product": "Launch the product",
    }.get(domain, "Move forward")


def _svg_shape_count(svg: str) -> int:
    return sum(
        len(re.findall(fr"<{tag}\b", svg, re.I))
        for tag in ("rect", "circle", "ellipse", "path", "polygon", "polyline", "line", "text", "image")
    )


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:60] or "slide"


def _summary_markdown(out_root: Path, summary: list[dict[str, Any]]) -> str:
    lines = ["# PPTMaster x R2S Prompt-Specific Run", "", f"Root: `{out_root}`", ""]
    lines.append("| Case | Domain | Slides | Refs | PPTX |")
    lines.append("| --- | --- | ---: | --- | --- |")
    for entry in summary:
        refs = ", ".join(entry["refs"])
        pptx = entry.get("pptx") or "(not exported)"
        lines.append(f"| {entry['case']} | {entry['domain']} | {entry['slides']} | {refs} | `{pptx}` |")
    lines.append("")
    lines.append("Validate with:")
    lines.append("")
    lines.append("```bash")
    lines.append(f"python domains/ppt/validate_pptmaster_r2s_run.py {out_root / 'summary.json'}")
    lines.append("```")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
