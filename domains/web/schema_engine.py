"""Web schema engine: generate per-brief composition plan, select variants
from the wiki pool, compose into a project, reflect via vision QA.

This implements Layer 1-4 of the Schema+Variant+Reflect architecture
described in docs/schema_variant_reflect_architecture.md.

The engine is stateless — each call takes the brief / project state and
returns a dict. The MCP server wraps it in tools.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.llm import call_azure_openai


# --------------------------------------------------------------------------
# Layer 1: Schema generator
# --------------------------------------------------------------------------
SCHEMA_PROMPT = """You are a senior web designer reading a project brief.
Generate a STRUCTURAL plan (a "schema") for the landing page. The schema
captures section ordering, variant intent, and theme — but is NOT a
template. Different briefs produce different schemas.

Brief:
<<<
{brief}
>>>

Theme hint (optional): {theme_hint}

Output a JSON object with this exact shape:
{{
  "page_archetype": "<one of: marketing_landing | dashboard_app | content_site | ecommerce_product | portfolio>",
  "tone": "<2-3 word vibe, e.g. 'dark cyber', 'warm editorial', 'minimalist clean'>",
  "palette": {{
    "bg":         "<hex>",
    "surface":    "<hex>",
    "accent":     "<hex>",
    "accent_alt": "<hex>",
    "text":       "<hex>",
    "muted":      "<hex>"
  }},
  "motion":  "subtle | moderate | heavy",
  "density": "compact | balanced | airy",
  "sections": [
    {{
      "role":         "<one of: nav, hero, features, pricing, testimonials, integrations, faq, stats, cta, footer, demo_preview, comparison, gallery, about, contact, logo_strip>",
      "variant_hint": "<2-4 keywords describing the visual style of this section, e.g. 'asymmetric_bento_glass', 'gradient_blob_typewriter', 'comparison_matrix_dark'>",
      "props": {{
        "headline":    "<short text the section should display>",
        "body":        "<longer text or description>",
        "cta_label":   "<optional CTA text>",
        "items":       ["<list of feature/testimonial/pricing tier descriptors, when applicable>"],
        "extra":       "<any other section-specific info>"
      }}
    }}
  ]
}}

Rules:
- Pick 5-9 sections appropriate for the page_archetype and the brief.
- Order them naturally (nav first, footer last).
- Each section's `variant_hint` must be specific enough that a downstream
  search returns a relevant skill from the wiki — write it like a search query.
- The palette should reflect the brief's mood (e.g. fintech B2B = navy/teal,
  artist portfolio = warm editorial, healthcare = soft greens, devtool = dark cyber).
- `props.items` only when the section type has multiple items (features, pricing tiers, etc).
- DO NOT use placeholder text ("Lorem ipsum"). Write real content tailored to the brief.
- Keep the JSON STRICTLY valid — no comments, no trailing commas.

