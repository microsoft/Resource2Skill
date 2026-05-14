"""Stale-registry guard for MCP servers that started on the legacy backend.

When a server starts with ``library_backend: legacy``, the universal wiki
registrar is never invoked, so the per-call ``ensure_consistent_backend``
hook inside ``mcp_tools.py`` never fires. A subsequent flip of
``domain.yaml`` to ``wiki`` would then leave the legacy discovery surface
serving silently.

``register_legacy_stale_check`` wraps every currently-registered tool on
the FastMCP instance with a guard that compares the configured backend to
the *expected* backend stored on the FastMCP instance. The expected
backend is initialised to the startup backend and can be re-keyed by
``mark_runtime_backend(mcp, backend)`` after a successful in-process
``_rebuild_runtime``. This lets the server unstick wrapped tools after
the operator flips ``library_backend`` and calls ``reload_registry``.

The guard is idempotent: re-registering wraps each tool only once.
"""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger("skill_wiki.legacy_stale")

_GUARDED_ATTR = "_skill_wiki_stale_guarded"
_STATE_ATTR = "_skill_wiki_guard_state"

# Tools that operators must be able to call even when the registry is
# stale; otherwise the documented remediation path becomes circular.
EXEMPT_TOOL_NAMES: frozenset[str] = frozenset({"reload_registry"})


def _get_state(mcp: Any) -> dict[str, Any]:
    """Lazily attach the guard's mutable state holder to the FastMCP instance."""
    state = getattr(mcp, _STATE_ATTR, None)
    if state is None:
        state = {"expected_backend": None, "domain": None}
        setattr(mcp, _STATE_ATTR, state)
    return state


def mark_runtime_backend(mcp: Any, backend: str) -> None:
    """Re-key the stale guard to a new expected backend.

    The server calls this after a successful ``_rebuild_runtime`` so
    previously wrapped tools become callable again under the new
    backend rather than returning ``stale_registry`` forever.
    """
    state = _get_state(mcp)
    state["expected_backend"] = backend


def register_legacy_stale_check(
    mcp: Any, *, domain: str, startup_backend: str,
    exempt: frozenset[str] | None = None,
) -> int:
    """Wrap every tool on ``mcp`` with a startup-backend consistency check.

    Tools whose name appears in ``exempt`` (default: ``{"reload_registry"}``)
    are left untouched so an operator can always invoke the remediation
    path after a backend flip. Returns the number of tools wrapped.
    """
    skip = (exempt if exempt is not None else EXEMPT_TOOL_NAMES)
    state = _get_state(mcp)
    state["expected_backend"] = startup_backend
    state["domain"] = domain
    manager = getattr(mcp, "_tool_manager", None)
    tools = getattr(manager, "_tools", None) if manager is not None else None
    if not tools:
        return 0
    wrapped = 0
    for name, tool in list(tools.items()):
        if name in skip:
            continue
        original_fn = getattr(tool, "fn", None)
        if not callable(original_fn):
            continue
        if getattr(original_fn, _GUARDED_ATTR, False):
            continue
        guarded = _wrap(original_fn, state=state, tool_name=name)
        setattr(guarded, _GUARDED_ATTR, True)
        tool.fn = guarded
        wrapped += 1
    return wrapped


def _wrap(fn: Any, *, state: dict[str, Any], tool_name: str) -> Any:
    def guarded(*args: Any, **kwargs: Any) -> Any:
        try:
            from core import get_active_library_backend
            current = get_active_library_backend(state.get("domain") or "")
        except Exception:  # noqa: BLE001
            return fn(*args, **kwargs)
        expected = state.get("expected_backend")
        if expected is not None and current != expected:
            log.warning(
                "skill_wiki: legacy server for %s detected backend flip %s -> %s on tool %s",
                state.get("domain"), expected, current, tool_name,
            )
            return {
                "error": "stale_registry",
                "domain": state.get("domain"),
                "startup_backend": expected,
                "configured_backend": current,
                "remediation": "restart the MCP server or call reload_registry",
                "tool": tool_name,
            }
        return fn(*args, **kwargs)
    guarded.__name__ = getattr(fn, "__name__", "guarded")
    guarded.__doc__ = getattr(fn, "__doc__", None)
    return guarded


__all__ = ["register_legacy_stale_check", "mark_runtime_backend", "EXEMPT_TOOL_NAMES"]
