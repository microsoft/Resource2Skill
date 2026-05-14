"""
core/harness.py
Self-evolution harness: score → evaluate → evolve → collect.

Six stages:
  1. score-skills     — execute + render each skill → GPT-5.4 vision scores
  2. score-demos      — render each demo page → GPT-5.4 vision scores
  3. evolve           — gap analysis → update queries, prune skills, improve architecture
  4. evolve-distiller — analyze skill failure patterns → fix distiller prompt (conservative)
  5. evolve-agent     — analyze high-scoring demos → extract best skill composition patterns
  6. auto-collect     — identify missing skills → run targeted YouTube collection

See docs/self_evolution_harness.md for the full loop design.
"""
from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import re
import tempfile
import shutil
from pathlib import Path
from typing import Any

log = logging.getLogger("harness")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════

def _render_html_to_png(html_path: Path, width: int = 1280, height: int = 900) -> bytes | None:
    """Render an HTML file to PNG using Playwright."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log.warning("Playwright not installed, skipping render")
        return None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"file://{html_path.resolve()}", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(500)
            png_bytes = page.screenshot(full_page=True)
            browser.close()
            return png_bytes
    except Exception as e:
        log.warning("Render failed for %s: %s", html_path, e)
        return None


def _render_audio_to_png(wav_path: Path) -> bytes | None:
    """Render an audio file spectrogram + waveform to PNG for vision scoring."""
    try:
        import numpy as np
        import soundfile as sf
        import librosa
        import librosa.display
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as e:
        log.warning("Audio visualization libs not available: %s", e)
        return None

    try:
        data, sr = sf.read(str(wav_path))
        mono = data.mean(axis=1) if data.ndim > 1 else data

        fig, axes = plt.subplots(2, 1, figsize=(12, 7))

        # Mel spectrogram
        S = librosa.feature.melspectrogram(y=mono, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
        librosa.display.specshow(S_dB, x_axis="time", y_axis="mel", sr=sr, fmax=8000, ax=axes[0])
        axes[0].set_title("Mel Spectrogram")
        axes[0].set_xlabel("")

        # Onset strength
        onset_env = librosa.onset.onset_strength(y=mono, sr=sr)
        times_onset = librosa.times_like(onset_env, sr=sr)
        axes[1].plot(times_onset, onset_env, color="#E91E63", linewidth=0.8)
        axes[1].set_title("Rhythm / Onset Strength")
        axes[1].set_xlabel("Time (s)")
        axes[1].set_xlim(0, len(mono) / sr)

        plt.tight_layout()
        import io
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
        plt.close(fig)
        return buf.getvalue()
    except Exception as e:
        log.warning("Audio spectrogram render failed for %s: %s", wav_path, e)
        return None


def _vision_score(png_bytes: bytes, prompt: str, *, model: str = "gpt-5.4",
                  reasoning_effort: str = "low", system_role: str = "web design") -> dict:
    """Send a screenshot/spectrogram to GPT-5.4 vision and parse JSON scores."""
    from core.llm import call_azure_openai
    b64 = base64.b64encode(png_bytes).decode()
    messages = [
        {"role": "system", "content": f"You are a {system_role} expert evaluator. Return ONLY valid JSON."},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "low"}},
        ]},
    ]
    msg = call_azure_openai(messages, model=model, reasoning_effort=reasoning_effort,
                            max_completion_tokens=1024)
    content = msg.get("content", "")
    match = re.search(r"\{[\s\S]*\}", content)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    log.warning("Failed to parse vision score JSON: %s", content[:200])
    return {}


def _llm_json(prompt: str, *, system: str = "", model: str = "gpt-5.4",
              reasoning_effort: str = "medium") -> dict:
    """Call GPT-5.4 with a text prompt, expect JSON back."""
    from core.llm import call_azure_openai
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    msg = call_azure_openai(messages, model=model, reasoning_effort=reasoning_effort,
                            max_completion_tokens=4096)
    content = msg.get("content", "")
    match = re.search(r"\{[\s\S]*\}", content)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return {"raw": content[:2000]}


def _load_domain_state(domain: str) -> dict:
    """Load all domain state into a single dict for analysis."""
    from core import load_domain, get_library_dir
    domain_cfg = load_domain(domain)
    lib_dir = get_library_dir(domain)
    demo_dir = _PROJECT_ROOT / "demo" / domain
    domain_dir = _PROJECT_ROOT / "domains" / domain

    index_path = lib_dir / "index.json"
    index_raw = json.loads(index_path.read_text()) if index_path.exists() else []
    # Normalize: index can be a list or {"skills": [...]}
    if isinstance(index_raw, dict):
        index = index_raw
    else:
        index = {"skills": index_raw}

    metadata_path = lib_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}

    demo_scores_path = demo_dir / "harness_scores.json"
    demo_scores = json.loads(demo_scores_path.read_text()) if demo_scores_path.exists() else {}

    # Build category stats
    cat_stats = {}
    for s in index.get("skills", []):
        cat = s.get("category", "unknown")
        sid = s["skill_id"]
        meta = metadata.get(sid, {})
        if cat not in cat_stats:
            cat_stats[cat] = {"count": 0, "exec_ok": 0, "visual_scores": [], "failed_errors": []}
        cat_stats[cat]["count"] += 1
        if meta.get("exec_ok"):
            cat_stats[cat]["exec_ok"] += 1
        vq = meta.get("visual_quality")
        if isinstance(vq, (int, float)):
            cat_stats[cat]["visual_scores"].append(vq)
        err = meta.get("error")
        if err:
            cat_stats[cat]["failed_errors"].append(err[:80])

    # Compute averages
    for st in cat_stats.values():
        scores = st.pop("visual_scores")
        st["avg_visual"] = round(sum(scores) / len(scores), 1) if scores else 0
        # Keep only top-5 unique errors
        errs = st.pop("failed_errors")
        st["top_errors"] = list(set(errs))[:5]

    return {
        "domain_cfg": domain_cfg,
        "domain_dir": domain_dir,
        "lib_dir": lib_dir,
        "demo_dir": demo_dir,
        "index": index,
        "metadata": metadata,
        "metadata_path": metadata_path,
        "demo_scores": demo_scores,
        "cat_stats": cat_stats,
        "categories": list(domain_cfg.get("categories", {}).keys()),
        "query_pool": domain_cfg.get("query_pool", []),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Stage 1: Score Skills
# ═══════════════════════════════════════════════════════════════════════════

SKILL_SCORE_PROMPT = """Rate this web component screenshot on these dimensions (1-5 each):

1. **visual_quality**: Does it look polished, modern, and professional?
2. **composability**: Could this component be dropped into a larger page and look good?
3. **creativity**: Is the technique interesting or novel?

Return JSON: {"visual_quality": N, "composability": N, "creativity": N, "notes": "one-line summary"}"""

SKILL_SCORE_PROMPT_AUDIO = """Rate this music production skill's spectrogram on these dimensions (1-5 each):

1. **musical_quality**: Does the frequency content look rich and well-balanced? Good harmonic structure visible in the mel spectrogram?
2. **composability**: Could this pattern be layered with other elements (drums + bass + melody) in a mix?
3. **rhythmic_interest**: Does the onset/rhythm graph show clear, defined rhythmic patterns with dynamic variation?

Return JSON: {"visual_quality": N, "composability": N, "creativity": N, "notes": "one-line summary"}"""


SKILL_SCORE_PROMPT_BLENDER = """Rate this Blender 3D render on these dimensions (1-5 each):

1. **visual_quality**: Does the geometry look clean? Materials realistic/stylized? Lighting well-composed?
2. **composability**: Could this object/effect be placed into a larger scene and integrate well?
3. **creativity**: Is the technique interesting — procedural, shader-driven, or geometrically novel?

Return JSON: {"visual_quality": N, "composability": N, "creativity": N, "notes": "one-line summary"}"""

SKILL_SCORE_PROMPT_CAD = """Rate this CAD drawing screenshot on these dimensions (1-5 each):

