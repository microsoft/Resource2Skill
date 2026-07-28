# Resource2Skill WebUI — 切片1：项目与 Domain 管理

## 本切片交付

**后端** (`webui/backend/`)
- 新增 `projects.py`：项目与领域的 CRUD + 校验，多项目隔离（零 core 重构）。
- `main.py` 新增端点：
  - `GET/POST/DELETE /api/projects`、`POST /api/projects/{name}/active`
  - `GET /api/repo-domains`（仓库已有领域，供“播种”下拉）
  - `GET/POST /api/projects/{name}/domains`、`POST /api/projects/{name}/domains/{domain}/active`、`POST .../validate`
- `models.py` 增加 `ProjectCreate` / `DomainCreate`。

**前端** (`webui/frontend/`)
- `api.js` 增加项目/领域 API 封装。
- `App.vue` 顶部 `el-menu` 在「LLM 配置 / 项目与 Domain 管理」间切换。
- 新增 `views/ProjectsDomains.vue`：项目表（激活/删除）、领域表（内联校验/激活）、新建项目与新建领域对话框（领域支持“从仓库播种”）。

## 关键设计
- **隔离模型**：项目 = `webui/projects/<name>/` 下独立 `domains/ skills_library/ fixtures/ output/ project.json`；校验经 `core.validate_domain(name, domains_dir=项目domains)` 覆盖参数实现，不改 core。
- **领域创建两模式**：
  - 播种：复制仓库 `domains/<name>`（如 ipd）→ 真实可用、`validate` 直接 PASS；自动改写 `mcp.cwd` 为项目根。
  - 空白脚手架：legacy 形态（不声明 `execution_mode`，`mcp: null`）→ `validate` 直接 PASS，后续再升级为新形态以支持 Agent 循环。
- **软删除**：沙箱拦截 `shutil.rmtree`，删除改为移动到 `projects/.trash/`（可恢复、不计入列表）。

## 验收结果（curl 实测）
```
建项目 demo
  → 新建领域 ipd（seed_from=ipd）   {"seeded": true}
  → POST .../ipd/validate           {"valid": true, "errors": []}   ✅ PASS
  → 新建领域 mytopic（空白脚手架）   {"seeded": false}
  → POST .../mytopic/validate       {"valid": true, "errors": []}   ✅ PASS（legacy）
  → 删除 demo / demo2              {"ok": true}（软删除）
```
前端 `vite build` 编译 1634 模块全过（仅生产构建的 dist 清理被沙箱拦截，dev 不受影响）。

## 当前运行
- 后端：uvicorn `webui.backend.main:app` @ `http://127.0.0.1:8000`
- 前端：vite dev @ `http://localhost:5173`（顶部切换“项目与 Domain 管理”）

## 下一步（切片2→4）
- 切片2 素材管理（上传/清单/预览/删除）
- 切片3 通用收集器 `core/collector.py` + 蒸馏工作台（后台线程 + SSE）
- 切片4 Agent 执行 + 产物仓库
