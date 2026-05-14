"""Article source connector.

Fetches public articles / docs and distils them into candidate skills.
The connector uses readability-lxml when available and derives license
metadata from common HTML signals (``<link rel="license">``,
``<meta name="license">``, ``<meta property="og:license">``, page meta
tags). The wash pipeline then quarantines ``None`` / ``"blocked"``.

When ``GEMINI_API_KEY`` is set, ``acquire`` runs a Gemini distillation
pass to extract a structured ``{title, applicability, tags, summary}``
payload from each article body. Round-14 enforces the spec's
Gemini-only contract: Azure ``gpt-5.4`` is no longer accepted as a
classification/distillation backend (`docs/skill_wiki_spec_final.md`
§model contract). Without a Gemini key the connector deterministically
falls back to readability output.

AC-14 (Round-14): when a ``BudgetTracker`` is supplied and the cap is
hit, ``tracker.check()`` raises ``BudgetExceeded`` and the connector
**propagates** that exception. Previously the cap was silently
converted into a ``readability_budget_blocked`` distillation_used
label, which let ``cli.py collect`` succeed mid-cap and violated AC-14
at the command level.

Returns ``[]`` when no URLs are configured so the cycle driver can
continue without a hard fail.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

from .base import CandidateSkill, SourceConnector


# Permissive license substrings we recognise in href / content fields.
_PERMISSIVE_LICENSE_SUBSTRINGS = (
    ("creativecommons.org/licenses/by/", "cc-by-4.0"),
    ("creativecommons.org/licenses/by-sa/", "cc-by-sa-4.0"),
    ("creativecommons.org/publicdomain/zero", "cc0-1.0"),
    ("opensource.org/licenses/mit", "mit"),
    ("opensource.org/licenses/apache", "apache-2.0"),
    ("apache.org/licenses/license-2.0", "apache-2.0"),
    ("publicdomain", "public-domain"),
)


class ArticleConnector(SourceConnector):
    SOURCE_TYPE = "article"

    def __init__(self, *, urls: list[str] | None = None,
                 default_license: str | None = None,
                 use_gemini: bool | None = None,
                 budget_tracker: Any = None) -> None:
        self.urls = list(urls or [])
        self.default_license = default_license
        # Round-14: distillation requires GEMINI_API_KEY per spec
        # (`docs/skill_wiki_spec_final.md` §model contract). Azure-only
        # environments fall back to readability extraction instead of
        # being treated as a valid distillation backend.
        if use_gemini is None:
            self.use_gemini = bool(os.environ.get("GEMINI_API_KEY"))
        else:
            self.use_gemini = bool(use_gemini)
        # Round-11: optional BudgetTracker; when present, distillation
        # consumes one quota unit per call. Round-14: a cap-reached
        # BudgetExceeded is no longer downgraded to a readability
        # fallback — it propagates so AC-14 holds at the command level.
        self.budget_tracker = budget_tracker

    def acquire(self, *, domain: str, quota: int, **kwargs: Any) -> list[CandidateSkill]:
        if quota <= 0:
            return []
        urls = list(kwargs.get("urls") or self.urls)
        if not urls:
            return []
        try:
            import requests  # type: ignore[import-untyped]
        except ImportError:
            return []
        out: list[CandidateSkill] = []
        for url in urls[:quota]:
            try:
                resp = requests.get(url, timeout=10, headers={"User-Agent": "skill-wiki/1.0"})
                if resp.status_code != 200:
                    continue
                html = resp.text
            except Exception:  # noqa: BLE001
                continue
            title, body = _extract_title_body(html)
            license_value = _derive_license(html) or self.default_license
            if not title:
                title = url
            slug = _slug_from_url(url)

            # Distillation pass: enrich with structured fields when API
            # access is configured. Falls back to readability output on
            # any failure (no behavioural change vs. the deterministic
            # path). Round-11: consumes BudgetTracker quota when one is
            # configured; cap-reached → deterministic fallback.
            distilled: dict[str, Any] | None = None
            distillation_used = "readability"
            tracker = kwargs.get("budget_tracker", self.budget_tracker)
            if self.use_gemini and body:
                # Round-14: a cap-reached BudgetExceeded must propagate
                # to the cycle driver so cli.py collect can exit 2.
                # Previously this was caught and converted to a
                # ``readability_budget_blocked`` label, which let the
                # command return success mid-cap (AC-14 violation).
                if tracker is not None:
                    tracker.check()
                distilled = _distill_with_gemini(title=title, body=body, domain=domain)
                if tracker is not None and distilled is not None:
                    try:
                        tracker.increment_gemini()
                    except Exception:  # noqa: BLE001
                        pass
                if distilled:
                    from core.skill_wiki.llm_client import model_backend
                    distillation_used = model_backend()  # "gemini" / "none"
                else:
                    distillation_used = "readability"

            applicability = (distilled or {}).get("applicability") or ""
            tags = (distilled or {}).get("tags") or []
            distilled_summary = (distilled or {}).get("summary") or ""
            text_overview = body
            if distilled_summary:
                text_overview = (
                    f"# {title}\n\n## Summary ({distillation_used} distilled)\n\n"
                    f"{distilled_summary}\n\n## Applicability\n\n"
                    f"{applicability}\n\n## Original body\n\n{body[:1500]}"
                )

            out.append(CandidateSkill(
                skill_id=slug,
                skill_name=(distilled or {}).get("title") or title,
                domain=domain,
                source_type=self.SOURCE_TYPE,
                source_url=url,
                source_channel="article",
                license=license_value,
                text_overview=text_overview,
                applicability=applicability or None,
                tags=tags if isinstance(tags, list) else [],
                extras={
                    "distilled": bool(distilled),
                    "distillation_used": distillation_used,
                },
            ))
        return out


def _extract_title_body(html: str) -> tuple[str, str]:
    try:
        from readability import Document  # type: ignore[import-untyped]
    except ImportError:
        return "", html[:1500]
    try:
        doc = Document(html)
        return doc.short_title() or "", doc.summary() or ""
    except Exception:  # noqa: BLE001
        return "", ""


def _distill_with_gemini(*, title: str, body: str, domain: str) -> dict[str, Any] | None:
    """Call the active model backend (Gemini-first, Azure-fallback) to
    extract structured metadata from an article body.

    Round-12: routes through ``core.skill_wiki.llm_client.call_model_json``
    so the connector follows the plan's Gemini-first contract while
    transparently falling back to Azure gpt-5.4. Returns a dict with
    keys ``title``, ``applicability``, ``tags``, ``summary`` on
    success, or ``None`` on any failure.
    """
    prompt = (
        f"You are extracting a candidate skill from a public article for the "
        f"{domain!r} skill wiki. Read the article and emit a JSON object with "
        f"keys: title (string), applicability (1-2 sentence description of "
        f"when this skill helps), tags (list of 3-6 short keywords), summary "
        f"(<=200 char paraphrase). Output JSON only.\n\n"
        f"Article title: {title}\n\nArticle body (truncated):\n{body[:6000]}"
    )
    from core.skill_wiki.llm_client import call_model_json
    return call_model_json(prompt=prompt)


def _derive_license(html: str) -> str | None:
    """Extract license information from common HTML signals."""
    if not html:
        return None
    text = html.lower()
    # <link rel="license" href="...">
    link_match = re.search(r"<link[^>]+rel=[\"']license[\"'][^>]*href=[\"']([^\"']+)[\"']", text)
    if link_match:
        href = link_match.group(1)
        for substring, label in _PERMISSIVE_LICENSE_SUBSTRINGS:
            if substring in href:
                return label
        return "blocked"
    # <meta name="license" content="..."> or property="og:license"
    meta_match = re.search(
        r"<meta[^>]+(?:name|property)=[\"'](?:og:)?license[\"'][^>]*content=[\"']([^\"']+)[\"']",
        text,
    )
    if meta_match:
        content = meta_match.group(1)
        for substring, label in _PERMISSIVE_LICENSE_SUBSTRINGS:
            if substring in content:
                return label
        if "creativecommons" in content or "permissive" in content:
            return "cc-by-4.0"
        return "blocked"
    return None


def _slug_from_url(url: str) -> str:
    import hashlib
    suffix = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    base = url.split("//", 1)[-1].split("/", 1)[0].replace(".", "_")
    return f"art_{base}_{suffix}".lower().replace("-", "_")


__all__ = ["ArticleConnector"]

