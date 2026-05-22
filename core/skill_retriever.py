"""
core/skill_retriever.py
Skill retrieval with embedding search (primary) and metadata keyword
matching (fallback when no Gemini API key is available).

Domain-agnostic: rerank_prompt loaded from domain config.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from pathlib import Path

import numpy as np
from google import genai

log = logging.getLogger("skill_retriever")

_EMBED_MODEL = "gemini-embedding-001"
_EMBED_DIM = 3072
_EMBED_BATCH = 100

_RERANK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
]

# Default rerank prompt — overridden by domain config.
_DEFAULT_RERANK_PROMPT = """You are an expert skill selector. Given the task, pick the {n} most relevant and complementary skills.

## Task
{query}

## Candidate Skills
{candidates}

## Requirements
- Selected skills should be complementary, covering different aspects
- Avoid functionally overlapping skills
- Output ONLY a JSON array, no other text:
[{{"skill_id": "...", "skill_name": "...", "reason": "one-sentence rationale"}}]
"""


# ---------------------------------------------------------------------------
# Summary extraction (standardized field names across domains)
# ---------------------------------------------------------------------------

def extract_summary(analysis_text: str, skill_name: str = "") -> str:
    """Extract a compact summary from the structured analysis Markdown.

    Looks for standardized fields:
      - **Skill Name**
      - **Core Visual Mechanism** or **Core Mechanism**
      - **Overall Applicability** or **Applicability**

    Falls back to first 300 chars if structure is missing.
    """
    parts: list[str] = []

    if skill_name:
        parts.append(skill_name)
    else:
        m = re.search(r"\*\*Skill Name\*\*\s*:\s*(.+)", analysis_text)
        if m:
            parts.append(re.sub(r"[*`\[\]]+", "", m.group(1)).strip())

    # Try both "Core Visual Mechanism" and "Core Mechanism"
    m = re.search(r"\*\*Core (?:Visual )?Mechanism\*\*\s*:\s*(.+)", analysis_text)
    if m:
        parts.append(m.group(1).strip()[:300])

    # Try both "Overall Applicability" and "Applicability"
    m = re.search(r"\*\*(?:Overall )?Applicability\*\*\s*:\s*(.+)", analysis_text)
    if m:
        parts.append(m.group(1).strip()[:200])

    if not parts:
        return analysis_text[:300].strip()

    return " | ".join(parts)


# ---------------------------------------------------------------------------
# Embedding index
# ---------------------------------------------------------------------------

class EmbeddingIndex:
    """Manages the (skill_id -> vector) mapping backed by an .npz file."""

    def __init__(self, path: Path):
        self._path = path
        self.skill_ids: list[str] = []
        self.vectors: np.ndarray | None = None

    def load(self) -> bool:
        if not self._path.exists():
            return False
        data = np.load(self._path, allow_pickle=True)
        self.skill_ids = data["skill_ids"].tolist()
        self.vectors = data["vectors"].astype(np.float32)
        return True

    def save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(
            self._path,
            skill_ids=np.array(self.skill_ids, dtype=object),
            vectors=self.vectors,
        )

    def set(self, skill_ids: list[str], vectors: np.ndarray):
        self.skill_ids = list(skill_ids)
        self.vectors = _l2_normalise(vectors.astype(np.float32))

    def append(self, skill_id: str, vector: np.ndarray):
        vec = _l2_normalise(vector.astype(np.float32).reshape(1, -1))
        if self.vectors is None or len(self.skill_ids) == 0:
            self.skill_ids = [skill_id]
            self.vectors = vec
        else:
            if skill_id in self.skill_ids:
                idx = self.skill_ids.index(skill_id)
                self.vectors[idx] = vec[0]
            else:
                self.skill_ids.append(skill_id)
                self.vectors = np.vstack([self.vectors, vec])

    def search(self, query_vec: np.ndarray, top_k: int = 20) -> list[tuple[str, float]]:
        """Return [(skill_id, score)] sorted descending by cosine similarity."""
        if self.vectors is None or len(self.skill_ids) == 0:
            return []
        qv = _l2_normalise(query_vec.astype(np.float32).reshape(1, -1))[0]
        scores = self.vectors @ qv
        k = min(top_k, len(scores))
        top_idx = np.argpartition(scores, -k)[-k:]
        top_idx = top_idx[np.argsort(scores[top_idx])[::-1]]
        return [(self.skill_ids[i], float(scores[i])) for i in top_idx]

    @property
    def size(self) -> int:
        return len(self.skill_ids)


def _l2_normalise(v: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(v, axis=-1, keepdims=True)
    norms = np.maximum(norms, 1e-12)
    return v / norms


# ---------------------------------------------------------------------------
# Gemini API helpers
# ---------------------------------------------------------------------------

def _make_client(api_key: str | None = None) -> genai.Client:
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("Gemini API key required. Pass api_key= or set GEMINI_API_KEY.")
    return genai.Client(api_key=key)


def embed_texts(texts: list[str], *, api_key: str | None = None) -> np.ndarray:
    """Embed a list of texts via Gemini, returns (N, dim) array."""
    client = _make_client(api_key)
    all_vecs: list[list[float]] = []

    for i in range(0, len(texts), _EMBED_BATCH):
        batch = texts[i : i + _EMBED_BATCH]
        for attempt in range(3):
            try:
                resp = client.models.embed_content(
                    model=_EMBED_MODEL,
                    contents=batch,
                )
                for emb in resp.embeddings:
                    all_vecs.append(emb.values)
                break
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait = 2 ** attempt * 5
                    log.warning(f"Rate limited on embed batch {i}, wait {wait}s...")
                    time.sleep(wait)
                else:
                    raise
        log.info(f"Embedded {min(i + _EMBED_BATCH, len(texts))}/{len(texts)}")

    return np.array(all_vecs, dtype=np.float32)


def embed_single(text: str, *, api_key: str | None = None) -> np.ndarray:
    """Embed a single text, returns (dim,) array."""
    vecs = embed_texts([text], api_key=api_key)
    return vecs[0]


# ---------------------------------------------------------------------------
# Builder: construct embeddings for all skills in a domain
# ---------------------------------------------------------------------------

def build_embeddings(library_dir: Path, *, api_key: str | None = None) -> EmbeddingIndex:
    """Build embeddings for every skill in the library."""
    index_path = library_dir / "index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"No index.json at {index_path}")

    index_data = json.loads(index_path.read_text("utf-8"))
    skills = index_data.get("skills", [])
    log.info(f"Building embeddings for {len(skills)} skills...")

    skill_ids: list[str] = []
    summaries: list[str] = []

    for entry in skills:
        sid = entry["skill_id"]
        detail_path = library_dir / entry["detail_path"]
        if not detail_path.exists():
            log.warning(f"Missing detail file: {detail_path}, skip")
            continue

        detail = json.loads(detail_path.read_text("utf-8"))
        summary = extract_summary(
            detail.get("analysis", ""),
            skill_name=detail.get("skill_name", ""),
        )
        skill_ids.append(sid)
        summaries.append(summary)

    vectors = embed_texts(summaries, api_key=api_key)

    idx = EmbeddingIndex(library_dir / "embeddings.npz")
    idx.set(skill_ids, vectors)
    idx.save()

    log.info(f"Done. {idx.size} embeddings saved to {idx._path}")
    return idx


# ---------------------------------------------------------------------------
# Retriever
# ---------------------------------------------------------------------------

class SkillRetriever:
    """Embedding-based skill retrieval with LLM rerank."""

    def __init__(
        self,
        library_dir: Path | str,
        api_key: str | None = None,
        rerank_prompt: str | None = None,
    ):
        self._dir = Path(library_dir)
        self._api_key = api_key
        self._rerank_prompt = rerank_prompt or _DEFAULT_RERANK_PROMPT
        self._index_data: dict | None = None
        self._embed_index = EmbeddingIndex(self._dir / "embeddings.npz")
        self._loaded = False

    def _ensure_loaded(self):
        if self._loaded:
            return
        idx_path = self._dir / "index.json"
        if idx_path.exists():
            self._index_data = json.loads(idx_path.read_text("utf-8"))
        else:
            self._index_data = {"skills": []}
        self._embed_available = self._embed_index.load()
        if not self._embed_available:
            log.info("No embeddings.npz found; metadata fallback will be used.")
        self._loaded = True

    def _has_api_key(self) -> bool:
        return bool(self._api_key or os.environ.get("GEMINI_API_KEY"))

    def _entry_by_id(self, skill_id: str) -> dict | None:
        for s in self._index_data.get("skills", []):
            if s["skill_id"] == skill_id:
                return s
        return None

    def retrieve(self, query: str, top_k: int = 20) -> list[dict]:
        """Retrieve skills by embedding similarity, or metadata keywords as fallback."""
        self._ensure_loaded()

        if self._embed_available and self._has_api_key():
            qvec = embed_single(query, api_key=self._api_key)
            results = self._embed_index.search(qvec, top_k=top_k)
            candidates = []
            for sid, score in results:
                entry = self._entry_by_id(sid)
                if entry:
                    candidates.append({**entry, "score": round(score, 4)})
            return candidates

        log.info("Using metadata keyword fallback for retrieval.")
        return self._metadata_retrieve(query, top_k=top_k)

    def _metadata_retrieve(self, query: str, top_k: int = 20) -> list[dict]:
        """Keyword-based retrieval over index.json metadata + detail summaries."""
        skills = self._index_data.get("skills", [])
        if not skills:
            return []

        query_lower = query.lower()
        query_tokens = set(re.findall(r"[a-z\u4e00-\u9fff]+", query_lower))

        scored: list[tuple[dict, float]] = []
        for entry in skills:
            score = 0.0
            name_lower = entry.get("skill_name", "").lower()
            cat_lower = entry.get("category", "").lower()

            # category exact match: +5 per token
            for tok in query_tokens:
                if tok in cat_lower.replace("_", " ").split():
                    score += 5.0

            # skill_name token overlap: +3 per token
            name_tokens = set(re.findall(r"[a-z\u4e00-\u9fff]+", name_lower))
            score += len(query_tokens & name_tokens) * 3.0

            # substring match in skill_name: +2
            if query_lower in name_lower:
                score += 2.0

            # load detail summary for deeper matching
            detail_path = self._dir / entry.get("detail_path", "")
            if detail_path.exists():
                try:
                    detail = json.loads(detail_path.read_text("utf-8"))
                    summary = extract_summary(
                        detail.get("analysis", ""),
                        skill_name=detail.get("skill_name", ""),
                    ).lower()
                    for tok in query_tokens:
                        if tok in summary:
                            score += 1.0
                except Exception:
                    pass

            if score > 0:
                scored.append((entry, score))

        if not scored:
            # no keyword match at all — return all skills with zero score
            return [{**e, "score": 0.0} for e in skills[:top_k]]

        scored.sort(key=lambda x: x[1], reverse=True)
        max_score = scored[0][1]
        results = []
        for entry, raw in scored[:top_k]:
            results.append({**entry, "score": round(raw / max_score, 4)})
        return results

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        n: int = 5,
    ) -> list[dict]:
        """LLM rerank: pick the best n skills from candidates.

        Falls back to score-sorted top-n when no API key is available.
        """
        if not candidates:
            return []
        n = min(n, len(candidates))

        if not self._has_api_key():
            return [{"skill_id": c["skill_id"], "skill_name": c.get("skill_name", ""), "reason": "keyword score"} for c in candidates[:n]]

        lines = []
        for i, c in enumerate(candidates, 1):
            lines.append(
                f"{i}. [{c.get('category', '?')}] {c.get('skill_name', c['skill_id'])} "
                f"(id: {c['skill_id']}, score: {c.get('score', '?')})"
            )

        prompt = self._rerank_prompt.format(
            n=n,
            query=query,
            candidates="\n".join(lines),
        )

        client = _make_client(self._api_key)
        for model in _RERANK_MODELS:
            try:
                resp = client.models.generate_content(model=model, contents=prompt)
                text = resp.text.strip()
                m = re.search(r"\[.*\]", text, re.DOTALL)
                if m:
                    selected = json.loads(m.group())
                    return selected[:n]
            except Exception as e:
                log.warning(f"Rerank with {model} failed: {e}")
                continue

        return [{"skill_id": c["skill_id"], "skill_name": c.get("skill_name", ""), "reason": "score"} for c in candidates[:n]]

    def select(self, query: str, n: int = 5, top_k: int = 20) -> list[dict]:
        """One-stop: retrieve + rerank."""
        candidates = self.retrieve(query, top_k=top_k)
        return self.rerank(query, candidates, n=n)
