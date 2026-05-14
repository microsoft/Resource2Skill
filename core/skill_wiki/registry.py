"""Authoritative wiki registry: per-domain ``index.json`` with file lock,
write-ahead log, atomic-rename commit, WAL replay, and collision detection.

The registry is the single source of truth for every domain's wiki state.
Per-skill ``meta.json`` files are denormalised views; ``wiki-audit`` rebuilds
``index.json`` from them on demand.

Concurrency model:

  1. Acquire per-domain advisory file lock on ``.index.lock``.
  2. Append the row to ``wal.jsonl`` (one JSON line per pending op) with
     ``fsync``.
  3. Compute new ``index.json`` from prior + WAL rows.
  4. Write to ``index.json.tmp`` and ``os.replace`` over the destination.
  5. Truncate the WAL.

A crash before step 4 leaves the prior ``index.json`` intact; replay on next
open re-applies any unfinished WAL rows. Replay is idempotent because a
``put`` of an existing ``skill_id`` is treated as upsert at the registry
boundary (the public API rejects collisions before WAL append).
"""
from __future__ import annotations

import errno
import fcntl
import json
import os
import re
import tempfile
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator

import jsonschema  # type: ignore[import-untyped]

_SCHEMA_DIR = Path(__file__).parent / "schemas"
_INDEX_SCHEMA_PATH = _SCHEMA_DIR / "index.schema.json"
_META_SCHEMA_PATH = _SCHEMA_DIR / "meta.schema.json"

_SKILL_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_]*[a-z0-9]$")


class RegistryError(Exception):
    """Base error for the wiki registry."""


class DuplicateSkillError(RegistryError):
    """Raised when the same ``skill_id`` is inserted twice."""


class SchemaValidationError(RegistryError):
    """Raised when an entry or the manifest violates its JSON Schema."""


