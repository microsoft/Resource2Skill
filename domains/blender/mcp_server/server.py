"""
domains/blender/mcp_server/server.py
Unified Blender MCP Server — skill library + direct bpy execution in one server.

Uses the `bpy` Python module (headless Blender) for direct in-process execution.
No need for a separate BlenderMCP addon or socket connection.

Tools:
  Skill library:
    list_skills           — browse skill library
    get_skill_info        — skill metadata + preview
    get_skill_code        — full bpy code

  Blender native (direct bpy execution):
    execute_blender_code  — run arbitrary bpy Python code
    get_scene_info        — scene object list, render engine, etc.
    get_viewport_screenshot — render a viewport preview as base64 PNG
    add_object_from_skill — execute skill code directly in bpy
    render_scene          — full render to demo/blender/
    save_scene            — save .blend to demo/blender/

Usage (stdio transport):
    python domains/blender/mcp_server/server.py --skills-dir skills_library/blender
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import io
import json
import logging
import os
import re
import sys
import tempfile
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

_SERVER_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SERVER_DIR.parents[2]
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_SERVER_DIR))

from mcp.server.fastmcp import FastMCP
from core.skill_grounding import artifact_manifest_path, make_grounding_entries, write_manifest

log = logging.getLogger("blender-mcp")

# ---------------------------------------------------------------------------
# Lazy imports — bpy is heavy, only import when first needed
# ---------------------------------------------------------------------------

_bpy = None
_engine = None


def _get_bpy():
    global _bpy
    if _bpy is None:
        # Suppress Blender's noisy render timing output that pollutes MCP stdio
        import contextlib
        old_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        try:
            import bpy
            _bpy = bpy
        finally:
            sys.stderr.close()
            sys.stderr = old_stderr
        log.info("bpy loaded: Blender %s", bpy.app.version_string)
    return _bpy


def _get_engine():
    global _engine
    if not _engine:
        import blender_engine
        _engine = blender_engine
    return _engine


@contextlib.contextmanager
def _suppress_render_output():
    """Silence Blender C/Python render output while preserving MCP stdio."""
    old_stdout_obj = sys.stdout
    old_stderr_obj = sys.stderr
    devnull = open(os.devnull, "w")
    saved_stdout_fd = None
    saved_stderr_fd = None
    try:
        try:
            saved_stdout_fd = os.dup(1)
            os.dup2(devnull.fileno(), 1)
        except OSError:
            saved_stdout_fd = None
        try:
            saved_stderr_fd = os.dup(2)
            os.dup2(devnull.fileno(), 2)
        except OSError:
            saved_stderr_fd = None
        sys.stdout = devnull
        sys.stderr = devnull
        yield
    finally:
        if saved_stdout_fd is not None:
            os.dup2(saved_stdout_fd, 1)
            os.close(saved_stdout_fd)
        if saved_stderr_fd is not None:
            os.dup2(saved_stderr_fd, 2)
            os.close(saved_stderr_fd)
        sys.stdout = old_stdout_obj
        sys.stderr = old_stderr_obj
        devnull.close()


# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------

_skills_dir: Path | None = None
_skill_index: list[dict] | None = None
_skill_metadata: dict | None = None
_demo_dir: Path = _PROJECT_ROOT / "demo" / "blender"
_skill_groundings: list[dict] = []


def _append_groundings(
    *,
    tool_name: str,
    from_skill_ids,
    target_node: str = "",
    adaptation_notes: str = "",
    fallback_target: str = "",
    extra: dict | None = None,
) -> list[dict]:
    entries = make_grounding_entries(
        domain="blender",
        tool_name=tool_name,
        from_skill_ids=from_skill_ids,
        target_node=target_node,
        adaptation_notes=adaptation_notes,
        fallback_target=fallback_target,
        extra=extra,
    )
    if entries:
        _skill_groundings.extend(entries)
    return entries


def _write_skill_manifest(artifact_path: str | Path) -> str:
    path = artifact_manifest_path(artifact_path)
    write_manifest(
        path,
        {
            "domain": "blender",
            "groundings": _skill_groundings,
        },
        domain="blender",
    )
    return str(path)


def _ensure_skills_loaded():
    """Load skill index and metadata from disk."""
    global _skill_index, _skill_metadata
    if _skill_index is not None:
        return

    if not _skills_dir or not _skills_dir.exists():
        _skill_index = []
        _skill_metadata = {}
        return

    index_path = _skills_dir / "index.json"
    if index_path.exists():
        data = json.loads(index_path.read_text(encoding="utf-8"))
        _skill_index = data.get("skills", data) if isinstance(data, dict) else data
    else:
        _skill_index = []

    meta_path = _skills_dir / "metadata.json"
    if meta_path.exists():
        raw = json.loads(meta_path.read_text(encoding="utf-8"))
        _skill_metadata = raw.get("metadata", raw) if isinstance(raw, dict) else {}
    else:
        _skill_metadata = {}


def _reload_skills():
    """Force-reload skill index (after new skills are added)."""
    global _skill_index, _skill_metadata
    _skill_index = None
    _skill_metadata = None
    _ensure_skills_loaded()


# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("blender-mcp")


# Server-owned reload_registry — exempt from the legacy stale guard so the
# documented stale_registry remediation path is real on this hybrid server.
@mcp.tool()
def reload_registry() -> dict:
    """Refresh the wiki discovery surface from disk and re-key the stale guard."""
    info: dict = {"reloaded": True, "domain": "blender"}
    try:
        from domains.blender.wiki_adapter import BlenderWikiAdapter
        from core.skill_wiki.mcp_tools import register_wiki_tools
        from core.skill_wiki.legacy_stale import mark_runtime_backend
        from core import get_active_library_backend
        register_wiki_tools(mcp, BlenderWikiAdapter())
        backend = get_active_library_backend("blender")
        mark_runtime_backend(mcp, backend)
        info["backend"] = backend
        info["tool_surface"] = "wiki+legacy"
    except Exception as exc:  # noqa: BLE001
        info["error"] = f"{type(exc).__name__}: {exc}"
    return info


# ===== Blender Native Tools =====

@mcp.tool()
def execute_blender_code(
    code: str,
    from_skill_ids: str = "",
    target_node: str = "",
    adaptation_notes: str = "",
) -> str:
    """Execute arbitrary Python code in the Blender environment.

The code has access to `bpy` and all Blender Python APIs.
stdout/stderr from the code is captured and returned.

Args:
    code: Python code to execute (must be valid bpy code).
    from_skill_ids: optional JSON/comma list of inspected wiki skill ids whose
        visual/code mechanisms this generated bpy code adapts.
    target_node: optional object/material/lighting/composition role, or
        JSON/comma list for multiple grounded scene roles.
    adaptation_notes: optional note describing borrowed mechanisms.

Returns:
    Captured stdout output, or error traceback on failure.
