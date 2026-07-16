#!/usr/bin/env python3
"""
VideoWorldSkills CLI — unified entry point.

Usage:
    python cli.py collect  --domain minecraft --cycles 3
    python cli.py analyze  --domain minecraft --video <url>
    python cli.py batch    --domain ppt --manifest manifests/ppt_v1.json
    python cli.py build    --domain minecraft          # build embeddings
    python cli.py retrieve --domain minecraft --query "build iron farm"
    python cli.py plan     --domain minecraft --task "build iron farm"
    python cli.py execute  --domain minecraft --skill <skill_id>
    python cli.py execute  --domain minecraft --skill <skill_id> --dry-run
    python cli.py agent    --domain minecraft --task "build a 5x5 house"
    python cli.py domains                               # list available domains
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Ensure project root is on path.
_PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_PROJECT_ROOT))

# Load .env file if present (for GEMINI_API_KEY, AZURE_OPENAI_API_KEY, etc.)
from dotenv import load_dotenv
load_dotenv(_PROJECT_ROOT / ".env")

from core import load_domain, get_distiller_prompt, get_library_dir, list_domains, validate_domain
from core.analyzer import DEFAULT_MODEL


def cmd_domains(args):
    """List available domains."""
    for name in list_domains():
        config = load_domain(name)
        n_cats = len(config.get("categories", {}))
        n_queries = len(config.get("query_pool", []))
        has_mcp = "yes" if config.get("mcp") else "no"
        exec_mode = config.get("execution_mode") or "legacy"
        print(f"  {name:15s}  categories={n_cats:2d}  queries={n_queries:3d}  mcp={has_mcp}  mode={exec_mode}")


def cmd_validate_domain(args):
    """Validate a domain configuration."""
    errors = validate_domain(args.domain)
    if errors:
        print(f"FAIL: {args.domain}")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        config = load_domain(args.domain)
        exec_mode = config.get("execution_mode") or "legacy"
        n_cats = len(config.get("categories", {}))
        print(f"PASS: {args.domain} (execution_mode={exec_mode}, categories={n_cats})")



def cmd_collect(args):
    """Run auto-collection.

    When ``--cycle-quota > 0`` we drive the connector-based wiki collector
    (writes into ``skills_wiki/<d>/`` with source-mix enforcement). Otherwise
    we keep the legacy YouTube-only daemon for backwards compatibility.
    """
    config = load_domain(args.domain)
    if args.cycle_quota > 0:
        from core.wiki_collector import parse_source_mix, run_connector_cycle
        from core.sources import (
            ArticleConnector, GitHubConnector, StaticArtifactConnector, YouTubeConnector,
        )
        connectors = [
            YouTubeConnector(
                max_videos=args.videos,
                query_pool=config.get("query_pool") or _flatten_categories(config),
            ),
            GitHubConnector(),
            ArticleConnector(urls=config.get("article_urls") or []),
            StaticArtifactConnector(
                corpus_path=_PROJECT_ROOT / "skills_wiki" / args.domain / "_static_corpus.json",
            ),
        ]
        source_mix = parse_source_mix(args.source_mix)
        report = run_connector_cycle(
            domain=args.domain,
            connectors=connectors,
            cycle_quota=args.cycle_quota,
            source_mix=source_mix,
            project_root=_PROJECT_ROOT,
            extras={"queries": (config.get("query_pool") or _flatten_categories(config))[:args.queries]},
        )
        if args.json:
            print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
        else:
            print(f"cycle finished: washed={report.washed} quarantined={report.quarantined} "
                  f"failed_hard={report.failed_hard}")
        # Round-14 (AC-14 command-level): non-zero exit when the cycle
        # tripped a budget cap mid-run. Mirrors the wiki-wash side fix
        # from Round 13. Codex Round 13 finding 1 reproducer:
        # cmd_collect previously returned None on cap and printed the
        # report as if the run had succeeded.
        if getattr(report, "cap_reached", None):
            return 2
        return 0

    from core.auto_collect import run_daemon
    run_daemon(
        config,
        max_cycles=args.cycles,
        cycle_delay=args.cycle_delay,
        queries_per_cycle=args.queries,
        videos_per_query=args.videos,
        model=args.model,
        workers=args.workers,
    )


def _flatten_categories(config: dict) -> list[str]:
    out: list[str] = []
    for queries in (config.get("categories") or {}).values():
        if isinstance(queries, list):
            out.extend(str(q) for q in queries)
    return out


def cmd_analyze(args):
    """Analyze a single video."""
    from core.analyzer import analyze_video
    config = load_domain(args.domain)
    prompt = get_distiller_prompt(config)

    result = analyze_video(
        args.video,
        model=args.model,
        prompt_text=prompt,
        start_offset=args.start,
        end_offset=args.end,
    )

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Saved to {args.output}")
    else:
        print(result)


def cmd_batch(args):
    """Batch-process videos."""
    from core.batch_run import run_batch, load_manifest
    config = load_domain(args.domain)
    prompt = get_distiller_prompt(config)

    if args.manifest:
        videos = load_manifest(args.manifest)
    elif args.urls:
        videos = [{"url": u} for u in args.urls]
    else:
        print("Provide --manifest or --urls")
        sys.exit(1)

    out_dir = Path(args.output_dir) if args.output_dir else _PROJECT_ROOT / "outputs" / args.domain
    run_batch(
        videos, model=args.model, prompt_text=prompt,
        output_dir=out_dir, delay=args.delay, dry_run=args.dry_run,
    )


def cmd_build(args):
    """Build embeddings for a domain."""
    from core.skill_retriever import build_embeddings
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    library_dir = get_library_dir(args.domain)
    build_embeddings(library_dir, api_key=args.api_key)


def cmd_retrieve(args):
    """Retrieve skills for a query."""
    from core.skill_retriever import SkillRetriever
    config = load_domain(args.domain)
    library_dir = get_library_dir(args.domain)
    rerank_prompt = config.get("rerank_prompt")

    retriever = SkillRetriever(library_dir, rerank_prompt=rerank_prompt, api_key=args.api_key)

    if args.select and args.select > 0:
        results = retriever.select(args.query, n=args.select, top_k=args.top_k)
        print(f"\n=== Selected {len(results)} skills for: {args.query} ===\n")
        for r in results:
            print(f"  {r.get('skill_name', r['skill_id'])}")
            print(f"    reason: {r.get('reason', '-')}")
            print()
    else:
        results = retriever.retrieve(args.query, top_k=args.top_k)
        print(f"\n=== Top-{len(results)} candidates for: {args.query} ===\n")
        for i, r in enumerate(results, 1):
            print(f"  {i:2d}. [{r.get('category', '?'):12s}] "
                  f"{r.get('skill_name', r['skill_id']):<45s} "
                  f"score={r.get('score', 0):.4f}")


def cmd_plan(args):
    """Plan a task."""
    from core.task_planner import plan_task
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = load_domain(args.domain)
    library_dir = get_library_dir(args.domain)

    plan = plan_task(args.task, config, library_dir=library_dir, n_steps=args.steps)

    if args.output:
        Path(args.output).write_text(json.dumps(plan, indent=2, ensure_ascii=False), "utf-8")
        print(f"Plan saved to {args.output}")
    else:
        print(json.dumps(plan, indent=2, ensure_ascii=False))


def cmd_execute(args):
    """Execute a skill via the domain's MCP server."""
    import json as _json
    from core.executor import run_skill, extract_code
    from core.skill_store import get_skill

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = load_domain(args.domain)
    library_dir = get_library_dir(args.domain)

    if not config.get("mcp"):
        print(f"Domain '{args.domain}' has no MCP config. Cannot execute.")
        sys.exit(1)

    skill = get_skill(library_dir, args.skill)
    if not skill:
        print(f"Skill not found: {args.skill}")
        print("Tip: run `python cli.py retrieve --domain {args.domain} --query ...` to find skill IDs")
        sys.exit(1)

    if args.dry_run:
        # Print extracted code without connecting to MCP server.
        try:
            code = extract_code(skill.get("analysis", ""))
            print(f"=== Skill: {skill.get('skill_name')} ===\n")
            print(code)
        except ValueError as exc:
            print(f"Error: {exc}")
            sys.exit(1)
        return

    # Parse optional kwargs (--kwargs key=value key2=value2)
    overrides: dict = {}
    if args.kwargs:
        for kv in args.kwargs:
            if "=" not in kv:
                print(f"Invalid --kwargs entry (expected key=value): {kv}")
                sys.exit(1)
            k, v = kv.split("=", 1)
            # Try to parse as JSON, fall back to string
            try:
                overrides[k] = _json.loads(v)
            except _json.JSONDecodeError:
                overrides[k] = v

    result = run_skill(skill, config, dry_run=False, **overrides)

    print(result.summary())
    if args.verbose and result.tool_calls:
        print("\n--- Tool call log ---")
        for i, tc in enumerate(result.tool_calls, 1):
            status = "OK" if tc.success else "ERR"
            print(f"  {i:3d}. [{status}] {tc.tool_name}({tc.arguments})")
            if tc.error:
                print(f"         error: {tc.error}")
            elif args.verbose >= 2:
                print(f"         -> {tc.result[:120]}")


