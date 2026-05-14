"""
core/auto_collect.py
Autonomous skill collection daemon.

Continuously:
  1. Picks search queries from a domain's query pool
  2. Searches YouTube for tutorials
  3. Filters out already-processed videos
  4. Analyzes each video via Gemini API
  5. Categorizes and stores skills in the domain's library

Usage:
    vse collect --domain minecraft --cycles 3
    vse collect --domain ppt --cycle-delay 1800
"""
from __future__ import annotations

import json
import time
import random
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from core.collector import search_youtube
from core.analyzer import analyze_video, parse_timestamps, extract_frames, DEFAULT_MODEL
from core.skill_store import store_skill, _load_index
from core import load_domain, get_distiller_prompt, get_library_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("auto_collect")


def _state_dir(domain_name: str) -> Path:
    return Path(__file__).resolve().parent.parent / "state" / domain_name


def _load_processed(domain_name: str) -> set[str]:
    """Load the set of already-processed video IDs."""
    path = _state_dir(domain_name) / "processed_videos.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return set(data.get("video_ids", []))
    return set()


def _save_processed(domain_name: str, ids: set[str]):
    state = _state_dir(domain_name)
    state.mkdir(parents=True, exist_ok=True)
    (state / "processed_videos.json").write_text(
        json.dumps({
            "updated_at": datetime.now().isoformat(),
            "count": len(ids),
            "video_ids": sorted(ids),
        }, indent=2),
        encoding="utf-8",
    )


def _pick_queries(query_pool: list[str], n: int = 3) -> list[str]:
    """Pick N random queries from the pool."""
    return random.sample(query_pool, min(n, len(query_pool)))


def _download_thumbnail(video_id: str, output_dir: Path) -> str | None:
    """Download YouTube thumbnail to output_dir. Returns filename or None."""
    import urllib.request
    output_dir.mkdir(parents=True, exist_ok=True)
    thumb_path = output_dir / "thumbnail.jpg"
    if thumb_path.exists():
        return "thumbnail.jpg"
    for quality in ("maxresdefault", "hqdefault", "mqdefault"):
        url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
        try:
            urllib.request.urlretrieve(url, str(thumb_path))
            if thumb_path.stat().st_size > 1000:  # valid image, not 404 placeholder
                return "thumbnail.jpg"
        except Exception:
            continue
    return None


def _process_video(
    v: dict,
    model: str,
    domain_config: dict,
    library_dir: Path,
    distiller_prompt: str,
) -> dict:
    """Analyze and store one video. Returns a result dict."""
    url = v["url"]
    title = v.get("title", url)
    try:
        analysis = analyze_video(url, model=model, prompt_text=distiller_prompt)

        # Extract key frames: prefer analysis timestamps, fallback to uniform sampling
        timestamps = parse_timestamps(analysis)
        duration_sec = v.get("duration_sec", 0)
        if not timestamps and duration_sec > 30:
            # Uniform sampling at 20%/40%/60%/80% of video duration
            timestamps = [
                {"seconds": int(duration_sec * p), "description": f"stage_{int(p*100)}pct"}
                for p in (0.2, 0.4, 0.6, 0.8)
            ]

        frames = []
        import tempfile
        tmp_frames_dir = Path(tempfile.mkdtemp(prefix="frames_"))
        if timestamps:
            try:
                frames = extract_frames(url, timestamps, tmp_frames_dir, max_frames=4)
            except Exception as fe:
                log.warning("Frame extraction failed for %s: %s", url, fe)

        result = store_skill(
            analysis,
            domain=domain_config["name"],
            library_dir=library_dir,
            category_list=domain_config["category_list"],
            category_keywords=domain_config["category_keywords"],
            video_url=url,
            video_title=title,
            video_id=v.get("video_id", ""),
            channel=v.get("channel", ""),
            duration_sec=v.get("duration_sec", 0),
            views=v.get("views", 0),
            model=model,
            frames=frames,
        )

        # Move extracted frames to the skill's directory
        if frames and result.get("detail_path"):
            import shutil
            skill_dir = Path(result["detail_path"]).parent
            for f in frames:
                src = tmp_frames_dir / f["path"]
                dst = skill_dir / f["path"]
                if src.exists():
                    shutil.move(str(src), str(dst))

        # Download YouTube thumbnail
        video_id = v.get("video_id", "")
        if video_id and result.get("detail_path"):
            skill_dir = Path(result["detail_path"]).parent
            _download_thumbnail(video_id, skill_dir)

        # Clean up temp frames dir
        import shutil
        shutil.rmtree(str(tmp_frames_dir), ignore_errors=True)

        return {"ok": True, "video_id": video_id, **result}
    except Exception as e:
        return {"ok": False, "video_id": v.get("video_id", ""), "error": str(e)}


