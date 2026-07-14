# PPTMaster x Resource2Skill Integration Contract

This contract defines the target state for using PPTMaster as an SVG-first
editable-PPTX backend while letting Resource2Skill guide visual design through
prompt-specific skill references.

## Ownership Boundary

PPTMaster remains the execution layer:

- create and manage SVG-first PPT projects
- add, read, replace, and delete SVG slide source
- import and inspect PPTX/template assets
- export SVG projects to native editable PPTX
- accept arbitrary valid SVG input without requiring Resource2Skill

Resource2Skill remains the optional design-reference layer:

- search and select prompt-relevant PPT skills
- inspect selected skill text, code, and visual evidence
- extract transferable visual mechanisms from those skills
- adapt those mechanisms into the downstream SVG source
- record audit trace in SVG comments, notes, or metadata

For the LLM/MCP path, `pptmaster_select_r2s_refs(task_description, ...)`
provides the prompt-specific reference policy as a callable helper. Agents
should call it before writing PPTMaster SVG, then inspect and adapt the returned
refs. Its design opportunities are non-binding affordances, not slide roles or
a deck skeleton; PPTMaster's own open-ended planning decides slide count,
ordering, layout, and template usage from the prompt. This helper is
intentionally outside `pptmaster_engine.py`; the backend continues to accept
plain SVG without Resource2Skill.

PPTMaster must not hard-code Resource2Skill policy, skill IDs, deck skeletons,
or prompt interpretation. Resource2Skill must not reduce PPTMaster to one fixed
template factory.

## Non-Negotiable Invariants

1. **PPTMaster standalone compatibility**
   - `pptmaster_create_project -> pptmaster_add_svg_slide ->
     pptmaster_export_project` works without skill discovery.
   - Template import/list/get/copy behavior remains available.
   - Exported PPTX should preserve editable native shapes and text where the
     upstream SVG-to-PPTX converter supports them.

2. **Prompt-specific skill selection**
   - With skill tools available, every deck chooses at least two long-tail PPT
     references that match the prompt's audience, tone, and domain.
   - A multi-prompt evaluation must not reuse the same reference set for every
     prompt.
   - Generic deck scaffolds, shell IDs, or template IDs are not sufficient
     Resource2Skill references by themselves.

3. **Mechanism transfer, not slide cloning**
   - Skill references are used as visual/code evidence, not as whole-slide
     source to copy.
   - The resulting SVG should visibly adapt mechanisms such as masked image
     reveal, kinetic typography, chart choreography, editorial split layout,
     Swiss grid, process flow, card depth, or cinematic image staging.
   - The mechanism must be rewritten for the current prompt's content.
   - Each slide should have one primary transferred mechanism. Other refs may
     influence minor styling, but must not create a second competing main
     visual. Teaching or explainer pages should have one conceptual center with
     precise labels/connectors.

4. **No template collapse**
   - Different prompts should produce different slide role sequences, page
     topology, and domain-specific visual grammar.
   - Respect explicit `n_slides`, `role_prefer`, and `role_avoid` from the
     brief unless the prompt itself asks for compression.
   - A batch where every deck has the same six pages, same reference set, and
     only different text/colors is a failed integration run.

5. **Clean audit trace**
   - Per-slide `design_refs` are recorded in SVG comments, notes, or metadata.
   - Audit trace must not appear as visible slide text.
   - Forbidden visible phrases include experiment labels such as
     `REFERENCE-ADAPTED`, `w/ skill mechanisms rewritten`, and other internal
     evaluation markers.

## Domain-Specific Expectations

These are examples of the level of prompt sensitivity expected in a diverse
batch:

- Kids lesson: diagrams, visual analogies, class activities, playful pacing.
- Restaurant pitch: menu logic, opening plan, unit economics, neighborhood
  scene, food/service imagery.
- Real estate packet: property gallery, map/location logic, features table,
  comparable-sales factsheet.
- Legal or financial review: restrained boardroom density, tables, risks,
  decisions, clear data hierarchy.
- Research talk: method pipeline, evidence trace, claims/limitations, results,
  related-work positioning.
- Esports or creative pitch: roster/media moments, cinematic covers, bold
  metrics, brand/world-building.

## Acceptance Gates

An integration run is acceptable only when all gates pass:

1. **Standalone backend gate**
   - A smoke test proves PPTMaster can export at least one arbitrary SVG deck
     without Resource2Skill references.

2. **Reference diversity gate**
   - Across a diverse batch, at least half of the decks have distinct selected
     reference sets.
   - No single reference set is used by every deck.

3. **Mechanism evidence gate**
   - Each deck has at least two unique `design_refs` recorded.
   - At least two slides per deck show `design_refs` in SVG comments or notes.

4. **Anti-collapse gate**
   - No single slide-count/shape-count signature dominates the batch.
   - No one generic phrase family appears across most decks as visible text.
   - The run respects prompt slide counts and role preferences when provided.

5. **Visual cleanliness gate**
   - No visible scratch or debug labels.
   - SVG text overflow warnings are fixed before export.
   - Contact sheets or rendered slides show domain-specific differences beyond
     palette swaps.
   - Quality runs call `pptmaster_validate_project(strict=true)`
     before export, then export with `layout_strict=true` after repairing any
     blocking layout errors.

## Validation Artifact

Use `domains/ppt/validate_pptmaster_r2s_run.py` on batch outputs that include
`summary.json` entries with `project`, `case`, `mode`, `refs`, `shape_counts`,
and render metadata. The validator is intentionally structural: it catches
obvious policy failures before any human/VLM visual review. Passing it is
necessary but not sufficient; final acceptance still requires visual inspection
of rendered decks.

For paired open-baseline runs, use:

```bash
python domains/ppt/validate_pptmaster_r2s_run.py <summary.json> --compare-open
```

This checks that `wo` stays a true no-R2S PPTMaster baseline, that `w` has
prompt-specific refs, and that the R2S-enhanced output is structurally richer
than the corresponding open baseline.

`domains/ppt/pptmaster_r2s_prompt_runner.py` is a deterministic reference
runner for this contract. It reads brief JSON files, selects prompt-specific
Resource2Skill PPT references, writes PPTMaster SVG projects with per-slide
`design_refs`, exports editable PPTX, and emits the `summary.json` consumed by
the validator. It is a regression harness for integration behavior, not a
replacement for the LLM agent path.
