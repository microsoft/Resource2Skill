"""
domains/reaper/mcp_server/server.py
Unified REAPER MCP Server — skill library + headless music production.

Headless architecture (no GUI REAPER needed):
  - In-memory project model: tracks → MIDI instruments → notes
  - pretty_midi for MIDI generation
  - fluidsynth for MIDI→WAV rendering (GM SoundFont)
  - Generates .mid + .wav + .rpp files

Tools:
  Skill library:
    list_skills, search_skills, get_skill_info, get_skill_text,
    get_skill_code, get_skill_visual

  Music production:
    execute_reaper_code   — run Python code against the in-memory project
    get_project_info      — project state (tempo, tracks, notes)
    create_track          — add a named track
    create_midi_item      — (implicit, tracks hold notes directly)
    add_midi_notes        — insert MIDI notes into a track
    set_tempo             — set project tempo
    add_fx                — record FX metadata (rendered via SoundFont)
    arrange_project_sections — extend patterns + create intro/breakdown/final dynamics
    apply_skill           — execute skill code
    render_project        — MIDI→WAV via fluidsynth
    save_project          — save .mid + .rpp to demo/reaper/

Usage (stdio transport):
    python domains/reaper/mcp_server/server.py --skills-dir skills_library/reaper
"""
from __future__ import annotations

import argparse
import io
import json
import logging
import os
import re
import shutil
import subprocess
import sys
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

log = logging.getLogger("reaper-mcp")

# ---------------------------------------------------------------------------
# In-memory project model
# ---------------------------------------------------------------------------

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def _note_name(pitch: int) -> str:
    return f"{NOTE_NAMES[pitch % 12]}{pitch // 12 - 1}"


class Track:
    """In-memory track holding MIDI notes and metadata."""

    def __init__(self, name: str, program: int = 0, is_drum: bool = False, channel: int = 0):
        self.name = name
        self.program = program  # GM program number
        self.is_drum = is_drum
        self.channel = channel
        self.notes: list[dict] = []  # {pitch, start_time, duration, velocity}
        self.fx: list[str] = []
        self.volume: float = 1.0
        self.pan: float = 0.0  # -1.0 left to 1.0 right

    def info(self, index: int) -> str:
        note_count = len(self.notes)
        fx_str = f" FX=[{', '.join(self.fx)}]" if self.fx else ""
        drum_str = " [DRUMS]" if self.is_drum else f" [GM:{self.program}]"
        if note_count > 0:
            pitches = [n["pitch"] for n in self.notes]
            return (
                f"  - [{index}] {self.name}{drum_str} "
                f"{note_count} notes "
                f"(range: {_note_name(min(pitches))}-{_note_name(max(pitches))})"
                f"{fx_str}"
            )
        return f"  - [{index}] {self.name}{drum_str} 0 notes{fx_str}"


class Project:
    """In-memory REAPER project."""

    def __init__(self):
        self.name = "Untitled"
        self.bpm: float = 120.0
        self.time_sig_num: int = 4
        self.time_sig_den: int = 4
        self.tracks: list[Track] = []

    @property
    def beat_duration(self) -> float:
        return 60.0 / self.bpm

    @property
    def bar_duration(self) -> float:
        return self.beat_duration * self.time_sig_num

    @property
    def length_beats(self) -> float:
        if not self.tracks:
            return 0
        max_end = 0
        for t in self.tracks:
            for n in t.notes:
                end = n["start_time"] + n["duration"]
                if end > max_end:
                    max_end = end
        return max_end

    @property
    def length_seconds(self) -> float:
        return self.length_beats * self.beat_duration

    def to_pretty_midi(self):
        import pretty_midi
        pm = pretty_midi.PrettyMIDI(initial_tempo=self.bpm)

        for track in self.tracks:
            # Auto-detect drum tracks that weren't explicitly marked
            if not track.is_drum:
                name_lower = track.name.lower()
                drum_kw = ("drum", "kick", "snare", "hat", "perc", "cymbal",
                           "boom bap", "trap groove", "breakbeat")
                if any(kw in name_lower for kw in drum_kw):
                    track.is_drum = True
                    track.channel = 9

            inst = pretty_midi.Instrument(
                program=track.program,
                is_drum=track.is_drum,
                name=track.name,
            )
            for n in track.notes:
                start_sec = n["start_time"] * self.beat_duration
                end_sec = start_sec + n["duration"] * self.beat_duration
                inst.notes.append(pretty_midi.Note(
                    velocity=n["velocity"],
                    pitch=n["pitch"],
                    start=start_sec,
                    end=end_sec,
                ))
            pm.instruments.append(inst)

        return pm


