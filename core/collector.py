"""
core/collector.py
Search YouTube for tutorial videos and build video manifests.

Domain-agnostic: queries are passed in by caller or loaded from domain.yaml.

Usage:
    # Search and print results:
    python -m core.collector "minecraft building tutorial"

    # Search multiple queries, save manifest:
    python -m core.collector \
        "minecraft redstone tutorial" "minecraft auto farm" \
        -n 10 -o manifests/mc_skills_v1.json
"""
from __future__ import annotations

import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

_MANIFEST_DIR = Path(__file__).resolve().parent.parent / "manifests"


def search_youtube(
    query: str,
    max_results: int = 10,
    min_duration: int = 60,
    max_duration: int = 3600,
) -> list[dict]:
    """Search YouTube and return video metadata.

    Args:
        query: Search query string.
        max_results: Max number of results to fetch.
        min_duration: Skip videos shorter than this (seconds).
        max_duration: Skip videos longer than this (seconds).

    Returns:
        List of dicts with video metadata.
    """
    fetch_n = max_results * 3

    cmd = [
        "yt-dlp",
        f"ytsearch{fetch_n}:{query}",
        "--flat-playlist",
        "--no-download",
        "--print", "%(id)s\t%(title)s\t%(duration)s\t%(view_count)s\t%(upload_date)s\t%(channel)s",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {result.stderr[:500]}")

    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 6:
            continue

        vid, title, dur_str, views_str, upload_date, channel = parts

        try:
            duration = int(float(dur_str)) if dur_str and dur_str != "NA" else 0
        except (ValueError, TypeError):
            duration = 0

        if duration < min_duration or duration > max_duration:
            continue

        try:
            views = int(views_str) if views_str and views_str != "NA" else 0
        except (ValueError, TypeError):
            views = 0

        videos.append({
            "url": f"https://www.youtube.com/watch?v={vid}",
            "video_id": vid,
            "title": title,
            "duration_sec": duration,
            "views": views,
            "upload_date": upload_date or "",
            "channel": channel or "",
            "query": query,
        })

        if len(videos) >= max_results:
            break

    return videos


def multi_search(
    queries: list[str],
    max_per_query: int = 10,
    **kwargs,
) -> list[dict]:
    """Run multiple queries and deduplicate results by video ID."""
    seen_ids = set()
    all_videos = []

    for q in queries:
        print(f"Searching: {q!r}")
        results = search_youtube(q, max_results=max_per_query, **kwargs)
        for v in results:
            if v["video_id"] not in seen_ids:
                seen_ids.add(v["video_id"])
                all_videos.append(v)
        print(f"  Found {len(results)} results ({len(all_videos)} total unique)")

    all_videos.sort(key=lambda v: v["views"], reverse=True)
    return all_videos


def save_manifest(videos: list[dict], path: str | Path) -> Path:
    """Save a video list as a JSON manifest."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "created_at": datetime.now().isoformat(),
        "total": len(videos),
        "videos": videos,
    }
    p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def main():
    ap = argparse.ArgumentParser(description="Search YouTube for tutorial videos")
    ap.add_argument("queries", nargs="+", help="Search queries")
    ap.add_argument("-n", "--max-results", type=int, default=10, help="Max results per query")
    ap.add_argument("--min-duration", type=int, default=60, help="Min video duration (sec)")
    ap.add_argument("--max-duration", type=int, default=3600, help="Max video duration (sec)")
    ap.add_argument("-o", "--output", default=None, help="Save manifest to file")
    args = ap.parse_args()

    videos = multi_search(
        args.queries,
        max_per_query=args.max_results,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
    )

    print(f"\n{'='*60}")
    print(f"Total unique videos: {len(videos)}")
    print(f"{'='*60}")
    for i, v in enumerate(videos, 1):
        dur_min = v['duration_sec'] // 60
        dur_sec = v['duration_sec'] % 60
        print(f"  {i:2d}. [{dur_min}:{dur_sec:02d}] ({v['views']:>10,} views) {v['title']}")
        print(f"      {v['url']}")

    if args.output:
        p = save_manifest(videos, args.output)
        print(f"\nManifest saved: {p}")
    else:
        default_path = _MANIFEST_DIR / f"search_{datetime.now():%Y%m%d_%H%M%S}.json"
        p = save_manifest(videos, default_path)
        print(f"\nManifest saved: {p}")


if __name__ == "__main__":
    main()
