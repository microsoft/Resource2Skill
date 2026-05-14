"""GPT-Image-2 client for the web domain.

The image deployment is on a SEPARATE Azure endpoint with a strict
2-req/min rate limit. This module provides:

  - generate_image(prompt, size, out_path) — single-image call with
    long retries to absorb the rate limit
  - populate_page_images(project_dir, schema, brief) — scans the
    project for <img> tags and section-level visual stubs, generates
    matching prompts via GPT-5.4, then calls gpt-image-2 to fill them

A per-prompt cache (sha1 of the prompt -> <cache_dir>/<hash>.png)
avoids paying twice for the same image across reruns.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.llm import call_azure_openai

CACHE_DIR = Path(os.environ.get("VWS_WEB_IMAGE_CACHE_DIR", "/tmp/vws_web_img_cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _load_env() -> dict[str, str]:
    """Read AZURE_IMAGE_* from os.environ, then fallback to repo-local .env."""
    keys = ("AZURE_IMAGE_ENDPOINT", "AZURE_IMAGE_DEPLOYMENT",
            "AZURE_IMAGE_API_VERSION", "AZURE_IMAGE_API_KEY")
    cfg = {k: os.environ.get(k, "") for k in keys}
    if all(cfg.values()):
        return cfg
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip("'\"")
            if k in keys and not cfg[k]:
                cfg[k] = v
    return cfg


def _cache_path(prompt: str, size: str) -> Path:
    h = hashlib.sha1(f"{size}::{prompt}".encode("utf-8")).hexdigest()[:16]
    return CACHE_DIR / f"{h}.png"


def generate_image(prompt: str, out_path: Path,
                   size: str = "1024x1024",
                   max_retries: int = 6,
                   retry_delay: float = 35.0) -> bool:
    """Generate a single image via gpt-image-2 and save to out_path.

    Cache-aware: if the same (size, prompt) was generated before,
    just copy from cache.

    Returns True on success, False otherwise.
    """
    cache = _cache_path(prompt, size)
    if cache.exists() and cache.stat().st_size > 1000:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(cache.read_bytes())
        return True

    cfg = _load_env()
    if not all(cfg.values()):
        return False

    url = (f"{cfg['AZURE_IMAGE_ENDPOINT'].rstrip('/')}/openai/deployments/"
           f"{cfg['AZURE_IMAGE_DEPLOYMENT']}/images/generations"
           f"?api-version={cfg['AZURE_IMAGE_API_VERSION']}")
    headers = {"api-key": cfg["AZURE_IMAGE_API_KEY"], "Content-Type": "application/json"}
    body = {"prompt": prompt[:3500], "size": size, "n": 1}

    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=180)
            if resp.status_code == 429 or resp.status_code >= 500:
                # rate-limited / server-side; back off harder
                time.sleep(retry_delay + attempt * 10)
                continue
            if resp.status_code != 200:
                return False
            data = resp.json()
            entries = data.get("data", [])
            if not entries:
                return False
            b64 = entries[0].get("b64_json")
            if b64:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                png_bytes = base64.b64decode(b64)
                out_path.write_bytes(png_bytes)
                cache.write_bytes(png_bytes)
                return True
            url2 = entries[0].get("url")
            if url2:
                r2 = requests.get(url2, timeout=60)
                if r2.status_code == 200:
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    out_path.write_bytes(r2.content)
                    cache.write_bytes(r2.content)
                    return True
            return False
        except Exception:
            time.sleep(retry_delay)
    return False


# --------------------------------------------------------------------------
# Image-prompt planner: given the schema + brief, ask GPT-5.4 to author
# 2-4 image prompts for the most visually-impactful sections.
# --------------------------------------------------------------------------
PROMPT_PLANNER = """You are an art director planning images for a landing page.

Brief:
<<<
{brief}
>>>

Schema:
- archetype: {archetype}
- tone: {tone}
- palette: {palette}
- sections (in order):
{section_list}

For the {budget} most visually-impactful sections (typically hero,
features visual, gallery, testimonials backdrop), author ONE concrete
image prompt each. Prompts should be:
- Photographic or polished render style appropriate to the tone (avoid
  generic stock-photo vibes).
- Specific: include subject, composition, lighting, color palette,
  background, mood.
- 25-50 words each.
- No text/logos/UI within the image.

