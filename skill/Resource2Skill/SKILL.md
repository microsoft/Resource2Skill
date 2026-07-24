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

Set the backend once per shell or task:

```bash
# Use a local agent CLI instead of API keys
export R2S_LLM_BACKEND=cli
export R2S_CLI_TOOL=claude   # claude | codex | kimi | omp

# Optional: use subtitle+keyframes for video analysis (no Gemini key)
export R2S_VIDEO_BACKEND=cli
```

If you leave these unset, Resource2Skill falls back to its original behavior:
`AZURE_OPENAI_API_KEY` for agent reasoning and `GEMINI_API_KEY` for video analysis.

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

## Output layout

- `skills_wiki/<domain>/` — structured, searchable skill entries.
- `skills_library/<domain>/` — executable code assets used by the agent loop.
- Results written with `-o` go to the path you specify.

## Key limitations

- `R2S_VIDEO_BACKEND=cli` currently supports image ingestion best with `claude`, because claude can read local image files in headless mode. kimi, codex, and omp either lack image input or have not been verified.
- The CLI LLM backend currently implements `claude` first; codex/kimi/omp backends are planned.
- Embeddings (`python cli.py build`) still require a Gemini key unless you rely on keyword-only retrieval.

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
