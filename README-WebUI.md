# Resource2Skill · WebUI 项目手册（领域无关 / 通用）

> 本仓库在 Microsoft `Resource2Skill` 内核之上套了一层本地可视壳（FastAPI + Vue3）。
> 本手册讲**通用 WebUI 这条线**——引擎与 UI 完全领域无关，领域行为 100% 来自
> `domain.yaml` + 该域的 `mcp_server/server.py`。仓库自带一个示例领域 `ipd`（可克隆、可删除、
> 可替换），你也可以新建任意领域。上游通用说明在 `README.md`。

本仓库在 Resource2Skill 内核之上套了一层本地可视壳：

- **后端**：FastAPI（`webui/backend/`），任务队列单 worker 串行，蒸馏 / Agent 共用。
- **前端**：Vue3 + Element Plus（`webui/frontend/`），纯本地 `localhost` 单人使用。
- **数据隔离**：引擎代码只有一份；"项目"是独立数据目录（`webui/projects/<项目>/`，含 `domains/ fixtures/ skills_library/ output/ + project.json`）。任务执行时把 `cwd` 切到项目根，R2S 相对路径自然生效，**不重构 core**。
- **领域驱动**：每个域自带一个 `domain.yaml`（persona / categories / mcp / agent 提示词）和一个 MCP server（`domains/<域>/mcp_server/server.py`），把蒸馏出的技能暴露成 Agent 可调用的工具。**换领域 = 换这两份配置，UI 零改动。**

---

## 1. 环境准备

### 1.1 Python（后端 + 蒸馏 + Agent）

```bash
# 用 3.11/3.12 即可（Blender 域才强制 3.11，一般领域不需要）
cd Resource2Skill
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # 含 mcp>=1.26、python-pptx、openpyxl 等
```

> ⚠️ `mcp` 必须 `>=1.26`。1.10.x 会让本仓库所有 MCP server 在 import 时崩溃
> （`issubclass() arg 1 must be a class`，因为 server 用了 `from __future__ import annotations`）。

### 1.2 Node（前端）

```bash
cd webui/frontend
npm install
```

### 1.3 LLM 接入（蒸馏与 Agent 都依赖它）

蒸馏会真实调用 LLM 来抽取 / 切片 / 生成技能；Agent 也会调用。先准备好一个兼容
OpenAI 协议的 endpoint（DeepSeek / Azure OpenAI / 本地 Ollama / 自建 OpenAI-compatible 均可）。

- 在 WebUI 的 **「LLM 配置」** 页新增模板：`provider`（azure/openai/deepseek/ollama/custom）、
  `endpoint`、`api_key`、`model`，点 **「测试」** 验证连通。
- 或用 API：`POST /api/llm`，body 见 `webui/backend/models.py` 的 `LLMTemplate`。

> 不想接 LLM？蒸馏可勾 **dry-run**：只验证「抽取 → 切片 → 写技能库」管线，不调用模型。

---

## 2. 启动

### 2.1 后端（FastAPI，端口 8000）

```bash
cd webui
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

> 后端用**相对导入**，必须从 `webui/` 目录启动（`backend.main:app`），不能裸 `uvicorn main:app`。
> 健康自检：`GET http://127.0.0.1:8000/api/health`。

### 2.2 前端（Vite dev，端口 5172）

```bash
cd webui/frontend
npm run dev
```

浏览器打开 `http://localhost:5172`（dev server 只绑 `localhost` / IPv6 `::1`，用 `localhost` 而非 `127.0.0.1`）。

> **Windows 路径坑（必读）**：本机 `C:\Users\...` 实为到 `D:\workbuddy\...` 的 junction。
> 若从 `C:` 路径跑 `vite build` 会报 `fileName absolute path` 错误。
> 解决：从**真实 D: 路径**启动（`webui/frontend/`），且确保没有残留的 `vite preview`（曾绑 5173 对 `/src/*` 回吐 index.html 导致 HMR 失效）；必要时先 `taskkill` 旧 5172/5173 进程再重启。

---

## 3. 蒸馏教程（把素材变成可执行技能）

蒸馏入口只有一个：**`POST /api/projects/{name}/domains/{domain}/distill`**，由 WebUI 的
**「蒸馏工作台」** 或 **「素材管理」** 触发。底层走 `core/collector.py` → 按 `domain.yaml`
的 `categories` 分类 → 写 `项目根/skills_library/<domain>/index.json` + 每技能一个目录。

> 蒸馏与领域无关：换 domain 只是换 `categories` 与提示词，**引擎代码不变**。

### 3.1 步骤一览（WebUI）

1. **新建项目**：「项目与Domain管理」→ 新建（如 `demo`）。项目数据落在 `webui/projects/demo/`。
2. **新建 / 克隆域**：可新建空白 `<domain>` 域，或「从已有域克隆」（仓库自带示例域如 `ipd` 可直接克隆）。
3. **上传素材**：进该域的「素材管理」，上传 PDF/Word/MD/TXT/PPTX 等。上传后写入
   `fixtures/<domain>/manifest.json`，默认 `enabled: true`。
   - 只有 `enabled: true` 的素材会参与蒸馏；可在素材列表里启用 / 停用。
