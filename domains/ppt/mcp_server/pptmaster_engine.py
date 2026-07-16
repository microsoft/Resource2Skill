"""PPT Master runtime adapter for the PPT MCP server.

The existing PPT domain is python-pptx-native and Resource2Skill-centric:
wiki entries expose executable Python code, while the MCP server maintains an
in-memory ``Presentation``.  PPT Master has a different execution model: a
project directory contains hand-authored SVG pages, then upstream scripts
convert those SVGs into native editable PPTX DrawingML.

This module keeps that second model isolated.  The MCP server can expose a
small tool surface for SVG projects without weakening the legacy
``add_slide``/``add_slide_from_skill`` path used by Resource2Skill.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


SERVER_DIR = Path(__file__).resolve().parent
DOMAIN_DIR = SERVER_DIR.parent
PROJECT_ROOT = DOMAIN_DIR.parent.parent
RUNTIME_DIR = DOMAIN_DIR / "ppt_master_runtime"
# The upstream directory is named "scripts", but this repository's release
# .gitignore excludes any scripts/ directory.  Keep the vendored runtime under
# tools/ so it is visible to git while preserving upstream filenames inside.
SCRIPTS_DIR = RUNTIME_DIR / "tools"
TEMPLATES_DIR = RUNTIME_DIR / "templates"
DEFAULT_PROJECT_ROOT = PROJECT_ROOT / "demo" / "ppt_master"

_FORMAT_VIEWBOX = {
    "ppt169": "0 0 1280 720",
    "ppt43": "0 0 1024 768",
    "xiaohongshu": "0 0 1242 1660",
    "xhs": "0 0 1242 1660",
    "story": "0 0 1080 1920",
    "banner": "0 0 1920 1080",
    "a4": "0 0 1240 1754",
}


class PPTMasterError(RuntimeError):
    """Raised when the PPT Master adapter cannot complete a request."""


@dataclass
class CommandResult:
    ok: bool
    stdout: str
    stderr: str
    returncode: int


def runtime_info() -> dict:
    """Return adapter paths and coarse capability flags."""
    return {
        "runtime_dir": str(RUNTIME_DIR),
        "scripts_dir": str(SCRIPTS_DIR),
        "templates_dir": str(TEMPLATES_DIR),
        "has_svg_to_pptx": (SCRIPTS_DIR / "svg_to_pptx.py").exists(),
        "has_template_import": (SCRIPTS_DIR / "pptx_template_import.py").exists(),
        "has_icon_bundle": (TEMPLATES_DIR / "icons").exists(),
        "default_project_root": str(DEFAULT_PROJECT_ROOT),
    }


def create_project(
    project_name: str,
    canvas_format: str = "ppt169",
    base_dir: str | None = None,
) -> dict:
    """Create a PPT Master project directory and return its metadata."""
    _require_runtime()
    fmt = _normalize_format(canvas_format)
    slug = _slugify(project_name or "deck")
    root = Path(base_dir).expanduser().resolve() if base_dir else DEFAULT_PROJECT_ROOT
    root.mkdir(parents=True, exist_ok=True)

    date = datetime.now().strftime("%Y%m%d")
    project_dir = _unique_project_path(root, slug, fmt, date)
    for rel in (
        "svg_output",
        "svg_final",
        "images",
        "notes",
        "templates",
        "sources",
        "exports",
    ):
        (project_dir / rel).mkdir(parents=True, exist_ok=True)

    readme = project_dir / "README.md"
    readme.write_text(
        (
            f"# {project_name or slug}\n\n"
            f"- Canvas format: {fmt}\n"
            f"- Created: {date}\n"
            "- Runtime: Resource2Skill PPT MCP with PPT Master SVG backend\n\n"
            "## Directories\n\n"
            "- `svg_output/`: editable source SVG pages\n"
            "- `svg_final/`: optional finalized SVG pages\n"
            "- `notes/`: speaker notes matched by SVG filename\n"
            "- `templates/`: copied PPT Master template assets for this project\n"
            "- `exports/`: generated native editable PPTX files\n"
        ),
        encoding="utf-8",
    )

    return {
        "project_path": str(project_dir),
        "project_name": project_name or slug,
        "canvas_format": fmt,
        "viewbox": _FORMAT_VIEWBOX.get(fmt, _FORMAT_VIEWBOX["ppt169"]),
        "svg_output": str(project_dir / "svg_output"),
        "exports": str(project_dir / "exports"),
    }


def list_svg_slides(project_path: str) -> list[dict]:
    """List SVG source pages in project order."""
    project = _resolve_project(project_path)
    out = []
    for idx, path in enumerate(sorted((project / "svg_output").glob("*.svg")), start=1):
        notes = project / "notes" / f"{path.stem}.md"
        out.append(
            {
                "index": idx,
                "name": path.name,
                "stem": path.stem,
                "path": str(path),
                "notes_path": str(notes) if notes.exists() else None,
                "bytes": path.stat().st_size,
            }
        )
    return out


def write_svg_slide(
    project_path: str,
    svg: str,
    slide_name: str = "",
    notes: str = "",
    overwrite: bool = False,
) -> dict:
    """Write a source SVG page.  This is the PPT Master equivalent of add/replace code."""
    project = _resolve_project(project_path)
    _validate_svg(svg)

    svg_dir = project / "svg_output"
    svg_dir.mkdir(parents=True, exist_ok=True)
    stem = None
    if overwrite and slide_name:
        try:
            stem = _resolve_svg(project, slide_name).stem
        except PPTMasterError:
            stem = None
    if stem is None:
        stem = _normalize_slide_stem(slide_name, svg_dir)
    path = svg_dir / f"{stem}.svg"
    if path.exists() and not overwrite:
        raise PPTMasterError(f"slide already exists: {path.name}; pass overwrite=true to replace it")
    path.write_text(_ensure_svg_trailing_newline(svg), encoding="utf-8")
    warnings = _svg_static_warnings(svg)

    notes_path = None
    if notes:
        notes_dir = project / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)
        notes_path = notes_dir / f"{stem}.md"
        notes_path.write_text(notes.strip() + "\n", encoding="utf-8")

    return {
        "slide": path.name,
        "path": str(path),
        "notes_path": str(notes_path) if notes_path else None,
        "slide_count": len(list((project / "svg_output").glob("*.svg"))),
        "warnings": warnings,
    }


def read_svg_slide(project_path: str, slide_name: str) -> dict:
    """Read a source SVG page for inspection or rewrite."""
    project = _resolve_project(project_path)
    path = _resolve_svg(project, slide_name)
    notes_path = project / "notes" / f"{path.stem}.md"
    return {
        "slide": path.name,
        "path": str(path),
        "svg": path.read_text(encoding="utf-8", errors="ignore"),
        "notes": notes_path.read_text(encoding="utf-8", errors="ignore") if notes_path.exists() else "",
    }


def delete_svg_slide(project_path: str, slide_name: str) -> dict:
    """Delete a source SVG page and matching notes file if present."""
    project = _resolve_project(project_path)
    path = _resolve_svg(project, slide_name)
    stem = path.stem
    path.unlink()
    notes_path = project / "notes" / f"{stem}.md"
    if notes_path.exists():
        notes_path.unlink()
    return {"deleted": stem, "slide_count": len(list((project / "svg_output").glob("*.svg")))}


def finalize_project(project_path: str) -> CommandResult:
    """Run PPT Master's SVG finalization pass."""
    project = _resolve_project(project_path)
    return _run_script([SCRIPTS_DIR / "finalize_svg.py", str(project), "--quiet"], timeout=120)


