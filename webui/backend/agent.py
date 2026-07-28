"""Agent 执行台（切片4）。

设计要点：
- 复用 tasks.py 单 worker 串行队列 + distill._llm_env 的 LLM 注入模式。
- run_agent 内部直接调用 core.llm.call_azure_openai（不接收外部 llm_fn），
  且会 spawn MCP 子进程（子进程从 os.environ 读取 LLM 凭证）。因此必须：
  1) 在「整段 agent 运行期间」保持 LLM 环境变量（用 with _llm_env 包裹 run_agent），
     这样 agent 循环与 MCP 子进程都能正确拿到 endpoint/key；
  2) 把 cwd 切到项目根（与 create_domain 已重写的 mcp.cwd 协同）。
- 对所有领域注入 R2S_DOMAIN / R2S_SKILLS_DIR / R2S_WORKSPACE 环境变量（领域无关），
  实现产物隔离；MCP server 据此把技能库与产物落到本项目数据目录（output/<domain>_workspace）。
- 把 run_agent 的 library_dir 指向项目 skills_library/<domain>，使 agent 自身技能召回隔离。
- 通过 logging.Handler 把 agent_executor 的日志实时灌入 task.log（前端轮询即可看到流式进度）。
"""
from __future__ import annotations

import logging
import os
import json
from pathlib import Path

from core import load_domain
from core.agent_executor import run_agent

from . import config_store, projects
from .distill import _llm_env


class _TaskLogHandler(logging.Handler):
    """把 agent_executor logger 的输出实时写入 task.log。"""

    def __init__(self, task):
        super().__init__()
        self._task = task

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self._task.append_log(self.format(record))
        except Exception:  # noqa: BLE001
            pass


def _safe_domain_config(project: str, domain: str) -> dict:
    """加载项目 domains/<domain>/domain.yaml（优先），失败回退仓库域。"""
    proj_domains = projects.project_dir(project) / "domains"
    try:
        return load_domain(domain, domains_dir=proj_domains)
    except Exception:
        # 项目未播种该领域时回退仓库自带领域配置
        return load_domain(domain)


def run_agent_task(
    task,
    project: str,
    domain: str,
    *,
    task_text: str,
    model: str,
    reasoning: str,
    max_iter: int,
    n_skills: int,
    top_k: int,
    dry_run: bool,
) -> None:
    cfg = config_store.load()
    template = cfg.templates.get(cfg.active_llm)
    pdir = projects.project_dir(project)
    skills_dir = pdir / "skills_library" / domain

    if not dry_run:
        if not template or not template.api_key or not template.endpoint or not template.model:
            task.append_log("[错误] 未配置有效 LLM（endpoint/api_key/model 缺失）。请先在「LLM 配置」页配置并测试。")
            raise RuntimeError("LLM 未配置")

    task.append_log(f"[Agent] 项目={project} 领域={domain} dry_run={dry_run}")
    task.append_log(f"[Agent] 技能库={skills_dir}")

    try:
        domain_config = _safe_domain_config(project, domain)
    except Exception as e:
        task.append_log(f"[错误] 加载领域配置失败：{type(e).__name__}: {e}")
        raise

    skills_dir.mkdir(parents=True, exist_ok=True)

    # 选用模型/推理档位：请求指定优先，否则用 LLM 模板值
    resolved_model = model or (template.model if template else "gpt-5.4")
    resolved_reasoning = reasoning or (template.reasoning if template else "low")

    # 捕获 agent_executor 日志 -> task.log
    agent_logger = logging.getLogger("agent_executor")
    handler = _TaskLogHandler(task)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    agent_logger.addHandler(handler)
    agent_logger.setLevel(logging.INFO)

    saved_cwd = os.getcwd()
    r2s_env = ("R2S_DOMAIN", "R2S_SKILLS_DIR", "R2S_WORKSPACE")
    saved_env = {k: os.environ.get(k) for k in r2s_env}
    try:
        os.chdir(str(pdir))
        # 领域无关：所有域都注入 R2S_DOMAIN / 技能库 / 产物工作区，
        # MCP server 据此把技能库与产物落到本项目数据目录（output/<domain>_workspace）。
        os.environ["R2S_DOMAIN"] = domain
        os.environ["R2S_SKILLS_DIR"] = str(skills_dir)
        os.environ["R2S_WORKSPACE"] = str(pdir / "output" / f"{domain}_workspace")

        # 预检连通（非 dry_run）：避免无效 key 触发 agent 内长时间重试空耗
        if not dry_run and template:
            with _llm_env(template):
                from core.llm import call_azure_openai

                call_azure_openai(
                    [{"role": "user", "content": "ping"}],
                    model=template.model,
                    max_completion_tokens=5,
                    reasoning_effort="none",
                    timeout=30,
                )

        # 整段 agent 运行期间保持 LLM 环境（agent 循环 + MCP 子进程均依赖 os.environ）
        with _llm_env(template):
            result = run_agent(
                task_text,
                domain_config,
                skills_dir,
                model=resolved_model,
                reasoning_effort=resolved_reasoning,
                max_iterations=max_iter,
                n_skills=n_skills,
                top_k=top_k,
                dry_run=dry_run,
            )

        task.append_log("=== Agent 完成 ===")
        task.append_log(result.summary())
        if result.final_message:
            fm = result.final_message if isinstance(result.final_message, str) else str(result.final_message)
            task.append_log(f"Final: {fm[:800]}{'...' if len(fm) > 800 else ''}")

        def _clip(v, n=400):
            if v is None:
                return ""
            if isinstance(v, str):
                return v[:n]
            try:
                return json.dumps(v, ensure_ascii=False)[:n]
            except Exception:  # noqa: BLE001
                return str(v)[:n]

        tool_calls = [
            {
                "tool": tc.tool_name,
                "success": bool(tc.success),
                "args": _clip(tc.arguments),
                "error": _clip(tc.error),
            }
            for tc in result.tool_calls
        ]
        task.extra = {
            "success": result.success,
            "iterations": result.iterations,
            "tool_calls": tool_calls,
            "final_message": result.final_message,
            "domain": domain,
            "project": project,
        }
        task.append_log(f"[工具调用] 共 {len(tool_calls)} 次")
    finally:
        os.chdir(saved_cwd)
        agent_logger.removeHandler(handler)
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
