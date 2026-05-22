"""Per-run append-only log files: ``logs/<command>_<timestamp>/<domain>.log``.

The plan's *Operational Conventions* require every wash run, collection
cycle, and snapshot to write a log under that path, headed with
``schema_version`` and ``wash_version`` so an operator can replay or
audit a run after the fact.

This module exposes a context manager + a structured-line writer the
CLI handlers wire into ``cmd_wiki_wash``, ``cmd_snapshot``, and the
connector cycle.
"""
from __future__ import annotations

import json
import logging
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, TextIO

from . import SCHEMA_VERSION, WASH_VERSION

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@contextmanager
def open_run_log(*, command: str, domain: str, project_root: Path | None = None) -> Iterator[TextIO]:
    """Yield an append-only file handle for ``logs/<command>_<ts>/<domain>.log``.

    Writes a header carrying the schema/wash versions before yielding;
    callers can then ``append`` structured lines via :func:`write_event`.
    """
    root = project_root or PROJECT_ROOT
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    log_dir = root / "logs" / f"{command}_{ts}"
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"{domain}.log"
    fh = path.open("a", encoding="utf-8")
    try:
        write_event(fh, "header", {
            "command": command,
            "domain": domain,
            "schema_version": SCHEMA_VERSION,
            "wash_version": WASH_VERSION,
            "ts": ts,
        })
        yield fh
    finally:
        fh.flush()
        fh.close()


def write_event(fh: TextIO, kind: str, payload: dict[str, Any]) -> None:
    """Append one structured event line."""
    record = {"kind": kind, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **payload}
    fh.write(json.dumps(record, sort_keys=True) + "\n")
    fh.flush()


__all__ = ["open_run_log", "write_event"]
