import sys
from pathlib import Path

# 让后端能 import 同一仓库的 core.*（distill / agent 在后续切片使用）
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import httpx

from . import config_store, projects, fixtures, tasks, distill, agent, repo
from .models import LLMTemplate, ProjectCreate, DomainCreate, DistillRequest, AgentRunRequest

app = FastAPI(title="Resource2Skill WebUI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/config")
def get_config():
    # 合并自 B 工作副本：让前端首页 Overview 读取全局激活上下文，无需客户端重算。
    cfg = config_store.load()
    tpl = None
    if cfg.active_llm and cfg.active_llm in cfg.templates:
        tpl = config_store.public_template(cfg.active_llm, cfg.templates[cfg.active_llm], cfg.active_llm)
    return {
        "active_project": cfg.active_project,
        "active_domain": cfg.active_domain,
        "active_llm": cfg.active_llm,
        "active_llm_template": tpl,
    }


@app.get("/api/llm")
def list_llm():
    cfg = config_store.load()
    templates = [
        config_store.public_template(name, t, cfg.active_llm)
        for name, t in cfg.templates.items()
    ]
    return {"active": cfg.active_llm, "templates": templates}


@app.post("/api/llm")
def upsert_llm(t: LLMTemplate):
    cfg = config_store.load()
    cfg.templates[t.name] = t
    config_store.save(cfg)
    return {"ok": True, "name": t.name}


@app.delete("/api/llm/{name}")
def delete_llm(name: str):
    cfg = config_store.load()
    if name in cfg.templates:
        del cfg.templates[name]
    if cfg.active_llm == name:
        cfg.active_llm = ""
    config_store.save(cfg)
    return {"ok": True}


@app.post("/api/llm/{name}/active")
def set_active(name: str):
    cfg = config_store.load()
    if name not in cfg.templates:
        raise HTTPException(404, "template not found")
    cfg.active_llm = name
    config_store.save(cfg)
    return {"ok": True, "active": name}


# ----------------------------- 项目 / 领域（切片1） -----------------------------

@app.get("/api/repo-domains")
def get_repo_domains():
    from core import list_domains as core_list_domains

    return {"domains": core_list_domains()}


@app.get("/api/projects")
def get_projects():
    return {"active": config_store.load().active_project, "projects": projects.list_projects()}


@app.post("/api/projects")
def post_project(body: ProjectCreate):
    try:
        meta = projects.create_project(body.name, body.description)
    except (ValueError, FileExistsError) as e:
        raise HTTPException(400, str(e))
    return {"ok": True, **meta}


@app.delete("/api/projects/{name}")
def del_project(name: str):
    try:
        projects.delete_project(name)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    return {"ok": True}


@app.post("/api/projects/{name}/active")
def activate_project(name: str):
    try:
        projects.set_active_project(name)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    return {"ok": True, "active": name}


@app.get("/api/projects/{name}/domains")
def get_domains(name: str):
    if not (projects.project_dir(name)).exists():
        raise HTTPException(404, f"项目不存在：{name}")
    cfg = config_store.load()
    # active_domain 是全局单值，但 set_active_domain 会同步写 active_project，
    # 故仅当请求的项目正是激活项目时才返回，避免串域。
    ad = cfg.active_domain if cfg.active_project == name else None
    return {"project": name, "domains": projects.list_domains(name), "active_domain": ad}


@app.post("/api/projects/{name}/domains")
def post_domain(name: str, body: DomainCreate):
    try:
        res = projects.create_domain(name, body.domain, body.seed_from)
    except (ValueError, FileExistsError, FileNotFoundError) as e:
        raise HTTPException(400, str(e))
    return {"ok": True, **res}


@app.post("/api/projects/{name}/domains/{domain}/active")
def activate_domain(name: str, domain: str):
    try:
        projects.set_active_domain(name, domain)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    return {"ok": True, "active_project": name, "active_domain": domain}


@app.post("/api/projects/{name}/domains/{domain}/validate")
def validate_project_domain(name: str, domain: str):
    try:
        res = projects.validate_domain(name, domain)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    return res


# ----------------------------- 素材管理（切片2） -----------------------------

@app.get("/api/projects/{name}/domains/{domain}/fixtures")
def get_fixtures(name: str, domain: str):
    if not (projects.project_dir(name) / "domains" / domain / "domain.yaml").exists():
        raise HTTPException(404, f"领域不存在：{domain}")
    return {"project": name, "domain": domain, "fixtures": fixtures.list_fixtures(name, domain)}


