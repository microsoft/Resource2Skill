"""Project / Domain 管理（切片1）。

设计原则（多项目隔离，零 core 重构）：
- 引擎代码保持单实例（Resource2Skill 仓库）。
- “项目” = webui/projects/<name>/ 下的独立数据目录：
      domains/<domain>/         领域配置（domain.yaml + 引用文件）
      skills_library/<domain>/  蒸馏产物（后续切片使用）
      fixtures/<domain>/        素材（后续切片使用）
      output/                   产物仓库（后续切片使用）
      project.json              项目元数据
- 校验直接调用 core.validate_domain(name, domains_dir=项目domains目录)，
  利用它已支持的 domains_dir 覆盖参数，无需改动 core。
- 已有同名仓库领域（如 ppt）可“播种”进项目，保证 validate 直接 PASS 且为真实可用领域。
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

import yaml

from . import config_store

# webui/backend -> webui -> Resource2Skill
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REPO_DOMAINS = REPO_ROOT / "domains"

_SAFE_NAME = lambda s: "".join(c for c in s if c.isalnum() or c in "-_")


def projects_root() -> Path:
    cfg = config_store.load()
    if cfg.projects_root:
        return Path(cfg.projects_root)
    return Path(__file__).resolve().parent.parent / "projects"


def project_dir(name: str) -> Path:
    return projects_root() / name


# ----------------------------- 项目 -----------------------------

def list_projects() -> list[dict]:
    root = projects_root()
    if not root.exists():
        return []
    cfg = config_store.load()
    out = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name == ".trash":
            continue
        pj = d / "project.json"
        meta = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
        dom_dir = d / "domains"
        domains = sorted(
            x.name for x in dom_dir.iterdir()
            if x.is_dir() and (x / "domain.yaml").exists()
        ) if dom_dir.exists() else []
        out.append({
            "name": d.name,
            "description": meta.get("description", ""),
            "created_at": meta.get("created_at", ""),
            "is_active": d.name == cfg.active_project,
            "domains": domains,
        })
    return out


def create_project(name: str, description: str = "") -> dict:
    name = _SAFE_NAME(name.strip())
    if not name:
        raise ValueError("项目名称非法（仅允许字母/数字/-/_）")
    root = projects_root()
    root.mkdir(parents=True, exist_ok=True)
    pdir = root / name
    if pdir.exists():
        raise FileExistsError(f"项目已存在：{name}")
    pdir.mkdir(parents=True)
    for sub in ("domains", "skills_library", "fixtures", "output"):
        (pdir / sub).mkdir()
    meta = {
        "name": name,
        "description": description,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    (pdir / "project.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # 首个项目自动激活
    cfg = config_store.load()
    if not cfg.active_project:
        cfg.active_project = name
        config_store.save(cfg)
    return meta


def delete_project(name: str) -> None:
    pdir = project_dir(name)
    if not pdir.exists():
        raise FileNotFoundError(f"项目不存在：{name}")
    # 沙箱禁止 shutil.rmtree 硬删除 -> 软删除：移动到 .trash（可恢复，且不计入列表）
    trash_root = projects_root() / ".trash"
    trash_root.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    dest = trash_root / f"{name}_{ts}"
    i = 1
    while dest.exists():
        dest = trash_root / f"{name}_{ts}_{i}"
        i += 1
    shutil.move(str(pdir), str(dest))
    cfg = config_store.load()
    if cfg.active_project == name:
        cfg.active_project = ""


def set_active_project(name: str) -> None:
    pdir = project_dir(name)
    if not pdir.exists():
        raise FileNotFoundError(f"项目不存在：{name}")
    cfg = config_store.load()
    cfg.active_project = name
    config_store.save(cfg)


# ----------------------------- 领域 -----------------------------

def list_domains(project: str) -> list[str]:
    ddir = project_dir(project) / "domains"
    if not ddir.exists():
        return []
    return sorted(
        x.name for x in ddir.iterdir()
        if x.is_dir() and (x / "domain.yaml").exists()
    )


def create_domain(project: str, domain: str, seed_from: str | None = None) -> dict:
    domain = _SAFE_NAME(domain.strip())
    if not domain:
        raise ValueError("领域名称非法（仅允许字母/数字/-/_）")
    pdir = project_dir(project)
    if not pdir.exists():
        raise FileNotFoundError(f"项目不存在：{project}")
    ddir = pdir / "domains"
    ddir.mkdir(parents=True, exist_ok=True)
    target = ddir / domain
    if target.exists():
        raise FileExistsError(f"领域已存在：{domain}")

    src = REPO_DOMAINS / (seed_from or domain)
    seeded = False
    if src.exists():
        shutil.copytree(src, target)
        # 播种时把 mcp.cwd 改写为项目根，并向 mcp.env 注入项目隔离路径（领域无关）。
        # 这样 MCP 子进程（cwd=项目根、args 相对解析到本项目 mcp_server）会把技能库与
        # 产物落到本项目数据目录，且产物位于 output/<domain>_workspace 下，便于产物仓库浏览与隔离。
        _rewrite_mcp_for_project(target / "domain.yaml", pdir, domain)
        seeded = True
    else:
        _write_blank_domain(target, domain)

    # 配套目录
    (pdir / "skills_library" / domain).mkdir(parents=True, exist_ok=True)
    (pdir / "fixtures" / domain).mkdir(parents=True, exist_ok=True)
    return {"domain": domain, "seeded": seeded}


def _rewrite_mcp_for_project(yaml_path: Path, project_dir: Path, domain: str) -> None:
    """播种领域时：把 mcp.cwd 改写为项目根，并向 mcp.args/mcp.env 注入项目隔离路径。

    对所有带 mcp 块（command/args）的领域通用，不再特殊对待任何领域：
    - mcp.env 注入 R2S_DOMAIN / R2S_SKILLS_DIR / R2S_WORKSPACE（MCP 子进程兜底读取）；
    - mcp.args 追加 --workspace / --skills-dir（主通道，server.py 解析后落本项目目录）。
    这样 MCP 子进程（cwd=项目根、args 相对解析到本项目 mcp_server）会把技能库与产物
    落到本项目数据目录，且产物位于 output/<domain>_workspace，便于产物仓库浏览与隔离。
    """
    if not yaml_path.exists():
        return
    try:
        cfg = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        mcp = cfg.get("mcp")
        if isinstance(mcp, dict) and mcp.get("command"):
            mcp["cwd"] = str(project_dir)
            skills_dir = (project_dir / "skills_library" / domain).resolve()
            workspace = (project_dir / "output" / f"{domain}_workspace").resolve()
            # 主通道：命令行参数（可靠透传）
            raw_args = list(mcp.get("args") or [])
            clean = []
            skip = False
            for a in raw_args:
                if skip:
                    skip = False
                    continue
                if a in ("--workspace", "--skills-dir"):
                    skip = True
                    continue
                clean.append(a)
            # args[0] 保持领域自带的 server.py 相对路径（cwd=项目根，由本项目 seed 副本承载，
            # 单一事实来源 = 本项目的 domains/<domain>/mcp_server/server.py），不再强指仓库根。
            clean += ["--workspace", str(workspace), "--skills-dir", str(skills_dir)]
            mcp["args"] = clean
            # 兜底环境变量（MCP 子进程继承）
            env = dict(mcp.get("env") or {})
            env["R2S_DOMAIN"] = domain
            env["R2S_SKILLS_DIR"] = str(skills_dir)
            env["R2S_WORKSPACE"] = str(workspace)
            mcp["env"] = env
            yaml_path.write_text(
                yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
    except Exception:  # noqa: BLE001
        pass


def _write_blank_domain(target: Path, domain: str) -> None:
    """生成“空白领域脚手架”。

    采用 legacy 形态（不声明 execution_mode），这样 validate_domain 直接 PASS，
    mcp 允许为 null。待用户配置 execution_mode / persona / query_pool /
    failure_patterns / tools_fallback_file / mcp 后即可用于新 Agent 循环。
    """
    target.mkdir(parents=True, exist_ok=True)
    cfg = {
        "name": domain,
        "display_name": domain,
        # 不声明 execution_mode -> legacy 形态，validate 直接通过
        "categories": {"general": [domain]},
        "mcp": None,
        "agent_prompt_file": "agent_prompt.md",
    }
    (target / "domain.yaml").write_text(
        yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    (target / "agent_prompt.md").write_text(
        f"# Agent Prompt — {domain}\n\n（空白领域脚手架，请按需补充任务引导。）\n",
        encoding="utf-8",
    )
    (target / "tools_fallback.json").write_text("[]", encoding="utf-8")
    (target / "distiller_prompt.md").write_text(
        f"# Distiller Prompt — {domain}\n\n从素材中抽取可复用技能。\n",
        encoding="utf-8",
    )


def set_active_domain(project: str, domain: str) -> None:
    pdir = project_dir(project)
    if not (pdir / "domains" / domain / "domain.yaml").exists():
        raise FileNotFoundError(f"领域不存在：{domain}")
    cfg = config_store.load()
    cfg.active_project = project
    cfg.active_domain = domain
    config_store.save(cfg)


def validate_domain(project: str, domain: str) -> dict:
    from core import validate_domain as core_validate

    pdir = project_dir(project)
    ddir = pdir / "domains"
    if not (ddir / domain / "domain.yaml").exists():
        raise FileNotFoundError(f"领域不存在：{domain}")
    errors = core_validate(domain, domains_dir=ddir)
    return {"domain": domain, "valid": len(errors) == 0, "errors": errors}