def cmd_agent(args):
    """Run LLM agent loop to accomplish a task."""
    from core.agent_executor import run_agent
    from domains.ppt import wiki_adapter as ppt_wiki_adapter

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = load_domain(args.domain)
    library_dir = get_library_dir(args.domain)
    ppt_wiki_adapter.set_active_brand(None)

    if not config.get("mcp") and not args.dry_run:
        print(f"Domain '{args.domain}' has no MCP config. Use --dry-run or add MCP config.")
        sys.exit(1)

    # --no-skills: filter out skill-discovery + skill-injection tools so the
    # agent only sees primitive tools. Used in the main ablation experiment.
    # --inline-skills: same tool filtering BUT keep auto_load_skills primer in prompt.
    if getattr(args, "no_skills", False) or getattr(args, "inline_skills", False):
        # Universal wiki contract tools — registered globally by
        # core/skill_wiki/mcp_tools.register_wiki_tools, so EVERY domain that
        # uses the wiki backend exposes all 9. The full set must be blocked
        # in --no-skills mode or skill knowledge leaks into the baseline.
        disabled = {
            "list_skills", "search_skills", "list_categories", "list_tiers",
            "get_skill_info", "get_skill_code", "get_skill_text",
            "get_skill_visual", "propose_category", "apply_skill",
            "reload_registry",
        }
        # Per-domain skill-injection tools (legacy / engine-specific).
        per_domain = {
            "web":     {"add_component_from_skill",
                        "generate_web_schema", "init_web_from_schema",
                        "reflect_and_swap"},
            # PPT scaffold (theme/shell/archetype) is the SHARED generator
            # used by both arms. Disabling it for --no-skills would compare
            # two different pipelines, not "same pipeline ± wiki skills".
            # Only disable wiki/skill-injection tools here.
            "ppt":     {"add_slide_from_skill",
                        "apply_component",
                        "get_technique_snippet", "get_palette_preset",
                        "list_motions", "get_motion_info", "get_motion_code",
                        "apply_motion", "suggest_morph_continuity",
                        # PPT Master's project/add/replace/export tools are a
                        # primitive backend. Its bundled template discovery is
                        # library knowledge and must not leak into --no-skills.
                        "pptmaster_select_r2s_refs",
                        "pptmaster_list_templates", "pptmaster_get_template",
                        "pptmaster_copy_template_to_project"},
            "excel":   {"init_from_archetype", "add_sheet_from_shell",
                        "apply_component", "list_tokens", "get_palette_preset",
                        "get_format_preset", "get_chart_template",
                        "get_formula_snippet"},
            "blender": {"list_scene_shells", "list_lighting_rigs",
                        "list_material_presets", "build_scene_from_shell",
                        "apply_lighting_rig", "apply_material_preset",
                        "add_object_from_skill",
                        "list_material_presets", "get_material_preset",
                        "list_lighting_rigs", "get_lighting_rig"},
            "reaper":  set(),  # apply_skill is in the universal set above
        }
        disabled |= per_domain.get(args.domain, set())
        config = dict(config)
        config["_disabled_tools"] = sorted(disabled)
        # Also force browse-first mode off so we don't preselect skills
        config["skill_selection"] = "none"
        # --inline-skills: keep auto_load primer in the system prompt even
        # though tools are disabled. The default gate disables auto-load
        # whenever skill discovery is disabled; this flag overrides that.
        if getattr(args, "inline_skills", False):
            config["_force_auto_load"] = True
        else:
            # --no-skills: clear auto_load_skills entirely so the baseline
            # really is "LLM with no library access".
            config["auto_load_skills"] = []
    elif getattr(args, "flat_skills", False):
        # --flat-skills: agent can still access skill code (list_skills /
        # get_skill_info / get_skill_code / apply_skill / per-domain
        # appliers) but the wiki ORGANIZATION (categories, archetypes,
        # themes, palettes, semantic search) is hidden. The list_skills
        # tool result is post-processed in the agent loop to strip metadata
        # and shuffle order; organization-aware tools are removed entirely.
        organization_disabled = {
            # Universal wiki organization tools (semantic search + taxonomy)
            "search_skills", "list_categories", "list_tiers", "propose_category",
            # PPT organization tools
            "pick_archetype", "pick_theme", "list_archetypes", "list_themes",
            "get_archetype", "get_theme", "select_shell", "list_shells",
            "get_palette_preset", "get_technique_snippet",
            "list_motions", "get_motion_info",
            "pptmaster_list_templates", "pptmaster_get_template",
            "pptmaster_select_r2s_refs",
            "pptmaster_copy_template_to_project",
            "add_slide_from_archetype",  # archetype-aware slide builder
            # Excel organization tools
            "list_tokens", "init_from_archetype",
            "get_format_preset", "get_chart_template",
            # Blender organization tools
            "list_scene_shells", "list_lighting_rigs", "list_material_presets",
            "build_scene_from_shell", "apply_lighting_rig",
            "apply_material_preset", "get_material_preset", "get_lighting_rig",
            # Web has no separate organization tools beyond the universal set
        }
        config = dict(config)
        config["_disabled_tools"] = sorted(organization_disabled)
        config["_flat_skills_mode"] = True
        # Suppress auto_load primer (it embeds taxonomy + design tokens)
        config["auto_load_skills"] = []
        config["skill_selection"] = "none"
    elif getattr(args, "schema_only", False) and args.domain == "web":
        # Force the agent into the Schema+Variant+Reflect flow by stripping
        # manual browsing/assembly tools. The agent can only call:
        #   create_project, generate_web_schema, init_web_from_schema,
        #   reflect_and_swap, render_page, inspect_dom, save_project,
        #   reload_registry
        # add_component_from_skill / write_file / read_file removed so the
        # agent CANNOT fall back to manual HTML assembly. If the schema
        # flow fails, the run fails — which is the right signal.
        disabled_manual = {
            "list_skills", "search_skills", "list_categories", "list_tiers",
            "get_skill_info", "get_skill_code", "get_skill_text",
            "add_component_from_skill",
            "write_file", "read_file",
        }
        config = dict(config)
        config["_disabled_tools"] = sorted(disabled_manual)
        config["skill_selection"] = "none"

    if getattr(args, "require_skill_path", False):
        incompatible = (
            getattr(args, "no_skills", False)
            or getattr(args, "inline_skills", False)
            or getattr(args, "flat_skills", False)
            or getattr(args, "schema_only", False)
        )
        if incompatible:
            print(
                "--require-skill-path is only valid for runtime with-skills "
                "runs; do not combine it with --no-skills, --flat-skills, "
                "--inline-skills, or --schema-only.",
                file=sys.stderr,
            )
            sys.exit(2)
        config = dict(config)
        config["_require_skill_path"] = True

    if args.brand:
        if args.domain != "ppt":
            print(f"--brand only supports --domain ppt in v2 (got {args.domain})")
            sys.exit(2)
        import yaml

        bp_path = Path("brand_wiki/ppt") / args.brand / "brand.yaml"
        if not bp_path.exists():
            print(f"brand pack not found: {bp_path}")
            sys.exit(2)
        bp = yaml.safe_load(bp_path.read_text())
        brand_skill_ids = bp.get("skills") or []
        if not brand_skill_ids:
            print(f"brand pack has no skills: {bp_path}")
            sys.exit(2)
        config = dict(config)
        existing = list(config.get("auto_load_skills") or [])
        config["auto_load_skills"] = existing + [
            s for s in brand_skill_ids if s not in existing
        ]
        config["_active_brand"] = args.brand
        config["_brand_skill_ids"] = brand_skill_ids
        disabled_tools = set(config.get("_disabled_tools") or [])
        # In brand mode, construction should flow through brand shell overlays
        # (`*_brand`) rather than generic skill cloning.
        disabled_tools.add("add_slide_from_skill")
        config["_disabled_tools"] = sorted(disabled_tools)
        mcp_cfg = dict(config.get("mcp") or {})
        mcp_env = dict(mcp_cfg.get("env") or {})
        mcp_env["PPT_ACTIVE_BRAND"] = args.brand
        mcp_cfg["env"] = mcp_env
        config["mcp"] = mcp_cfg
        ppt_wiki_adapter.set_active_brand(args.brand)
        logging.info("brand auto_load_skills=%s", brand_skill_ids)

    result = run_agent(
        args.task, config, library_dir,
        model=args.model,
        reasoning_effort=args.reasoning,
        max_iterations=args.max_iter,
        n_skills=args.n_skills,
        top_k=args.top_k,
        dry_run=args.dry_run,
        brand=args.brand,
    )

    # Print summary
    print(f"\n{result.summary()}")
    if result.final_message:
        # Strip very long final messages
        msg = result.final_message
        if len(msg) > 500:
            msg = msg[:500] + "..."
        print(f"\nFinal: {msg}")

    # Verbose tool log
    if args.verbose and result.tool_calls:
        print("\n--- Tool call log ---")
        for i, tc in enumerate(result.tool_calls, 1):
            status = "OK" if tc.success else "ERR"
            print(f"  {i:3d}. [{status}] {tc.tool_name}({tc.arguments})")
            if tc.error:
                print(f"         error: {tc.error}")
            elif args.verbose >= 2:
                print(f"         -> {tc.result[:120]}")

    # Save conversation log
    if args.output:
        log_data = {
            "task": result.task,
            "success": result.success,
            "iterations": result.iterations,
            "tool_calls": [
                {"tool": tc.tool_name, "args": tc.arguments,
                 "result": tc.result, "error": tc.error,
                 "verify_feedback": tc.verify_feedback}
                for tc in result.tool_calls
            ],
            "conversation": result.conversation,
            "final_message": result.final_message,
        }
        Path(args.output).write_text(
            json.dumps(log_data, indent=2, ensure_ascii=False), "utf-8"
        )
        print(f"\nConversation log saved to {args.output}")