@app.post("/api/projects/{name}/domains/{domain}/fixtures")
async def upload_fixture(name: str, domain: str, file: UploadFile = File(...)):
    if not (projects.project_dir(name) / "domains" / domain / "domain.yaml").exists():
        raise HTTPException(404, f"领域不存在：{domain}")
    try:
        content = await file.read()
        meta = fixtures.save_fixture(name, domain, file.filename or "unnamed", content)
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(400, str(e))
    return {"ok": True, **meta}


@app.post("/api/projects/{name}/domains/{domain}/fixtures/{filename}/enable")
def enable_fixture(name: str, domain: str, filename: str, body: dict):
    try:
        res = fixtures.set_enabled(name, domain, filename, bool(body.get("enabled", True)))
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    return {"ok": True, **res}


@app.delete("/api/projects/{name}/domains/{domain}/fixtures/{filename}")
def del_fixture(name: str, domain: str, filename: str):
    try:
        fixtures.delete_fixture(name, domain, filename)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    return {"ok": True}


@app.get("/api/projects/{name}/domains/{domain}/fixtures/{filename}/preview")
def preview_fixture(name: str, domain: str, filename: str):
    try:
        return fixtures.preview_text(name, domain, filename)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))


# ----------------------------- 蒸馏工作台 + 任务中心（切片3） -----------------------------

@app.post("/api/projects/{name}/domains/{domain}/distill")
def post_distill(name: str, domain: str, body: DistillRequest):
    if not (projects.project_dir(name) / "domains" / domain / "domain.yaml").exists():
        raise HTTPException(404, f"领域不存在：{domain}")
    task = tasks.submit(
        type="distill",
        project=name,
        domain=domain,
        label=f"蒸馏 {name}/{domain}" + ("（dry-run）" if body.dry_run else ""),
        runner=lambda t: distill.run_distill_task(t, name, domain, body.dry_run),
    )
    return {"ok": True, "task_id": task.id}


@app.get("/api/tasks")
def get_tasks():
    return {"tasks": tasks.list_all()}


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    t = tasks.get(task_id)
    if not t:
        raise HTTPException(404, "task not found")
    return tasks.public_view(t)


@app.post("/api/tasks/{task_id}/stop")
def stop_task(task_id: str):
    if not tasks.stop(task_id):
        raise HTTPException(404, "task not found")
    return {"ok": True}


@app.post("/api/llm/test")
async def test_llm(t: LLMTemplate):
    if not t.endpoint or not t.api_key or not t.model:
        return {"ok": False, "message": "endpoint / api_key / model 均为必填"}
    url = t.endpoint.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {t.api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": t.model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5,
    }
    kwargs = {"timeout": t.timeout}
    if t.proxy:
        kwargs["proxy"] = t.proxy
    try:
        async with httpx.AsyncClient(**kwargs) as c:
            r = await c.post(url, headers=headers, json=body)
        ok = r.status_code == 200
        detail = "" if ok else r.text[:300]
        return {"ok": ok, "status": r.status_code, "message": detail}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "message": f"{type(e).__name__}: {e}"}


# ----------------------------- Agent 执行台（切片4） -----------------------------

@app.post("/api/projects/{name}/agent/run")
def post_agent_run(name: str, body: AgentRunRequest):
    if not (projects.project_dir(name) / "domains" / body.domain / "domain.yaml").exists():
        raise HTTPException(404, f"领域不存在：{body.domain}")
    task = tasks.submit(
        type="agent",
        project=name,
        domain=body.domain,
        label=f"Agent {name}/{body.domain}" + ("（dry-run）" if body.dry_run else ""),
        runner=lambda t: agent.run_agent_task(
            t, name, body.domain,
            task_text=body.task,
            model=body.model,
            reasoning=body.reasoning,
            max_iter=body.max_iter,
            n_skills=body.n_skills,
            top_k=body.top_k,
            dry_run=body.dry_run,
        ),
    )
    return {"ok": True, "task_id": task.id}


# ----------------------------- 产物仓库（切片4） -----------------------------

@app.get("/api/projects/{name}/repo")
def get_repo(name: str, domain: str):
    return repo.list_repo(name, domain)


@app.get("/api/projects/{name}/repo/file")
def get_repo_file(name: str, kind: str, domain: str = "", rel_path: str = ""):
    return repo.serve_repo_file(name, kind, domain, rel_path)