1. **visual_quality**: Is the drawing crisp, legible, and framed properly?
2. **composability**: Could this drawing pattern be reused as a building block in a larger technical drawing?
3. **creativity**: Does it show a useful drafting pattern beyond a trivial primitive?

Return JSON: {"visual_quality": N, "composability": N, "creativity": N, "notes": "one-line summary"}"""

DEMO_SCORE_PROMPT_AUDIO = """Rate this music production beat's spectrogram (1-5 each):

1. **mix_quality**: Balanced frequency spectrum? Clear separation between bass, mids, highs?
2. **rhythm**: Strong, well-defined drum patterns with dynamic variation?
3. **harmonic_richness**: Rich chord content, interesting melodic elements in the mid-high frequencies?
4. **arrangement**: Energy changes over time? Sections feel different? Dynamic contrast?
5. **production_polish**: Warm, full sound? No harsh frequencies or dead zones?

Return JSON: {"design": N, "animation_richness": N, "skill_utilization": N, "responsiveness": N, "cohesion": N, "overall": N, "strengths": "...", "weaknesses": "..."}
Map: design=mix_quality, animation_richness=rhythm, skill_utilization=harmonic_richness, responsiveness=arrangement, cohesion=production_polish.
"overall" = average of 5 scores, rounded to 1 decimal."""

_AUDIO_DOMAINS = {"reaper", "ableton", "music"}
_BLENDER_DOMAINS = {"blender"}
_CAD_DOMAINS = {"cad"}


def _is_audio_domain(domain: str) -> bool:
    return domain in _AUDIO_DOMAINS


def _is_blender_domain(domain: str) -> bool:
    return domain in _BLENDER_DOMAINS


def _is_cad_domain(domain: str) -> bool:
    return domain in _CAD_DOMAINS


def _domain_type(domain: str) -> str:
    """Return the domain type string for prompt generation."""
    if _is_audio_domain(domain):
        return "music production"
    if _is_blender_domain(domain):
        return "3D modeling and scene design"
    if _is_cad_domain(domain):
        return "CAD drafting and technical drawing"
    return "web"


def score_skills(domain: str, *, limit: int = 0, offset: int = 0,
                 max_new: int = 0, model: str = "gpt-5.4") -> dict:
    """Score skills by executing code + rendering + GPT-5.4 vision.

    Args:
        offset: Skip the first N skills in the index.
        limit: Max skills to process from offset (0=all remaining).
        max_new: Stop after scoring this many NEW (previously unscored) skills (0=no limit).
    Returns: {"scored": total, "new_scored": freshly scored, "already_scored": skipped,
              "failed": N, "total_skills": N, "results": dict}
    """
    from core import get_library_dir
    from core.executor import extract_code

    is_audio = _is_audio_domain(domain)
    is_blender = _is_blender_domain(domain)
    is_cad = _is_cad_domain(domain)
    lib_dir = get_library_dir(domain)
    index_path = lib_dir / "index.json"
    metadata_path = lib_dir / "metadata.json"

    if not index_path.exists():
        return {"scored": 0, "new_scored": 0, "already_scored": 0, "failed": 0, "results": {}}

    index = json.loads(index_path.read_text())
    skills = index.get("skills", index) if isinstance(index, dict) else index
    metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}

    total_skills = len(skills)
    if offset > 0:
        skills = skills[offset:]
    if limit > 0:
        skills = skills[:limit]

    results = {}
    new_scored = already_scored = failed = 0
    if is_audio:
        score_prompt = SKILL_SCORE_PROMPT_AUDIO
    elif is_blender:
        score_prompt = SKILL_SCORE_PROMPT_BLENDER
    elif is_cad:
        score_prompt = SKILL_SCORE_PROMPT_CAD
    else:
        score_prompt = SKILL_SCORE_PROMPT
    system_role = _domain_type(domain)

    for i, entry in enumerate(skills):
        # Stop if we've scored enough new ones this round
        if max_new > 0 and new_scored >= max_new:
            log.info("Reached max_new=%d, stopping", max_new)
            break

        sid = entry["skill_id"]
        sname = entry.get("skill_name", sid)
        log.info("[%d/%d] Scoring: %s", i + 1, len(skills), sname)

        # Skip already-scored
        if sid in metadata and "visual_quality" in metadata[sid] and not metadata[sid].get("error"):
            already_scored += 1
            continue

        # Load detail
        detail_path = lib_dir / entry.get("detail_path", f"{sid}.json")
        if not detail_path.exists():
            detail_path = lib_dir / entry.get("category", "") / f"{sid}.json"
        if not detail_path.exists():
            failed += 1
            continue

        analysis = json.loads(detail_path.read_text()).get("analysis", "")
        code = extract_code(analysis)
        if not code:
            results[sid] = {"exec_ok": False, "error": "no_code"}
            failed += 1
            continue

        # --- Audio domain: execute via reaper shim + render spectrogram ---
        if is_audio:
            png_bytes = _score_audio_skill(code, sid, lib_dir)
            if png_bytes is None:
                results[sid] = {"exec_ok": False, "error": "audio_exec_failed"}
                metadata[sid] = results[sid]
                failed += 1
                continue
            exec_ok = True
        elif is_blender:
            # --- Blender domain: execute bpy code + render ---
            png_bytes = _score_blender_skill(code, sid, lib_dir)
            if png_bytes is None:
                results[sid] = {"exec_ok": False, "error": "blender_exec_failed"}
                metadata[sid] = results[sid]
                failed += 1
                continue
            exec_ok = True
        elif is_cad:
            # --- CAD domain: execute MCP code + render DWG through the VM ---
            png_bytes = _score_cad_skill(code, sid, lib_dir)
            if png_bytes is None:
                results[sid] = {"exec_ok": False, "error": "cad_exec_failed"}
                metadata[sid] = results[sid]
                failed += 1
                continue
            exec_ok = True
        else:
            # --- Web domain: execute + render HTML ---
            tmpdir = tempfile.mkdtemp(prefix=f"harness_{sid[:20]}_")
            html_path = None
            exec_ok = False
            try:
                if "def create_component" in code:
                    full_code = code + f"\n\ncreate_component(r'{tmpdir}')\n"
                elif match := re.search(r"def (create_\w+)", code):
                    full_code = code + f"\n\n{match.group(1)}(r'{tmpdir}')\n"
                else:
                    full_code = code

                old_cwd = os.getcwd()
                os.chdir(tmpdir)
                try:
                    exec(full_code, {"__name__": "__main__"})
                    exec_ok = True
                except Exception as e:
                    results[sid] = {"exec_ok": False, "error": str(e)[:200]}
                    metadata[sid] = results[sid]
                    failed += 1
                    continue
                finally:
                    os.chdir(old_cwd)

                for name in ["index.html", "output.html", "demo.html"]:
                    if (Path(tmpdir) / name).exists():
                        html_path = Path(tmpdir) / name
                        break
                if not html_path:
                    htmls = list(Path(tmpdir).glob("*.html"))
                    html_path = htmls[0] if htmls else None
            except Exception as e:
                failed += 1
                continue

            if not html_path:
                results[sid] = {"exec_ok": True, "error": "no_html_output"}
                metadata[sid] = results[sid]
                failed += 1
                shutil.rmtree(tmpdir, ignore_errors=True)
                continue

            png_bytes = _render_html_to_png(html_path)
            shutil.rmtree(tmpdir, ignore_errors=True)

        if not png_bytes:
            results[sid] = {"exec_ok": exec_ok, "error": "render_failed"}
            metadata[sid] = results[sid]
            failed += 1
            continue

        try:
            scores = _vision_score(png_bytes, score_prompt, model=model, system_role=system_role)
            scores["exec_ok"] = True
            results[sid] = scores
            metadata[sid] = {**metadata.get(sid, {}), **scores}
            metadata[sid].pop("error", None)
            new_scored += 1
            log.info("  visual=%s composability=%s creativity=%s",
                     scores.get("visual_quality", "?"), scores.get("composability", "?"),
                     scores.get("creativity", "?"))
        except Exception as e:
            results[sid] = {"exec_ok": True, "error": f"vision_failed: {e}"}
            failed += 1

    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    return {
        "scored": new_scored + already_scored,
        "new_scored": new_scored,
        "already_scored": already_scored,
        "failed": failed,
        "total_skills": total_skills,
        "results": results,
    }


def _score_audio_skill(code: str, skill_id: str, lib_dir: Path) -> bytes | None:
    """Execute a REAPER audio skill and render its output as a spectrogram PNG."""
    import sys as _sys

    # Set up the reaper shim + in-memory project
    mcp_dir = _PROJECT_ROOT / "domains" / "reaper" / "mcp_server"
    _sys.path.insert(0, str(mcp_dir))

    try:
        # Fresh imports to avoid stale module state
        import importlib
        if "reaper_shim" in _sys.modules:
            importlib.reload(_sys.modules["reaper_shim"])
        if "server" in _sys.modules:
            importlib.reload(_sys.modules["server"])

        from server import Track, Project
        import reaper_shim

        project = Project()
        project.bpm = 120
        reaper_shim.bind_project(project)
        reaper_shim._reset()
        _sys.modules["reaper_python"] = reaper_shim

        # Execute the skill code
        exec_code = code + "\ntry:\n    result = create_pattern(bpm=90, key='C', scale='minor', bars=4)\n    print(f'SKILL_RESULT: {result}')\nexcept Exception as e:\n    print(f'SKILL_ERROR: {e}')\n"

        exec(compile(exec_code, f"<skill-{skill_id[:20]}>", "exec"),
             {"project": project, "Track": Track, "__builtins__": __builtins__})

        total_notes = sum(len(t.notes) for t in project.tracks)
        if total_notes == 0:
            return None

        # Render to WAV
        import subprocess
        pm = project.to_pretty_midi()
        tmpdir = tempfile.mkdtemp(prefix=f"harness_audio_{skill_id[:15]}_")
        midi_path = os.path.join(tmpdir, "test.mid")
        wav_path = os.path.join(tmpdir, "test.wav")
        pm.write(midi_path)

        sf_path = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
        if not os.path.exists(sf_path):
            sf_path = "/usr/share/sounds/sf2/default-GM.sf2"

        subprocess.run(
            ["fluidsynth", "-ni", sf_path, midi_path, "-F", wav_path, "-r", "44100", "-g", "0.5"],
            capture_output=True, timeout=30,
        )

        if not os.path.exists(wav_path):
            shutil.rmtree(tmpdir, ignore_errors=True)
            return None

        png_bytes = _render_audio_to_png(Path(wav_path))
        shutil.rmtree(tmpdir, ignore_errors=True)
        return png_bytes

    except Exception as e:
        log.warning("Audio skill execution failed for %s: %s", skill_id, e)
        return None


def _score_blender_skill(code: str, skill_id: str, lib_dir: Path) -> bytes | None:
    """Execute a Blender skill's create_object() code and render to PNG for vision scoring."""
    import sys as _sys

    tmpdir = tempfile.mkdtemp(prefix=f"harness_bpy_{skill_id[:15]}_")
    render_path = os.path.join(tmpdir, "render.png")

    try:
        import bpy

        # Reset scene — remove all non-default objects
        for obj in list(bpy.data.objects):
            if obj.name not in ("Camera", "Light"):
                bpy.data.objects.remove(obj, do_unlink=True)

        # Execute skill code
        full_code = code
        # Call create_object() if defined
        if "def create_object" in code:
            full_code += "\n\ntry:\n    create_object()\nexcept Exception as e:\n    print(f'SKILL_ERROR: {e}')\n"

        old_stdout, old_stderr = _sys.stdout, _sys.stderr
        _sys.stdout = open(os.devnull, 'w')
        _sys.stderr = open(os.devnull, 'w')
        try:
            exec(compile(full_code, f"<skill-{skill_id[:20]}>", "exec"),
                 {"bpy": bpy, "__builtins__": __builtins__})
        finally:
            _sys.stdout.close()
            _sys.stderr.close()
            _sys.stdout = old_stdout
            _sys.stderr = old_stderr

        # Check if any non-default objects were created
        objects = [o for o in bpy.data.objects if o.name not in ("Camera", "Light")]
        if not objects:
            shutil.rmtree(tmpdir, ignore_errors=True)
            return None

        # Set up camera to frame objects
        cam = bpy.data.objects.get("Camera")
        if cam:
            cam.location = (5, -5, 4)
            cam.rotation_euler = (1.1, 0.0, 0.78)
            bpy.context.scene.camera = cam

        # Render
        scene = bpy.context.scene
        scene.render.engine = 'BLENDER_EEVEE'
        scene.render.resolution_x = 512
        scene.render.resolution_y = 512
        scene.render.filepath = render_path
        scene.render.image_settings.file_format = 'PNG'

        old_stdout, old_stderr = _sys.stdout, _sys.stderr
        _sys.stdout = open(os.devnull, 'w')
        _sys.stderr = open(os.devnull, 'w')
        try:
            bpy.ops.render.render(write_still=True)
        finally:
            _sys.stdout.close()
            _sys.stderr.close()
            _sys.stdout = old_stdout
            _sys.stderr = old_stderr

        if not os.path.exists(render_path):
            shutil.rmtree(tmpdir, ignore_errors=True)
            return None

        png_bytes = Path(render_path).read_bytes()
        shutil.rmtree(tmpdir, ignore_errors=True)
        return png_bytes

    except Exception as e:
        log.warning("Blender skill execution failed for %s: %s", skill_id, e)
        shutil.rmtree(tmpdir, ignore_errors=True)
        return None


