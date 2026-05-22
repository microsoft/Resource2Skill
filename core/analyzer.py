"""
core/analyzer.py
Gemini API wrapper: send a YouTube URL + domain-specific distiller prompt,
get back a structured skill analysis in Markdown.

Also handles key frame extraction from videos using yt-dlp + ffmpeg.
"""
from __future__ import annotations

import os
import re
import subprocess
import tempfile
import time
import logging
from pathlib import Path
from google import genai
from google.genai import types

log = logging.getLogger("analyzer")

# Models to try in order — if one hits rate limit, fall through to next.
MODEL_POOL = [
    "gemini-3.1-pro-preview",
    "gemini-2.5-pro",
    "gemini-2.5-pro-preview-03-25",
    "gemini-2.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite-preview",
]
DEFAULT_MODEL = MODEL_POOL[0]


def _load_prompt(path: Path | str | None = None) -> str:
    if path is None:
        raise ValueError("prompt_path is required. Pass the domain's distiller_prompt.md path.")
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Distiller prompt not found: {p}")
    return p.read_text(encoding="utf-8")


def _make_client(api_key: str | None = None) -> genai.Client:
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError(
            "Gemini API key required. Pass api_key= or set GEMINI_API_KEY env var."
        )
    return genai.Client(api_key=key)


def analyze_video(
    video_url: str,
    *,
    model: str = DEFAULT_MODEL,
    api_key: str | None = None,
    prompt_path: str | Path | None = None,
    prompt_text: str | None = None,
    extra_instructions: str = "",
    start_offset: str | None = None,
    end_offset: str | None = None,
) -> str:
    """Analyze a YouTube video and return a skill extraction in Markdown.

    Args:
        video_url: Public YouTube URL.
        model: Gemini model to use.
        api_key: Optional API key override.
        prompt_path: Path to a distiller prompt file.
        prompt_text: Direct prompt text (overrides prompt_path).
        extra_instructions: Additional text appended to the prompt.
        start_offset: Optional video start offset (e.g., "120s").
        end_offset: Optional video end offset (e.g., "300s").

    Returns:
        Raw Markdown analysis from the model.
    """
    client = _make_client(api_key)

    if prompt_text:
        text = prompt_text
    else:
        text = _load_prompt(prompt_path)

    if extra_instructions:
        text += "\n\n" + extra_instructions

    # Build the video part (with optional clipping).
    video_part_kwargs: dict = {
        "file_data": types.FileData(file_uri=video_url),
    }
    if start_offset or end_offset:
        video_part_kwargs["video_metadata"] = types.VideoMetadata(
            start_offset=start_offset or "0s",
            end_offset=end_offset,
        )
    video_part = types.Part(**video_part_kwargs)

    response = _call_with_retry(client, model, [video_part, types.Part(text=text)])
    return response.text


def _call_with_retry(client, model, parts, max_retries=3):
    """Call Gemini API with auto retry on 429 + model fallback."""
    models_to_try = [model] + [m for m in MODEL_POOL if m != model]

    for m in models_to_try:
        for attempt in range(max_retries):
            try:
                return client.models.generate_content(
                    model=m,
                    contents=types.Content(parts=parts),
                )
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    match = re.search(r"retry in ([\d.]+)s", err)
                    wait = float(match.group(1)) + 5 if match else 60
                    if attempt < max_retries - 1:
                        log.warning(f"Rate limited on {m} (attempt {attempt+1}), waiting {wait:.0f}s...")
                        time.sleep(wait)
                    else:
                        log.warning(f"{m} exhausted, trying next model...")
                        break
                else:
                    raise
    raise RuntimeError(f"All models exhausted: {models_to_try}")


# ---------------------------------------------------------------------------
# Key frame extraction from video analysis
# ---------------------------------------------------------------------------

def parse_timestamps(analysis_text: str) -> list[dict]:
    """Parse key frame timestamps from the analysis Markdown.

    Looks for the "### 0. Key Frame Timestamps" table.
    Returns list of {"seconds": int, "description": str}.
    """
    timestamps = []
    # Match table rows: | N | seconds | description |
    for m in re.finditer(
        r"\|\s*\d+\s*\|\s*(\d+(?:\.\d+)?)\s*\|\s*(.+?)\s*\|",
        analysis_text,
    ):
        seconds = int(float(m.group(1)))
        desc = m.group(2).strip()
        if desc.lower() not in ("e.g.", "timestamp (seconds)", "stage description", "---"):
            timestamps.append({"seconds": seconds, "description": desc})
    return timestamps


def extract_frames(
    video_url: str,
    timestamps: list[dict],
    output_dir: Path,
    *,
    max_frames: int = 8,
) -> list[dict]:
    """Download video and extract frames at specified timestamps.

    Args:
        video_url: YouTube video URL.
        timestamps: List of {"seconds": int, "description": str}.
        output_dir: Directory to save extracted frames.

    Returns:
        List of {"path": str, "seconds": int, "description": str} for successfully extracted frames.
    """
    if not timestamps:
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamps = timestamps[:max_frames]

    # Download video to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "video.mp4")
        log.info("Downloading video: %s", video_url)
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "-f", "bestvideo[height<=720][vcodec^=avc1]+bestaudio/best[height<=720][vcodec^=avc1]/bestvideo[height<=720]+bestaudio/best[height<=720]",
                    "--merge-output-format", "mp4",
                    "-S", "vcodec:h264",
                    "-o", video_path,
                    "--no-playlist",
                    "--quiet",
                    video_url,
                ],
                check=True,
                timeout=120,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            log.warning("Failed to download video: %s", e)
            return []

        if not os.path.exists(video_path):
            log.warning("Video file not found after download")
            return []

        # Extract frames at each timestamp
        frames = []
        for i, ts in enumerate(timestamps):
            sec = ts["seconds"]
            desc = ts["description"]
            slug = re.sub(r"[^a-z0-9]+", "_", desc.lower()).strip("_")[:30]
            frame_name = f"frame_{i:02d}_{slug}.jpg"
            frame_path = output_dir / frame_name

            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-ss", str(sec),
                        "-i", video_path,
                        "-frames:v", "1",
                        "-q:v", "2",
                        "-y",
                        str(frame_path),
                    ],
                    check=True,
                    timeout=30,
                    capture_output=True,
                )
                if frame_path.exists() and frame_path.stat().st_size > 0:
                    frames.append({
                        "path": frame_name,
                        "seconds": sec,
                        "description": desc,
                    })
                    log.info("Extracted frame %d/%d: t=%ds %s", i + 1, len(timestamps), sec, desc)
                else:
                    log.warning("Frame extraction produced empty file at t=%ds", sec)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                log.warning("Failed to extract frame at t=%ds: %s", sec, e)

    log.info("Extracted %d/%d frames to %s", len(frames), len(timestamps), output_dir)
    return frames


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Analyze a YouTube tutorial video.")
    ap.add_argument("url", help="Public YouTube video URL")
    ap.add_argument("--prompt", required=True, help="Path to distiller prompt file")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--start", default=None, help="Start offset, e.g. '60s'")
    ap.add_argument("--end", default=None, help="End offset, e.g. '300s'")
    ap.add_argument("-o", "--output", default=None, help="Save result to file")
    args = ap.parse_args()

    result = analyze_video(
        args.url,
        model=args.model,
        prompt_path=args.prompt,
        start_offset=args.start,
        end_offset=args.end,
    )

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Saved to {args.output}")
    else:
        print(result)
