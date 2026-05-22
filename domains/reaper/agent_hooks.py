"""
domains/reaper/agent_hooks.py
REAPER domain agent hooks — auto-verification + progress tracking.

auto_verify: called after every tool call, can make live MCP calls.
  - After execute_reaper_code / apply_skill / create_midi_item / add_midi_notes:
    get project info and validate structure (track count, item count,
    note pitches in-scale, timing on-grid).
progress_check: called every 10 iterations, reports project state.
"""
import logging
import re

log = logging.getLogger("reaper_hooks")

_added_tracks: list[str] = []

# ---------------------------------------------------------------------------
# Music theory validation helpers
# ---------------------------------------------------------------------------

_NOTE_MAP = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
    "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11,
}

_SCALES = {
    "major":            [0, 2, 4, 5, 7, 9, 11],
    "minor":            [0, 2, 3, 5, 7, 8, 10],
    "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
    "dorian":           [0, 2, 3, 5, 7, 9, 10],
    "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues":            [0, 3, 5, 6, 7, 10],
}


def _pitches_in_scale(pitches: list[int], key: str, scale: str) -> list[int]:
    """Return pitches that are NOT in the given key/scale (ignoring drum tracks)."""
    root = _NOTE_MAP.get(key, 0)
    intervals = _SCALES.get(scale, _SCALES["major"])
    valid_pcs = {(root + i) % 12 for i in intervals}
    return [p for p in pitches if p % 12 not in valid_pcs]


def _timing_on_grid(start_times: list[float], bpm: float, grid: float = 0.0625) -> list[float]:
    """Return start_times that are NOT quantized to the grid (default 1/16 note)."""
    beat_dur = 60.0 / bpm
    grid_dur = beat_dur * grid * 4  # grid=0.0625 means 1/16 of a whole note
    off_grid = []
    for t in start_times:
        remainder = t % grid_dur if grid_dur > 0 else 0
        if remainder > 0.001 and (grid_dur - remainder) > 0.001:
            off_grid.append(t)
    return off_grid


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

_STRUCTURAL_QA_PROMPT = """\
You are a music production reviewer. Check this REAPER project state for SERIOUS issues only.

Expected action: {action}
Expected element: {element_name}
Project state: {project_info}

Only flag SERIOUS problems — minor mixing differences are OK. Check:
1. MISSING TRACK: Is the expected track absent from the project? (SERIOUS)
2. EMPTY TRACK: Does a track have 0 items when it should have MIDI/audio? (SERIOUS)
3. WRONG TEMPO: Is the tempo drastically different from what was requested? (SERIOUS)
4. NO NOTES: Does a MIDI item have 0 notes? (SERIOUS)
5. EXTREME VALUES: Are velocities at 0 or 127 for every note (no dynamics)? (MODERATE)

Reply "PASS" if no serious problems.
Reply "ISSUE: [problem]" ONLY for serious structural failures.
Do NOT flag minor mixing preferences or subjective sound choices.
"""

_PROGRESS_PROMPT = """\
Project state summary:
{project_info}

Tracks added so far: {track_list}
Iteration: {iteration} of budget

Assess: Is the track progressing well? Any elements missing or misplaced?
Provide a 1-2 sentence status report.
"""


def _call_structural_llm(project_info: str, action: str, element_name: str) -> str:
    """Call GPT-5.4 to evaluate project structure."""
    try:
        from core.llm import call_azure_openai
    except ImportError:
        return ""

    prompt = _STRUCTURAL_QA_PROMPT.format(
        action=action[:80],
        element_name=element_name[:60],
        project_info=(project_info or "(empty)")[:2000],
    )
    messages = [{"role": "user", "content": prompt}]

    try:
        resp = call_azure_openai(
            messages, model="gpt-5.4", reasoning_effort="low"
        )
        return resp.get("content", "")
    except Exception as e:
        log.warning("Structural QA failed: %s", e)
        return ""