def _score_cad_skill(code: str, skill_id: str, lib_dir: Path) -> bytes | None:
    """Execute a CAD skill through the real CLI path, then render the DWG."""
    import subprocess
    import sys as _sys

    tmpdir = tempfile.mkdtemp(prefix=f"harness_cad_{skill_id[:15]}_")
    save_path = Path(tmpdir) / f"{skill_id}.dwg"
    session_name = f"harness_{skill_id[:20]}"

    try:
        env = os.environ.copy()
        env["CAD_VM_SESSION_NAME"] = session_name
        cmd = [
            _sys.executable,
            "cli.py",
            "execute",
            "--domain",
            "cad",
            "--skill",
            skill_id,
            "--kwargs",
            f"save_path={save_path}",
            "file_path=" + str(save_path),
            "output_path=" + str(save_path),
            "title=HARNESS_CAD_SKILL",
            "project_title=HARNESS_CAD_SKILL",
            "-v",
        ]
        proc = subprocess.run(
            cmd,
            cwd=_PROJECT_ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=900,
        )
        if proc.returncode != 0:
            log.warning("CAD CLI skill execution failed for %s: %s", skill_id, (proc.stderr or proc.stdout)[-800:])
            shutil.rmtree(tmpdir, ignore_errors=True)
            return None

        if not save_path.exists():
            dwgs = list(Path(tmpdir).glob("*.dwg"))
            if dwgs:
                save_path.write_bytes(dwgs[0].read_bytes())
        if not save_path.exists():
            shutil.rmtree(tmpdir, ignore_errors=True)
            return None

        from domains.cad import verification
        capture_path = Path(tmpdir) / f"{skill_id}.png"
        result = verification.render_and_inspect_dwg(
            save_path,
            view_name=f"skill_{skill_id[:24]}",
            capture_path=capture_path,
        )
        png_bytes = result.get("png_bytes")
        shutil.rmtree(tmpdir, ignore_errors=True)
        return png_bytes
    except Exception as e:
        log.warning("CAD skill execution failed for %s: %s", skill_id, e)
        shutil.rmtree(tmpdir, ignore_errors=True)
        return None


# ═══════════════════════════════════════════════════════════════════════════
# Stage 2: Score Demos
# ═══════════════════════════════════════════════════════════════════════════

