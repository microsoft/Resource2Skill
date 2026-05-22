# Resource2Skill: Distilling Executable Skills from Human-Created Resources for Software Agents

[![Project](https://img.shields.io/badge/Project-Resource2Skill-blue)](#)
[![Paper](https://img.shields.io/badge/Paper-arXiv%20preprint-lightgrey)](#)
[![Code](https://img.shields.io/badge/Code-Open%20Source-green)](#)

<p align="center">
  <img src="assets/teaser.png" alt="Resource2Skill overview" width="92%">
</p>

Resource2Skill is a runtime and skill-library system for software agents. It
converts human-created resources such as tutorial videos, reference artifacts,
articles, and code examples into reusable executable skills. At inference time,
an agent can browse a domain-specific skill wiki, inspect text/code/visual
evidence, compose relevant skills, and operate real software tools to create
artifacts.

The paper is available as an arXiv preprint. We are releasing the runtime and
skill libraries first; full benchmark orchestration, score aggregation, and
private evaluation artifacts are not included in this public repository.

## Highlights

- **Executable skills from resources.** Skills include procedural text, code
  assets, visual references, metadata, and runtime application hooks.
- **Hierarchical LM Wiki.** Each domain exposes a structured skill wiki for
  browsing, search, inspection, and skill application.
- **Multi-domain artifact generation.** The current release supports Web,
  PowerPoint, Excel, Blender, and REAPER-style audio generation.
- **Real tool execution.** Domains run through MCP servers and produce actual
  files such as `.html`, `.pptx`, `.xlsx`, `.blend`, `.png`, `.mid`, and `.wav`.
- **Open runtime boundary.** This repository focuses on the runnable system and
  skill libraries, while internal experiments and private evaluation artifacts
  remain outside the public release.

## Supported Domains

| Domain | Status | Output |
| --- | --- | --- |
| Web | Released | HTML/CSS/JS pages |
| PowerPoint | Released | `.pptx` decks |
| Excel | Released | `.xlsx` workbooks |
| Blender | Released | `.blend` scenes and rendered images |
| REAPER-style audio | Released | MIDI/WAV music projects |
| CAD | Coming soon | Data and release packaging are still being coordinated |
| UE5 | Coming soon | Data and release packaging are still being coordinated |

## Method Overview

Resource2Skill separates resource learning from task-time execution:

1. **Resource ingestion.** Human-created multimodal resources are processed into
   candidate procedural knowledge.
2. **Skill distillation.** Each candidate is normalized into a reusable skill
   entry with metadata, applicability, text explanations, code, and optional
   visual evidence.
3. **Skill wiki construction.** Skills are organized by domain, tier, category,
   tags, and source information.
4. **Agent execution.** Given a task, the agent browses or searches the wiki,
   inspects relevant skills, composes them, and executes through domain MCP
   tools.

## Repository Layout

```text
cli.py                 Unified command-line entry point
core/                  Agent runtime, MCP adapter, skill wiki, retrieval logic
domains/               Domain configs, prompts, MCP servers, tool adapters
skills_wiki/           Active structured skill wiki used by runtime discovery
skills_library/        Executable assets, helper code, and compatibility files
briefs/                Small task briefs
briefs_showcase/       Curated showcase prompts
examples/              Example case prompts
fixtures/              Lightweight fixture data for skill/wiki checks
```

The following are intentionally excluded from this public release:

```text
experiments/           Internal benchmark runs and ablations
bench/                 Internal benchmark wrappers and historical results
reports/               Internal reports
demo/                  Generated artifacts
scripts/               Internal experiment/scoring/orchestration scripts
docs/                  Private notes and paper-supporting experiment docs
```

## Installation

Use Python 3.10+ in a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install common dependencies plus domain-specific MCP dependencies:

```bash
python -m pip install mcp fastmcp python-dotenv pyyaml requests pillow lxml
python -m pip install -r domains/web/mcp_server/requirements.txt
python -m pip install -r domains/ppt/mcp_server/requirements.txt
python -m pip install -r domains/excel/mcp_server/requirements.txt
python -m pip install -r domains/blender/mcp_server/requirements.txt
python -m pip install -r domains/reaper/mcp_server/requirements.txt
```

Optional system dependencies:

- `web`: Playwright/Chromium for visual inspection.
- `ppt`: LibreOffice for rendering slides.
- `blender`: Blender for scene execution and rendering.
- `reaper`: `fluidsynth` plus a GM soundfont for WAV rendering.

## Model Configuration

Copy the example environment file and fill in your provider settings:

```bash
cp .env.example .env
```

For Azure OpenAI:

```text
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
```

For per-model deployments, use model-specific overrides from `.env.example`,
for example `AZURE_OPENAI_ENDPOINT_54` and `AZURE_OPENAI_DEPLOYMENT_54`.

If your Azure resource requires Entra ID/AAD instead of API keys:

```text
AZURE_OPENAI_USE_AAD=1
```

## Quick Start

List available domains:

```bash
python cli.py domains
```

Validate released domains:

```bash
python cli.py validate-domain --domain web
python cli.py validate-domain --domain ppt
python cli.py validate-domain --domain excel
python cli.py validate-domain --domain blender
python cli.py validate-domain --domain reaper
```

Run a case:

```bash
python cli.py agent \
  --domain web \
  --task "Build a one-page landing site for a neighborhood arts nonprofit called Quartz. Use a warm hand-made editorial style, include programs, impact, donation tiers, FAQ, and a footer. Save and STOP." \
  --model gpt-5.4 \
  --reasoning low \
  --max-iter 40
```

More example prompts are available in:

```text
examples/case_prompts.json
```

## Example Commands

PowerPoint:

```bash
python cli.py agent \
  --domain ppt \
  --task "Build an 8-slide strategy deck for a renewable energy startup called Dune Renewables. Include cover, agenda, market pull, where to play, entry model, roadmap, risks, and closing ask. Save and STOP." \
  --model gpt-5.4 \
  --reasoning low \
  --max-iter 80
```

Excel:

```bash
python cli.py agent \
  --domain excel \
  --task "Build a 4-sheet manufacturing defects workbook with Summary, Defect Log, Products, and Production Lines. Include realistic data, formulas, tables, and one summary chart. Save and STOP." \
  --model gpt-5.4 \
  --reasoning low \
  --max-iter 50
```

Blender:

```bash
python cli.py agent \
  --domain blender \
  --task "Build a moody product hero scene with stacked books and a lit candle on a tabletop. Use warm side lighting, realistic materials, and a close editorial camera. Save and STOP." \
  --model gpt-5.4 \
  --reasoning low \
  --max-iter 60
```

REAPER-style audio:

```bash
python cli.py agent \
  --domain reaper \
  --task "Compose a 24-bar psychedelic rock track in G minor at 150 BPM with drums, bass, harmonic instrument, lead element, arrangement sections, and a rendered WAV. Save and STOP." \
  --model gpt-5.4 \
  --reasoning low \
  --max-iter 80
```

## Skill Libraries

Resource2Skill uses two library roots:

- `skills_wiki/<domain>/`: active structured wiki entries used for runtime
  discovery and inspection.
- `skills_library/<domain>/`: executable assets, helper modules, shell
  templates, and compatibility resources used by domain MCP servers.

Both are required for the current release.

## Notes

- Generated artifacts are written under `demo/<domain>/` by default and are
  ignored by git.
- Some visual/audio review hooks require model credentials. When unavailable,
  agents may skip or work around those hooks while still producing artifacts.
- The released code is intended for running and extending the skill runtime,
  not for reproducing internal benchmark tables.

## Citation

The arXiv citation will be added before public release.

## License

This project is released under the MIT License. See `LICENSE`.
