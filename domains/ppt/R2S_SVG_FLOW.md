# How Resource2Skill skills are applied to PowerPoint (PPT Master + svg_recipe)

This note documents how R2S skills actually reach a generated deck, the bugs that
silently prevented it, the fix that now makes a distilled wiki skill **visibly and
attributably** render on real slides, and how to reproduce/verify a with/without
pair. Last audited & fixed 2026-06-24.

## TL;DR

- PPT execution uses the **PPT Master** SVG-first backend (authored SVG slides →
  editable native PowerPoint shapes). It does **not** execute the python-pptx code
  stored in each skill's `code/skill.py`.
- Every PPT skill in `skills_wiki/ppt/<id>/` ships an **`svg_recipe.md`** — the SVG
  construction recipe (layout grids, hero-metric cards, neon hubs, editorial
  interstitials, masked reveals, motion paths, …). This is the distilled,
  SVG-native form of the skill.
- The canonical path is
  **`domains/ppt/pptmaster_r2s_prompt_runner.py --mode both`**. For the **with-R2S**
  deck it (1) selects the most relevant skill IDs for the brief (keyword pre-filter →
  GPT-5.5 rerank by tone), (2) ranks them by distinctiveness, and (3) for each of the
  **four content slides (2, 3, 4, 5)** calls **GPT-5.4 to AUTHOR a fresh SVG slide**:
  the chosen skill's `svg_recipe` is handed to the model as a *design reference* (its
  layout structure, palette, shapes, signature mechanism) together with **this slide's
  real content**, and the model lays out that content in the skill's style. So the
  skill is genuinely *applied to the deck's own content* — not pasted text into the
  skill's static example. The cover (1) and close (last) stay the genuine PPT Master
  template; the **without-R2S** deck is the genuine PPT Master template throughout
  (NOT degraded). PPT Master then converts each SVG to native .pptx shapes.
  Fallback chain per content slide: LLM author → deterministic recipe-fill →
  open template (so a slow/invalid LLM call can never crash the deck).

## What went wrong (all fixed except the agent-path follow-up)

Auditing the first PPT comparison batch showed the wiki SVG skills were **not
actually applied**. Three causes:

1. **A crash bug.** The runner imported `from datetime import UTC`; `datetime.UTC`
   only exists in Python ≥ 3.11 but the runtime env is 3.10, so the skill-selection
   step (`pptmaster_select_r2s_refs`) raised `ImportError` and returned nothing.
   **Fixed**: `from datetime import timezone` + `UTC = timezone.utc`.

2. **A fake "skill" overlay.** Even once skills were selected, the runner did not
   render their recipes. A helper `_r2s_mechanism_overlay()` picked **1 of 5 generic
   decorations by `hash(skill_name) % 5`** and stamped it on template slides — the
   real `svg_recipe` was never drawn. Selecting a skill changed a hash, not the
   slide. **Fixed**: removed that overlay; added real recipe rendering (below).

3. **A prompt mismatch (still open).** The LLM agent prompt
   (`domains/ppt/agent_prompt.md`) is written for the *old python-pptx* path — it
   tells the agent to call `get-skill-code` and extract gradient/animation **XML**,
   and never mentions `svg_recipe`. So the **agent** path (`cli.py agent --domain
   ppt`) still doesn't apply SVG skills. Until that prompt is reworked, the
   **runner is the canonical R2S→PPT path** and is what the project-page pairs use.

## The fix (real recipe rendering)

In `pptmaster_r2s_prompt_runner.py`:

- `RECIPE_SLIDE_INDICES = (2, 3, 4, 5)` — the content slides that become skill-recipe
  slides under R2S (cover + close stay the genuine PPT Master template).
