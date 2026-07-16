"""Universal discovery + execution MCP tool registrar.

Wires the eight discovery methods + ``apply_skill`` + ``reload_registry``
onto a FastMCP instance, all routed through the supplied ``WikiAdapter``.

Per AC-6, ``check_discovery_surface()`` and ``check_capability_matrix()``
run at registration time so missing methods crash loudly *before*
``mcp.run()``.

When the host server has already registered legacy tools under any of the
universal names (``list_skills``, ``get_skill_code``, ``reload_registry``,
…), the registrar removes them before installing the wiki versions, so
the runtime surface is the wiki contract — not a legacy shadow.
"""
from __future__ import annotations

import logging
from typing import Any

from .contract import WikiAdapter

log = logging.getLogger("skill_wiki.mcp_tools")

# Universal tool names this registrar owns. Anything previously registered
# under these names on the host FastMCP instance is replaced.
#
# ``reload_registry`` is intentionally NOT in this set: the host server
# owns it permanently (the wiki registrar must not steal that tool, or a
# subsequent flip back to ``legacy`` would leave the server with no
# in-process recovery path).
_OWNED_NAMES: tuple[str, ...] = (
    "list_tiers",
    "list_categories",
    "list_skills",
    "get_skill_text",
    "get_skill_code",
    "get_skill_visual",
    "get_skill_recipe",
    "search_skills",
    "propose_category",
    "apply_skill",
)


def _purge_legacy_tools(mcp: Any) -> list[str]:
    """Remove any tool registered under one of our owned names.

    FastMCP's ``@mcp.tool()`` decorator does not overwrite an existing
    name; the original implementation keeps serving. The runtime surface
    therefore stays legacy unless the conflicting names are dropped.

    Returns the list of removed names so the caller can log them.
    """
    removed: list[str] = []
    manager = getattr(mcp, "_tool_manager", None)
    if manager is None:
        return removed
    tools = getattr(manager, "_tools", None)
    if tools is None:
        return removed
    for name in _OWNED_NAMES:
        if name in tools:
            del tools[name]
            removed.append(name)
    return removed


def register_wiki_tools(mcp: Any, adapter: WikiAdapter) -> None:
    """Register the universal discovery + execution surface.

    ``mcp`` is a FastMCP-like object with a ``tool()`` decorator factory.
    """
    adapter.check_discovery_surface()
    adapter.check_capability_matrix()

    purged = _purge_legacy_tools(mcp)
    if purged:
        log.info(
            "skill_wiki: replaced legacy MCP tools with wiki contract: %s", purged
        )

    @mcp.tool()
    def list_tiers() -> list[str]:
        """List the wiki tier identifiers (T1 through T5)."""
        return adapter.list_tiers()

    @mcp.tool()
    def list_categories(
        tier: str | None = None,
        category_path: str | None = None,
        depth: int = 2,
    ) -> dict:
        """Return the taxonomy subtree for the given tier and path."""
        return adapter.list_categories(tier=tier, category_path=category_path, depth=depth)

    @mcp.tool()
    def list_skills(
        tier: str | None = None,
        category_path: str | None = None,
        source_type: str | None = None,
        verified_only: bool = False,
        limit: int = 50,
    ) -> list:
        """List wiki entries filtered by tier, category prefix, source type, and verified status."""
        _ensure_fresh(adapter)
        return adapter.list_skills(
            tier=tier, category_path=category_path,
            source_type=source_type, verified_only=verified_only, limit=limit,
        )

    @mcp.tool()
    def get_skill_text(skill_id: str) -> dict:
        """Return the wiki text bundle for a skill (overview, name, applicability, tags)."""
        return adapter.get_skill_text(skill_id)

    @mcp.tool()
    def get_skill_code(skill_id: str) -> str:
        """Return the canonical code asset (or JSON dump for reference-only tiers)."""
        return adapter.get_skill_code(skill_id)

    @mcp.tool()
    def get_skill_visual(skill_id: str) -> dict:
        """Return the wiki visual bundle for a skill (thumbnail / preview path)."""
        return adapter.get_skill_visual(skill_id)

    @mcp.tool()
    def get_skill_recipe(skill_id: str) -> dict:
        """Return the compositional recipe for a skill, explicit or synthesized."""
        return adapter.get_skill_recipe(skill_id)

    @mcp.tool()
    def search_skills(
        query: str,
        tier: str | None = None,
        category_path: str | None = None,
        k: int = 5,
    ) -> list:
        """Nearest-neighbor (or substring fallback) search over wiki entries."""
        _ensure_fresh(adapter)
        return adapter.search_skills(query=query, tier=tier, category_path=category_path, k=k)

    @mcp.tool()
    def propose_category(
        tier: str,
        path: list[str],
        reason: str,
        example_skill_id: str | None = None,
    ) -> dict:
        """Queue a taxonomy proposal. Operator approves via cli.py taxonomy-merge."""
        return adapter.propose_category(
            tier=tier, path=path, reason=reason, example_skill_id=example_skill_id
        )

    @mcp.tool()
    def apply_skill(skill_id: str, target_id: str, kwargs_json: str = "{}") -> dict:
        """Tier+capability-matrix dispatch for a wiki skill against a target."""
        _ensure_fresh(adapter)
        return adapter.apply_skill(skill_id=skill_id, target_id=target_id, kwargs_json=kwargs_json)


def _ensure_fresh(adapter: WikiAdapter) -> None:
    """Detect a mid-session ``library_backend`` flip and react accordingly.

    Adapter subclasses that opted into backend tracking expose
    ``ensure_consistent_backend()``; calling it raises ``StaleRegistryError``
    when the flag has flipped without a reload, or auto-reloads when the
    adapter is configured to do so.
    """
    fn = getattr(adapter, "ensure_consistent_backend", None)
    if callable(fn):
        fn()


__all__ = ["register_wiki_tools"]