Output STRICT JSON list:
[
  {{"section_idx": <int>, "role": "<role>", "prompt": "<image prompt>", "size": "1536x1024" | "1024x1024" | "1024x1536"}},
  ...
]
"""


def plan_image_prompts(brief: str, schema: dict, budget: int = 3) -> list[dict]:
    """Ask GPT-5.4 for image prompts for the top-N sections."""
    sections = schema.get("sections", []) or []
    if not sections:
        return []
    section_list = "\n".join(
        f"  [{i}] {s.get('role','?')} — {s.get('variant_hint','')}"
        for i, s in enumerate(sections)
    )
    prompt = PROMPT_PLANNER.format(
        brief=brief[:1200],
        archetype=schema.get("page_archetype", ""),
        tone=schema.get("tone", ""),
        palette=json.dumps(schema.get("palette", {})),
        section_list=section_list,
        budget=budget,
    )
    try:
        msg = call_azure_openai(
            [{"role": "user", "content": prompt}],
            model="gpt-5.4",
            reasoning_effort="low",
            max_completion_tokens=2048,
            max_retries=4,
            retry_delay=10.0,
        )
        raw = msg.get("content", "").strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.rsplit("```", 1)[0]
        plans = json.loads(raw.strip())
        if isinstance(plans, list):
            return plans[:budget]
    except Exception:
        pass
    return []


# --------------------------------------------------------------------------
# Project-level integration: replace stub <img> placeholders + inject
# section background images for hero/gallery/cta.
# --------------------------------------------------------------------------
_STUB_IMG_PATTERNS = (
    "placeholder", "via.placeholder", "picsum", "unsplash.com/random",
    "lorem", "example.com", "data:image/svg",
    "/mock", "/dummy", "/sample-",
)


def _is_stub_src(src: str) -> bool:
    s = src.lower()
    return any(p in s for p in _STUB_IMG_PATTERNS) or src.strip() in ("", "#")


def populate_page_images(project_dir: Path, schema: dict, brief: str,
                         budget: int = 3, role_filter: tuple[str, ...] = (
                             "hero", "gallery", "features", "cta",
                             "testimonials", "comparison", "showcase")
                         ) -> dict:
    """Generate images for the top-N sections and inject them into the
    assembled index.html.

    Two injection strategies:
      1. If a section has an <img> tag with a stub src, replace src.
      2. Else, prepend a <div class="vws-img-fill"> with background-image
         set to the generated PNG, scoped under the section.

    Returns a dict {plans, generated, replaced, injected}.
    """
    out = {"plans": [], "generated": 0, "replaced": 0, "injected": 0,
           "errors": []}

    plans = plan_image_prompts(brief, schema, budget=budget)
    if not plans:
        out["errors"].append("planner returned no prompts")
        return out
    out["plans"] = plans

    images_dir = project_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    index_path = project_dir / "index.html"
    if not index_path.exists():
        out["errors"].append("index.html missing")
        return out
    html = index_path.read_text(encoding="utf-8", errors="ignore")

    style_path = project_dir / "style.css"
    css_extra: list[str] = []

    for plan in plans:
        role = plan.get("role", "")
        if role_filter and role not in role_filter:
            continue
        idx = plan.get("section_idx", -1)
        prompt = plan.get("prompt", "")
        size = plan.get("size", "1536x1024")
        if size not in ("1024x1024", "1536x1024", "1024x1536"):
            size = "1024x1024"

        out_path = images_dir / f"{role}_{idx}.png"
        ok = generate_image(prompt, out_path, size=size)
        if not ok:
            out["errors"].append(f"gen failed for {role}#{idx}")
            continue
        out["generated"] += 1

        rel_src = f"images/{out_path.name}"

        # Strategy 1: find a stub <img> inside the section block and replace src
        section_re = re.compile(
            rf"(<section[^>]*class=\"[^\"]*vws-{re.escape(role)}[^\"]*\"[^>]*>)(.*?)(</section>)",
            re.DOTALL | re.IGNORECASE,
        )
        m = section_re.search(html)
        replaced_in_section = False
        if m:
            tag_open, body, tag_close = m.group(1), m.group(2), m.group(3)
            def _replace_first_stub(b: str) -> tuple[str, bool]:
                pattern = re.compile(r"<img\b([^>]*?)src=\"([^\"]*)\"([^>]*?)>", re.IGNORECASE)
                rep = {"done": False}
                def _sub(mm):
                    if rep["done"]:
                        return mm.group(0)
                    src = mm.group(2)
                    if _is_stub_src(src) or len(src) < 4:
                        rep["done"] = True
                        return f'<img{mm.group(1)}src="{rel_src}"{mm.group(3)}>'
                    return mm.group(0)
                new_b = pattern.sub(_sub, b)
                return new_b, rep["done"]
            new_body, done = _replace_first_stub(body)
            if done:
                html = html.replace(m.group(0), tag_open + new_body + tag_close)
                replaced_in_section = True
                out["replaced"] += 1

        if not replaced_in_section:
            # Strategy 2: inject a background-image filler at the top of the section
            if m:
                tag_open, body, tag_close = m.group(1), m.group(2), m.group(3)
                fill_div = (f"\n<div class=\"vws-img-fill vws-img-fill-{role}\" "
                            f"data-img=\"{role}_{idx}\"></div>\n")
                html = html.replace(
                    m.group(0),
                    tag_open + fill_div + body + tag_close,
                )
                out["injected"] += 1
                # Add CSS for this filler
                css_extra.append(
                    f'.vws-{role} .vws-img-fill-{role} {{\n'
                    f'  width: 100%; min-height: 360px;\n'
                    f'  background-image: linear-gradient(135deg, rgba(0,0,0,0.35), rgba(0,0,0,0.15)), '
                    f'url("{rel_src}");\n'
                    f'  background-size: cover; background-position: center;\n'
                    f'  border-radius: var(--radius, 16px);\n'
                    f'  margin-bottom: 1.5rem;\n'
                    f'}}'
                )

    # Persist
    if html != index_path.read_text(encoding="utf-8", errors="ignore"):
        index_path.write_text(html, encoding="utf-8")
    if css_extra and style_path.exists():
        style_path.write_text(
            style_path.read_text(encoding="utf-8") +
            "\n\n/* ===== IMAGE-GEN FILLERS ===== */\n" + "\n".join(css_extra),
            encoding="utf-8",
        )

    return out
