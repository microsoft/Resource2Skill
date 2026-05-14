"""``SourceConnector`` ABC: pluggable ingestion sources for the wiki.

A connector returns ``CandidateSkill`` records that the wash pipeline turns
into wiki entries. Each connector declares its ``source_type`` so the
per-cycle source-mix policy can route quotas; ``acquire`` accepts the
remaining quota for the cycle and is allowed to return fewer.
"""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CandidateSkill:
    """Raw skill payload yielded by a connector before wash.

    ``license`` may be ``None`` when the connector cannot determine it; the
    wash pipeline routes ``None`` and ``"blocked"`` to ``_quarantine/``.
    """

    skill_id: str
    skill_name: str
    domain: str
    source_type: str
    source_url: str | None = None
    source_channel: str | None = None
    license: str | None = None
    code_text: str | None = None
    code_filename: str | None = None
    text_overview: str | None = None
    visual_path: str | None = None
    applicability: str | None = None
    tags: list[str] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)

    def to_legacy_payload(self) -> dict[str, Any]:
        """Shape this candidate as a payload that ``wash_legacy_skill`` accepts.

        Includes ``text_overview`` / ``code_text`` / ``code_filename`` /
        ``visual_path`` so the collector can either materialize them to
        disk before the wash or fall back to ``_synthesise_overview``
        reading them straight from the payload. (Round-11: previously
        these were dropped silently.)
        """
        payload: dict[str, Any] = {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "domain": self.domain,
            "source": {
                "type": self.source_type,
                "url": self.source_url,
                "channel": self.source_channel,
            },
            "license": self.license,
            **self.extras,
        }
        if self.applicability:
            payload["applicability"] = self.applicability
        if self.tags:
            payload["tags"] = list(self.tags)
        if self.text_overview:
            payload["text_overview"] = self.text_overview
        if self.code_text is not None:
            payload["code_text"] = self.code_text
        if self.code_filename:
            payload["code_filename"] = self.code_filename
        if self.visual_path:
            payload["visual_path"] = self.visual_path
        return payload


class SourceConnector(abc.ABC):
    """Abstract base for ingestion connectors."""

    SOURCE_TYPE: str = ""

    @property
    def source_type(self) -> str:
        return self.SOURCE_TYPE

    @abc.abstractmethod
    def acquire(self, *, domain: str, quota: int, **kwargs: Any) -> list[CandidateSkill]:
        """Try to acquire up to ``quota`` candidates for ``domain``.

        Returning fewer than ``quota`` is allowed; only the YouTube
        connector is treated as hard-fail when its quota is unmet.
        """
        ...


__all__ = ["CandidateSkill", "SourceConnector"]
