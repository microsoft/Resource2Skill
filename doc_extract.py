#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""doc_extract.py — generic document text extraction & chunking helpers (domain-agnostic).

This is the domain-neutral extraction layer used by the generic collector
(core/collector.py) and the WebUI fixture-preview endpoint. It deliberately
contains NO domain-specific logic (no hard-coded domain paths, keyword tables, or prompts) —
domain behaviour lives in the caller (e.g. core/collector.py's
GENERIC_SYSTEM_PROMPT, or a domain's own distiller_prompt.md).

Supported source formats: .pdf .pptx .docx .xlsx
"""
from __future__ import annotations

import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("doc_extract")

CHUNK = 16000
OVERLAP = 1200
MAX_CHUNKS_PER_FILE = 30

# Formats that cannot be reliably extracted in this environment / are not sources.
SKIP_EXT = {".doc", ".ppt", ".vsd", ".jpg", ".jpeg", ".png", ".gif", ".bmp",
            ".tif", ".vsdx", ".md", ".xls"}


def _slug(s: str) -> str:
    """ASCII/CJK-safe slug used for category folder names."""
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", s.lower()).strip("_")
    return s[:24] or "general"


def categorize(path: Path) -> str:
    """Best-effort category for a source file, fully domain-agnostic.

    Uses the parent folder name (e.g. a sub-folder organising fixtures) as the
    category; falls back to "general". No domain keyword tables.
    """
    parent = path.parent.name
    if parent and parent.lower() not in ("fixtures", "resources", ""):
        return _slug(parent)
    return "general"


# ---------------------------------------------------------------------------
# text extraction
# ---------------------------------------------------------------------------

def extract_pdf(path: Path) -> str:
    import fitz  # PyMuPDF
    out = []
    doc = fitz.open(str(path))
    for page in doc:
        out.append(page.get_text())
    return "\n".join(out)


def extract_pptx(path: Path) -> str:
    from pptx import Presentation
    p = Presentation(str(path))
    out = []
    for slide in p.slides:
        for shape in slide.shapes:
            if shape.has_table:
                for row in shape.table.rows:
                    out.append(" | ".join(c.text for c in row.cells))
            if shape.has_text_frame:
                txt = shape.text_frame.text.strip()
                if txt:
                    out.append(txt)
    return "\n".join(out)


def extract_docx(path: Path) -> str:
    # python-docx parses paragraphs/tables robustly, including OCR-generated
    # malformed XML; zipfile+regex is a fallback.
    try:
        from docx import Document
        d = Document(str(path))
        parts = [p.text for p in d.paragraphs]
        for tb in d.tables:
            for row in tb.rows:
                parts.append(" | ".join(c.text for c in row.cells))
        return "\n".join(parts)
    except Exception as e:  # noqa: BLE001
        log.warning("python-docx 抽取失败 %s，回退 zipfile: %s", path.name, e)
        try:
            import zipfile
            z = zipfile.ZipFile(str(path))
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
            texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml, re.S)
            return "".join(texts)
        except Exception as e2:  # noqa: BLE001
            log.warning("zipfile 回退也失败 %s: %s", path.name, e2)
            return ""


def extract_xlsx(path: Path) -> str:
    from openpyxl import load_workbook
    wb = load_workbook(str(path), read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            cells = ["" if c is None else str(c) for c in row]
            line = " | ".join(cells).strip()
            if line:
                out.append(line)
    return "\n".join(out)


EXTRACTORS = {".pdf": extract_pdf, ".pptx": extract_pptx,
              ".docx": extract_docx, ".xlsx": extract_xlsx}


def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    fn = EXTRACTORS.get(ext)
    if not fn:
        return ""
    try:
        return fn(path)
    except Exception as e:  # noqa: BLE001
        log.warning("抽取失败 %s: %s", path.name, e)
        return ""


def chunk_text(text: str, max_chunks: int = MAX_CHUNKS_PER_FILE) -> list[str]:
    text = re.sub(r"\s+\n", "\n", text).strip()
    if len(text) <= CHUNK:
        return [text] if text else []
    chunks = []
    start = 0
    while start < len(text) and len(chunks) < max_chunks:
        end = min(start + CHUNK, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - OVERLAP
    return chunks


def parse_skill_name(text: str, fallback: str) -> str:
    m = re.search(r"\*\*Skill Name\*\*[:：]\s*(.+)", text)
    if m:
        name = re.sub(r"[*`\[\]]+", "", m.group(1)).strip()
        return name or fallback
    return fallback