def cmd_score_skills(args):
    from core.harness import score_skills
    result = score_skills(args.domain, limit=args.limit, model=args.model)
    print(f"\nSkill scoring complete: {result['scored']} scored, {result['failed']} failed")

    # Print category summary
    from core import get_library_dir
    import json as _json
    meta_path = get_library_dir(args.domain) / "metadata.json"
    if meta_path.exists():
        meta = _json.loads(meta_path.read_text())
        scored_entries = {k: v for k, v in meta.items() if isinstance(v.get("visual_quality"), (int, float))}
        if scored_entries:
            avg = sum(v["visual_quality"] for v in scored_entries.values()) / len(scored_entries)
            print(f"Average visual quality: {avg:.1f}/5 ({len(scored_entries)} scored)")


def cmd_score_demos(args):
    from core.harness import score_demos
    result = score_demos(args.domain, model=args.model)
    print(f"\nDemo scoring complete: {len(result['demos'])} demos, avg_overall={result['avg_overall']}")
    for name, scores in result.get("demos", {}).items():
        overall = scores.get("overall", "?")
        strengths = scores.get("strengths", "")[:60]
        print(f"  {name}: {overall}/5 — {strengths}")


def cmd_evolve(args):
    from core.harness import evolve
    result = evolve(args.domain, model=args.model, dry_run=args.dry_run)
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Evolution report:")
    print(f"  Analysis: {result.get('analysis', '?')}")
    print(f"  Weak categories: {result.get('weak_categories', [])}")
    print(f"  Missing categories: {result.get('missing_categories', [])}")
    new_q = result.get("new_queries", [])
    if new_q:
        print(f"  New queries ({len(new_q)}):")
        for q in new_q:
            print(f"    - {q}")
    actions = result.get("actions_taken", [])
    if actions:
        print(f"  Actions taken:")
        for a in actions:
            print(f"    - {a}")
    prompt_imp = result.get("prompt_changes", result.get("prompt_improvements", []))
    if prompt_imp:
        print(f"  Prompt changes:")
        for p in prompt_imp:
            print(f"    - {p}")
    arch = result.get("architecture_suggestions", result.get("architecture_changes", []))
    if arch:
        print(f"  Architecture suggestions:")
        for c in arch:
            print(f"    - {c}")