def _load_schema(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


_INDEX_SCHEMA: dict[str, Any] = _load_schema(_INDEX_SCHEMA_PATH)
_META_SCHEMA: dict[str, Any] = _load_schema(_META_SCHEMA_PATH)


@dataclass
class SkillEntry:
    """Lightweight wrapper around an index/meta entry dict."""

    skill_id: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_index_dict(self) -> dict[str, Any]:
        """Return the dict shape used inside ``index.json:entries[]``."""
        out = dict(self.data)
        out["skill_id"] = self.skill_id
        return out


def _validate_index(payload: dict[str, Any]) -> None:
    try:
        jsonschema.validate(instance=payload, schema=_INDEX_SCHEMA)
    except jsonschema.ValidationError as exc:  # type: ignore[attr-defined]
        raise SchemaValidationError(f"index.json schema violation: {exc.message}") from exc


def _validate_meta(payload: dict[str, Any]) -> None:
    try:
        jsonschema.validate(instance=payload, schema=_META_SCHEMA)
    except jsonschema.ValidationError as exc:  # type: ignore[attr-defined]
        raise SchemaValidationError(f"meta.json schema violation: {exc.message}") from exc


@contextmanager
def _file_lock(path: Path) -> Iterator[None]:
    """Per-domain advisory file lock backed by ``fcntl.flock``.

    Reentrant within the same process via a thread-local depth counter so
    nested ``with reg.write_lock():`` blocks do not deadlock.
    """
    lock_state = _file_lock._state  # type: ignore[attr-defined]
    key = str(path)
    depth = lock_state.depth.get(key, 0)
    if depth > 0:
        lock_state.depth[key] = depth + 1
        try:
            yield
        finally:
            lock_state.depth[key] = depth
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        lock_state.depth[key] = 1
        try:
            yield
        finally:
            lock_state.depth[key] = 0
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
    finally:
        os.close(fd)


_file_lock._state = threading.local()  # type: ignore[attr-defined]
if not hasattr(_file_lock._state, "depth"):  # type: ignore[attr-defined]
    _file_lock._state.depth = {}  # type: ignore[attr-defined]


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON atomically: tmp file in same dir + ``os.replace``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _append_wal(wal_path: Path, row: dict[str, Any]) -> None:
    wal_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, sort_keys=True) + "\n"
    with wal_path.open("a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())


def _read_wal(wal_path: Path) -> list[dict[str, Any]]:
    if not wal_path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with wal_path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError:
                # Tail of a partial line from a crashed writer; ignore.
                continue
    return rows


def _truncate_wal(wal_path: Path) -> None:
    if wal_path.exists():
        wal_path.write_text("", encoding="utf-8")


class WikiRegistry:
    """Per-domain wiki manifest with crash-safe writes.

    Layout::

        skills_wiki/<domain>/
            index.json           # authoritative manifest
            taxonomy.json        # operator-edited
            taxonomy_pending.jsonl
            wal.jsonl            # write-ahead log
            .index.lock          # advisory lock
            <skill_id>/
                source/ visual/ text/ code/ meta.json
            _quarantine/<skill_id>/
                quarantine_reason.json
    """

    def __init__(self, root: Path | str, *, domain: str, schema_version: str = "1.0.0",
                 wash_version: str = "1.0.0") -> None:
        self.root = Path(root).resolve()
        self.domain = domain
        self.schema_version = schema_version
        self.wash_version = wash_version
        self._cache: dict[str, Any] | None = None
        self._cache_mtime_ns: int | None = None
        self.root.mkdir(parents=True, exist_ok=True)

    # Path helpers ---------------------------------------------------------

    @property
    def index_path(self) -> Path:
        return self.root / "index.json"

    @property
    def wal_path(self) -> Path:
        return self.root / "wal.jsonl"

    @property
    def lock_path(self) -> Path:
        return self.root / ".index.lock"

    @property
    def quarantine_root(self) -> Path:
        return self.root / "_quarantine"

    def skill_dir(self, skill_id: str) -> Path:
        return self.root / skill_id

    # Lock surface ---------------------------------------------------------

    @contextmanager
    def write_lock(self) -> Iterator[None]:
        with _file_lock(self.lock_path):
            yield

    # Index (de)serialisation ---------------------------------------------

    def _empty_index(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "wash_version": self.wash_version,
            "domain": self.domain,
            "built_at": _utc_now(),
            "entries": [],
        }

    def load(self, *, force: bool = False) -> dict[str, Any]:
        """Read ``index.json`` (or seed an empty one), refreshing on mtime change."""
        path = self.index_path
        if not path.exists():
            self._cache = self._empty_index()
            self._cache_mtime_ns = None
            return self._cache

        mtime_ns = path.stat().st_mtime_ns
        if not force and self._cache is not None and self._cache_mtime_ns == mtime_ns:
            return self._cache

        with path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)

        if "domain" not in payload:
            payload["domain"] = self.domain
        if "entries" not in payload:
            payload["entries"] = []
        if "schema_version" not in payload:
            payload["schema_version"] = self.schema_version
        if "wash_version" not in payload:
            payload["wash_version"] = self.wash_version

        self._cache = payload
        self._cache_mtime_ns = mtime_ns
        return payload

    def reload(self) -> dict[str, Any]:
        """Force-refresh the in-memory cache; used by adapter cache invalidation."""
        return self.load(force=True)

    def list_entries(self) -> list[dict[str, Any]]:
        return list(self.load().get("entries", []))

    def get(self, skill_id: str) -> dict[str, Any] | None:
        for entry in self.list_entries():
            if entry.get("skill_id") == skill_id:
                return entry
        return None

    # Mutation -------------------------------------------------------------

    def put(self, entry: SkillEntry | dict[str, Any], *, allow_replace: bool = False) -> dict[str, Any]:
        """Insert or upsert a skill entry. Without ``allow_replace`` a duplicate raises."""
        payload = self._normalise_entry(entry)
        skill_id = payload["skill_id"]
        if not _SKILL_ID_RE.match(skill_id):
            raise RegistryError(
                f"invalid skill_id {skill_id!r}: must be lowercase snake-case, alphanumeric"
            )
        with self.write_lock():
            self._replay_wal_unsafe()
            existing = self._index_unsafe()
            seen = {e["skill_id"]: i for i, e in enumerate(existing["entries"])}
            if skill_id in seen and not allow_replace:
                raise DuplicateSkillError(
                    f"skill_id={skill_id!r} already present in domain={self.domain!r}"
                )
            row = {"op": "put", "entry": payload, "ts": _utc_now()}
            _append_wal(self.wal_path, row)
            self._apply_rows_and_commit_unsafe(existing, [row])
        return payload

    def remove(self, skill_id: str) -> bool:
        """Remove an entry from the index. Returns True if removed, False if absent."""
        with self.write_lock():
            self._replay_wal_unsafe()
            existing = self._index_unsafe()
            seen = {e["skill_id"]: i for i, e in enumerate(existing["entries"])}
            if skill_id not in seen:
                return False
            row = {"op": "remove", "skill_id": skill_id, "ts": _utc_now()}
            _append_wal(self.wal_path, row)
            self._apply_rows_and_commit_unsafe(existing, [row])
        return True

    def quarantine(self, skill_id: str, reason: str, *, payload: dict[str, Any] | None = None) -> None:
        """Route an entry to ``_quarantine/<skill_id>/``.

        Moves the on-disk skill directory under the quarantine root (so no
        orphan dir is left in the active manifest), removes the index row,
        and writes a ``quarantine_reason.json`` record alongside the moved
        payload.
        """
        target = self.quarantine_root / skill_id
        if target.exists():
            # Idempotent: a prior quarantine left state behind. Remove it
            # before reusing the slot to keep this path deterministic.
            import shutil as _shutil
            _shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)
        source_dir = self.skill_dir(skill_id)
        if source_dir.exists() and source_dir.is_dir():
            payload_dir = target / "payload"
            os.rename(source_dir, payload_dir)
        record = {
            "skill_id": skill_id,
            "quarantine_reason": reason,
            "ts": _utc_now(),
            "snapshot": payload,
        }
        _atomic_write_json(target / "quarantine_reason.json", record)
        self.remove(skill_id)

    def commit_meta(self, skill_id: str, meta: dict[str, Any]) -> None:
        """Write the per-skill ``meta.json`` after schema validation."""
        meta = dict(meta)
        meta["skill_id"] = skill_id
        meta.setdefault("schema_version", self.schema_version)
        meta.setdefault("wash_version", self.wash_version)
        _validate_meta(meta)
        skill_dir = self.skill_dir(skill_id)
        skill_dir.mkdir(parents=True, exist_ok=True)
        for sub in ("source", "visual", "text", "code"):
            (skill_dir / sub).mkdir(exist_ok=True)
        _atomic_write_json(skill_dir / "meta.json", meta)

    # WAL machinery --------------------------------------------------------

    def replay_wal(self) -> int:
        """Public WAL replay; returns number of rows applied."""
        with self.write_lock():
            return self._replay_wal_unsafe()

    def _replay_wal_unsafe(self) -> int:
        rows = _read_wal(self.wal_path)
        if not rows:
            return 0
        existing = self._index_unsafe()
        self._apply_rows_and_commit_unsafe(existing, rows, _from_replay=True)
        return len(rows)

    def _index_unsafe(self) -> dict[str, Any]:
        if self.index_path.exists():
            with self.index_path.open("r", encoding="utf-8") as fh:
                doc = json.load(fh)
        else:
            doc = self._empty_index()
        doc.setdefault("entries", [])
        doc.setdefault("schema_version", self.schema_version)
        doc.setdefault("wash_version", self.wash_version)
        doc.setdefault("domain", self.domain)
        return doc

    def _apply_rows_and_commit_unsafe(
        self,
        existing: dict[str, Any],
        rows: Iterable[dict[str, Any]],
        *,
        _from_replay: bool = False,
    ) -> None:
        index_by_id: dict[str, int] = {e["skill_id"]: i for i, e in enumerate(existing["entries"])}
        for row in rows:
            op = row.get("op")
            if op == "put":
                entry = self._normalise_entry(row["entry"])
                skill_id = entry["skill_id"]
                if skill_id in index_by_id:
                    existing["entries"][index_by_id[skill_id]] = entry
                else:
                    existing["entries"].append(entry)
                    index_by_id[skill_id] = len(existing["entries"]) - 1
            elif op == "remove":
                skill_id = row["skill_id"]
                idx = index_by_id.pop(skill_id, None)
                if idx is not None:
                    del existing["entries"][idx]
                    # Reindex downstream rows.
                    index_by_id = {e["skill_id"]: i for i, e in enumerate(existing["entries"])}
            else:
                # Unknown op — skip rather than crash so future schema bumps stay tolerant.
                continue
        existing["entries"].sort(key=lambda e: e["skill_id"])
        existing["built_at"] = _utc_now()
        _validate_index(existing)
        _atomic_write_json(self.index_path, existing)
        _truncate_wal(self.wal_path)
        self._cache = existing
        try:
            self._cache_mtime_ns = self.index_path.stat().st_mtime_ns
        except OSError:
            self._cache_mtime_ns = None

    # Helpers --------------------------------------------------------------

    def _normalise_entry(self, entry: SkillEntry | dict[str, Any]) -> dict[str, Any]:
        if isinstance(entry, SkillEntry):
            data = entry.to_index_dict()
        else:
            data = dict(entry)
        data.setdefault("schema_version", self.schema_version)
        data.setdefault("wash_version", self.wash_version)
        data.setdefault("modalities_present", [])
        data.setdefault("source", {"type": "manual"})
        data.setdefault("license", None)
        data.setdefault("exec_ok", None)
        return data

    # Audit / rebuild ------------------------------------------------------

    def rebuild_from_meta(self) -> dict[str, Any]:
        """Rebuild ``index.json`` from per-skill ``meta.json`` files."""
        with self.write_lock():
            payload = self._empty_index()
            for skill_dir in sorted(p for p in self.root.iterdir() if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")):
                meta_path = skill_dir / "meta.json"
                if not meta_path.exists():
                    continue
                with meta_path.open("r", encoding="utf-8") as fh:
                    meta = json.load(fh)
                payload["entries"].append(self._normalise_entry(meta))
            payload["entries"].sort(key=lambda e: e["skill_id"])
            _validate_index(payload)
            _atomic_write_json(self.index_path, payload)
            _truncate_wal(self.wal_path)
            self._cache = payload
            self._cache_mtime_ns = self.index_path.stat().st_mtime_ns
            return payload


def _utc_now() -> str:
    # ISO-8601 UTC with second precision; second precision is enough for our audit trail.
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# Convenience helpers -------------------------------------------------------

def open_registry(root: Path | str, *, domain: str, **kwargs: Any) -> WikiRegistry:
    return WikiRegistry(root=root, domain=domain, **kwargs)


def silence_unused_errno() -> None:  # pragma: no cover - kept for static analysis
    _ = errno  # noqa: F841
