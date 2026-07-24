"""
core/analyzer_cli_video.py

Keyless video analysis backend for Resource2Skill.

Used when ``R2S_VIDEO_BACKEND=cli`` is set. It replaces the Gemini native
YouTube-URL understanding with a local pipeline:

  1. yt-dlp downloads the video's auto-generated subtitles (VTT).
  2. ffmpeg extracts a small set of key frames from the video.
  3. A local agent CLI (currently Claude Code via core.llm_cli) reads the
     subtitle transcript + frame image paths and produces the same Markdown
     skill analysis that ``analyze_video`` would return.

The transcript parser handles YouTube's rolling-caption format by deduplicating
overlapping cue text, preserving timestamps so the model can map statements to
video moments.
"""
from __future__ import annotations

import glob
import json
import logging
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.analyzer import analyze_video

log = logging.getLogger("analyzer")

# ---------------------------------------------------------------------------
# Subtitle acquisition and parsing
# ---------------------------------------------------------------------------


def _run_ytdlp(*args, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run a yt-dlp command and return the result."""
    cmd = ["yt-dlp", *args]
    log.debug("yt-dlp command: %s", " ".join(cmd))
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _get_duration_sec(video_url: str) -> int:
    """Get video duration in seconds without downloading the video."""
    try:
        result = _run_ytdlp("--print", "duration", "--skip-download", "--quiet", video_url)
        if result.returncode == 0 and result.stdout.strip():
            return int(float(result.stdout.strip().splitlines()[0]))
    except Exception as e:
        log.warning("Could not determine video duration: %s", e)
    return 0


def _fetch_vtt(video_url: str, output_dir: Path, *, start_offset: str | None, end_offset: str | None) -> Path | None:
    """Download auto-generated subtitles; return the VTT file path or None."""
    # Prefer English, then any Chinese variant, then auto-detect by leaving a
    # fallback that accepts whatever yt-dlp can find.
    lang_list = ["en.*", "zh.*", "zh-Hans.*"]
    base = output_dir / "video"
    try:
        result = _run_ytdlp(
            "--write-auto-subs",
            "--write-subs",
            "--sub-langs", ",".join(lang_list),
            "--skip-download",
            "--sub-format", "vtt",
            "--convert-subs", "vtt",
            "--output", str(base) + ".%(ext)s",
            video_url,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        log.warning("yt-dlp subtitle fetch timed out")
        return None

    # yt-dlp names files like video.en.auto.vtt or video.zh-Hans.vtt
    candidates = sorted(glob.glob(str(base) + "*.vtt"))
    if not candidates:
        log.warning("No VTT subtitles found for %s", video_url)
        return None
    return Path(candidates[0])


def _parse_vtt(vtt_path: Path) -> str:
    """Parse a VTT file into a timestamped transcript with rolling dedup.

    YouTube auto-generated captions emit overlapping cues where cue N is often a
    suffix of cue N-1 plus a few new words. This function strips cue tags and
    merges the rolling window so each word appears only once.
    """
    text = vtt_path.read_text(encoding="utf-8", errors="ignore")

    # Strip WEBVTT header and any NOTE blocks / STYLE blocks.
    body = re.sub(r"WEBVTT[^\n]*\n", "", text, count=1)
    body = re.sub(r"(?m)^NOTE[\s\S]*?(?=\n\n|\n[A-Z0-9])", "", body)
    body = re.sub(r"(?m)^STYLE[\s\S]*?(?=\n\n|\n[A-Z0-9])", "", body)

    timing_re = re.compile(r"^(\d{1,2}:)?\d{1,2}:\d{2}(\.\d{3})?\s+-->")

    cues: list[tuple[int, str]] = []
    blocks = re.split(r"\n\s*\n", body)
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        # The timing line is the first line that looks like a cue arrow.
        timing_line: str | None = None
        for ln in lines:
            if timing_re.match(ln):
                timing_line = ln
                break
        if timing_line is None:
            continue
        # Cue body is everything after the timing line.
        idx = lines.index(timing_line)
        cue_body = "\n".join(lines[idx + 1:])
        # Strip cue tags like <v>, <c>, <lang>, positioning tags, and empty brackets.
        cue_body = re.sub(r"<[^>]+>", "", cue_body)
        cue_body = re.sub(r"\[\s*\]", "", cue_body)
        cue_body = " ".join(cue_body.split())
        if not cue_body:
            continue
        # Parse the start timestamp (first token on timing line).
        start_token = timing_line.split()[0]
        parts = start_token.split(":")
        try:
            if len(parts) == 2:
                mins = int(parts[0])
                secs = float(parts[1])
                start_sec = mins * 60 + int(secs)
            elif len(parts) == 3:
                hrs = int(parts[0])
                mins = int(parts[1])
                secs = float(parts[2])
                start_sec = hrs * 3600 + mins * 60 + int(secs)
            else:
                start_sec = 0
        except ValueError:
            continue
        cues.append((start_sec, cue_body))

    if not cues:
        return ""

    # Rolling dedup: build one continuous transcript by removing text that has
    # already appeared at the end of the previous cue.
    merged: list[str] = []
    prev = ""
    for sec, raw in cues:
        # Normalize for overlap detection
        a = prev.strip()
        b = raw.strip()
        # Case 1: new cue is a suffix of previous cue (YouTube rarely does this)
        if b and a.endswith(b):
            continue
        # Case 2: new cue starts with previous cue (common in rolling captions)
        if b.startswith(a):
            suffix = b[len(a):].strip()
            if suffix:
                merged.append(f"[{_fmt_time(sec)}] {suffix}")
                prev = b
            continue
        # Case 3: overlap smaller than full previous cue: find longest common
        # suffix/prefix match.
        overlap_len = 0
        for i in range(min(len(a), len(b)), 0, -1):
            if a.endswith(b[:i]):
                overlap_len = i
                break
        if overlap_len:
            suffix = b[overlap_len:].strip()
            if suffix:
                merged.append(f"[{_fmt_time(sec)}] {suffix}")
                prev = b
        else:
            merged.append(f"[{_fmt_time(sec)}] {b}")
            prev = b

    return "\n".join(merged)


def _fmt_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


# ---------------------------------------------------------------------------
# Frame extraction helper
# ---------------------------------------------------------------------------


def _uniform_timestamps(duration: int, n: int = 8) -> list[dict]:
    """Return n evenly spaced timestamps across the video."""
    if duration <= 0 or n <= 0:
        return []
    if n == 1:
        return [{"seconds": max(1, duration // 2), "description": "midpoint"}]
    return [
        {"seconds": int(duration * i / (n + 1)), "description": f"stage_{int(100*i/(n+1))}pct"}
        for i in range(1, n + 1)
    ]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def analyze_video_cli(
    video_url: str,
    *,
    prompt_path: str | Path | None = None,
    prompt_text: str | None = None,
    extra_instructions: str = "",
    start_offset: str | None = None,
    end_offset: str | None = None,
    max_frames: int = 6,
) -> str:
    """Analyze a video using only local tools and a local agent CLI."""
    from core.llm_cli import call_cli
    from core.analyzer import _load_prompt

    if prompt_text:
        text = prompt_text
    else:
        text = _load_prompt(prompt_path)
    if extra_instructions:
        text += "\n\n" + extra_instructions

    # Determine the effective time range so we can place frames correctly.
    start_sec = _parse_offset(start_offset) if start_offset else 0
    full_duration = _get_duration_sec(video_url)
    end_sec = _parse_offset(end_offset) if end_offset else full_duration
    effective_duration = max(0, end_sec - start_sec)
    log.info(
        "CLI video backend: duration=%ss, window=[%ss, %ss]",
        full_duration, start_sec, end_sec,
    )

    with tempfile.TemporaryDirectory(prefix="r2s_video_cli_") as tmpdir:
        tmp = Path(tmpdir)

        # 1. Subtitles
        transcript = ""
        vtt_path = _fetch_vtt(video_url, tmp, start_offset=start_offset, end_offset=end_offset)
        if vtt_path:
            transcript = _parse_vtt(vtt_path)
            log.info("Parsed transcript length: %d chars", len(transcript))
        else:
            log.warning("No subtitle transcript available; analysis will rely on frames only")

        # 2. Key frames (extract to the same temp dir)
        timestamps = _uniform_timestamps(effective_duration, n=max_frames)
        if start_sec:
            timestamps = [
                {"seconds": start_sec + ts["seconds"], "description": ts["description"]}
                for ts in timestamps
            ]
        # Imported here to avoid circular import at module load.
        from core.analyzer import extract_frames

        frames = extract_frames(video_url, timestamps, tmp, max_frames=max_frames) if timestamps else []
        log.info("Extracted %d frames", len(frames))

        # 3. Build prompt
        transcript_block = (
            "## Video Subtitle Transcript (timestamped)\n\n" + transcript
            if transcript
            else "## Video Subtitle Transcript\n\n[No subtitles available for this video.]"
        )
        frame_block = "## Key Frames Extracted\n\n"
        if frames:
            for f in frames:
                abs_path = str(tmp / f["path"])
                frame_block += f"- `{abs_path}` at t={_fmt_time(f['seconds'])} ({f['description']})\n"
            frame_block += (
                "\nRead the image files above to understand the visual state at each timestamp.\n"
            )
        else:
            frame_block += "[No frames extracted.]\n"

        user_prompt = (
            f"{text}\n\n{transcript_block}\n\n{frame_block}\n\n"
            "Produce the Markdown skill analysis following the instructions in the distiller prompt.\n"
            "Include the 'Key Frame Timestamps' table using the exact timestamps shown above."
        )

        system_prompt = (
            "You are a tutorial-to-skill distiller. You have access to a Read tool that can open local image files. "
            "Use it when the visual state matters. Return ONLY the Markdown analysis."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            msg = call_cli(messages, timeout=600)
            return msg.get("content", "")
        except Exception as e:
            log.error("CLI video analysis failed: %s", e)
            raise


def _parse_offset(offset: str) -> int:
    """Parse '120s' or '2m' or '1:30' into seconds."""
    offset = offset.strip().lower()
    # try explicit suffix
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(s|sec|m|min|h|hr)?$", offset)
    if m:
        value = float(m.group(1))
        unit = m.group(2) or "s"
        if unit in ("h", "hr"):
            return int(value * 3600)
        if unit in ("m", "min"):
            return int(value * 60)
        return int(value)
    # try h:mm:ss or m:ss
    parts = offset.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    raise ValueError(f"Cannot parse offset: {offset}")
