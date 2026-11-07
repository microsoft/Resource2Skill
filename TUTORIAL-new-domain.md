# 教学实战：从零创建一个自定义领域（Resource2Skill WebUI）

> **本教程的目的**：演示本项目的核心设计 —— **领域驱动**：**不改任何前端 / 后端代码**，
> 就能新增一个自己的领域，并把素材蒸馏成 Agent 可调用的技能。整个系统的"性格"由两份配置决定
> （`domain.yaml` + 该域的 `mcp_server/server.py`），UI 和引擎对具体领域一无所知。跟着做一遍即可体会。

---

## 0. 你会学到什么

1. 领域驱动设计在这个项目里是怎么落地的（换域 = 换两份配置，UI/引擎零改动）。
2. 怎么用 API 或 WebUI 新建一个域（克隆自带示例域 `ppt` 作为起点）。
3. 怎么改 `domain.yaml`，把示例域"变成"你自己的领域。
4. 怎么加素材、蒸馏、再用 Agent 调用技能，跑通端到端闭环。
5. **引擎为什么能做到领域无关** —— 原理小讲（§7）。

---

## 1. 前置条件

- 后端 8000 + 前端 5172 已起（步骤见 `README-WebUI.md` §2）。
- 已配好一个 LLM 模板（蒸馏要真调 LLM；或先全程用 dry-run 验证管线）。
- 已有一个项目（教程用自带的 `demo` 项目；没有就先在「项目与Domain管理」新建一个）。

---

## 2. 第一步：新建领域（克隆示例域）

领域通过 `POST /api/projects/<项目>/domains` 创建。`seed_from` 指定从哪个已有域克隆，
克隆会把该域的 `domain.yaml` + `mcp_server` 复制过来作为起点。

### 方式 A：API

```bash
curl -X POST http://127.0.0.1:8000/api/projects/demo/domains \
  -H 'Content-Type: application/json' \
  -d '{"domain":"marketing","seed_from":"ppt"}'
```

> 这个调用在后端会触发 `_rewrite_mcp_for_project`：把克隆出来的 `domain.yaml` 的 `mcp` 块改写为
> **本项目隔离**形态 —— `mcp.cwd` = 项目根，`mcp.env` 注入 `R2S_DOMAIN=marketing`，并追加
> `--workspace <项目>/output/marketing_workspace` 与 `--skills-dir <项目>/skills_library/marketing`。
> 引擎完全由 `R2S_DOMAIN` 决定当前域，不写死任何特定领域名。

### 方式 B：WebUI

「项目与Domain管理」→ 选中 `demo` → 「新建域」→ 域名填 `marketing` → 来源选 `ppt`（克隆）。

**预期结果**：

- 左侧领域列表出现 `marketing`。
- 文件系统生成 `webui/projects/demo/domains/marketing/`，内含 `domain.yaml` 和 `mcp_server/server.py`。
- 头部「当前领域」可切到 `marketing`。

---

## 3. 第二步：把示例域改成你的领域

编辑 `webui/projects/demo/domains/marketing/domain.yaml`，把示例域的语言换成你的领域语言：

```yaml
name: marketing
display_name: 营销方案
persona: 你是一名资深的营销方案专家，擅长基于资料生成可落地的 launch 方案。
categories:
  market: [市场分析, 用户画像]
  competitor: [竞品, 差异化]
  strategy: [投放策略, 渠道]
  copy: [文案, 卖点]
agent_initial_prompt: 请基于已蒸馏的营销技能，为新产品撰写一份 launch 营销方案。
query_pool:
  - 为新产品写一份 launch 营销方案
  - 分析竞品的营销策略差异
mcp:
  command: python
  args:
    - domains/marketing/mcp_server/server.py
    - --workspace
    - output/marketing_workspace
    - --skills-dir
    - skills_library/marketing
  env:
    R2S_DOMAIN: marketing
```

> **原理**：上面这些字段 100% 驱动 UI 标签、蒸馏的分类维度、Agent 的提示词。
> **改这里就改了整个领域的"性格"，前端一行不用动。** 这就是领域驱动——引擎只负责"读配置、跑流程"。

---

## 4. 第三步：加素材

进 `marketing` 的「素材管理」，上传你的 PDF / Word / MD（如《2024 营销白皮书.docx》《竞品分析.pdf》）。
上传后写入 `fixtures/marketing/manifest.json`，默认 `enabled: true`。

> 只有 `enabled: true` 的素材参与蒸馏；可在素材列表里临时停用某份素材。

---

