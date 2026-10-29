"""蒸馏任务（切片3）。

把 WebUI 配置的 active LLM 模板，通过环境变量注入喂给 core.llm.call_azure_openai，
再调用 core.collector.run_collect 完成通用采集蒸馏。dry_run 模式跳过 LLM，仅验证管线。
"""
from __future__ import annotations

import contextlib
import os
from pathlib import Path

from core import collector
from core.llm import call_azure_openai

from . import config_store, projects

# 需要临时写入并事后还原的环境变量（call_azure_openai 仅从这些读配置）
_ENV_KEYS = [
    "LLM_PROVIDER", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY",
    "OAI_COMPAT_CHAT_PATH", "HTTPS_PROXY", "HTTP_PROXY",
]


@contextlib.contextmanager
def _llm_env(template):
    saved = {k: os.environ.get(k) for k in _ENV_KEYS}
    try:
        provider = (template.provider or "azure").lower()
        os.environ["AZURE_OPENAI_API_KEY"] = template.api_key or ""
        os.environ["AZURE_OPENAI_ENDPOINT"] = template.endpoint or ""
        if provider == "azure":
            os.environ["LLM_PROVIDER"] = "azure"
        elif provider == "deepseek":
            os.environ["LLM_PROVIDER"] = "deepseek"
        else:
            # openai / ollama / custom 等：按 OpenAI 兼容处理，
            # 用户 endpoint 需自带 /v1（如 https://api.openai.com/v1 或 http://host:11434/v1）
            os.environ["LLM_PROVIDER"] = "openai_compatible"
            os.environ["OAI_COMPAT_CHAT_PATH"] = "chat/completions"
        if template.proxy:
            os.environ["HTTPS_PROXY"] = template.proxy
            os.environ["HTTP_PROXY"] = template.proxy
        else:
            # 模板未指定代理 → 走直连。显式清除可能从启动 shell 继承的系统代理
            # （如 HTTP_PROXY=127.0.0.1:10810），否则请求会被强制路由到本地代理，
            # 代理挂掉时整条 LLM 链路直接 ProxyError 失败。已验证 deepseek 直连可达。
            for _pk in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
                os.environ.pop(_pk, None)
            os.environ["NO_PROXY"] = "*"
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def run_distill_task(task, project: str, domain: str, dry_run: bool) -> None:
    cfg = config_store.load()
    template = cfg.templates.get(cfg.active_llm)
    fixtures_dir = projects.project_dir(project) / "fixtures" / domain
    skills_dir = projects.project_dir(project) / "skills_library" / domain
    domain_dir = projects.project_dir(project) / "domains" / domain

    if not fixtures_dir.exists():
        raise FileNotFoundError(f"素材目录不存在：{domain}（请先上传素材）")

    if dry_run:
        task.append_log("[dry-run] 不调用 LLM，仅验证 抽取→切片→写技能库 管线")
        llm_fn = lambda *a, **k: {"content": "x"}
        model = "dry-run"
        max_tokens = 6000
        reasoning = "low"
    else:
        if not template or not template.api_key or not template.endpoint or not template.model:
            task.append_log("[错误] 未配置有效 LLM（endpoint/api_key/model 缺失）。可勾选 dry-run 仅验证管线。")
            raise RuntimeError("LLM 未配置")
        task.append_log(f"[LLM] 模板={cfg.active_llm} 模型={template.model} provider={template.provider}")

        # 预检：先用一次极简 ping 验证 endpoint/key 连通，避免无效 key 触发长时间重试空耗。
        def _ping():
            with _llm_env(template):
                return call_azure_openai(
                    [{"role": "user", "content": "ping"}],
                    model=template.model,
                    max_completion_tokens=5,
                    reasoning_effort="none",
                    timeout=30,
                )
        try:
            _ping()
        except Exception as e:  # noqa: BLE001
            task.append_log(f"[错误] LLM 连通性预检失败：{type(e).__name__}: {e}")
            task.append_log("[提示] 请先在「LLM 配置」页用「测试」按钮验证连通，再开始蒸馏。")
            raise

        def llm_fn(messages, **_kw):
            with _llm_env(template):
                return call_azure_openai(
                    messages,
                    model=template.model,
                    max_completion_tokens=template.max_tokens,
                    reasoning_effort=template.reasoning,
                    timeout=180,
                )

        model = template.model
        max_tokens = template.max_tokens
        reasoning = template.reasoning

    summary = collector.run_collect(
        fixtures_dir=fixtures_dir,
        skills_dir=skills_dir,
        domain_dir=domain_dir,
        domain=domain,
        llm_fn=llm_fn,
        on_log=task.append_log,
        dry_run=dry_run,
        model=model,
        max_tokens=max_tokens,
        reasoning=reasoning,
        stop_check=task.should_stop,
    )
    task.summary = summary
    task.append_log(
        f"[完成] 新增 {summary['added']} 条，跳过 {summary['skipped']} 个，技能库现有 {summary['total_skills']} 条"
    )