"""
    bpy = _get_bpy()

    # Capture stdout and redirect stderr to devnull (suppress Blender render timing)
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    captured = io.StringIO()
    sys.stdout = captured
    sys.stderr = open(os.devnull, 'w')

    try:
        exec(compile(code, "<agent-code>", "exec"), {"bpy": bpy, "__builtins__": __builtins__})
        output = captured.getvalue()
        entries = _append_groundings(
            tool_name="execute_blender_code",
            from_skill_ids=from_skill_ids,
            target_node=target_node,
            adaptation_notes=adaptation_notes,
            fallback_target=target_node or "scene_code",
            extra={"code_chars": len(code)},
        )
        suffix = f"\ngrounded_sections={len(entries)}" if entries else ""
        return (output if output.strip() else "Code executed successfully (no output)") + suffix
    except Exception:
        output = captured.getvalue()
        tb = traceback.format_exc()
        return f"{output}\nError:\n{tb}" if output else f"Error:\n{tb}"
    finally:
        sys.stderr.close()
        sys.stdout = old_stdout
        sys.stderr = old_stderr


@mcp.tool()
def get_scene_info() -> str:
    """Get information about the current Blender scene.

Returns:
    Scene name, render engine, object list with types and locations.
"""
    bpy = _get_bpy()
    scene = bpy.context.scene

    lines = [
        f"Scene: {scene.name}",
        f"Render Engine: {scene.render.engine}",
        f"Frame: {scene.frame_current} (range: {scene.frame_start}-{scene.frame_end})",
        f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}",
        f"Objects ({len(bpy.data.objects)}):",
    ]

    for obj in bpy.data.objects:
        loc = obj.location
        lines.append(
            f"  - {obj.name} [{obj.type}] at ({loc.x:.2f}, {loc.y:.2f}, {loc.z:.2f})"
        )
        if obj.type == 'MESH' and obj.data:
            lines.append(f"    verts={len(obj.data.vertices)}, faces={len(obj.data.polygons)}")
        if obj.active_material:
            lines.append(f"    material: {obj.active_material.name}")

    # Active object
    active = bpy.context.view_layer.objects.active
    if active:
        lines.append(f"Active Object: {active.name}")

    return "\n".join(lines)


@mcp.tool()
def get_viewport_screenshot(width: int = 512, height: int = 512) -> str:
    """Render a quick viewport preview of the current scene.

Uses EEVEE for fast rendering. Returns JSON with `_image_attachment` so the
agent loop can attach the PNG to the next vision turn without embedding base64
inside the tool result.

Args:
    width: Preview width in pixels (default 512).
    height: Preview height in pixels (default 512).

Returns:
    JSON containing path, `_image_attachment`, and scene summary.
"""
    bpy = _get_bpy()
    scene = bpy.context.scene

    # Save current settings
    old_engine = scene.render.engine
    old_x = scene.render.resolution_x
    old_y = scene.render.resolution_y
    old_path = scene.render.filepath

    try:
        # Use EEVEE for fast preview
        scene.render.engine = 'BLENDER_EEVEE'
        scene.render.resolution_x = width
        scene.render.resolution_y = height

        # Per-call unique path under /data/tmp to avoid collisions between
        # concurrent MCP processes (all using the same demo/blender/ dir would
        # corrupt each other's renders during high-concurrency benches).
        import tempfile as _tempfile
        _scratch_dir = "/data/tmp"
        os.makedirs(_scratch_dir, exist_ok=True)
        _fd, preview_path = _tempfile.mkstemp(
            dir=_scratch_dir, prefix="bpy_preview_", suffix=".png"
        )
        os.close(_fd)
        scene.render.filepath = preview_path
        scene.render.image_settings.file_format = 'PNG'

        with _suppress_render_output():
            bpy.ops.render.render(write_still=True)

        if os.path.exists(preview_path):
            size_kb = os.path.getsize(preview_path) / 1024
            obj_names = [o.name for o in bpy.data.objects]
            image_metrics = _png_image_metrics(preview_path)
            return json.dumps({
                "path": preview_path,
                "_image_attachment": preview_path,
                "size_kb": round(size_kb, 1),
                "resolution": f"{width}x{height}",
                "image_metrics": image_metrics,
                "objects": obj_names,
                "summary": (
                    f"Viewport preview saved to {preview_path} "
                    f"({size_kb:.0f} KB). Objects in scene: "
                    f"{', '.join(obj_names)}"
                ),
            }, ensure_ascii=False, indent=2)
        return "Error: render produced no output file"
    except Exception as e:
        return f"Error rendering preview: {e}"
    finally:
        scene.render.engine = old_engine
        scene.render.resolution_x = old_x
        scene.render.resolution_y = old_y
        scene.render.filepath = old_path


# ===== Skill Library Tools =====

@mcp.tool()
def list_skills(category: str = "", query: str = "", verified_only: bool = False) -> str:
    """List or search skills in the Blender 3D skill library.

Args:
    category: Filter by category (e.g., 'environment', 'material_shader').
              Leave empty for category summary.
    query: Search query to filter skills by name.
    verified_only: Only show verified skills (default: false).

Returns:
    List of matching skills with IDs and metadata.
"""
    _ensure_skills_loaded()
    if not _skill_index:
        return "Skill library is empty. Collect and analyze tutorials first."

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
    """Get detailed information about a specific Blender skill.

Args:
    skill_id: The skill ID to look up.

Returns:
    Skill details: name, category, tags, scope, code preview, and reference images.
"""
    _ensure_skills_loaded()
    engine = _get_engine()
    detail = engine.get_skill_detail(_skills_dir, skill_id, _skill_index or [])
    if not detail:
        return f"Error: skill '{skill_id}' not found"

    name = detail.get("skill_name", skill_id)
    cat = detail.get("category", "unknown")
    meta = (_skill_metadata or {}).get(skill_id, {})

    lines = [f"Skill: {name}"]
    lines.append(f"  ID: {skill_id}")
    lines.append(f"  Category: {cat}")

    # Source info
    source = detail.get("source", {})
    if source.get("video_title"):
        lines.append(f"  Source: {source['video_title']}")
    if source.get("channel"):
        lines.append(f"  Channel: {source['channel']}")

    if meta:
        lines.append(f"  Scope: {meta.get('scope', '?')}")
        lines.append(f"  Complexity: {meta.get('complexity', '?')}")
        tags = meta.get("semantic_tags", [])
        if tags:
            lines.append(f"  Tags: {', '.join(tags)}")
        lines.append(f"  Exec OK: {meta.get('exec_ok', '?')}")
        obj_names = meta.get("object_names", [])
        if obj_names:
            lines.append(f"  Creates: {', '.join(obj_names)}")

    # Reference images
    skill_dir = detail.get("_skill_dir", "")
    if skill_dir:
        skill_path = Path(skill_dir)
        images = []
        # Thumbnail
        thumb = skill_path / "thumbnail.jpg"
        if thumb.exists():
            images.append(f"    thumbnail: {thumb} ({thumb.stat().st_size // 1024} KB)")
        # Key frames
        for f in sorted(skill_path.glob("frame_*.jpg")):
            images.append(f"    frame: {f} ({f.stat().st_size // 1024} KB)")
        if images:
            lines.append("  Reference Images:")
            lines.extend(images)
            lines.append("  (Use these images as visual reference for what this skill creates)")

    # Frames from analysis
    frames = detail.get("frames", [])
    if frames:
        lines.append(f"  Key Frames ({len(frames)}):")
        for f in frames:
            lines.append(f"    t={f.get('seconds', '?')}s: {f.get('description', '?')}")

    analysis = detail.get("analysis", "")
    code = engine.extract_code_from_analysis(analysis)
    if code:
        preview = "\n".join(code.split("\n")[:8])
        lines.append(f"  Code preview:\n    {preview}")

    return "\n".join(lines)


@mcp.tool()
def get_skill_code(skill_id: str) -> str:
    """Get full bpy Python code from a skill.