def cmd_evolve_distiller(args):
    from core.harness import evolve_distiller
    result = evolve_distiller(args.domain, model=args.model, dry_run=args.dry_run)
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Distiller evolution:")
    print(f"  Analysis: {result.get('analysis', '?')}")
    print(f"  Changes needed: {result.get('changes_needed', False)}")
    for fix in result.get("fixes", []):
        print(f"  [{fix.get('pattern')}] ({fix.get('count', 0)}x): {fix.get('fix', '?')[:100]}")
    for a in result.get("actions_taken", []):
        print(f"  Action: {a}")


def cmd_evolve_agent(args):
    from core.harness import evolve_agent
    result = evolve_agent(args.domain, model=args.model, dry_run=args.dry_run)
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Agent evolution:")
    print(f"  Analysis: {result.get('analysis', '?')}")
    for w in result.get("winning_patterns", []):
        print(f"  [WIN] {w.get('pattern', '?')} (demo: {w.get('example_demo')}, score: {w.get('score')})")
    for c in result.get("recommended_combos", []):
        cats = ", ".join(c.get("skill_categories", []))
        print(f"  [COMBO] {c.get('task_type', '?')}: [{cats}]")
    for a in result.get("actions_taken", []):
        print(f"  Action: {a}")


def cmd_auto_collect(args):
    from core.harness import auto_collect
    result = auto_collect(args.domain, model=args.model, cycles=args.cycles,
                          videos_per_query=args.videos, workers=args.workers)
    print(f"\nAuto-collect:")
    print(f"  Gap analysis: {result.get('gap_analysis', '?')}")
    print(f"  Queries used: {len(result.get('queries_used', []))}")
    print(f"  Skills collected: {result.get('collected', 0)}")