# Global project instance
_project = Project()


def _get_engine():
    global _engine
    if not _engine:
        import reaper_engine
        _engine = reaper_engine
    return _engine


_engine = None

# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------

_skills_dir: Path | None = None
_skill_index: list[dict] | None = None
_skill_metadata: dict | None = None
_demo_dir: Path = _PROJECT_ROOT / "demo" / "reaper"
_soundfont_path: str = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
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
        domain="reaper",
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
            "domain": "reaper",
            "bpm": _project.bpm,
            "track_count": len(_project.tracks),
            "groundings": _skill_groundings,
        },
        domain="reaper",
    )
    return str(path)


def _ensure_skills_loaded():
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
    global _skill_index, _skill_metadata
    _skill_index = None
    _skill_metadata = None
    _ensure_skills_loaded()


# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("reaper-mcp")


# Server-owned reload_registry — exempt from the legacy stale guard so the
# documented stale_registry remediation path is real on this hybrid server.
@mcp.tool()
def reload_registry() -> dict:
    """Refresh the wiki discovery surface from disk and re-key the stale guard."""
    info: dict = {"reloaded": True, "domain": "reaper"}
    try:
        from domains.reaper.wiki_adapter import ReaperWikiAdapter
        from core.skill_wiki.mcp_tools import register_wiki_tools
        from core.skill_wiki.legacy_stale import mark_runtime_backend
        from core import get_active_library_backend
        register_wiki_tools(mcp, ReaperWikiAdapter())
        backend = get_active_library_backend("reaper")
        mark_runtime_backend(mcp, backend)
        info["backend"] = backend
        info["tool_surface"] = "wiki+legacy"
    except Exception as exc:  # noqa: BLE001
        info["error"] = f"{type(exc).__name__}: {exc}"
    return info


# ===== Music Production Tools =====

@mcp.tool()
def execute_reaper_code(
    code: str,
    from_skill_ids: str = "",
    target_node: str = "",
    adaptation_notes: str = "",
) -> str:
    """Execute Python code against the in-memory project.

The code has access to the `project` object (Project instance with
tracks, notes, tempo) and `pretty_midi` module. Skills that use
`import reaper_python as RPR` are also supported via a shim layer.

Args:
    code: Python code to execute.
    from_skill_ids: optional JSON/comma list of inspected wiki skill ids whose
        musical/code mechanisms this generated code adapts.
    target_node: optional musical role target, or JSON/comma list for multiple
        grounded roles (e.g. drums,bass,harmony,fx).
    adaptation_notes: optional note describing borrowed mechanisms.

Returns:
    Captured stdout output, or error traceback on failure.
"""
    import pretty_midi
    import reaper_shim

    # Bind shim to our project and reset its internal state
    reaper_shim.bind_project(_project)
    reaper_shim._reset()

    # Register the shim as the `reaper_python` module so skills can import it
    sys.modules["reaper_python"] = reaper_shim

    old_stdout = sys.stdout
    captured = io.StringIO()
    sys.stdout = captured

    try:
        exec(
            compile(code, "<agent-code>", "exec"),
            {
                "project": _project,
                "Track": Track,
                "pretty_midi": pretty_midi,
                "__builtins__": __builtins__,
            },
        )
        output = captured.getvalue()
        entries = _append_groundings(
            tool_name="execute_reaper_code",
            from_skill_ids=from_skill_ids,
            target_node=target_node,
            adaptation_notes=adaptation_notes,
            fallback_target=target_node or "arrangement_code",
            extra={"code_chars": len(code)},
        )
        suffix = f"\ngrounded_sections={len(entries)}" if entries else ""
        return (output if output.strip() else "Code executed successfully (no output)") + suffix
    except Exception:
        output = captured.getvalue()
        tb = traceback.format_exc()
        return f"{output}\nError:\n{tb}" if output else f"Error:\n{tb}"
    finally:
        sys.stdout = old_stdout


@mcp.tool()
def get_project_info() -> str:
    """Get information about the current project.

Returns:
    Project name, tempo, time signature, track list with note counts.
"""
    p = _project
    lines = [
        f"Project: {p.name}",
        f"Tempo: {p.bpm:.1f} BPM",
        f"Time Sig: {p.time_sig_num}/{p.time_sig_den}",
        f"Length: {p.length_beats:.1f} beats ({p.length_seconds:.1f}s)",
        f"Tracks ({len(p.tracks)}):",
    ]
    for i, track in enumerate(p.tracks):
        lines.append(track.info(i))

    total_notes = sum(len(t.notes) for t in p.tracks)
    lines.append(f"Total notes: {total_notes}")
    return "\n".join(lines)