4. **配置 LLM**：在「LLM 配置」选好活动模板（见 1.3）。
5. **跑蒸馏**：在「蒸馏工作台」点 **「蒸馏」**。首次建议先勾 **dry-run** 验证管线；再取消勾跑真实蒸馏。
6. **看进度 / 重跑**：「任务中心」实时看日志。`task_id` 记下了参数，**「重跑」** 按钮可一键用相同参数复跑，
   不用重新填表。

### 3.2 用 API 蒸馏

```bash
# dry-run（不调 LLM，验证管线）
curl -X POST http://127.0.0.1:8000/api/projects/demo/domains/<domain>/distill \
  -H 'Content-Type: application/json' \
  -d '{"dry_run": true}'

# 真实蒸馏
curl -X POST http://127.0.0.1:8000/api/projects/demo/domains/<domain>/distill \
  -H 'Content-Type: application/json' \
  -d '{"dry_run": false}'
# -> {"ok": true, "task_id": "xxxxxxxx"}
```

> Git Bash 注意：单引号 JSON 里含中文会被 locale 改写导致 `400 error parsing the body`。
> 用 ASCII 字段或 `-d @file`（把 body 写进文件再 `-d @body.json`）避免。

轮询任务状态：

```bash
curl http://127.0.0.1:8000/api/tasks/<task_id>
```

### 3.3 蒸馏产物长什么样

```
webui/projects/demo/
└── skills_library/<domain>/
    ├── index.json                 # 总索引：{updated_at, total, skills:[{skill_id,skill_name,category,source_document,source_title,detail_path}]}
    ├── <cat1>/...
    ├── <cat2>/...
    └── ...
```

- `index.json` 是入口，每条技能含 `skill_id / skill_name / category / source_document / source_title / detail_path`。
- 每个技能是一个目录，里面有 `skill.json` 及正文（.md/.json/.txt）。
- 幂等：已蒸馏的源文件记录在 `source_document`，重跑只补新文件、跳过已有的。

---

## 4. 使用蒸馏出来的技能（教程）

蒸馏出的技能通过 **MCP server** 被 Agent 消费。每个域的 server 在
`webui/projects/<项目>/domains/<域>/mcp_server/server.py`，用 `FastMCP` 以 stdio 传输。
server 通过环境变量 `R2S_DOMAIN` / `R2S_SKILLS_DIR` / `R2S_WORKSPACE` 感知当前领域与隔离路径
（不写死领域名，因此同一份代码可服务任意域）。

### 4.1 方式一：WebUI Agent 执行台（最常用，自动拉起 MCP）

1. 进 **「Agent 执行台」**，选域（如 `ipd`），填任务文本。
2. 可选：模型、`reasoning`、`max_iter`、`n_skills`、`top_k`、`dry_run`。
3. 点 **「运行」**。后端按 `domain.yaml` 的 `mcp:` 块自动拉起 MCP server（cwd=项目根），
   Agent 通过它调用技能与阶段工具；执行日志与产物实时可见。

API 等价调用：

```bash
curl -X POST http://127.0.0.1:8000/api/projects/demo/agent/run \
  -H 'Content-Type: application/json' \
  -d '{"domain":"<domain>","task":"用本域技能完成 XXX","max_iter":12,"n_skills":5,"top_k":20}'
```

### 4.2 示例域（ipd）的 MCP 工具清单

下面以仓库自带的 **示例域 `ipd`** 为例，它的 `mcp_server/server.py` 注册了 12 个 `@mcp.tool`。
**换成别的域，工具集由该域的 server.py 决定**——UI 与引擎不关心具体工具有哪些。

知识召回：

| 工具 | 作用 |
|------|------|
| `search_ipd_skills(query, category, k)` | 按关键词 / 分类召回知识技能 |
| `get_ipd_skill(skill_id)` | 读取某技能的完整正文（md/json/txt） |

阶段子 Agent（每个 = 一个 `@mcp.tool`，产出阶段交付物到 `output/<domain>_workspace/<产品>/<阶段>/`）：

| 工具 | 阶段 |
|------|------|
| `develop_charter(product, brief)` | 概念 |
| `develop_plan(product, notes)` | 计划 |
| `develop_spec(product, notes)` | 开发 |
| `verify_product(product, notes)` | 验证 |
| `launch_product(product, notes)` | 发布 |
| `manage_lifecycle(product, notes)` | 生命周期 |

门禁（质量闸）：

| 工具 | 作用 |
|------|------|
| `run_dcp_gate(product, stage)` | 决策评审门禁：检查交付物 + 4W+2H 是否齐备，返回 `GATE: PASS/FAIL` |
| `run_tr_gate(product, tr)` | 技术评审门禁（TR1-TR6）：提示按 TR 清单核对 |