def export_project(
    project_path: str,
    output_path: str = "",
    source: str = "output",
    transition: str = "fade",
    animation: str = "auto",
    animation_trigger: str = "after-previous",
    compat: bool = False,
    finalize: bool = False,
    layout_strict: bool = False,
) -> dict:
    """Export a PPT Master project to an editable native PPTX."""
    project = _resolve_project(project_path)
    if not list((project / "svg_output").glob("*.svg")):
        raise PPTMasterError(f"no SVG slides found in {project / 'svg_output'}")

    layout_report = validate_project(str(project), strict=layout_strict)
    if layout_strict and not layout_report["ok"]:
        issue_text = "; ".join(
            f"{slide['slide']}: {issue}"
            for slide in layout_report["slides"]
            for issue in slide.get("errors", [])
        )
        raise PPTMasterError(f"layout validation failed before export: {issue_text[:900]}")

    finalize_result = None
    actual_source = source
    if finalize:
        finalize_result = finalize_project(str(project))
        if not finalize_result.ok:
            raise PPTMasterError(_format_command_error("finalize_svg.py", finalize_result))
        actual_source = "final"

    out = Path(output_path).expanduser().resolve() if output_path else _default_export_path(project)
    out.parent.mkdir(parents=True, exist_ok=True)

    args: list[str | Path] = [
        SCRIPTS_DIR / "svg_to_pptx.py",
        str(project),
        "-o",
        str(out),
        "-s",
        actual_source,
        "-t",
        transition,
        "-a",
        animation,
        "--animation-trigger",
        animation_trigger,
    ]
    if not compat:
        args.append("--no-compat")

    result = _run_script(args, timeout=240)
    if not result.ok:
        raise PPTMasterError(_format_command_error("svg_to_pptx.py", result))

    return {
        "pptx_path": str(out),
        "project_path": str(project),
        "source": actual_source,
        "compat": bool(compat),
        "finalized": bool(finalize),
        "slide_count": len(list((project / "svg_output").glob("*.svg"))),
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "finalize_stdout": finalize_result.stdout.strip() if finalize_result else "",
        "finalize_stderr": finalize_result.stderr.strip() if finalize_result else "",
        "layout": layout_report,
    }


