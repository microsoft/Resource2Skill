"""GitHub source connector.

Pulls candidate skills from GitHub via search + raw-file fetch. Each
candidate carries the repo's licence label (best-effort, derived from
the repo metadata; ``None`` when the API call fails or the repo has no
SPDX licence). The wash pipeline then quarantines ``None`` and
``"blocked"`` entries.

When a per-domain file extension allow-list is provided, the connector
also fetches up to ``files_per_repo`` source files from the default
branch and emits one CandidateSkill per file. This gives the wash
pipeline file-grained inputs instead of one repo-level row per repo
(see Round-10 / task10).
"""
from __future__ import annotations

import os
from typing import Any

from .base import CandidateSkill, SourceConnector


# Default per-domain file-extension allow-list. Used when the caller does
# not supply ``file_extensions``. Keep narrow + permissive to favour
# code/markup that the domain wash can do something with.
_DOMAIN_FILE_EXTENSIONS: dict[str, tuple[str, ...]] = {
    "web": (".html", ".css", ".js", ".jsx", ".ts", ".tsx"),
    "excel": (".py",),  # openpyxl scripts only
    "ppt": (".py",),    # python-pptx scripts only
    "blender": (".py",),
    "reaper": (".py",),
}


class GitHubConnector(SourceConnector):
    SOURCE_TYPE = "github"

    def __init__(
        self,
        *,
        token: str | None = None,
        query_template: str | None = None,
        permissive_licences: tuple[str, ...] = (
            "mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "isc", "cc0-1.0", "0bsd",
        ),
        files_per_repo: int = 0,
        file_extensions: tuple[str, ...] | None = None,
    ) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.query_template = query_template or "{domain} skill"
        self.permissive_licences = {l.lower() for l in permissive_licences}
        # Round-10: when files_per_repo > 0, emit one candidate per source
        # file in addition to (or instead of) the repo-level row.
        self.files_per_repo = max(0, int(files_per_repo))
        self.file_extensions = file_extensions

    def acquire(self, *, domain: str, quota: int, **kwargs: Any) -> list[CandidateSkill]:
        if quota <= 0 or not self.token:
            return []
        try:
            import requests  # type: ignore[import-untyped]
        except ImportError:
            return []
        query = (kwargs.get("query") or self.query_template).format(domain=domain)
        try:
            resp = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": query, "per_page": min(quota, 25)},
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                timeout=10,
            )
            if resp.status_code != 200:
                return []
            payload = resp.json()
        except Exception:  # noqa: BLE001
            return []
        out: list[CandidateSkill] = []
        files_per_repo = int(kwargs.get("files_per_repo", self.files_per_repo) or 0)
        extensions = tuple(
            ext.lower() for ext in (
                kwargs.get("file_extensions")
                or self.file_extensions
                or _DOMAIN_FILE_EXTENSIONS.get(domain, (".py",))
            )
        )
        for repo in payload.get("items", []):
            license_obj = repo.get("license") or {}
            license_key = (license_obj.get("spdx_id") or license_obj.get("key") or "").lower()
            if license_key in self.permissive_licences:
                license_value: str | None = license_key
            elif license_key:
                license_value = "blocked"
            else:
                license_value = None
            full_name = repo.get("full_name") or repo.get("name") or "unknown"
            skill_id = full_name.replace("/", "_").replace("-", "_").lower()
            readme_text = self._fetch_readme(full_name) if license_value not in {"blocked"} else ""
            out.append(CandidateSkill(
                skill_id=skill_id,
                skill_name=str(repo.get("name") or full_name),
                domain=domain,
                source_type=self.SOURCE_TYPE,
                source_url=str(repo.get("html_url") or ""),
                source_channel="github",
                license=license_value,
                text_overview=str(repo.get("description") or "") + (
                    "\n\n## README\n\n" + readme_text if readme_text else ""
                ),
                extras={
                    "stars": repo.get("stargazers_count"),
                    "topics": repo.get("topics") or [],
                    "default_branch": repo.get("default_branch"),
                    "scope": "repo",
                },
            ))
            if len(out) >= quota:
                break
            # File-level extraction: emit one candidate per relevant source
            # file from the default branch, up to files_per_repo.
            if files_per_repo > 0 and license_value not in {"blocked", None}:
                file_candidates = self._fetch_files(
                    full_name=full_name,
                    domain=domain,
                    repo_html_url=str(repo.get("html_url") or ""),
                    repo_skill_id=skill_id,
                    license_value=license_value,
                    extensions=extensions,
                    limit=files_per_repo,
                    default_branch=str(repo.get("default_branch") or "main"),
                )
                for cand in file_candidates:
                    out.append(cand)
                    if len(out) >= quota:
                        break
            if len(out) >= quota:
                break
        return out[:quota]

    def _fetch_readme(self, full_name: str, *, max_chars: int = 8192) -> str:
        try:
            import requests  # type: ignore[import-untyped]
        except ImportError:
            return ""
        try:
            resp = requests.get(
                f"https://api.github.com/repos/{full_name}/readme",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github.raw",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                timeout=10,
            )
            if resp.status_code != 200:
                return ""
            return resp.text[:max_chars]
        except Exception:  # noqa: BLE001
            return ""

    def _fetch_files(
        self, *, full_name: str, domain: str, repo_html_url: str, repo_skill_id: str,
        license_value: str | None, extensions: tuple[str, ...], limit: int,
        default_branch: str = "main", max_chars: int = 12000,
    ) -> list[CandidateSkill]:
        """Fetch up to ``limit`` source files from the repo and emit one
        ``CandidateSkill`` per file. Uses the git-trees recursive API
        once + raw-content fetch per selected path.
        """
        try:
            import requests  # type: ignore[import-untyped]
        except ImportError:
            return []
        try:
            tree_resp = requests.get(
                f"https://api.github.com/repos/{full_name}/git/trees/{default_branch}",
                params={"recursive": "1"},
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                timeout=10,
            )
            if tree_resp.status_code != 200:
                return []
            tree = tree_resp.json()
        except Exception:  # noqa: BLE001
            return []
        entries = tree.get("tree", []) if isinstance(tree, dict) else []
        # Filter to blob-type entries that match our extension allow-list.
        selected: list[dict[str, Any]] = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("type") != "blob":
                continue
            path = str(entry.get("path") or "")
            if not any(path.lower().endswith(ext) for ext in extensions):
                continue
            # Skip clearly-uninteresting paths.
            lower = path.lower()
            if any(skip in lower for skip in ("test/", "tests/", "/__pycache__/", ".min.")):
                continue
            selected.append(entry)
            if len(selected) >= limit:
                break
        out: list[CandidateSkill] = []
        for entry in selected:
            path = str(entry.get("path") or "")
            try:
                raw = requests.get(
                    f"https://raw.githubusercontent.com/{full_name}/{default_branch}/{path}",
                    timeout=10,
                )
                if raw.status_code != 200:
                    continue
                content = raw.text[:max_chars]
            except Exception:  # noqa: BLE001
                continue
            file_slug = path.replace("/", "_").replace(".", "_").replace("-", "_").lower()
            file_skill_id = f"{repo_skill_id}__{file_slug}"
            out.append(CandidateSkill(
                skill_id=file_skill_id,
                skill_name=path,
                domain=domain,
                source_type=self.SOURCE_TYPE,
                source_url=f"{repo_html_url}/blob/{default_branch}/{path}",
                source_channel="github",
                license=license_value,
                text_overview=f"# {path}\n\nFile-level extraction from {full_name}.\n\n```\n{content[:2048]}\n```",
                extras={
                    "scope": "file",
                    "repo": full_name,
                    "path": path,
                    "default_branch": default_branch,
                    "raw_content": content,
                },
            ))
        return out


__all__ = ["GitHubConnector"]