Output ONLY the JSON object, nothing else.
"""


def generate_schema(brief: str, theme_hint: str = "") -> dict:
    """Generate a per-brief schema by calling GPT-5.4."""
    prompt = SCHEMA_PROMPT.format(brief=brief, theme_hint=theme_hint or "auto-detect from brief")
    msg = call_azure_openai(
        [{"role": "user", "content": prompt}],
        model="gpt-5.4",
        reasoning_effort="medium",
        max_completion_tokens=4096,
        max_retries=5,
        retry_delay=15.0,
    )
    raw = msg.get("content", "").strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0]
    schema = json.loads(raw)
    if "sections" not in schema or not isinstance(schema["sections"], list):
        raise ValueError("schema missing 'sections' list")
    return schema


# --------------------------------------------------------------------------
# Layer 2: Variant selection
# --------------------------------------------------------------------------
def select_variant(role: str, variant_hint: str, tone: str,
                   wiki_index: list[dict]) -> str | None:
    """Pick the best wiki skill_id for this section role.

    Strategy: simple text-similarity match against skill_name + tags.
    Returns None if no candidates pass a minimum threshold.
    """
    if not wiki_index:
        return None

    role_keywords = {
        "nav":           ["nav", "header", "menu", "navigation", "navbar"],
        "hero":          ["hero", "banner", "landing", "above_fold"],
        "features":      ["feature", "card", "grid", "bento", "showcase"],
        "pricing":       ["pricing", "plan", "tier", "subscription"],
        "testimonials":  ["testimonial", "quote", "review", "social_proof"],
        "integrations":  ["integration", "logo", "partner", "stack"],
        "faq":           ["faq", "accordion", "question", "help"],
        "stats":         ["stat", "metric", "number", "kpi", "counter"],
        "cta":           ["cta", "call_to_action", "signup", "subscribe"],
        "footer":        ["footer", "site_links"],
        "demo_preview":  ["demo", "preview", "screenshot", "mockup"],
        "comparison":    ["comparison", "matrix", "vs", "table"],
        "gallery":       ["gallery", "masonry", "portfolio"],
        "about":         ["about", "team", "story"],
        "contact":       ["contact", "form", "input"],
        "logo_strip":    ["logo", "brand", "client"],
    }
    keywords = role_keywords.get(role, [role])
    hint_tokens = re.findall(r"[a-z]+", variant_hint.lower())
    tone_tokens = re.findall(r"[a-z]+", tone.lower())

    scored: list[tuple[float, dict]] = []
    for entry in wiki_index:
        name = (entry.get("skill_name", "") or "").lower()
        cat  = (entry.get("category", "") or "").lower()
        tags = entry.get("tags") or []
        if isinstance(tags, list):
            tags_text = " ".join(str(t).lower() for t in tags)
        else:
            tags_text = str(tags).lower()
        bag = f"{name} {cat} {tags_text}"
        score = 0.0
        for k in keywords:
            if k in bag: score += 3.0
        for h in hint_tokens:
            if len(h) >= 4 and h in bag: score += 1.0
        for t in tone_tokens:
            if len(t) >= 4 and t in bag: score += 0.5
        if score > 0:
            scored.append((score, entry))

    if not scored:
        return None
    scored.sort(key=lambda x: -x[0])
    # Return top match's skill_id
    return scored[0][1].get("skill_id")


# --------------------------------------------------------------------------
# Layer 4 helper: vision QA prompt for reflect_and_swap
# --------------------------------------------------------------------------
REFLECT_PROMPT = """You are a senior web designer reviewing a rendered
landing page against the original brief.

Brief:
<<<
{brief}
>>>

Schema (sections in order):
{schema_json}

The screenshot shows the current rendered page (may be tall — scroll
through it). Identify the SINGLE WEAKEST section that least matches the
brief's tone or expected visual quality. If all sections are passable
(>= 6/10 each), respond `{{"status": "ok"}}`.

Otherwise respond:
{{
  "status": "swap",
  "section_idx": <int, 0-based index into schema.sections>,
  "reason": "<one short sentence on what's wrong>",
  "new_variant_hint": "<2-4 keyword search query for a better variant>",
  "new_props": {{ <optional: updated headline/body/items if needed> }}
}}

Output STRICTLY a single JSON object, no commentary outside it.
"""


def reflect_qa(brief: str, schema: dict, png_b64: str) -> dict:
    """GPT-5.4 vision QA on rendered page; returns swap decision."""
    msg = call_azure_openai(
        [{"role": "user", "content": [
            {"type": "text", "text": REFLECT_PROMPT.format(
                brief=brief, schema_json=json.dumps(schema, indent=2)
            )},
            {"type": "image_url",
             "image_url": {"url": f"data:image/png;base64,{png_b64}"}},
        ]}],
        model="gpt-5.4",
        reasoning_effort="medium",
        max_completion_tokens=2048,
        max_retries=5,
        retry_delay=15.0,
    )
    raw = msg.get("content", "").strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0]
    return json.loads(raw)


# --------------------------------------------------------------------------
# Layer 5: Theme harmonizer — unified CSS rewriter for cross-skill coordination
# --------------------------------------------------------------------------
HARMONIZE_PROMPT = """You are a senior web designer writing a TWO-LAYER
override stylesheet for a landing page composed of {n_sections} sections.
Each section comes from a different reusable component with its own CSS,
already scoped under `.vws-{{role}}`. Your CSS will sandwich those scoped
rules:

  TOP LAYER (your output, before component CSS): :root tokens, base
  typography, body background, container alignment, link/button defaults.
  Component CSS overrides this for layout/structure.

  BOTTOM LAYER (your output, after component CSS): targeted color/font
  overrides with `!important` ON COLOR PROPERTIES ONLY, to force visual
  cohesion across mismatched component palettes.

