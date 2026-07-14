"""Shared LLM-rerank for skill discovery.

Each domain's ``wiki_adapter.search_skills`` runs cheap BoW substring scoring
to produce a top-N candidate pool, then calls :func:`llm_rerank_skills`
to ask Azure GPT-5.5 (reasoning=low) which k candidates best match the query.

This generalises the PPT-Master ``pptmaster_select_r2s_refs`` rerank
(``domains/ppt/pptmaster_r2s_prompt_runner.py``) so all 5 domains
(web / ppt / excel / blender / reaper) share the same selection mechanism.
The PPTMaster brief-aware rerank stays separate — it takes a structured
brief dict, not a raw query string.

Fail-loud policy: every failure path raises :class:`LLMRerankError`. Callers
must NOT swallow the exception silently — surface it so the underlying cause
(missing Azure creds, rate limit, malformed LLM output) gets fixed.
"""

from __future__ import annotations

import json as _json
import logging
import os
import re
from typing import Any

log = logging.getLogger(__name__)


class LLMRerankError(RuntimeError):
    """Raised when the LLM-rerank pipeline cannot produce a usable picks list.

    The default contract is fail-loud: callers MUST surface this rather than
    fall back to the BoW pool silently, so configuration / quota / parsing
    issues actually get reported. If a caller has a legitimate reason to
    degrade gracefully (e.g. an experiment ablation), it can catch this
    explicitly.
    """


# Per-domain hint that nudges the rerank toward the right kind of skill.
# Kept short so the system prompt stays small.
DOMAIN_HINTS: dict[str, str] = {
    "ppt": (
        "Each skill is a documented PPT slide construction technique distilled "
        "from a human designer. Pick skills whose visual TONE matches the query "
        "(cinematic/editorial/data-dashboard/playful)."
    ),
    "web": (
        "Each skill is a documented HTML/CSS/JS technique. Pick skills whose "
        "interaction model + layout + visual language match the query — "
        "not just keyword overlap."
    ),
    "excel": (
        "Each skill is a workbook construction technique (formulas, tables, "
        "charts, dashboards). Pick skills matching the data shape and analytical "
        "intent of the query."
    ),
    "blender": (
        "Each skill is a 3D scene construction technique. Pick skills matching "
        "the query's subject, style, lighting, and composition."
    ),
    "reaper": (
        "Each skill is a music production technique. Pick skills matching the "
        "query's genre, mood, instrumentation, and arrangement intent."
    ),
}

_GENERIC_HINT = (
    "Each skill is a documented procedural technique. Pick the skills whose "
    "mechanism matches the query intent."
)


def llm_rerank_skills(
    *,
    query: str,
    candidate_ids: list[str],
    registry_entries: list[dict[str, Any]],
    k: int,
    domain: str = "",
    model: str = "gpt-5.5",
    reasoning_effort: str = "low",
    max_completion_tokens: int = 600,
    timeout: int = 60,
) -> list[str]:
    """Ask Azure GPT-5.5 to pick the ``k`` candidates best matching ``query``.

    Reads each candidate's name, category, applicability, and tags — not
    full overview/code/visual — to keep the prompt under ~6K tokens.
    Returns the reranked skill_ids in priority order (length <= k).

    Raises :class:`LLMRerankError` on:
      * Missing ``core.llm`` (broken install)
      * Azure call failure (no creds, network, rate limit, content filter)
      * Empty / non-JSON / malformed LLM response
      * Picks list does not intersect candidate set

    Callers should NOT swallow this exception — let it propagate so the
    real failure gets fixed instead of silently degrading to BoW.
    """
    if not candidate_ids:
        raise LLMRerankError("no candidates to rerank")
    if k <= 0:
        raise LLMRerankError(f"invalid k={k}")
    try:
        from core.llm import call_azure_openai  # local import to avoid cycle
    except ImportError as exc:
        raise LLMRerankError(f"core.llm unavailable: {exc}") from exc

    os.environ.setdefault("AZURE_OPENAI_USE_AAD", "1")

    by_id = {str(e.get("skill_id")): e for e in registry_entries}
    catalog_lines: list[str] = []
    for cid in candidate_ids:
        e = by_id.get(cid)
        if not e:
            continue
        cat = " / ".join(str(x) for x in (e.get("category_path") or [])) or "(uncat)"
        applic = (e.get("applicability") or "").strip().replace("\n", " ")
        if len(applic) > 200:
            applic = applic[:200] + "…"
        tags = ", ".join(str(t) for t in (e.get("tags") or [])[:6])
        catalog_lines.append(
            f"- id: {cid}\n  name: {e.get('skill_name', '?')}\n"
            f"  category: {cat}\n  applicability: {applic}\n"
            f"  tags: {tags}"
        )
    if not catalog_lines:
        raise LLMRerankError(
            f"none of {len(candidate_ids)} candidate ids matched registry entries"
        )
    catalog = "\n".join(catalog_lines)

    hint = DOMAIN_HINTS.get(domain, _GENERIC_HINT)
    system = (
        f"You pick skill references from a library. {hint} "
        "Pick the k skill_ids whose mechanism BEST matches the query — "
        "not just surface keyword overlap. Avoid stacking near-duplicates."
    )
    user = (
        f"Query:\n{query}\n\n"
        f"Candidates ({len(catalog_lines)}):\n{catalog}\n\n"
        f"Pick the top {k} skill_ids in priority order. "
        f"Output ONLY a JSON object: "
        f'{{"picks": ["id1", "id2", ...], "why": "one sentence rationale"}}. '
        f"No prose outside the JSON."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    try:
        resp = call_azure_openai(
            messages,
            model=model,
            reasoning_effort=reasoning_effort,
            max_completion_tokens=max_completion_tokens,
            timeout=timeout,
            max_retries=2,
            retry_delay=4.0,
        )
    except Exception as exc:  # noqa: BLE001
        raise LLMRerankError(
            f"Azure {model} reasoning={reasoning_effort} call failed: "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    text = (resp.get("content") or "").strip()
    if not text:
        raise LLMRerankError(f"Azure {model} returned empty content")
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = _json.loads(text)
    except _json.JSONDecodeError as exc:
        raise LLMRerankError(
            f"LLM response is not valid JSON: {text[:200]!r}"
        ) from exc
    if not isinstance(data, dict):
        raise LLMRerankError(f"LLM response is not a JSON object: {type(data).__name__}")
    picks = data.get("picks")
    if not isinstance(picks, list):
        raise LLMRerankError(
            f"LLM response missing 'picks' list (got {type(picks).__name__})"
        )

    candidate_set = set(candidate_ids)
    out: list[str] = []
    for p in picks:
        sid = str(p).strip()
        if sid and sid in candidate_set and sid not in out:
            out.append(sid)
        if len(out) >= k:
            break
    if not out:
        raise LLMRerankError(
            f"LLM picks {picks!r} do not intersect candidate set "
            f"({len(candidate_ids)} ids)"
        )
    return out


def candidate_pool_size(k: int, *, multiplier: int = 5, floor: int = 25) -> int:
    """Pick the candidate pool size for the BoW pre-filter.

    Default: max(k*5, 25). Adapters can override but this is a sensible
    floor that gives the LLM rerank enough variety without overflowing the
    prompt.
    """
    return max(k * multiplier, floor)
