"""Wiki-style skill registry: per-skill modality bundle, file-locked manifest,
versioned wash pipeline, capability-matrix execution adapters.

The package is domain-agnostic. Per-domain customisation lives in
``domains/<d>/wiki_adapter.py`` and the adapter's ``capabilities.json``.
"""
from __future__ import annotations

from .registry import (
    SkillEntry,
    WikiRegistry,
    RegistryError,
    DuplicateSkillError,
    SchemaValidationError,
)
from .contract import (
    WikiAdapter,
    DiscoveryContract,
    ExecutionResult,
    NotExecutableReason,
    StaleRegistryError,
)
from .budget import BudgetCap, BudgetExceeded, MissingBudgetConfig, load_budget_caps
from .taxonomy import TaxonomyGate, ProposalResult

SCHEMA_VERSION = "1.0.0"
WASH_VERSION = "1.0.0"

__all__ = [
    "SkillEntry",
    "WikiRegistry",
    "RegistryError",
    "DuplicateSkillError",
    "SchemaValidationError",
    "WikiAdapter",
    "DiscoveryContract",
    "ExecutionResult",
    "NotExecutableReason",
    "StaleRegistryError",
    "BudgetCap",
    "BudgetExceeded",
    "MissingBudgetConfig",
    "load_budget_caps",
    "TaxonomyGate",
    "ProposalResult",
    "SCHEMA_VERSION",
    "WASH_VERSION",
]