@mcp.tool()
def create_track(
    name: str,
    program: int = 0,
    is_drum: bool = False,
) -> str:
    """Create a new MIDI track.

Args:
    name: Track name.
    program: General-MIDI program number (0-127). Ignored for drum tracks.
    is_drum: If True, track uses the GM drum map (channel 10).

Returns:
    Confirmation with track index.
"""
    channel = 9 if is_drum else len([t for t in _project.tracks if not t.is_drum]) % 15
    if channel >= 9 and not is_drum:
        channel += 1  # Skip channel 10 (drums)
    track = Track(name=name, program=program, is_drum=is_drum, channel=channel)
    _project.tracks.append(track)
    idx = len(_project.tracks) - 1
    gm_str = "GM Drums" if is_drum else f"GM program {program}"
    return f"Created track '{name}' at index {idx} ({gm_str})"


@mcp.tool()
def add_midi_notes(
    track_index: int,
    notes: list[dict],
) -> str:
    """Add MIDI notes to a track.

Each note is {pitch, start_time, duration, velocity} where
start_time and duration are in BEATS (not seconds).

Args:
    track_index: Track index (0-based).
    notes: Array of note objects. Each: {pitch: 0-127, start_time: float (beats),
           duration: float (beats), velocity: 0-127}.

Returns:
    Confirmation with note count and pitch range.
"""
    if track_index < 0 or track_index >= len(_project.tracks):
        return f"Error: track index {track_index} out of range (0-{len(_project.tracks) - 1})"

    track = _project.tracks[track_index]
    pitches = []
    velocities = []

    for note in notes:
        pitch = int(note["pitch"])
        start = float(note["start_time"])
        dur = float(note["duration"])
        vel = int(note.get("velocity", 100))
        track.notes.append({
            "pitch": pitch,
            "start_time": start,
            "duration": dur,
            "velocity": max(1, min(127, vel)),
        })
        pitches.append(pitch)
        velocities.append(vel)

    lo_name = _note_name(min(pitches)) if pitches else "?"
    hi_name = _note_name(max(pitches)) if pitches else "?"

    return (
        f"Added {len(notes)} MIDI notes to track [{track_index}] '{track.name}' "
        f"(pitches: {lo_name}-{hi_name}, velocities: {min(velocities)}-{max(velocities)})"
    )


@mcp.tool()
def set_tempo(bpm: float) -> str:
    """Set the project tempo.

Args:
    bpm: Tempo in BPM (30-300).

Returns:
    Confirmation.
"""
    bpm = max(30, min(300, bpm))
    _project.bpm = bpm
    return f"Tempo set to {bpm:.1f} BPM (beat = {_project.beat_duration:.3f}s)"


@mcp.tool()
def add_fx(track_index: int, fx_name: str) -> str:
    """Record an FX plugin on a track (metadata only — rendering uses GM SoundFont).

Args:
    track_index: Track index.
    fx_name: Plugin name string.

Returns:
    Confirmation.
"""
    if track_index < 0 or track_index >= len(_project.tracks):
        return f"Error: track index {track_index} out of range"

    track = _project.tracks[track_index]
    track.fx.append(fx_name)
    return f"Added FX '{fx_name}' to track [{track_index}] '{track.name}' (metadata recorded)"