Args:
    skill_id: The skill ID to look up.

Returns:
    Full code with create_object() function and detected techniques.
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

    mechanism = ""
    m = re.search(r'\*\*Core (?:Visual )?Mechanism\*\*[:\s]*(.+?)(?:\n\n|\n\*\*)', analysis, re.DOTALL)
    if m:
        mechanism = m.group(1).strip()[:300]

    techniques = []
    if 'bpy.ops.mesh' in code:
        techniques.append('MESH_OPS')
    if 'nodes' in code.lower() and 'shader' in code.lower():
        techniques.append('SHADER_NODES')
    if 'geometry_nodes' in code.lower() or 'GeometryNodeTree' in code:
        techniques.append('GEOMETRY_NODES')
    if 'keyframe' in code.lower():
        techniques.append('ANIMATION')
    if 'particle' in code.lower():
        techniques.append('PARTICLES')
    if 'modifier' in code.lower():
        techniques.append('MODIFIERS')

    lines = [f"# Skill Reference: {name}"]
    if mechanism:
        lines.append(f"\n## Visual Mechanism\n{mechanism}")
    if techniques:
        lines.append(f"\n## Detected Techniques\n" + "\n".join(f"- {t}" for t in techniques))

    # Reference images for visual guidance
    skill_dir = detail.get("_skill_dir", "")
    if skill_dir:
        skill_path = Path(skill_dir)
        ref_images = []
        thumb = skill_path / "thumbnail.jpg"
        if thumb.exists():
            ref_images.append(f"- Thumbnail: {thumb}")
        for f in sorted(skill_path.glob("frame_*.jpg")):
            ref_images.append(f"- Frame: {f}")
        if ref_images:
            lines.append("\n## Visual References (from tutorial video)")
            lines.extend(ref_images)
            lines.append("Match your output to these reference images when using this skill.")

    lines.append(f"\n## Full Code ({len(code.splitlines())} lines)\n```python\n{code}\n```")
    return "\n".join(lines)


@mcp.tool()
def add_object_from_skill(
    skill_id: str,
    object_name: str = "",
    location: str = "0,0,0",
    scale: float = 1.0,
) -> str:
    """Execute a skill's create_object() code directly in Blender.

This loads the skill code and runs it in the bpy environment immediately.

Args:
    skill_id: Skill ID from list_skills.
    object_name: Override the default object name.
    location: Object location as 'x,y,z' (default: '0,0,0').
    scale: Object scale factor (default: 1.0).

Returns:
    Names of newly created objects, or error message.
"""
    _ensure_skills_loaded()
    engine = _get_engine()
    detail = engine.get_skill_detail(_skills_dir, skill_id, _skill_index or [])
    if not detail:
        return f"Error: skill '{skill_id}' not found"

    code = engine.extract_code_from_analysis(detail.get("analysis", ""))
    if not code:
        return f"Error: no code found in skill '{skill_id}'"

    # Parse location
    try:
        loc = tuple(float(x.strip()) for x in location.split(","))
    except ValueError:
        loc = (0, 0, 0)

    params = {"location": loc, "scale": scale}
    if object_name:
        params["object_name"] = object_name

    wrapped = engine.wrap_skill_for_blender(code, params)
    skill_name = detail.get("skill_name", skill_id)

    # Execute directly in bpy
    result = execute_blender_code(wrapped)

    # Parse result
    success, obj_names = engine.parse_skill_result(result)
    if success:
        _append_groundings(
            tool_name="add_object_from_skill",
            from_skill_ids=[skill_id],
            target_node=object_name or ", ".join(obj_names) or skill_id,
            adaptation_notes=f"direct object skill; location={location}; scale={scale}",
            extra={"skill_name": skill_name},
        )
    if success and obj_names:
        return f"Added from skill '{skill_name}': {', '.join(obj_names)}\n{result}"
    elif success:
        return f"Skill '{skill_name}' executed (no new objects detected)\n{result}"
    else:
        return f"Skill '{skill_name}' failed:\n{result}"


@mcp.tool()
def render_scene(
    output_name: str = "render",
    width: int = 1920,
    height: int = 1080,
    samples: int = 64,
    engine: str = "EEVEE",
) -> str:
    """Render the current scene to a PNG file in demo/blender/.

Args:
    output_name: Filename (without extension).
    width: Render width in pixels.
    height: Render height in pixels.
    samples: Render samples (higher = better quality, slower).
    engine: Render engine: 'EEVEE' (fast) or 'CYCLES' (quality).

Returns:
    Path to the rendered image.
"""
    bpy = _get_bpy()
    scene = bpy.context.scene

    _demo_dir.mkdir(parents=True, exist_ok=True)
    out_path = str(_demo_dir / f"{output_name}.png")

    # Configure render
    render_engine = 'CYCLES' if engine.upper() == 'CYCLES' else 'BLENDER_EEVEE'
    scene.render.engine = render_engine
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.filepath = out_path
    scene.render.image_settings.file_format = 'PNG'

    if render_engine == 'CYCLES':
        scene.cycles.samples = samples
        scene.cycles.device = 'GPU'
    else:
        scene.eevee.taa_render_samples = samples

    # Final generic sanity pass. This is intentionally task-agnostic: it
    # prevents scored renders from being ruined by macro-cropped cameras or
    # stacked light rigs, while leaving the agent's actual geometry/materials.
    tone_changes = _normalize_render_tone(bpy)
    camera_fit = _fit_camera_to_scene(bpy)

    def _render_silent() -> None:
        with _suppress_render_output():
            bpy.ops.render.render(write_still=True)

    _render_silent()

    if os.path.exists(out_path):
        size_kb = os.path.getsize(out_path) / 1024
        metrics = _png_image_metrics(out_path)
        repair = {}
        quality_error = _render_quality_error(metrics)
        if quality_error and "underexposed" in quality_error:
            repair = _boost_render_visibility(bpy, metrics)
            if repair:
                _render_silent()
                size_kb = os.path.getsize(out_path) / 1024
                metrics = _png_image_metrics(out_path)
                quality_error = _render_quality_error(metrics)
        if quality_error:
            return (
                "Error: ARTIFACT_QUALITY_REQUIRED: final render unusable; "
                f"{quality_error}; image_metrics={json.dumps(metrics, sort_keys=True)}; "
                f"render_sanity={json.dumps({'tone_changes': tone_changes, 'camera_fit': camera_fit, 'repair': repair}, sort_keys=True)}"
            )
        manifest_path = _write_skill_manifest(out_path)
        return (
            f"Rendered to {out_path} ({size_kb:.0f} KB, {width}x{height}, "
            f"{render_engine}); image_metrics={json.dumps(metrics, sort_keys=True)}; "
            f"render_sanity={json.dumps({'tone_changes': tone_changes, 'camera_fit': camera_fit, 'repair': repair}, sort_keys=True)}; "
            f"skill_trace_manifest={manifest_path}"
        )
    return "Error: render produced no output file"


