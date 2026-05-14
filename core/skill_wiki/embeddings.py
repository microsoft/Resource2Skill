"""Pinned embedding model with sidecar metadata + compatibility check.

The wiki embeds skill text with a single, configured model. Each
``embeddings.npz`` is paired with an ``embeddings.meta.json`` sidecar that
records the model identity and version. ``search_skills`` refuses to load an
index whose sidecar disagrees with the runtime config: the goal is to make
silent model swaps loud.

This module deliberately avoids importing any concrete embedding SDK: it
operates on raw float arrays produced by callers (the wash pipeline or a test
harness), so the registry stays decoupled from Azure / OpenAI clients.
"""
from __future__ import annotations

import json
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np


class IncompatibleEmbeddingIndex(Exception):
    """Raised when an embeddings sidecar's model identity does not match config."""


@dataclass
class EmbeddingsMeta:
    embedding_model: str
    model_version: str
    dim: int
    built_at: str
    index_schema_version: str
    entry_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "embedding_model": self.embedding_model,
            "model_version": self.model_version,
            "dim": self.dim,
            "built_at": self.built_at,
            "index_schema_version": self.index_schema_version,
            "entry_count": self.entry_count,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EmbeddingsMeta":
        return cls(
            embedding_model=str(payload.get("embedding_model", "")),
            model_version=str(payload.get("model_version", "")),
            dim=int(payload.get("dim", 0)),
            built_at=str(payload.get("built_at", "")),
            index_schema_version=str(payload.get("index_schema_version", "")),
            entry_count=int(payload.get("entry_count", 0)),
        )


def write_embeddings(
    *,
    npz_path: Path | str,
    meta_path: Path | str,
    skill_ids: Sequence[str],
    matrix: np.ndarray,
    embedding_model: str,
    model_version: str,
    index_schema_version: str,
) -> EmbeddingsMeta:
    """Write the matrix + sidecar atomically together."""
    if matrix.ndim != 2:
        raise ValueError("embedding matrix must be 2-D (n_entries, dim)")
    if matrix.shape[0] != len(skill_ids):
        raise ValueError("len(skill_ids) must equal matrix rows")
    npz_path = Path(npz_path)
    meta_path = Path(meta_path)
    npz_path.parent.mkdir(parents=True, exist_ok=True)

    # numpy.savez auto-appends ".npz" when the destination does not already
    # end with it, so the temp path must keep that suffix to land where we
    # intend. We use a unique sibling that already ends in .npz, then
    # os.replace it onto the final destination (also .npz).
    fd, tmp_str = tempfile.mkstemp(prefix=npz_path.stem + ".", suffix=".npz", dir=str(npz_path.parent))
    os.close(fd)
    tmp_npz = Path(tmp_str)
    try:
        np.savez(tmp_npz, ids=np.array(list(skill_ids), dtype=object), matrix=matrix.astype(np.float32))
        os.replace(tmp_npz, npz_path)
    except Exception:
        try:
            tmp_npz.unlink(missing_ok=True)
        except OSError:
            pass
        raise

    meta = EmbeddingsMeta(
        embedding_model=embedding_model,
        model_version=model_version,
        dim=int(matrix.shape[1]),
        built_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        index_schema_version=index_schema_version,
        entry_count=int(matrix.shape[0]),
    )
    tmp_meta = meta_path.with_suffix(meta_path.suffix + ".tmp")
    tmp_meta.write_text(json.dumps(meta.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp_meta, meta_path)
    return meta


def read_meta(meta_path: Path | str) -> EmbeddingsMeta:
    payload = json.loads(Path(meta_path).read_text(encoding="utf-8"))
    return EmbeddingsMeta.from_dict(payload)


def load_compatible(
    *,
    npz_path: Path | str,
    meta_path: Path | str,
    expected_model: str,
) -> tuple[list[str], np.ndarray, EmbeddingsMeta]:
    """Load embeddings only if the sidecar matches ``expected_model``."""
    meta = read_meta(meta_path)
    if meta.embedding_model != expected_model:
        raise IncompatibleEmbeddingIndex(
            f"embedding model mismatch: index={meta.embedding_model!r} "
            f"expected={expected_model!r}; rebuild required",
        )
    bundle = np.load(Path(npz_path), allow_pickle=True)
    ids = list(bundle["ids"].tolist())
    matrix = np.asarray(bundle["matrix"], dtype=np.float32)
    if matrix.shape[1] != meta.dim:
        raise IncompatibleEmbeddingIndex(
            f"sidecar dim={meta.dim} but matrix dim={matrix.shape[1]}",
        )
    return ids, matrix, meta


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def cosine_matrix(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q_norm = np.linalg.norm(query)
    m_norms = np.linalg.norm(matrix, axis=1)
    denom = (m_norms * q_norm).clip(min=1e-12)
    return matrix @ query / denom
