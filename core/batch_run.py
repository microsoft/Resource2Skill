"""
core/batch_run.py
Batch-process a list of YouTube URLs through the skill distiller pipeline.

Usage:
    vse batch --domain minecraft --manifest manifests/mc_v1.json
    vse batch --domain ppt --urls "https://..." "https://..."
"""
from __future__ import annotations

import json
import time
import argparse
from datetime import datetime
from pathlib import Path

from core.analyzer import analyze_video, DEFAULT_MODEL

_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def _slug(url: str) -> str:
    """Extract a filesystem-safe slug from a YouTube URL."""
    for prefix in ("https://www.youtube.com/watch?v=", "https://youtu.be/"):
        if url.startswith(prefix):
            vid = url[len(prefix):].split("&")[0]
            return vid
    return url.replace("https://", "").replace("/", "_")[:40]


def load_manifest(path: str | Path) -> list[dict]:
    """Load a JSON manifest file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [{"url": u} if isinstance(u, str) else u for u in data]
    return data.get("videos", [])


def run_batch(
    videos: list[dict],
    *,
    model: str = DEFAULT_MODEL,
    prompt_path: str | Path | None = None,
    prompt_text: str | None = None,
    output_dir: Path = _OUTPUT_DIR,
    delay: float = 5.0,
    dry_run: bool = False,
) -> list[dict]:
    """Process a list of videos and save results.

    Args:
        videos: List of dicts with at least {"url": "..."}.
        model: Gemini model name.
        prompt_path: Path to distiller prompt (domain-specific).
        prompt_text: Direct prompt text (overrides prompt_path).
        output_dir: Where to write .md result files.
        delay: Seconds to wait between API calls.
        dry_run: If True, print plan but don't call API.

    Returns:
        List of result dicts.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    total = len(videos)

    for i, entry in enumerate(videos, 1):
        url = entry["url"]
        title = entry.get("title", url)
        slug = _slug(url)
        out_path = output_dir / f"{slug}.md"

        print(f"[{i}/{total}] {title}")
        print(f"         URL: {url}")

        if dry_run:
            print(f"         (dry-run, skipping)")
            results.append({"url": url, "title": title, "status": "skipped"})
            continue

        if out_path.exists():
            print(f"         Already exists: {out_path}, skipping.")
            results.append({
                "url": url, "title": title,
                "output_path": str(out_path), "status": "cached",
            })
            continue

        try:
            text = analyze_video(
                url, model=model,
                prompt_path=prompt_path, prompt_text=prompt_text,
            )
            out_path.write_text(text, encoding="utf-8")
            print(f"         Saved: {out_path}")
            results.append({
                "url": url, "title": title,
                "output_path": str(out_path), "status": "ok",
            })
        except Exception as e:
            print(f"         FAILED: {e}")
            results.append({
                "url": url, "title": title,
                "status": "error", "error": str(e),
            })

        if i < total:
            time.sleep(delay)

    summary_path = output_dir / f"_batch_summary_{datetime.now():%Y%m%d_%H%M%S}.json"
    summary_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nBatch complete. Summary: {summary_path}")

    ok = sum(1 for r in results if r["status"] == "ok")
    cached = sum(1 for r in results if r["status"] == "cached")
    err = sum(1 for r in results if r["status"] == "error")
    print(f"Results: {ok} new, {cached} cached, {err} errors, {total} total")
    return results
