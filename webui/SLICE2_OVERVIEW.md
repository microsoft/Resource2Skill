# 切片2：素材管理 — 交付概览

日期：2026-07-28

## 本片交付

### 后端
- 新增 `webui/backend/fixtures.py`：素材管理核心模块（零 core 重构）。
  - `list_fixtures`：扫描 `fixtures/<domain>/`，与 `manifest.json` 对账（自动剔除已删条目），返回 `{name, ext, size, enabled, uploaded_at}`。
  - `save_fixture`：落盘到 `fixtures/<domain>/`，写 manifest（默认 enabled=true），校验扩展名。
  - `set_enabled`：更新 manifest 启用/停用标记。
  - `delete_fixture`：软删除（移动到 `fixtures/<domain>/.trash/`，可恢复，且不计入列表）。
  - `preview_text`：复用 `distill_ipd.extract_text` 抽取 PDF/PPTX/DOCX/XLSX 纯文本；MD/TXT 直接读；为空时返回友好提示。
  - `_safe_name`：文件名归一 + 路径穿越校验（`/` `..` 一律拒绝）。
- `main.py` 新增 5 个端点（`GET/POST fixtures`、`POST .../enable`、`DELETE ...`、`GET .../preview`）。

### 前端
- `views/Fixtures.vue`：项目+领域下拉、el-upload 上传、表格（文件名/类型/大小/启用开关/上传时间/预览·删除）、预览对话框（可滚动文本，超长截断提示）。
- `api.js` 封装 5 个素材 API + `fixtureUploadUrl`。
- `App.vue` 顶部导航新增「素材管理」。

## 验收实测（curl）
| 项目 | 结果 |
|---|---|
| 上传 sample.md / sample.txt | ok，enabled=true ✅ |
| 列表显示两个素材 | ✅ |
| 预览 MD/TXT | available:true + 文本 ✅ |
| 停用 sample.txt | enabled:false 反映到列表 ✅ |
| 上传 .zip | 400「不支持的类型」✅ |
| 删除 sample.txt | 软删除，列表剩 sample.md，.trash 留存 ✅ |
| 恶意文件名 `../../pwn.txt` 上传 | 400「非法文件名」，无文件逃逸 ✅ |
| 前端 vite build | 1635 模块全部 transformed，dist 生成 ✅ |

## 关键决策 / 契约
- **R2S core 本身不消费 `fixtures/`**：`distill_ipd.py` 无 manifest 概念。启用/停用 manifest 是 WebUI 侧新引入的契约，**切片3 通用 collect 将读取它来筛选素材**（只蒸馏 enabled 的）。
- 删除统一走软删除（沙箱禁硬删，且可恢复）。
- 预览复用 distill 抽取逻辑，不触发 LLM 蒸馏。

## 下一步
切片3：通用采集器 `core/collector.py`（领域无关，读取本片 manifest 筛选素材）+ 蒸馏工作台（后台线程 + SSE 日志）+ 任务中心。
