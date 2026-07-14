"""Dependency-free Okapi BM25 candidate pool for wiki skill discovery.

This is stage 1 of the universal two-stage ``search_skills`` pipeline shared
by all five domains (web / ppt / excel / blender / reaper):

    BM25 candidate pool (this module)  ->  LLM rerank (``llm_rerank.py``)  ->  top k

It replaces the older bag-of-words *substring-presence* count
(``sum(1 for token in query.split() if token in haystack)``), which had no
IDF (every matched token weighed the same, so a query's rare discriminative
term was drowned out by common ones), no length normalisation, and matched on
substrings (``"art"`` hit ``"chart"``). Standard Okapi BM25 fixes all three:
IDF down-weights common terms, length normalisation removes the long-document
bias, and proper word tokenisation removes spurious substring hits.

Scope note: stage 1 only needs *recall into the pool* — the LLM rerank re-reads
every candidate and makes the final pick, so within-pool ordering is not
critical. A skill with zero lexical overlap still scores 0 and is excluded
(same recall floor as before); BM25's gain is pulling rare-term matches above
common-term matches so they survive into the pool.

No external dependency (``rank_bm25`` etc.) and no inverted index: the corpora
are < ~1000 entries per domain, so a single linear pass per query is sub-ms.

The embedding-based nearest-neighbour path that used to be scaffolded in the
ppt/web/excel adapters was removed — it was loaded-but-ignored dead code and no
index was ever built. Discovery is intentionally lexical (BM25) + LLM rerank.
"""
from __future__ import annotations

import math
import re
from typing import Any, Callable, Iterable

# Okapi BM25 free parameters (standard defaults).
_K1 = 1.5
_B = 0.75

# Skills are expected to ship a text/code + visual pair for the skill-path
# gate, so a visual asset is a mild positive signal. It is a *multiplicative*
# nudge on the BM25 relevance score (not a hard pre-sort and not a flat additive
# bonus), so relevance stays primary and visual only breaks near-ties. Tune here.
_VISUAL_BOOST = 1.25

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase word tokenisation: runs of ``[a-z0-9]`` (drops punctuation)."""
    return _TOKEN_RE.findall(text.lower())


def _haystack(entry: dict[str, Any]) -> str:
    """The searchable text for one registry entry: name + applicability + tags.

    Identical field set to the previous substring scorer, so the corpus the
    pool is drawn from does not change — only the scoring function does.
    """
    return " ".join([
        str(entry.get("skill_name") or ""),
        str(entry.get("applicability") or ""),
        " ".join(str(t) for t in (entry.get("tags") or [])),
    ])


def bm25_pool(
    entries: Iterable[dict[str, Any]],
    query: str,
    pool_size: int,
    *,
    has_visual: Callable[[str], bool],
    summary_view: Callable[[dict[str, Any]], dict[str, Any]],
    tier: str | None = None,
    skip_ids: Iterable[str] = (),
    visual_boost: float = _VISUAL_BOOST,
    k1: float = _K1,
    b: float = _B,
) -> list[dict[str, Any]]:
    """Score ``entries`` against ``query`` with Okapi BM25, return top pool.

    Args:
        entries: registry entries (the full domain list); filtered here.
        query: raw query string (tokenised internally).
        pool_size: max candidates to return (caller passes
            ``candidate_pool_size(k)``).
        has_visual: ``skill_id -> bool``, supplies the visual boost signal.
        summary_view: ``entry -> dict``, the per-domain summary projection.
        tier: optional exact-tier filter (caller resolves any aliases first).
        skip_ids: skill_ids to exclude (e.g. experiment opt-outs).
        visual_boost / k1 / b: tunables; defaults are the module constants.

    Returns the ``summary_view`` of each surviving entry, highest score first,
    truncated to ``pool_size``. Entries with no overlapping query term score 0
    and are dropped.
    """
    skip = set(skip_ids)
    # Pass 1: tokenise + accumulate document frequencies and total length.
    docs: list[tuple[dict[str, Any], int, dict[str, int]]] = []
    df: dict[str, int] = {}
    total_len = 0
    for entry in entries:
        if entry.get("skill_id") in skip:
            continue
        if tier is not None and entry.get("tier") != tier:
            continue
        tokens = tokenize(_haystack(entry))
        if not tokens:
            continue
        tf: dict[str, int] = {}
        for tok in tokens:
            tf[tok] = tf.get(tok, 0) + 1
        for tok in tf:
            df[tok] = df.get(tok, 0) + 1
        total_len += len(tokens)
        docs.append((entry, len(tokens), tf))

    n = len(docs)
    if n == 0:
        return []
    avgdl = total_len / n
    # Unique query terms, order preserved (dedup so a repeated query word does
    # not double-count).
    q_terms = list(dict.fromkeys(tokenize(query)))

    scored: list[tuple[float, dict[str, Any]]] = []
    for entry, doc_len, tf in docs:
        score = 0.0
        for term in q_terms:
            freq = tf.get(term)
            if not freq:
                continue
            # ``1 +`` guard keeps IDF non-negative even for terms appearing in
            # more than half the corpus (standard BM25+ idf).
            idf = math.log(1.0 + (n - df[term] + 0.5) / (df[term] + 0.5))
            denom = freq + k1 * (1.0 - b + b * doc_len / avgdl)
            score += idf * (freq * (k1 + 1.0)) / denom
        if score <= 0.0:
            continue
        if visual_boost != 1.0 and has_visual(entry["skill_id"]):
            score *= visual_boost
        scored.append((score, summary_view(entry)))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [view for _, view in scored[:pool_size]]


__all__ = ["bm25_pool", "tokenize"]
