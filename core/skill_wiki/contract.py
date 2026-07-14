"""Universal discovery contract + per-domain capability-matrix execution.

The discovery surface is identical across every domain MCP server. Execution
is dispatched through a per-domain ``WikiAdapter`` that declares a
``capabilities.json`` enumerating which verbs it implements; missing
capability returns a structured ``ExecutionResult.not_executable(...)`` error
rather than crashing.

Both halves are imported by every domain's MCP server, so this module must
remain free of domain-specific imports.
"""
from __future__ import annotations

import abc
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("skill_wiki.contract")


# Discovery contract method names — these are the universal MCP tool names
# every domain server must expose.
DISCOVERY_METHOD_NAMES: tuple[str, ...] = (
    "list_tiers",
    "list_categories",
    "list_skills",
    "get_skill_text",
    "get_skill_code",
    "get_skill_visual",
    "search_skills",
    "propose_category",
)


class NotExecutableReason:
    REFERENCE_ONLY = "reference_only"
    DOMAIN_CAPABILITY_MISSING = "domain_capability_missing"
    TIER_HAS_NO_CODE = "tier_has_no_code"
    SKILL_NOT_FOUND = "skill_not_found"
    EXEC_OK_FALSE = "exec_ok_false"


class StaleRegistryError(RuntimeError):
    """Raised when the configured ``library_backend`` has flipped mid-session.

    The runbook contract says the operator must restart or call
    ``reload_registry`` after a flip. When ``WikiAdapter`` is constructed
    with ``stale_registry_policy="error"`` and a flip is detected, the
    adapter raises this rather than silently serving stale data.
    """


@dataclass
class ExecutionResult:
    """Outcome of an ``apply_skill`` dispatch."""

    success: bool
    skill_id: str
    verb: str | None = None
    target_id: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    not_executable_reason: str | None = None

    @classmethod
    def ok(cls, skill_id: str, verb: str, target_id: str | None, detail: dict[str, Any] | None = None) -> "ExecutionResult":
        return cls(success=True, skill_id=skill_id, verb=verb, target_id=target_id, detail=detail or {})

    @classmethod
    def not_executable(cls, skill_id: str, reason: str, *, message: str | None = None) -> "ExecutionResult":
        return cls(
            success=False,
            skill_id=skill_id,
            error=message or f"skill is not executable: {reason}",
            not_executable_reason=reason,
        )

    @classmethod
    def fail(cls, skill_id: str, message: str, *, verb: str | None = None) -> "ExecutionResult":
        return cls(success=False, skill_id=skill_id, verb=verb, error=message)

    def to_json(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "success": self.success,
            "skill_id": self.skill_id,
        }
        if self.verb is not None:
            out["verb"] = self.verb
        if self.target_id is not None:
            out["target_id"] = self.target_id
        if self.detail:
            out["detail"] = self.detail
        if self.error is not None:
            out["error"] = self.error
        if self.not_executable_reason is not None:
            out["not_executable_reason"] = self.not_executable_reason
        return out


class DiscoveryContract(abc.ABC):
    """Interface implemented by every domain adapter for universal discovery.

    All return shapes are domain-agnostic; per-domain enrichment lives in the
    ``detail`` field of individual entries.
    """

    @abc.abstractmethod
    def list_tiers(self) -> list[str]:
        ...

    @abc.abstractmethod
    def list_categories(self, tier: str | None = None, category_path: str | None = None,
                        depth: int = 2) -> dict[str, Any]:
        ...

    @abc.abstractmethod
    def list_skills(self, tier: str | None = None, category_path: str | None = None,
                    source_type: str | None = None, verified_only: bool = False,
                    limit: int = 50) -> list[dict[str, Any]]:
        ...

    @abc.abstractmethod
    def get_skill_text(self, skill_id: str) -> dict[str, Any]:
        ...

    @abc.abstractmethod
    def get_skill_code(self, skill_id: str) -> str:
        ...

    @abc.abstractmethod
    def get_skill_visual(self, skill_id: str) -> dict[str, Any]:
        ...

    @abc.abstractmethod
    def search_skills(self, query: str, tier: str | None = None,
                      category_path: str | None = None, k: int = 5) -> list[dict[str, Any]]:
        ...

    @abc.abstractmethod
    def propose_category(self, tier: str, path: list[str], reason: str,
                         example_skill_id: str | None = None) -> dict[str, Any]:
        ...


