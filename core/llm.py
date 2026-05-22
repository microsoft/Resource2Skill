"""
core/llm.py
Unified LLM backend: Azure OpenAI (GPT-5.4 with function calling) + Gemini fallback.

Usage:
    from core.llm import call_azure_openai, call_llm

    # Function-calling agent loop
    msg = call_azure_openai(messages, tools=openai_tools, model="gpt-5.4")

    # Simple text generation (drop-in for task_planner)
    text = call_llm("prompt", "system", backend="gemini")
"""
from __future__ import annotations

import json
import logging
import os
import threading
import time
from typing import Any

import requests

log = logging.getLogger("llm")

_AAD_TOKEN_CACHE: dict[tuple[str, str], tuple[str, float]] = {}
_AAD_TOKEN_LOCK = threading.Lock()

# ---------------------------------------------------------------------------
# Azure OpenAI configuration
# ---------------------------------------------------------------------------

_DEFAULT_ENDPOINT = ""

_DEPLOYMENT_MAP = {
    "gpt-5.5":      ("AZURE_OPENAI_DEPLOYMENT_55", "gpt-5.5"),
    "gpt-5.4":      ("AZURE_OPENAI_DEPLOYMENT_54", "gpt-5.4"),
    "gpt-5.4-pro":  ("AZURE_OPENAI_DEPLOYMENT_54PRO", "gpt-5.4-pro"),
    "gpt-5.4-mini": ("AZURE_OPENAI_DEPLOYMENT_54MINI", "gpt-5.4-mini"),
    "gpt-5.4-nano": ("AZURE_OPENAI_DEPLOYMENT_54NANO", "gpt-5.4-nano"),
    "gpt-5.1":      ("AZURE_OPENAI_DEPLOYMENT_51", "gpt-5.1"),
    "gpt-4.5":      ("AZURE_OPENAI_DEPLOYMENT_45", "gpt-4.5-preview"),
    "gpt-4o":       ("AZURE_OPENAI_DEPLOYMENT_4O", "gpt-4o"),
    "gpt-4o-audio-preview": ("AZURE_OPENAI_DEPLOYMENT_4O_AUDIO", "gpt-4o-audio-preview"),
    "gpt-audio":    ("AZURE_OPENAI_DEPLOYMENT_AUDIO", "gpt-audio"),
    "o3":           ("AZURE_OPENAI_DEPLOYMENT_O3", "o3-DR"),
}

