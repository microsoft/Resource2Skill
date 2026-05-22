"""
domains/reaper/mcp_server/audio_review.py
Audio reflection via Azure 4o/audio-capable input.

We keep spectrogram rendering helpers for diagnostics, but the review score
listens to the rendered audio directly instead of sending a visual proxy to
GPT-5.4.
"""
from __future__ import annotations

import base64
import io
import logging
import os
import subprocess

import numpy as np

log = logging.getLogger("audio_review")

# Cached so matplotlib/librosa only load once
_LIBS_LOADED = False


def _ensure_libs():
    global _LIBS_LOADED
    if not _LIBS_LOADED:
        import matplotlib
        matplotlib.use("Agg")
        _LIBS_LOADED = True


def generate_spectrogram(
    wav_path: str,
    sections: list[tuple[float, float, str]] | None = None,
    bpm: float = 120,
) -> str:
    """Generate a spectrogram + waveform + onset visualization.

    Returns base64-encoded PNG string.
    """
    _ensure_libs()
    import matplotlib.pyplot as plt
    import librosa
    import librosa.display
    import soundfile as sf

    data, sr = sf.read(wav_path)
    mono = data.mean(axis=1) if data.ndim > 1 else data

    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    # 1. Mel spectrogram
    S = librosa.feature.melspectrogram(y=mono, sr=sr, n_mels=128, fmax=8000)
    S_dB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_dB, x_axis="time", y_axis="mel", sr=sr, fmax=8000, ax=axes[0])
    axes[0].set_title("Mel Spectrogram (frequency content)")
    axes[0].set_xlabel("")

    # 2. Waveform with sections
    times = np.arange(len(mono)) / sr
    axes[1].plot(times, mono, linewidth=0.3, color="#2196F3")
    axes[1].set_xlim(0, len(mono) / sr)
    axes[1].set_title("Waveform (energy)")
    axes[1].set_ylabel("Amplitude")

    if sections:
        colors = ["#FFC107", "#4CAF50", "#F44336", "#2196F3", "#9C27B0", "#FF9800"]
        for i, (s_t, e_t, name) in enumerate(sections):
            c = colors[i % len(colors)]
            axes[1].axvspan(s_t, e_t, alpha=0.15, color=c)
            mid = (s_t + e_t) / 2
            axes[1].text(mid, 0.8 * axes[1].get_ylim()[1], name, ha="center", fontsize=9, fontweight="bold")

    # 3. Onset strength
    onset_env = librosa.onset.onset_strength(y=mono, sr=sr)
    times_onset = librosa.times_like(onset_env, sr=sr)
    axes[2].plot(times_onset, onset_env, color="#E91E63", linewidth=0.8)
    axes[2].set_title("Rhythm / Onset Strength")
    axes[2].set_xlabel("Time (s)")
    axes[2].set_xlim(0, len(mono) / sr)

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("ascii")


def _structural_midi_analysis(project) -> str:
    """Analyze in-memory project for structural issues that spectrograms can't detect.

    Returns a text summary of problems found (empty if no issues).
    """
    if project is None:
        return ""

    issues = []
    track_summary = []

    for i, t in enumerate(project.tracks):
        n = len(t.notes)
        name = t.name
        is_drum = t.is_drum
        program = t.program

        track_summary.append(
            f"  [{i}] {name}: {n} notes, program={program}, is_drum={is_drum}"
        )

        # Check: drum-named track not marked as drum
        name_lower = name.lower()
        drum_kw = ("drum", "kick", "snare", "hat", "perc", "cymbal", "boom bap", "trap")
        if any(kw in name_lower for kw in drum_kw) and not is_drum:
            issues.append(
                f"CRITICAL: Track '{name}' sounds like drums but is_drum=False (program={program}). "
                f"Drum notes will play as piano! Set is_drum=True or use create_track(is_drum=True)."
            )

        # Check: empty tracks
        if n == 0 and "guide" not in name_lower and "marker" not in name_lower:
            issues.append(f"WARNING: Track '{name}' has 0 notes — is it intentionally silent?")

        # Check: melody/chords in wrong octave (too low or too high)
        if n > 0 and not is_drum:
            pitches = [note["pitch"] for note in t.notes]
            avg_pitch = sum(pitches) / len(pitches)
            if "bass" in name_lower and avg_pitch > 55:  # > G3
                issues.append(f"WARNING: Bass track '{name}' avg pitch={avg_pitch:.0f} seems too high for bass")
            if "chipmunk" in name_lower and avg_pitch < 72:  # < C5
                issues.append(f"WARNING: Chipmunk track '{name}' avg pitch={avg_pitch:.0f} — should be higher (octave 5-6+)")

    return "\n".join(track_summary + (["", "STRUCTURAL ISSUES:"] + issues if issues else []))


def _audio_review_models() -> list[str]:
    raw = (
        os.environ.get("VWS_REAPER_AUDIO_REVIEW_MODEL", "").strip()
        or os.environ.get("VWS_REAPER_AUDIO_SCORE_MODEL", "").strip()
    )
    if raw:
        models = [item.strip() for item in raw.split(",") if item.strip()]
        if models:
            return models
    return ["gpt-4o-audio-preview", "gpt-audio"]