@mcp.tool()
def save_scene(output_name: str = "my_scene") -> str:
    """Save the .blend file to demo/blender/.

Args:
    output_name: Filename (without extension) for the saved scene.

Returns:
    Path to the saved .blend file.
"""
    bpy = _get_bpy()

    _demo_dir.mkdir(parents=True, exist_ok=True)
    filepath = str(_demo_dir / f"{output_name}.blend")

    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    manifest_path = _write_skill_manifest(filepath)
    return f"Saved scene to {filepath} ({size_mb:.1f} MB); skill_trace_manifest={manifest_path}"


# ---------------------------------------------------------------------------
# Tier-based design system: material presets / lighting rigs / scene shells
# ---------------------------------------------------------------------------

def _list_token_kind(kind: str) -> list[str]:
    if not _skills_dir:
        return []
    base = _skills_dir / kind
    if not base.exists():
        return []
    return sorted(p.stem for p in base.glob("*.json"))


def _read_token(kind: str, name: str) -> dict:
    if not _skills_dir:
        raise RuntimeError("--skills-dir not configured")
    p = _skills_dir / kind / f"{name}.json"
    if not p.exists():
        raise FileNotFoundError(f"{kind}/{name}.json not found in {_skills_dir}")
    return json.loads(p.read_text(encoding="utf-8"))


def _load_helpers():
    """Import skills_library/blender/_helpers.py as a module."""
    import importlib.util as _ilu
    helper_path = _skills_dir / "_helpers.py"
    if not helper_path.exists():
        raise FileNotFoundError(f"_helpers.py missing in {_skills_dir}")
    spec = _ilu.spec_from_file_location("_blender_helpers", helper_path)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@mcp.tool()
def list_material_presets() -> str:
    """List PBR material preset names available under skills_library/blender/material_presets/.
    Each preset bundles Principled BSDF inputs (Base Color, Metallic, Roughness, etc.) tuned for a
    specific look (metal_brushed, glass_frosted, water_ocean, neon_emissive, …)."""
    return json.dumps({"kind": "material_presets",
                       "names": _list_token_kind("material_presets")},
                      indent=2)


@mcp.tool()
def get_material_preset(name: str) -> str:
    """Return the full JSON for a material preset (Principled BSDF inputs + best_for hint)."""
    try:
        return json.dumps(_read_token("material_presets", name), indent=2)
    except FileNotFoundError as e:
        return f"Error: {e}"


@mcp.tool()
def apply_material_preset(preset_name: str, object_name: str,
                          material_name: str = "") -> str:
    """Create a Principled-BSDF material from the preset and assign it to ``object_name``.

    Use this instead of writing raw shader-node code. Returns the material name on success.
    """
    bpy = _get_bpy()
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        return f"Error: object {object_name!r} not found"
    try:
        preset = _read_token("material_presets", preset_name)
        helpers = _load_helpers()
        mat_name = material_name or f"{preset_name}_mat"
        mat = helpers.make_principled_material(mat_name, preset)
        helpers.assign_material(obj, mat)
        return json.dumps({"ok": True, "material": mat.name,
                           "preset": preset_name, "object": object_name})
    except Exception as e:
        return f"Error: apply_material_preset failed: {e}\n{traceback.format_exc()[:500]}"


@mcp.tool()
def list_lighting_rigs() -> str:
    """List lighting rig presets (studio_3point, golden_hour, neon_corridor, overcast_overhead,
    dramatic_rim, …). Each rig is a curated set of lights + world settings for a specific mood."""
    return json.dumps({"kind": "lighting_rigs",
                       "names": _list_token_kind("lighting_rigs")},
                      indent=2)


@mcp.tool()
def get_lighting_rig(name: str) -> str:
    """Return the full JSON for a lighting rig (lights array + world strength/color)."""
    try:
        return json.dumps(_read_token("lighting_rigs", name), indent=2)
    except FileNotFoundError as e:
        return f"Error: {e}"


@mcp.tool()
def apply_lighting_rig(rig_name: str) -> str:
    """Add the rig's lights to the current scene and configure the world background.

    Replaces existing lights by default so repeated rig application does not
    stack exposure and wash out the final render.
    """
    try:
        bpy = _get_bpy()
        for obj in list(bpy.data.objects):
            if obj.type == "LIGHT":
                bpy.data.objects.remove(obj, do_unlink=True)
        rig = _read_token("lighting_rigs", rig_name)
        helpers = _load_helpers()
        created = helpers.apply_lighting_rig(rig)
        _normalize_render_tone(bpy)
        return json.dumps({"ok": True, "rig": rig_name,
                           "lights_added": [o.name for o in created],
                           "world_strength": rig.get("world_strength")})
    except Exception as e:
        return f"Error: apply_lighting_rig failed: {e}\n{traceback.format_exc()[:500]}"


def _mat(name: str, *, base=(0.2, 0.2, 0.22, 1), rough=0.55,
         metal=0.0, emission=None, strength=0.0, alpha=1.0):
    bpy = _get_bpy()
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.blend_method = "BLEND" if alpha < 1.0 else "OPAQUE"
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        inputs = bsdf.inputs
        for key, value in {
            "Base Color": base,
            "Metallic": metal,
            "Roughness": rough,
            "Alpha": alpha,
        }.items():
            if key in inputs:
                try:
                    inputs[key].default_value = value
                except Exception:
                    pass
        if emission is not None:
            if "Emission Color" in inputs:
                inputs["Emission Color"].default_value = emission
            if "Emission Strength" in inputs:
                inputs["Emission Strength"].default_value = strength
    return mat


def _assign(obj, mat) -> None:
    if obj and getattr(obj, "data", None) and hasattr(obj.data, "materials"):
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)