DEMO_SCORE_PROMPT = """Rate this web page screenshot (1-5 each):

1. **design**: Layout, color harmony, typography, whitespace
2. **animation_richness**: Motion hints, gradients, hover states, scroll cues
3. **skill_utilization**: Diverse techniques (glassmorphism, grids, effects) vs plain HTML
4. **responsiveness**: Flexible grids, readable text sizes, mobile-ready layout
5. **cohesion**: Consistent palette, spacing, shape language across sections

Return JSON: {"design": N, "animation_richness": N, "skill_utilization": N, "responsiveness": N, "cohesion": N, "overall": N, "strengths": "...", "weaknesses": "..."}
"overall" = average of 5 scores, rounded to 1 decimal."""


DEMO_SCORE_PROMPT_BLENDER = """Rate this Blender 3D scene render (1-5 each):

1. **composition**: Camera angle, framing, rule of thirds, depth
2. **lighting**: Key/fill/rim balance, atmosphere, volumetrics
3. **skill_utilization**: Diverse 3D techniques (procedural materials, particle systems, modifiers, shader nodes) vs plain primitives
4. **material_quality**: Surface fidelity — PBR realism or stylized consistency
5. **scene_cohesion**: Consistent art style, scale, color palette across all elements

Return JSON: {"design": N, "animation_richness": N, "skill_utilization": N, "responsiveness": N, "cohesion": N, "overall": N, "strengths": "...", "weaknesses": "..."}
Map: design=composition, animation_richness=lighting, skill_utilization=skill_utilization, responsiveness=material_quality, cohesion=scene_cohesion.
"overall" = average of 5 scores, rounded to 1 decimal."""


DEMO_SCORE_PROMPT_CAD = """Rate this CAD technical drawing screenshot (1-5 each):

1. **design**: Is the drawing framed cleanly and visually legible?
2. **animation_richness**: Use this as drafting richness — dimensions, labels, repeated features, layering cues.
3. **skill_utilization**: Does the drawing combine multiple useful drafting techniques instead of just one primitive?
4. **responsiveness**: Use this as precision/readability — text scale, line placement, uncluttered annotations.
5. **cohesion**: Do the geometry and annotations feel like one coherent technical drawing?

Return JSON: {"design": N, "animation_richness": N, "skill_utilization": N, "responsiveness": N, "cohesion": N, "overall": N, "strengths": "...", "weaknesses": "..."}
"overall" = average of 5 scores, rounded to 1 decimal."""


def score_demos(domain: str, *, model: str = "gpt-5.4") -> dict:
    """Score all demos in demo/<domain>/."""
    demo_dir = _PROJECT_ROOT / "demo" / domain
    if not demo_dir.exists():
        return {"demos": {}, "avg_overall": 0}

    is_audio = _is_audio_domain(domain)
    is_blender = _is_blender_domain(domain)
    is_cad = _is_cad_domain(domain)
    demo_results = {}

    if is_audio:
        # Audio domain: score WAV files directly
        score_prompt = DEMO_SCORE_PROMPT_AUDIO
        system_role = "music production"
        wavs = sorted(demo_dir.glob("*.wav"), key=os.path.getmtime, reverse=True)

        for wav_file in wavs:
            name = wav_file.stem
            log.info("Scoring demo: %s", name)

            png_bytes = _render_audio_to_png(wav_file)
            if not png_bytes:
                demo_results[name] = {"error": "spectrogram_render_failed"}
                continue

            # Find skills used from agent log
            skills_used = []
            log_file = demo_dir / f"{name}.json"
            if not log_file.exists():
                # Try matching log files
                for lf in demo_dir.glob("*.json"):
                    if lf.stem != "harness_scores" and lf.stem != "evolution_report":
                        log_file = lf
                        break

            if log_file.exists():
                try:
                    text = log_file.read_text()
                    skills_used = re.findall(r"apply_skill.*?skill_id['\"]:\s*['\"]([^'\"]+)", text)
                except Exception:
                    pass

            try:
                scores = _vision_score(png_bytes, score_prompt, model=model, system_role=system_role)
                scores["skills_used"] = skills_used
                scores["skills_count"] = len(skills_used)
                demo_results[name] = scores
                log.info("  Overall: %s", scores.get("overall", "?"))
            except Exception as e:
                demo_results[name] = {"error": str(e)[:200]}
    elif is_blender:
        # Blender domain: score rendered PNG files
        score_prompt = DEMO_SCORE_PROMPT_BLENDER
        system_role = "3D modeling and scene design"
        pngs = sorted(
            [f for f in demo_dir.glob("*.png") if not f.name.startswith("_")],
            key=os.path.getmtime, reverse=True,
        )

        for png_file in pngs:
            name = png_file.stem
            log.info("Scoring demo: %s", name)

            try:
                png_bytes = png_file.read_bytes()
            except Exception:
                demo_results[name] = {"error": "read_failed"}
                continue

            # Find skills used from agent log
            skills_used = []
            log_file = demo_dir / f"{name}.json"
            if log_file.exists():
                try:
                    text = log_file.read_text()
                    skills_used = re.findall(r"add_object_from_skill.*?skill_id['\"]:\s*['\"]([^'\"]+)", text)
                    if not skills_used:
                        skills_used = re.findall(r"get_skill_code.*?skill_id['\"]:\s*['\"]([^'\"]+)", text)
                except Exception:
                    pass

            try:
                scores = _vision_score(png_bytes, score_prompt, model=model, system_role=system_role)
                scores["skills_used"] = skills_used
                scores["skills_count"] = len(skills_used)
                demo_results[name] = scores
                log.info("  Overall: %s", scores.get("overall", "?"))
            except Exception as e:
                demo_results[name] = {"error": str(e)[:200]}
    elif is_cad:
        score_prompt = DEMO_SCORE_PROMPT_CAD
        system_role = "CAD drafting and technical drawing"
        pngs = sorted(
            [
                f for f in demo_dir.glob("*.png")
                if not f.name.startswith("_") and ".verify." not in f.name
            ],
            key=os.path.getmtime, reverse=True,
        )

        for png_file in pngs:
            name = png_file.stem
            log.info("Scoring demo: %s", name)
            try:
                png_bytes = png_file.read_bytes()
            except Exception:
                demo_results[name] = {"error": "read_failed"}
                continue

            skills_used = []
            for log_file in (demo_dir / f"{name}.json", demo_dir / f"{name}_log.json"):
                if not log_file.exists():
                    continue
                try:
                    text = log_file.read_text()
                    skills_used = re.findall(r'"skill_id"\s*:\s*"([^"]+)"', text)
                    break
                except Exception:
                    pass

            try:
                scores = _vision_score(png_bytes, score_prompt, model=model, system_role=system_role)
                scores["skills_used"] = skills_used
                scores["skills_count"] = len(skills_used)
                demo_results[name] = scores
                log.info("  Overall: %s", scores.get("overall", "?"))
            except Exception as e:
                demo_results[name] = {"error": str(e)[:200]}
    else:
        # Web domain: score HTML pages
        score_prompt = DEMO_SCORE_PROMPT
        system_role = "web design"
        for subdir in sorted(demo_dir.iterdir()):
            if not subdir.is_dir() or not (subdir / "index.html").exists():
                continue

            name = subdir.name
            log.info("Scoring demo: %s", name)

            png_bytes = _render_html_to_png(subdir / "index.html")
            if not png_bytes:
                demo_results[name] = {"error": "render_failed"}
                continue

            skills_used = []
            for lf in demo_dir.glob("agent_log_*.json"):
                try:
                    text = lf.read_text()
                    if name.replace("-", "_") in text or name in text:
                        skills_used = re.findall(r"add_component_from_skill.*?skill_id['\"]:\s*['\"](\w+)", text)
                        break
                except Exception:
                    pass

            try:
                scores = _vision_score(png_bytes, score_prompt, model=model, system_role=system_role)
                scores["skills_used"] = skills_used
                scores["skills_count"] = len(skills_used)
                demo_results[name] = scores
                log.info("  Overall: %s", scores.get("overall", "?"))
            except Exception as e:
                demo_results[name] = {"error": str(e)[:200]}

    overalls = [d["overall"] for d in demo_results.values() if isinstance(d.get("overall"), (int, float))]
    avg = round(sum(overalls) / len(overalls), 1) if overalls else 0

    output = {"demos": demo_results, "avg_overall": avg}
    (demo_dir / "harness_scores.json").write_text(json.dumps(output, indent=2, ensure_ascii=False))
    return output


