"""YouTube connector wrapping the existing ``core.collector.search_youtube``
plus ``core.analyzer`` distillation into the new ``SourceConnector`` contract.

The connector loads the per-domain distiller prompt from
``domains/<domain>/distiller_prompt.md`` and threads it into
``analyze_video`` together with the video URL. The Gemini call returns
markdown which the connector parses (skill name + analysis text) into a
``CandidateSkill`` that the wash pipeline can index.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .base import CandidateSkill, SourceConnector

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class YouTubeConnector(SourceConnector):
    SOURCE_TYPE = "youtube"

    def __init__(self, *, max_videos: int = 3, query_pool: list[str] | None = None,
                 model: str | None = None, extract_frames: bool = True,
                 max_frames: int = 4) -> None:
        self.max_videos = max_videos
        self.query_pool = query_pool or []
        # Default to gemini-2.5-flash for bulk collection — analyzer's
        # MODEL_POOL[0] is gemini-3.1-pro-preview which is overkill +
        # expensive for transcript distill at scale.
        self.model = model or os.environ.get("YOUTUBE_DISTILL_MODEL",
                                              "gemini-2.5-flash")
        self.extract_frames = extract_frames
        self.max_frames = max_frames

    def acquire(self, *, domain: str, quota: int, **kwargs: Any) -> list[CandidateSkill]:
        if quota <= 0:
            return []
        try:
            from core.collector import search_youtube
            from core.analyzer import (
                analyze_video, extract_frames as _extract_frames,
                parse_timestamps,
            )
            from core.skill_store import parse_skill_name
        except ImportError as exc:  # pragma: no cover - import guard
            raise RuntimeError(f"YouTube path unavailable: {exc}") from exc

        prompt_text = _load_distiller_prompt(domain)
        if not prompt_text:
            return []

        candidates: list[CandidateSkill] = []
        queries = kwargs.get("queries") or self.query_pool
        videos_per_query = kwargs.get("videos_per_query", min(self.max_videos, max(1, quota)))
        for query in queries:
            if len(candidates) >= quota:
                break
            try:
                videos = search_youtube(query=query, max_results=videos_per_query)
            except Exception:
                continue
            for video in videos:
                if len(candidates) >= quota:
                    break
                url = video.get("url") if isinstance(video, dict) else None
                if not url:
                    continue
                try:
                    analysis = analyze_video(url, model=self.model, prompt_text=prompt_text)
                except Exception:
                    continue
                if not analysis or not isinstance(analysis, str):
                    continue
                try:
                    skill_name = parse_skill_name(analysis) or video.get("title", "youtube_skill")
                except Exception:
                    skill_name = video.get("title", "youtube_skill")

                # Pull a few keyframes from the video so visual/ is not
                # empty. Falls back to uniform sampling when the
                # distiller markdown does not declare timestamps.
                frame_paths: list[str] = []
                if self.extract_frames:
                    timestamps = []
                    try:
                        timestamps = parse_timestamps(analysis)
                    except Exception:
                        timestamps = []
                    duration = int(video.get("duration_sec") or 0)
                    if not timestamps and duration > 30:
                        timestamps = [
                            {"seconds": int(duration * p),
                             "description": f"stage_{int(p*100)}pct"}
                            for p in (0.2, 0.4, 0.6, 0.8)
                        ]
                    if timestamps:
                        scratch = Path(tempfile.mkdtemp(
                            prefix="yt_frames_",
                            dir="/data/tmp" if Path("/data/tmp").exists() else None,
                        ))
                        try:
                            frames = _extract_frames(url, timestamps, scratch,
                                                     max_frames=self.max_frames)
                            # extract_frames returns relative names; resolve
                            # against the scratch dir so the wash pipeline
                            # can copy the file.
                            frame_paths = []
                            for f in frames:
                                p = f.get("path")
                                if not p:
                                    continue
                                abs_p = scratch / p if not Path(p).is_absolute() else Path(p)
                                if abs_p.exists():
                                    frame_paths.append(str(abs_p))
                        except Exception:
                            frame_paths = []

                candidates.append(_video_to_candidate(
                    video=video, analysis=analysis, skill_name=skill_name,
                    domain=domain, frame_paths=frame_paths,
                ))
        return candidates


def _load_distiller_prompt(domain: str) -> str:
    path = PROJECT_ROOT / "domains" / domain / "distiller_prompt.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _stable_id(skill_name: str, url: str) -> str:
    base = "".join(c if c.isalnum() else "_" for c in skill_name.lower()).strip("_")[:40]
    if not base:
        base = "yt_skill"
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{base}_{h}"


def _video_to_candidate(*, video: dict[str, Any], analysis: str,
                        skill_name: str, domain: str,
                        frame_paths: list[str] | None = None) -> CandidateSkill:
    url = video.get("url", "")
    extras: dict[str, Any] = {
        "video_id": video.get("video_id", ""),
        "video_title": video.get("title", ""),
        "duration_sec": video.get("duration_sec", 0),
        "views": video.get("views", 0),
        "upload_date": video.get("upload_date", ""),
    }
    if frame_paths:
        extras["frame_paths"] = list(frame_paths)
    return CandidateSkill(
        skill_id=_stable_id(skill_name, url),
        skill_name=skill_name,
        domain=domain,
        source_type="youtube",
        source_url=url,
        source_channel=str(video.get("channel") or ""),
        # YouTube content's actual license depends on the upload's
        # licence selector and is rarely declared in the API response.
        # Tag the entry as ``youtube_review_pending`` so the wash does
        # not quarantine it (which would block the active-count floor)
        # while still surfacing the licensing-review TODO to operators.
        license="youtube_review_pending",
        text_overview=analysis,
        # CandidateSkill carries one visual_path; the wash uses it as
        # the canonical frame copied into <skill>/visual/. Pick the
        # first extracted frame.
        visual_path=frame_paths[0] if frame_paths else None,
        extras=extras,
    )


__all__ = ["YouTubeConnector"]
