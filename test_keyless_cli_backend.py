from __future__ import annotations

from types import SimpleNamespace

import pytest

from core import analyzer, llm, llm_cli


def test_call_cli_keeps_runs_separate_with_explicit_conversation_ids(monkeypatch):
    llm_cli.reset_sessions()
    resume_ids: list[str | None] = []

    def fake_run_claude(prompt, *, system_prompt, resume_id, model, timeout):
        resume_ids.append(resume_id)
        return {"session_id": f"sess-{len(resume_ids)}", "result": "ok"}

    monkeypatch.setattr(llm_cli, "_run_claude", fake_run_claude)

    messages = [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "task"},
    ]

    llm_cli.call_cli(messages, conversation_id="run-a")
    llm_cli.call_cli(messages, conversation_id="run-b")

    assert resume_ids == [None, None]


def test_call_llm_honors_explicit_gemini_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("R2S_LLM_BACKEND", raising=False)
    monkeypatch.setattr(llm, "_cli_tool_available", lambda preferred=None: "claude")
    monkeypatch.setattr(llm, "_call_gemini", lambda prompt, system="", **kw: "gemini-ok")
    monkeypatch.setattr(
        "core.llm_cli.call_cli",
        lambda *args, **kwargs: pytest.fail("CLI fallback should not run when api_key is provided"),
    )

    assert llm.call_llm("prompt", backend="gemini", api_key="explicit-key") == "gemini-ok"


def test_analyze_video_honors_explicit_gemini_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("R2S_VIDEO_BACKEND", raising=False)
    monkeypatch.setattr(
        analyzer,
        "analyze_video_cli",
        lambda *args, **kwargs: pytest.fail("CLI fallback should not run when api_key is provided"),
    )
    monkeypatch.setattr(analyzer, "_load_prompt", lambda path=None: "prompt")
    monkeypatch.setattr(analyzer, "_make_client", lambda api_key=None: object())
    monkeypatch.setattr(
        analyzer,
        "types",
        SimpleNamespace(
            FileData=lambda file_uri: SimpleNamespace(file_uri=file_uri),
            VideoMetadata=lambda start_offset=None, end_offset=None: SimpleNamespace(
                start_offset=start_offset,
                end_offset=end_offset,
            ),
            Part=lambda **kwargs: SimpleNamespace(**kwargs),
        ),
    )
    monkeypatch.setattr(
        analyzer,
        "_call_with_retry",
        lambda client, model, parts, max_retries=3: SimpleNamespace(text="gemini-ok"),
    )

    assert analyzer.analyze_video("https://example.com/video", api_key="explicit-key") == "gemini-ok"
