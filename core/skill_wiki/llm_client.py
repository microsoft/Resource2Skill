"""Gemini-only model-call helper for the wash + connector distillation paths.

Per ``docs/skill_wiki_spec_final.md`` (§191-194, §1110-1113), the
normative model backend for skill-wiki classification and distillation
is **Gemini**. ``gemini-2.5-flash`` is the cheaper default;
``gemini-2.5-pro`` is reserved for the malformed-JSON / empty-response
retry. Round-14 removes the Azure ``gpt-5.4`` fallback that earlier
rounds kept around — Codex Round 13 review rejected it as a spec
violation.

If callers need an Azure path elsewhere in the project they should call
``core.llm.call_azure_openai`` directly. This helper is scoped to the
skill-wiki classification path and the spec only allows Gemini there.

Returns ``None`` on every failure path so call sites stay observable
via the diagnostics added in earlier rounds.
"""
from __future__ import annotations

import json
import os
from typing import Any


def model_backend() -> str:
    """Report the active backend name without making a call.

    Returns ``"gemini"`` when ``GEMINI_API_KEY`` is set; ``"none"``
    otherwise. Round-14: Azure is no longer reported here because the
    spec does not permit it as a wash/article classification backend.
    """
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    return "none"


def call_model_json(*, prompt: str, system: str | None = None,
                    max_tokens: int = 1024) -> dict[str, Any] | None:
    """Call Gemini with ``prompt`` and parse a JSON response.

    Round-14: Gemini-only. ``GEMINI_MODEL`` (default
    ``gemini-2.5-flash``) is tried first; on a malformed-JSON / empty
    / network failure the helper retries once with
    ``GEMINI_MODEL_FALLBACK`` (default ``gemini-2.5-pro``). When
    ``GEMINI_API_KEY`` is missing the helper returns ``None`` instead of
    silently falling back to Azure (Codex Round 13 finding 2).
    """
    if not os.environ.get("GEMINI_API_KEY"):
        return None
    primary = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    out = _call_gemini(model=primary, prompt=prompt, system=system,
                       max_tokens=max_tokens)
    if out is not None:
        return out
    fallback_model = os.environ.get("GEMINI_MODEL_FALLBACK", "gemini-2.5-pro")
    if fallback_model != primary:
        out = _call_gemini(model=fallback_model, prompt=prompt, system=system,
                           max_tokens=max_tokens)
        if out is not None:
            return out
    return None


def _call_gemini(*, model: str, prompt: str, system: str | None,
                 max_tokens: int) -> dict[str, Any] | None:
    """Invoke a specific Gemini model. Returns parsed JSON dict or None."""
    try:
        from google import genai  # type: ignore[import-untyped]
        from google.genai import types as genai_types  # type: ignore[import-untyped]
    except ImportError:
        return None
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        client = genai.Client(api_key=api_key)
        config = genai_types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=max_tokens,
            system_instruction=system,
        )
        resp = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        text = getattr(resp, "text", None) or ""
    except Exception:  # noqa: BLE001
        return None
    if not text:
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


__all__ = ["call_model_json", "model_backend"]