def import_pptx_template(
    pptx_path: str,
    output_dir: str = "",
    inheritance_mode: str = "both",
    manifest_only: bool = False,
) -> dict:
    """Run PPT Master's PPTX -> SVG/template import pipeline."""
    source = Path(pptx_path).expanduser().resolve()
    if not source.exists():
        raise PPTMasterError(f"template source does not exist: {source}")
    if source.suffix.lower() != ".pptx":
        raise PPTMasterError(f"expected a .pptx file, got: {source.name}")
    if inheritance_mode not in {"both", "layered", "flat"}:
        raise PPTMasterError("inheritance_mode must be one of: both, layered, flat")

    out = (
        Path(output_dir).expanduser().resolve()
        if output_dir
        else source.with_name(f"{source.stem}_template_import")
    )
    args: list[str | Path] = [
        SCRIPTS_DIR / "pptx_template_import.py",
        str(source),
        "-o",
        str(out),
        "--inheritance-mode",
        inheritance_mode,
    ]
    if manifest_only:
        args.append("--manifest-only")
    result = _run_script(args, timeout=240)
    if not result.ok:
        raise PPTMasterError(_format_command_error("pptx_template_import.py", result))
    return {
        "output_dir": str(out),
        "manifest": str(out / "manifest.json") if (out / "manifest.json").exists() else None,
        "summary": str(out / "summary.md") if (out / "summary.md").exists() else None,
        "svg_dir": str(out / "svg") if (out / "svg").exists() else None,
        "svg_flat_dir": str(out / "svg-flat") if (out / "svg-flat").exists() else None,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def list_templates(kind: str = "layout") -> dict:
    """List bundled PPT Master templates/charts."""
    kind = _normalize_template_kind(kind)
    index_path = _template_index_path(kind)
    if not index_path.exists():
        return {"kind": kind, "index_path": str(index_path), "templates": {}}
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PPTMasterError(f"invalid template index {index_path}: {exc}") from exc
    return {"kind": kind, "index_path": str(index_path), "templates": payload}


def get_template(kind: str, template_id: str, svg_name: str = "") -> dict:
    """Return template metadata and optionally one SVG file's source."""
    kind = _normalize_template_kind(kind)
    template_dir = _template_dir(kind) / template_id
    if not template_dir.exists():
        raise PPTMasterError(f"{kind} template not found: {template_id}")
    spec_path = template_dir / "design_spec.md"
    svg_files = sorted(p.name for p in template_dir.glob("*.svg"))
    result = {
        "kind": kind,
        "template_id": template_id,
        "template_dir": str(template_dir),
        "design_spec": spec_path.read_text(encoding="utf-8", errors="ignore") if spec_path.exists() else "",
        "svg_files": svg_files,
    }
    if svg_name:
        svg_path = _resolve_template_svg(template_dir, svg_name)
        result["svg_name"] = svg_path.name
        result["svg"] = svg_path.read_text(encoding="utf-8", errors="ignore")
    return result


def copy_template_to_project(project_path: str, kind: str, template_id: str) -> dict:
    """Copy a bundled PPT Master template into a project-local templates directory."""
    project = _resolve_project(project_path)
    kind = _normalize_template_kind(kind)
    source = _template_dir(kind) / template_id
    if not source.exists():
        raise PPTMasterError(f"{kind} template not found: {template_id}")
    dest = project / "templates" / kind / template_id
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest)
    return {"copied_from": str(source), "copied_to": str(dest)}


