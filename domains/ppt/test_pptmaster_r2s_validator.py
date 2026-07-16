import json
import importlib.util
import sys
from pathlib import Path


_VALIDATOR_PATH = Path(__file__).with_name("validate_pptmaster_r2s_run.py")
_SPEC = importlib.util.spec_from_file_location("validate_pptmaster_r2s_run", _VALIDATOR_PATH)
assert _SPEC and _SPEC.loader
_VALIDATOR = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _VALIDATOR
_SPEC.loader.exec_module(_VALIDATOR)
validate_summary = _VALIDATOR.validate_summary
validate_open_compare = _VALIDATOR.validate_open_compare

_RUNNER_PATH = Path(__file__).with_name("pptmaster_r2s_prompt_runner.py")
_RUNNER_SPEC = importlib.util.spec_from_file_location("pptmaster_r2s_prompt_runner", _RUNNER_PATH)
assert _RUNNER_SPEC and _RUNNER_SPEC.loader
_RUNNER = importlib.util.module_from_spec(_RUNNER_SPEC)
sys.modules[_RUNNER_SPEC.name] = _RUNNER
_RUNNER_SPEC.loader.exec_module(_RUNNER)

_SERVER_PATH = Path(__file__).parent / "mcp_server" / "server.py"
_SERVER_SPEC = importlib.util.spec_from_file_location("ppt_mcp_server", _SERVER_PATH)
assert _SERVER_SPEC and _SERVER_SPEC.loader
_SERVER = importlib.util.module_from_spec(_SERVER_SPEC)
sys.path.insert(0, str(_SERVER_PATH.parent))
sys.modules[_SERVER_SPEC.name] = _SERVER
_SERVER_SPEC.loader.exec_module(_SERVER)

_ENGINE_PATH = Path(__file__).parent / "mcp_server" / "pptmaster_engine.py"
_ENGINE_SPEC = importlib.util.spec_from_file_location("pptmaster_engine_for_test", _ENGINE_PATH)
assert _ENGINE_SPEC and _ENGINE_SPEC.loader
_ENGINE = importlib.util.module_from_spec(_ENGINE_SPEC)
sys.modules[_ENGINE_SPEC.name] = _ENGINE
_ENGINE_SPEC.loader.exec_module(_ENGINE)


def _write_deck(root: Path, case: str, refs: list[str], texts: list[str]) -> Path:
    project = root / case / "project"
    (project / "svg_output").mkdir(parents=True)
    (project / "notes").mkdir()
    for idx, text in enumerate(texts, start=1):
        ref = refs[(idx - 1) % len(refs)] if refs else ""
        comment = f"<!-- design_refs: {ref} -->" if ref else ""
        (project / "svg_output" / f"{idx:02d}.svg").write_text(
            (
                '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">'
                f"{comment}"
                '<rect width="1280" height="720" fill="#fff"/>'
                f'<text x="80" y="120">{text}</text>'
                "</svg>"
            ),
            encoding="utf-8",
        )
        note = f"refs={ref}\n" if ref else "mode=wo\n"
        (project / "notes" / f"{idx:02d}.md").write_text(note, encoding="utf-8")
    return project


def test_validate_summary_accepts_prompt_specific_refs(tmp_path):
    project_a = _write_deck(tmp_path, "kids_lesson", ["diagram_skill", "playful_motion"], ["Orbit game", "Draw along"])
    project_b = _write_deck(tmp_path, "legal_review", ["board_table", "risk_matrix"], ["Matter mix", "Risk vote"])
    summary = [
        {
            "case": "kids_lesson",
            "mode": "w",
            "project": str(project_a),
            "refs": ["diagram_skill", "playful_motion"],
            "shape_counts": [3, 4],
            "layout_families": ["cover", "diagram"],
        },
        {
            "case": "legal_review",
            "mode": "w",
            "project": str(project_b),
            "refs": ["board_table", "risk_matrix"],
            "shape_counts": [5, 6],
            "layout_families": ["cover", "matrix"],
        },
    ]
    path = tmp_path / "summary.json"
    path.write_text(json.dumps(summary), encoding="utf-8")

    result = validate_summary(path)

    assert result.ok, result.failures
    assert result.metrics["distinct_ref_sets"] == 2


