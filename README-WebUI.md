# Resource2Skill · WebUI Manual (Domain-Agnostic / Generic)

> This repository wraps a local visual shell (FastAPI + Vue3) around the Microsoft
> `Resource2Skill` engine. This manual covers **the generic WebUI line** — the engine and
> UI are fully domain-agnostic; all domain behavior comes 100% from `domain.yaml` plus that
> domain's `mcp_server/server.py`. The repo ships several official example domains
> (`ppt` / `web` / `excel` / `blender` / `reaper`, see `domains/`) that can be cloned,
> deleted, or replaced. Upstream generic docs live in `README.md`.

The whole thing has three parts:

- **Backend**: FastAPI (`webui/backend/`), a single-worker serial task queue shared by
  distillation and the Agent.
- **Frontend**: Vue3 + Element Plus (`webui/frontend/`), pure local `localhost`, single-user.
- **Data isolation**: there is only one copy of the engine code; a "project" is an
  independent data directory (`webui/projects/<project>/`, containing
  `domains/ fixtures/ skills_library/ output/ + project.json`). At task execution time the
  `cwd` is switched to the project root, so R2S relative paths take effect naturally —
  **no need to refactor `core`**.
- **Domain-driven**: each domain ships its own `domain.yaml` (persona / categories / mcp /
  agent prompts) and an MCP server (`domains/<domain>/mcp_server/server.py`) that exposes the
  distilled skills as tools the Agent can call. **Switching domains = swapping these two
  config files; the UI needs zero changes.**

---

## 1. Environment Setup

### 1.1 Python (backend + distillation + Agent)

```bash
# 3.11/3.12 works fine (only the Blender domain forces 3.11; most domains don't need it)
cd Resource2Skill
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # includes mcp>=1.26, python-pptx, openpyxl, etc.
```

> ⚠️ `mcp` must be `>=1.26`. On 1.10.x every MCP server in this repo crashes at import
> (`issubclass() arg 1 must be a class`), because the servers use
> `from __future__ import annotations`.

### 1.2 Node (frontend)

```bash
cd webui/frontend
npm install
```

### 1.3 LLM access (distillation and the Agent both depend on it)

Distillation really calls an LLM to extract / chunk / generate skills; the Agent calls it
too. First prepare an OpenAI-compatible endpoint (DeepSeek / Azure OpenAI / local Ollama /
any self-hosted OpenAI-compatible server all work).

- In the WebUI **"LLM Configuration"** page, add a template: `provider`
  (azure/openai/deepseek/ollama/custom), `endpoint`, `api_key`, `model`, then click
  **"Test"** to verify connectivity.
- Or via API: `POST /api/llm`, body schema in `webui/backend/models.py` (`LLMTemplate`).

> Don't want to wire up an LLM? Distillation supports **dry-run**: it only validates the
> "extract → chunk → write skill library" pipeline without calling the model.

---

## 2. Launch

### 2.1 Backend (FastAPI, port 8000)

```bash
cd webui
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

> The backend uses **relative imports**, so it must be started from the `webui/` directory
> (`backend.main:app`), not a bare `uvicorn main:app`.
> Health check: `GET http://127.0.0.1:8000/api/health`.

### 2.2 Frontend (Vite dev, port 5172)

```bash
cd webui/frontend
npm run dev
```

Open `http://localhost:5172` in the browser (the dev server binds only `localhost` / IPv6
`::1`; use `localhost` rather than `127.0.0.1`).

> **Windows path gotcha (must read)**: if your local `C:\Users\...` is a junction to
> `D:\workbuddy\...`, running `vite build` from the `C:` path raises a
> `fileName absolute path` error. Fix: launch from the **real D: path**
> (`webui/frontend/`); if HMR misbehaves, first `taskkill` any leftover `vite preview`
> or old process occupying 5172/5173, then restart the dev server.

---

## 3. Distillation Tutorial (turn materials into executable skills)

There is exactly one distillation entry point:
**`POST /api/projects/{name}/domains/{domain}/distill`**, triggered from the WebUI's
**"Distillation Workbench"** or **"Materials Management"**. Under the hood it goes through
`core/collector.py` → categorizes by `domain.yaml`'s `categories` → writes
`project_root/skills_library/<domain>/index.json` plus one directory per skill.

> Distillation is domain-agnostic: switching domains only swaps `categories` and prompts —
> **the engine code does not change**.

### 3.1 Steps at a glance (WebUI)

