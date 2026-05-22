"""
domains/web/mcp_server/server.py
Web MCP Server — tools for building web pages from skill components.

Tools:
  create_project           — create a project workspace
  write_file               — write/overwrite a file in the project
  read_file                — read a file's content
  add_component_from_skill — execute a skill and inject into project
  render_page              — screenshot via headless Chromium (Playwright)
  inspect_dom              — DOM structure + console errors
  list_skills              — browse skill library
  get_skill_info           — skill metadata + preview
  get_skill_code           — full HTML/CSS/JS code
  save_project             — copy project to demo/web/

Usage (stdio transport):
    python domains/web/mcp_server/server.py --skills-dir skills_library/web
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

_SERVER_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SERVER_DIR.parents[2]
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_SERVER_DIR))

from mcp.server.fastmcp import FastMCP
from core.skill_grounding import append_groundings, MANIFEST_FILENAME, write_manifest

log = logging.getLogger("web-mcp")

# ---------------------------------------------------------------------------
# Lazy imports
# ---------------------------------------------------------------------------

_engine = None
_demo_dir: Path = _PROJECT_ROOT / "demo" / "web"


def _get_engine():
    global _engine
    if not _engine:
        import web_engine
        _engine = web_engine
    return _engine


# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------

_projects: dict[str, dict] = {}  # project_id -> {"dir": Path, "name": str}

# Skills
_skills_dir: Path | None = None
_skill_index: list[dict] | None = None
_skill_metadata: dict | None = None


def _ensure_skills_loaded():
    """Load skill index and metadata from disk if not already loaded."""
    global _skill_index, _skill_metadata
    if _skill_index is not None:
        return

    if not _skills_dir or not _skills_dir.exists():
        _skill_index = []
        _skill_metadata = {}
        return

    # Load index.
    index_path = _skills_dir / "index.json"
    if index_path.exists():
        data = json.loads(index_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            # Wiki format: {"entries": [...]} (list) or {"entries": {...}} (dict).
            # Legacy format: {"skills": [...]} or just a list at top level.
            entries = data.get("entries")
            if isinstance(entries, list):
                _skill_index = entries
            elif isinstance(entries, dict):
                _skill_index = [
                    {"skill_id": sid, **(meta if isinstance(meta, dict) else {})}
                    for sid, meta in entries.items()
                ]
            else:
                _skill_index = data.get("skills", [])
        elif isinstance(data, list):
            _skill_index = data
        else:
            _skill_index = []
    else:
        _skill_index = []

    # Load metadata envelope.
    meta_path = _skills_dir / "metadata.json"
    if meta_path.exists():
        raw = json.loads(meta_path.read_text(encoding="utf-8"))
        _skill_metadata = raw.get("metadata", raw) if isinstance(raw, dict) else {}
    else:
        _skill_metadata = {}


def _scaling_pool_ids() -> set[str] | None:
    """Return the active scaling whitelist, if this server is running under
    experiments/scaling_v1.

    The agent-level pool runtime can gate explicit MCP calls like
    add_component_from_skill(), but init_web_from_schema() selects and applies
    components inside this server process. Filtering the local index here keeps
    schema-based web runs honest under a sampled skill pool.
    """
    pool_file = os.environ.get("SCALING_POOL_FILE")
    if not pool_file:
        return None
    try:
        payload = json.loads(Path(pool_file).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not read SCALING_POOL_FILE=%s: %s", pool_file, exc)
        return None
    ids = payload.get("skill_ids") or []
    return {str(x) for x in ids if x}


def _skill_index_for_active_pool() -> list[dict]:
    _ensure_skills_loaded()
    index = list(_skill_index or [])
    pool = _scaling_pool_ids()
    if pool is None:
        return index
    filtered = [e for e in index if e.get("skill_id") in pool]
    log.info(
        "SCALING_POOL_FILE active: web schema index filtered %d -> %d",
        len(index), len(filtered),
    )
    return filtered


def _component_dir_name(skill_id: str) -> str:
    """Stable, collision-resistant component directory name."""
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(skill_id)).strip("._-")
    return (cleaned or "component")[:96]


def _component_dir_for_skill(project_dir: Path, skill_id: str) -> Path:
    return project_dir / "components" / _component_dir_name(skill_id)


def _schema_intro_html(role: str, props: dict) -> str:
    """Deterministic brief-specific copy layer for composed skill sections.

    We keep the selected skill fragment for visual structure, but prepend a
    small schema-owned layer so the artifact never depends on slow LLM HTML
    rewriting to replace tutorial/stub text.
    """
    props = props or {}

    def esc(value: object) -> str:
        return html_lib.escape(str(value or "").strip(), quote=True)

    headline = esc(props.get("headline", ""))
    body = esc(props.get("body", ""))
    cta = esc(props.get("cta_label", ""))
    items_raw = props.get("items") or []
    items = [str(x).strip() for x in items_raw if str(x).strip()] if isinstance(items_raw, list) else []
    extra = esc(props.get("extra", ""))
    if not any([headline, body, cta, items, extra]):
        return ""

    kicker = role.replace("_", " ").title()
    title_tag = "h1" if role == "hero" else "h2"
    out = [f'<div class="vws-schema-intro vws-schema-intro-{esc(role)}">']
    out.append(f'<p class="vws-schema-kicker">{esc(kicker)}</p>')
    if headline:
        out.append(f"<{title_tag}>{headline}</{title_tag}>")
    if body:
        out.append(f'<p class="vws-schema-lede">{body}</p>')
    if cta:
        out.append(f'<a class="vws-schema-cta" href="#pricing">{cta}</a>')

    if items:
        if role == "faq":
            out.append('<div class="vws-schema-faq-grid">')
            for item in items[:6]:
                question = esc(item.rstrip("?") + "?")
                out.append(
                    "<article>"
                    f"<h3>{question}</h3>"
                    "<p>This answer keeps scope, timing, trust signals, and the "
                    "next step visible so visitors can decide without guesswork.</p>"
                    "</article>"
                )
            out.append("</div>")
        elif role == "pricing":
            prices = ["$19", "$49", "Custom", "$99", "$149", "$249"]
            out.append('<div class="vws-schema-card-grid vws-schema-pricing-grid">')
            for idx, item in enumerate(items[:4]):
                label, _, desc = item.partition(" - ")
                price = prices[idx] if idx < len(prices) else "$49"
                badge = '<span class="vws-schema-badge">Recommended</span>' if idx == 1 else ""
                out.append(
                    f'<article class="{"is-recommended" if idx == 1 else ""}">'
                    f"{badge}<h3>{esc(label)}</h3><strong>{price}</strong>"
                    f"<p>{esc(desc or item)}</p>"
                    "<ul><li>Guided setup</li><li>Priority support</li><li>Usage insights</li></ul>"
                    "</article>"
                )
            out.append("</div>")
        elif role == "testimonials":
            out.append('<div class="vws-schema-card-grid vws-schema-testimonial-grid">')
            for item in items[:3]:
                out.append(f"<article><p>{esc(item)}</p></article>")
            out.append("</div>")
        elif role in {"integrations", "logo_strip"}:
            out.append('<div class="vws-schema-chip-row">')
            for item in items[:8]:
                label = item.split(" for ", 1)[0].split(" - ", 1)[0]
                out.append(f"<span>{esc(label)}</span>")
            out.append("</div>")
        else:
            out.append('<div class="vws-schema-card-grid">')
            for item in items[:6]:
                label, _, desc = item.partition(" with ")
                if not desc:
                    label, _, desc = item.partition(" - ")
                out.append(
                    "<article>"
                    f"<h3>{esc(label[:64])}</h3>"
                    f"<p>{esc(desc or item)}</p>"
                    "</article>"
                )
            out.append("</div>")
    elif extra and role not in {"nav", "footer"}:
        out.append(f'<p class="vws-schema-note">{extra}</p>')

    out.append("</div>")
    return "\n".join(out)


def _display_name_from_brief(brief: str, fallback: str) -> str:
    """Extract a presentable brand/person/place name without sample-specific rules."""
    text = str(brief or "")
    patterns = [
        r"\bcalled\s+([A-Z][A-Za-z0-9&'’.-]*(?:\s+[A-Z][A-Za-z0-9&'’.-]*){0,3})",
        r"\bnamed\s+([A-Z][A-Za-z0-9&'’.-]*(?:\s+[A-Z][A-Za-z0-9&'’.-]*){0,3})",
        r"\bfor\s+(?:a|an|the)?\s*[a-z -]{0,40}\s+called\s+([A-Z][A-Za-z0-9&'’.-]*(?:\s+[A-Z][A-Za-z0-9&'’.-]*){0,3})",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            name = re.split(r"\s+(?:that|with|aimed|focused|using|Save|Aim)\b|[,.;:]", m.group(1))[0]
            name = re.sub(r"\s+", " ", name).strip(" -_")
            if name:
                return html_lib.escape(name, quote=True)

    cleaned = re.sub(r"_(?:with|without)_skills$", "", str(fallback), flags=re.I)
    cleaned = re.sub(r"-(?:with|without)-skills$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"[_-]?\d+$", "", cleaned)
    cleaned = cleaned.replace("_", " ").replace("-", " ").strip()
    return html_lib.escape((cleaned or "Product").title(), quote=True)


def _focus_phrase_from_brief(brief: str, product_name: str) -> str:
    """Short, visible phrase for generic polish copy."""
    text = re.sub(r"\s+", " ", str(brief or "")).strip()
    m = re.search(r"Aim for a vibe that is ([^.]+)\.", text, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"\b(?:for|about)\s+([^.,;]{10,90})", text, re.I)
    if m:
        phrase = re.sub(r"\bcalled\s+" + re.escape(html_lib.unescape(product_name)) + r"\b", "", m.group(1), flags=re.I)
        phrase = re.sub(r"\s+", " ", phrase).strip(" -")
        if phrase:
            return phrase[:90]
    return "the core promise"


def _insert_before_footer_or_close(html: str, insert: str) -> str:
    """Place injected polish sections in the content flow, never below footer."""
    footer_match = re.search(r"<footer\b", html, re.I)
    if footer_match:
        return html[:footer_match.start()] + insert + "\n" + html[footer_match.start():]

    vws_footer_match = re.search(
        r"<section\b[^>]*class=\"[^\"]*\bvws-footer\b[^\"]*\"",
        html,
        re.I,
    )
    if vws_footer_match:
        return html[:vws_footer_match.start()] + insert + "\n" + html[vws_footer_match.start():]

    for marker in ("<script src=\"script.js\"></script>", "</body>", "</html>"):
        idx = html.lower().find(marker.lower())
        if idx >= 0:
            return html[:idx] + insert + "\n" + html[idx:]
    return html + insert


def _deterministic_theme_css(schema: dict) -> tuple[str, str]:
    """Fast schema-aware CSS harmonizer used by default for experiments."""
    palette = schema.get("palette", {}) or {}
    bg = palette.get("bg") or palette.get("bg_primary") or "#0a0f1a"
    surface = palette.get("surface") or palette.get("bg_surface") or "#121c2a"
    accent = palette.get("accent") or "#5eead4"
    accent_alt = palette.get("accent_alt") or "#7c5cff"
    text = palette.get("text") or palette.get("text_primary") or "#f5f7ff"
    muted = palette.get("muted") or "#a7b0c8"
    density = str(schema.get("density", "balanced")).lower()
    pad = "clamp(56px, 7vw, 96px)" if density == "compact" else "clamp(72px, 9vw, 128px)"
    base_css = f""":root {{
  --bg: {bg};
  --surface: {surface};
  --accent: {accent};
  --accent-alt: {accent_alt};
  --text: {text};
  --muted: {muted};
  --border: color-mix(in srgb, var(--text) 16%, transparent);
  --shadow: 0 18px 70px rgba(0,0,0,.28);
  --container: 1200px;
  --section-pad: {pad};
  --radius: 12px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
  min-width: 320px;
  background:
    radial-gradient(circle at 14% 6%, color-mix(in srgb, var(--accent) 26%, transparent), transparent 34rem),
    radial-gradient(circle at 86% 18%, color-mix(in srgb, var(--accent-alt) 22%, transparent), transparent 32rem),
    var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}}