def test_validate_summary_rejects_template_collapse(tmp_path):
    shared_refs = ["same_cover", "same_metric"]
    project_a = _write_deck(
        tmp_path,
        "restaurant",
        shared_refs,
        ["REFERENCE-ADAPTED STRATEGY DECK", "Five decisions for the room"],
    )
    project_b = _write_deck(
        tmp_path,
        "real_estate",
        shared_refs,
        ["REFERENCE-ADAPTED STRATEGY DECK", "Five decisions for the room"],
    )
    summary = [
        {"case": "restaurant", "mode": "w", "project": str(project_a), "refs": shared_refs, "shape_counts": [7, 7], "layout_families": ["cover", "cover"]},
        {"case": "real_estate", "mode": "w", "project": str(project_b), "refs": shared_refs, "shape_counts": [7, 7], "layout_families": ["cover", "cover"]},
    ]
    path = tmp_path / "summary.json"
    path.write_text(json.dumps(summary), encoding="utf-8")

    result = validate_summary(path)

    assert not result.ok
    joined = "\n".join(result.failures)
    assert "ref set dominates" in joined
    assert "shape signature dominates" in joined
    assert "visible internal/eval label leaked" in joined
    assert "generic skeleton phrase" in joined


def test_runner_infers_expected_domains_for_diverse_briefs():
    fixtures = {
        "product": {
            "title": "Lumen Pro product launch",
            "audience": "bold product launch keynote",
            "core_points": ["semantic search across every doc", "install this week"],
        },
        "kids": {
            "title": "Volcanoes! How mountains breathe fire",
            "audience": "8-year-old kids learning earth science in a classroom",
            "core_points": ["draw a volcano diagram"],
        },
        "restaurant": {
            "title": "Noon Kitchen",
            "audience": "angel investors reviewing a restaurant concept",
            "core_points": ["menu logic", "chef team", "lunch counter"],
        },
        "real_estate": {
            "title": "The Headlands House",
            "audience": "buyer's agent packet for a listing",
            "core_points": ["4 bedrooms", "3.1 acres", "open houses"],
        },
        "esports": {
            "title": "Midnight Reef Esports - Series A",
            "audience": "gaming-focused VC partners",
            "core_points": ["roster", "Twitch audience"],
        },
    }

    for expected, brief in fixtures.items():
        assert _RUNNER.infer_domain(brief) == expected


def test_runner_selects_distinct_reference_sets_for_different_prompts():
    skill_entries = [
        {
            "skill_id": "product_compare",
            "skill_name": "Tiered Feature Comparison Grid",
            "category_path": ["tables", "comparison_grid"],
            "tags": ["product", "feature", "comparison"],
            "applicability": "product launch feature comparison",
        },
        {
            "skill_id": "kids_diagram",
            "skill_name": "Playful Process Diagram",
            "category_path": ["diagram", "process_flow"],
            "tags": ["playful", "diagram", "classroom"],
            "applicability": "kids lesson diagram",
        },
        {
            "skill_id": "finance_dashboard",
            "skill_name": "Executive KPI Dashboard",
            "category_path": ["dashboard", "data"],
            "tags": ["financial", "dashboard", "boardroom"],
            "applicability": "financial boardroom data dashboard",
        },
    ]
    briefs = [
        {"title": "Product launch", "audience": "product launch keynote", "core_points": ["feature grid"]},
        {"title": "Volcano lesson", "audience": "classroom lesson", "core_points": ["playful diagram"]},
        {"title": "Q3 board review", "audience": "quarterly board briefing", "core_points": ["revenue dashboard"]},
    ]

    ref_sets = {tuple(_RUNNER.select_skill_refs(brief, skill_entries, k=2)) for brief in briefs}

    assert len(ref_sets) == len(briefs)


def test_mcp_helper_returns_prompt_specific_refs():
    kids = _SERVER.pptmaster_select_r2s_refs(
        json.dumps(
            {
                "title": "Volcanoes! How mountains breathe fire",
                "audience": "8-year-old kids classroom lesson",
                "core_points": ["diagram magma chamber", "draw activity"],
                "n_slides": 9,
            }
        )
    )
    financial = _SERVER.pptmaster_select_r2s_refs(
        json.dumps(
            {
                "title": "Q3 2026 Board Review",
                "audience": "quarterly board briefing",
                "core_points": ["revenue dashboard", "risk register"],
                "n_slides": 10,
            }
        )
    )

    assert kids["domain"] == "kids"
    assert financial["domain"] == "financial"
    assert set(kids["refs"]) != set(financial["refs"])
    assert "suggested_roles" not in kids
    assert "suggested_roles" not in financial
    assert any("diagram" in item.lower() for item in kids["design_opportunities"])
    assert any("dashboard" in item.lower() for item in financial["design_opportunities"])


def test_validate_open_compare_requires_w_to_improve_wo(tmp_path):
    wo_project = _write_deck(tmp_path, "open_wo", [], ["Open baseline", "No refs"])
    w_project = _write_deck(tmp_path, "open_w", ["skill_a", "skill_b"], ["Open enhanced", "No labels"])
    summary = [
        {
            "case": "case_a",
            "mode": "wo",
            "project": str(wo_project),
            "refs": [],
            "shape_counts": [3, 3],
            "layout_families": ["cover", "cards"],
        },
        {
            "case": "case_a",
            "mode": "w",
            "project": str(w_project),
            "refs": ["skill_a", "skill_b"],
            "shape_counts": [8, 9],
            "layout_families": ["cover", "cards"],
        },
    ]
    path = tmp_path / "summary.json"
    path.write_text(json.dumps(summary), encoding="utf-8")

    result = validate_open_compare(path)

    assert result.ok, result.failures
    assert result.metrics["w_richer_than_wo"] == 1