_API_VERSION_MAP = {
    "gpt-5.5":      ("AZURE_OPENAI_API_VERSION_55", "2024-12-01-preview"),
    "gpt-5.4":      ("AZURE_OPENAI_API_VERSION_54", "2024-12-01-preview"),
    "gpt-5.4-pro":  ("AZURE_OPENAI_API_VERSION_54PRO", "2025-03-01-preview"),
    "gpt-5.4-mini": ("AZURE_OPENAI_API_VERSION_54", "2024-12-01-preview"),
    "gpt-5.4-nano": ("AZURE_OPENAI_API_VERSION_54", "2024-12-01-preview"),
    "gpt-5.1":      ("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    "gpt-4.5":      ("AZURE_OPENAI_API_VERSION_45", "2025-01-01-preview"),
    "gpt-4o":       ("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    "gpt-4o-audio-preview": ("AZURE_OPENAI_API_VERSION_4O_AUDIO", "2025-01-01-preview"),
    "gpt-audio":    ("AZURE_OPENAI_API_VERSION_AUDIO", "2025-01-01-preview"),
    "o3":           ("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
}

# Models that require the Responses API instead of chat/completions.
# gpt-5.5 is here because chat/completions rejects (tools + reasoning_effort)
# but the Responses API accepts both — we need reasoning=low parity with 5.4.
_RESPONSES_API_MODELS = {"gpt-5.4-pro", "gpt-5.5"}

# Models where Responses API DOES accept function-calling tools.
# (gpt-5.4-pro historically did not; we keep that behavior.)
_RESPONSES_API_SUPPORTS_TOOLS = {"gpt-5.5"}

# Valid reasoning efforts per model family
_REASONING_EFFORT_MAP = {
    "gpt-5.4-pro": ("medium", "high", "xhigh"),
}


def _model_env_suffix(model: str) -> str:
    """Map "gpt-5.5" -> "55", "gpt-5.4-pro" -> "54PRO" for per-model env vars."""
    key = model.lower().strip()
    return key.replace("gpt-", "").replace(".", "").replace("-", "").upper()


def _resolve_endpoint(model: str | None = None) -> str:
    """Per-model endpoint with fallback to global AZURE_OPENAI_ENDPOINT.

    Set AZURE_OPENAI_ENDPOINT_<MODEL_SUFFIX> to override a single model,
    for example AZURE_OPENAI_ENDPOINT_55 for gpt-5.5. Otherwise set the
    global AZURE_OPENAI_ENDPOINT.
    """
    if model:
        suffix = _model_env_suffix(model)
        ep = os.environ.get(f"AZURE_OPENAI_ENDPOINT_{suffix}", "").strip()
        if ep:
            if not ep.endswith("/"):
                ep += "/"
            return ep
    ep = os.environ.get("AZURE_OPENAI_ENDPOINT", _DEFAULT_ENDPOINT).strip()
    if not ep:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT is not set. Set it in the environment or "
            "use a per-model override such as AZURE_OPENAI_ENDPOINT_54."
        )
    if not ep.endswith("/"):
        ep += "/"
    return ep


def _resolve_deployment(model: str) -> str:
    key = model.lower().strip()
    env_var, default = _DEPLOYMENT_MAP.get(key, (None, key))
    if env_var:
        return os.environ.get(env_var, default)
    return default


def _resolve_api_version(model: str) -> str:
    key = model.lower().strip()
    env_var, default = _API_VERSION_MAP.get(key, (None, "2024-12-01-preview"))
    if env_var:
        return os.environ.get(env_var, default)
    return default


def _resolve_headers(model: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    # Per-model AAD opt-in: AZURE_OPENAI_USE_AAD_55=1 only flips 5.5 to AAD,
    # leaving 5.4 on key auth. Falls back to global AZURE_OPENAI_USE_AAD if
    # no per-model override is set.
    aad_flag = ""
    if model:
        suffix = _model_env_suffix(model)
        aad_flag = os.environ.get(f"AZURE_OPENAI_USE_AAD_{suffix}", "").strip().lower()
    if not aad_flag:
        aad_flag = os.environ.get("AZURE_OPENAI_USE_AAD", "0").strip().lower()
    if aad_flag in ("1", "true"):
        import subprocess
        scope = os.environ.get(
            "AZURE_OPENAI_AAD_SCOPE",
            "https://cognitiveservices.azure.com/",
        )
        suffix = _model_env_suffix(model or "")
        env_token = os.environ.get(f"AZURE_OPENAI_AAD_TOKEN_{suffix}", "").strip()
        if not env_token:
            env_token = os.environ.get("AZURE_OPENAI_AAD_TOKEN", "").strip()
        if env_token:
            token = env_token
        else:
            cache_key = (suffix, scope)
            now = time.time()
            with _AAD_TOKEN_LOCK:
                cached = _AAD_TOKEN_CACHE.get(cache_key)
                if cached and cached[1] > now + 300:
                    token = cached[0]
                else:
                    proc = subprocess.run(
                        ["az", "account", "get-access-token", "--resource", scope, "-o", "json"],
                        capture_output=True, text=True,
                    )
                    if proc.returncode != 0:
                        raise RuntimeError(f"AAD token fetch failed: {proc.stderr[:300]}")
                    data = json.loads(proc.stdout)
                    token = data.get("accessToken", "")
                    expires_on = data.get("expires_on")
                    try:
                        expiry = float(expires_on)
                    except (TypeError, ValueError):
                        expiry = now + 50 * 60
                    _AAD_TOKEN_CACHE[cache_key] = (token, expiry)
        headers["Authorization"] = f"Bearer {token}"
    else:
        api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError(
                "AZURE_OPENAI_API_KEY not set. "
                "Set it or use AZURE_OPENAI_USE_AAD=1 for AAD auth."
            )
        headers["api-key"] = api_key
    return headers


# ---------------------------------------------------------------------------
# Azure OpenAI call (with function calling support)
# ---------------------------------------------------------------------------

class LLMError(Exception):
    """Raised when all LLM call attempts fail."""


def _chat_to_responses_input(messages: list[dict]) -> list[dict]:
    """Translate chat-format messages into Responses API input items.

    Handles multi-turn agent conversations including tool calls and tool
    results so the Responses API can replay history.
    """
    items: list[dict] = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "") or ""
        content = _normalize_responses_content(content)
        if role == "system":
            items.append({"role": "developer", "content": content})
        elif role == "user":
            items.append({"role": "user", "content": content})
        elif role == "assistant":
            tcs = msg.get("tool_calls") or []
            if content:
                items.append({"role": "assistant", "content": content})
            for tc in tcs:
                fn = tc.get("function") or {}
                items.append({
                    "type": "function_call",
                    "call_id": tc.get("id", ""),
                    "name": fn.get("name", ""),
                    "arguments": fn.get("arguments", "") or "{}",
                })
        elif role == "tool":
            items.append({
                "type": "function_call_output",
                "call_id": msg.get("tool_call_id", ""),
                "output": content if isinstance(content, str) else json.dumps(content),
            })
        else:
            items.append({"role": role, "content": content})
    return items


def _normalize_responses_content(content: Any) -> Any:
    """Convert chat/completions content parts to Responses API parts.

    Chat payloads use {"type": "text"} and {"type": "image_url"} for
    multimodal messages. Responses API expects input_text/input_image instead.
    Plain string content is already accepted by the Responses API and is left
    unchanged.
    """
    if not isinstance(content, list):
        return content
    normalized: list[dict[str, Any]] = []
    for part in content:
        if not isinstance(part, dict):
            normalized.append({"type": "input_text", "text": str(part)})
            continue
        kind = part.get("type")
        if kind == "text":
            normalized.append({
                "type": "input_text",
                "text": str(part.get("text", "")),
            })
        elif kind == "image_url":
            image_url = part.get("image_url")
            if isinstance(image_url, dict):
                image_url = image_url.get("url", "")
            normalized.append({
                "type": "input_image",
                "image_url": str(image_url or ""),
            })
        elif kind in {
            "input_text", "input_image", "output_text", "refusal",
            "input_file", "computer_screenshot", "summary_text",
            "tether_browsing_display",
        }:
            normalized.append(part)
        else:
            normalized.append({
                "type": "input_text",
                "text": json.dumps(part, ensure_ascii=False),
            })
    return normalized


def _chat_tools_to_responses(tools: list[dict]) -> list[dict]:
    """Flatten chat-format tool specs ({type:function, function:{...}}) into
    Responses API format ({type:function, name, description, parameters})."""
    out: list[dict] = []
    for t in tools:
        if t.get("type") != "function":
            out.append(t); continue
        fn = t.get("function") or {}
        out.append({
            "type": "function",
            "name": fn.get("name", ""),
            "description": fn.get("description", ""),
            "parameters": fn.get("parameters", {"type": "object", "properties": {}}),
        })
    return out


def _responses_output_to_chat(data: dict) -> dict:
    """Translate Responses API output back into a chat-format assistant
    message with optional tool_calls. Uses call_id (not the function_call.id)
    as the chat tool_call.id so subsequent tool messages match correctly."""
    text_parts: list[str] = []
    tool_calls: list[dict] = []
    for item in data.get("output", []):
        t = item.get("type")
        if t == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    text_parts.append(part.get("text", ""))
        elif t == "function_call":
            tool_calls.append({
                "id": item.get("call_id", item.get("id", "")),
                "type": "function",
                "function": {
                    "name": item.get("name", ""),
                    "arguments": item.get("arguments", "") or "{}",
                },
            })
    msg: dict[str, Any] = {"role": "assistant"}
    msg["content"] = "".join(text_parts) or None
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return msg


def _call_responses_api(
    messages: list[dict],
    *,
    model: str,
    tools: list[dict] | None = None,
    reasoning_effort: str,
    max_completion_tokens: int,
    timeout: int,
    max_retries: int,
    retry_delay: float,
) -> dict:
    """
    Call Azure OpenAI Responses API for models like gpt-5.4-pro and gpt-5.5.

    Returns a chat/completions-style assistant message dict for compatibility
    with existing agent loops (may include tool_calls when the model invokes
    a function).
    """
    model_key = model.lower().strip()
    endpoint = _resolve_endpoint(model)
    deployment = _resolve_deployment(model)
    headers = _resolve_headers(model)

    # Responses API uses /openai/v1/responses (model in body, not URL path)
    url = f"{endpoint}openai/v1/responses"

    # Validate reasoning effort for this model
    allowed = _REASONING_EFFORT_MAP.get(model_key)
    if allowed and reasoning_effort not in allowed:
        log.warning("Model %s does not support reasoning_effort=%s, clamping to %s",
                    model, reasoning_effort, allowed[0])
        reasoning_effort = allowed[0]

    input_items = _chat_to_responses_input(messages)

    payload: dict[str, Any] = {
        "model": deployment,
        "input": input_items,
        "max_output_tokens": max_completion_tokens,
    }
    if reasoning_effort and reasoning_effort != "none":
        payload["reasoning"] = {"effort": reasoning_effort}

    if tools:
        if model_key in _RESPONSES_API_SUPPORTS_TOOLS:
            payload["tools"] = _chat_tools_to_responses(tools)
            payload["tool_choice"] = "auto"
            payload["parallel_tool_calls"] = False  # mirror chat path
        else:
            log.warning("%s via Responses API does not support function calling tools; ignoring tools param", model)

    last_error = ""
    for attempt in range(1, max_retries + 1):
        try:
            log.debug("Azure Responses API call attempt %d/%d → %s (effort=%s, tools=%s)",
                      attempt, max_retries, deployment, reasoning_effort, bool(tools))
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)

            if resp.status_code == 200:
                data = resp.json()
                msg = _responses_output_to_chat(data)
                log.debug("Azure Responses API response: content=%s, tool_calls=%s",
                          bool(msg.get("content")),
                          len(msg.get("tool_calls") or []))
                return msg

            if resp.status_code == 429 or resp.status_code >= 500:
                last_error = f"HTTP {resp.status_code}: {resp.text[:300]}"
                log.warning("Azure Responses API %d (attempt %d/%d), retrying in %.0fs...",
                            resp.status_code, attempt, max_retries, retry_delay)
                time.sleep(retry_delay)
                continue

            raise LLMError(f"Azure Responses API HTTP {resp.status_code}: {resp.text[:500]}")

        except requests.exceptions.Timeout:
            last_error = f"Timeout after {timeout}s"
            log.warning("Azure Responses API timeout (attempt %d/%d)", attempt, max_retries)
            time.sleep(retry_delay / 2)
        except requests.exceptions.ConnectionError as e:
            last_error = str(e)
            log.warning("Azure Responses API connection error (attempt %d/%d): %s",
                        attempt, max_retries, last_error[:200])
            time.sleep(retry_delay)

    raise LLMError(f"Azure Responses API exhausted {max_retries} retries. Last error: {last_error}")


def call_azure_openai(
    messages: list[dict],
    *,
    tools: list[dict] | None = None,
    model: str = "gpt-5.4",
    reasoning_effort: str = "medium",
    max_completion_tokens: int = 4096,
    timeout: int = 120,
    max_retries: int = 5,
    retry_delay: float = 10.0,
    tool_choice: str | dict | None = None,
) -> dict:
    """
    Call Azure OpenAI chat/completions with optional function calling.

    For models in _RESPONSES_API_MODELS (e.g. gpt-5.4-pro), automatically
    dispatches to the Responses API instead.

    Args:
        messages: Conversation history (system/user/assistant/tool messages).
        tools: OpenAI function calling tool definitions, or None.
        model: Model key (gpt-5.4, gpt-5.4-pro, gpt-4o, etc.).
        reasoning_effort: Thinking effort level.
            - chat/completions models: low/medium/high/none
            - gpt-5.4-pro: medium/high/xhigh only
        max_completion_tokens: Max tokens in response.
        timeout: HTTP request timeout in seconds.
        max_retries: Number of retry attempts on 429/5xx.
        retry_delay: Seconds to wait between retries.

    Returns:
        The assistant message dict from choices[0]["message"].
        May contain "content" (str), "tool_calls" (list), or both.

    Raises:
        LLMError: If all retries are exhausted.
    """
    model_key = model.lower().strip()

    # Dispatch to Responses API for models that need it. gpt-5.5 goes here so
    # we can pass tools + reasoning_effort together (chat/completions rejects
    # that combination for 5.5). gpt-5.4 stays on chat/completions unchanged.
    if model_key in _RESPONSES_API_MODELS:
        return _call_responses_api(
            messages,
            model=model,
            tools=tools,
            reasoning_effort=reasoning_effort or "medium",
            max_completion_tokens=max_completion_tokens,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

    endpoint = _resolve_endpoint(model)
    deployment = _resolve_deployment(model)
    api_version = _resolve_api_version(model)
    headers = _resolve_headers(model)

    url = f"{endpoint}openai/deployments/{deployment}/chat/completions?api-version={api_version}"

    payload: dict[str, Any] = {
        "messages": messages,
        "max_completion_tokens": max_completion_tokens,
    }

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = tool_choice or "auto"
        payload["parallel_tool_calls"] = False  # Force sequential, one at a time

    if reasoning_effort and reasoning_effort != "none":
        payload["reasoning_effort"] = reasoning_effort

    last_error = ""
    for attempt in range(1, max_retries + 1):
        try:
            log.debug("Azure OpenAI call attempt %d/%d → %s", attempt, max_retries, deployment)
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)

            if resp.status_code == 200:
                data = resp.json()
                msg = data["choices"][0]["message"]
                log.debug("Azure OpenAI response: content=%s, tool_calls=%s",
                          bool(msg.get("content")),
                          len(msg.get("tool_calls", [])))
                return msg

            if resp.status_code == 429 or resp.status_code >= 500:
                last_error = f"HTTP {resp.status_code}: {resp.text[:300]}"
                log.warning("Azure OpenAI %d (attempt %d/%d), retrying in %.0fs...",
                            resp.status_code, attempt, max_retries, retry_delay)
                time.sleep(retry_delay)
                continue

            # Non-retryable error
            raise LLMError(f"Azure OpenAI HTTP {resp.status_code}: {resp.text[:500]}")

        except requests.exceptions.Timeout:
            last_error = f"Timeout after {timeout}s"
            log.warning("Azure OpenAI timeout (attempt %d/%d)", attempt, max_retries)
            time.sleep(retry_delay / 2)
        except requests.exceptions.ConnectionError as e:
            last_error = str(e)
            log.warning("Azure OpenAI connection error (attempt %d/%d): %s",
                        attempt, max_retries, last_error[:200])
            time.sleep(retry_delay)

    raise LLMError(f"Azure OpenAI exhausted {max_retries} retries. Last error: {last_error}")


# ---------------------------------------------------------------------------
# Gemini backend (for backward compatibility with task_planner)
# ---------------------------------------------------------------------------

def _call_gemini(prompt: str, system: str = "", *, api_key: str | None = None) -> str:
    """Call Gemini for text generation."""
    from google import genai
    key = api_key or os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    models = ["gemini-2.5-flash", "gemini-2.5-pro"]
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    for model in models:
        try:
            resp = client.models.generate_content(model=model, contents=full_prompt)
            return resp.text.strip()
        except Exception as e:
            log.warning("Gemini %s failed: %s", model, e)
    return ""


# ---------------------------------------------------------------------------
# Unified call_llm (drop-in for task_planner)
# ---------------------------------------------------------------------------

def call_llm(
    prompt: str,
    system: str = "",
    *,
    backend: str = "gemini",
    **kw,
) -> str:
    """
    Simple text generation via Gemini or Azure OpenAI.

    For function-calling agent loops, use call_azure_openai() directly.
    """
    if backend == "azure" or backend == "gpt-5.4":
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        model = kw.pop("model", "gpt-5.4")
        try:
            msg = call_azure_openai(messages, model=model, **kw)
            return msg.get("content", "") or ""
        except LLMError as e:
            log.error("Azure call_llm failed: %s", e)
            return ""
    else:
        return _call_gemini(prompt, system, **kw)