img, svg, canvas, video {{ max-width: 100%; height: auto; }}
a {{ color: inherit; }}
.vws-section {{
  width: 100%;
  padding: var(--section-pad) clamp(20px, 4vw, 44px);
  position: relative;
  isolation: isolate;
}}
.vws-section > * {{
  max-width: min(var(--container), 100%);
  margin-inline: auto;
}}
.vws-section:nth-of-type(even) {{
  background: color-mix(in srgb, var(--surface) 72%, transparent);
}}
.vws-section h1 {{
  font-size: clamp(3rem, 7vw, 5.8rem);
  line-height: .96;
  letter-spacing: 0;
  font-weight: 850;
}}
.vws-section h2 {{
  font-size: clamp(2.1rem, 4.6vw, 4.1rem);
  line-height: 1.04;
  letter-spacing: 0;
  font-weight: 820;
}}
.vws-section h3 {{
  font-size: clamp(1.12rem, 1.5vw, 1.45rem);
  line-height: 1.2;
  letter-spacing: 0;
}}
.vws-section p,
.vws-section li {{
  font-size: clamp(1rem, 1.05vw, 1.1rem);
  line-height: 1.62;
}}
.vws-schema-intro {{
  display: grid;
  gap: clamp(16px, 2vw, 26px);
  margin-bottom: clamp(28px, 4vw, 56px);
}}
.vws-schema-intro-hero {{
  grid-template-columns: minmax(0, .95fr) minmax(320px, 1.05fr);
  align-items: center;
  min-height: 520px;
}}
.vws-schema-intro-hero .vws-schema-card-grid,
.vws-schema-intro-hero .vws-schema-chip-row {{
  grid-column: 2;
  grid-row: 1 / span 4;
}}
.vws-schema-kicker {{
  width: fit-content;
  color: var(--accent);
  font-size: .78rem !important;
  font-weight: 850;
  letter-spacing: .1em !important;
  text-transform: uppercase;
}}
.vws-schema-lede {{
  max-width: 62ch;
  color: var(--muted);
}}
.vws-schema-cta {{
  width: fit-content;
  min-height: 46px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 22px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--accent), var(--accent-alt));
  color: #061016;
  text-decoration: none;
  font-weight: 850;
  box-shadow: var(--shadow);
}}
.vws-schema-card-grid,
.vws-schema-faq-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: clamp(14px, 2vw, 22px);
}}
.vws-schema-card-grid article,
.vws-schema-faq-grid article {{
  min-height: 150px;
  padding: clamp(18px, 2.4vw, 28px);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: linear-gradient(145deg, color-mix(in srgb, var(--surface) 90%, white 6%), color-mix(in srgb, var(--surface) 72%, transparent));
  box-shadow: var(--shadow);
}}
.vws-schema-card-grid article h3,
.vws-schema-faq-grid article h3 {{
  margin-bottom: .65rem;
}}
.vws-schema-pricing-grid article strong {{
  display: block;
  margin: .4rem 0 .8rem;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1;
}}
.vws-schema-pricing-grid article.is-recommended {{
  border-color: color-mix(in srgb, var(--accent) 70%, white 10%);
  box-shadow: 0 24px 90px color-mix(in srgb, var(--accent) 24%, transparent);
}}
.vws-schema-badge {{
  display: inline-flex;
  margin-bottom: 14px;
  padding: 5px 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--accent) 22%, transparent);
  color: var(--accent);
  font-size: .76rem !important;
  font-weight: 850;
}}
.vws-schema-chip-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}}
.vws-schema-chip-row span {{
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  padding: 0 15px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: color-mix(in srgb, var(--surface) 74%, transparent);
  color: var(--muted);
  font-weight: 750;
}}
.vws-skill-fragment {{
  max-width: min(var(--container), 100%);
  margin-inline: auto;
}}
@media (max-width: 860px) {{
  .vws-schema-intro-hero {{ grid-template-columns: 1fr; min-height: auto; }}
  .vws-schema-intro-hero .vws-schema-card-grid,
  .vws-schema-intro-hero .vws-schema-chip-row {{ grid-column: auto; grid-row: auto; }}
}}
"""
    override_css = """/* ===== DETERMINISTIC OVERRIDE LAYER ===== */
.vws-section h1,
.vws-section h2,
.vws-section h3 { color: var(--text) !important; letter-spacing: 0 !important; }
.vws-section p,
.vws-section li { color: var(--muted) !important; }
.vws-section a { text-decoration-thickness: 1px; text-underline-offset: 4px; }
.vws-section button,
.vws-section .btn,
.vws-section [class*="cta"] {
  border-color: color-mix(in srgb, var(--accent) 50%, transparent) !important;
}
.vws-section [class*="card"],
.vws-section article,
.vws-section [class*="tier"],
.vws-section [class*="panel"] {
  border-color: var(--border) !important;
}
.vws-section h1 { font-size: clamp(3rem, 7vw, 5.8rem) !important; }
.vws-section h2 { font-size: clamp(2.1rem, 4.6vw, 4.1rem) !important; }
.vws-section p,
.vws-section li { font-size: clamp(1rem, 1.05vw, 1.1rem) !important; }
"""
    return base_css, override_css


# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("web-mcp")


def _auto_polish_project(project_id: str) -> str:
    """Deterministic final polish pass for composed skill pages.

    The schema path already gives the agent good components; this pass makes
    the combined artifact read as one product surface: consistent type scale,
    dense CTAs, visible mockup/proof section, and a short FAQ if the selected
    component set did not provide one.
    """
    proj = _projects.get(project_id)
    if proj is None:
        return "polish skipped: project not found"
    root = proj["dir"]
    html_path = root / "index.html"
    css_path = root / "style.css"
    if not html_path.exists():
        return "polish skipped: index.html missing"

    html = html_path.read_text(encoding="utf-8", errors="ignore")
    original_html = html
    css = css_path.read_text(encoding="utf-8", errors="ignore") if css_path.exists() else ""
    if "VWS_FINAL_POLISH_V3" in html and "VWS_FINAL_POLISH_V3" in css:
        return "polish already applied"

    brief = str(proj.get("brief") or proj.get("name") or "product").strip()
    product_name = _display_name_from_brief(brief, str(proj.get("name") or "Product"))
    focus_phrase = html_lib.escape(_focus_phrase_from_brief(brief, product_name), quote=True)

    nav_html = f"""
<nav class="vws-polished-nav" data-vws-polish="nav">
  <a class="vws-polished-brand" href="#top">{product_name}</a>
  <div class="vws-polished-links">
    <a href="#features">Features</a>
    <a href="#integrations">Integrations</a>
    <a href="#pricing">Pricing</a>
    <a href="#faq">FAQ</a>
  </div>
  <a class="vws-polished-nav-cta" href="#pricing">Start free</a>
</nav>
"""
    html = re.sub(
        r"<section([^>]*)class=\"([^\"]*\bvws-nav\b[^\"]*)\"[^>]*>.*?</section>",
        nav_html,
        html,
        count=1,
        flags=re.S | re.I,
    )

    footer_html = f"""