## 5. 第四步：蒸馏

「蒸馏工作台」选 `marketing` → **先勾 dry-run** 验证管线（不调 LLM，确认"抽取→切片→写技能库"通）
→ 取消勾，跑真实蒸馏。

产物落到 `webui/projects/demo/skills_library/marketing/index.json`，结构与其他域一致：

```json
{
  "updated_at": "...",
  "total": 42,
  "skills": [
    {"skill_id":"...","skill_name":"...","category":"market",
     "source_document":"2024 营销白皮书.docx","source_title":"...",
     "detail_path":"market/xxx/skill.json"}
  ]
}
```

**验证点**：

- 「任务中心」日志出现"蒸馏完成 / N 条技能"。
- `index.json` 的 `total` > 0。
- 「素材管理」里能看到素材已被标记为"已蒸馏"。

---

## 6. 第五步：用 Agent 调用技能

「Agent 执行台」选 `marketing`，填任务如"基于素材为新产品写一份 launch 营销方案"，点「运行」。

后端按 `domain.yaml` 的 `mcp:` 块自动拉起 `marketing` 的 MCP server（cwd = 项目根、
`R2S_DOMAIN=marketing`），Agent 通过它召回知识并产出交付物到
`webui/projects/demo/output/marketing_workspace/<产品>/`。

> **关于工具名**：克隆来的 `server.py` 工具函数名来自源域（本例为 `ppt`），例如知识召回类工具。
> 它们内部按 `R2S_DOMAIN` 读取的是 `skills_library/marketing`，与源域名无关，**功能不受影响**。
> 想要更"干净"的专属领域，直接编辑 `domains/marketing/mcp_server/server.py` 里的 `@mcp.tool`
> 函数即可——删掉不需要的、或把函数名改成你的领域语言。引擎只认 `R2S_DOMAIN` 隔离路径。
>
> 这就是领域驱动架构的设计意图：**最小改动，拥有自己的领域**。

---

## 7. 原理小讲：引擎为什么能做到领域无关

- **领域由配置定义**：每个域有一份 `domain.yaml`（persona / categories / mcp / agent 提示词）和一个
  `mcp_server/server.py`。UI 与引擎不写死任何领域逻辑，只负责"读配置、跑流程"。
- **领域隔离靠环境变量**：`agent.py` 在启动 Agent 时向 MCP 子进程注入 `R2S_DOMAIN` /
  `R2S_SKILLS_DIR` / `R2S_WORKSPACE`，把技能库与产物落在本项目、本领域的目录里。
- **播种时自动改写**：`projects.py` 的 `_rewrite_mcp_for_project` 对**所有带 `mcp` 块的域一视同仁**
  地改写 `domain.yaml`——注入 `R2S_DOMAIN` + 隔离路径，使同一份 server 代码可服务任意域。
- **server 按领域参数化**：`mcp_server/server.py` 用 `_DOMAIN = os.environ.get("R2S_DOMAIN") or "ppt"`
  推算技能库 / 产物路径（`skills_library/<域>`、`output/<域>_workspace`），不写死领域名。

**结论**：新增领域 = 写 `domain.yaml` + （可选）`mcp_server`，**UI / 后端零改动**。
仓库自带的 `ppt` 只是被这样配置出来的一个示例，不是特殊存在——任意领域都能复制这条路径。

---

## 8. 排错

| 现象 | 排查 |
|------|------|
| 新域 Agent 跑不起来 / MCP 启动即崩 | 检查 `domain.yaml` 的 `mcp.args[0]` 路径存在；`mcp.env.R2S_DOMAIN` 是否等于域名；`mcp>=1.26`（见 README §1.1） |
| 技能召回为空 | 确认蒸馏已完成且 `skills_library/<域>/index.json` 存在、`total>0`；素材 `enabled:true` |
| dry-run 通过但真跑 401 | LLM 模板 key 无效，先在「LLM 配置」点「测试」验证连通 |
| 换域后产物跑到了别的域目录 | 确认 `mcp.env.R2S_DOMAIN` 与该域一致（由 `_rewrite_mcp_for_project` 自动注入，一般无需手改） |

---

## 9. 小结

你刚刚完成了一条**完全领域无关**的端到端链路：建域 → 配 `domain.yaml` → 加素材 → 蒸馏 → Agent 调用技能。
全程没有碰前端 / 后端一行代码。这正是领域驱动设计的目标 —— **新增领域只需写配置，UI / 后端零改动**，
而 `ppt` 只是仓库自带的一个可被任意领域复制的示例。
