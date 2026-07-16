"""Enrich brand.yaml with vision-derived style_rules using GPT-5.5 vision."""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path

import yaml

from core.llm import call_azure_openai

VISION_PROMPT = """\
You are a senior visual brand analyst. The attached images are representative slides
from a single corporate brand's PowerPoint deck. The extracted palette and
typography are:

  primary:   {primary}
  secondary: {secondary}
  accents:   {accents}
  neutrals:  {neutrals}
  heading:   {heading}
  body:      {body}

Produce a JSON object with EXACTLY these keys (each value a single English string,
1-3 sentences, concrete and tied to what you actually see -- NEVER vague like
"professional and clean"):

  cover_style            -- how do title/cover slides treat the wordmark,
                           background, and hero element?
  section_divider_style  -- how do chapter/section breaks look?
  content_layout         -- typical body slide grid, density, where copy sits
  data_viz_palette       -- how are charts/tables colored vs body
  typography_hierarchy   -- H1/H2/body weight/size relationships you see
  decorative_motifs      -- recurring shapes/lines/patterns (curves, grids, gradients)
  dont_use_layouts       -- what would clearly NOT belong (busy stock-photo overlays?
                           cliche clip-art? specific colors that contradict the palette?)

Return ONLY the JSON object, no prose.
"""

STYLE_RULE_KEYS = (
    "cover_style",
    "section_divider_style",
    "content_layout",
    "data_viz_palette",
    "typography_hierarchy",
    "decorative_motifs",
    "dont_use_layouts",
)


def _b64_image(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()


def _parse_json_object(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def enrich_brand_pack(brand_yaml: Path, max_images: int = 6) -> None:
    bp = yaml.safe_load(brand_yaml.read_text())
    thumbs_dir = brand_yaml.parent / "source" / "thumbs"
    pngs = sorted(thumbs_dir.glob("*.png"))[:max_images]
    if not pngs:
        bp.setdefault("style_rules", {})
        brand_yaml.write_text(yaml.safe_dump(bp, sort_keys=False))
        return

    prompt = VISION_PROMPT.format(
        primary=bp["palette"]["primary"],
        secondary=bp["palette"]["secondary"],
        accents=", ".join(bp["palette"]["accents"]),
        neutrals=", ".join(bp["palette"]["neutrals"]),
        heading=bp["typography"]["heading"],
        body=bp["typography"]["body"],
    )

    image_messages = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{_b64_image(p)}"},
        }
        for p in pngs
    ]
    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}] + image_messages,
        }
    ]

    response = call_azure_openai(
        messages=messages,
        model="gpt-5.5",
        reasoning_effort="medium",
        max_completion_tokens=2048,
    )
    rules = _parse_json_object(response.get("content") or "")
    bp["style_rules"] = {
        key: str(rules[key]).strip()
        for key in STYLE_RULE_KEYS
        if key in rules and str(rules[key]).strip()
    }
    brand_yaml.write_text(yaml.safe_dump(bp, sort_keys=False))