1. **Create a project**: "Project & Domain Management" → New (e.g. `demo`). Project data
   lands in `webui/projects/demo/`.
2. **Create / clone a domain**: you can create a blank `<domain>`, or "Clone from existing
   domain" (the repo's built-in example domains such as `ppt` can be cloned directly).
3. **Upload materials**: go to that domain's "Materials Management" and upload
   PDF/Word/MD/TXT/PPTX, etc. After upload they are written to
   `fixtures/<domain>/manifest.json`, default `enabled: true`.
   - Only materials with `enabled: true` participate in distillation; you can enable/disable
     them from the materials list.
4. **Configure LLM**: pick the active template in "LLM Configuration" (see 1.3).
5. **Run distillation**: in the "Distillation Workbench" click **"Distill"**. For the first
   run, tick **dry-run** to validate the pipeline, then untick it for a real run.
6. **Watch progress / re-run**: "Task Center" shows logs in real time. With the `task_id`
   recording the parameters, the **"Re-run"** button re-executes with the same parameters
   in one click — no need to refill the form.

### 3.2 Distill via API

```bash
# dry-run (no LLM call, validates the pipeline)
curl -X POST http://127.0.0.1:8000/api/projects/demo/domains/<domain>/distill \
  -H 'Content-Type: application/json' \
  -d '{"dry_run": true}'

# real distillation
curl -X POST http://127.0.0.1:8000/api/projects/demo/domains/<domain>/distill \
  -H 'Content-Type: application/json' \
  -d '{"dry_run": false}'
# -> {"ok": true, "task_id": "xxxxxxxx"}
```

> Git Bash note: a single-quoted JSON containing Chinese gets mangled by locale, causing
> `400 error parsing the body`. Use ASCII fields or `-d @file` (write the body to a file
> then `-d @body.json`) to avoid this.

Poll task status:

```bash
curl http://127.0.0.1:8000/api/tasks/<task_id>
```

### 3.3 What distillation produces

```
webui/projects/demo/
└── skills_library/<domain>/
    ├── index.json                 # master index: {updated_at, total, skills:[{skill_id,skill_name,category,source_document,source_title,detail_path}]}
    ├── <cat1>/...
    ├── <cat2>/...
    └── ...
```

- `index.json` is the entry point; each skill entry has `skill_id / skill_name / category /
  source_document / source_title / detail_path`.
- Each skill is a directory containing `skill.json` and the body (.md/.json/.txt).
- Idempotent: already-distilled source files are recorded in `source_document`; a re-run only
  adds new files and skips existing ones.

---

## 4. Using the distilled skills (tutorial)

Distilled skills are consumed by the Agent through an **MCP server**. Each domain's server
lives at `webui/projects/<project>/domains/<domain>/mcp_server/server.py` and uses `FastMCP`
over stdio transport. The server learns the current domain and isolation paths via the
environment variables `R2S_DOMAIN` / `R2S_SKILLS_DIR` / `R2S_WORKSPACE` (the domain name is
never hard-coded, so the same code serves any domain).

### 4.1 Option 1: WebUI Agent Console (most common, auto-spawns MCP)

1. Go to **"Agent Console"**, pick a domain (e.g. `ppt`), and enter the task text.
2. Optional: model, `reasoning`, `max_iter`, `n_skills`, `top_k`, `dry_run`.
3. Click **"Run"**. The backend auto-spawns the MCP server per the `mcp:` block in
   `domain.yaml` (cwd = project root); the Agent calls skills and stage tools through it;
   execution logs and artifacts are visible in real time.

Equivalent API call:

```bash
curl -X POST http://127.0.0.1:8000/api/projects/demo/agent/run \
  -H 'Content-Type: application/json' \
  -d '{"domain":"<domain>","task":"Complete XXX using this domain skills","max_iter":12,"n_skills":5,"top_k":20}'
```

### 4.2 MCP tools of the example domain (`ppt`)

The repo's built-in **example domain `ppt`** registers several `@mcp.tool`s in
`domains/ppt/mcp_server/server.py` (knowledge recall, deliverable generation, etc. — see the
source for the exact list). **For other domains, the toolset is decided by that domain's
`server.py`** — the UI and engine don't care which tools exist. All tools internally
identify the domain via `R2S_DOMAIN` and read/write this project's skill library / artifact
directory, so the same server code serves any domain.