Brief:
<<<
{brief}
>>>

Schema:
- page_archetype: {archetype}
- tone: {tone}
- motion: {motion}
- density: {density}
- palette: {palette_json}

Assembled HTML structure (each section is wrapped in `<section class="vws-section vws-{{role}}">`):
<<<
{html_skeleton}
>>>

Output a JSON object with TWO string fields:
{{
  "base_css":     "<top-layer CSS, ~150-250 lines>",
  "override_css": "<bottom-layer CSS, ~80-160 lines>"
}}

base_css MUST contain:
1. `:root {{}}` with --bg, --surface, --accent, --accent-alt, --text, --muted (use the palette EXACTLY as given), plus tasteful semantic vars (--border, --radius, --shadow, --container, --section-pad).
2. `*` reset (box-sizing, margin/padding 0).
3. `html, body` with the schema bg, font stack (Inter + system fallback), text color, line-height, scroll-behavior.
4. **GENEROUS heading scale (avoid tiny text)**:
   - `h1 {{ font-size: clamp(2.6rem, 5.5vw, 4.4rem); line-height: 1.05; letter-spacing: -0.02em; font-weight: 800; }}`
   - `h2 {{ font-size: clamp(2.0rem, 4vw, 3.0rem); line-height: 1.15; font-weight: 700; }}`
   - `h3 {{ font-size: clamp(1.35rem, 2.2vw, 1.65rem); line-height: 1.3; font-weight: 600; }}`
   - `p, li {{ font-size: clamp(1rem, 1.2vw, 1.125rem); line-height: 1.65; }}`
   - h1+, h2+ should have `margin-bottom: 1rem`; section heading + subheading should have generous spacing.
5. `.vws-section` container styles with **generous padding** (max-width: var(--container, 1180px); margin: 0 auto; padding: clamp(64px, 9vw, 120px) clamp(20px, 4vw, 40px)). Each section should breathe.
6. Subtle global animations matching motion={motion} (fade-in-on-load, hover transitions on buttons).

override_css MUST contain ONLY:
1. Color/background/border-color rules using `!important` on common patterns: `.vws-section h1, .vws-section h2, .vws-section h3 {{ color: var(--text) !important; }}`, `.vws-section p, .vws-section li {{ color: var(--text) !important; }}` (or muted for descriptions), `.vws-section a {{ color: var(--accent) !important; }}`, `.vws-section button, .vws-section .btn, .vws-section [class*="cta"] {{ background: var(--accent) !important; color: #fff !important; }}`.
2. Background unification: `.vws-section {{ background: var(--bg) !important; }}` on odd sections; `.vws-section:nth-of-type(even) {{ background: var(--surface) !important; }}` if appropriate (or skip if all same bg suits the tone).
3. Border-radius normalization on cards: `.vws-section [class*="card"], .vws-section .feature, .vws-section [class*="tier"] {{ border-radius: var(--radius) !important; border-color: var(--border) !important; }}`.
4. **TYPOGRAPHY size overrides** with !important to defeat per-component tiny-text decisions: `.vws-section h1 {{ font-size: clamp(2.6rem, 5.5vw, 4.4rem) !important; }}`, `.vws-section h2 {{ font-size: clamp(2.0rem, 4vw, 3.0rem) !important; }}`, `.vws-section p, .vws-section li {{ font-size: clamp(1rem, 1.2vw, 1.125rem) !important; }}`.
5. DO NOT touch layout properties (display, grid-template, flex, width, padding, margin) — let the component CSS decide layout.

