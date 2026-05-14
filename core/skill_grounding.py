"""Helpers for skill-grounding provenance manifests.

The B-route experiment treats skills as multimodal procedural references: the
agent may still write adapted code, but claimed provenance must stay explicit
and auditable.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


MANIFEST_FILENAME = "skill_trace_manifest.json"
SCHEMA_VERSION = 1


def coerce_str_list(value: Any) -> list[str]:
    """Normalize JSON-list, Python-list, or comma-separated strings."""
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            parsed = json.loads(text)
        except Exception:
            parsed = None
        if isinstance(parsed, (list, tuple)):
            return [str(v).strip() for v in parsed if str(v).strip()]
        return [v.strip() for v in text.split(",") if v.strip()]
    return [str(value).strip()] if str(value).strip() else []


def coerce_target_nodes(value: Any, fallback: str = "") -> list[str]:
    """Normalize target_node into one or more semantic section ids."""
    targets = coerce_str_list(value)
    if targets:
        return targets
    fallback = str(fallback or "").strip()
    return [fallback] if fallback else []


def artifact_manifest_path(artifact_path: str | Path) -> Path:
    """Return the standard sidecar path for an artifact file or directory."""
    path = Path(artifact_path)
    if path.suffix:
        return path.with_name(f"{path.stem}.{MANIFEST_FILENAME}")
    return path / MANIFEST_FILENAME


def load_manifest(path: str | Path, *, domain: str = "") -> dict[str, Any]:
    manifest_path = Path(path)
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("schema_version", SCHEMA_VERSION)
                data.setdefault("domain", domain or data.get("domain") or "")
                data.setdefault("groundings", [])
                return data
        except Exception:
            pass
    return {
        "schema_version": SCHEMA_VERSION,
        "domain": domain,
        "groundings": [],
    }


def make_grounding_entries(
    *,
    domain: str,
    tool_name: str,
    from_skill_ids: Any,
    target_node: Any = "",
    adaptation_notes: str = "",
    fallback_target: str = "",
    extra: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Create one manifest grounding per target node."""
    skill_ids = coerce_str_list(from_skill_ids)
    if not skill_ids:
        return []
    targets = coerce_target_nodes(target_node, fallback=fallback_target) or ["unspecified"]
    base = {
        "domain": domain,
        "tool_name": tool_name,
        "from_skill_ids": skill_ids,
        "adaptation_notes": str(adaptation_notes or "").strip(),
        "timestamp": time.time(),
    }
    if extra:
        base.update(extra)
    return [
        {
            **base,
            "target_node": target,
        }
        for target in targets
    ]


def append_groundings(
    manifest_path: str | Path,
    *,
    domain: str,
    tool_name: str,
    from_skill_ids: Any,
    target_node: Any = "",
    adaptation_notes: str = "",
    fallback_target: str = "",
    extra: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Append provenance entries to a JSON sidecar manifest."""
    entries = make_grounding_entries(
        domain=domain,
        tool_name=tool_name,
        from_skill_ids=from_skill_ids,
        target_node=target_node,
        adaptation_notes=adaptation_notes,
        fallback_target=fallback_target,
        extra=extra,
    )
    if not entries:
        return []

    path = Path(manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(path, domain=domain)
    manifest.setdefault("groundings", []).extend(entries)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return entries


def write_manifest(path: str | Path, manifest: dict[str, Any], *, domain: str = "") -> None:
    """Write a normalized manifest dictionary."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = dict(manifest or {})
    data.setdefault("schema_version", SCHEMA_VERSION)
    data.setdefault("domain", domain or data.get("domain") or "")
    data.setdefault("groundings", [])
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