> These example-domain tools are that domain's capabilities, not part of the UI. To build a
> new domain you only write that domain's `domain.yaml` + `mcp_server/server.py` (reference
> `domains/ppt/`) — no frontend/backend code changes needed.

### 4.3 Option 2: run the MCP server manually (for external Agents / debugging)

The server derives the project root from `__file__` (`parents[2]`) and identifies the domain
via the `R2S_DOMAIN` env var, so **you can run it directly** without manually switching cwd:

```bash
cd Resource2Skill/webui/projects/demo
R2S_DOMAIN=ppt python domains/ppt/mcp_server/server.py        # stdio transport, waits for an MCP client
```

Any MCP-compatible client (Claude Desktop / a self-built Agent / the `mcp` CLI inspector)
can be configured to use it as a stdio server. It reads **this project's**
`skills_library/<domain>` (not the repo root's), matching the distillation output one-to-one.

### 4.4 Artifact repository (view deliverables)

Agent-produced files land in
`webui/projects/<project>/output/<domain>_workspace/<product>/...`. The WebUI
**"Artifact Repository"** page can browse / download them directly; equivalent APIs:

```bash
curl "http://127.0.0.1:8000/api/projects/demo/repo?domain=<domain>"
curl "http://127.0.0.1:8000/api/projects/demo/repo/file?kind=output&domain=<domain>&rel_path=<product>/<stage>/<file>"
```

---

## 5. Add your own domain (generic usage)

1. `POST /api/projects/<project>/domains` `{"domain":"<your-domain>","seed_from":"ppt"}`
   clones the example domain as a starting point; or leave `seed_from` empty to create a
   blank domain (`mcp: null`, configure later).
2. Edit `webui/projects/<project>/domains/<your-domain>/domain.yaml`:
   - Change `persona` / `categories` / `query_pool` / `agent_initial_prompt` to your
     domain's language;
   - Point `mcp.command` / `mcp.args[0]` at your `mcp_server/server.py`; `mcp.env` will
     auto-inject isolation vars like `R2S_DOMAIN`.
3. Write `mcp_server/server.py`: register that domain's skill tools with `@mcp.tool()`
   (reference `domains/ppt/mcp_server/server.py`; use `R2S_DOMAIN` to distinguish domains
   and `_SKILLS_DIR` / `_WORKSPACE` to read/write — never hard-code the domain name).
4. Upload that domain's materials → distill → pick that domain in the Agent Console to run.

The engine has **zero special-casing** for any of this; `ppt` is just one example configured
this way.

---

## 6. Practical tips

- **Dry-run before the real run**: both distillation and the Agent have `dry_run` that skips
  the LLM and validates the pipeline first.
- **Re-run without refilling the form**: terminal tasks in "Task Center" carry a "Re-run"
  button that copies the original parameters for a one-click re-run (supported for both
  distillation and the Agent).
- **Proxy gotcha**: during distillation, if the template leaves the proxy unset, the code
  **explicitly clears** `HTTP_PROXY/HTTPS_PROXY` inherited from the shell and goes direct.
- **Data isolation**: projects are mutually isolated, decided by `projects_root` in
  `webui_config.json` (which `webui/projects` to read). LLM keys are Fernet-encrypted into
  `webui_config.json` (key in `webui/backend/.key`), and logs are desensitized.

---

## 7. Directory quick reference

```
webui/
├── backend/            # FastAPI: main.py(API) models.py(request bodies) tasks.py(task queue) distill.py(distill entry) agent.py(Agent scheduler) projects.py(project/domain + generic mcp rewrite)
├── frontend/           # Vue3 + Element Plus (domain-agnostic; UI hard-codes no domain)
└── projects/<project>/
    ├── domains/<domain>/domain.yaml     # domain definition + mcp block (Agent spawns MCP server from this)
    ├── domains/<domain>/mcp_server/server.py   # that domain's skill consumption surface (MCP tools, parameterized by R2S_DOMAIN)
    ├── fixtures/<domain>/manifest.json  # materials manifest (enabled switch)
    ├── skills_library/<domain>/         # distillation output (index.json + one dir per skill)
    └── output/<domain>_workspace/        # Agent deliverable landing zone (<domain> decided by R2S_DOMAIN)

domains/<domain>/mcp_server/server.py   # repo's built-in example domains (e.g. ppt); copy this structure for new domains
```

---

A Chinese version of this manual is available at [README-WebUI-zh.md](./README-WebUI-zh.md).