- `_load_recipe_svg(skill_id)` — reads `skills_wiki/ppt/<id>/svg_recipe.md` and
  extracts its ```svg block.
- `_recipe_distinctiveness(skill_id)` — ranks a skill by how much real mechanism its
  recipe carries (`<filter>`, `clipPath`, `<mask>`, `feGaussianBlur` counts), so the
  *most visually distinctive* selected skills are the ones rendered.
- `_llm_skill_slide(...)` — **the primary path.** Hands the skill's `svg_recipe`
  (capped to ~6.5K chars) to GPT-5.4 (`reasoning="medium"`, `max_completion_tokens=20000`)
  as a *design reference*, plus this slide's real headline + points, and asks for a
  fresh 1280×720 SVG that applies the skill's approach to that content. The prompt
  forbids copying the reference's example text, overlapping shapes, empty image/
  mockup placeholders, and overflowing/duplicated titles.
- `_clean_llm_svg(text)` — extracts `<svg>…</svg>`, strips any `<image>`/`foreignObject`,
  repairs bare `&`, forces width/height/viewBox to 1280×720, and validates it parses;
  returns `None` (→ fallback) if the model truncated or emitted invalid XML.
  (Token budget matters: complex slides truncate below ~16K completion tokens, which
  silently drops them to the fallback — keep it ≥ 20K.)
- `_recipe_svg_slide(skill_id, headline, supports)` — **fallback** that renders the
  recipe verbatim with this deck's copy substituted into the largest `<text>` nodes:
  - strips placeholder `<image href="https://images.example.com/…">` photos (they
    can't load and break SVG→PPTX export; the gradients/masks/filters/shapes/text —
    i.e. the actual mechanism — stay intact);
  - substitutes this deck's copy into the recipe's **largest-font** `<text>` nodes
    (headline + supports), leaving the small structural labels (column guides,
    "MODULE / 01", grid baselines) intact so the skill's structure stays legible;
  - **auto-fits** each substitution to the placeholder's own character capacity so
    longer deck copy doesn't overflow/clip the box;
  - repairs bare ampersands ("R&D") and, as a final guard, validates the result
    parses as XML — if a recipe is still malformed it returns `None` and that one
    slide falls back to the template (a bad recipe can't crash the deck).
- `build_deck` selects `k=4` skills and assigns them to slides 2, 3, 4 & 5 (one
  distinct skill each, most-distinctive first). For each it calls `_llm_skill_slide`
  first (`layout_family = "skill_llm"`); on `None` it falls back to `_recipe_svg_slide`
  (`"skill_recipe"`), then the open template. Set `PPT_LLM_SLIDES=0` to force the
  deterministic path. (Generation driver: `/data/tmp/ppt_fix/regen_all.py`, ~5 LLM
  calls per deck; run it at low concurrency — the local proxy serialises, so 4-way
  concurrency times some calls out into the fallback. Re-render from the **newest**
  `*/w/*/svg_output` dir; the runner versions project dirs on re-run.)
- The **without** deck calls `render_slide(..., use_r2s=False)` with **no** recipe
  slides, so it is the *genuine PPT Master template deck* (styled cards, charts, real
  cover/close). The baseline is deliberately NOT degraded — an earlier attempt to
  force a constant difference by rendering the without deck as plain white
  title+bullets was a strawman and was reverted. The honest difference is generic
  PPT Master template (without) vs the four R2S-redesigned content slides (with);
  cover + close are identical PPT Master bookends.

## Verification (2026-06-24)

- **Provenance.** Each run's `summary.json` `w` record carries `refs` (selected skill
  IDs), `ref_details` (name/category/applicability), and `layout_families`. Across
  all 8 project-page briefs the with-deck reports `recipe_slides == [2, 3, 4, 5]` (the
  recipe landed on all four content slides every time); the `wo` record has
  `refs == []` (genuine PPT Master template throughout).
- **SVG-level.** On the restaurant brief, with-deck slide 2 contains `4 clipPath,
  2 feGaussianBlur, 2 linearGradient` (the Editorial Split-Grid mechanism); the
  baseline slide 2 contains none.
- **Visual.** Rendered slide 2 differs unmistakably per domain — esports → *Neon
  Circular Hub Team Roster* (8 neon-ringed nodes around a glowing hub); healthtech →
  *High Data-Ink Dashboard* + Gantt; kids → *Animated Process Trajectory* motion
  path; nonprofit → *High-Impact Geometric Quote Reveal* — while every baseline stays
  a plain card template. (See `_review_ppt/FIXED_*.png`.)

## Reproduce a verified with/without pair

```bash
# brief JSON fields: variant_id, title, audience, tone_words[], mood_preference[],
# n_slides, core_points[] (6-8 strings)
AZURE_OPENAI_ENDPOINT=http://127.0.0.1:18082/ AZURE_OPENAI_API_KEY=local-proxy \
AZURE_OPENAI_USE_AAD=0 \
conda run -n openai python domains/ppt/pptmaster_r2s_prompt_runner.py \
  path/to/brief.json --mode both --max-slides 6 --out OUTDIR

# OUTDIR/<case>/w/<...>/  = with R2S (slides 2,3,4,5 from svg_recipe; see summary.json refs)
# OUTDIR/<case>/wo/<...>/ = baseline (templates only, refs == [])
# each has svg_output/*.svg + exports/*.pptx
```

The project-page showcase clips (`project_page/assets/videos/ppt_<slug>_with.mp4`
and `_without.mp4`) are rendered from these decks' SVG slides
(`domains/ppt/` driver → playwright PNG per slide → ffmpeg loop). The 8 pairs and
their applied-skill notes are recorded in `/data/tmp/r2s_partb/ppt_fixed.json`.

## Open follow-up

- Rework `domains/ppt/agent_prompt.md` to mandate the
  `pptmaster_select_r2s_refs → get_skill_text(id).svg_recipe` flow so the **LLM
  agent** path (not just the deterministic runner) applies SVG skills — then the PPT
  comparison can be agent-based and consistent with the other domains.
