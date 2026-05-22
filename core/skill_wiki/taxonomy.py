"""Operator-gated taxonomy growth: ``propose_category`` writes to a queue,
not directly to ``taxonomy.json``. A separate ``cli.py taxonomy-merge`` step
applies accepted entries with a ``node_history`` audit row.
"""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .registry import _atomic_write_json, _file_lock  # type: ignore[attr-defined]

_SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_MAX_PATH_DEPTH = 3


class TaxonomyError(Exception):
    """Base error for the taxonomy gate."""


@dataclass
class ProposalResult:
    accepted: bool
    status: str
    merged_into: list[str] | None = None
    queue_row_id: str | None = None
    error: str | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"accepted": self.accepted, "status": self.status}
        if self.merged_into is not None:
            out["merged_into"] = list(self.merged_into)
        if self.queue_row_id is not None:
            out["queue_row_id"] = self.queue_row_id
        if self.error is not None:
            out["error"] = self.error
        if self.message is not None:
            out["message"] = self.message
        return out


class TaxonomyGate:
    """Validate proposals, dedupe against existing tree + queue, append to queue.

    The gate is intentionally pure-Python with pluggable similarity hooks: the
    embedding-based sibling match is supplied by the caller so this module
    stays decoupled from the embeddings backend.
    """

    def __init__(
        self,
        *,
        domain_root: Path | str,
        similarity_threshold: float = 0.85,
        similarity_fn: Callable[[str, str], float] | None = None,
    ) -> None:
        self.domain_root = Path(domain_root)
        self.similarity_threshold = float(similarity_threshold)
        self._similarity_fn = similarity_fn

    @property
    def taxonomy_path(self) -> Path:
        return self.domain_root / "taxonomy.json"

    @property
    def queue_path(self) -> Path:
        return self.domain_root / "taxonomy_pending.jsonl"

    @property
    def lock_path(self) -> Path:
        return self.domain_root / ".taxonomy.lock"

    # Validation -----------------------------------------------------------

    @staticmethod
    def _validate_path(tier: str, path: list[str]) -> str | None:
        if not isinstance(tier, str) or not tier:
            return "tier must be a non-empty string"
        if not isinstance(path, list) or not path:
            return "path must be a non-empty list of segment names"
        if len(path) > _MAX_PATH_DEPTH:
            return f"path depth exceeds limit of {_MAX_PATH_DEPTH}"
        for segment in path:
            if not isinstance(segment, str) or not _SNAKE_CASE_RE.match(segment):
                return f"path segment {segment!r} must be snake_case"
        return None

    # Existing-tree probes -------------------------------------------------

    def _read_taxonomy(self) -> dict[str, Any]:
        if not self.taxonomy_path.exists():
            return {"domain": self.domain_root.name, "tree": {}, "node_history": []}
        with self.taxonomy_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _path_exists(self, tier: str, path: list[str]) -> bool:
        tree = self._read_taxonomy().get("tree", {}).get(tier, {})
        node = tree
        for segment in path:
            if not isinstance(node, dict) or segment not in node:
                return False
            node = node[segment]
        return True

    def _siblings(self, tier: str, path: list[str]) -> list[str]:
        tree = self._read_taxonomy().get("tree", {}).get(tier, {})
        node = tree
        for segment in path[:-1]:
            if not isinstance(node, dict) or segment not in node:
                return []
            node = node[segment]
        if not isinstance(node, dict):
            return []
        return [k for k in node.keys() if not k.startswith("_")]

    # Public API ----------------------------------------------------------

    def propose_category(
        self,
        *,
        tier: str,
        path: list[str],
        reason: str,
        example_skill_id: str | None = None,
    ) -> ProposalResult:
        validation_error = self._validate_path(tier, path)
        if validation_error:
            return ProposalResult(
                accepted=False,
                status="rejected",
                error=validation_error,
            )

        if self._path_exists(tier, path):
            return ProposalResult(
                accepted=False,
                status="duplicate",
                merged_into=list(path),
                message="proposed leaf already exists in taxonomy",
            )

        # Sibling-similarity probe.
        if self._similarity_fn is not None:
            best_sibling: tuple[str, float] | None = None
            for sibling in self._siblings(tier, path):
                key = f"{sibling} :: {reason}".strip()
                score = float(self._similarity_fn(path[-1], sibling) or 0.0)
                # Use the higher of (new_leaf vs sibling) and (reason vs sibling)
                # so both name- and reason-based merges are caught.
                rscore = float(self._similarity_fn(reason, key) or 0.0)
                score = max(score, rscore)
                if best_sibling is None or score > best_sibling[1]:
                    best_sibling = (sibling, score)
            if best_sibling and best_sibling[1] >= self.similarity_threshold:
                return ProposalResult(
                    accepted=False,
                    status="merged",
                    merged_into=list(path[:-1]) + [best_sibling[0]],
                    message=f"sibling cosine={best_sibling[1]:.3f} ≥ {self.similarity_threshold:.2f}",
                )

        with _file_lock(self.lock_path):
            row_id = self._append_queue_unsafe(
                tier=tier,
                path=path,
                reason=reason,
                example_skill_id=example_skill_id,
            )
        return ProposalResult(
            accepted=False,
            status="pending_review",
            queue_row_id=row_id,
            message="proposal queued for operator review",
        )

    def propose_rename(
        self,
        *,
        tier: str,
        old_path: list[str],
        new_path: list[str],
        reason: str,
    ) -> ProposalResult:
        """Queue a path-rename proposal.

        ``apply_merge`` for a renamed row triggers the rewrite hook so
        existing entries' ``category_path`` migrate from ``old_path`` to
        ``new_path``.
        """
        validation_error = self._validate_path(tier, new_path)
        if validation_error:
            return ProposalResult(accepted=False, status="rejected", error=validation_error)
        if not self._path_exists(tier, old_path):
            return ProposalResult(
                accepted=False, status="rejected",
                error=f"old_path {'/'.join(old_path)} does not exist under tier {tier}",
            )
        with _file_lock(self.lock_path):
            row_id = self._append_queue_unsafe(
                tier=tier, path=new_path, reason=reason, example_skill_id=None,
                rename_from=old_path,
            )
        return ProposalResult(
            accepted=False,
            status="pending_review",
            queue_row_id=row_id,
            message="rename proposal queued for operator review",
        )

    def _append_queue_unsafe(
        self,
        *,
        tier: str,
        path: list[str],
        reason: str,
        example_skill_id: str | None,
        rename_from: list[str] | None = None,
    ) -> str:
        # Dedupe: same (tier, path, rename_from) within the queue → reuse row id.
        existing_rows = self.read_queue()
        for row in existing_rows:
            same_path = list(row.get("path", [])) == list(path)
            same_rename = list(row.get("rename_from") or []) == list(rename_from or [])
            if row.get("tier") == tier and same_path and same_rename:
                return str(row.get("row_id", ""))
        row_id = f"prop_{int(time.time() * 1000)}_{os.getpid()}"
        record: dict[str, Any] = {
            "row_id": row_id,
            "tier": tier,
            "path": list(path),
            "reason": reason,
            "example_skill_id": example_skill_id,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        if rename_from is not None:
            record["rename_from"] = list(rename_from)
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, sort_keys=True) + "\n"
        with self.queue_path.open("a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
        return row_id

    def read_queue(self) -> list[dict[str, Any]]:
        if not self.queue_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        with self.queue_path.open("r", encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rows.append(json.loads(raw))
                except json.JSONDecodeError:
                    continue
        return rows

    # Operator merge ------------------------------------------------------

    def apply_merge(
        self,
        *,
        accepted_row_ids: list[str],
        approver: str,
        path_rewriter: Callable[[dict[tuple[str, ...], list[str]]], int] | None = None,
    ) -> dict[str, Any]:
        """Apply approved queue rows to ``taxonomy.json``.

        When the operator passes ``path_rewriter``, any row carrying an
        explicit ``rename_from`` (old path) results in a rewrite mapping
        that the registry-side hook applies to ``index.json`` and
        ``meta.json`` entries. Plain ``create`` rows insert a new node
        without rewriting existing entries (nothing has used the new path
        yet).
        """
        with _file_lock(self.lock_path):
            taxonomy = self._read_taxonomy()
            taxonomy.setdefault("tree", {})
            taxonomy.setdefault("node_history", [])
            queue = self.read_queue()
            applied: list[dict[str, Any]] = []
            remaining: list[dict[str, Any]] = []
            rewrites: dict[tuple[str, ...], list[str]] = {}
            for row in queue:
                if row.get("row_id") in set(accepted_row_ids):
                    self._insert_path(taxonomy["tree"], row["tier"], row["path"])
                    rename_from = row.get("rename_from")
                    history_row: dict[str, Any] = {
                        "action": "rename" if rename_from else "create",
                        "tier": row["tier"],
                        "path": list(row["path"]),
                        "approver": approver,
                        "reason": row.get("reason", ""),
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    }
                    if rename_from:
                        history_row["rename_from"] = list(rename_from)
                        rewrites[(row["tier"], tuple(rename_from))] = list(row["path"])
                    taxonomy["node_history"].append(history_row)
                    applied.append(row)
                else:
                    remaining.append(row)
            _atomic_write_json(self.taxonomy_path, taxonomy)
            self._rewrite_queue(remaining)

        rewritten_entries = 0
        if rewrites and path_rewriter is not None:
            rewritten_entries = int(path_rewriter(rewrites) or 0)
        return {
            "applied": applied,
            "remaining_pending": len(remaining),
            "rewritten_entries": rewritten_entries,
        }

    def _rewrite_queue(self, rows: list[dict[str, Any]]) -> None:
        if not rows:
            self.queue_path.write_text("", encoding="utf-8")
            return
        lines = [json.dumps(r, sort_keys=True) + "\n" for r in rows]
        tmp = self.queue_path.with_suffix(self.queue_path.suffix + ".tmp")
        tmp.write_text("".join(lines), encoding="utf-8")
        os.replace(tmp, self.queue_path)

    @staticmethod
    def _insert_path(tree: dict[str, Any], tier: str, path: list[str]) -> None:
        cursor = tree.setdefault(tier, {})
        for segment in path:
            cursor = cursor.setdefault(segment, {})
