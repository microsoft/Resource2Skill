"""素材管理（切片2）。

设计原则（与切片1一致，零 core 重构）：
- 素材落地到项目的 fixtures/<domain>/。
- 启用/停用由本模块引入的 manifest.json 记录（R2S core 本身不消费 fixtures，
  该 manifest 是 WebUI 侧的契约，后续切片3 通用 collect 会读取它来筛选素材）。
- 删除走软删除（移动到 fixtures/<domain>/.trash/），沙箱禁止硬删，且可恢复。
- 预览复用 distill_ipd.extract_text 的抽取逻辑（不跑蒸馏，仅抽纯文本），
  MD/TXT 直接读文本；无抽取器或抽取为空时返回友好提示。
- 文件名一律做 Path.name 归一 + 路径穿越校验，避免 ../ 攻击。
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from . import config_store, projects

ALLOWED_EXT = {".pdf", ".docx", ".pptx", ".xlsx", ".md", ".txt"}
PREVIEW_LIMIT = 8000


def _safe_name(name: str) -> str:
    base = Path(name).name
    if not base or base != name or "/" in name or "\\" in name or name.startswith(".."):
        raise ValueError(f"非法文件名：{name}")
    return base


def fixtures_dir(project: str, domain: str) -> Path:
    return projects.project_dir(project) / "fixtures" / domain


def manifest_path(project: str, domain: str) -> Path:
    return fixtures_dir(project, domain) / "manifest.json"


def _load_manifest(project: str, domain: str) -> dict:
    p = manifest_path(project, domain)
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("files"), dict):
                return data
        except Exception:  # noqa: BLE001
            pass
    return {"updated_at": "", "files": {}}


def _save_manifest(project: str, domain: str, data: dict) -> None:
    data["updated_at"] = datetime.now().isoformat(timespec="seconds")
    manifest_path(project, domain).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def list_fixtures(project: str, domain: str) -> list[dict]:
    fdir = fixtures_dir(project, domain)
    if not fdir.exists():
        return []
    manifest = _load_manifest(project, domain)
    files = manifest.setdefault("files", {})
    # 目录真实文件（排除 manifest 与 .trash）
    on_disk = [
        p for p in sorted(fdir.iterdir())
        if p.is_file() and p.name != "manifest.json"
    ]
    trash = fdir / ".trash"
    on_disk = [p for p in on_disk if not str(p).startswith(str(trash))]
    out = []
    seen = set()
    for p in on_disk:
        seen.add(p.name)
        meta = files.get(p.name, {})
        enabled = bool(meta.get("enabled", True))
        files.setdefault(p.name, {
            "enabled": enabled,
            "size": p.stat().st_size,
            "uploaded_at": meta.get("uploaded_at", ""),
        })
        out.append({
            "name": p.name,
            "ext": p.suffix.lower(),
            "size": p.stat().st_size,
            "enabled": enabled,
            "uploaded_at": files[p.name]["uploaded_at"],
        })
    # 清理 manifest 中已不存在的文件条目
    for gone in [k for k in files if k not in seen]:
        del files[gone]
    _save_manifest(project, domain, manifest)
    return out


def save_fixture(project: str, domain: str, filename: str, content: bytes) -> dict:
    name = _safe_name(filename)
    ext = Path(name).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise ValueError(f"不支持的素材类型：{ext}（允许：{', '.join(sorted(ALLOWED_EXT))}）")
    fdir = fixtures_dir(project, domain)
    if not fdir.exists():
        raise FileNotFoundError(f"领域素材目录不存在：{domain}（请先创建领域）")
    dest = fdir / name
    dest.write_bytes(content)
    manifest = _load_manifest(project, domain)
    manifest.setdefault("files", {})[name] = {
        "enabled": True,
        "size": len(content),
        "uploaded_at": datetime.now().isoformat(timespec="seconds"),
    }
    _save_manifest(project, domain, manifest)
    return {"name": name, "size": len(content), "enabled": True}


def set_enabled(project: str, domain: str, filename: str, enabled: bool) -> dict:
    name = _safe_name(filename)
    fdir = fixtures_dir(project, domain)
    if not (fdir / name).exists():
        raise FileNotFoundError(f"素材不存在：{name}")
    manifest = _load_manifest(project, domain)
    meta = manifest.setdefault("files", {}).setdefault(name, {})
    meta["enabled"] = bool(enabled)
    _save_manifest(project, domain, manifest)
    return {"name": name, "enabled": bool(enabled)}


def delete_fixture(project: str, domain: str, filename: str) -> None:
    name = _safe_name(filename)
    fdir = fixtures_dir(project, domain)
    src = fdir / name
    if not src.exists():
        raise FileNotFoundError(f"素材不存在：{name}")
    # 软删除：移动到 .trash（沙箱禁止 rmtree，且可恢复）
    trash = fdir / ".trash"
    trash.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    dest = trash / f"{name}_{ts}"
    i = 1
    while dest.exists():
        dest = trash / f"{name}_{ts}_{i}"
        i += 1
    shutil.move(str(src), str(dest))
    # 从 manifest 移除条目
    manifest = _load_manifest(project, domain)
    manifest.setdefault("files", {}).pop(name, None)
    _save_manifest(project, domain, manifest)


def preview_text(project: str, domain: str, filename: str, max_chars: int = PREVIEW_LIMIT) -> dict:
    name = _safe_name(filename)
    fdir = fixtures_dir(project, domain)
    src = fdir / name
    if not src.exists():
        raise FileNotFoundError(f"素材不存在：{name}")
    ext = src.suffix.lower()
    text = ""
    if ext in (".md", ".txt"):
        try:
            raw = src.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = src.read_text(encoding="gbk", errors="ignore")
        text = raw
    else:
        # 复用 distill_ipd 的抽取逻辑（懒导入，避免启动即加载重型依赖）
        try:
            from distill_ipd import extract_text
            text = extract_text(src)
        except Exception as e:  # noqa: BLE001
            return {"name": name, "text": "", "available": False,
                    "message": f"文本抽取不可用：{e}"}
    if not text or not text.strip():
        return {"name": name, "text": "", "available": False,
                "message": "该文件无可用文本（可能是扫描版图片 PDF，需先 OCR；或格式不受支持）"}
    truncated = len(text) > max_chars
    return {"name": name, "text": text[:max_chars], "available": True,
            "truncated": truncated, "total_chars": len(text)}