@mcp.tool()
def arrange_project_sections(
    total_bars: int = 24,
    pattern_bars: int = 8,
    style: str = "auto",
) -> str:
    """Turn skill-generated loops into a full arrangement.

    Skills often generate strong 4-8 bar role patterns but leave the final
    spectrogram too static. This tool repeats each role across the full form
    and applies deterministic section dynamics:

    - intro: reduced velocity and lighter drums
    - main: full pattern
    - breakdown: sparse drums / lighter bass
    - final: full pattern plus fills / stronger melodic accents

    Args:
        total_bars: target song length in 4/4 bars.
        pattern_bars: source loop length to repeat from each track.
        style: optional label for the report only.
    """
    total_bars = max(8, min(96, int(total_bars or 24)))
    pattern_bars = max(2, min(total_bars, int(pattern_bars or 8)))
    beats_per_bar = _project.time_sig_num or 4
    target_beats = float(total_bars * beats_per_bar)
    pattern_beats = float(pattern_bars * beats_per_bar)
    if not _project.tracks:
        return "Error: project has no tracks to arrange"

    added = 0
    adjusted = 0
    tracks_changed: list[str] = []
    for track in _project.tracks:
        if not track.notes:
            continue
        # Use the earliest pattern window as the role's source phrase.
        source = [
            dict(n) for n in track.notes
            if float(n.get("start_time", 0.0)) < pattern_beats
        ]
        if not source:
            source = [dict(n) for n in track.notes[:64]]
        existing = {
            (
                int(n.get("pitch", 0)),
                round(float(n.get("start_time", 0.0)), 3),
                round(float(n.get("duration", 0.0)), 3),
            )
            for n in track.notes
        }
        offset = pattern_beats
        while offset < target_beats - 0.01:
            for n in source:
                start = float(n.get("start_time", 0.0))
                rel = start % pattern_beats
                new_start = offset + rel
                dur = min(float(n.get("duration", 0.25)), max(0.05, target_beats - new_start))
                if new_start >= target_beats or dur <= 0:
                    continue
                key = (int(n.get("pitch", 0)), round(new_start, 3), round(dur, 3))
                if key in existing:
                    continue
                track.notes.append({
                    "pitch": int(n.get("pitch", 60)),
                    "start_time": new_start,
                    "duration": dur,
                    "velocity": int(n.get("velocity", 92)),
                })
                existing.add(key)
                added += 1
            offset += pattern_beats

        name_lower = track.name.lower()
        is_drum_role = track.is_drum or any(k in name_lower for k in ("drum", "kick", "snare", "hat", "perc", "break"))
        is_bass_role = any(k in name_lower for k in ("bass", "808", "sub"))
        is_lead_role = any(k in name_lower for k in ("lead", "melody", "hook", "synth", "vocal"))

        arranged_notes = []
        for n in track.notes:
            start = float(n.get("start_time", 0.0))
            if start >= target_beats:
                continue
            bar = int(start // beats_per_bar)
            vel = int(n.get("velocity", 92))
            keep = True
            # Intro: lighter energy, hats/percussion sparse.
            if bar < max(2, total_bars // 6):
                vel = int(vel * (0.58 if is_drum_role else 0.72))
                if is_drum_role and (bar % 2 == 1) and int(start * 4) % 2 == 1:
                    keep = False
            # Breakdown: remove some drums/bass so the spectrogram visibly thins.
            elif total_bars // 2 <= bar < total_bars // 2 + max(2, total_bars // 6):
                if is_drum_role and int(start * 4) % 3 == 0:
                    keep = False
                if is_bass_role and bar % 2 == 1:
                    vel = int(vel * 0.45)
                else:
                    vel = int(vel * 0.72)
            # Final section: stronger energy.
            elif bar >= int(total_bars * 0.72):
                vel = min(124, int(vel * 1.12) + 6)
            if keep:
                nn = dict(n)
                nn["velocity"] = max(18, min(127, vel))
                arranged_notes.append(nn)
                adjusted += 1
        track.notes = arranged_notes

        # Add short role-specific fills at section boundaries.
        boundaries = [
            max(2, total_bars // 6),
            total_bars // 2,
            total_bars // 2 + max(2, total_bars // 6),
            int(total_bars * 0.72),
        ]
        for b in boundaries:
            base = b * beats_per_bar - 1.0
            if base < 0 or base >= target_beats:
                continue
            if is_drum_role:
                fill_pitch = 38 if track.is_drum else int(track.notes[0].get("pitch", 60))
                for j in range(4):
                    track.notes.append({
                        "pitch": fill_pitch if j % 2 == 0 else 42,
                        "start_time": base + j * 0.25,
                        "duration": 0.12,
                        "velocity": min(124, 88 + j * 8),
                    })
                    added += 1
            elif is_lead_role and track.notes:
                seed = track.notes[0]
                pitch = min(96, int(seed.get("pitch", 72)) + 12)
                track.notes.append({
                    "pitch": pitch,
                    "start_time": base,
                    "duration": 0.75,
                    "velocity": 96,
                })
                added += 1
        tracks_changed.append(track.name)

    _project.tracks.sort(key=lambda t: (
        0 if t.is_drum or any(k in t.name.lower() for k in ("kick", "drum")) else
        1 if any(k in t.name.lower() for k in ("bass", "808", "sub")) else
        2 if any(k in t.name.lower() for k in ("chord", "pad", "piano", "keys")) else
        3
    ))
    total_notes = sum(len(t.notes) for t in _project.tracks)
    return (
        f"Arranged {len(tracks_changed)} tracks into {total_bars} bars "
        f"({target_beats:.0f} beats, style={style}); added {added} notes, "
        f"adjusted {adjusted} notes, total_notes={total_notes}. "
        "Sections: intro -> main -> breakdown -> final lift -> outro."
    )


# ===== Skill Library Tools =====

@mcp.tool()
def list_skills(category: str = "", query: str = "", verified_only: bool = False) -> str:
    """List or search skills in the REAPER music production skill library.

Args:
    category: Filter by category (e.g., 'drums', 'melody', 'chords', 'bass').
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
    """Get detailed information about a specific REAPER skill.

When the hybrid wiki registry is available, this inspects the wiki skill
including text/code/visual summaries. The universal wiki registrar owns
list_skills/search_skills/get_skill_text/get_skill_code/get_skill_visual/apply_skill,
but not get_skill_info, so this Reaper-local tool bridges that inspection
gap for wiki skill IDs.

Args:
    skill_id: The skill ID to look up.

Returns:
    Skill details: name, category, tags, scope, code preview.
"""
    try:
        from domains.reaper.wiki_adapter import ReaperWikiAdapter
        adapter = ReaperWikiAdapter()
        info = adapter.get_skill_info(skill_id)
        if "error" not in info:
            lines = [f"Skill: {info.get('skill_name') or skill_id}"]
            lines.append(f"  ID: {skill_id}")
            lines.append(f"  Tier: {info.get('tier', '?')}")
            lines.append(f"  Category Path: {'/'.join(info.get('category_path') or []) or '?'}")
            lines.append(f"  Exec OK: {info.get('exec_ok', '?')}")
            modalities = info.get("modalities_present") or []
            if modalities:
                lines.append(f"  Modalities: {', '.join(modalities)}")
            tags = info.get("tags") or []
            if tags:
                lines.append(f"  Tags: {', '.join(tags[:12])}")
            applicability = info.get("applicability")
            if applicability:
                lines.append(f"  Applicability: {applicability}")
            visual = info.get("visual") or {}
            if visual.get("path"):
                lines.append(f"  Visual: {visual.get('path')}")
            text_preview = (info.get("text_preview") or "").strip()
            if text_preview:
                lines.append(f"  Text preview:\n    {text_preview[:700].replace(chr(10), chr(10) + '    ')}")
            code_preview = (info.get("code_preview") or "").strip()
            if code_preview:
                lines.append(
                    f"  Code preview ({info.get('code_line_count', 0)} lines):\n"
                    f"    {code_preview[:1000].replace(chr(10), chr(10) + '    ')}"
                )
            return "\n".join(lines)
    except Exception as exc:  # noqa: BLE001
        log.debug("wiki get_skill_info failed for %s: %s", skill_id, exc)

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

    if meta:
        lines.append(f"  Scope: {meta.get('scope', '?')}")
        lines.append(f"  Complexity: {meta.get('complexity', '?')}")
        tags = meta.get("semantic_tags", [])
        if tags:
            lines.append(f"  Tags: {', '.join(tags)}")
        lines.append(f"  Exec OK: {meta.get('exec_ok', '?')}")

    analysis = detail.get("analysis", "")
    code = engine.extract_code_from_analysis(analysis)
    if code:
        preview = "\n".join(code.split("\n")[:8])
        lines.append(f"  Code preview:\n    {preview}")

    return "\n".join(lines)


@mcp.tool()
def get_skill_code(skill_id: str) -> str:
    """Get full Python code from a skill.

Args:
    skill_id: The skill ID to look up.

Returns:
    Full code with create_pattern() function and detected techniques.
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
    m = re.search(
        r'\*\*Core (?:Musical )?Mechanism\*\*[:\s]*(.+?)(?:\n\n|\n\*\*)',
        analysis, re.DOTALL,
    )
    if m:
        mechanism = m.group(1).strip()[:300]

    techniques = []
    if 'add_note' in code or 'notes' in code.lower():
        techniques.append('MIDI_NOTES')
    if any(kw in code.lower() for kw in ('fx', 'effect', 'eq', 'comp')):
        techniques.append('FX_CHAIN')
    if any(kw in code.lower() for kw in ('chord', 'voicing', 'progression')):
        techniques.append('HARMONY')
    if any(kw in code.lower() for kw in ('kick', 'snare', 'hihat', 'drum')):
        techniques.append('DRUMS')

    lines = [f"# Skill Reference: {name}"]
    if mechanism:
        lines.append(f"\n## Musical Mechanism\n{mechanism}")
    if techniques:
        lines.append(
            f"\n## Detected Techniques\n" + "\n".join(f"- {t}" for t in techniques)
        )
    lines.append(f"\n## Full Code ({len(code.splitlines())} lines)\n```python\n{code}\n```")
    return "\n".join(lines)


@mcp.tool()
def apply_skill(
    skill_id: str,
    track_name: str = "",
    bpm: int = 0,
    key: str = "",
    scale: str = "",
    bars: int = 4,
) -> str:
    """Execute a skill's create_pattern() code to add a musical element.

Args:
    skill_id: Skill ID from list_skills.
    track_name: Override the default track name.
    bpm: Override tempo (0 = use project tempo).
    key: Musical key (e.g., 'C', 'A', 'F#').
    scale: Scale type (e.g., 'minor', 'dorian', 'pentatonic_minor').
    bars: Number of bars to generate (default: 4).

Returns:
    Names of newly created tracks/items, or error message.
"""
    _ensure_skills_loaded()
    engine = _get_engine()
    detail = engine.get_skill_detail(_skills_dir, skill_id, _skill_index or [])
    if not detail:
        return f"Error: skill '{skill_id}' not found"

    code = engine.extract_code_from_analysis(detail.get("analysis", ""))
    if not code:
        return f"Error: no code found in skill '{skill_id}'"

    params = {"bars": bars}
    if track_name:
        params["track_name"] = track_name
    if bpm > 0:
        params["bpm"] = bpm
    if key:
        params["key"] = key
    if scale:
        params["scale"] = scale

    wrapped = engine.wrap_skill_for_reaper(code, params)
    skill_name = detail.get("skill_name", skill_id)

    result = execute_reaper_code(wrapped)

    success, track_names = engine.parse_skill_result(result)
    if success:
        _append_groundings(
            tool_name="apply_skill",
            from_skill_ids=[skill_id],
            target_node=track_name or ", ".join(track_names) or skill_id,
            adaptation_notes=f"direct music skill; bpm={bpm or _project.bpm}; key={key}; scale={scale}; bars={bars}",
            extra={"skill_name": skill_name},
        )
    if success and track_names:
        return f"Applied skill '{skill_name}': {', '.join(track_names)}\n{result}"
    elif success:
        return f"Skill '{skill_name}' executed (check project for new elements)\n{result}"
    else:
        return f"Skill '{skill_name}' failed:\n{result}"


@mcp.tool()
def render_project(
    output_name: str = "render",
    sample_rate: int = 44100,
    style: str = "auto",
) -> str:
    """Render the current project to a WAV file.

Args:
    output_name: Filename (without extension).
    sample_rate: Sample rate in Hz.
    style: Audio post-processing style preset name.

Returns:
    Path to the rendered audio file + duration info.
"""
    if not _project.tracks:
        return "Error: project has no tracks. Add some music first."

    total_notes = sum(len(t.notes) for t in _project.tracks)
    if total_notes == 0:
        return "Error: project has tracks but no notes. Add notes first."

    # Create dated subfolder: demo/reaper/<output_name>_YYYYMMDD_HHMM/
    from datetime import datetime as _dt
    ts = _dt.now().strftime("%Y%m%d_%H%M")
    sub_dir = _demo_dir / f"{output_name}_{ts}"
    sub_dir.mkdir(parents=True, exist_ok=True)
    midi_path = str(sub_dir / f"{output_name}.mid")
    wav_path = str(sub_dir / f"{output_name}.wav")

    # Generate MIDI
    try:
        pm = _project.to_pretty_midi()
        pm.write(midi_path)
    except Exception as e:
        return f"Error generating MIDI: {e}"

    # Find soundfont
    sf_path = _soundfont_path
    if not os.path.exists(sf_path):
        # Try alternative paths
        for alt in [
            "/usr/share/sounds/sf2/default-GM.sf2",
            "/usr/share/soundfonts/FluidR3_GM.sf2",
        ]:
            if os.path.exists(alt):
                sf_path = alt
                break
        else:
            return (
                f"Error: no GM SoundFont found. MIDI saved to {midi_path}. "
                "Install fluid-soundfont-gm: sudo apt install fluid-soundfont-gm"
            )

    # Render with fluidsynth
    if not shutil.which("fluidsynth"):
        return (
            f"MIDI saved to {midi_path} but fluidsynth not found. "
            "Install: sudo apt install fluidsynth"
        )

    try:
        cmd = [
            "fluidsynth",
            "-ni",           # no interactive, no MIDI input
            sf_path,
            midi_path,
            "-F", wav_path,  # output file
            "-r", str(sample_rate),
            "-g", "0.5",     # gain (avoid clipping)
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            return f"fluidsynth error:\n{result.stderr[:500]}"

        if os.path.exists(wav_path):
            # --- Audio post-processing ---
            fx_style = style
            if fx_style == "auto":
                # Detect style from track names
                names_lower = " ".join(t.name.lower() for t in _project.tracks)
                if any(kw in names_lower for kw in ("soul", "kanye", "gospel", "chipmunk", "808")):
                    fx_style = "kanye_soul"
                elif any(kw in names_lower for kw in ("lofi", "lo-fi", "chill", "vinyl")):
                    fx_style = "lofi_hiphop"
                elif any(kw in names_lower for kw in ("synth", "retro", "wave", "neon")):
                    fx_style = "synthwave"
                else:
                    fx_style = "clean"

            try:
                import soundfile as sf
                import audio_fx
                audio_data, audio_sr = sf.read(wav_path)
                processed = audio_fx.apply_kanye_chain(audio_data, sr=audio_sr, style=fx_style)
                sf.write(wav_path, processed, audio_sr)
                fx_label = f", fx={fx_style}"
            except Exception as e:
                log.warning("Audio post-processing failed: %s", e)
                fx_label = ", fx=none (raw)"

            size_kb = os.path.getsize(wav_path) / 1024
            duration = _project.length_seconds
            manifest_path = _write_skill_manifest(wav_path)
            return (
                f"Rendered to {wav_path} ({size_kb:.0f} KB, "
                f"{sample_rate} Hz, {duration:.1f}s, {total_notes} notes{fx_label})\n"
                f"MIDI also saved to {midi_path}\n"
                f"skill_trace_manifest={manifest_path}"
            )
        return f"fluidsynth ran but no output at {wav_path}"
    except subprocess.TimeoutExpired:
        return "Error: fluidsynth timed out (60s)"
    except Exception as e:
        return f"Error rendering: {e}"


@mcp.tool()
def save_project(output_name: str = "my_track") -> str:
    """Save the project as MIDI file to demo/reaper/.

Args:
    output_name: Filename (without extension).

Returns:
    Path to the saved files.
"""
    if not _project.tracks:
        return "Error: project has no tracks"

    # Save into the most recent render subfolder, or create a new one
    from datetime import datetime as _dt
    recent_dirs = sorted(
        [d for d in _demo_dir.iterdir() if d.is_dir() and output_name in d.name],
        key=os.path.getmtime, reverse=True,
    ) if _demo_dir.exists() else []
    if recent_dirs:
        sub_dir = recent_dirs[0]
    else:
        ts = _dt.now().strftime("%Y%m%d_%H%M")
        sub_dir = _demo_dir / f"{output_name}_{ts}"
        sub_dir.mkdir(parents=True, exist_ok=True)

    midi_path = str(sub_dir / f"{output_name}.mid")

    try:
        pm = _project.to_pretty_midi()
        pm.write(midi_path)
        size_kb = os.path.getsize(midi_path) / 1024
        total_notes = sum(len(t.notes) for t in _project.tracks)
        manifest_path = _write_skill_manifest(midi_path)
        return (
            f"Saved project to {midi_path} ({size_kb:.0f} KB, "
            f"{len(_project.tracks)} tracks, {total_notes} notes); "
            f"skill_trace_manifest={manifest_path}"
        )
    except Exception as e:
        return f"Error saving project: {e}"


@mcp.tool()
def review_audio(
    wav_filename: str = "",
    style_target: str = "auto",
) -> str:
    """Review a rendered beat using Azure 4o/audio-capable analysis.

Sends a compact MP3 preview of the WAV file to an Azure audio-capable model
for musical quality assessment. Returns scores and specific actionable fixes.

Args:
    wav_filename: WAV file in demo/reaper/ to review (default: most recent render).
    style_target: Target style description (default: auto-detect from project).

Returns:
    Structured review with scores (1-10) and top 3 fixes.
"""
    # Find WAV file
    if wav_filename:
        wav_path = str(_demo_dir / wav_filename)
        if not wav_filename.endswith(".wav"):
            wav_path += ".wav"
        if not os.path.exists(wav_path) and not Path(wav_filename).is_absolute():
            matches = sorted(
                _demo_dir.glob(f"**/{Path(wav_path).name}"),
                key=os.path.getmtime,
                reverse=True,
            )
            if matches:
                wav_path = str(matches[0])
    else:
        # Find most recent WAV in demo dir, including render_project subfolders.
        wavs = sorted(_demo_dir.glob("**/*.wav"), key=os.path.getmtime, reverse=True)
        if not wavs:
            return "Error: no WAV files found in demo/reaper/. Render first."
        wav_path = str(wavs[0])

    if not os.path.exists(wav_path):
        return f"Error: file not found: {wav_path}"

    # Auto-detect style
    if style_target == "auto":
        names_lower = " ".join(t.name.lower() for t in _project.tracks)
        if any(kw in names_lower for kw in ("kanye", "soul", "chipmunk", "gospel")):
            style_target = "Kanye West Late Registration chipmunk soul hip-hop"
        elif any(kw in names_lower for kw in ("lofi", "lo-fi", "chill")):
            style_target = "lo-fi hip-hop chill beat"
        elif any(kw in names_lower for kw in ("synth", "retro", "wave")):
            style_target = "synthwave / retrowave"
        elif any(kw in names_lower for kw in ("trap", "808", "drill")):
            style_target = "modern trap / drill"
        else:
            style_target = "hip-hop beat"

    # Build section markers from project
    sections = []
    beat_dur = _project.beat_duration
    bar_dur = beat_dur * _project.time_sig_num
    total_bars = _project.length_beats / _project.time_sig_num if _project.time_sig_num else 0

    try:
        import audio_review
        result = audio_review.review_beat(
            wav_path,
            style_target=style_target,
            bpm=_project.bpm,
            sections=sections if sections else None,
            project=_project,
        )

        # Format for agent
        lines = [f"Audio Review for: {os.path.basename(wav_path)}"]
        lines.append(f"Target style: {style_target}")
        lines.append(f"")
        lines.append(f"Scores:")
        lines.append(f"  Style Match:  {result.get('style_match', '?')}/10")
        lines.append(f"  Rhythm:       {result.get('rhythm', '?')}/10")
        lines.append(f"  Harmony:      {result.get('harmony', '?')}/10")
        lines.append(f"  Bass:         {result.get('bass', '?')}/10")
        lines.append(f"  Arrangement:  {result.get('arrangement', '?')}/10")
        lines.append(f"  OVERALL:      {result.get('overall', '?')}/10")
        lines.append(f"")

        summary = result.get("summary", "")
        if summary:
            lines.append(f"Summary: {summary}")
            lines.append(f"")

        fixes = result.get("fixes", [])
        if fixes:
            lines.append(f"Top fixes to improve:")
            for i, fix in enumerate(fixes, 1):
                lines.append(f"  {i}. {fix}")

        return "\n".join(lines)
    except Exception as e:
        log.warning("Audio review failed: %s", e)
        return f"Error during audio review: {e}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Unified REAPER MCP Server")
    parser.add_argument("--skills-dir", default=None)
    parser.add_argument("--demo-dir", default=None,
                        help="Path to saved REAPER artifacts (default: <project>/demo/reaper).")
    args = parser.parse_args()

    global _skills_dir, _demo_dir
    if args.skills_dir:
        _skills_dir = Path(args.skills_dir).resolve()
    if args.demo_dir:
        _demo_dir = Path(args.demo_dir).resolve()
    _demo_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=logging.INFO)
    log.info("REAPER MCP starting (skills_dir=%s, demo_dir=%s, headless mode)", _skills_dir, _demo_dir)
    log.info(
        "Using pretty_midi + fluidsynth for headless rendering "
        "(no REAPER GUI needed)"
    )

    # Hybrid wiki discovery surface — wiki contract + thin legacy bridge.
    try:
        from domains.reaper.wiki_adapter import ReaperWikiAdapter
        from core.skill_wiki.mcp_tools import register_wiki_tools
        register_wiki_tools(mcp, ReaperWikiAdapter())
        log.info("Reaper MCP: registered universal wiki discovery surface")
    except Exception as exc:  # noqa: BLE001
        log.warning("Reaper MCP: failed to register wiki discovery surface: %s", exc)
    try:
        from core import get_active_library_backend
        from core.skill_wiki.legacy_stale import register_legacy_stale_check
        backend = get_active_library_backend("reaper")
        register_legacy_stale_check(mcp, domain="reaper", startup_backend=backend)
    except Exception as exc:  # noqa: BLE001
        log.warning("Reaper MCP: failed to install stale-registry guard: %s", exc)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