def command_result_to_dict(result: CommandResult) -> dict:
    return {
        "ok": result.ok,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def validate_project(project_path: str, strict: bool = False) -> dict:
    """Validate SVG source slides for common layout issues.

    This is a source-level guard, not a browser-grade layout engine. It catches
    the issues that most often make PPTMaster exports look broken: text outside
    the canvas, long single-line text, severe text/text overlap, and empty
    slides. It deliberately avoids prescribing visual style or templates.
    """
    project = _resolve_project(project_path)
    slides: list[dict] = []
    total_errors = 0
    total_warnings = 0
    for path in sorted((project / "svg_output").glob("*.svg")):
        svg = path.read_text(encoding="utf-8", errors="ignore")
        errors, warnings = _svg_layout_issues(svg, strict=strict)
        slides.append({
            "slide": path.name,
            "path": str(path),
            "errors": errors,
            "warnings": warnings,
        })
        total_errors += len(errors)
        total_warnings += len(warnings)
    return {
        "ok": total_errors == 0,
        "project_path": str(project),
        "slide_count": len(slides),
        "error_count": total_errors,
        "warning_count": total_warnings,
        "slides": slides,
    }


def _require_runtime() -> None:
    missing = [p for p in (RUNTIME_DIR, SCRIPTS_DIR, TEMPLATES_DIR) if not p.exists()]
    if missing:
        raise PPTMasterError("PPT Master runtime is incomplete: " + ", ".join(str(p) for p in missing))


def _run_script(args: list[str | Path], timeout: int) -> CommandResult:
    _require_runtime()
    cmd = [sys.executable] + [str(a) for a in args]
    env = None
    proc = subprocess.run(
        cmd,
        cwd=str(RUNTIME_DIR),
        text=True,
        capture_output=True,
        timeout=timeout,
        env=env,
    )
    return CommandResult(
        ok=proc.returncode == 0,
        stdout=proc.stdout,
        stderr=proc.stderr,
        returncode=proc.returncode,
    )


def _format_command_error(name: str, result: CommandResult) -> str:
    stderr = result.stderr.strip()
    stdout = result.stdout.strip()
    detail = stderr or stdout or "no output"
    return f"{name} failed with code {result.returncode}: {detail}"


def _normalize_format(canvas_format: str) -> str:
    value = (canvas_format or "ppt169").strip().lower()
    if value == "xhs":
        return "xiaohongshu"
    return value if value in _FORMAT_VIEWBOX else "ppt169"


def _slugify(value: str) -> str:
    out = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    out = re.sub(r"_+", "_", out).strip("._-")
    return (out or "deck")[:80]


def _unique_project_path(root: Path, slug: str, fmt: str, date: str) -> Path:
    candidate = root / f"{slug}_{fmt}_{date}"
    if not candidate.exists():
        candidate.mkdir(parents=True)
        return candidate
    for i in range(2, 1000):
        candidate = root / f"{slug}_{i}_{fmt}_{date}"
        if not candidate.exists():
            candidate.mkdir(parents=True)
            return candidate
    raise PPTMasterError(f"could not allocate a unique project directory under {root}")


def _resolve_project(project_path: str) -> Path:
    project = Path(project_path).expanduser().resolve()
    if not project.exists():
        raise PPTMasterError(f"project does not exist: {project}")
    if not project.is_dir():
        raise PPTMasterError(f"project path is not a directory: {project}")
    (project / "svg_output").mkdir(parents=True, exist_ok=True)
    (project / "notes").mkdir(parents=True, exist_ok=True)
    (project / "exports").mkdir(parents=True, exist_ok=True)
    return project


def _validate_svg(svg: str) -> None:
    if not svg or "<svg" not in svg:
        raise PPTMasterError("SVG content must contain an <svg> root")
    try:
        root = ET.fromstring(svg.encode("utf-8"))
    except ET.ParseError as exc:
        raise PPTMasterError(f"invalid SVG XML: {exc}") from exc
    tag = root.tag.split("}", 1)[-1].lower()
    if tag != "svg":
        raise PPTMasterError(f"root element must be <svg>, got <{tag}>")


def _svg_static_warnings(svg: str) -> list[str]:
    """Cheap SVG lint for issues that frequently survive into PPTX export.

    This is intentionally advisory.  It catches obvious text overflow before a
    render/VLM pass, without trying to be a browser layout engine.
    """
    warnings: list[str] = []
    try:
        root = ET.fromstring(svg.encode("utf-8"))
    except ET.ParseError:
        return warnings

    width, height = _svg_canvas_size(root)
    for el in root.iter():
        if el.tag.split("}", 1)[-1] != "text":
            continue
        text = "".join(el.itertext()).strip()
        if not text:
            continue
        try:
            x = float(str(el.attrib.get("x", "0")).replace("px", ""))
            y = float(str(el.attrib.get("y", "0")).replace("px", ""))
            font_size = float(str(el.attrib.get("font-size", "16")).replace("px", ""))
        except ValueError:
            continue
        estimated_width = len(text) * font_size * 0.56
        if x + estimated_width > width + 8:
            warnings.append(
                f"text may overflow right edge: {text[:48]!r} "
                f"(x={x:.0f}, est_width={estimated_width:.0f}, canvas_width={width:.0f})"
            )
        if y < -font_size or y > height + font_size:
            warnings.append(
                f"text y-position may be outside canvas: {text[:48]!r} "
                f"(y={y:.0f}, canvas_height={height:.0f})"
            )
    return warnings[:8]


def _svg_layout_issues(svg: str, *, strict: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        root = ET.fromstring(svg.encode("utf-8"))
    except ET.ParseError as exc:
        return [f"invalid SVG XML: {exc}"], []

    width, height = _svg_canvas_size(root)
    text_boxes: list[dict[str, float | str]] = []
    shape_boxes: list[dict[str, float | str]] = []
    connector_boxes: list[dict[str, float | str]] = []
    drawable_count = 0

    def walk(el: ET.Element, tx: float = 0.0, ty: float = 0.0) -> None:
        nonlocal drawable_count
        ntx, nty = _translate_offset(el.attrib.get("transform", ""), tx, ty)
        tag = el.tag.split("}", 1)[-1].lower()
        if tag in {"text", "rect", "circle", "ellipse", "image", "path", "polygon", "polyline", "line"}:
            drawable_count += 1
        if tag == "text":
            box = _text_bbox(el, ntx, nty)
            if box:
                text_boxes.append(box)
                _check_bbox(box, width, height, errors, warnings)
                if box["x"] + box["w"] > width + 8:
                    msg = (
                        f"text may overflow right edge: {str(box['text'])[:48]!r} "
                        f"(x={box['x']:.0f}, est_width={box['w']:.0f}, canvas_width={width:.0f})"
                    )
                    (errors if strict else warnings).append(msg)
        elif tag in {"rect", "image", "circle", "ellipse"}:
            box = _shape_bbox(el, tag, ntx, nty)
            if box:
                shape_boxes.append(box)
                _check_bbox(box, width, height, errors, warnings)
        elif tag in {"line", "path", "polyline"}:
            box = _connector_bbox(el, tag, ntx, nty)
            if box:
                connector_boxes.append(box)
                _check_bbox(box, width, height, errors, warnings)
        for child in list(el):
            walk(child, ntx, nty)

    walk(root)

    if drawable_count == 0:
        errors.append("slide has no drawable SVG elements")
    if not text_boxes:
        warnings.append("slide has no text elements")

    # ---- Text-text overlap (lowered threshold; catches visible 'side-by-side' overlaps) ----
    overlap_hits = 0
    for i, a in enumerate(text_boxes):
        for b in text_boxes[i + 1:]:
            ratio = _bbox_overlap_ratio(a, b)
            if ratio > 0.15:
                overlap_hits += 1
                msg = (
                    f"text overlap: {str(a['text'])[:32]!r} vs {str(b['text'])[:32]!r} "
                    f"(overlap={ratio:.2f})"
                )
                (errors if strict else warnings).append(msg)
                if overlap_hits >= 6:
                    break
        if overlap_hits >= 6:
            break

    # ---- Text-text near-gap (visually crowded but not strictly overlapping) ----
    gap_hits = 0
    for i, a in enumerate(text_boxes):
        for b in text_boxes[i + 1:]:
            if _bbox_overlap_ratio(a, b) > 0:
                continue  # already flagged above
            ay1, ay2 = float(a["y"]), float(a["y"]) + float(a["h"])
            by1, by2 = float(b["y"]), float(b["y"]) + float(b["h"])
            y_overlap = min(ay2, by2) - max(ay1, by1)
            if y_overlap < min(float(a["h"]), float(b["h"])) * 0.5:
                continue  # not sharing a horizontal band
            ax1, ax2 = float(a["x"]), float(a["x"]) + float(a["w"])
            bx1, bx2 = float(b["x"]), float(b["x"]) + float(b["w"])
            gap = max(bx1 - ax2, ax1 - bx2)
            if 0 < gap < 16:
                gap_hits += 1
                warnings.append(
                    f"text blocks too close (gap={gap:.0f}px): "
                    f"{str(a['text'])[:24]!r} vs {str(b['text'])[:24]!r}"
                )
                if gap_hits >= 6:
                    break
        if gap_hits >= 6:
            break

    # ---- Text overlaps a connector/arrow line ----
    connector_hits = 0
    for text_box in text_boxes:
        for connector in connector_boxes:
            ratio = _bbox_overlap_ratio(text_box, connector)
            if ratio > 0.18:
                connector_hits += 1
                msg = (
                    f"text overlaps connector/arrow: {str(text_box['text'])[:32]!r} "
                    f"(overlap={ratio:.2f})"
                )
                (errors if strict else warnings).append(msg)
                if connector_hits >= 8:
                    break
        if connector_hits >= 8:
            break

    # ---- Shape-shape overlap (two cards visibly stacked) ----
    # Only flag when both shapes are of SIMILAR SIZE — "small icon inside big
    # card" is a legitimate container-and-content pattern (ratio=1.0 because
    # the smaller is fully contained), not a stacking bug.
    shape_overlap_hits = 0
    for i, a in enumerate(shape_boxes):
        for b in shape_boxes[i + 1:]:
            area_a = max(1e-6, float(a["w"]) * float(a["h"]))
            area_b = max(1e-6, float(b["w"]) * float(b["h"]))
            size_ratio = min(area_a, area_b) / max(area_a, area_b)
            if size_ratio < 0.5:
                continue  # one fits inside the other; not a stacking pattern
            ratio = _bbox_overlap_ratio(a, b)
            if ratio > 0.30:
                shape_overlap_hits += 1
                warnings.append(
                    f"shape overlap: {a['kind']} vs {b['kind']} "
                    f"(overlap={ratio:.2f}, size_ratio={size_ratio:.2f})"
                )
                if shape_overlap_hits >= 6:
                    break
        if shape_overlap_hits >= 6:
            break

    # ---- Text spilling out of its container shape ----
    # Text fully inside a shape is OK (label-on-card pattern). Text that
    # partially overlaps a shape but isn't contained in ANY shape is
    # "spilling" — almost always a visible layout bug.
    text_spill_hits = 0
    for tb in text_boxes:
        overlapping_shapes = [
            sb for sb in shape_boxes
            if _bbox_overlap_ratio(tb, sb) > 0.05
        ]
        if not overlapping_shapes:
            continue
        tx1, ty1 = float(tb["x"]), float(tb["y"])
        tx2, ty2 = tx1 + float(tb["w"]), ty1 + float(tb["h"])
        fully_inside = False
        for sb in overlapping_shapes:
            sx1, sy1 = float(sb["x"]), float(sb["y"])
            sx2, sy2 = sx1 + float(sb["w"]), sy1 + float(sb["h"])
            if tx1 >= sx1 - 2 and ty1 >= sy1 - 2 and tx2 <= sx2 + 2 and ty2 <= sy2 + 2:
                fully_inside = True
                break
        if not fully_inside:
            text_spill_hits += 1
            warnings.append(
                f"text overlaps shape but spills out: {str(tb['text'])[:32]!r}"
            )
            if text_spill_hits >= 6:
                break

    return errors[:16], warnings[:16]


def _translate_offset(transform: str, base_x: float, base_y: float) -> tuple[float, float]:
    tx, ty = base_x, base_y
    if not transform:
        return tx, ty
    for match in re.finditer(r"translate\(([^)]*)\)", transform):
        nums = _numbers(match.group(1))
        if nums:
            tx += nums[0]
            ty += nums[1] if len(nums) > 1 else 0.0
    return tx, ty


def _numbers(value: str) -> list[float]:
    out: list[float] = []
    for token in re.findall(r"-?\d+(?:\.\d+)?", value or ""):
        try:
            out.append(float(token))
        except ValueError:
            pass
    return out


def _text_bbox(el: ET.Element, tx: float, ty: float) -> dict[str, float | str] | None:
    text = "".join(el.itertext()).strip()
    if not text:
        return None
    try:
        x = float(str(el.attrib.get("x", "0")).replace("px", "")) + tx
        y = float(str(el.attrib.get("y", "0")).replace("px", "")) + ty
        font_size = float(str(el.attrib.get("font-size", "16")).replace("px", ""))
    except ValueError:
        return None
    anchor = el.attrib.get("text-anchor", "start")
    estimated_width = len(text) * font_size * 0.56
    if anchor == "middle":
        x -= estimated_width / 2
    elif anchor == "end":
        x -= estimated_width
    return {
        "x": x,
        "y": y - font_size * 0.82,
        "w": estimated_width,
        "h": font_size * 1.14,
        "text": text,
        "kind": "text",
    }


def _shape_bbox(el: ET.Element, tag: str, tx: float, ty: float) -> dict[str, float | str] | None:
    def num(name: str, default: float = 0.0) -> float:
        return float(str(el.attrib.get(name, default)).replace("px", ""))
    try:
        if tag in {"rect", "image"}:
            return {"x": num("x") + tx, "y": num("y") + ty, "w": num("width"), "h": num("height"), "text": tag, "kind": tag}
        if tag == "circle":
            r = num("r")
            return {"x": num("cx") - r + tx, "y": num("cy") - r + ty, "w": r * 2, "h": r * 2, "text": tag, "kind": tag}
        if tag == "ellipse":
            rx, ry = num("rx"), num("ry")
            return {"x": num("cx") - rx + tx, "y": num("cy") - ry + ty, "w": rx * 2, "h": ry * 2, "text": tag, "kind": tag}
    except ValueError:
        return None
    return None


def _connector_bbox(el: ET.Element, tag: str, tx: float, ty: float) -> dict[str, float | str] | None:
    stroke = el.attrib.get("stroke")
    if not stroke or stroke.lower() == "none":
        return None
    fill = (el.attrib.get("fill") or "").lower()
    # Filled paths/polylines are often large decorative areas. Only treat
    # unfilled stroked geometry as connectors for text-collision checks.
    if tag in {"path", "polyline"} and fill not in {"", "none"}:
        return None
    try:
        stroke_width = float(str(el.attrib.get("stroke-width", "1")).replace("px", ""))
    except ValueError:
        stroke_width = 1.0
    pad = max(4.0, stroke_width * 1.5)
    try:
        if tag == "line":
            nums = [
                float(str(el.attrib.get(name, "0")).replace("px", ""))
                for name in ("x1", "y1", "x2", "y2")
            ]
            xs = [nums[0] + tx, nums[2] + tx]
            ys = [nums[1] + ty, nums[3] + ty]
        else:
            nums = _numbers(el.attrib.get("points", "") if tag == "polyline" else el.attrib.get("d", ""))
            if len(nums) < 4:
                return None
            xs = [nums[i] + tx for i in range(0, len(nums) - 1, 2)]
            ys = [nums[i] + ty for i in range(1, len(nums), 2)]
    except ValueError:
        return None
    if not xs or not ys:
        return None
    x1, x2 = min(xs) - pad, max(xs) + pad
    y1, y2 = min(ys) - pad, max(ys) + pad
    return {
        "x": x1,
        "y": y1,
        "w": max(1.0, x2 - x1),
        "h": max(1.0, y2 - y1),
        "text": "connector",
        "kind": "connector",
    }


def _check_bbox(
    box: dict[str, float | str],
    width: float,
    height: float,
    errors: list[str],
    warnings: list[str],
) -> None:
    x, y, w, h = float(box["x"]), float(box["y"]), float(box["w"]), float(box["h"])
    label = str(box.get("text", ""))[:48]
    is_text = str(box.get("kind", "")) == "text"
    fully_outside = x + w < 0 or y + h < 0 or x > width or y > height
    if fully_outside:
        errors.append(
            f"element outside canvas: {label!r} "
            f"(bbox {x:.0f},{y:.0f},{x+w:.0f},{y+h:.0f}; canvas {width:.0f}x{height:.0f})"
        )
    elif is_text and (x < -80 or y < -80 or x + w > width + 80 or y + h > height + 80):
        errors.append(
            f"text outside canvas: {label!r} "
            f"(bbox {x:.0f},{y:.0f},{x+w:.0f},{y+h:.0f}; canvas {width:.0f}x{height:.0f})"
        )
    elif x < -8 or y < -8 or x + w > width + 8 or y + h > height + 8:
        warnings.append(
            f"element near/outside canvas edge: {label!r} "
            f"(bbox {x:.0f},{y:.0f},{x+w:.0f},{y+h:.0f}; canvas {width:.0f}x{height:.0f})"
        )


def _bbox_overlap_ratio(a: dict[str, float | str], b: dict[str, float | str]) -> float:
    ax1, ay1 = float(a["x"]), float(a["y"])
    ax2, ay2 = ax1 + float(a["w"]), ay1 + float(a["h"])
    bx1, by1 = float(b["x"]), float(b["y"])
    bx2, by2 = bx1 + float(b["w"]), by1 + float(b["h"])
    iw = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    ih = max(0.0, min(ay2, by2) - max(ay1, by1))
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(1.0, float(a["w"]) * float(a["h"]))
    area_b = max(1.0, float(b["w"]) * float(b["h"]))
    return inter / min(area_a, area_b)


def _svg_canvas_size(root: ET.Element) -> tuple[float, float]:
    viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox") or ""
    parts = viewbox.replace(",", " ").split()
    if len(parts) == 4:
        try:
            return float(parts[2]), float(parts[3])
        except ValueError:
            pass
    def _num(name: str, default: float) -> float:
        try:
            return float(str(root.attrib.get(name, default)).replace("px", ""))
        except ValueError:
            return default
    return _num("width", 1280.0), _num("height", 720.0)


def _ensure_svg_trailing_newline(svg: str) -> str:
    return svg if svg.endswith("\n") else svg + "\n"


def _normalize_slide_stem(slide_name: str, svg_dir: Path) -> str:
    name = (slide_name or "").strip()
    if name.endswith(".svg"):
        name = name[:-4]
    if not name:
        idx = len(list(svg_dir.glob("*.svg"))) + 1
        return f"{idx:02d}_slide"
    stem = _slugify(name)
    if not re.match(r"^\d{2}[_-]", stem):
        idx = len(list(svg_dir.glob("*.svg"))) + 1
        stem = f"{idx:02d}_{stem}"
    return stem


def _resolve_svg(project: Path, slide_name: str) -> Path:
    if not slide_name:
        raise PPTMasterError("slide_name is required")
    candidate = Path(slide_name)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    name = candidate.name
    if not name.endswith(".svg"):
        name = f"{name}.svg"
    direct = project / "svg_output" / name
    if direct.exists():
        return direct
    # Allow lookup by stem without numeric prefix.
    stem = Path(name).stem
    matches = [p for p in (project / "svg_output").glob("*.svg") if p.stem == stem or p.stem.endswith(f"_{stem}")]
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise PPTMasterError(f"ambiguous slide_name {slide_name!r}: {[p.name for p in matches]}")
    raise PPTMasterError(f"slide not found: {slide_name}")


def _default_export_path(project: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return project / "exports" / f"{project.name}_{timestamp}.pptx"


def _normalize_template_kind(kind: str) -> str:
    value = (kind or "layout").strip().lower()
    aliases = {
        "layouts": "layout",
        "brand": "brand",
        "brands": "brand",
        "deck": "deck",
        "decks": "deck",
        "chart": "chart",
        "charts": "chart",
        "visualization": "chart",
    }
    normalized = aliases.get(value, value)
    if normalized not in {"brand", "layout", "deck", "chart"}:
        raise PPTMasterError("kind must be one of: brand, layout, deck, chart")
    return normalized


def _template_dir(kind: str) -> Path:
    dirname = "charts" if kind == "chart" else f"{kind}s"
    return TEMPLATES_DIR / dirname


def _template_index_path(kind: str) -> Path:
    dirname = "charts" if kind == "chart" else f"{kind}s"
    filename = "charts_index.json" if kind == "chart" else f"{kind}s_index.json"
    return TEMPLATES_DIR / dirname / filename


def _resolve_template_svg(template_dir: Path, svg_name: str) -> Path:
    name = svg_name.strip()
    if not name.endswith(".svg"):
        name = f"{name}.svg"
    path = template_dir / name
    if path.exists():
        return path
    matches = [p for p in template_dir.glob("*.svg") if p.stem == Path(name).stem]
    if len(matches) == 1:
        return matches[0]
    raise PPTMasterError(f"template SVG not found: {svg_name}")