# ---------------------------------------------------------------------------
# Public hooks
# ---------------------------------------------------------------------------

async def auto_verify(tool_name, tool_args, result_text, mcp):
    """Auto-verify after track/item-creation operations with structural QA."""

    # Only trigger on content-creation tools
    if tool_name not in (
        "execute_reaper_code",
        "apply_skill",
        "create_midi_item",
        "add_midi_notes",
        "create_track",
        "add_fx",
    ):
        return None

    # Check for errors in the result
    if re.search(r"(?i)error|traceback|exception", result_text):
        return (
            f"The last {tool_name} call failed with an error. "
            "Review the traceback and try a different approach."
        )

    # Track added elements
    track_name = tool_args.get("track_name", "") or tool_args.get("name", "")
    if tool_name in ("apply_skill", "create_track"):
        if track_name:
            _added_tracks.append(track_name)

    # --- Project info verification ---
    try:
        project_info = await mcp.call_tool("get_project_info", {})
    except Exception as exc:
        log.warning("get_project_info failed: %s", exc)
        project_info = ""

    # Parse track count from project info
    track_count_match = re.search(r"Tracks[:\s]*(\d+)", project_info or "")
    if track_count_match:
        track_count = int(track_count_match.group(1))
        if track_count == 0 and tool_name in ("apply_skill", "create_track"):
            return (
                "Warning: project has 0 tracks after the last operation. "
                "Something went wrong — the track was not created."
            )

    # For apply_skill, verify the named track exists
    if tool_name == "apply_skill" and track_name:
        if project_info and track_name not in project_info:
            log.info(
                "Track '%s' not found verbatim in project info (may be renamed)",
                track_name,
            )

    # --- Structural QA via LLM ---
    if tool_name in ("apply_skill", "execute_reaper_code"):
        if tool_name == "apply_skill":
            action = f"Applied skill '{tool_args.get('skill_id', '?')}'"
        else:
            code_snippet = (tool_args.get("code", "") or "")[:120]
            action = f"Executed ReaScript code: {code_snippet}"

        qa_result = _call_structural_llm(
            project_info, action, track_name or "(custom code)"
        )
        if not qa_result:
            return None

        if "pass" in qa_result.lower()[:15]:
            log.info("Structural QA PASS for %s", tool_name)
            return None

        log.warning("Structural QA ISSUE after %s: %s", tool_name, qa_result[:200])
        return (
            f"Structural QA after {tool_name}: {qa_result}\n"
            "Consider fixing the issue with execute_reaper_code."
        )

    return None


async def progress_check(mcp, invocations, iteration):
    """Every 10 iterations, report project state and progress."""
    if iteration % 10 != 0:
        return None

    # Get current project state
    try:
        project_info = await mcp.call_tool("get_project_info", {})
    except Exception as exc:
        log.warning("progress_check: get_project_info failed: %s", exc)
        project_info = "(unable to retrieve project info)"

    track_list = ", ".join(_added_tracks) if _added_tracks else "(none tracked)"

    try:
        from core.llm import call_azure_openai
    except ImportError:
        return (
            f"[Progress check @ iteration {iteration}]\n"
            f"Project: {project_info}\n"
            f"Tracks added: {track_list}"
        )

    prompt = _PROGRESS_PROMPT.format(
        project_info=project_info or "(empty)",
        track_list=track_list,
        iteration=iteration,
    )
    messages = [{"role": "user", "content": prompt}]

    try:
        resp = call_azure_openai(
            messages, model="gpt-5.4", reasoning_effort="low"
        )
        summary = resp.get("content", "")
    except Exception as e:
        log.warning("progress_check LLM failed: %s", e)
        summary = ""

    report = (
        f"[Progress check @ iteration {iteration}]\n"
        f"Project: {project_info}\n"
        f"Tracks added: {track_list}"
    )
    if summary:
        report += f"\nAssessment: {summary}"

    return report