def _prepare_audio_for_review(wav_path: str) -> tuple[str, dict]:
    """Transcode WAV to bounded mono MP3 and return base64 + metadata."""
    max_seconds = int(os.environ.get("VWS_REAPER_AUDIO_MAX_SECONDS", "240"))
    base, _ = os.path.splitext(wav_path)
    mp3_path = f"{base}.review.mp3"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if max_seconds > 0:
        cmd.extend(["-t", str(max_seconds)])
    cmd.extend([
        "-i", wav_path,
        "-vn", "-ac", "1", "-ar", "32000", "-b:a", "96k",
        mp3_path,
    ])
    subprocess.run(cmd, check=True, capture_output=True, timeout=300)
    with open(mp3_path, "rb") as fh:
        audio_b64 = base64.b64encode(fh.read()).decode("ascii")
    meta = {
        "audio_review_input": mp3_path,
        "audio_review_format": "mp3",
        "audio_review_size_kb": round(os.path.getsize(mp3_path) / 1024, 1),
        "audio_review_max_seconds": max_seconds,
    }
    return audio_b64, meta


def review_beat(
    wav_path: str,
    style_target: str = "Kanye West Late Registration chipmunk soul",
    bpm: float = 120,
    sections: list[tuple[float, float, str]] | None = None,
    project=None,
) -> dict:
    """Analyze a rendered beat via structural MIDI check + Azure audio review.

    Returns:
        {
            "scores": {"chipmunk_soul": 6, "drums": 7, "bass": 8, "arrangement": 8, "overall": 6.5},
            "issues": ["issue 1", "issue 2", "issue 3"],
            "review": "full review text",
        }
    """
    # Structural MIDI analysis (catches issues spectrograms miss)
    struct_report = _structural_midi_analysis(project) if project else ""
    struct_section = ""
    if struct_report:
        struct_section = f"""

## STRUCTURAL ANALYSIS (from MIDI data — trust this over the spectrogram)
{struct_report}

If any CRITICAL issues are listed above (e.g., drum track not marked as drums), they MUST be reflected in the scores. A beat with no audible drums cannot score above 3/10 for rhythm, regardless of what the spectrogram looks like.
"""

    prompt = f"""You are a hip-hop music production expert analyzing a beat.

This beat was generated by an AI trying to recreate: {style_target}
{struct_section}
Listen to the audio attachment and provide:

1. **Style Match Score** (1-10): How close is this to the target style?
2. **Rhythm Score** (1-10): Are the drums punchy, well-defined, with the right feel?
3. **Harmony/Melody Score** (1-10): Is the harmonic/melodic content appropriate for the style?
4. **Bass Score** (1-10): Is the low-end present, warm, and well-balanced?
5. **Arrangement Score** (1-10): Do the sections have dynamic contrast?
6. **Overall Score** (1-10): Final quality rating.

7. **Top 3 Specific Fixes** — each must be an actionable production instruction, e.g.:
   - "Increase velocity of notes on track X by N"
   - "Add more notes in octave 5-6 for brightness"
   - "Reduce 808 sustain duration by 30%"

Reply in this exact JSON format:
```json
{{
  "style_match": <int>,
  "rhythm": <int>,
  "harmony": <int>,
  "bass": <int>,
  "arrangement": <int>,
  "overall": <float>,
  "fixes": ["fix 1", "fix 2", "fix 3"],
  "summary": "1-2 sentence overall assessment"
}}
```"""

    from core.llm import call_azure_openai
    import json
    import re

    audio_b64, audio_meta = _prepare_audio_for_review(wav_path)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "input_audio",
                    "input_audio": {"data": audio_b64, "format": "mp3"},
                },
            ],
        }
    ]

    last_exc: Exception | None = None
    text = ""
    model_used = ""
    models = _audio_review_models()
    for idx, model in enumerate(models):
        try:
            resp = call_azure_openai(
                messages,
                model=model,
                reasoning_effort="none",
                max_completion_tokens=2048,
                timeout=int(os.environ.get("VWS_REAPER_AUDIO_REVIEW_TIMEOUT", "180")),
                max_retries=3,
                retry_delay=8.0,
            )
            text = resp.get("content", "") or ""
            model_used = model
            break
        except Exception as exc:
            last_exc = exc
            if idx + 1 < len(models):
                log.warning(
                    "Reaper audio review %s failed (%s); trying %s",
                    model,
                    type(exc).__name__,
                    models[idx + 1],
                )
    if not text and last_exc is not None:
        raise last_exc

    # Parse JSON from response
    m = re.search(r"```json\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        try:
            result = json.loads(m.group(1))
            result["review"] = text
            result["review_model"] = model_used
            result["review_input_modality"] = "audio"
            result["audio_review_metadata"] = audio_meta
            return result
        except json.JSONDecodeError:
            pass

    # Fallback: try to parse the whole response as JSON
    try:
        result = json.loads(text)
        result["review"] = text
        result["review_model"] = model_used
        result["review_input_modality"] = "audio"
        result["audio_review_metadata"] = audio_meta
        return result
    except json.JSONDecodeError:
        pass

    # Last resort: return raw text
    return {
        "style_match": 5,
        "rhythm": 5,
        "harmony": 5,
        "bass": 5,
        "arrangement": 5,
        "overall": 5.0,
        "fixes": [],
        "summary": "Could not parse structured review",
        "review": text,
        "review_model": model_used,
        "review_input_modality": "audio",
        "audio_review_metadata": audio_meta,
    }