def test_validator_ignores_none_design_refs_with_comments(tmp_path):
    wo_project = tmp_path / "wo" / "project"
    (wo_project / "svg_output").mkdir(parents=True)
    (wo_project / "notes").mkdir()
    (wo_project / "svg_output" / "01.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><!-- design_refs: none; open baseline comment --><rect width="10" height="10"/></svg>',
        encoding="utf-8",
    )
    (wo_project / "notes" / "01.md").write_text("design_refs: none; no skill refs\n", encoding="utf-8")
    w_project = _write_deck(tmp_path, "w", ["skill_a", "skill_b"], ["Enhanced", "More"])
    summary = [
        {"case": "case_b", "mode": "wo", "project": str(wo_project), "refs": [], "shape_counts": [1], "layout_families": ["cover"]},
        {"case": "case_b", "mode": "w", "project": str(w_project), "refs": ["skill_a", "skill_b"], "shape_counts": [4, 5], "layout_families": ["cover", "cards"]},
    ]
    path = tmp_path / "summary.json"
    path.write_text(json.dumps(summary), encoding="utf-8")

    result = validate_open_compare(path)

    assert result.ok, result.failures


def test_validator_ignores_no_skills_baseline_sentinel(tmp_path):
    wo_project = tmp_path / "wo_baseline" / "project"
    (wo_project / "svg_output").mkdir(parents=True)
    (wo_project / "notes").mkdir()
    (wo_project / "svg_output" / "01.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><!-- design_refs: no-skills-baseline --><rect width="10" height="10"/></svg>',
        encoding="utf-8",
    )
    (wo_project / "notes" / "01.md").write_text("design_refs: no-skills-baseline\n", encoding="utf-8")
    w_project = _write_deck(tmp_path, "w_baseline", ["skill_a", "skill_b"], ["Enhanced", "More"])
    summary = [
        {"case": "case_c", "mode": "wo", "project": str(wo_project), "refs": [], "shape_counts": [1], "layout_families": ["cover"]},
        {"case": "case_c", "mode": "w", "project": str(w_project), "refs": ["skill_a", "skill_b"], "shape_counts": [4, 5], "layout_families": ["cover", "cards"]},
    ]
    path = tmp_path / "summary.json"
    path.write_text(json.dumps(summary), encoding="utf-8")

    result = validate_open_compare(path)

    assert result.ok, result.failures


def test_pptmaster_layout_validate_project_strict(tmp_path):
    meta = _ENGINE.create_project("layout_ok", base_dir=str(tmp_path))
    project = Path(meta["project_path"])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
        '<rect width="1280" height="720" fill="#fff"/>'
        '<text x="100" y="120" font-size="32">Short title</text>'
        '<rect x="100" y="180" width="300" height="120" rx="18" fill="#ddd"/>'
        "</svg>"
    )
    _ENGINE.write_svg_slide(str(project), svg, slide_name="01_ok")

    report = _ENGINE.validate_project(str(project), strict=True)

    assert report["ok"], report


def test_pptmaster_layout_strict_export_blocks_bad_svg(tmp_path):
    meta = _ENGINE.create_project("layout_bad", base_dir=str(tmp_path))
    project = Path(meta["project_path"])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
        '<rect width="1280" height="720" fill="#fff"/>'
        '<text x="1240" y="120" font-size="44">This title is intentionally far too long for the slide edge</text>'
        "</svg>"
    )
    _ENGINE.write_svg_slide(str(project), svg, slide_name="01_bad")

    report = _ENGINE.validate_project(str(project), strict=True)

    assert not report["ok"]
    assert report["error_count"] > 0


def test_pptmaster_layout_strict_catches_text_on_connector(tmp_path):
    meta = _ENGINE.create_project("layout_connector_bad", base_dir=str(tmp_path))
    project = Path(meta["project_path"])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
        '<rect width="1280" height="720" fill="#fff"/>'
        '<path d="M100 200 L800 200" stroke="#f00" stroke-width="10" fill="none"/>'
        '<text x="420" y="208" font-size="24">on top of line</text>'
        "</svg>"
    )
    _ENGINE.write_svg_slide(str(project), svg, slide_name="01_bad_connector")

    report = _ENGINE.validate_project(str(project), strict=True)

    assert not report["ok"]
    joined = "\n".join(issue for slide in report["slides"] for issue in slide["errors"])
    assert "connector" in joined