def _cube_obj(name: str, loc, scale, mat=None, bevel: float = 0.0):
    bpy = _get_bpy()
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        _assign(obj, mat)
    if bevel > 0:
        mod = obj.modifiers.new(f"{name}_bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        obj.modifiers.new(f"{name}_weighted_normals", "WEIGHTED_NORMAL")
    return obj


def _look_at(obj, target) -> None:
    from mathutils import Vector
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def _png_image_metrics(path: str) -> dict:
    try:
        from PIL import Image, ImageFilter, ImageStat
        import numpy as np
        im = Image.open(path).convert("RGB")
        arr = np.asarray(im, dtype="float32")
        luma = arr[:, :, 0] * 0.2126 + arr[:, :, 1] * 0.7152 + arr[:, :, 2] * 0.0722
        gray = Image.fromarray(np.clip(luma, 0, 255).astype("uint8"), mode="L")
        if gray.width > 512:
            h = max(1, int(gray.height * 512 / gray.width))
            gray = gray.resize((512, h))
        edge_mean = ImageStat.Stat(gray.filter(ImageFilter.FIND_EDGES)).mean[0]
        hist = gray.histogram()
        total = max(sum(hist), 1)
        return {
            "mean_luma": round(float(luma.mean()), 1),
            "luma_std": round(float(luma.std()), 1),
            "edge_mean": round(float(edge_mean), 2),
            "highlight_pct": round(float((luma > 245).mean() * 100.0), 2),
            "shadow_pct": round(float((luma < 12).mean() * 100.0), 2),
            "near_black_pct": round(float(sum(hist[:18]) / total * 100.0), 2),
        }
    except Exception:
        return {}


def _render_quality_error(metrics: dict) -> str | None:
    if not metrics:
        return None
    mean = float(metrics.get("mean_luma") or 0.0)
    std = float(metrics.get("luma_std") or 0.0)
    edge = float(metrics.get("edge_mean") or 0.0)
    near_black = float(metrics.get("near_black_pct") or 0.0)
    highlight = float(metrics.get("highlight_pct") or 0.0)
    if mean < 18.0:
        return f"underexposed final PNG: mean_luma={mean:.1f}"
    if near_black > 96.0 and mean < 32.0:
        return f"mostly black final PNG: near_black_pct={near_black:.1f}"
    if highlight > 99.0:
        return f"washed-out final PNG: highlight_pct={highlight:.1f}"
    if std < 2.0 and edge < 1.0:
        return f"near-blank final PNG: luma_std={std:.1f}, edge_mean={edge:.1f}"
    return None


def _boost_render_visibility(bpy, metrics: dict) -> dict:
    """One conservative recovery pass for renders that are visibly too dark."""
    mean = float(metrics.get("mean_luma") or 0.0)
    if mean >= 24.0:
        return {}

    scene = bpy.context.scene
    changed: dict = {}
    try:
        current = float(getattr(scene.view_settings, "exposure", 0.0) or 0.0)
        boost = 1.25 if mean < 18.0 else 0.65
        scene.view_settings.exposure = min(current + boost, 1.6)
        changed["exposure"] = round(float(scene.view_settings.exposure), 2)
    except Exception:
        pass

    world = scene.world
    if world and getattr(world, "use_nodes", False):
        bg = world.node_tree.nodes.get("Background")
        if bg and "Strength" in bg.inputs:
            strength = float(bg.inputs["Strength"].default_value)
            if strength < 0.45:
                bg.inputs["Strength"].default_value = 0.45
                changed["world_strength"] = 0.45

    lights = [obj for obj in bpy.data.objects if obj.type == "LIGHT" and obj.data]
    if lights:
        total = sum(float(getattr(obj.data, "energy", 0.0) or 0.0) for obj in lights)
        scale = 3.0 if total < 1800 else 1.6
        for obj in lights:
            obj.data.energy = float(obj.data.energy) * scale
        changed["light_energy_scale"] = scale
    else:
        try:
            bpy.ops.object.light_add(type="AREA", location=(0.0, -4.0, 5.0))
            fill = bpy.context.active_object
            fill.name = "VWS_RenderRecoveryFill"
            fill.data.energy = 550.0
            fill.data.size = 5.0
            changed["added_fill_light"] = fill.name
        except Exception:
            pass
    return changed


def _visible_mesh_objects(bpy):
    return [
        obj for obj in bpy.data.objects
        if obj.type == "MESH"
        and not getattr(obj, "hide_render", False)
        and getattr(obj, "data", None) is not None
    ]


def _world_bbox(obj):
    from mathutils import Vector
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    xs = [c.x for c in corners]
    ys = [c.y for c in corners]
    zs = [c.z for c in corners]
    return Vector((min(xs), min(ys), min(zs))), Vector((max(xs), max(ys), max(zs)))


def _bbox_for_objects(objects):
    from mathutils import Vector
    mins = []
    maxs = []
    for obj in objects:
        try:
            mn, mx = _world_bbox(obj)
        except Exception:
            continue
        mins.append(mn)
        maxs.append(mx)
    if not mins:
        return None
    return (
        Vector((min(v.x for v in mins), min(v.y for v in mins), min(v.z for v in mins))),
        Vector((max(v.x for v in maxs), max(v.y for v in maxs), max(v.z for v in maxs))),
    )


def _select_framing_meshes(bpy):
    """Choose subject meshes for camera framing without task-specific names."""
    meshes = _visible_mesh_objects(bpy)
    if len(meshes) <= 2:
        return meshes

    env_keywords = (
        "floor", "ground", "wall", "backdrop", "background", "horizon",
        "plane", "tabletop", "table_top", "stage", "base", "pedestal",
        "foreground", "ceiling",
    )
    candidates = []
    for obj in meshes:
        name = obj.name.lower()
        if any(k in name for k in env_keywords):
            continue
        try:
            mn, mx = _world_bbox(obj)
            ext = mx - mn
        except Exception:
            continue
        max_dim = max(ext.x, ext.y, ext.z)
        min_dim = max(min(ext.x, ext.y, ext.z), 1e-6)
        # Large paper-thin planes are usually floors/backdrops even when
        # named generically; don't let them push the hero subject off-center.
        if max_dim > 2.0 and min_dim / max_dim < 0.04:
            continue
        candidates.append(obj)
    return candidates if len(candidates) >= 2 else meshes


def _normalize_render_tone(bpy) -> dict:
    scene = bpy.context.scene
    changed = {}
    try:
        scene.view_settings.view_transform = "Filmic"
        scene.view_settings.look = "Medium High Contrast"
        exposure = float(getattr(scene.view_settings, "exposure", 0.0) or 0.0)
        if exposure > 0.35:
            scene.view_settings.exposure = 0.0
            changed["exposure"] = "clamped_to_0.0"
        elif exposure < -1.75:
            scene.view_settings.exposure = -1.0
            changed["exposure"] = "raised_to_-1.0"
        try:
            scene.view_settings.gamma = 1.0
        except Exception:
            pass
    except Exception:
        pass

    world = scene.world
    if world and getattr(world, "use_nodes", False):
        bg = world.node_tree.nodes.get("Background")
        if bg and "Strength" in bg.inputs:
            strength = float(bg.inputs["Strength"].default_value)
            if strength > 1.25:
                bg.inputs["Strength"].default_value = 0.85
                changed["world_strength"] = "clamped_to_0.85"

    lights = [obj for obj in bpy.data.objects if obj.type == "LIGHT" and obj.data]
    total_energy = sum(float(getattr(obj.data, "energy", 0.0) or 0.0) for obj in lights)
    if total_energy > 8000:
        scale = 8000.0 / total_energy
        for obj in lights:
            obj.data.energy = float(obj.data.energy) * scale
        changed["light_energy_scale"] = round(scale, 3)
    return changed


def _fit_camera_to_scene(bpy) -> dict:
    """Frame the main mesh cluster with margin before preview/final render."""
    from mathutils import Vector
    import math

    subjects = _select_framing_meshes(bpy)
    bbox = _bbox_for_objects(subjects)
    if bbox is None:
        return {"camera_fit": "skipped_no_meshes"}
    mn, mx = bbox
    center = (mn + mx) * 0.5
    ext = mx - mn
    if max(ext.x, ext.y, ext.z) <= 0:
        return {"camera_fit": "skipped_degenerate_bbox"}

    scene = bpy.context.scene
    cam = scene.camera
    if cam is None:
        cam_data = bpy.data.cameras.new("Camera")
        cam = bpy.data.objects.new("Camera", cam_data)
        bpy.context.collection.objects.link(cam)
        scene.camera = cam

    try:
        lens = float(getattr(cam.data, "lens", 45.0) or 45.0)
        cam.data.lens = min(max(lens, 35.0), 58.0)
        # Final benchmark renders must be inspectable. Agent-authored shallow
        # depth of field has repeatedly hidden the actual scene geometry.
        cam.data.dof.use_dof = False
        cam.data.dof.aperture_fstop = max(float(getattr(cam.data.dof, "aperture_fstop", 8.0) or 8.0), 8.0)
    except Exception:
        pass

    target = Vector((center.x, center.y, center.z + max(ext.z * 0.08, 0.03)))
    if cam.location.length > 0:
        view_dir = target - cam.location
    else:
        view_dir = Vector((-2.4, 3.2, -1.4))
    if view_dir.length < 0.01:
        view_dir = Vector((-2.4, 3.2, -1.4))
    view_dir.normalize()
    # Keep a three-quarter product angle. If the existing camera is too flat
    # or below the subject, lift it instead of preserving a broken macro view.
    if view_dir.z > -0.18:
        view_dir.z = -0.32
        view_dir.normalize()

    aspect = max(float(scene.render.resolution_x or 1920) / float(scene.render.resolution_y or 1080), 0.1)
    try:
        fov_y = float(cam.data.angle_y)
        fov_x = float(cam.data.angle_x)
    except Exception:
        fov_y = math.radians(31.0)
        fov_x = 2.0 * math.atan(math.tan(fov_y / 2.0) * aspect)
    width_need = max(ext.x, ext.y * 0.55, 0.35)
    height_need = max(ext.z * 1.35, ext.y * 0.35, 0.35)
    distance_x = (width_need * 0.5) / max(math.tan(fov_x * 0.5), 0.1)
    distance_y = (height_need * 0.5) / max(math.tan(fov_y * 0.5), 0.1)
    diag = max(ext.length, 0.5)
    distance = max(distance_x, distance_y, diag * 1.65, 1.35) * 1.28
    cam.location = target - view_dir * distance
    _look_at(cam, target)
    return {
        "camera_fit": "ok",
        "framed_meshes": len(subjects),
        "target": [round(target.x, 3), round(target.y, 3), round(target.z, 3)],
        "distance": round(distance, 3),
        "lens": round(float(getattr(cam.data, "lens", 0.0) or 0.0), 1),
    }


def _apply_cyberpunk_polish_pack() -> dict:
    """Deterministic environment detail pass for corridor-style scenes."""
    bpy = _get_bpy()
    import math

    # Idempotent: repeated QA loops should replace the pack, not duplicate
    # hundreds of panels/lights and slow the render into failure.
    for obj in list(bpy.data.objects):
        if obj.name.startswith("VWS_"):
            bpy.data.objects.remove(obj, do_unlink=True)
    for obj in list(bpy.data.objects):
        nm = obj.name.lower()
        if any(k in nm for k in ("fog", "mist", "steam", "volume", "haze")):
            bpy.data.objects.remove(obj, do_unlink=True)

    dark_metal = _mat("VWS_DarkBrushedMetal", base=(0.055, 0.065, 0.09, 1), rough=0.42, metal=0.75)
    wall_panel = _mat("VWS_GunmetalWallPanel", base=(0.075, 0.08, 0.105, 1), rough=0.62, metal=0.35)
    wet_floor = _mat("VWS_WetReflectiveFloor", base=(0.025, 0.033, 0.045, 1), rough=0.06, metal=0.26)
    rubber = _mat("VWS_BlackCableRubber", base=(0.012, 0.012, 0.018, 1), rough=0.7, metal=0.0)
    magenta = _mat("VWS_NeonMagenta", base=(0.03, 0.0, 0.025, 1), emission=(1.0, 0.18, 0.72, 1), strength=8.0)
    cyan = _mat("VWS_NeonCyan", base=(0.0, 0.025, 0.03, 1), emission=(0.18, 0.92, 1.0, 1), strength=8.5)
    amber = _mat("VWS_NeonAmber", base=(0.03, 0.018, 0.0, 1), emission=(1.0, 0.68, 0.18, 1), strength=5.0)
    holo = _mat("VWS_HologramGlass", base=(0.48, 0.95, 1.0, 0.36), rough=0.08, metal=0.0, emission=(0.24, 0.9, 1.0, 1), strength=2.2, alpha=0.42)
    steam = _mat("VWS_SoftSteamCards", base=(0.75, 0.88, 1.0, 0.14), rough=1.0, emission=(0.5, 0.8, 1.0, 1), strength=0.12, alpha=0.18)

    # Neutralize bright shell placeholders without deleting user work. The
    # cyberpunk corridor shell can leave large white walls/ceiling and white
    # area lights; those make the final render read as blockout.
    for obj in bpy.data.objects:
        if obj.name.startswith("VWS_"):
            continue
        if obj.type == "MESH" and obj.name.startswith("Cube") and obj.active_material is None:
            _assign(obj, wall_panel)
        if obj.type == "MESH" and max(obj.dimensions) > 1.2:
            nm = obj.name.lower()
            is_neon_like = any(k in nm for k in ("neon", "holo", "light", "sign", "strip"))
            if is_neon_like:
                continue
            if "floor" in nm or obj.location.z < 0.22:
                _assign(obj, wet_floor)
            elif "ceiling" in nm or "wall" in nm or obj.location.z > 2.35:
                _assign(obj, wall_panel)
            elif nm.startswith("cube") or "panel" in nm or min(obj.dimensions) < 0.22:
                _assign(obj, dark_metal)
            if not any(m.type == "BEVEL" for m in obj.modifiers):
                mod = obj.modifiers.new("VWS_existing_edge_bevel", "BEVEL")
                mod.width = 0.018
                mod.segments = 2
                obj.modifiers.new("VWS_existing_weighted_normals", "WEIGHTED_NORMAL")
        if obj.type == "LIGHT":
            try:
                obj.data.energy *= 0.38
                obj.data.color = (0.68, 0.88, 1.0)
            except Exception:
                pass

    created: list[str] = []
    # Wet floor panel grid and center light path.
    for i, y in enumerate([v * 1.55 for v in range(0, 13)]):
        for x, mat in [(-1.35, wet_floor), (1.35, wet_floor)]:
            obj = _cube_obj(f"VWS_WetFloorPanel_{i}_{'L' if x < 0 else 'R'}", (x, y, 0.035), (1.18, 0.62, 0.018), mat, bevel=0.025)
            created.append(obj.name)
        if i % 2 == 0:
            obj = _cube_obj(f"VWS_CenterNeonInlay_{i}", (0, y, 0.07), (0.055, 0.48, 0.014), magenta if i % 4 == 0 else cyan, bevel=0.012)
            created.append(obj.name)

    # Repeating wall panels, trims, and emissive slits.
    for side, x in [("L", -2.35), ("R", 2.35)]:
        for i, y in enumerate([1.1 + v * 2.05 for v in range(9)]):
            panel = _cube_obj(f"VWS_WallServicePanel_{side}_{i}", (x, y, 1.45), (0.055, 0.72, 0.72), wall_panel, bevel=0.035)
            created.append(panel.name)
            strip = _cube_obj(f"VWS_WallNeonSlit_{side}_{i}", (x * 0.995, y, 2.55), (0.035, 0.42, 0.035), cyan if side == "L" else magenta, bevel=0.01)
            created.append(strip.name)
            rail = _cube_obj(f"VWS_ServiceRail_{side}_{i}", (x * 0.99, y, 0.98), (0.035, 0.86, 0.035), dark_metal, bevel=0.012)
            created.append(rail.name)

    # Pipe bundles as cylinders running down the corridor.
    for side, x in [("L", -2.05), ("R", 2.05)]:
        for z in (2.65, 3.02, 0.82):
            bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.045, depth=17.5, location=(x, 8.2, z), rotation=(math.radians(90), 0, 0))
            pipe = bpy.context.active_object
            pipe.name = f"VWS_ExposedPipe_{side}_{z:.1f}"
            _assign(pipe, dark_metal if z > 1 else rubber)
            pipe.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
            created.append(pipe.name)

    # Foreground set dressing: crates, cable loops, floor grates, and hazard
    # ticks prevent the hero shot from feeling empty near the camera.
    crate_specs = [
        (-1.58, 1.15, 0.34, 0.34, 0.46, 0.34),
        (1.48, 2.25, 0.26, 0.42, 0.34, 0.26),
        (-1.72, 3.15, 0.22, 0.28, 0.26, 0.22),
        (1.63, 5.1, 0.31, 0.34, 0.42, 0.31),
    ]
    for i, (x, y, z, sx, sy, sz) in enumerate(crate_specs):
        crate = _cube_obj(f"VWS_ForegroundTechCrate_{i}", (x, y, z), (sx, sy, sz), dark_metal, bevel=0.035)
        created.append(crate.name)
        for dz, mat in [(sz + 0.018, cyan if i % 2 else magenta), (-sz - 0.018, amber)]:
            tick = _cube_obj(f"VWS_CrateNeonTick_{i}_{dz:.2f}", (x, y - sy * 0.55, z + dz), (sx * 0.72, 0.018, 0.014), mat, bevel=0.006)
            created.append(tick.name)
    for i, (x, y, z, rot) in enumerate([(-1.05, 1.9, 0.08, 18), (1.08, 3.75, 0.08, -22), (-0.78, 6.0, 0.08, 32)]):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.012, major_segments=36, minor_segments=8, location=(x, y, z))
        cable = bpy.context.active_object
        cable.name = f"VWS_CableCoil_{i}"
        cable.rotation_euler[2] = math.radians(rot)
        _assign(cable, rubber)
        created.append(cable.name)
    for i, y in enumerate([1.05, 2.15, 3.25, 4.35, 5.45, 6.55]):
        grate = _cube_obj(f"VWS_ForegroundFloorGrate_{i}", (0, y, 0.095), (0.72, 0.028, 0.012), dark_metal, bevel=0.006)
        created.append(grate.name)

    # Holographic signs / translucent UI cards.
    for i, (x, y, z, mat, label) in enumerate([
        (-1.65, 4.0, 1.92, holo, "ROUTE_7"),
        (1.72, 6.8, 2.12, holo, "ACCESS"),
        (-1.35, 10.6, 2.28, holo, "NOVA"),
        (1.35, 12.9, 1.76, holo, "SYNC"),
    ]):
        sign = _cube_obj(f"VWS_HoloSign_{label}", (x, y, z), (0.032, 0.74, 0.36), mat, bevel=0.018)
        created.append(sign.name)
        # Add a smaller emissive caption strip so it reads as signage.
        cap = _cube_obj(f"VWS_HoloCaption_{label}", (x, y - 0.36, z - 0.28), (0.035, 0.22, 0.025), cyan if i % 2 else magenta, bevel=0.008)
        created.append(cap.name)

    # A readable midground hero target, built from curves/torus/sphere rather than cubes.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=16, radius=0.34, location=(0, 9.2, 1.45))
    core = bpy.context.active_object
    core.name = "VWS_HeroHologramCore"
    _assign(core, holo)
    created.append(core.name)
    for idx, rot in enumerate((0, 60, 120)):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.62, minor_radius=0.012, major_segments=80, minor_segments=8, location=(0, 9.2, 1.45))
        ring = bpy.context.active_object
        ring.name = f"VWS_HeroOrbitRing_{idx}"
        ring.rotation_euler[1] = math.radians(rot)
        _assign(ring, magenta if idx != 1 else cyan)
        created.append(ring.name)

    # Steam as thin translucent cards facing the camera.
    for i, (x, y, z, sx, sz) in enumerate([
        (-0.75, 2.7, 0.72, 0.62, 1.05),
        (0.9, 4.6, 0.86, 0.5, 1.14),
        (-0.9, 7.2, 0.98, 0.66, 1.2),
        (0.95, 10.6, 1.06, 0.6, 1.05),
        (-1.1, 13.2, 0.95, 0.72, 0.98),
    ]):
        obj = _cube_obj(f"VWS_DriftingSteamCard_{i}", (x, y, z), (0.012, sx, sz), steam, bevel=0.04)
        obj.rotation_euler[2] = math.radians(6 if i % 2 else -8)
        created.append(obj.name)

    # Add practical area lights that read in the final render.
    for name, loc, color, energy in [
        ("VWS_CyanNearRim", (2.3, -0.4, 2.1), (0.18, 0.9, 1.0), 260),
        ("VWS_MagentaNearRim", (-2.3, -0.8, 2.0), (1.0, 0.2, 0.75), 260),
        ("VWS_HeroBackGlow", (0.0, 8.5, 2.5), (0.35, 0.9, 1.0), 380),
    ]:
        light_data = bpy.data.lights.new(name, type="AREA")
        light_data.energy = energy
        light_data.size = 1.2
        light_data.color = color
        light = bpy.data.objects.new(name, light_data)
        bpy.context.collection.objects.link(light)
        light.location = loc
        _look_at(light, (0, 8.5, 1.2))
        created.append(light.name)

    # Camera: lower/closer, focal target on hero core, less empty foreground.
    cam = bpy.context.scene.camera
    if cam is None:
        cam_data = bpy.data.cameras.new("Camera")
        cam = bpy.data.objects.new("Camera", cam_data)
        bpy.context.collection.objects.link(cam)
        bpy.context.scene.camera = cam
    cam.location = (0.55, -1.25, 1.05)
    cam.data.lens = 24
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = bpy.data.objects.get("VWS_HeroHologramCore")
    cam.data.dof.aperture_fstop = 5.6
    _look_at(cam, (0, 9.2, 1.45))

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    try:
        scene.eevee.taa_render_samples = 128
        if hasattr(scene.eevee, "use_ssr"):
            scene.eevee.use_ssr = True
        if hasattr(scene.eevee, "use_ssr_refraction"):
            scene.eevee.use_ssr_refraction = True
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = True
            scene.eevee.bloom_intensity = 0.28
            scene.eevee.bloom_radius = 5.5
    except Exception:
        pass
    if scene.world:
        scene.world.use_nodes = True
        bg = scene.world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs[0].default_value = (0.015, 0.018, 0.03, 1.0)
            bg.inputs[1].default_value = 0.08

    return {
        "scene_type": "cyberpunk_corridor",
        "objects_added": len(created),
        "created_sample": created[:16],
        "total_objects": len(bpy.data.objects),
    }