# ═══════════════════════════════════════════════════════════════════════════
# Stage 3: Evolve — Core Architecture
# ═══════════════════════════════════════════════════════════════════════════

def evolve(domain: str, *, model: str = "gpt-5.4", dry_run: bool = False) -> dict:
    """Main evolution: gap analysis → queries, pruning, architecture suggestions."""
    state = _load_domain_state(domain)

    prompt = f"""You are an architecture evolution advisor for a {_domain_type(domain)} skill library.

## Current State
**Total skills**: {len(state['index'].get('skills', []))}
**Categories**: {json.dumps(state['cat_stats'], indent=2)}
**Demo scores**: {json.dumps(state['demo_scores'].get('demos', {}), indent=2)[:2000]}
**Current query_pool** ({len(state['query_pool'])} queries): {json.dumps(state['query_pool'][:15])}
**Available categories**: {state['categories']}

## Rules
- Only suggest prompt changes if there are CLEAR PROBLEMS (failures, bugs, wrong behavior). Do NOT suggest style/tone tweaks.
- Focus on concrete, data-driven recommendations.

Return JSON:
{{
  "analysis": "2-3 sentence health summary",
  "weak_categories": ["categories with <5 skills or avg_visual < 3"],
  "missing_categories": ["configured categories with 0 skills"],
  "new_queries": ["5-10 YouTube search queries to fill gaps"],
  "prune_threshold": 2.0,
  "prompt_changes": ["ONLY if there are actual bugs/failures in demos — otherwise empty list"],
  "architecture_suggestions": ["0-2 structural changes to domain.yaml or workflow"]
}}"""

    evolution = _llm_json(prompt, system="You are a skill library architect. Return ONLY valid JSON.",
                          model=model)
    actions = []

    if not dry_run and "analysis" in evolution:
        # Add new queries
        new_queries = evolution.get("new_queries", [])
        yaml_path = state["domain_dir"] / "domain.yaml"
        if new_queries and yaml_path.exists():
            yaml_text = yaml_path.read_text()
            additions = [q.strip().strip('"\'') for q in new_queries if q.strip().strip('"\'') not in yaml_text]
            if additions:
                lines = yaml_text.splitlines()
                insert_at = None
                in_query_pool = False
                for i, line in enumerate(lines):
                    if re.match(r"^query_pool:\s*$", line):
                        in_query_pool = True
                        insert_at = i + 1
                        continue
                    if in_query_pool:
                        if re.match(r"^  - ", line) or not line.strip():
                            insert_at = i + 1
                            continue
                        break
                if insert_at is not None:
                    new_lines = [f'  - "{q}"' for q in additions]
                    lines[insert_at:insert_at] = new_lines
                    yaml_path.write_text("\n".join(lines) + "\n")
                    actions.append(f"Added {len(additions)} queries to domain.yaml")

        # Prune low-quality
        threshold = evolution.get("prune_threshold", 2.0)
        pruned = 0
        for sid, meta in state["metadata"].items():
            vq = meta.get("visual_quality")
            if isinstance(vq, (int, float)) and vq < threshold and not meta.get("pruned"):
                meta["pruned"] = True
                meta["prune_reason"] = f"visual_quality={vq} < {threshold}"
                pruned += 1
        if pruned:
            state["metadata_path"].write_text(json.dumps(state["metadata"], indent=2, ensure_ascii=False))
            actions.append(f"Pruned {pruned} low-quality skills")

        # Prompt changes — ONLY for real bugs
        prompt_changes = evolution.get("prompt_changes", [])
        if prompt_changes:
            for change in prompt_changes:
                actions.append(f"[PROMPT SUGGESTION] {change}")

        for s in evolution.get("architecture_suggestions", []):
            actions.append(f"[ARCHITECTURE] {s}")

    evolution["actions_taken"] = actions
    report_dir = state["demo_dir"] if state["demo_dir"].exists() else state["lib_dir"]
    (report_dir / "evolution_report.json").write_text(json.dumps(evolution, indent=2, ensure_ascii=False))
    return evolution


# ═══════════════════════════════════════════════════════════════════════════
# Stage 4: Evolve Distiller — Fix Skill Extraction
# ═══════════════════════════════════════════════════════════════════════════

def evolve_distiller(domain: str, *, model: str = "gpt-5.4", dry_run: bool = False) -> dict:
    """Analyze skill failure patterns → suggest distiller prompt fixes.

    CONSERVATIVE: only changes distiller_prompt.md if there are clear,
    recurring failure patterns (>3 skills with same error type).
    """
    state = _load_domain_state(domain)

    # Collect failure patterns
    failures = {}
    for sid, meta in state["metadata"].items():
        if meta.get("exec_ok"):
            continue
        err = meta.get("error", "unknown")
        # Normalize errors
        err_type = "unknown"
        if "no_code" in err:
            err_type = "no_code_extracted"
        elif "no_html_output" in err:
            err_type = "code_runs_but_no_html"
        elif "ImportError" in err or "ModuleNotFoundError" in err:
            err_type = "missing_import"
        elif "SyntaxError" in err:
            err_type = "syntax_error"
        elif "NameError" in err or "AttributeError" in err:
            err_type = "code_bug"
        elif "render_failed" in err:
            err_type = "render_failed"
        else:
            err_type = "runtime_error"

        if err_type not in failures:
            failures[err_type] = {"count": 0, "examples": []}
        failures[err_type]["count"] += 1
        if len(failures[err_type]["examples"]) < 3:
            failures[err_type]["examples"].append(err[:150])

    if not failures:
        return {"analysis": "No failures found — distiller prompt is working well.", "changes": []}

    # Read current distiller prompt
    distiller_path = state["domain_dir"] / "distiller_prompt.md"
    distiller_text = distiller_path.read_text() if distiller_path.exists() else "(not found)"

    prompt = f"""You are a distiller prompt engineer. Analyze these skill extraction FAILURE patterns
and suggest MINIMAL, TARGETED fixes to the distiller prompt.

## Failure Patterns
{json.dumps(failures, indent=2)}

## Current Distiller Prompt (first 1500 chars)
{distiller_text[:1500]}

## Rules
- ONLY suggest changes that directly address a failure pattern with count >= 3
- Do NOT rewrite the prompt — suggest specific additions or clarifications
- If failures are < 3 occurrences each, say "no changes needed"
- Preserve all existing working behavior

Return JSON:
{{
  "analysis": "summary of failure patterns",
  "changes_needed": true/false,
  "fixes": [
    {{"pattern": "error_type", "count": N, "fix": "specific text to add/change in distiller_prompt.md", "location": "which section to modify"}}
  ]
}}"""

    result = _llm_json(prompt, system="You are conservative. Only fix real problems.", model=model)
    actions = []

    if not dry_run and result.get("changes_needed") and distiller_path.exists():
        fixes = result.get("fixes", [])
        applied = 0
        distiller_text = distiller_path.read_text()
        for fix in fixes:
            if fix.get("count", 0) >= 3 and fix.get("fix"):
                # Append fix as a note rather than modifying existing text
                note = f"\n\n<!-- HARNESS FIX ({fix['pattern']}, {fix['count']} failures) -->\n"
                note += f"<!-- {fix['fix']} -->\n"
                if note.strip() not in distiller_text:
                    distiller_text += note
                    applied += 1
        if applied:
            distiller_path.write_text(distiller_text)
            actions.append(f"Added {applied} fix notes to distiller_prompt.md")

    result["actions_taken"] = actions
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Stage 5: Evolve Agent — Best Composition Patterns
# ═══════════════════════════════════════════════════════════════════════════

