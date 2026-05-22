"""
core/retrieval/picker.py — LLM pickers for archetype / theme / shell.

No embeddings. We dump all candidate cards to the LLM and ask it to
choose the best fit. Short prompts, Gemini Flash where possible.
"""
from __future__ import annotations

import json
import logging
import re

from core.llm import call_azure_openai, LLMError

from .archetype_loader import list_archetypes
from .cards import (
    format_archetype_card, format_shell_card_list, format_theme_card,
)

log = logging.getLogger("ppt.retrieval")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_id(text: str, candidates: list[str]) -> str | None:
    """Find the first candidate id that appears in the LLM response text."""
    if not text:
        return None
    # Try fenced JSON first
    m = re.search(r'"(?:chosen|archetype_id|theme_id|shell_id)"\s*:\s*"([a-z0-9_]+)"', text)
    if m and m.group(1) in candidates:
        return m.group(1)
    # Fall back to substring match, preferring the earliest mention
    best_pos = len(text) + 1
    best_id = None
    for c in candidates:
        p = text.find(c)
        if 0 <= p < best_pos:
            best_pos = p
            best_id = c
    return best_id


def _ask_llm(system: str, user: str, model: str = "gpt-5.4",
             reasoning_effort: str = "none") -> str:
    """One-shot call with low reasoning. Returns content string (possibly empty)."""
    try:
        msg = call_azure_openai(
            [{"role": "system", "content": system},
             {"role": "user",   "content": user}],
            model=model,
            reasoning_effort=reasoning_effort,
        )
        return msg.get("content", "") or ""
    except LLMError as e:
        log.warning("picker LLM call failed: %s", e)
        return ""


# ---------------------------------------------------------------------------
# Pickers
# ---------------------------------------------------------------------------


def pick_archetype(task_description: str) -> dict:
    """Ask the LLM which deck archetype fits a task description.

    Returns: {"archetype_id": str, "reasoning": str} or {"error": ...}
    """
    archetypes = list_archetypes()
    if not archetypes:
        return {"error": "No archetypes available"}

    cards = "\n\n".join(format_archetype_card(a) for a in archetypes)
    ids = [a["archetype_id"] for a in archetypes]

    system = (
        "You are helping pick a deck narrative structure for a presentation task. "
        "You will be given the user's task and a list of deck archetypes. "
        "Return JSON: {\"chosen\": \"<archetype_id>\", \"reasoning\": \"<one sentence>\"}."
    )
    user = (
        f"TASK: {task_description}\n\n"
        f"ARCHETYPES:\n\n{cards}\n\n"
        f"Reply with JSON only. Available ids: {', '.join(ids)}."
    )
    resp = _ask_llm(system, user)
    chosen = _extract_id(resp, ids)
    return {"archetype_id": chosen or ids[0], "reasoning": resp[:400]}


def pick_theme(task_description: str, themes: list[dict],
               archetype_id: str | None = None) -> dict:
    """Pick a theme id for the deck.

    Args:
        task_description: task string
        themes: list of theme summary dicts (from shell_loader.list_themes)
        archetype_id: optional, used only to narrow candidates by recommended_themes
    Returns: {"theme_id": str, "reasoning": str}
    """
    if not themes:
        return {"error": "No themes available"}

    # Narrow to archetype-recommended themes if available
    if archetype_id:
        try:
            arch = next((a for a in list_archetypes() if a["archetype_id"] == archetype_id), None)
            if arch and arch.get("recommended_themes"):
                themes = [t for t in themes if t["theme_id"] in arch["recommended_themes"]] or themes
        except Exception:
            pass

    cards = "\n\n".join(format_theme_card(t) for t in themes)
    ids = [t["theme_id"] for t in themes]
    system = (
        "You are picking a deck-wide design theme for a presentation task. "
        "Consider the industry and mood the task implies. "
        "Return JSON: {\"chosen\": \"<theme_id>\", \"reasoning\": \"<one sentence>\"}."
    )
    user = (
        f"TASK: {task_description}\n\n"
        f"THEMES:\n\n{cards}\n\n"
        f"Reply with JSON only. Available ids: {', '.join(ids)}."
    )
    resp = _ask_llm(system, user)
    chosen = _extract_id(resp, ids)
    return {"theme_id": chosen or ids[0], "reasoning": resp[:400]}


def pick_shell(slide_intent: str, candidate_shells: list[dict],
               top_k: int = 3) -> dict:
    """Ask LLM to pick the best shell for a slide intent from filtered candidates.

    Args:
        slide_intent: {"role": str, "content": str, "mood": str?, "theme_id": str?}
                       packed as a single string
        candidate_shells: list of shell cards post-filter
        top_k: how many to return in ranked order
    Returns: {"ranked": [{"shell_id": str, "reasoning": str}, ...]}
    """
    if not candidate_shells:
        return {"ranked": []}
    if len(candidate_shells) == 1:
        return {"ranked": [{"shell_id": candidate_shells[0]["shell_id"], "reasoning": "only candidate"}]}

    cards = format_shell_card_list(candidate_shells)
    ids = [s["shell_id"] for s in candidate_shells]
    system = (
        "You are picking a slide layout (shell) for a specific slide intent. "
        "Return JSON: {\"ranked\": [{\"shell_id\": \"...\", \"reasoning\": \"...\"}, ...]} "
        "in preference order, top choice first."
    )
    user = (
        f"SLIDE INTENT:\n{slide_intent}\n\n"
        f"CANDIDATE SHELLS:\n\n{cards}\n\n"
        f"Return top {top_k} ranked choices as JSON. Available ids: {', '.join(ids)}."
    )
    resp = _ask_llm(system, user)

    # Try to parse the ranked list; fall back to best-effort ordering
    ranked: list[dict] = []
    try:
        # Strip fences
        clean = resp.strip()
        if clean.startswith("```"):
            clean = re.sub(r"^```[a-z]*\n?|\n?```$", "", clean, flags=re.M)
        data = json.loads(clean)
        if isinstance(data, dict) and "ranked" in data and isinstance(data["ranked"], list):
            for item in data["ranked"]:
                if isinstance(item, dict) and item.get("shell_id") in ids:
                    ranked.append({
                        "shell_id": item["shell_id"],
                        "reasoning": str(item.get("reasoning", ""))[:200],
                    })
    except Exception:
        pass

    # Fallback: regex scan for each id in response order
    if not ranked:
        seen = set()
        for m in re.finditer(r'([a-z0-9_]+)', resp):
            cand = m.group(1)
            if cand in ids and cand not in seen:
                ranked.append({"shell_id": cand, "reasoning": "inferred from response text"})
                seen.add(cand)
                if len(ranked) >= top_k:
                    break

    # Ultimate fallback: first candidate
    if not ranked:
        ranked.append({"shell_id": ids[0], "reasoning": "fallback: first candidate"})

    return {"ranked": ranked[:top_k]}


__all__ = ["pick_archetype", "pick_theme", "pick_shell"]