@mcp.tool()
def apply_scene_polish_pack(scene_type: str = "auto") -> str:
    """Apply a generic scene-quality pass before final render.

    Main experiments must not get brief-specific hidden assets from this
    helper. By default this only does generic anti-blockout work: soften mesh
    edges, assign non-default materials to blank meshes, add missing area
    lights, and keep camera/render settings sane. Scene-specific asset packs
    are disabled unless BLENDER_ENABLE_SCENE_SPECIFIC_POLISH=1 is explicitly
    set for a separate ablation.
    """
    try:
        bpy = _get_bpy()
        kind = (scene_type or "auto").lower().strip()
        scene_specific_enabled = os.environ.get(
            "BLENDER_ENABLE_SCENE_SPECIFIC_POLISH", "0"
        ).strip().lower() in {"1", "true", "yes"}
        if (
            scene_specific_enabled
            and kind in {"cyberpunk", "cyberpunk_corridor", "corridor", "neon_corridor"}
        ):
            result = _apply_cyberpunk_polish_pack()
        else:
            # Generic polish: bevel obvious blockout meshes, add lights, and
            # make materials non-default without imposing a themed asset pack.
            mat = _mat("VWS_GenericPolishedMaterial", base=(0.18, 0.2, 0.24, 1), rough=0.45, metal=0.15)
            changed = []
            for obj in bpy.data.objects:
                if obj.type == "MESH":
                    if obj.active_material is None:
                        _assign(obj, mat)
                    if not any(m.type == "BEVEL" for m in obj.modifiers):
                        mod = obj.modifiers.new("VWS_soft_bevel", "BEVEL")
                        mod.width = 0.025
                        mod.segments = 2
                        obj.modifiers.new("VWS_weighted_normals", "WEIGHTED_NORMAL")
                    changed.append(obj.name)
            if len([o for o in bpy.data.objects if o.type == "LIGHT"]) < 3:
                for i, loc in enumerate([(-3, -4, 4), (3, -2, 3), (0, 3, 5)]):
                    ld = bpy.data.lights.new(f"VWS_GenericArea_{i}", "AREA")
                    ld.energy = 120
                    ld.size = 3.0
                    lo = bpy.data.objects.new(ld.name, ld)
                    bpy.context.collection.objects.link(lo)
                    lo.location = loc
                    _look_at(lo, (0, 0, 1))
            tone_changes = _normalize_render_tone(bpy)
            camera_fit = _fit_camera_to_scene(bpy)
            result = {
                "scene_type": "generic",
                "requested_scene_type": kind,
                "scene_specific_enabled": scene_specific_enabled,
                "meshes_polished": len(changed),
                "tone_changes": tone_changes,
                "camera_fit": camera_fit,
                "total_objects": len(bpy.data.objects),
            }
        return json.dumps({"ok": True, **result}, indent=2)
    except Exception as e:
        return f"Error: apply_scene_polish_pack failed: {e}\n{traceback.format_exc()[:900]}"