def evolve_agent(domain: str, *, model: str = "gpt-5.4", dry_run: bool = False) -> dict:
    """Analyze high-scoring demos → extract best skill composition patterns.

    Writes a COMPOSITION_PATTERNS section to agent_prompt.md showing
    which skill combos produce the best results.
    """
    state = _load_domain_state(domain)
    demo_scores = state["demo_scores"].get("demos", {})

    if not demo_scores:
        return {"analysis": "No demo scores available. Run score-demos first.", "patterns": []}

    # Build demo analysis data
    demo_data = []
    for name, scores in demo_scores.items():
        if isinstance(scores.get("overall"), (int, float)):
            demo_data.append({
                "name": name,
                "overall": scores["overall"],
                "design": scores.get("design"),
                "animation_richness": scores.get("animation_richness"),
                "skills_used": scores.get("skills_used", []),
                "skills_count": scores.get("skills_count", 0),
                "strengths": scores.get("strengths", ""),
                "weaknesses": scores.get("weaknesses", ""),
            })

    demo_data.sort(key=lambda x: x["overall"], reverse=True)

    domain_type = _domain_type(domain)
    prompt = f"""Analyze these {domain_type} demo results and extract SKILL COMPOSITION PATTERNS.

## Demo Results (sorted by score)
{json.dumps(demo_data, indent=2)}

## Task
Identify what makes high-scoring demos different from low-scoring ones.
Focus on: which skill categories they combine, how many skills they use,
what structural patterns they follow.

Return JSON:
{{
  "analysis": "what separates good demos from bad ones",
  "winning_patterns": [
    {{"pattern": "description", "example_demo": "name", "score": N}},
  ],
  "losing_patterns": [
    {{"pattern": "description", "example_demo": "name", "score": N}},
  ],
  "recommended_combos": [
    {{"task_type": "e.g. landing page", "skill_categories": ["animation", "card_layout", "navigation"], "min_skills": N}},
  ],
  "mcp_server_suggestions": ["0-2 suggestions for MCP tool improvements based on demo patterns"]
}}"""

    result = _llm_json(prompt, system=f"You are a {_domain_type(domain)} composition analyst. Return ONLY valid JSON.",
                       model=model)
    actions = []

    if not dry_run:
        # Write composition patterns to agent_prompt
        combos = result.get("recommended_combos", [])
        winning = result.get("winning_patterns", [])
        mcp_suggestions = result.get("mcp_server_suggestions", [])

        if combos or winning:
            prompt_path = state["domain_dir"] / "agent_prompt.md"
            if prompt_path.exists():
                prompt_text = prompt_path.read_text()
                section = "\n\n# COMPOSITION PATTERNS (auto-learned from demo scoring)\n\n"
                section += "These patterns are extracted from the highest-scoring demos:\n\n"

                if winning:
                    section += "## What Works\n"
                    for w in winning[:5]:
                        section += f"- **{w.get('pattern', '?')}** (score: {w.get('score', '?')}, demo: {w.get('example_demo', '?')})\n"
                    section += "\n"

                if combos:
                    section += "## Recommended Skill Combos\n"
                    for c in combos[:5]:
                        cats = ", ".join(c.get("skill_categories", []))
                        section += f"- **{c.get('task_type', '?')}**: use [{cats}], min {c.get('min_skills', 2)} skills\n"
                    section += "\n"

                # Replace or append
                if "# COMPOSITION PATTERNS" in prompt_text:
                    prompt_text = re.sub(r"# COMPOSITION PATTERNS.*?(?=\n# [A-Z]|\Z)",
                                         section.strip() + "\n\n", prompt_text, flags=re.DOTALL)
                else:
                    # Insert before EVOLUTION NOTES or at end
                    if "# EVOLUTION NOTES" in prompt_text:
                        prompt_text = prompt_text.replace("# EVOLUTION NOTES",
                                                          section.strip() + "\n\n# EVOLUTION NOTES")
                    else:
                        prompt_text += section

                prompt_path.write_text(prompt_text)
                actions.append(f"Updated COMPOSITION PATTERNS in agent_prompt.md")

        # Log MCP suggestions
        for s in mcp_suggestions:
            actions.append(f"[MCP SUGGESTION] {s}")

    result["actions_taken"] = actions
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Demo Task Generation
# ═══════════════════════════════════════════════════════════════════════════

_WEB_TASK_POOL = [
    "Build a fintech SaaS landing page with animated hero, feature cards with hover effects, pricing table, and testimonial carousel. Dark theme with teal (#14b8a6) accent.",
    "Build a creative agency portfolio with canvas particle background, project grid with lightbox, team section, and contact form. Dark theme with coral (#ff6b6b) accent.",
    "Build a music streaming app landing page with waveform animation hero, playlist showcase cards, artist spotlight section, and dark glassmorphism pricing toggle. Purple (#a855f7) accent.",
    "Build an e-commerce product page for luxury sneakers with floating product hero, color picker, size selector, review carousel, and animated add-to-cart button. Dark theme with gold (#fbbf24) accent.",
    "Build a cybersecurity startup landing page with matrix-style animated background, threat dashboard mockup, feature bento grid with neon borders, and enterprise CTA. Dark theme with green (#22c55e) accent.",
    "Build a fitness tracking app landing page with animated stat counters, workout category cards with 3D tilt, progress ring animations, and a glassmorphism signup form. Dark theme with orange (#f97316) accent.",
    "Build a developer tools documentation landing page with code syntax highlighting hero, feature comparison table, integration cards grid, and terminal-style CTA section. Dark theme with blue (#3b82f6) accent.",
    "Build a travel booking landing page with parallax destination hero, destination cards with hover zoom, animated booking form, and customer review section. Dark theme with sky blue (#0ea5e9) accent.",
]


