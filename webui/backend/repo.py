"""产物仓库（切片4）。

浏览项目数据目录：
- 技能库：projects/<project>/skills_library/<domain>/（R2S 蒸馏产物，含 skill.json）
- 产物：  projects/<project>/output/<domain>_workspace/（agent 交付物落点，领域无关）

提供：列举（技能 + 文件树）+ 安全下载/预览（防目录穿越）。
"""
from __future__ import annotations

import mimetypes
import os
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse

from . import projects

_TEXT_EXT = {".md", ".txt", ".json", ".csv", ".py", ".yaml", ".yml", ".html", ".htm",
             ".xml", ".log", ".toml", ".ini", ".cfg"}
_IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}


def _safe_join(base: Path, rel: str) -> Path:
    """将相对路径安全拼接到 base 之下，禁止目录穿越。"""
    if not rel:
        raise HTTPException(400, "路径为空")
    rel = rel.replace("\\", "/").strip("/")
    if ".." in rel.split("/"):
        raise HTTPException(400, "非法路径（含 ..）")
    target = (base / rel).resolve()
    base_res = base.resolve()
    if target != base_res and base_res not in target.parents:
        raise HTTPException(400, "非法路径（越界）")
    if not target.exists():
        raise HTTPException(404, "文件不存在")
    if target.is_dir():
        raise HTTPException(400, "目标是目录，不是文件")
    return target


def _file_info(rel_path: str, base: Path) -> dict:
    p = (base / rel_path).resolve()
    try:
        st = p.stat()
        mtime = st.st_mtime
        size = st.st_size
    except OSError:
        mtime = 0
        size = 0
    ext = p.suffix.lower()
    return {
        "rel_path": rel_path,
        "name": p.name,
        "ext": ext.lstrip("."),
        "size": size,
        "mtime": mtime,
        "kind": "image" if ext in _IMAGE_EXT else ("text" if ext in _TEXT_EXT else "binary"),
    }


def list_repo(project: str, domain: str) -> dict:
    """列举项目的技能库与产物目录。"""
    pdir = projects.project_dir(project)
    if not pdir.exists():
        raise HTTPException(404, f"项目不存在：{project}")

    skills_dir = pdir / "skills_library" / domain
    output_dir = pdir / "output"

    skills: list[dict] = []
    files: list[dict] = []
    if skills_dir.exists():
        for skill_json in sorted(skills_dir.rglob("skill.json")):
            if ".trash" in skill_json.parts:
                continue
            rel = skill_json.relative_to(skills_dir).as_posix()
            entry: dict = {
                "rel_path": rel,
                "name": skill_json.parent.name,
                "category": skill_json.parent.parent.name,
            }
            try:
                import json as _json

                data = _json.loads(skill_json.read_text(encoding="utf-8"))
                entry["skill_name"] = data.get("skill_name", entry["name"])
                entry["updated_at"] = data.get("extracted_at", "")
            except Exception:  # noqa: BLE001
                entry["skill_name"] = entry["name"]
            skills.append(entry)
        # 技能库下全部文件（便于直接预览 skill.md / skill.html / frames 等）
        for f in sorted(skills_dir.rglob("*")):
            if f.is_file():
                files.append(_file_info(f.relative_to(skills_dir).as_posix(), skills_dir))

    output_files: list[dict] = []
    if output_dir.exists():
        for f in sorted(output_dir.rglob("*")):
            if f.is_file():
                output_files.append(_file_info(f.relative_to(output_dir).as_posix(), output_dir))

    return {
        "project": project,
        "domain": domain,
        "skills_dir": skills_dir.as_posix(),
        "output_dir": output_dir.as_posix(),
        "skills": skills,
        "skill_files": files,
        "output_files": output_files,
    }


def serve_repo_file(project: str, kind: str, domain: str, rel_path: str) -> FileResponse:
    """安全返回项目内的某个文件（下载 / 预览）。"""
    pdir = projects.project_dir(project)
    if not pdir.exists():
        raise HTTPException(404, f"项目不存在：{project}")
    if kind == "skills":
        base = pdir / "skills_library" / domain
    elif kind == "output":
        base = pdir / "output"
    else:
        raise HTTPException(400, "kind 必须为 skills 或 output")
    target = _safe_join(base, rel_path)
    mime, _ = mimetypes.guess_type(str(target))
    return FileResponse(
        str(target),
        media_type=mime or "application/octet-stream",
        filename=target.name,
    )
