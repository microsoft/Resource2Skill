"""通用采集器（切片3，领域无关）。

与 distill_ipd.py 的关系：
- 复用其文本抽取（extract_text）、切片（chunk_text）、技能名解析（parse_skill_name）、
  归类启发式（categorize）等纯逻辑；
- 但目录**参数化**：素材读项目 fixtures/<domain>/，技能写项目 skills_library/<domain>/，
  **不碰** distill_ipd 的全局 LIB_DIR/RES_DIR，保持多项目隔离、零 core 全局副作用。
- 蒸馏 LLM 传输由调用方注入的 llm_fn 提供（后端用环境变量 + call_azure_openai 实现），
  因此本模块不直接依赖 webui 配置，也不读写全局环境变量。

manifest 约定（与 webui/backend/fixtures.py 一致）：
  fixtures/<domain>/manifest.json -> {"files": {文件名: {"enabled": bool, ...}}}
  仅 enabled 且磁盘存在的素材参与蒸馏。
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

# 复用 distill_ipd 的纯逻辑（不触发其全局 main / 全局目录）
from distill_ipd import (
    extract_text,
    chunk_text,
    parse_skill_name,
    categorize,
)

GENERIC_SYSTEM_PROMPT = """你是一名资深的知识蒸馏专家。下面是一段来自企业资料《{domain}》领域的原文节选。
请将其蒸馏为一条"过程知识技能"，必须严格按如下 Markdown 结构输出，且全文第一行必须是：

**Skill Name**: <8-20 字以内的技能名>

# 概述
（一两句话说明这是什么知识/方法/模板）
# 适用阶段与场景
# 关键角色与职责
（用「角色: 职责」逐条列出，保留原文缩写）
# 标准流程/操作步骤
（编号清单，要可执行）
# 核心交付物
（清单）
# 模板与表单要点
（关键字段/表格名）
# 决策评审/技术评审检查点
（如适用）
# 常用工具与方法
# 常见风险与注意事项
# 来源标注
（资料名）