def cmd_brand_extract(args):
    """Extract a brand pack from a folder/zip of PPTX files."""
    from pathlib import Path

    from domains.ppt.brand_extractor.pipeline import extract

    if args.domain != "ppt":
        print(f"brand-extract only supports --domain ppt in v1 (got {args.domain})")
        sys.exit(2)

    src = Path(args.source).expanduser().resolve()
    out_root = (
        Path(args.output_root).expanduser().resolve()
        if args.output_root
        else Path("brand_wiki/ppt").resolve()
    )

    result = extract(
        brand_name=args.brand,
        source=src,
        output_root=out_root,
        render=not args.no_render,
        vision=not args.no_vision,
        synthesize_skills=not args.no_skills,
    )
    print(f"OK brand={args.brand} dir={result.brand_dir} skills={len(result.skill_ids)}")


def cmd_harness_loop(args):
    from core.harness import run_full_loop
    result = run_full_loop(args.domain, model=args.model, skill_limit=args.skill_limit,
                           collect_cycles=args.collect_cycles, dry_run=args.dry_run)
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Full harness loop complete:")
    ss = result.get("score_skills", {})
    print(f"  Skills scored: {ss.get('scored', 0)}, failed: {ss.get('failed', 0)}")
    sd = result.get("score_demos", {})
    print(f"  Demo avg: {sd.get('avg_overall', 0)}")
    ev = result.get("evolve", {})
    print(f"  Evolution actions: {len(ev.get('actions_taken', []))}")
    ed = result.get("evolve_distiller", {})
    print(f"  Distiller changes: {ed.get('changes_needed', False)}")
    ea = result.get("evolve_agent", {})
    print(f"  Agent patterns: {len(ea.get('winning_patterns', []))}")
    ac = result.get("auto_collect", {})
    print(f"  Auto-collected: {ac.get('collected', ac.get('skipped', '?'))}")


