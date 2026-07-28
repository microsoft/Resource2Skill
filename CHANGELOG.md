# CHANGELOG / 分支说明

> 本文档是**技术追溯记录**，独立于面向使用者的 `README-WebUI.md` 与 `TUTORIAL-new-domain.md`。
> 它记录当前工作副本相对 `origin/main` 的差异，便于代码评审与合入时对齐。
>
> 状态快照时间：2026-07-28

---

## 1. 当前与 `origin/main` 的分歧状态

| 项 | 值 |
|----|----|
| 当前分支 | 本地 `main` |
| HEAD | `23563e69` |
| 相对 `origin/main` | **领先 2 个 commit** |
| 去特殊化（de-specialization）改动 | **尚未提交**，仅在工作区 |
| 无独立 feature 分支 | 差异 = 本地 `main` 的 2 个 commit + 未提交工作区改动 |

> ⚠️ **重要**：截止本记录，引擎去特殊化（领域无关化）仍是**未提交**的工作区改动。
> 它只存在于本机工作副本，没有进入任何分支历史。建议后续提交为独立 feature 分支再合入 `main`
> （见 §6 建议）。

---

## 2. 已提交（领先 `origin/main` 的 2 个 commit）

### `4b94922c` — webui: add Overview homepage + /api/config; commit C1/C2/I1 WebUI
- 新增首页 `Overview.vue`（总览仪表盘），成为默认落地页。
- 新增 `GET /api/config` 端点，统一对外暴露配置（LLM 模板、域/项目概览等）。
- 前端 C1 重构：引入模块级 `reactive` 单例 composable（`useActiveContext`），统一项目/域选择，
  替代各视图各自拉取激活态的重复代码。
- C2：领域粘性（后端 `get_domains` 返回 `active_domain`，前端跨刷新保持选中域）。
- I1：修复「点了激活没反应」——行点击即 `loadDomains`，不必再点激活按钮。
- 移植自 B 副本的部分能力（Overview 首页 + `/api/config`）。

### `23563e69` — feat(webui): add task rerun (copy-params) ported from B
- 任务模型 `Task` 新增 `params: dict` 字段，使任务可被完整复跑。
- `POST /api/tasks/{id}/rerun`：读取 `t.params` 重建请求体重跑；无 params 返回 400，任务缺失返回 404。
- 提取 `_submit_distill` / `_submit_agent` 辅助函数，消除重复提交逻辑。
- 前端 `TaskProgress.vue` 新增「重跑」按钮（仅终态且有 params 时显示），并向上 emit 新任务 id。
- 已在 **8000 真实后端**端到端验证：distill 路径与 agent 路径均复跑成功，404/400 边界正确。
- 移植自 B 副本的 rerun 端点（B 的独有亮点之一，已在对比评审中采纳）。

---

## 3. 未提交（工作区）—— 引擎去特殊化（domain-agnostic）

目标：移除后端引擎与示例中写死的 `if domain == "ipd"` / `IPD_*` 特殊处理，使任意领域
都能像 IPD 一样工作；IPD 退居为仓库自带的一个示例域。

### 3.1 已跟踪文件修改（5 个，构成相对 `origin/main` 的 diff）
`git diff --stat` 结果：
```
webui/backend/agent.py                       | 16 ++++---
webui/backend/projects.py                    | 70 ++++++++---------------
webui/backend/repo.py                        |  2 +-
webui/frontend/src/views/AgentConsole.vue    |  2 +-
webui/frontend/src/views/ProjectsDomains.vue |  2 +-
5 files changed, 44 insertions(+), 48 deletions(-)
```

| 文件 | 改动要点 |
|------|----------|
| `webui/backend/agent.py` | 删除 `if domain == "ipd":` 分支；改为**所有域**注入 `R2S_DOMAIN` / `R2S_SKILLS_DIR` / `R2S_WORKSPACE`（取代旧的 `IPD_*` 环境变量）。 |
| `webui/backend/projects.py` | `_rewrite_mcp_for_project` 去掉 `if domain == "ipd"` 特殊判定与「强指仓库根 server.py」逻辑；改为**所有带 `mcp` 块的域**通用：注入 `R2S_DOMAIN` 等隔离变量 + `--workspace`/`--skills-dir` 参数。 |
| `webui/backend/repo.py` | 修正一条注释（去掉 `ipd_workspace` 专属措辞，改为通用描述）。 |
| `webui/frontend/src/views/AgentConsole.vue` | placeholder 去掉「生成 IPD Charter」示例，改为通用自然语言任务描述提示。 |
| `webui/frontend/src/views/ProjectsDomains.vue` | 新建域 placeholder 由「如 ipd / ppt / 自定义」改为「如 marketing / finance / 自定义」。 |