<footer class="vws-polished-footer" data-vws-polish="footer">
  <strong>{product_name}</strong>
  <span>{focus_phrase.title()} with clear proof, details, and next steps.</span>
  <div>
    <a href="#features">Product</a>
    <a href="#pricing">Plans</a>
    <a href="#faq">Support</a>
    <a href="#top">Back to top</a>
  </div>
</footer>
"""
    html = re.sub(
        r"<section([^>]*)class=\"([^\"]*\bvws-footer\b[^\"]*)\"[^>]*>.*?</section>",
        footer_html,
        html,
        count=1,
        flags=re.S | re.I,
    )

    injected_sections: list[str] = []
    html_lower = html.lower()
    section_count_before = len(re.findall(r"<(section|nav|header|footer)\b", html, re.I))
    has_product_visual = any(
        k in html_lower
        for k in (
            "vws-product-proof", "data-vws-polish=\"interface-preview\"",
            "mockup", "showcase", "gallery", "bento", "product-preview",
            "interface", "phone-frame", "dashboard", "logo-row",
        )
    )
    if not has_product_visual or section_count_before < 7:
        injected_sections.append(f"""
<section id="integrations" class="vws-section vws-product-proof" data-vws-polish="interface-preview">
  <div class="vws-proof-copy">
    <p class="vws-kicker">Signature proof</p>
    <h2>{product_name} makes the promise tangible.</h2>
    <p>A compact visual layer connects the requested {focus_phrase} mood with concrete benefits, proof points, and the next action.</p>
  </div>
  <div class="vws-ui-mockup" aria-label="Product interface preview">
    <div class="vws-ui-topbar"><span></span><span></span><span></span></div>
    <div class="vws-ui-grid">
      <div class="vws-ui-card vws-ui-card-wide"><strong>Signature moment</strong><em>01</em><i></i></div>
      <div class="vws-ui-card"><strong>Trust cue</strong><em>92%</em><i></i></div>
      <div class="vws-ui-card"><strong>Next step</strong><em>Clear</em><i></i></div>
      <div class="vws-ui-chart"><span></span><span></span><span></span><span></span><span></span></div>
    </div>
  </div>
</section>
""")
    if "faq" not in html_lower and "question" not in html_lower:
        injected_sections.append(f"""
<section id="faq" class="vws-section vws-faq" data-vws-polish="faq">
  <p class="vws-kicker">Decision support</p>
  <h2>Questions before choosing {product_name}</h2>
  <div class="vws-faq-grid">
    <article><h3>What makes {product_name} different?</h3><p>The experience keeps the requested mood, concrete details, and primary action visible instead of relying on generic claims.</p></article>
    <article><h3>Who is it designed for?</h3><p>It is framed for visitors who care about {focus_phrase} and need a fast way to understand fit, value, and next steps.</p></article>
    <article><h3>What should visitors do next?</h3><p>The page points toward one confident action while still giving enough context to compare, trust, and decide.</p></article>
  </div>
</section>
""")

    if injected_sections:
        insert = "\n<!-- VWS_FINAL_POLISH_V3 injected sections -->\n" + "\n".join(injected_sections)
        html = _insert_before_footer_or_close(html, insert)
    if html != original_html:
        html_path.write_text(html, encoding="utf-8")

    polish_css = """

