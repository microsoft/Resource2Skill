"""Hard budget caps: read from config before any model-backed run, refuse on
missing values, write a structured ``cap_reached.json`` on hit, surface via
``cli.py budget-status``.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_CONFIG_PATH = Path(__file__).parent / "config.json"

REQUIRED_KEYS: tuple[str, ...] = (
    "gemini_call_cap_per_run",
    "gemini_call_cap_per_domain_per_day",
    "wall_clock_cap_minutes_per_run",
)


class MissingBudgetConfig(Exception):
    """Raised when a required cap is absent or null in config.json."""


class BudgetExceeded(Exception):
    """Raised when a cap is hit mid-run; carries a cap_reached payload."""

    def __init__(self, payload: dict[str, Any]) -> None:
        super().__init__(payload.get("reason", "budget exceeded"))
        self.payload = payload


@dataclass
class BudgetCap:
    gemini_call_cap_per_run: int
    gemini_call_cap_per_domain_per_day: int
    wall_clock_cap_minutes_per_run: int


def load_budget_caps(config_path: Path | str = _CONFIG_PATH) -> BudgetCap:
    payload = json.loads(Path(config_path).read_text(encoding="utf-8"))
    missing: list[str] = []
    values: dict[str, Any] = {}
    for key in REQUIRED_KEYS:
        if key not in payload or payload[key] in (None, "", 0):
            missing.append(key)
        else:
            values[key] = payload[key]
    if missing:
        raise MissingBudgetConfig(
            "missing_required_config: " + ", ".join(missing)
        )
    return BudgetCap(**{k: int(values[k]) for k in REQUIRED_KEYS})


class BudgetTracker:
    """Per-run budget meter. Caller increments after every Gemini call.

    Once a cap is hit, ``check()`` raises ``BudgetExceeded`` with a payload
    enumerating remaining work supplied by the caller via ``register_pending``.
    """

    def __init__(
        self,
        *,
        cap: BudgetCap,
        domain: str,
        run_id: str,
        cap_reached_path: Path | str,
        daily_usage_loader: "callable[[str], int] | None" = None,
    ) -> None:
        self.cap = cap
        self.domain = domain
        self.run_id = run_id
        self.cap_reached_path = Path(cap_reached_path)
        self.gemini_calls_this_run = 0
        self.daily_usage_loader = daily_usage_loader
        self.start_ts = time.time()
        self._pending: list[dict[str, Any]] = []
        self._completed: list[str] = []

    def register_pending(self, work: list[dict[str, Any]]) -> None:
        """Caller declares the planned unit-of-work list at start."""
        self._pending = list(work)

    def mark_completed(self, work_id: str) -> None:
        if work_id in self._pending_ids():
            self._pending = [w for w in self._pending if w.get("id") != work_id]
            self._completed.append(work_id)

    def _pending_ids(self) -> list[str]:
        return [w.get("id", "") for w in self._pending]

    def increment_gemini(self, n: int = 1) -> None:
        self.gemini_calls_this_run += n

    def remaining_minutes(self) -> float:
        elapsed_minutes = (time.time() - self.start_ts) / 60.0
        return max(self.cap.wall_clock_cap_minutes_per_run - elapsed_minutes, 0.0)

    def check(self) -> None:
        if self.gemini_calls_this_run >= self.cap.gemini_call_cap_per_run:
            self._raise("gemini_call_cap_per_run")
        if self.daily_usage_loader is not None:
            daily = int(self.daily_usage_loader(self.domain))
            if daily + self.gemini_calls_this_run >= self.cap.gemini_call_cap_per_domain_per_day:
                self._raise("gemini_call_cap_per_domain_per_day")
        if self.remaining_minutes() <= 0.0:
            self._raise("wall_clock_cap_minutes_per_run")

    def _raise(self, reason: str) -> None:
        payload = {
            "reason": reason,
            "domain": self.domain,
            "run_id": self.run_id,
            "gemini_calls_this_run": self.gemini_calls_this_run,
            "elapsed_minutes": (time.time() - self.start_ts) / 60.0,
            "completed": list(self._completed),
            "remaining": list(self._pending),
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        self.cap_reached_path.parent.mkdir(parents=True, exist_ok=True)
        self.cap_reached_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
        raise BudgetExceeded(payload)