### 3.2 示例域 `server.py` 参数化（未跟踪 / 忽略区，见 §5 说明）
- `domains/ipd/mcp_server/server.py`（仓库根示例种子）：`mcp` 改名 `r2s-mcp`；
  `_DOMAIN = os.environ.get("R2S_DOMAIN") or "ipd"`，技能库/产物路径改为
  `skills_library/<domain>` + `output/<domain>_workspace`，保留 `parents[2]` 回退（默认 ipd 向后兼容）。
- `webui/projects/demo/domains/ipd/mcp_server/server.py`（demo 种子副本）：同上参数化。

> 这两个 `server.py` **不在已提交 diff 中**：仓库根的 `domains/ipd/` 整个是未跟踪目录（见 §5），
> demo 副本位于 gitignored 的 `webui/projects/` 下。它们的改动是真实生效的磁盘文件，
> 但 git 不视为对 `origin/main` 的修改。

### 3.3 验证证据（非「看着像对」）
- `py_compile` 五个改动的 .py 全部通过。
- 新代码起 8077 端口，seed 一个**非 ipd 域 `pptx`**（from ipd）→ 重写出的 `domain.yaml`
  为 `R2S_DOMAIN: pptx` + `output/pptx_workspace` + `R2S_SKILLS_DIR`，**全程无 `IPD_*`**；
  `demo/domains` 仍返回 `active_domain: ipd`（无回归）；测试项目已清理。
- demo `server.py` 导入核验：默认 `DOMAIN=ipd`、路径 `skills_library\ipd` + `output\ipd_workspace`
  （与去特殊化前**完全一致**），`R2S_DOMAIN=pptx` 覆盖正确，12 个工具齐全。

---

## 4. 新增文档（均未提交）
| 文件 | 说明 |
|------|------|
| `README-WebUI.md` | 通用 WebUI 手册（领域驱动，IPD 仅作示例域中性出现）：启动、蒸馏教程、技能使用教程、新增领域、目录速查。 |
| `TUTORIAL-new-domain.md` | 教学实战：从零创建自定义领域（以 `marketing` 为例）的端到端 walkthrough + 领域驱动架构原理。 |

> 上游 `README.md` 保留微软通用英文说明，未被覆盖。

---

## 5. 未跟踪 / 忽略区里需注意的内容
当前工作区有大量**未跟踪**文件，其中大部分是运行产物与临时脚本，不应合入：

- `domains/ipd/`（整个目录未跟踪）—— 本地 IPD 示例种子域，含参数化后的 `server.py`。
  注意：已提交树里 `domains/` 只有 `blender / excel / ppt / reaper / web` 等，**没有 ipd**。
- `webui/projects/`（0 个跟踪文件，gitignored）—— 含 `demo` 项目及其 IPD 种子副本。
- 一堆运行日志与临时脚本：`agent_run*.log`、`distill_ipd*.log`、`webui/**/run*.log`、
  `_scratch/`、`build_cdt_charter.py`、`distill_ipd.py` 等 —— 建议加入 `.gitignore` 或清理，勿提交。

---

## 6. 已知限制 / 后续建议
1. **去特殊化尚未提交**：当前只是工作区改动。建议新建分支（如 `feat/generic-engine`）提交后合 `main`，
   以便评审与回滚。
2. **示例域 `server.py` 工具函数名仍带 `ipd` 字样**：`develop_charter` / `run_dcp_gate` /
   `generate_charter_pptx` 等是 IPD 专属能力函数名。新建其他域时应按需改名或另写工具，
   但**引擎层已不再依赖这个名字**——它们只是示例域的实现细节。
3. **运行中的 8000 后端仍是旧代码**：要加载去特殊化后的新代码，需在自备终端重启后端
   （`run_in_background` 起的后端会被回收，见项目长期约定）。
4. **分析类文档（未提交）**：`b_scripts_review.md`（B 副本脚本缺陷评审）、
   `r2s_dual_checkout_merge_proposal.md`（双副本对比与合并建议）—— 技术决策留痕，非代码。

---

## 7. 评审结论留痕（对比 B 副本）
- 采纳了 B 的 2 项真实亮点：**rerun 端点**（已提交 `23563e69`）、**Overview + /api/config**（已提交 `4b94922c`）。
- 未采纳：B 的 3 个独有脚本（经评审为脱节孤儿/有缺陷）、「删 A 用 B」（B 是空骨架）。
- 去特殊化证明：本项目的运行引擎（`core/agent_executor.py` / `core/llm.py`）与 B 副本**逐字节一致**，
  故 B 的「更泛化」实质是「空骨架无域」——本项目在保留可用示例的前提下去特殊化，更实用。