/* VWS_FINAL_POLISH_V3 */
:root {
  --vws-polish-bg: color-mix(in srgb, var(--bg, #080b14) 88%, #05070d 12%);
  --vws-polish-surface: color-mix(in srgb, var(--surface, #111827) 82%, white 6%);
  --vws-polish-border: rgba(255,255,255,.12);
  --vws-polish-text: var(--text, #f7f9ff);
  --vws-polish-muted: color-mix(in srgb, var(--text, #f7f9ff) 72%, transparent);
  --vws-polish-accent: var(--accent, #64d8ff);
}
html { background: var(--vws-polish-bg); }
body {
  min-width: 320px;
  overflow-x: hidden;
  text-rendering: optimizeLegibility;
}
body > .vws-section {
  position: relative;
  isolation: isolate;
  padding-block: clamp(72px, 9vw, 132px) !important;
  padding-inline: clamp(20px, 4vw, 48px) !important;
}
body > .vws-section > * {
  max-width: min(1180px, 100%);
  margin-inline: auto;
}
.fade-up,
.fade-in,
.reveal,
.reveal-up,
.scroll-reveal,
.js-reveal,
[data-animate],
[data-aos],
[data-reveal],
[data-scroll-reveal] {
  opacity: 1 !important;
  transform: none !important;
  visibility: visible !important;
}
.vws-section h1 {
  max-width: 11ch;
  font-size: clamp(48px, 7vw, 92px) !important;
  line-height: .93 !important;
  letter-spacing: 0 !important;
}
.vws-section h2 {
  max-width: 15ch;
  font-size: clamp(32px, 4vw, 58px) !important;
  line-height: 1.02 !important;
  letter-spacing: 0 !important;
}
.vws-section h3 { font-size: clamp(18px, 1.5vw, 24px) !important; line-height: 1.18 !important; }
.vws-section p,
.vws-section li,
.vws-section span {
  font-size: max(15px, 1rem) !important;
  line-height: 1.58 !important;
}
.vws-section a,
.vws-section button,
.vws-section [class*="btn"],
.vws-section [class*="cta"] {
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .55rem;
  border-radius: 999px;
  font-weight: 750;
  text-decoration: none;
  white-space: nowrap;
}
.vws-section [class*="card"],
.vws-section article,
.vws-section .vws-ui-mockup {
  border: 1px solid var(--vws-polish-border);
  background: color-mix(in srgb, var(--vws-polish-surface) 82%, transparent);
  box-shadow: 0 18px 60px rgba(0,0,0,.22);
}
.vws-polished-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  width: min(1180px, calc(100% - 32px));
  margin: 16px auto 0;
  padding: 12px 14px 12px 18px;
  border: 1px solid var(--vws-polish-border);
  border-radius: 999px;
  background: color-mix(in srgb, var(--vws-polish-bg) 74%, transparent);
  backdrop-filter: blur(18px);
  box-shadow: 0 10px 40px rgba(0,0,0,.2);
}
.vws-polished-brand,
.vws-polished-nav a {
  color: var(--vws-polish-text);
  text-decoration: none;
}
.vws-polished-brand {
  font-weight: 850;
  letter-spacing: 0 !important;
}
.vws-polished-links {
  display: flex;
  align-items: center;
  gap: clamp(14px, 2vw, 26px);
}
.vws-polished-links a {
  color: var(--vws-polish-muted);
  font-size: 14px !important;
  font-weight: 650;
}
.vws-polished-nav-cta {
  min-height: 38px;
  padding: 0 18px;
  border-radius: 999px;
  background: var(--vws-polish-accent);
  color: #061018 !important;
  font-weight: 800;
}
.vws-product-proof {
  display: grid !important;
  grid-template-columns: minmax(0, .9fr) minmax(320px, 1.1fr);
  gap: clamp(28px, 5vw, 72px);
  align-items: center;
}
.vws-kicker {
  color: var(--vws-polish-accent) !important;
  font-size: 13px !important;
  font-weight: 800;
  letter-spacing: .12em !important;
  text-transform: uppercase;
  margin-bottom: 14px;
}
.vws-ui-mockup {
  border-radius: 24px;
  padding: 18px;
  min-height: 390px;
  overflow: hidden;
}
.vws-ui-topbar {
  height: 36px;
  display: flex;
  gap: 8px;
  border-bottom: 1px solid var(--vws-polish-border);
  margin: -2px -2px 18px;
}
.vws-ui-topbar span {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--vws-polish-accent);
  opacity: .85;
}
.vws-ui-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.vws-ui-card,
.vws-ui-chart {
  min-height: 118px;
  border-radius: 18px;
  border: 1px solid var(--vws-polish-border);
  background: linear-gradient(145deg, rgba(255,255,255,.13), rgba(255,255,255,.035));
  padding: 18px;
}
.vws-ui-card-wide { grid-column: span 3; display: grid; grid-template-columns: 1fr auto; align-items: start; }
.vws-ui-card strong { color: var(--vws-polish-muted); }
.vws-ui-card em { font-size: 38px; color: var(--vws-polish-text); font-style: normal; font-weight: 850; }
.vws-ui-card i {
  grid-column: 1 / -1;
  height: 8px;
  margin-top: 18px;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--vws-polish-accent), transparent 72%);
}
.vws-ui-chart { grid-column: span 3; min-height: 150px; display: flex; align-items: end; gap: 10px; }
.vws-ui-chart span {
  flex: 1;
  border-radius: 10px 10px 0 0;
  background: linear-gradient(180deg, var(--vws-polish-accent), rgba(255,255,255,.12));
}
.vws-ui-chart span:nth-child(1) { height: 38%; }
.vws-ui-chart span:nth-child(2) { height: 58%; }
.vws-ui-chart span:nth-child(3) { height: 46%; }
.vws-ui-chart span:nth-child(4) { height: 74%; }
.vws-ui-chart span:nth-child(5) { height: 88%; }
.vws-faq-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}
.vws-faq article {
  border-radius: 18px;
  padding: clamp(20px, 3vw, 28px);
}
.vws-polished-footer {
  width: min(1180px, calc(100% - 40px));
  margin: 48px auto 36px;
  padding: 26px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  border-top: 1px solid var(--vws-polish-border);
  color: var(--vws-polish-muted);
}
.vws-polished-footer strong {
  color: var(--vws-polish-text);
  font-size: 18px;
}
.vws-polished-footer div {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
}
.vws-polished-footer a {
  color: var(--vws-polish-muted);
  text-decoration: none;
  font-size: 14px !important;
}
@media (max-width: 820px) {
  .vws-product-proof,
  .vws-faq-grid { grid-template-columns: 1fr !important; }
  .vws-section h1 { max-width: 12ch; font-size: clamp(42px, 13vw, 70px) !important; }
  .vws-section h2 { max-width: 16ch; font-size: clamp(30px, 9vw, 48px) !important; }
  .vws-ui-grid { grid-template-columns: 1fr; }
  .vws-ui-card-wide,
  .vws-ui-chart { grid-column: auto; }
  .vws-polished-links { display: none; }
  .vws-polished-footer { align-items: flex-start; flex-direction: column; }
}
"""
    if "VWS_FINAL_POLISH_V3" not in css:
        css_path.write_text(css + polish_css, encoding="utf-8")

    section_count = len(re.findall(r"<(section|nav|header|footer)\b", html, re.I))
    return (
        f"polish applied: injected_sections={len(injected_sections)}, "
        f"sections={section_count}, css_bytes={css_path.stat().st_size if css_path.exists() else 0}"
    )


# ---- Backend reload controller --------------------------------------------

_startup_backend: str | None = None
_wiki_tools_registered: bool = False


def _rebuild_runtime() -> dict:
    """Re-resolve _skills_dir from the current library_backend, refresh
    caches, and toggle the universal wiki tool surface to match.

    Operator-facing AC-13 recovery path: a flip in domain.yaml followed
    by ``reload_registry`` swaps the served registry without restart.
    """
    global _skills_dir, _wiki_tools_registered, _skill_index, _skill_metadata
    info: dict = {"reloaded": True}
    try:
        from core import get_active_library_backend, get_library_dir
        backend = get_active_library_backend("web")
        _skills_dir = get_library_dir("web").resolve()
    except Exception as exc:  # noqa: BLE001
        info["error"] = f"backend resolve failed: {type(exc).__name__}: {exc}"
        return info
    info["backend"] = backend
    info["skills_dir"] = str(_skills_dir)

    # Drop legacy library caches so subsequent _ensure_skills_loaded()
    # reads the new on-disk index.json/metadata.json.
    _skill_index = None
    _skill_metadata = None

    try:
        from domains.web.wiki_adapter import WebWikiAdapter
        from core.skill_wiki.mcp_tools import register_wiki_tools, _OWNED_NAMES
        from core.skill_wiki.legacy_stale import mark_runtime_backend
    except ImportError as exc:
        info["adapter_error"] = f"adapter import failed: {exc}"
        return info

    rebuild_succeeded = False
    if backend == "wiki":
        try:
            adapter = WebWikiAdapter()
            adapter.reload()
            register_wiki_tools(mcp, adapter)
            _wiki_tools_registered = True
            info["adapter_reloaded"] = True
            info["tool_surface"] = "wiki"
            rebuild_succeeded = True
        except Exception as exc:  # noqa: BLE001
            info["adapter_reloaded"] = False
            info["adapter_error"] = f"{type(exc).__name__}: {exc}"
    else:
        if _wiki_tools_registered:
            manager = getattr(mcp, "_tool_manager", None)
            tools = getattr(manager, "_tools", {}) if manager else {}
            for name in _OWNED_NAMES:
                tools.pop(name, None)
            _wiki_tools_registered = False
        info["tool_surface"] = "legacy"
        rebuild_succeeded = True

    # Only re-key the stale guard if the rebuild succeeded. A failed wiki
    # registration must leave guarded legacy tools returning stale_registry.
    if rebuild_succeeded:
        mark_runtime_backend(mcp, backend)
    else:
        info["stale_guard_left_armed"] = True
    return info


@mcp.tool()
def reload_registry() -> dict:
    """Recover after a ``library_backend`` flip or external registry update.

    Re-reads the configured backend, recomputes the served skills directory,
    and rebuilds the MCP tool surface to match. Exempt from the legacy
    stale guard so it remains callable after a flip.
    """
    return _rebuild_runtime()


# ---- Project management ---------------------------------------------------

@mcp.tool()
def create_project(name: str = "my_project") -> str:
    """Create a new web project workspace with starter files.

Args:
    name: Project name (used for directory naming).

Returns:
    Project ID and path, or error message.
"""
    project_id = f"proj_{uuid.uuid4().hex[:8]}"
    project_dir = Path(tempfile.mkdtemp(prefix=f"web_{name}_"))

    # Create starter files.
    (project_dir / "index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Components will be added here -->
    <script src="script.js"></script>
</body>
</html>""",
        encoding="utf-8",
    )
    (project_dir / "style.css").write_text(
        """/* Global styles */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; }
""",
        encoding="utf-8",
    )
    (project_dir / "script.js").write_text(
        "// Main script\n", encoding="utf-8"
    )

    _projects[project_id] = {"dir": project_dir, "name": name}
    write_manifest(project_dir / MANIFEST_FILENAME, {
        "domain": "web",
        "project_id": project_id,
        "project_name": name,
        "groundings": [],
    }, domain="web")
    return f"Created project '{name}' (id: {project_id}) at {project_dir} with index.html, style.css, script.js"


@mcp.tool()
def write_file(
    project_id: str,
    filename: str,
    content: str,
    from_skill_ids: str = "",
    target_node: str = "",
    adaptation_notes: str = "",
) -> str:
    """Write or overwrite a file in the project workspace.

Args:
    project_id: Project ID from create_project.
    filename: Filename (e.g., 'style.css', 'components/hero.html').
    content: File content to write.
    from_skill_ids: optional JSON/comma list of inspected wiki skill ids whose
        mechanisms were adapted in this file write.
    target_node: optional section/role target, or JSON/comma list for multiple
        sections (e.g. ["nav","hero","pricing"]).
    adaptation_notes: optional note describing the borrowed mechanisms.

Returns:
    Confirmation with byte count, or error.
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    project_dir = proj["dir"]
    file_path = project_dir / filename

    # Safety: prevent path traversal.
    try:
        file_path.resolve().relative_to(project_dir.resolve())
    except ValueError:
        return f"Error: path '{filename}' escapes the project directory"

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    entries = append_groundings(
        project_dir / MANIFEST_FILENAME,
        domain="web",
        tool_name="write_file",
        from_skill_ids=from_skill_ids,
        target_node=target_node,
        adaptation_notes=adaptation_notes,
        fallback_target=filename,
        extra={"filename": filename},
    )
    suffix = f"; grounded_sections={len(entries)}" if entries else ""
    return f"Written {len(content)} bytes to {filename}{suffix}"


@mcp.tool()
def read_file(project_id: str, filename: str) -> str:
    """Read a file's content from the project workspace.

Args:
    project_id: Project ID.
    filename: Filename to read.

Returns:
    File content, or error.
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    file_path = proj["dir"] / filename
    if not file_path.exists():
        return f"Error: file '{filename}' not found"

    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def add_component_from_skill(
    project_id: str,
    skill_id: str,
    content_brief: str = "",
    style_hints: str = "",
) -> str:
    """Add a component to the project by executing a skill from the library.

The skill's create_component() function is called with parameters derived
from content_brief and style_hints. The output HTML/CSS/JS is written into
a component subdirectory in the project.

Args:
    project_id: Project ID.
    skill_id: Skill ID from list_skills.
    content_brief: Text content for the component (title, body, etc.).
    style_hints: Style preferences (e.g., 'dark theme, accent #00bfff').

Returns:
    Confirmation with files created, or error.
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    _ensure_skills_loaded()
    engine = _get_engine()

    detail = engine.get_skill_detail(_skills_dir, skill_id, _skill_index or [])

    # Wiki backend fallback: legacy detail.json doesn't exist; read code from
    # text/overview.md (the gemini analysis is the canonical store for wiki).
    if not detail and _skills_dir:
        wiki_overview = _skills_dir / skill_id / "text" / "overview.md"
        wiki_meta = _skills_dir / skill_id / "meta.json"
        if wiki_overview.exists():
            detail = {
                "analysis": wiki_overview.read_text(encoding="utf-8"),
                "skill_name": skill_id,
            }
            if wiki_meta.exists():
                try:
                    m = json.loads(wiki_meta.read_text(encoding="utf-8"))
                    detail["skill_name"] = m.get("skill_name", skill_id)
                except Exception:
                    pass

    if not detail:
        return f"Error: skill '{skill_id}' not found"

    code = engine.extract_code_from_analysis(detail.get("analysis", ""))
    if not code:
        return f"Error: no code found in skill '{skill_id}'"

    # Build params from content_brief.
    params = {}
    if content_brief:
        lines = content_brief.strip().split("\n")
        params["title_text"] = lines[0][:80]
        if len(lines) > 1:
            params["body_text"] = "\n".join(lines[1:])[:500]
    if style_hints:
        params["style"] = style_hints
        # Extract color hints.
        color_m = re.search(r"#([0-9a-fA-F]{6})", style_hints)
        if color_m:
            params["accent_color"] = f"#{color_m.group(1)}"
        if "dark" in style_hints.lower():
            params["color_scheme"] = "dark"
        elif "light" in style_hints.lower():
            params["color_scheme"] = "light"

    # Execute skill code.
    skill_name = detail.get("skill_name", skill_id)
    component_dir = _component_dir_for_skill(proj["dir"], skill_id)
    success, files = engine.exec_skill_code(code, str(component_dir), params)

    if not success:
        err_msg = files[0] if files else "Unknown error"
        return f"Error executing skill '{skill_name}': {err_msg}"

    append_groundings(
        proj["dir"] / MANIFEST_FILENAME,
        domain="web",
        tool_name="add_component_from_skill",
        from_skill_ids=[skill_id],
        target_node=_component_dir_name(skill_id),
        adaptation_notes=style_hints or content_brief[:160],
        extra={"component_dir": str(component_dir.name), "skill_name": skill_name},
    )
    return f"Added component from skill '{skill_name}' ({len(files)} files: {', '.join(files)})"


# ---- Rendering & inspection -----------------------------------------------

@mcp.tool()
def render_page(project_id: str, width: int = 1280, height: int = 800) -> str:
    """Render the project's index.html to a PNG screenshot via headless Chromium.

Requires Playwright to be installed (`pip install playwright && playwright install chromium`).

Args:
    project_id: Project ID.
    width: Viewport width in pixels.
    height: Viewport height in pixels.

Returns:
    A short text summary with the screenshot path + page dimensions. The
    raw PNG is saved to disk (under the project's ``_renders/``) but is NOT
    inlined into the agent context — base64 PNGs blow the input-token cap
    after a couple of renders. Tools that need pixels (visual QA hooks,
    schema reflect_and_swap) read the file directly.
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    index_path = proj["dir"] / "index.html"
    if not index_path.exists():
        return "Error: index.html not found in project"

    import subprocess
    import sys as _sys
    import tempfile
    runner = (
        "from playwright.sync_api import sync_playwright\n"
        "import sys\n"
        "url = sys.argv[1]; out = sys.argv[2]; w = int(sys.argv[3]); h = int(sys.argv[4])\n"
        "with sync_playwright() as p:\n"
        "    b = p.chromium.launch(headless=True)\n"
        "    page = b.new_page(viewport={'width': w, 'height': h})\n"
        "    page.goto(url)\n"
        "    try: page.wait_for_load_state('networkidle', timeout=10000)\n"
        "    except Exception: pass\n"
        "    # Force any scroll-triggered fade-in / reveal animations to be\n"
        "    # visible. Without this, sections with .fade-in / .reveal /\n"
        "    # data-animate stay at opacity:0 in the screenshot, making the\n"
        "    # page look half-empty even though the markup is dense.\n"
        "    page.add_style_tag(content='*{animation:none!important;transition:none!important;}.fade-up,.fade-in,.reveal,.reveal-up,.scroll-reveal,.js-reveal,.animate,[data-animate],[data-aos],[data-reveal],[data-scroll-reveal]{opacity:1!important;transform:none!important;visibility:visible!important;}')\n"
        "    page.screenshot(path=out, full_page=True)\n"
        "    info = page.evaluate('() => ({h: document.body.scrollHeight, w: document.body.scrollWidth, sec: document.querySelectorAll(\"section, nav, header, footer\").length})')\n"
        "    print(info['h'], info['w'], info['sec'])\n"
        "    b.close()\n"
    )
    renders_dir = proj["dir"] / "_renders"
    renders_dir.mkdir(exist_ok=True)
    out_png = str(renders_dir / "preview.png")
    try:
        proc = subprocess.run(
            [_sys.executable, "-c", runner,
             f"file://{index_path.resolve()}", out_png, str(width), str(height)],
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "(no output)")[:500]
            return f"Error rendering page: subprocess rc={proc.returncode}: {err}"
        if not os.path.exists(out_png) or os.path.getsize(out_png) < 200:
            return f"Error rendering page: screenshot empty"
        size_kb = os.path.getsize(out_png) / 1024
        # Parse "<scrollHeight> <scrollWidth> <section_count>" from stdout
        page_h = page_w = sec_count = "?"
        try:
            parts = (proc.stdout or "").strip().split()
            if len(parts) >= 3:
                page_h, page_w, sec_count = parts[0], parts[1], parts[2]
        except Exception:
            pass
        return (
            f"Rendered: {page_w}x{page_h}px (viewport {width}x{height}), "
            f"{sec_count} top-level sections, {size_kb:.1f}KB PNG at {out_png}. "
            f"Use inspect_dom for structural details; the file is on disk for "
            f"server-side visual review."
        )
    except subprocess.TimeoutExpired:
        return "Error rendering page: timeout (>60s)"
    except Exception as e:
        return f"Error rendering page: {type(e).__name__}: {e}"


@mcp.tool()
def inspect_dom(project_id: str) -> str:
    """Inspect the DOM structure and check for console errors.

Args:
    project_id: Project ID.

Returns:
    DOM summary (element count, tag tree, console errors).
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    index_path = proj["dir"] / "index.html"
    if not index_path.exists():
        return "Error: index.html not found in project"

    # Subprocess so Playwright sync API doesn't collide with MCP asyncio loop.
    import subprocess
    import sys as _sys
    import tempfile, json as _json
    runner = (
        "from playwright.sync_api import sync_playwright\n"
        "import json, sys\n"
        "url = sys.argv[1]; out = sys.argv[2]\n"
        "msgs = []\n"
        "with sync_playwright() as p:\n"
        "    b = p.chromium.launch(headless=True)\n"
        "    page = b.new_page()\n"
        "    page.on('console', lambda m: msgs.append(f'[{m.type}] {m.text}'))\n"
        "    page.goto(url)\n"
        "    try: page.wait_for_load_state('networkidle', timeout=10000)\n"
        "    except Exception: pass\n"
        "    info = page.evaluate('''() => {\n"
        "      const all = document.querySelectorAll('*');\n"
        "      const tags = {};\n"
        "      all.forEach(el => { const t = el.tagName.toLowerCase(); tags[t] = (tags[t]||0)+1; });\n"
        "      const tree = [];\n"
        "      const body = document.body;\n"
        "      if (body) for (const c of body.children) {\n"
        "        const t = c.tagName.toLowerCase();\n"
        "        const cls = c.className ? '.'+c.className.split(' ')[0] : '';\n"
        "        const size = c.getBoundingClientRect();\n"
        "        tree.push('  '+t+cls+' ('+Math.round(size.width)+'x'+Math.round(size.height)+')');\n"
        "      }\n"
        "      return { totalElements: all.length, tags, tree };\n"
        "    }''')\n"
        "    b.close()\n"
        "json.dump({'info': info, 'msgs': msgs}, open(out, 'w'))\n"
    )
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, dir="/data/tmp", mode="w") as f:
        out_json = f.name
    try:
        proc = subprocess.run(
            [_sys.executable, "-c", runner,
             f"file://{index_path.resolve()}", out_json],
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "(no output)")[:500]
            return f"Error inspecting DOM: subprocess rc={proc.returncode}: {err}"
        with open(out_json) as f:
            data = _json.load(f)
        info = data.get("info", {})
        msgs = data.get("msgs", [])
        lines = [f"DOM: {info.get('totalElements', 0)} elements"]
        errors = [m for m in msgs if m.startswith("[error")]
        lines.append(f"Console errors: {len(errors)}")
        for err in errors[:5]:
            lines.append(f"  {err}")
        lines.append("Body children:")
        for item in info.get("tree", [])[:15]:
            lines.append(item)
        return "\n".join(lines)
    except subprocess.TimeoutExpired:
        return "Error inspecting DOM: timeout (>60s)"
    except Exception as e:
        return f"Error inspecting DOM: {type(e).__name__}: {e}"
    finally:
        try: os.remove(out_json)
        except OSError: pass


# ---- Skill library tools ---------------------------------------------------

@mcp.tool()
def list_skills(category: str = "", query: str = "", verified_only: bool = True) -> str:
    """List or search skills in the web component library.

Args:
    category: Filter by category (e.g., 'hero_section', 'animation').
              Leave empty to list all categories with counts.
    query: Search query to filter skills by name (substring match).
    verified_only: If true (default), only show verified skills.

Returns:
    List of matching skills with IDs and metadata.
"""
    _ensure_skills_loaded()
    if not _skill_index:
        return "Skill library is empty. Collect and analyze tutorials first."

    # No filters → category summary.
    if not category and not query:
        cats: dict[str, int] = {}
        cats_verified: dict[str, int] = {}
        for s in _skill_index:
            c = s.get("category", "unknown")
            cats[c] = cats.get(c, 0) + 1
            meta = (_skill_metadata or {}).get(s["skill_id"], {})
            if meta.get("exec_ok") is True:
                cats_verified[c] = cats_verified.get(c, 0) + 1

        total = len(_skill_index)
        total_v = sum(cats_verified.values())
        lines = [f"Skill library: {total} skills in {len(cats)} categories ({total_v} verified)"]
        for c, n in sorted(cats.items(), key=lambda x: -x[1]):
            v = cats_verified.get(c, 0)
            lines.append(f"  {c}: {n} skills ({v} verified)")
        return "\n".join(lines)

    results = list(_skill_index)
    if category:
        results = [s for s in results if s.get("category") == category]
    if query:
        q = query.lower()
        results = [s for s in results if q in s.get("skill_name", "").lower()]
    if verified_only:
        results = [
            s for s in results
            if (_skill_metadata or {}).get(s["skill_id"], {}).get("exec_ok") is True
        ]

    if not results:
        hint = " (try verified_only=false to see all)" if verified_only else ""
        return f"No skills found (category={category!r}, query={query!r}){hint}"

    import random
    random.shuffle(results)

    lines = [f"Found {len(results)} skills:"]
    for s in results[:30]:
        sid = s["skill_id"]
        name = s.get("skill_name", sid)
        cat = s.get("category", "?")
        meta = (_skill_metadata or {}).get(sid, {})
        tags = meta.get("semantic_tags", [])
        tag_str = f" tags=[{', '.join(tags[:5])}]" if tags else ""
        verified = " [VERIFIED]" if meta.get("exec_ok") else ""
        lines.append(f"  [{cat}] {name} (id: {sid}){verified}{tag_str}")

    if len(results) > 30:
        lines.append(f"  ... and {len(results) - 30} more")
    return "\n".join(lines)


@mcp.tool()
def get_skill_info(skill_id: str) -> str:
    """Get detailed information about a specific skill.

Args:
    skill_id: The skill ID to look up.

Returns:
    Skill details: name, category, tags, scope, code preview.
"""
    _ensure_skills_loaded()
    engine = _get_engine()
    detail = engine.get_skill_detail(_skills_dir, skill_id, _skill_index or [])

    # Wiki backend fallback: legacy detail.json doesn't exist; read from wiki layout.
    if not detail and _skills_dir:
        wiki_overview = _skills_dir / skill_id / "text" / "overview.md"
        wiki_meta = _skills_dir / skill_id / "meta.json"
        if wiki_overview.exists():
            detail = {
                "analysis": wiki_overview.read_text(encoding="utf-8"),
                "skill_name": skill_id,
                "category": "wiki",
            }
            if wiki_meta.exists():
                try:
                    m = json.loads(wiki_meta.read_text(encoding="utf-8"))
                    detail["skill_name"] = m.get("skill_name", skill_id)
                    detail["category"] = m.get("category_path", "wiki")
                except Exception:
                    pass

    if not detail:
        return f"Error: skill '{skill_id}' not found"
    name = detail.get("skill_name", skill_id)
    cat = detail.get("category", "unknown")
    meta = (_skill_metadata or {}).get(skill_id, {})

    lines = [f"Skill: {name}"]
    lines.append(f"  ID: {skill_id}")
    lines.append(f"  Category: {cat}")

    if meta:
        scope = meta.get("scope", "?")
        complexity = meta.get("complexity", "?")
        tags = meta.get("semantic_tags", [])
        lines.append(f"  Scope: {scope}")
        lines.append(f"  Complexity: {complexity}")
        if tags:
            lines.append(f"  Tags: {', '.join(tags)}")
        lines.append(f"  Exec OK: {meta.get('exec_ok', '?')}")
        file_list = meta.get("file_list", [])
        if file_list:
            lines.append(f"  Files: {', '.join(file_list)}")

    # Code preview.
    analysis = detail.get("analysis", "")
    code = engine.extract_code_from_analysis(analysis)
    if code:
        preview = "\n".join(code.split("\n")[:8])
        lines.append(f"  Code preview:\n    {preview}")

    return "\n".join(lines)


@mcp.tool()
def get_skill_code(skill_id: str) -> str:
    """Get full code from a skill for reference or direct use.

Args:
    skill_id: The skill ID to look up.

Returns:
    Full Python code with create_component() function and detected techniques.
"""
    _ensure_skills_loaded()
    engine = _get_engine()
    detail = engine.get_skill_detail(_skills_dir, skill_id, _skill_index or [])
    if not detail:
        return f"Error: skill '{skill_id}' not found"

    analysis = detail.get("analysis", "")
    code = engine.extract_code_from_analysis(analysis)
    if not code:
        return f"Error: no code found in skill '{skill_id}'"

    name = detail.get("skill_name", skill_id)

    # Extract mechanism.
    mechanism = ""
    m = re.search(r'\*\*Core (?:Visual )?Mechanism\*\*[:\s]*(.+?)(?:\n\n|\n\*\*)', analysis, re.DOTALL)
    if m:
        mechanism = m.group(1).strip()[:300]

    # Detect web techniques.
    techniques = []
    if 'flexbox' in code.lower() or 'display: flex' in code.lower():
        techniques.append('FLEXBOX')
    if 'grid' in code.lower() or 'display: grid' in code.lower():
        techniques.append('CSS_GRID')
    if 'keyframe' in code.lower() or '@keyframes' in code:
        techniques.append('CSS_ANIMATION')
    if 'gradient' in code.lower():
        techniques.append('CSS_GRADIENT')
    if 'canvas' in code.lower() or 'getContext' in code:
        techniques.append('CANVAS')
    if 'three' in code.lower() or 'WebGL' in code:
        techniques.append('WEBGL')
    if 'IntersectionObserver' in code:
        techniques.append('SCROLL_OBSERVER')

    lines = [f"# Skill Reference: {name}"]
    if mechanism:
        lines.append(f"\n## Visual Mechanism\n{mechanism}")
    if techniques:
        lines.append(f"\n## Detected Techniques\n" + "\n".join(f"- {t}" for t in techniques))
    lines.append(f"\n## Full Code ({len(code.splitlines())} lines)\n```python\n{code}\n```")
    return "\n".join(lines)


@mcp.tool()
def save_project(project_id: str, output_name: str = "") -> str:
    """Save the project to demo/web/ for permanent storage.

Args:
    project_id: Project ID.
    output_name: Output directory name under demo/web/ (defaults to project name).

Returns:
    Path where the project was saved.
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    polish_summary = _auto_polish_project(project_id)

    name = output_name or proj["name"]
    dest = _demo_dir / name
    dest.mkdir(parents=True, exist_ok=True)

    # Copy all files.
    src_dir = proj["dir"]
    for item in src_dir.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src_dir)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)

    file_count = sum(1 for _ in dest.rglob("*") if _.is_file())
    return f"Saved project to {dest} ({file_count} files). {polish_summary}"


# ---------------------------------------------------------------------------
# Schema + Variant + Reflect (Layer 1-4) — see
# docs/schema_variant_reflect_architecture.md
# ---------------------------------------------------------------------------

@mcp.tool()
def generate_web_schema(brief: str, theme_hint: str = "") -> str:
    """Generate a per-brief composition schema (NOT a fixed template).

GPT-5.4 reads the brief and produces a JSON dict describing:
  - page_archetype (marketing_landing / dashboard_app / content_site / ...)
  - tone, palette, motion, density
  - sections[] — each with role, variant_hint, props (real content, no Lorem)

This is the FIRST tool to call when building a page with skills. It
replaces 5+ iterations of list_skills/search_skills planning.

Args:
    brief: The full task brief from the user.
    theme_hint: Optional tone hint ("dark cyber", "warm editorial", etc).

Returns:
    JSON string of the schema dict. Pass to init_web_from_schema next.
"""
    try:
        sys.path.insert(0, str(_PROJECT_ROOT / "domains" / "web"))
        from schema_engine import generate_schema
    except Exception as e:
        return f"Error: schema_engine import failed: {e}"
    try:
        schema = generate_schema(brief, theme_hint)
    except Exception as e:
        return f"Error: schema generation failed: {e}"
    return json.dumps(schema, indent=2)


@mcp.tool()
def init_web_from_schema(project_id: str, schema_json: str, brief: str = "") -> str:
    """Compose a project from a schema by selecting and injecting one
component per section, then run the theme harmonizer to write ONE unified
style.css that coordinates all skills under the schema's palette.

For each section in schema.sections:
  1. Search the wiki for skills matching role + variant_hint + tone
  2. Pick the best-matching skill_id
  3. Call add_component_from_skill with content_brief from props
Then strip per-component CSS and write a single cohesive style.css. By
default this uses a deterministic schema-aware harmonizer so experiment
runs cannot hang on auxiliary LLM polish calls; set WEB_SCHEMA_LLM_HARMONIZE=1
to opt into the older GPT harmonizer.

Args:
    project_id: Project ID from create_project.
    schema_json: Schema JSON string from generate_web_schema.
    brief: The original task brief (recommended; used by the theme
        harmonizer to tune typography/spacing/motion to the brief).

Returns:
    Summary of which sections were composed and which skill_ids were picked.
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    if brief:
        proj["brief"] = brief

    try:
        schema = json.loads(schema_json)
    except Exception as e:
        return f"Error: invalid schema JSON: {e}"

    skill_index = _skill_index_for_active_pool()
    if not skill_index:
        return "Error: no skill index loaded"

    try:
        sys.path.insert(0, str(_PROJECT_ROOT / "domains" / "web"))
        from schema_engine import (
            select_variant, harmonize_theme, clean_component_body,
            rewrite_section_content, scope_css_to_section,
        )
    except Exception as e:
        return f"Error: schema_engine import failed: {e}"

    log_lines = [f"Composing from schema: {schema.get('page_archetype','?')}, "
                 f"tone={schema.get('tone','?')}, "
                 f"sections={len(schema.get('sections',[]))}"]

    composed: list[dict] = []
    for idx, sec in enumerate(schema.get("sections", [])):
        role = sec.get("role", "")
        hint = sec.get("variant_hint", "")
        skill_id = select_variant(role, hint, schema.get("tone", ""), skill_index)
        props = sec.get("props", {}) or {}
        # Build content_brief for the component
        cb_parts = []
        if props.get("headline"): cb_parts.append(props["headline"])
        if props.get("body"):     cb_parts.append(props["body"])
        if props.get("items"):    cb_parts.append("Items: " + " | ".join(str(x) for x in props["items"]))
        if props.get("cta_label"): cb_parts.append(f"CTA: {props['cta_label']}")
        if props.get("extra"):    cb_parts.append(str(props["extra"]))
        content_brief = "\n".join(cb_parts)

        palette = schema.get("palette", {}) or {}
        style_hints = (
            f"role={role}; tone={schema.get('tone','')}; "
            f"motion={schema.get('motion','subtle')}; "
            f"density={schema.get('density','balanced')}; "
            f"bg={palette.get('bg','')}; accent={palette.get('accent','')}"
        )

        if skill_id:
            try:
                result = add_component_from_skill(
                    project_id=project_id,
                    skill_id=skill_id,
                    content_brief=content_brief,
                    style_hints=style_hints,
                )
            except Exception as e:
                result = f"add_component_from_skill failed: {e}"
            log_lines.append(f"  [{idx}] {role} ({hint}) -> {skill_id}: {str(result)[:120]}")
            composed.append({"idx": idx, "role": role, "skill_id": skill_id,
                             "component_dir": _component_dir_name(skill_id),
                             "variant_hint": hint, "result": str(result)[:120]})
            if not str(result).startswith("Error"):
                append_groundings(
                    proj["dir"] / MANIFEST_FILENAME,
                    domain="web",
                    tool_name="init_web_from_schema",
                    from_skill_ids=[skill_id],
                    target_node=role or f"section_{idx}",
                    adaptation_notes=f"schema role={role}; variant_hint={hint}; {style_hints}",
                    extra={"section_index": idx, "variant_hint": hint},
                )
        else:
            log_lines.append(f"  [{idx}] {role} ({hint}) -> NO MATCH (will be custom-coded)")
            composed.append({"idx": idx, "role": role, "skill_id": None,
                             "variant_hint": hint, "result": "no match"})

    # ------------------------------------------------------------------
    # Assemble main index.html by concatenating each component's HTML
    # ------------------------------------------------------------------
    palette = schema.get("palette", {}) or {}
    bg = palette.get("bg") or palette.get("bg_primary") or "#0a0f1a"
    accent = palette.get("accent") or "#00c8ff"
    accent_alt = palette.get("accent_alt") or "#7864ff"
    text = palette.get("text") or palette.get("text_primary") or "#f0f5ff"
    surface = palette.get("surface") or palette.get("bg_surface") or "#121c2a"

    sections_html = []
    sections_css = []  # per-component CSS, scoped under .vws-{role}
    sections_js = []
    for c in composed:
        sec_idx = c.get("idx", 0)
        sec = (schema.get("sections", []) or [])[sec_idx] if sec_idx < len(schema.get("sections", []) or []) else {}
        props = sec.get("props", {}) or {}
        intro_html = _schema_intro_html(c["role"], props)
        if not c.get("skill_id"):
            if intro_html:
                sections_html.append(
                    f"<!-- fallback section: role={c['role']} -->\n"
                    f"<section class=\"vws-section vws-{c['role']}\">\n{intro_html}\n</section>"
                )
            continue
        comp_dir = proj["dir"] / "components" / (c.get("component_dir") or _component_dir_name(c["skill_id"]))
        if not comp_dir.exists():
            legacy_dir = proj["dir"] / "components" / c["skill_id"].split("_")[0]
            if legacy_dir.exists():
                comp_dir = legacy_dir
        if not comp_dir.exists():
            if intro_html:
                sections_html.append(
                    f"<!-- skill unavailable: {c['skill_id']} role={c['role']} -->\n"
                    f"<section class=\"vws-section vws-{c['role']}\">\n{intro_html}\n</section>"
                )
            continue
        comp_html = comp_dir / "index.html"
        comp_css = comp_dir / "style.css"
        comp_js = comp_dir / "script.js"
        if comp_html.exists():
            html = comp_html.read_text(encoding="utf-8", errors="ignore")
            body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
            body = body_match.group(1) if body_match else html
            # Strip <style>/<link>/<script> only — keep classes + inline styles
            body = clean_component_body(body)
            section_block = (
                f"<!-- skill: {c['skill_id']} role={c['role']} -->\n"
                f"<section class=\"vws-section vws-{c['role']}\">\n"
                f"{intro_html}\n"
                f"<div class=\"vws-skill-fragment\">\n{body}\n</div>\n"
                f"</section>"
            )
            # Content rewriter: tailor visible text to schema props
            if os.environ.get("WEB_SCHEMA_LLM_REWRITE", "0").strip().lower() in ("1", "true", "yes"):
                harmonize_brief = proj.get("brief") or schema.get("page_archetype", "")
                try:
                    rewritten = rewrite_section_content(c["role"], props, harmonize_brief, section_block)
                    section_block = rewritten
                except Exception as e:
                    log_lines.append(f"  [{sec_idx}] content rewrite failed: {e}")
            sections_html.append(section_block)
        elif intro_html:
            sections_html.append(
                f"<!-- skill missing index.html: {c['skill_id']} role={c['role']} -->\n"
                f"<section class=\"vws-section vws-{c['role']}\">\n{intro_html}\n</section>"
            )
        if comp_css.exists():
            raw_css = comp_css.read_text(encoding="utf-8", errors="ignore")
            try:
                scoped = scope_css_to_section(raw_css, c["role"])
                sections_css.append(f"/* === skill: {c['skill_id']} role={c['role']} === */\n{scoped}")
            except Exception as e:
                log_lines.append(f"  CSS scope failed for {c['skill_id']}: {e}; using raw CSS")
                sections_css.append(f"/* === skill: {c['skill_id']} (unscoped fallback) === */\n{raw_css}")
        if comp_js.exists():
            sections_js.append(f"// skill: {c['skill_id']} role={c['role']}\n"
                               f"{comp_js.read_text(encoding='utf-8', errors='ignore')}")

    # Build unified index.html
    title = schema.get("page_archetype", "Page").replace("_", " ").title()
    body_html = chr(10).join(sections_html)
    unified_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{body_html}
<script src="script.js"></script>
</body>
</html>
"""

    # ------------------------------------------------------------------
    # Theme harmonizer (cross-skill coordination layer)
    # GPT-5.4 emits TWO CSS layers: base (palette + typography) and
    # override (color/!important rules). We sandwich the per-component
    # scoped CSS between them.
    # ------------------------------------------------------------------
    base_css, override_css = "", ""
    if os.environ.get("WEB_SCHEMA_LLM_HARMONIZE", "0").strip().lower() in ("1", "true", "yes"):
        try:
            harmonize_brief = proj.get("brief") or schema.get("page_archetype", "")
            base_css, override_css = harmonize_theme(harmonize_brief, schema, body_html)
            if not base_css or len(base_css) < 200:
                raise ValueError(f"harmonizer base too short ({len(base_css)} chars)")
            log_lines.append(f"Theme harmonizer: base={len(base_css)}c, override={len(override_css)}c.")
        except Exception as e:
            log_lines.append(f"Theme harmonizer FAILED ({e}); using deterministic schema CSS.")
            base_css, override_css = _deterministic_theme_css(schema)
    else:
        base_css, override_css = _deterministic_theme_css(schema)
        log_lines.append(f"Theme harmonizer: deterministic base={len(base_css)}c, override={len(override_css)}c.")

    if not base_css or len(base_css) < 200:
        log_lines.append("Theme harmonizer fallback: scaffolded base only.")
        base_css = f""":root {{
  --bg: {bg};
  --surface: {surface};
  --accent: {accent};
  --accent-alt: {accent_alt};
  --text: {text};
  --container: 1200px;
  --section-pad: clamp(64px, 8vw, 112px);
  --radius: 16px;
  --border: rgba(255,255,255,0.08);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
}}
img, svg, canvas, video {{ max-width: 100%; height: auto; }}
.vws-section {{ padding: var(--section-pad) clamp(20px, 4vw, 40px); }}
"""
        override_css = ""

    unified_css = (
        "/* ===== BASE LAYER (harmonizer) ===== */\n" + base_css + "\n\n"
        "/* ===== COMPONENT LAYER (per-section, scoped) ===== */\n" + "\n\n".join(sections_css) + "\n\n"
        "/* ===== OVERRIDE LAYER (harmonizer, !important on color only) ===== */\n" + override_css + "\n"
    )
    unified_js = "\n".join(sections_js)

    (proj["dir"] / "index.html").write_text(unified_html, encoding="utf-8")
    (proj["dir"] / "style.css").write_text(unified_css, encoding="utf-8")
    (proj["dir"] / "script.js").write_text(unified_js, encoding="utf-8")

    log_lines.append(
        f"Assembled {len([c for c in composed if c.get('skill_id')])} sections "
        f"into index.html ({(proj['dir']/'index.html').stat().st_size} bytes)."
    )

    # ------------------------------------------------------------------
    # Image-gen pass (opt-in via WEB_IMAGE_GEN=1; endpoint is rate-limited).
    # Generates 2 images for hero/gallery/features and injects into HTML/CSS.
    # ------------------------------------------------------------------
    if os.environ.get("WEB_IMAGE_GEN", "0").strip() in ("1", "true", "True"):
        try:
            sys.path.insert(0, str(_PROJECT_ROOT / "domains" / "web"))
            from image_engine import populate_page_images
            harmonize_brief = proj.get("brief") or schema.get("page_archetype", "")
            ig = populate_page_images(proj["dir"], schema, harmonize_brief, budget=2)
            log_lines.append(
                f"Image-gen: generated={ig['generated']} replaced={ig['replaced']} "
                f"injected={ig['injected']} errors={len(ig.get('errors', []))}"
            )
        except Exception as e:
            log_lines.append(f"Image-gen FAILED ({e}); proceeding with stub images.")

    # ------------------------------------------------------------------
    # Optional vision polish. The default experiment path is deterministic:
    # save_project() applies the final CSS/HTML polish, while the agent still
    # calls render_page + inspect_dom before save for an auditable QA trace.
    # ------------------------------------------------------------------
    if os.environ.get("WEB_SCHEMA_VISION_POLISH", "0").strip().lower() in ("1", "true", "yes"):
        try:
            from schema_engine import polish_overrides_from_render
            png_bytes = b""
            try:
                index_path = proj["dir"] / "index.html"
                out_png = proj["dir"] / "_polish_render.png"
                render_script = (
                    "import sys\n"
                    "from playwright.sync_api import sync_playwright\n"
                    "url, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])\n"
                    "with sync_playwright() as p:\n"
                    "    b = p.chromium.launch(headless=True)\n"
                    "    pg = b.new_page(viewport={'width': w, 'height': h})\n"
                    "    pg.goto(url)\n"
                    "    pg.wait_for_load_state('networkidle', timeout=10000)\n"
                    "    pg.screenshot(path=out, full_page=True)\n"
                    "    b.close()\n"
                )
                import subprocess as _sp
                res = _sp.run(
                    ["python", "-c", render_script,
                     f"file://{index_path.resolve()}", str(out_png), "1280", "900"],
                    capture_output=True, text=True, timeout=60,
                )
                if out_png.exists() and out_png.stat().st_size > 1000:
                    png_bytes = out_png.read_bytes()
                else:
                    log_lines.append(f"Polish render subproc failed: {res.stderr[:200]}")
            except Exception as e:
                log_lines.append(f"Polish render failed: {e}")

            if png_bytes and len(png_bytes) > 1000:
                import base64 as _b64
                png_b64 = _b64.b64encode(png_bytes).decode("ascii")
                harmonize_brief = proj.get("brief") or schema.get("page_archetype", "")
                polish = polish_overrides_from_render(harmonize_brief, schema, png_b64)
                fix_css = polish.get("fix_css", "") or ""
                issues = polish.get("issues", []) or []
                if fix_css and len(fix_css) > 80:
                    style_path = proj["dir"] / "style.css"
                    style_path.write_text(
                        style_path.read_text(encoding="utf-8") +
                        "\n\n/* ===== POLISH OVERRIDES (vision QA) ===== */\n" +
                        fix_css + "\n",
                        encoding="utf-8",
                    )
                    log_lines.append(
                        f"Polish: applied {len(fix_css)}c CSS, issues={issues[:3]}"
                    )
                else:
                    log_lines.append(f"Polish: no fixes needed (issues={issues[:3]})")
            else:
                log_lines.append("Polish SKIPPED: render unavailable.")
        except Exception as e:
            log_lines.append(f"Polish FAILED ({e}); skipping.")
    else:
        log_lines.append("Vision polish skipped; save_project applies deterministic final polish.")

    # Stash schema in project metadata for reflect_and_swap to use later
    proj.setdefault("schema_log", []).append({"schema": schema, "composed": composed})

    return "\n".join(log_lines)


@mcp.tool()
def reflect_and_swap(project_id: str, brief: str) -> str:
    """Render the current page and ask GPT-5.4 vision to identify the
weakest section. If one is found, swap that section's variant for a
better one and re-inject it. Other sections are preserved.

This is the per-section reflection loop (Layer 4). Call 1-3 times for
diminishing returns.

Args:
    project_id: Project ID.
    brief: The original task brief (so the QA can compare against intent).

Returns:
    Summary of the swap (or 'no swap needed').
"""
    proj = _projects.get(project_id)
    if proj is None:
        return f"Error: project '{project_id}' not found"

    if os.environ.get("WEB_SCHEMA_REFLECT", "0").strip().lower() not in ("1", "true", "yes"):
        return (
            "Reflect skipped: WEB_SCHEMA_REFLECT=0. "
            "Use render_page + inspect_dom, then save_project; save_project applies deterministic final polish."
        )

    schema_logs = proj.get("schema_log") or []
    if not schema_logs:
        return "Error: no schema in project history. Call init_web_from_schema first."
    last = schema_logs[-1]
    schema = last["schema"]

    # Render current page
    try:
        result = render_page(project_id=project_id, width=1280, height=900)
    except Exception as e:
        return f"Error: render_page failed: {e}"
    # render_page returns a base64 data URI ("data:image/png;base64,...").
    # Decode that directly; only fall back to file-path parsing for older
    # render_page variants that wrote to disk.
    import base64
    png_b64 = None
    result_str = str(result)
    if result_str.startswith("data:image/") and ";base64," in result_str:
        png_b64 = result_str.split(";base64,", 1)[1].strip()
    elif result_str.lower().startswith("error"):
        return f"Error: render_page returned error: {result_str[:200]}"
    if png_b64 is None:
        png_path = None
        for line in result_str.splitlines():
            if ".png" in line:
                for tok in line.split():
                    if tok.endswith(".png"):
                        png_path = tok.strip("'\"")
                        break
            if png_path:
                break
        if not png_path:
            png_path = str(proj["dir"] / "_render.png")
        p = Path(png_path)
        if not p.exists() or p.stat().st_size < 1000:
            return f"Error: rendered PNG not found or empty at {png_path}"
        png_b64 = base64.b64encode(p.read_bytes()).decode("ascii")

    try:
        sys.path.insert(0, str(_PROJECT_ROOT / "domains" / "web"))
        from schema_engine import reflect_qa, select_variant
    except Exception as e:
        return f"Error: schema_engine import failed: {e}"

    try:
        decision = reflect_qa(brief, schema, png_b64)
    except Exception as e:
        return f"Error: reflect_qa failed: {e}"

    if decision.get("status") == "ok":
        return "Reflect: all sections look good, no swap needed."

    if decision.get("status") != "swap":
        return f"Reflect: unrecognized status: {decision}"

    idx = decision.get("section_idx")
    if idx is None or not isinstance(idx, int):
        return f"Reflect: invalid section_idx: {decision}"
    if idx < 0 or idx >= len(schema.get("sections", [])):
        return f"Reflect: section_idx out of range: {idx}"

    new_hint = decision.get("new_variant_hint", "")
    new_props = decision.get("new_props") or {}
    section = schema["sections"][idx]
    role = section.get("role", "")

    new_skill_id = select_variant(role, new_hint, schema.get("tone", ""), _skill_index or [])
    if not new_skill_id:
        return f"Reflect: no replacement variant found for role={role}, hint={new_hint}"

    # Update schema in proj history
    section["variant_hint"] = new_hint
    section["replaced_with"] = new_skill_id
    section["reason"] = decision.get("reason", "")
    if new_props:
        section.setdefault("props", {}).update(new_props)

    # Re-inject this section
    props = section.get("props", {}) or {}
    cb_parts = []
    if props.get("headline"): cb_parts.append(props["headline"])
    if props.get("body"):     cb_parts.append(props["body"])
    if props.get("items"):    cb_parts.append("Items: " + " | ".join(str(x) for x in props["items"]))
    if props.get("cta_label"): cb_parts.append(f"CTA: {props['cta_label']}")
    content_brief = "\n".join(cb_parts)

    palette = schema.get("palette", {}) or {}
    style_hints = (
        f"role={role}; tone={schema.get('tone','')}; "
        f"motion={schema.get('motion','subtle')}; "
        f"bg={palette.get('bg','')}; accent={palette.get('accent','')}"
    )

    try:
        inject_result = add_component_from_skill(
            project_id=project_id,
            skill_id=new_skill_id,
            content_brief=content_brief,
            style_hints=style_hints,
        )
    except Exception as e:
        return f"Reflect: swap failed during re-inject: {e}"

    return (f"Reflect: swapped section {idx} ({role}) -> {new_skill_id}. "
            f"Reason: {decision.get('reason','?')[:120]}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Web MCP Server")
    parser.add_argument("--skills-dir", default=None, help="Path to skills library (override). "
                        "When omitted, resolves from domain.yaml's library_backend flag.")
    parser.add_argument("--demo-dir", default=None,
                        help="Path to saved web artifacts (default: <project>/demo/web).")
    args = parser.parse_args()

    global _skills_dir, _demo_dir
    if args.skills_dir:
        _skills_dir = Path(args.skills_dir).resolve()
    else:
        # Honour the per-domain library_backend flag.
        try:
            from core import get_library_dir
            _skills_dir = get_library_dir("web").resolve()
        except Exception as exc:  # noqa: BLE001
            log.warning("Web MCP: could not resolve library_backend (%s); falling back to legacy", exc)
    if args.demo_dir:
        _demo_dir = Path(args.demo_dir).resolve()
    _demo_dir.mkdir(parents=True, exist_ok=True)

    # When the wiki backend is active, expose the universal discovery surface
    # alongside the legacy Web tools so an agent can browse and dispatch via
    # the wiki contract.
    backend = "legacy"
    try:
        from core import get_active_library_backend
        backend = get_active_library_backend("web")
    except Exception as exc:  # noqa: BLE001
        log.warning("Web MCP: could not read library_backend: %s", exc)
    global _startup_backend, _wiki_tools_registered
    _startup_backend = backend
    if backend == "wiki":
        try:
            from domains.web.wiki_adapter import WebWikiAdapter
            from core.skill_wiki.mcp_tools import register_wiki_tools
            register_wiki_tools(mcp, WebWikiAdapter())
            _wiki_tools_registered = True
            log.info("Web MCP: registered universal wiki discovery tools")
        except Exception as exc:  # noqa: BLE001
            log.error("Web MCP: failed to register wiki tools: %s", exc)
            raise

    # Stale-registry guard: regardless of startup backend, detect a later
    # library_backend flip and surface a structured error.
    try:
        from core.skill_wiki.legacy_stale import register_legacy_stale_check
        wrapped = register_legacy_stale_check(mcp, domain="web", startup_backend=backend)
        log.info("Web MCP: stale-registry guard installed on %d tools", wrapped)
    except Exception as exc:  # noqa: BLE001
        log.warning("Web MCP: failed to install stale-registry guard: %s", exc)

    logging.basicConfig(level=logging.INFO)
    log.info(f"Web MCP Server starting (skills_dir={_skills_dir}, backend={backend})")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