class WikiAdapter(DiscoveryContract, abc.ABC):
    """Per-domain bridge between the wiki registry and the domain runtime.

    Subclasses declare:
      * ``DOMAIN``: the domain name string.
      * ``capabilities_path``: path to the adapter's ``capabilities.json``.

    They implement the abstract discovery methods plus zero or more execution
    verbs. The set of implemented verbs MUST match the ``capabilities.json``
    file at start-up; mismatches crash the server (loud failure, never silent).
    """

    DOMAIN: str = ""

    def __init__(
        self,
        *,
        capabilities_path: Path | str | None = None,
        stale_registry_policy: str = "auto_reload",
    ) -> None:
        self._capabilities_path = Path(capabilities_path) if capabilities_path else None
        self._capabilities: dict[str, Any] | None = None
        # ``error`` raises StaleRegistryError; ``auto_reload`` triggers reload();
        # any other value is treated as ``auto_reload`` for safety.
        self._stale_policy = stale_registry_policy if stale_registry_policy in {"error", "auto_reload"} else "auto_reload"
        self._observed_backend: str | None = self._read_active_backend()

    def _read_active_backend(self) -> str | None:
        """Best-effort read of the configured backend label for this domain."""
        if not self.DOMAIN:
            return None
        try:
            from core import get_active_library_backend  # local import to avoid cycle
        except ImportError:
            return None
        try:
            return str(get_active_library_backend(self.DOMAIN))
        except Exception:  # noqa: BLE001
            return None

    def ensure_consistent_backend(self) -> None:
        """Re-check the configured backend; react if it has flipped.

        Called by the universal MCP registrar on every list/search/apply
        call. If the policy is ``error``, raises ``StaleRegistryError``;
        otherwise calls ``reload()`` and updates the observed label.
        """
        current = self._read_active_backend()
        if current is None:
            return
        if self._observed_backend is None:
            self._observed_backend = current
            return
        if current != self._observed_backend:
            log.warning(
                "skill_wiki: %s backend flipped %s -> %s mid-session (policy=%s)",
                self.DOMAIN, self._observed_backend, current, self._stale_policy,
            )
            if self._stale_policy == "error":
                raise StaleRegistryError(
                    f"library_backend for {self.DOMAIN!r} flipped from "
                    f"{self._observed_backend!r} to {current!r}; call reload_registry "
                    f"or restart the MCP server"
                )
            # auto_reload
            self.reload()
            self._observed_backend = current

    # Capability surface ----------------------------------------------------

    @property
    def capabilities(self) -> dict[str, Any]:
        if self._capabilities is None:
            if self._capabilities_path is None or not self._capabilities_path.exists():
                self._capabilities = {"verbs": [], "tier_to_verbs": {}}
            else:
                with self._capabilities_path.open("r", encoding="utf-8") as fh:
                    self._capabilities = json.load(fh)
        return self._capabilities

    def declared_verbs(self) -> list[str]:
        return list(self.capabilities.get("verbs", []))

    def verbs_for_tier(self, tier: str) -> list[str]:
        return list(self.capabilities.get("tier_to_verbs", {}).get(tier, []))

    def check_capability_matrix(self) -> None:
        """Fail loudly at start-up if a declared verb is not implemented.

        Raises ``NotImplementedError`` listing the missing verbs.
        """
        missing = [v for v in self.declared_verbs() if not callable(getattr(self, v, None))]
        if missing:
            raise NotImplementedError(
                f"adapter for domain={self.DOMAIN!r} declares verbs {missing!r} in "
                f"capabilities.json but does not implement them"
            )

    def check_discovery_surface(self) -> None:
        """Fail loudly at start-up if a discovery method has not been overridden."""
        missing: list[str] = []
        for name in DISCOVERY_METHOD_NAMES:
            method = getattr(self, name, None)
            if method is None:
                missing.append(name)
        if missing:
            raise NotImplementedError(
                f"adapter for domain={self.DOMAIN!r} is missing discovery methods: {missing!r}"
            )

    # Execution dispatcher --------------------------------------------------

    def apply_skill(self, skill_id: str, target_id: str, kwargs_json: str = "{}") -> dict[str, Any]:
        """Tier+capability-matrix dispatch for a skill.

        Looks up the skill via ``self.list_skills`` (filtered to ``skill_id``).
        Resolves the verb from ``capabilities.tier_to_verbs[tier]``. Returns
        a structured ``ExecutionResult`` JSON dict in all cases — including
        not-executable / not-found / failure.
        """
        try:
            kwargs = json.loads(kwargs_json) if kwargs_json else {}
        except json.JSONDecodeError as exc:
            return ExecutionResult.fail(skill_id, f"invalid kwargs_json: {exc}").to_json()

        entries = self.list_skills(limit=10000)
        match = next((e for e in entries if e.get("skill_id") == skill_id), None)
        if match is None:
            return ExecutionResult.not_executable(
                skill_id, NotExecutableReason.SKILL_NOT_FOUND
            ).to_json()
        if match.get("exec_ok") is False:
            return ExecutionResult.not_executable(
                skill_id, NotExecutableReason.EXEC_OK_FALSE
            ).to_json()

        tier = match.get("tier", "")
        verbs = self.verbs_for_tier(tier)
        if not verbs:
            reason = (
                NotExecutableReason.TIER_HAS_NO_CODE
                if tier in {"T1", "T2"}
                else NotExecutableReason.DOMAIN_CAPABILITY_MISSING
            )
            return ExecutionResult.not_executable(skill_id, reason).to_json()

        verb = verbs[0]
        impl = getattr(self, verb, None)
        if not callable(impl):
            return ExecutionResult.not_executable(
                skill_id, NotExecutableReason.DOMAIN_CAPABILITY_MISSING,
                message=f"verb {verb!r} declared but not implemented",
            ).to_json()
        try:
            result = impl(skill_id=skill_id, target_id=target_id, **kwargs)
        except Exception as exc:  # noqa: BLE001
            return ExecutionResult.fail(skill_id, f"{type(exc).__name__}: {exc}", verb=verb).to_json()
        if isinstance(result, ExecutionResult):
            return result.to_json()
        if isinstance(result, dict):
            return ExecutionResult.ok(skill_id, verb, target_id, detail=result).to_json()
        return ExecutionResult.ok(skill_id, verb, target_id).to_json()

    def get_skill_recipe(self, skill_id: str) -> dict[str, Any]:
        """Return the per-skill compositional recipe.

        Domains can add explicit ``recipe.md`` files beside existing
        ``text/overview.md`` and ``code/*`` assets. To avoid a brittle
        all-at-once migration, this default implementation also synthesizes a
        compact recipe from the overview and code asset when no explicit file
        exists.
        """
        registry = getattr(self, "_registry", None)
        if registry is None:
            return {
                "skill_id": skill_id,
                "recipe": "",
                "source": None,
                "error": "adapter has no registry",
            }
        skill_dir = registry.skill_dir(skill_id)
        entry = registry.get(skill_id) or {}
        recipe_path = skill_dir / "recipe.md"
        if recipe_path.exists():
            return {
                "skill_id": skill_id,
                "name": entry.get("skill_name"),
                "tags": entry.get("tags", []),
                "confidence": _confidence_from_entry(entry),
                "reproducibility": _reproducibility_from_entry(entry),
                "recipe": recipe_path.read_text(encoding="utf-8", errors="ignore"),
                "source": "recipe.md",
            }

        overview_path = skill_dir / "text" / "overview.md"
        overview = (
            overview_path.read_text(encoding="utf-8", errors="ignore")
            if overview_path.exists()
            else ""
        )
        code = ""
        code_dir = skill_dir / "code"
        if code_dir.exists():
            for pattern in ("*.py", "*.html", "*.css", "*.js", "*.json"):
                found = sorted(code_dir.glob(pattern))
                if found:
                    code = found[0].read_text(encoding="utf-8", errors="ignore")
                    break
        if not code and overview:
            match = re.search(r"```(?:python|html|css|js|json)?\s*\n(.*?)```", overview, re.DOTALL | re.IGNORECASE)
            if match:
                code = match.group(1).strip()
        snippet = "\n".join(code.splitlines()[:70]) if code else ""
        overview_excerpt = "\n".join(overview.splitlines()[:80]) if overview else ""
        recipe = (
            f"# Recipe: {entry.get('skill_name') or skill_id}\n\n"
            f"- skill_id: `{skill_id}`\n"
            f"- tier: `{entry.get('tier', '')}`\n"
            f"- confidence: `{_confidence_from_entry(entry)}`\n"
            f"- reproducibility: `{_reproducibility_from_entry(entry)}`\n\n"
            "## Mechanism\n\n"
            f"{overview_excerpt or 'No overview text is available.'}\n\n"
            "## Composable Snippet\n\n"
            "Use this as a mechanism reference. Adapt workbook/project-specific "
            "data, labels, timing, and roles to the current brief.\n\n"
            "```text\n"
            f"{snippet or 'No code snippet is available; treat this as prose-only reference.'}\n"
            "```\n"
        )
        return {
            "skill_id": skill_id,
            "name": entry.get("skill_name"),
            "tags": entry.get("tags", []),
            "confidence": _confidence_from_entry(entry),
            "reproducibility": _reproducibility_from_entry(entry),
            "recipe": recipe,
            "source": "synthesized",
        }

    # Cache invalidation ----------------------------------------------------

    def reload(self) -> None:
        """Drop any cached state. Domain implementations should override and
        propagate to their underlying registry; the base implementation just
        clears the capabilities cache."""
        self._capabilities = None
        # Re-read the active backend so subsequent ensure_consistent_backend
        # calls see the post-reload value.
        self._observed_backend = self._read_active_backend()


def _confidence_from_entry(entry: dict[str, Any]) -> str:
    if entry.get("exec_ok") is True:
        return "verified"
    if entry.get("exec_ok") is False:
        return "experimental"
    return "source-reported"


def _reproducibility_from_entry(entry: dict[str, Any]) -> str:
    modalities = set(entry.get("modalities_present") or [])
    if "code" in modalities or entry.get("tier") in {"T3", "T4", "T5"}:
        return "snippet"
    if "text" in modalities:
        return "prose-only"
    return "unknown"