def run_cycle(
    domain_config: dict,
    *,
    queries_per_cycle: int = 3,
    videos_per_query: int = 5,
    model: str = DEFAULT_MODEL,
    workers: int = 3,
) -> dict:
    """Run one collection cycle: search -> analyze -> store."""
    domain_name = domain_config["name"]
    library_dir = get_library_dir(domain_name)
    distiller_prompt = get_distiller_prompt(domain_config)
    query_pool = domain_config.get("query_pool", [])

    if not query_pool:
        log.warning(f"No query_pool defined for domain '{domain_name}'")
        return {"searched": 0, "new_videos": 0, "skills_stored": 0, "errors": 0}

    processed = _load_processed(domain_name)
    queries = _pick_queries(query_pool, queries_per_cycle)
    log.info(f"Cycle start [{domain_name}] — queries: {queries}")

    new_videos = []
    for q in queries:
        try:
            results = search_youtube(q, max_results=videos_per_query)
            for v in results:
                if v["video_id"] not in processed:
                    new_videos.append(v)
        except Exception as e:
            log.warning(f"Search failed for {q!r}: {e}")

    seen = set()
    unique_videos = []
    for v in new_videos:
        if v["video_id"] not in seen:
            seen.add(v["video_id"])
            unique_videos.append(v)

    log.info(f"Found {len(unique_videos)} new videos (skipped {len(processed)} processed)")

    if not unique_videos:
        return {"searched": len(queries), "new_videos": 0, "skills_stored": 0, "errors": 0}

    stored = 0
    errors = 0
    total = len(unique_videos)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(
                _process_video, v, model, domain_config, library_dir, distiller_prompt
            ): v
            for v in unique_videos
        }
        for i, fut in enumerate(as_completed(futures), 1):
            v = futures[fut]
            res = fut.result()
            video_id = res.get("video_id", v.get("video_id", ""))
            processed.add(video_id)

            if res["ok"]:
                log.info(f"  [{i}/{total}] Stored: [{res['category']}] {res['skill_name']}")
                stored += 1
            else:
                log.error(f"  [{i}/{total}] FAILED {v.get('title','')}: {res['error']}")
                errors += 1

    _save_processed(domain_name, processed)

    summary = {
        "searched": len(queries),
        "new_videos": total,
        "skills_stored": stored,
        "errors": errors,
        "total_processed": len(processed),
    }
    log.info(f"Cycle complete: {summary}")
    return summary