_REAPER_TASK_POOL = [
    # === Famous Artists ===
    "Create a Kanye West chipmunk soul beat. 92 BPM, E minor, 24 bars. Chipmunk piano chops (octave 5-6), gospel choir pad, boom-bap drums (is_drum=True), 808 sub bass, soul melody hook. Use render_project(style='kanye_soul'), review_audio, save.",
    "Create a Metro Boomin dark trap beat. 142 BPM half-time, A minor, 24 bars. Dark sustained pad, rolling 16th hi-hats (is_drum=True), hard 808 glide bass, sparse eerie melody. Use render_project(style='clean'), review_audio, save.",
    "Create a J Dilla boom-bap beat. 88 BPM, D minor, 24 bars. MPC-style swung drums (is_drum=True) with human feel, jazzy Rhodes chords, warm walking bass, subtle melody. Use render_project(style='lofi_hiphop'), review_audio, save.",
    "Create a Pharrell/Neptunes style beat. 100 BPM, G minor, 24 bars. Punchy staccato synth stabs, crisp four-on-the-floor kick (is_drum=True), funky bass, minimal melody. Use render_project(style='clean'), review_audio, save.",
    "Create a Dr. Dre G-funk beat. 96 BPM, C minor, 24 bars. Smooth electric piano chords, bouncy syncopated drums (is_drum=True), deep rolling bass, whining lead synth. Use render_project(style='clean'), review_audio, save.",
    "Create a Tyler the Creator jazzy indie beat. 82 BPM, Eb major, 24 bars. Warm jazzy piano chords, soft vinyl drums (is_drum=True), mellow bass, playful synth melody. Use render_project(style='lofi_hiphop'), review_audio, save.",
    "Create a Frank Ocean R&B beat. 78 BPM, F minor, 24 bars. Warm dreamy chords, soft drums (is_drum=True), deep sub bass, emotional vocal-style melody. Use render_project(style='lofi_hiphop'), review_audio, save.",
    "Create a Travis Scott dark ambient trap beat. 136 BPM half-time, F# minor, 24 bars. Heavy reverb pad atmosphere, sparse hard drums (is_drum=True), 808 bass, eerie autotuned-style melody. Use render_project(style='kanye_soul'), review_audio, save.",
    "Create a MF DOOM / Madlib abstract hip-hop beat. 94 BPM, Bb minor, 24 bars. Dusty vinyl sample chops, off-kilter drum pattern (is_drum=True) with unusual timing, warm bass, quirky melody. Use render_project(style='lofi_hiphop'), review_audio, save.",
    "Create a Nujabes-style jazzy lo-fi beat. 85 BPM, G minor, 24 bars. Smooth jazz piano + Rhodes, gentle brush drums (is_drum=True), upright bass, flute melody (program 73). Use render_project(style='lofi_hiphop'), review_audio, save.",
    "Create a Timbaland-style futuristic R&B beat. 108 BPM, D minor, 24 bars. Staccato vocal-like synth hits, heavy kick pattern (is_drum=True), bouncy bass, eastern-influenced melody. Use render_project(style='clean'), review_audio, save.",
    "Create a Flying Lotus experimental beat. 130 BPM, Ab minor, 24 bars. Glitchy broken drums (is_drum=True), deep sub bass, ethereal pad layers, unpredictable melodic fragments. Use render_project(style='clean'), review_audio, save.",
    # === Genre/Era Styles ===
    "Create a Daft Punk French house track. 122 BPM, F minor, 24 bars. Filtered disco chords (program 0), four-on-the-floor kick (is_drum=True), funky bass guitar (program 33), vocodered lead. Use render_project(style='clean'), review_audio, save.",
    "Create a 70s funk/disco groove. 112 BPM, Bb major, 24 bars. Wah-wah guitar chords (program 28), tight funk drums (is_drum=True), slap bass (program 36), brass stabs (program 61). Use render_project(style='clean'), review_audio, save.",
    "Create a jazz trio piece. 140 BPM swing, C major, 24 bars. Walking upright bass (program 32), ride cymbal swing drums (is_drum=True), jazz piano comping (program 0) with 7th/9th voicings. Use render_project(style='clean'), review_audio, save.",
    "Create a bossa nova piece. 120 BPM, D major, 24 bars. Nylon guitar chords (program 24), brushed bossa drums (is_drum=True), acoustic bass (program 32), flute melody (program 73). Use render_project(style='clean'), review_audio, save.",
    "Create a 80s city pop / Japanese pop track. 108 BPM, A major, 24 bars. Bright FM electric piano (program 4), gated reverb drums (is_drum=True), slap bass, soprano sax (program 64) melody. Use render_project(style='synthwave'), review_audio, save.",
    "Create a lo-fi hip-hop chill beat. 75 BPM, A minor, 24 bars. Dusty piano chords, lazy boom-bap drums (is_drum=True), warm bass, ambient texture. Use render_project(style='lofi_hiphop'), review_audio, save.",
    "Create a synthwave retrowave track. 110 BPM, C minor, 24 bars. Arpeggiated synth, lush pad chords, driving octave bass, electronic drums (is_drum=True), soaring lead. Use render_project(style='synthwave'), review_audio, save.",
    "Create a reggae/dub track. 76 BPM, G major, 24 bars. Organ bubble chords on upbeats (program 16), one-drop drums (is_drum=True), deep dub bass, melodica melody (program 22). Use render_project(style='lofi_hiphop'), review_audio, save.",
    "Create a vaporwave future funk beat. 96 BPM, Eb major, 24 bars. Slowed detuned piano, slap bass (program 33), retro 80s drums (is_drum=True), shimmer pad (program 89), smooth sax (program 66). Use render_project(style='synthwave'), review_audio, save.",
    "Create a UK garage 2-step beat. 130 BPM, Bb minor, 24 bars. Shuffled skippy drums (is_drum=True), deep sub bass, chopped vocal-style stabs, warm organ pad. Use render_project(style='clean'), review_audio, save.",
    "Create an afrobeat groove. 110 BPM, F major, 24 bars. Polyrhythmic drums (is_drum=True), Tony Allen-style hi-hat patterns, Fela-style organ, rhythmic guitar, bass groove. Use render_project(style='clean'), review_audio, save.",
    "Create a drum & bass track. 174 BPM, A minor, 24 bars. Fast breakbeat drums (is_drum=True), deep rolling sub bass, atmospheric pad, reese bass lead. Use render_project(style='clean'), review_audio, save.",
    "Create a post-punk / dark wave track. 130 BPM, E minor, 24 bars. Driving bass guitar (program 33), sparse angular guitar (program 25), motorik drums (is_drum=True), cold synth pad, baritone vocal-range melody. Use render_project(style='clean'), review_audio, save.",
]

_BLENDER_TASK_POOL = [
    "Build a stylized low-poly medieval village: cobblestone ground, 3-4 small houses, a market stall, a well, and a large oak tree. Warm golden-hour lighting with volumetric fog. Use skills for scatter, materials, and HDRI lighting. Render to demo/blender/medieval_village.png, save as medieval_village.",
    "Build a sci-fi space station docking bay: large hangar with metallic paneled walls (use hard-surface paneling skills), glowing control panels, neon strip lighting along floor guides (cyan), and volumetric haze. Low camera angle. Render to demo/blender/space_station.png, save as space_station.",
    "Build a Japanese zen garden: raked sand (procedural texture), mossy rocks scattered around a small pond (water shader skill), a bamboo fence, a stone lantern, and cherry blossom petals (particle system). Soft overcast HDRI lighting. Render to demo/blender/zen_garden.png, save as zen_garden.",
    "Build a neon-lit rainy alleyway: narrow alley with brick walls, puddles on the ground (reflective water material), neon signs on walls (glow emission skills), steam/fog rising, a few crates. Moody cinematic lighting with cyan and magenta accents. Render to demo/blender/neon_alley.png, save as neon_alley.",
    "Build a floating island fantasy diorama: a chunk of earth floating in sky, with a tiny house, a waterfall (particle + water skills), scattered trees, and volumetric clouds. Bright stylized lighting. Render to demo/blender/floating_island.png, save as floating_island.",
    "Build an abandoned factory interior: rusted metal beams, broken windows with god rays (volumetric lighting skill), overgrown plants, puddles on cracked concrete floor, industrial machinery. Moody atmospheric lighting. Render to demo/blender/abandoned_factory.png, save as abandoned_factory.",
    "Build a crystal cave scene: large cave with bioluminescent crystals (emission material + glow skills), stalactites, an underground pool (water shader), and volumetric light beams from a crack above. Deep blue and purple palette. Render to demo/blender/crystal_cave.png, save as crystal_cave.",
    "Build a retro-futuristic living room: 1960s space-age curved furniture, a large window showing a planetary vista, chrome and velvet materials, warm tungsten lighting mixed with cool moonlight. Render to demo/blender/retro_living_room.png, save as retro_living_room.",
]

_CAD_TASK_POOL = [
    "Create a mechanical mounting plate with an outer boundary 200x140, four corner holes, one center hole, overall dimensions, and a title note. Save to demo/cad/auto_plate_showcase.dwg and finish.",
    "Create a title-block sheet setup with outer border, inner border, title panel, scale field, revision field, and project title text. Save to demo/cad/title_block_showcase.dwg and finish.",
    "Create a two-room floor plan shell with one partition wall, room labels, one door label, one window label, and overall width/height dimensions. Save to demo/cad/two_room_showcase.dwg and finish.",
    "Create a flange face drawing with outer diameter, inner bore, four symmetric bolt holes, and a title note. Save to demo/cad/flange_showcase.dwg and finish.",
]

_TASK_POOLS = {
    "web": _WEB_TASK_POOL,
    "reaper": _REAPER_TASK_POOL,
    "blender": _BLENDER_TASK_POOL,
    "cad": _CAD_TASK_POOL,
}