def main():
    parser = argparse.ArgumentParser(
        prog="vse",
        description="VideoWorldSkills — domain-agnostic skill extraction from tutorial videos",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # domains
    sub.add_parser("domains", help="List available domains")

    # validate-domain
    p = sub.add_parser("validate-domain", help="Validate a domain configuration")
    p.add_argument("--domain", required=True, help="Domain name to validate")

    # collect
    p = sub.add_parser("collect", help="Run auto-collection daemon")
    p.add_argument("--domain", required=True)
    p.add_argument("--cycles", type=int, default=0)
    p.add_argument("--cycle-delay", type=float, default=1800)
    p.add_argument("--queries", type=int, default=3)
    p.add_argument("--videos", type=int, default=5)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--workers", type=int, default=3)
    p.add_argument("--cycle-quota", type=int, default=0,
                   help="Per-cycle skill quota for the connector path. When >0, "
                        "collection runs through SourceConnector and writes into "
                        "skills_wiki/<d>/. Without this flag, the legacy YouTube-only "
                        "path (writing to skills_library/<d>/) is used.")
    p.add_argument("--source-mix", default="youtube=80,github=5,article=5,static_artifact=10",
                   help="Per-cycle quota mix as 'youtube=80,github=5,...'. Only used "
                        "when --cycle-quota>0.")
    p.add_argument("--json", action="store_true",
                   help="Emit cycle report as JSON to stdout (connector path).")

    # analyze
    p = sub.add_parser("analyze", help="Analyze a single video")
    p.add_argument("--domain", required=True)
    p.add_argument("--video", required=True, help="YouTube URL")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--start", default=None)
    p.add_argument("--end", default=None)
    p.add_argument("-o", "--output", default=None)

    # batch
    p = sub.add_parser("batch", help="Batch-process videos")
    p.add_argument("--domain", required=True)
    p.add_argument("--manifest", default=None)
    p.add_argument("--urls", nargs="+", default=None)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--output-dir", default=None)
    p.add_argument("--delay", type=float, default=5.0)
    p.add_argument("--dry-run", action="store_true")

    # build
    p = sub.add_parser("build", help="Build embeddings for a domain")
    p.add_argument("--domain", required=True)
    p.add_argument("--api-key", default=None)

    # retrieve
    p = sub.add_parser("retrieve", help="Retrieve skills for a query")
    p.add_argument("--domain", required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--top-k", type=int, default=20)
    p.add_argument("--select", type=int, default=0)
    p.add_argument("--api-key", default=None)

    # plan
    p = sub.add_parser("plan", help="Plan a task")
    p.add_argument("--domain", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("-o", "--output", default=None)

    # execute
    p = sub.add_parser("execute", help="Execute a skill via MCP")
    p.add_argument("--domain", required=True)
    p.add_argument("--skill", required=True, help="Skill ID to execute")
    p.add_argument("--dry-run", action="store_true",
                   help="Extract and print code without connecting to MCP server")
    p.add_argument("--kwargs", nargs="*", metavar="KEY=VALUE",
                   help="Optional parameter overrides passed to skill function (e.g. width=10 material=oak_log)")
    p.add_argument("-v", "--verbose", action="count", default=0,
                   help="Show tool call log (-v) or full results (-vv)")

    # agent
    p = sub.add_parser("agent", help="Run LLM agent loop to accomplish a task")
    p.add_argument("--domain", required=True)
    p.add_argument("--task", required=True, help="Natural language task description")
    p.add_argument("--model", default="gpt-5.4", help="LLM model (default: gpt-5.4)")
    p.add_argument("--reasoning", default="medium", choices=["none", "low", "medium", "high", "xhigh"],
                   help="Reasoning effort (default: medium). gpt-5.4-pro only supports medium/high/xhigh")
    p.add_argument("--max-iter", type=int, default=30, help="Max agent loop iterations")
    p.add_argument("--n-skills", type=int, default=5, help="Number of skills to retrieve")
    p.add_argument("--top-k", type=int, default=20, help="Embedding recall pool size")
    p.add_argument("--dry-run", action="store_true",
                   help="Run with mock MCP (no server connection)")
    p.add_argument("--brand", default=None,
                   help="Activate a brand pack from brand_wiki/<domain>/<brand>/. "
                        "Brand-locked skills and constraints are layered on top of "
                        "the generic library. Default None = current behavior.")
    p.add_argument("--no-skills", action="store_true",
                   help="Disable skill-discovery and skill-injection tools "
                        "(ablation: agent only sees primitive tools).")
    p.add_argument("--flat-skills", action="store_true",
                   help="Skills accessible (list/get_code/apply) but the wiki "
                        "organization (categories, archetypes, themes, palettes, "
                        "semantic search) is hidden. Tool results are stripped "
                        "of metadata and shuffled into a flat (id, name) list. "
                        "Tests whether the wiki structure adds value beyond "
                        "raw skill access.")
    p.add_argument("--inline-skills", action="store_true",
                   help="Disable skill-discovery tools BUT keep auto_load_skills "
                        "active (skill knowledge embedded in system prompt). "
                        "Tests whether having library knowledge in-context helps "
                        "without the cost of browsing.")
    p.add_argument("--schema-only", action="store_true",
                   help="Force the Schema+Variant+Reflect flow (web domain only). "
                        "Disables manual browsing/assembly tools so the agent "
                        "MUST use generate_web_schema -> init_web_from_schema "
                        "-> reflect_and_swap.")
    p.add_argument("--require-skill-path", action="store_true",
                   help="Runtime with-skills guard: block manual/scaffold build "
                        "tools until the trace shows skill search/list, "
                        "text/code/info inspection, visual inspection, and a "
                        "domain runtime skill attempt.")
    p.add_argument("-v", "--verbose", action="count", default=0,
                   help="Show tool call log (-v) or full results (-vv)")
    p.add_argument("-o", "--output", default=None, help="Save conversation log to JSON")

    # score-skills
    p = sub.add_parser("score-skills", help="Score skills via execution + GPT-5.4 vision")
    p.add_argument("--domain", required=True)
    p.add_argument("--limit", type=int, default=0, help="Max skills to score (0=all)")
    p.add_argument("--model", default="gpt-5.4")

    # score-demos
    p = sub.add_parser("score-demos", help="Score demo outputs via GPT-5.4 vision")
    p.add_argument("--domain", required=True)
    p.add_argument("--model", default="gpt-5.4")

    # evolve
    p = sub.add_parser("evolve", help="Analyze scores and auto-improve domain architecture")
    p.add_argument("--domain", required=True)
    p.add_argument("--model", default="gpt-5.4")
    p.add_argument("--dry-run", action="store_true", help="Show recommendations without applying")

    # evolve-distiller
    p = sub.add_parser("evolve-distiller", help="Fix distiller prompt based on skill failure patterns")
    p.add_argument("--domain", required=True)
    p.add_argument("--model", default="gpt-5.4")
    p.add_argument("--dry-run", action="store_true")

    # evolve-agent
    p = sub.add_parser("evolve-agent", help="Extract best skill composition patterns from demo scores")
    p.add_argument("--domain", required=True)
    p.add_argument("--model", default="gpt-5.4")
    p.add_argument("--dry-run", action="store_true")

    # auto-collect
    p = sub.add_parser("auto-collect", help="Identify missing skills and run targeted YouTube collection")
    p.add_argument("--domain", required=True)
    p.add_argument("--model", default="gpt-5.4")
    p.add_argument("--cycles", type=int, default=1)
    p.add_argument("--videos", type=int, default=3)
    p.add_argument("--workers", type=int, default=3)

    # harness-loop
    p = sub.add_parser("harness-loop", help="Run full self-evolution loop (all 6 stages)")
    p.add_argument("--domain", required=True)
    p.add_argument("--model", default="gpt-5.4")
    p.add_argument("--skill-limit", type=int, default=50, help="Max skills to score per loop")
    p.add_argument("--collect-cycles", type=int, default=1)
    p.add_argument("--dry-run", action="store_true")

    # brand-extract
    p = sub.add_parser("brand-extract", help="Extract a brand pack from PPTX resources")
    p.add_argument("--domain", required=True, help="Domain (only 'ppt' supported in v1)")
    p.add_argument("--brand", required=True, help="Brand slug (lowercase, _-separated)")
    p.add_argument("--source", required=True, help="Path to a folder of .pptx or a .zip")
    p.add_argument("--output-root", default=None, help="Output root (default brand_wiki/ppt)")
    p.add_argument("--no-render", action="store_true", help="Skip LibreOffice slide rendering")
    p.add_argument("--no-vision", action="store_true", help="Skip GPT-5.4 vision enrichment")
    p.add_argument("--no-skills", action="store_true", help="Skip skill synthesis")
    p.set_defaults(func=cmd_brand_extract)

    # Wiki registry commands (skill_wiki package).
    from core.skill_wiki.cli_handlers import register_subparsers as _register_wiki
    _register_wiki(sub)

    args = parser.parse_args()

    if args.command == "domains":
        cmd_domains(args)
    elif args.command == "validate-domain":
        cmd_validate_domain(args)
    elif args.command == "collect":
        # Round-14: cmd_collect now returns an int exit code so AC-14
        # cap-reached propagates through to the shell. Other commands
        # in this dispatch still return None on success, so we only
        # sys.exit when an explicit non-zero is reported.
        rc = cmd_collect(args)
        if rc:
            sys.exit(rc)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "batch":
        cmd_batch(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "retrieve":
        cmd_retrieve(args)
    elif args.command == "plan":
        cmd_plan(args)
    elif args.command == "execute":
        cmd_execute(args)
    elif args.command == "agent":
        cmd_agent(args)
    elif args.command == "score-skills":
        cmd_score_skills(args)
    elif args.command == "score-demos":
        cmd_score_demos(args)
    elif args.command == "evolve":
        cmd_evolve(args)
    elif args.command == "evolve-distiller":
        cmd_evolve_distiller(args)
    elif args.command == "evolve-agent":
        cmd_evolve_agent(args)
    elif args.command == "auto-collect":
        cmd_auto_collect(args)
    elif args.command == "harness-loop":
        cmd_harness_loop(args)
    elif getattr(args, "func", None) is not None:
        # Wiki registry subcommands wired via register_subparsers attach func= to args.
        sys.exit(args.func(args) or 0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