def run_daemon(
    domain_config: dict,
    *,
    max_cycles: int = 0,
    cycle_delay: float = 1800.0,
    queries_per_cycle: int = 3,
    videos_per_query: int = 5,
    model: str = DEFAULT_MODEL,
    workers: int = 3,
    cycle_quota: int = 0,
    source_mix: str | None = None,
):
    """Run the collection daemon continuously.

    When ``cycle_quota > 0`` (or the domain has ``library_backend: wiki``),
    the daemon delegates each cycle to the connector-based wiki collector
    so legacy-domain runs keep working while wiki-mode runs honour the
    ``--cycle-quota`` / ``--source-mix`` policy and write into
    ``skills_wiki/<d>/``.
    """
    domain_name = domain_config["name"]

    # Honour the per-domain library_backend flag: in wiki mode the daemon
    # routes through run_connector_cycle so the AC-5 source-mix policy
    # and license quarantine apply.
    backend = str(domain_config.get("library_backend", "legacy")).lower()
    use_wiki = cycle_quota > 0 or backend == "wiki"

    log.info("=" * 60)
    log.info(f"Auto-collect daemon starting — domain: {domain_name}")
    log.info(f"  Backend: {backend}{' (wiki collector)' if use_wiki else ''}")
    log.info(f"  Model: {model}")
    log.info(f"  Workers: {workers}")
    log.info(f"  Queries/cycle: {queries_per_cycle}")
    log.info(f"  Videos/query: {videos_per_query}")
    log.info(f"  Cycle delay: {cycle_delay}s ({cycle_delay/60:.0f} min)")
    log.info(f"  Max cycles: {'unlimited' if max_cycles == 0 else max_cycles}")
    log.info("=" * 60)

    cycle_num = 0
    total_skills = 0
    while True:
        cycle_num += 1
        log.info(f"\n{'='*40} CYCLE {cycle_num} {'='*40}")

        if use_wiki:
            summary = _run_wiki_cycle(
                domain_config=domain_config,
                queries_per_cycle=queries_per_cycle,
                videos_per_query=videos_per_query,
                cycle_quota=cycle_quota or 100,
                source_mix=source_mix,
            )
        else:
            summary = run_cycle(
                domain_config,
                queries_per_cycle=queries_per_cycle,
                videos_per_query=videos_per_query,
                model=model,
                workers=workers,
            )
        total_skills += summary["skills_stored"]
        log.info(f"Running total: {total_skills} skills collected")

        if max_cycles > 0 and cycle_num >= max_cycles:
            log.info(f"Reached max cycles ({max_cycles}). Stopping.")
            break

        log.info(f"Sleeping {cycle_delay}s until next cycle...")
        time.sleep(cycle_delay)


def _run_wiki_cycle(
    *, domain_config: dict, queries_per_cycle: int, videos_per_query: int,
    cycle_quota: int, source_mix: str | None,
) -> dict:
    """Drive one cycle through the connector-based wiki collector."""
    from pathlib import Path
    from core.sources import (
        ArticleConnector, GitHubConnector, StaticArtifactConnector, YouTubeConnector,
    )
    from core.wiki_collector import parse_source_mix, run_connector_cycle

    project_root = Path(__file__).resolve().parents[1]
    domain_name = domain_config["name"]
    connectors = [
        YouTubeConnector(
            max_videos=videos_per_query,
            query_pool=domain_config.get("query_pool")
            or _flatten_categories_inline(domain_config),
        ),
        GitHubConnector(),
        ArticleConnector(urls=domain_config.get("article_urls") or []),
        StaticArtifactConnector(
            corpus_path=project_root / "skills_wiki" / domain_name / "_static_corpus.json",
        ),
    ]
    mix = parse_source_mix(source_mix or "youtube=80,github=5,article=5,static_artifact=10")
    queries = (
        domain_config.get("query_pool")
        or _flatten_categories_inline(domain_config)
    )[:queries_per_cycle]
    report = run_connector_cycle(
        domain=domain_name,
        connectors=connectors,
        cycle_quota=cycle_quota,
        source_mix=mix,
        project_root=project_root,
        extras={"queries": queries},
    )
    return {"skills_stored": report.washed, "report": report.to_dict()}


def _flatten_categories_inline(config: dict) -> list[str]:
    out: list[str] = []
    for queries in (config.get("categories") or {}).values():
        if isinstance(queries, list):
            out.extend(str(q) for q in queries)
    return out