def generate_demo_task(domain: str, *, model: str = "gpt-5.4",
                       existing_demos: list[str] | None = None) -> str:
    """Generate a novel demo task based on skill library state.

    Falls back to a hardcoded task pool if LLM fails.
    """
    state = _load_domain_state(domain)

    # Build strong categories list
    strong_cats = [
        c for c, s in state["cat_stats"].items()
        if s.get("exec_ok", 0) > 0 or s.get("count", 0) >= 5
    ]
    existing = existing_demos or []

    prompt = f"""Generate ONE specific, creative demo task for a {_domain_type(domain)} agent.

Available skill categories: {strong_cats}
Previously completed demos: {existing[:10]}

Requirements:
- The task should use 2-4 different skill categories
- Be specific about objects, colors, materials, lighting, and theme
- Must be DIFFERENT from previous demos
- For Blender: include "Render to demo/blender/<name>.png, save as <name>" at the end
- For CAD: include "Save to demo/cad/<name>.dwg and finish" at the end
- For web: include specific sections and visual details
- Emphasize using SKILLS from the library (via add_object_from_skill or adapting skill code)
- Output ONLY the task description as a single paragraph. No JSON, no formatting."""

    try:
        msg = _llm_json.__wrapped__ if hasattr(_llm_json, '__wrapped__') else None
        from core.llm import call_azure_openai
        result = call_azure_openai(
            [{"role": "user", "content": prompt}],
            model=model, reasoning_effort="low", max_completion_tokens=512,
        )
        task = result.get("content", "").strip()
        if task and len(task) > 30:
            # Ensure Blender tasks have render/save instructions
            if _is_blender_domain(domain) and "render" not in task.lower():
                import re as _re
                name_m = _re.search(r'called\s+(\w+)|named\s+(\w+)', task)
                name = (name_m.group(1) or name_m.group(2)) if name_m else "auto_demo"
                task += f" Render to demo/blender/{name}.png and save as {name}."
            if _is_cad_domain(domain) and "demo/cad/" not in task.lower():
                import re as _re
                name_m = _re.search(r'called\s+(\w+)|named\s+(\w+)', task)
                name = (name_m.group(1) or name_m.group(2)) if name_m else "auto_demo"
                task += f" Save to demo/cad/{name}.dwg and finish."
            return task
    except Exception as e:
        log.warning("Task generation failed: %s", e)

    # Fallback to pool
    import random
    pool = _TASK_POOLS.get(domain, _WEB_TASK_POOL)
    available = [t for t in pool if not any(d in t.lower() for d in existing)]
    return random.choice(available if available else pool)


# ═══════════════════════════════════════════════════════════════════════════
# Stage 6: Auto-Collect — Search & Fill Gaps
# ═══════════════════════════════════════════════════════════════════════════

def auto_collect(domain: str, *, model: str = "gpt-5.4", cycles: int = 1,
                 videos_per_query: int = 3, workers: int = 3) -> dict:
    """Identify missing skills via web search → run targeted collection.

    Uses GPT-5.4 to analyze gaps, generate targeted YouTube queries,
    then calls the collect pipeline to fill them.
    """
    state = _load_domain_state(domain)

    # Ask GPT-5.4 what skills are missing
    prompt = f"""You are a {_domain_type(domain)} skills librarian. The library needs more skills in certain areas.

## Current Library
**Categories**: {json.dumps(state['cat_stats'], indent=2)}
**Configured categories**: {state['categories']}

## Task
Generate 10-15 highly specific YouTube search queries designed to find tutorials
for the MOST NEEDED skills. Prioritize:
1. Categories with 0 skills (highest priority)
2. Categories with < 5 skills
3. Categories where avg_visual < 3.0 (need higher quality tutorials)
4. Specific techniques the demos are missing

Return JSON:
{{
  "gap_analysis": "summary of what's missing",
  "priority_queries": [
    {{"query": "YouTube search string", "target_category": "category", "reason": "why this is needed"}}
  ]
}}

Make queries SPECIFIC enough to find good tutorials (include "tutorial", "REAPER", "DAW" or "CSS", "HTML" etc. as appropriate for the domain)."""

    result = _llm_json(prompt, system="You are a web tutorial curator. Return ONLY valid JSON.",
                       model=model)

    queries = [q["query"] for q in result.get("priority_queries", []) if "query" in q]
    if not queries:
        return {"analysis": "No queries generated", "collected": 0}

    log.info("Auto-collect: %d targeted queries generated", len(queries))
    for i, q in enumerate(queries):
        reason = result["priority_queries"][i].get("reason", "")
        log.info("  [%d] %s — %s", i + 1, q, reason)

    # Run collection with these specific queries
    # Temporarily override query_pool with targeted queries
    from core.auto_collect import run_cycle
    from core import load_domain

    domain_cfg = load_domain(domain)
    original_pool = domain_cfg.get("query_pool", [])
    domain_cfg["query_pool"] = queries  # Override with targeted queries

    total_collected = 0
    try:
        for cycle in range(cycles):
            log.info("Auto-collect cycle %d/%d with %d targeted queries", cycle + 1, cycles, len(queries))
            cycle_result = run_cycle(
                domain_cfg,
                queries_per_cycle=min(len(queries), 5),
                videos_per_query=videos_per_query,
                workers=workers,
            )
            total_collected += cycle_result.get("skills_stored", 0)
            log.info("  Cycle %d: %d skills stored", cycle + 1, cycle_result.get("skills_stored", 0))
    finally:
        domain_cfg["query_pool"] = original_pool  # Restore

    result["collected"] = total_collected
    result["queries_used"] = queries
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Full Loop: Run All Stages
# ═══════════════════════════════════════════════════════════════════════════

def run_full_loop(domain: str, *, model: str = "gpt-5.4", skill_limit: int = 50,
                  collect_cycles: int = 1, dry_run: bool = False) -> dict:
    """Run the complete self-evolution loop:
    score-skills → score-demos → evolve → evolve-distiller → evolve-agent → auto-collect

    Returns summary of all stages.
    """
    log.info("=" * 60)
    log.info("SELF-EVOLUTION LOOP — domain: %s", domain)
    log.info("=" * 60)

    results = {}

    # Stage 1
    log.info("\n--- Stage 1: Score Skills ---")
    results["score_skills"] = score_skills(domain, limit=skill_limit, model=model)
    log.info("Scored: %d, Failed: %d", results["score_skills"]["scored"], results["score_skills"]["failed"])

    # Stage 2
    log.info("\n--- Stage 2: Score Demos ---")
    results["score_demos"] = score_demos(domain, model=model)
    log.info("Avg overall: %.1f", results["score_demos"]["avg_overall"])

    # Stage 3
    log.info("\n--- Stage 3: Evolve Architecture ---")
    results["evolve"] = evolve(domain, model=model, dry_run=dry_run)
    log.info("Actions: %s", results["evolve"].get("actions_taken", []))

    # Stage 4
    log.info("\n--- Stage 4: Evolve Distiller ---")
    try:
        results["evolve_distiller"] = evolve_distiller(domain, model=model, dry_run=dry_run)
        log.info("Changes needed: %s", results["evolve_distiller"].get("changes_needed", False))
    except Exception as e:
        log.warning("Stage 4 failed (continuing): %s", e)
        results["evolve_distiller"] = {"error": str(e)[:300]}

    # Stage 5
    log.info("\n--- Stage 5: Evolve Agent Patterns ---")
    try:
        results["evolve_agent"] = evolve_agent(domain, model=model, dry_run=dry_run)
    except Exception as e:
        log.warning("Stage 5 failed (continuing): %s", e)
        results["evolve_agent"] = {"error": str(e)[:300]}
    log.info("Patterns: %d winning, %d combos",
             len(results["evolve_agent"].get("winning_patterns", [])),
             len(results["evolve_agent"].get("recommended_combos", [])))

    # Stage 6
    if not dry_run and collect_cycles > 0:
        log.info("\n--- Stage 6: Auto-Collect ---")
        try:
            results["auto_collect"] = auto_collect(domain, model=model, cycles=collect_cycles)
            log.info("Collected: %s", results["auto_collect"].get("collected", 0))
        except Exception as e:
            log.warning("Auto-collect failed: %s", e)
            results["auto_collect"] = {"error": str(e)}
    else:
        results["auto_collect"] = {"skipped": True}

    log.info("\n" + "=" * 60)
    log.info("SELF-EVOLUTION LOOP COMPLETE")
    log.info("=" * 60)

    return results