@mcp.tool()
def list_scene_shells() -> str:
    """List scene shells (full pre-baked themed scenes). USE ONLY when the
    brief is a clear match — a wrong-fit shell installs a fixed camera +
    lighting + render settings that fight your custom geometry and ruin
    the final render. Fit table:

      cyberpunk_corridor   — sci-fi hallway with neon strips, crates,
                              pipes. Fits: corridor / tunnel / metro / hallway.
      forest_landscape     — stylized low-poly forest, golden hour, trees.
                              Fits: forest / outdoor nature / woods.
      product_hero_shot    — studio infinity backdrop + 3-point lighting,
                              ONE central object on plain ground. Fits ONLY:
                              clean product on backdrop (sphere, cube, torus
                              hero). DO NOT use for: portraits, jewelry,
                              vehicles, abstract sculpture, busts.
      interior_living_room — modern living room with sofa/table/rug/lamp +
                              warm daylight. Fits: living room / loft /
                              architectural interior.
      sci_fi_exterior      — hexagonal landing pad with arches, dramatic
                              rim lights. Fits ONLY: hex landing pad +
                              arches scenes. DO NOT use for: moon outposts,
                              alien terrain, supercars, cityscapes — the
                              hex pad geometry intrudes on the frame.

    If the brief doesn't map cleanly to one of these five, SKIP shells
    entirely and start from `execute_blender_code`. Then layer
    `apply_lighting_rig` + `apply_material_preset` for polish."""
    if not _skills_dir:
        return json.dumps({"kind": "scene_shells", "names": []})
    base = _skills_dir / "scene_shells_seed"
    if not base.exists():
        return json.dumps({"kind": "scene_shells", "names": []})
    names = sorted(p.stem for p in base.glob("*.py") if not p.stem.startswith("_"))
    return json.dumps({"kind": "scene_shells", "names": names}, indent=2)


