# 切片3：通用采集器 + 蒸馏工作台 + 任务中心 — 交付概览

日期：2026-07-28

## 本片交付

### 通用采集器（core/collector.py，领域无关）
- 读 `fixtures/<domain>/manifest.json` 筛 **enabled** 素材 → 复用 `distill_ipd` 的抽取/切片/技能名解析 → 用 domain 的 `distiller_prompt.md`（无则通用提示词）蒸馏 → 写**项目** `skills_library/<domain>/` 的 R2S 兼容 `skill.json` + `index.json`。
- MD/TXT 由本地 `_extract_text` 直读（`distill_ipd` 全局 `SKIP_EXT` 故意跳过 `.md`，未改 core）。
- LLM 传输由调用方注入的 `llm_fn(messages, *, model, max_tokens, reasoning) -> str` 提供，core 不依赖 webui、不碰全局 env。

### 后端：蒸馏任务 + 任务中心
- `webui/backend/tasks.py`：单 worker **串行**任务注册表（蒸馏 / 后续 Agent 共用），内存态（重启即丢）；Task 带 log 缓冲（封顶 3000 行）+ `stop_requested` 终止标志。
- `webui/backend/distill.py`：把用户 active LLM 模板经**环境变量上下文管理器**注入 `core.llm.call_azure_openai`；**蒸馏前 ping 预检**（reasoning=none, 5 token），坏 key 立即 error 拒绝，避免 5×10s 重试空耗；`dry_run` 换桩跳过 LLM。
- 端点：`POST /api/projects/{p}/domains/{d}/distill`、`GET /api/tasks`、`GET /api/tasks/{id}`、`POST /api/tasks/{id}/stop`。

### 前端
- `views/DistillWorkbench.vue`：项目/域选择 + 开始蒸馏 + `dry_run` 勾选 + 实时日志轮询 + 终止。
- `views/TaskCenter.vue`：任务列表（类型/项目域/状态/时间）+ 日志查看 + 终止。
- `api.js` 封装 4 个 API；`App.vue` 导航新增「蒸馏工作台」「任务中心」。

## 验收实测
| 项目 | 结果 |
|---|---|
| dry_run 蒸馏（不调 LLM） | 写 `skills_library/ipd` skill.json + index.json total=1 ✅ |
| **真实蒸馏**（DS 模板 key 有效） | sample.md → 真实技能「基于 4W+2H 的 IPD Charter 快速生成模板」，任务 done ✅ |
| 预检失败快速 error（坏 key） | 不进入蒸馏循环、不空耗 ✅ |
| env 注入/还原（无 API 调用） | IN 正确、AFTER 完整还原 ✅ |
| 任务中心列表/日志/终止 | ✅ |
| 前端 vite build | 1637 模块全过 ✅ |

## 关键决策 / 契约
- **LLM 接入**：`call_azure_openai` 仅从环境变量读配置（不收参数）。故用 **env 注入 + 单 worker 串行** 把用户模板喂给 core，避免并发改 env 互相踩；provider 映射：deepseek / azure / openai_compatible(ollama 等)。
- **零 core 重构**：采集器写**项目**技能库，不碰全局 `skills_library/`；distill_ipd 全局行为未改。
- **预检闸**：真实蒸馏前先 ping，连通才继续，保护无效 key 不空耗、不花冤枉 token。

## 下一步
切片4：Agent 执行台（`core.agent_executor` 以项目根 cwd 运行，流式 token+工具调用+gate）+ 产物仓库（浏览 skills/output、预览 md/html/img、下载）。