Strictly valid JSON. No markdown fences, no commentary outside the JSON.
"""


def harmonize_theme(brief: str, schema: dict, html_skeleton: str) -> tuple[str, str]:
    """Generate two CSS layers (base + override) for cross-skill cohesion.

    Two-tier retry: try the full prompt first; on timeout/failure, try a
    compact prompt with shorter skeleton and lower token budget. This
    eliminates the all-or-nothing fallback path that broke web_04/10.

    Returns:
        (base_css, override_css) tuple. base_css goes BEFORE component CSS;
        override_css goes AFTER, using !important to force palette cohesion
        on color properties only (layout untouched).
    """
    palette = schema.get("palette", {}) or {}
    sections = schema.get("sections", []) or []

    def _attempt(skel_max: int, token_max: int, retries: int) -> tuple[str, str]:
        skel = html_skeleton
        if len(skel) > skel_max:
            skel = skel[:skel_max] + "\n<!-- ...truncated... -->"
        prompt = HARMONIZE_PROMPT.format(
            n_sections=len(sections),
            brief=brief[:1200],
            archetype=schema.get("page_archetype", "marketing_landing"),
            tone=schema.get("tone", ""),
            motion=schema.get("motion", "subtle"),
            density=schema.get("density", "balanced"),
            palette_json=json.dumps(palette),
            html_skeleton=skel,
        )
        msg = call_azure_openai(
            [{"role": "user", "content": prompt}],
            model="gpt-5.4",
            reasoning_effort="medium",
            max_completion_tokens=token_max,
            max_retries=retries,
            retry_delay=10.0,
        )
        raw = msg.get("content", "").strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.rsplit("```", 1)[0]
        obj = json.loads(raw.strip())
        return obj.get("base_css", ""), obj.get("override_css", "")

    # Tier 1: full prompt
    try:
        return _attempt(skel_max=5000, token_max=10240, retries=3)
    except Exception as e1:
        # Tier 2: compact (smaller skeleton, lower tokens, more retries)
        try:
            return _attempt(skel_max=1500, token_max=6144, retries=4)
        except Exception as e2:
            raise RuntimeError(f"harmonize_theme: tier1={e1}; tier2={e2}")


# --------------------------------------------------------------------------
# Cross-skill HTML coordinator: strip per-component <style>/<link>, normalize
# inline styles, and emit clean section markup.
# --------------------------------------------------------------------------
def clean_component_body(body_html: str) -> str:
    """Strip <style>, <link rel=stylesheet>, <script> tags from a component
    body so they don't clobber the unified <head>. Inline `style=` and
    `class=` attributes are KEPT so per-component layout still works.

    The unified style.css is constructed as:
      [base layer from harmonizer]
      [per-component CSS, scoped under .vws-{role}]
      [override layer from harmonizer with !important]
    """
    s = body_html
    # Remove <style>...</style> (we re-inject CSS into <head> via style.css)
    s = re.sub(r"<style\b[^>]*>.*?</style>", "", s, flags=re.DOTALL | re.IGNORECASE)
    # Remove <link rel="stylesheet" ...>
    s = re.sub(r"<link\b[^>]*?rel=[\"']?stylesheet[\"']?[^>]*?/?>", "", s, flags=re.IGNORECASE)
    # Remove <script>...</script> (we move JS separately)
    s = re.sub(r"<script\b[^>]*>.*?</script>", "", s, flags=re.DOTALL | re.IGNORECASE)
    return s


def scope_css_to_section(css: str, role: str) -> str:
    """Crude but effective: prepend `.vws-{role} ` to each top-level CSS
    rule so per-component styles only affect their own section. Skips
    @-rules (media, keyframes, supports, etc.) to keep them at the page level.

    Critical mapping for `body`/`html`/`*` selectors: when a tutorial
    component was authored as a stand-alone page, its `body { ... }` and
    `html { ... }` rules describe how the COMPONENT-as-page looks. In the
    composed page these would all collide on the real `<body>` (one
    component's `background: black` clobbering another's), producing
    visually broken pages. We rewrite:
      body, html  ->  .vws-{role}        (the section IS the "body" now)
      *           ->  .vws-{role} *      (scoped universal)
      :root       ->  :root              (keep — CSS vars are page-level)

    Not a full CSS parser — handles ~95% of well-formed component CSS.
    """
    out = []
    i = 0
    n = len(css)
    scope = f".vws-{role}"
    while i < n:
        # Skip leading whitespace + comments
        while i < n and css[i].isspace():
            out.append(css[i]); i += 1
        if i >= n:
            break
        # Comment
        if css.startswith("/*", i):
            end = css.find("*/", i + 2)
            if end == -1:
                out.append(css[i:])
                break
            out.append(css[i:end+2]); i = end + 2; continue
        # @-rules: keep as-is; copy until matching close brace at depth 0 or ;
        if css[i] == "@":
            # Find selector or end-of-rule
            j = i
            while j < n and css[j] not in "{;":
                j += 1
            if j < n and css[j] == ";":
                out.append(css[i:j+1]); i = j + 1; continue
            if j < n and css[j] == "{":
                # Find matching close brace
                depth = 1
                k = j + 1
                while k < n and depth > 0:
                    if css[k] == "{": depth += 1
                    elif css[k] == "}": depth -= 1
                    k += 1
                # For @media/@supports: scope inner rules; for others (keyframes, font-face), keep as-is
                rule_name = css[i:j].strip().split()[0].lower()
                inner = css[j+1:k-1]
                if rule_name in ("@media", "@supports", "@container"):
                    inner_scoped = scope_css_to_section(inner, role)
                    out.append(f"{css[i:j+1]}{inner_scoped}}}")
                else:
                    out.append(css[i:k])
                i = k; continue
        # Normal rule: selectors { ... }
        j = i
        while j < n and css[j] != "{":
            j += 1
        if j >= n:
            out.append(css[i:])
            break
        selectors = css[i:j].strip()
        # Find matching close brace
        depth = 1
        k = j + 1
        while k < n and depth > 0:
            if css[k] == "{": depth += 1
            elif css[k] == "}": depth -= 1
            k += 1
        body = css[j:k]  # includes outer braces
        # Scope each comma-separated selector
        def _map_sel(s_: str) -> str:
            s_ = s_.strip()
            if not s_:
                return s_
            head_m = re.match(r"([a-zA-Z][\w-]*|\*|:root)\b", s_)
            head = head_m.group(1) if head_m else ""
            tail = s_[head_m.end():] if head_m else s_
            hl = head.lower()
            if hl in ("body", "html"):
                # body { ... }   ->  .vws-{role} { ... }
                # body.dark { }  ->  .vws-{role}.dark { }
                # body > .x { }  ->  .vws-{role} > .x { }
                return f"{scope}{tail}" if tail else scope
            if hl == "*":
                # *  ->  .vws-{role} *
                return f"{scope} *{tail}"
            if hl == ":root":
                return s_  # keep CSS vars at page level
            # generic class/element/etc — descendant selector under scope
            return f"{scope} {s_}"

        scoped = ", ".join(_map_sel(s_) for s_ in selectors.split(",") if s_.strip())
        out.append(f"{scoped} {body}")
        i = k
    return "".join(out)


# --------------------------------------------------------------------------
# Layer 6: Content rewriter — rewrite each section's HTML text content to
# match the schema props (so YouTube-tutorial stub text doesn't leak
# through). This runs AFTER assembly, BEFORE harmonization.
# --------------------------------------------------------------------------
CONTENT_REWRITE_PROMPT = """You are a senior copywriter. Below is the HTML
of a single section of a landing page. Its visible text is generic stub
content from a tutorial. Rewrite the visible text content (text inside
tags only) to match the props below. PRESERVE all HTML tags, classes,
attributes, structure, and DOM nesting EXACTLY. Only change visible text.