交付物落盘 / 生成：

| 工具 | 作用 |
|------|------|
| `save_deliverable(product, stage, filename, content)` | 通用落盘任意交付物到 `output/<domain>_workspace/<产品>/<阶段>/` |
| `generate_charter_pptx(product, ...)` | 基于《Charter模板.pptx》+ 已写好的 Charter，生成《Charter汇报.pptx》（示例域专用） |

> 这些示例域工具是该域的能力，不是 UI 的一部分。要做一个新域，只需写该域的
> `domain.yaml` + `mcp_server/server.py`（参考 `domains/ipd/`），无需改任何前端/后端代码。

### 4.3 方式二：手动跑 MCP server（给外部 Agent / 调试）

server 用 `__file__` 反推项目根（`parents[2]`），并通过 `R2S_DOMAIN` 环境变量识别领域，
所以**直接运行即可**，无需手动切 cwd：

```bash
cd Resource2Skill/webui/projects/demo
R2S_DOMAIN=ipd python domains/ipd/mcp_server/server.py        # stdio 传输，等待 MCP 客户端连
```

任何兼容 MCP 的客户端（Claude Desktop / 自建 Agent / `mcp` CLI inspector）把它配成 stdio server 即可。
它读的是**本项目**的 `skills_library/<domain>`（不是仓库根的），与蒸馏产物一一对应。

### 4.4 产物仓库（看交付物）

Agent 产出的文件落在 `webui/projects/<项目>/output/<domain>_workspace/<产品>/...`。
WebUI **「产物仓库」** 页可直接浏览 / 下载；等价 API：

```bash
curl "http://127.0.0.1:8000/api/projects/demo/repo?domain=<domain>"
curl "http://127.0.0.1:8000/api/projects/demo/repo/file?kind=output&domain=<domain>&rel_path=<产品>/<阶段>/<file>"
```

---

## 5. 新增一个自己的领域（泛化用法）

1. `POST /api/projects/<项目>/domains` `{"domain":"<你的域>","seed_from":"ipd"}` 克隆示例域作为起点；
   或留空 `seed_from` 新建空白域（`mcp: null`，后续自己配）。
2. 编辑 `webui/projects/<项目>/domains/<你的域>/domain.yaml`：
   - `persona` / `categories` / `query_pool` / `agent_initial_prompt` 改成你的领域语言；
   - `mcp.command` / `mcp.args[0]` 指向你的 `mcp_server/server.py`，`mcp.env` 会自动注入 `R2S_DOMAIN` 等隔离变量。
3. 写 `mcp_server/server.py`：用 `@mcp.tool()` 注册该域的技能工具（参考 `domains/ipd/mcp_server/server.py`，
   用 `R2S_DOMAIN` 区分领域、用 `_SKILLS_DIR` / `_WORKSPACE` 读写，不要写死领域名）。
4. 上传该域素材 → 蒸馏 → Agent 执行台选该域运行。

引擎对这一切**零特殊分支**，IPD 只是被这样配置出来的一个例子。

---

## 6. 实用 tips

- **先 dry-run 再真跑**：蒸馏 / Agent 都有 `dry_run`，不调 LLM，先验证管线不踩坑。
- **重跑不复填表**：「任务中心」里终态任务带「重跑」按钮，复制原参数一键复跑（蒸馏 / Agent 均支持）。
- **代理坑**：蒸馏时若模板未填代理，代码会**显式清除**从 shell 继承的 `HTTP_PROXY/HTTPS_PROXY` 走直连。
- **数据隔离**：多项目互不相通，靠 `webui_config.json` 的 `projects_root` 决定读哪个 `webui/projects`。
  LLM Key 用 Fernet 加密落 `webui_config.json`（key 在 `webui/backend/.key`），日志脱敏。

---

## 7. 目录速查

```
webui/
├── backend/            # FastAPI：main.py(API) models.py(请求体) tasks.py(任务队列) distill.py(蒸馏入口) agent.py(Agent 调度) projects.py(项目/域+通用 mcp 重写)
├── frontend/           # Vue3 + Element Plus（领域无关，UI 不写死任何域）
└── projects/<项目>/
    ├── domains/<域>/domain.yaml     # 域定义 + mcp 块（Agent 据此拉起 MCP server）
    ├── domains/<域>/mcp_server/server.py   # 该域技能的消费面（MCP 工具，按 R2S_DOMAIN 参数化）
    ├── fixtures/<域>/manifest.json  # 素材清单（enabled 开关）
    ├── skills_library/<域>/         # 蒸馏产物（index.json + 每技能一目录）
    └── output/<域>_workspace/        # Agent 交付物落点（<域> 由 R2S_DOMAIN 决定）

domains/<域>/mcp_server/server.py   # 仓库自带示例域（如 ipd）；新建域时复制此结构
```
