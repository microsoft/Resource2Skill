---
name: Resource2Skill
author: Resource2Skill project
description: Drive the Resource2Skill CLI from an agent session. No LLM API key is required if the target machine has claude/codex/kimi/omp installed and logged in.
---

# Resource2Skill

Operate the Resource2Skill skill-distillation harness from within an agent session.

## When to use

- The user wants to turn a YouTube tutorial, article, repo, or reference artifact into an executable agent skill.
- The user wants to search, inspect, or execute skills in the local `skills_library/`.
- The user wants to run the agent loop to build a web page, PowerPoint deck, Excel workbook, Blender scene, or REAPER-style audio project using the skill library.

## Prerequisites

- Python 3.11+ and the project dependencies installed:
  ```bash
  cd /path/to/Resource2Skill
  pip install -r requirements.txt
  ```
- `yt-dlp` and `ffmpeg` on PATH for the video-analysis path.
- At least one local agent CLI installed and authenticated (Claude Code is best supported):
  - `claude` (Claude Code)
  - `codex` (OpenAI Codex CLI)
  - `kimi` (Moonshot Kimi Code CLI)
  - `omp` (Oh My Pi agent harness)

## Configuration

The fastest way is to create a `.env` file in the repo root:

```bash
cp .env.example .env
# edit .env and uncomment the CLI backend lines
```

`.env` is **not** automatically read by the OS; `cli.py` uses `python-dotenv` to
load it when you run a command.

You can also export per shell:

```bash
# Use a local agent CLI instead of API keys
export R2S_LLM_BACKEND=cli
export R2S_CLI_TOOL=claude   # claude | codex | kimi | omp

# Optional: use subtitle+keyframes for video analysis (no Gemini key)
export R2S_VIDEO_BACKEND=cli

# Optional: if native subtitles are missing, generate them with local ASR
export R2S_VIDEO_ASR=auto    # auto | faster-whisper | whisper
export R2S_VIDEO_ASR_MODEL=tiny  # tiny | base | small
```

### Default behavior when no keys are set

If you leave the variables unset, the system will **auto-detect** a keyless path
whenever possible:

- If `AZURE_OPENAI_API_KEY` is missing and an agent CLI (`claude`, `codex`,
  `kimi`, `omp`) is on PATH, `R2S_LLM_BACKEND` defaults to `cli`.
- If `GEMINI_API_KEY` is missing, `R2S_VIDEO_BACKEND` defaults to `cli`
  (subtitle + keyframes).
- If `R2S_VIDEO_ASR=auto` is set and `faster-whisper` or `openai-whisper` is
  installed, missing native subtitles fall back to local ASR on the audio track.

So on a machine with `claude`, `yt-dlp`, and `faster-whisper` installed, you can
often run without setting anything manually.

## Commands

All commands run from the repository root.

### Discover available domains

```bash
python cli.py domains
```

Use this to list the supported authoring domains (web, ppt, excel, blender, reaper).

### Distill a skill from a YouTube video

```bash
python cli.py analyze --domain web \
  --video "https://www.youtube.com/watch?v=yefgBA1CecI" \
  -o /tmp/typewriter_skill.md
```

The command writes a Markdown skill analysis. With `R2S_VIDEO_BACKEND=cli` it uses
yt-dlp subtitles + ffmpeg keyframes instead of Gemini video understanding.

### Run the agent loop to execute a task

```bash
python cli.py agent --domain web \
  --task "Build a responsive glassmorphism navigation bar" \
  --dry-run
```

`--dry-run` uses a mock MCP server so the agent plans and shows tool calls without
muting real files. Remove `--dry-run` to let the agent write files through the domain MCP server.

### Retrieve skills for a query

```bash
python cli.py retrieve --domain web --query "typewriter animation" --select 3
```

Returns the top-3 matching skills from `skills_library/web/`.

### Validate a domain configuration

```bash
python cli.py validate-domain --domain web
```

Run this after changing a domain YAML or before a long agent loop to catch config errors early.

## How skills are stored and discovered

Resource2Skill keeps skills in two roots:

- `skills_wiki/<domain>/` — browse/search entries. Each skill has
  `code/skill.json` (metadata + code pointers) and `text/overview.md` (human
  readable summary).
- `skills_library/<domain>/` — executable assets. Each skill is a folder
  containing `skill.json` plus any code, frames, or helper files.

The `skill.json` file is **not** a Markdown skill file. It is structured JSON
with fields such as `skill_id`, `skill_name`, `domain`, `source` (provenance),
`analysis` (the Markdown distillation), and executable code. Use the CLI or read
the JSON directly.

### Search for a skill

```bash
python cli.py retrieve --domain web --query "typewriter animation" --select 3
```

This returns the top matching skills from `skills_library/web/`. The query can
use natural language; keyword fallback works even without embedding keys.

### Inspect a specific skill

Option 1 — read the JSON directly:

```bash
cat skills_library/web/animation/dynamic_pure_css_typewriter_effect_12449511/skill.json
```

Option 2 — use the agent loop dry-run to see how the skill would be executed:

```bash
python cli.py execute --domain web \
  --skill dynamic_pure_css_typewriter_effect_12449511 \
  --dry-run
```

### List skills in a domain

```bash
find skills_library/web -name skill.json | head -20
```

## Output layout

- `skills_wiki/<domain>/` — structured, searchable skill entries.
- `skills_library/<domain>/` — executable code assets used by the agent loop.
- Results written with `-o` go to the path you specify.

## Key limitations

- `R2S_VIDEO_BACKEND=cli` currently supports image ingestion best with `claude`, because claude can read local image files in headless mode. kimi, codex, and omp either lack image input or have not been verified.
- The CLI LLM backend currently implements `claude` first; codex/kimi/omp backends are planned.
- Embeddings (`python cli.py build`) still require a Gemini key unless you rely on keyword-only retrieval.
- ASR fallback (`R2S_VIDEO_ASR`) requires `faster-whisper` or `openai-whisper` and first model download is ~40MB (`tiny`) to ~150MB (`base`). Transcription speed depends on CPU; Apple Silicon with `faster-whisper` int8 is usable for short videos.

## Examples

```bash
# 1. Keyless skill distillation from a short web tutorial
export R2S_LLM_BACKEND=cli
export R2S_CLI_TOOL=claude
export R2S_VIDEO_BACKEND=cli
python cli.py analyze --domain web \
  --video "https://www.youtube.com/watch?v=yefgBA1CecI" \
  -o /tmp/typewriter_skill.md

# 2. Keyless agent loop (dry-run) for a web component
python cli.py agent --domain web \
  --task "Create a pure-CSS typewriter hero text effect" \
  --dry-run
```