Section role: {role}
Brief context: {brief}
Section props (use these as the source of truth for content):
{props_json}

Rules:
- Keep ALL `<tag class=...>` markup, IDs, data-*, aria-*, src, href EXACTLY.
- Replace visible text (between tags, inside `<h*>`, `<p>`, `<li>`, `<a>`,
  `<span>`, `<button>`, `<strong>`, `<em>`, etc.).
- For lists/grids: if props.items is a list of N items but the existing
  HTML has M item slots, fill min(N, M) slots; leave extras with shortened
  generic copy if M > N (do not delete tags).
- Tone: match the brief's vibe. Length: similar to original (don't
  inflate text beyond ~110% of original character count).
- Do NOT add new sections, headings, or images.
- Do NOT touch SVG inner text (icons stay as-is).

Output: the rewritten HTML for this section ONLY (one `<section>...</section>`
block), nothing else.

Original HTML:
<<<
{html}
>>>
"""


def rewrite_section_content(role: str, props: dict, brief: str, section_html: str) -> str:
    """Rewrite the visible text of a section to match schema props.

    Returns the rewritten HTML, or the original if rewriting fails.
    """
    if not props:
        return section_html
    if len(section_html) > 12000:
        # Too big to safely rewrite; skip
        return section_html
    try:
        prompt = CONTENT_REWRITE_PROMPT.format(
            role=role,
            brief=brief[:600],
            props_json=json.dumps(props, ensure_ascii=False),
            html=section_html,
        )
        msg = call_azure_openai(
            [{"role": "user", "content": prompt}],
            model="gpt-5.4",
            reasoning_effort="low",
            max_completion_tokens=4096,
            max_retries=3,
            retry_delay=10.0,
        )
        raw = msg.get("content", "").strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("html"):
                raw = raw[4:]
            raw = raw.rsplit("```", 1)[0]
        raw = raw.strip()
        # Sanity check: must still contain a section tag
        if "<section" in raw.lower() and len(raw) > 100:
            return raw
        return section_html
    except Exception:
        return section_html


# --------------------------------------------------------------------------
# Layer 7: Global polish pass — render the assembled page, ask GPT-5.4
# vision to identify visual problems, return ADDITIONAL override CSS that
# fixes them. Mandatory step at the end of init_web_from_schema.
# --------------------------------------------------------------------------
POLISH_PROMPT = """You are a senior web designer reviewing a RENDERED
landing page. The page is assembled from multiple skills wrapped under
`.vws-section.vws-{{role}}` classes, with a unified palette already applied.