要求：内容必须来自原文、不得编造；保留原文专业术语与中英对照；步骤可执行；篇幅 600-1500 字。"""


def _load_manifest(fixtures_dir: Path) -> dict:
    p = fixtures_dir / "manifest.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("files"), dict):
                return data
        except Exception:  # noqa: BLE001
            pass
    return {"files": {}}


def _extract_text(path: Path) -> str:
    """抽取素材纯文本。

    distill_ipd.extract_text 仅覆盖 PDF/PPTX/DOCX/XLSX；MD/TXT 在其全局 SKIP_EXT
    中被故意跳过。通用采集器需支持文档类，故此处对 MD/TXT 直接读文本（UTF-8→GBK
    兜底），其余委托 distill_ipd，保持不修改 core 全局行为。
    """
    ext = path.suffix.lower()
    if ext in (".md", ".txt"):
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="gbk", errors="ignore")
    return extract_text(path)


def iter_enabled_fixtures(fixtures_dir: Path) -> list[Path]:
    """返回 manifest 中 enabled 且磁盘确实存在的素材，按文件名排序。"""
    manifest = _load_manifest(fixtures_dir)
    files = manifest.get("files", {})
    trash = fixtures_dir / ".trash"
    out = []
    for p in sorted(fixtures_dir.iterdir()):
        if not p.is_file() or p.name == "manifest.json":
            continue
        if str(p).startswith(str(trash)):
            continue
        meta = files.get(p.name, {})
        if meta.get("enabled", True):
            out.append(p)
    return out


def _read_system_prompt(domain_dir: Path, domain: str) -> str:
    dp = domain_dir / "distiller_prompt.md"
    if dp.exists():
        txt = dp.read_text(encoding="utf-8", errors="ignore").strip()
        if txt:
            return txt
    return GENERIC_SYSTEM_PROMPT.format(domain=domain)


def _store_skill(skills_dir: Path, analysis: str, *, title: str, category: str,
                 rel_path: str, idx: int, total: int, domain: str, index: dict) -> bool:
    skill_name = parse_skill_name(analysis, fallback=title)
    base = re.sub(r"[^a-z0-9]+", "_", title.lower())[:24]
    sid = f"{base}_{idx}_{hashlib.md5((title + analysis[:120]).encode()).hexdigest()[:6]}"
    detail = {
        "skill_id": sid,
        "skill_name": skill_name,
        "domain": domain,
        "category": category,
        "source": {"type": "document", "path": rel_path, "title": title,
                   "chunk": idx, "chunks": total},
        "extracted_at": datetime.now().isoformat(),
        "analysis": analysis,
        "frames": [],
    }
    cat_dir = skills_dir / category / sid
    cat_dir.mkdir(parents=True, exist_ok=True)
    (cat_dir / "skill.json").write_text(
        json.dumps(detail, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    existing = {s["skill_id"] for s in index["skills"]}
    if sid not in existing:
        index["skills"].append({
            "skill_id": sid,
            "skill_name": skill_name,
            "category": category,
            "source_document": rel_path,
            "source_title": title,
            "detail_path": f"{category}/{sid}/skill.json",
        })
    return True


def _save_index(skills_dir: Path, index: dict) -> None:
    skills_dir.mkdir(parents=True, exist_ok=True)
    index["updated_at"] = datetime.now().isoformat()
    index["total"] = len(index["skills"])
    (skills_dir / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _load_index(skills_dir: Path) -> dict:
    p = skills_dir / "index.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "skills" in data:
                return data
        except Exception:  # noqa: BLE001
            pass
    return {"updated_at": "", "total": 0, "skills": []}


def distill_document(
    path: Path,
    *,
    skills_dir: Path,
    domain: str,
    system_prompt: str,
    llm_fn,
    index: dict,
    on_log=print,
    dry_run: bool = False,
    model: str = "deepseek-v4-pro",
    max_tokens: int = 6000,
    reasoning: str = "low",
) -> dict:
    """蒸馏单个素材文件（可能多段），写入技能库。返回 {added, skipped}。"""
    rel = f"fixtures/{domain}/{path.name}"
    category = categorize(path)
    text = _extract_text(path)
    chunks = chunk_text(text)
    if not chunks:
        on_log(f"[跳过] {path.name}：无可用文本（可能需 OCR / 不支持格式）")
        return {"added": 0, "skipped": 1}
    total = len(chunks)
    on_log(f"[素材] {path.name} → 类别={category}，切片 {total} 段")
    added = 0
    for i, ch in enumerate(chunks, 1):
        user = (
            f"【资料来源】《{path.stem}》\n【归类类别】{category}\n"
            f"【节选段落】第 {i}/{total} 段\n\n以下为原文节选：\n\n{ch}"
        )
        if dry_run:
            analysis = (
                f"**Skill Name**: {path.stem} 草稿（dry-run 未调用 LLM）\n\n"
                "# 概述\n（dry-run 占位，未调用 LLM）\n# 适用阶段与场景\n# 关键角色与职责\n"
                "# 标准流程/操作步骤\n# 核心交付物\n# 模板与表单要点\n# 决策评审/技术评审检查点\n"
                "# 常用工具与方法\n# 常见风险与注意事项\n# 来源标注\n" + path.name
            )
        else:
            try:
                msg = llm_fn(
                    [{"role": "system", "content": system_prompt},
                     {"role": "user", "content": user}],
                    model=model, max_tokens=max_tokens, reasoning_effort=reasoning,
                )
                analysis = (msg.get("content") if isinstance(msg, dict) else str(msg) or "").strip()
            except Exception as e:  # noqa: BLE001
                on_log(f"[错误] {path.name} 段{i}/{total} 蒸馏失败：{e}")
                continue
        if not analysis:
            on_log(f"[警告] {path.name} 段{i}/{total} 返回空，跳过")
            continue
        _store_skill(skills_dir, analysis, title=path.stem, category=category, rel_path=rel,
                     idx=i, total=total, domain=domain, index=index)
        added += 1
        on_log(f"[OK] {path.name} 段{i}/{total} → {parse_skill_name(analysis, path.stem)}")
    return {"added": added, "skipped": 0}


def run_collect(
    *,
    fixtures_dir: Path,
    skills_dir: Path,
    domain_dir: Path,
    domain: str,
    llm_fn,
    on_log=print,
    dry_run: bool = False,
    model: str = "deepseek-v4-pro",
    max_tokens: int = 6000,
    reasoning: str = "low",
    stop_check=None,
) -> dict:
    """通用采集主流程。返回 {added, skipped, total_skills}。"""
    system_prompt = _read_system_prompt(domain_dir, domain)
    index = _load_index(skills_dir)
    sources = iter_enabled_fixtures(fixtures_dir)
    on_log(f"通用采集：发现 enabled 素材 {len(sources)} 个（领域={domain}）")
    added = 0
    skipped = 0
    for path in sources:
        if stop_check and stop_check():
            on_log("[停止] 收到终止信号，提前结束")
            break
        res = distill_document(
            path, skills_dir=skills_dir, domain=domain, system_prompt=system_prompt,
            llm_fn=llm_fn, index=index, on_log=on_log, dry_run=dry_run,
            model=model, max_tokens=max_tokens, reasoning=reasoning,
        )
        added += res["added"]
        skipped += res["skipped"]
        _save_index(skills_dir, index)
    _save_index(skills_dir, index)
    on_log(f"采集完成：新增技能 {added} 条，跳过 {skipped} 个，技能库现有 {len(index['skills'])} 条")
    return {"added": added, "skipped": skipped, "total_skills": len(index["skills"])}