@mcp.tool()
def build_scene_from_shell(shell_id: str, kwargs_json: str = "{}") -> str:
    """Build a complete scene from a shell. Resets the current scene, then calls the shell's
    build(**kwargs) function which adds geometry + materials + lighting + camera in one go.

    After this, you can iterate with execute_blender_code, apply_material_preset, etc.

    Args:
        shell_id: file stem under skills_library/blender/scene_shells_seed/
        kwargs_json: JSON dict passed to the shell's build() function
    """
    try:
        kwargs = json.loads(kwargs_json) if kwargs_json else {}
    except json.JSONDecodeError as e:
        return f"Error: kwargs_json invalid: {e}"
    if not _skills_dir:
        return "Error: --skills-dir not configured"
    py = _skills_dir / "scene_shells_seed" / f"{shell_id}.py"
    if not py.exists():
        return f"Error: shell {shell_id!r} not found at {py}"
    try:
        import importlib.util as _ilu
        spec = _ilu.spec_from_file_location(f"_shell_{shell_id}", py)
        mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, "build"):
            return f"Error: shell {shell_id!r} missing build() function"
        result = mod.build(**kwargs)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: build_scene_from_shell failed: {e}\n{traceback.format_exc()[:800]}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Unified Blender MCP Server")
    parser.add_argument("--skills-dir", default=None)
    parser.add_argument("--demo-dir", default=None,
                        help="Path to saved Blender artifacts (default: <project>/demo/blender).")
    args = parser.parse_args()

    global _skills_dir, _demo_dir
    if args.skills_dir:
        _skills_dir = Path(args.skills_dir).resolve()
    if args.demo_dir:
        _demo_dir = Path(args.demo_dir).resolve()
    _demo_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=logging.INFO)
    log.info("Blender MCP starting (skills_dir=%s, demo_dir=%s)", _skills_dir, _demo_dir)

    # Pre-load bpy to catch import errors early
    _get_bpy()
    log.info("bpy ready — unified server (skill library + bpy execution)")

    # Hybrid wiki discovery surface — wiki contract + thin legacy bridge.
    try:
        from domains.blender.wiki_adapter import BlenderWikiAdapter
        from core.skill_wiki.mcp_tools import register_wiki_tools
        register_wiki_tools(mcp, BlenderWikiAdapter())
        log.info("Blender MCP: registered universal wiki discovery surface")
    except Exception as exc:  # noqa: BLE001
        log.warning("Blender MCP: failed to register wiki discovery surface: %s", exc)
    try:
        from core import get_active_library_backend
        from core.skill_wiki.legacy_stale import register_legacy_stale_check
        backend = get_active_library_backend("blender")
        register_legacy_stale_check(mcp, domain="blender", startup_backend=backend)
    except Exception as exc:  # noqa: BLE001
        log.warning("Blender MCP: failed to install stale-registry guard: %s", exc)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