Brief:
<<<
{brief}
>>>

Schema palette: {palette}
Sections present (in order): {section_roles}

The image is the full-page render at 1280x{render_h}. Identify the THREE
most visually-damaging problems and write CSS that fixes them. Common
problems to fix:
- Content squeezed into a narrow column (component CSS often imposes
  `max-width: 300-450px` that the harmonized container cannot override
  without `!important`)
- Overflow / squished text / ridiculously tiny fonts
- Sections collapsing to <100px tall
- Inconsistent backgrounds (one section neon, one beige)
- Buttons invisible against bg
- Text touching edges
- Missing vertical rhythm between sections

Output STRICT JSON:
{{
  "issues": ["<short issue 1>", "<short issue 2>", "<short issue 3>"],
  "fix_css": "<CSS targeting `.vws-section`, `.vws-{{role}} <selector>`, with `!important` only on color/min-height/font-size/padding>"
}}

Constraints on fix_css:
- 60-200 lines.
- Use selectors like `.vws-section`, `.vws-hero`, `.vws-features`, `.vws-section h1`,
  `.vws-section [class*="card"]`, `.vws-{{role}} .specific-class`.
- Layout properties you MAY change: padding, margin, min-height, max-width,
  width, gap. Layout properties you must NOT change: grid-template-*,
  flex-direction, position, transform.
- Use the palette vars (var(--bg), var(--accent), etc).
- Each rule must have at least one `!important` to defeat per-component CSS.
"""


def polish_overrides_from_render(brief: str, schema: dict, png_b64: str) -> dict:
    """Render-aware polish: GPT-5.4 vision returns delta CSS to fix
    issues visible in the rendered page.

    Returns:
        {"issues": [...], "fix_css": "..."}
    """
    sections = schema.get("sections", []) or []
    roles = ", ".join(
        (s.get("role", "?") if isinstance(s, dict) else "?")
        for s in sections
    )
    # Estimate render height from sections (rough)
    render_h = 700 + len(sections) * 320
    prompt = POLISH_PROMPT.format(
        brief=brief[:1000],
        palette=json.dumps(schema.get("palette", {})),
        section_roles=roles,
        render_h=render_h,
    )
    try:
        msg = call_azure_openai(
            [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/png;base64,{png_b64}"}},
            ]}],
            model="gpt-5.4",
            reasoning_effort="low",
            max_completion_tokens=3072,
            max_retries=2,
            retry_delay=8.0,
        )
        raw = msg.get("content", "").strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.rsplit("```", 1)[0]
        return json.loads(raw.strip())
    except Exception as e:
        return {"issues": [f"polish_call_failed: {type(e).__name__}: {str(e)[:120]}"], "fix_css": ""}
