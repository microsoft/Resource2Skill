"""Brand extraction pipeline orchestrator. Real logic lands in Phase 2+."""
from __future__ import annotations

import datetime as _dt
import json
import shutil
import tempfile
import zipfile as _zip
from dataclasses import dataclass
from pathlib import Path

import jsonschema
import yaml

from .theme_xml_reader import aggregate_brand_signals, read_pptx_theme

SCHEMA_PATH = Path(__file__).parent / "brand_pack_schema.json"


@dataclass(frozen=True)
class ExtractionResult:
    brand_dir: Path
    brand_yaml_path: Path
    skill_ids: list[str]


def _collect_pptx(src: Path, scratch: Path) -> list[Path]:
    if src.is_file() and src.suffix.lower() == ".zip":
        with _zip.ZipFile(src) as zf:
            zf.extractall(scratch)
        return sorted(scratch.glob("**/*.pptx"))
    if src.is_dir():
        return sorted(src.glob("**/*.pptx"))
    raise ValueError(f"unsupported source: {src}")


def extract(
    *,
    brand_name: str,
    source: Path,
    output_root: Path,
    render: bool = True,
    vision: bool = True,
    synthesize_skills: bool = True,
) -> ExtractionResult:
    """Run the brand extraction pipeline.

    Args:
        brand_name: lowercase slug, e.g. 'acme_brand'.
        source: path to a folder of .pptx files or a .zip containing them.
        output_root: root dir for brand_wiki (default brand_wiki/ppt).
        render: run LibreOffice slide rendering pass.
        vision: run GPT-5.4 vision enrichment pass.
        synthesize_skills: emit R2S-shaped skill folders.

    Phase 2: deterministic XML extraction and provenance copy.
    """
    if not source.exists():
        raise FileNotFoundError(f"brand source not found: {source}")
    brand_dir = output_root / brand_name
    (brand_dir / "source").mkdir(parents=True, exist_ok=True)
    (brand_dir / "skills").mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(dir="/data/tmp") as scratch_str:
        scratch = Path(scratch_str)
        pptxs = _collect_pptx(source, scratch)
        if not pptxs:
            raise RuntimeError(f"no .pptx files found in {source}")

        copied = []
        for p in pptxs:
            dst = brand_dir / "source" / p.name
            shutil.copy2(p, dst)
            copied.append(p.name)

        sigs = [read_pptx_theme(p) for p in pptxs]
        bs = aggregate_brand_signals(sigs)

    brand_pack = {
        "brand_name": brand_name,
        "display_name": brand_name.replace("_", " ").title(),
        "version": "1.0.0",
        "source": {
            "type": "brand_pptx",
            "files": copied,
            "extracted_at": _dt.datetime.now(_dt.UTC).isoformat().replace("+00:00", "Z"),
        },
        "palette": {
            "primary": bs.primary,
            "secondary": bs.secondary,
            "accents": bs.accents,
            "neutrals": bs.neutrals,
        },
        "typography": {
            "heading": bs.heading_font,
            "body": bs.body_font,
            **({"mono": bs.mono_font} if bs.mono_font else {}),
        },
        "skills": [],
    }

    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(brand_pack, schema)

    brand_yaml_path = brand_dir / "brand.yaml"
    brand_yaml_path.write_text(yaml.safe_dump(brand_pack, sort_keys=False))

    if render:
        from .slide_renderer import render_thumbs

        render_thumbs(brand_dir / "source", brand_dir / "source/thumbs")
    if vision:
        from .vision_describer import enrich_brand_pack

        enrich_brand_pack(brand_yaml_path)
    skill_ids: list[str] = []
    if synthesize_skills:
        from .skill_synthesizer import synthesize

        skill_ids = synthesize(brand_dir)
        if skill_ids:
            bp = yaml.safe_load(brand_yaml_path.read_text())
            bp["skills"] = skill_ids
            brand_yaml_path.write_text(yaml.safe_dump(bp, sort_keys=False))

    return ExtractionResult(brand_dir=brand_dir, brand_yaml_path=brand_yaml_path, skill_ids=skill_ids)
