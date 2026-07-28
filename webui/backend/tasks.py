"""后台任务注册表（切片3 起，蒸馏 / Agent 共用）。

设计要点：
- 单 worker 线程串行执行任务。原因：蒸馏时需在进程内环境注入用户 LLM 配置
  （call_azure_openai 从环境变量读取 endpoint/key），串行可避免并发任务互相踩 env。
- 每个 Task 自带 log 缓冲（封顶长度）与 stop_requested 标志，runner 应通过
  task.should_stop() 周期性检查以支持「终止」。
- 内存态（localhost 单人用，重启即丢），不做持久化。
"""
from __future__ import annotations

import queue
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional

_LOG_CAP = 3000

_TASKS: dict[str, "Task"] = {}
_Q: "queue.Queue[Optional[Task]]" = queue.Queue()
_WORKER: Optional[threading.Thread] = None
_LOCK = threading.Lock()


def _iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class Task:
    id: str
    type: str
    project: str
    domain: str
    status: str = "queued"          # queued | running | done | error | stopped
    label: str = ""
    created_at: str = ""
    started_at: str = ""
    finished_at: str = ""
    summary: dict = field(default_factory=dict)
    stop_requested: bool = False
    log: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)   # 任务提交参数，供「复制参数重跑」复用
    _runner: Callable[["Task"], None] = lambda t: None

    def append_log(self, line: str) -> None:
        self.log.append(line)
        if len(self.log) > _LOG_CAP:
            del self.log[: len(self.log) - _LOG_CAP]

    def should_stop(self) -> bool:
        return self.stop_requested


def _ensure_worker() -> None:
    global _WORKER
    if _WORKER is None or not _WORKER.is_alive():
        _WORKER = threading.Thread(target=_worker, daemon=True)
        _WORKER.start()


def _worker() -> None:
    while True:
        task = _Q.get()
        if task is None:
            _Q.task_done()
            break
        task.status = "running"
        task.started_at = _iso()
        try:
            task._runner(task)
        except Exception as e:  # noqa: BLE001
            task.append_log(f"[异常] {type(e).__name__}: {e}")
            task.status = "error"
        else:
            task.status = "stopped" if task.stop_requested else "done"
        task.finished_at = _iso()
        _Q.task_done()


def submit(*, type: str, project: str, domain: str, runner: Callable[["Task"], None],
           label: str = "", params: dict | None = None) -> Task:
    tid = uuid.uuid4().hex[:8]
    t = Task(id=tid, type=type, project=project, domain=domain,
             label=label, created_at=_iso(), params=params or {})
    t._runner = runner
    with _LOCK:
        _TASKS[tid] = t
    _ensure_worker()
    _Q.put(t)
    return t


def get(task_id: str) -> Optional[Task]:
    return _TASKS.get(task_id)


def list_all() -> list[dict]:
    with _LOCK:
        items = list(_TASKS.values())
    items.sort(key=lambda t: t.created_at, reverse=True)
    return [
        {
            "id": t.id, "type": t.type, "project": t.project, "domain": t.domain,
            "status": t.status, "label": t.label, "created_at": t.created_at,
            "started_at": t.started_at, "finished_at": t.finished_at,
            "summary": t.summary, "extra": t.extra, "params": t.params,
        }
        for t in items
    ]


def stop(task_id: str) -> bool:
    t = _TASKS.get(task_id)
    if not t:
        return False
    t.stop_requested = True
    # queued 任务被 worker 取走后，runner 会在开头检查 should_stop 直接退出
    return True


def public_view(t: Task) -> dict:
    return {
        "id": t.id, "type": t.type, "project": t.project, "domain": t.domain,
        "status": t.status, "label": t.label, "created_at": t.created_at,
        "started_at": t.started_at, "finished_at": t.finished_at,
        "summary": t.summary, "log": t.log, "extra": t.extra, "params": t.params,
    }
