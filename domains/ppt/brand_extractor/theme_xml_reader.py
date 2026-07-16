"""Deterministic OOXML brand-signal extractor.

Reads ppt/theme/themeN.xml inside .pptx files and aggregates color/font
signals across a brand bundle. No LLM calls.

Pure stdlib (zipfile + xml.etree). Refuses to crash on malformed files:
returns an empty signal instead, since brand bundles often contain
half-broken template files.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET
import zipfile

A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


@dataclass
class PptxThemeSignal:
    source_file: str
    colors_raw: list[str] = field(default_factory=list)  # 6-hex, no '#'
    fonts_raw: list[str] = field(default_factory=list)
    scheme_colors_raw: list[str] = field(default_factory=list)
    custom_scheme_colors_raw: list[str] = field(default_factory=list)
    scheme_name: str | None = None


@dataclass
class BrandSignals:
    primary: str  # '#RRGGBB'
    secondary: str
    accents: list[str]
    neutrals: list[str]
    heading_font: str
    body_font: str
    mono_font: str | None


def _iter_theme_xmls(pptx: Path):
    with zipfile.ZipFile(pptx) as zf:
        for name in zf.namelist():
            if name.startswith("ppt/theme/") and name.endswith(".xml"):
                with zf.open(name) as f:
                    yield name, f.read()


def _is_hex_color(value: str | None) -> bool:
    if not value or len(value) != 6:
        return False
    return all(ch in "0123456789ABCDEFabcdef" for ch in value)


def read_pptx_theme(pptx: Path) -> PptxThemeSignal:
    sig = PptxThemeSignal(source_file=pptx.name)
    try:
        for _name, data in _iter_theme_xmls(pptx):
            root = ET.fromstring(data)
            for el in root.iter(f"{A_NS}srgbClr"):
                v = el.get("val")
                if _is_hex_color(v):
                    sig.colors_raw.append(v.upper())

            clr_scheme = root.find(f".//{A_NS}clrScheme")
            if clr_scheme is not None:
                scheme_name = clr_scheme.get("name")
                if sig.scheme_name is None:
                    sig.scheme_name = scheme_name
                for token in list(clr_scheme):
                    srgb = token.find(f"{A_NS}srgbClr")
                    if srgb is not None:
                        v = srgb.get("val")
                        if _is_hex_color(v):
                            color = v.upper()
                            sig.scheme_colors_raw.append(color)
                            if scheme_name and scheme_name.lower() != "office":
                                sig.custom_scheme_colors_raw.append(color)

            for el in root.iter(f"{A_NS}latin"):
                t = el.get("typeface")
                if t:
                    sig.fonts_raw.append(t)
            for el in root.iter(f"{A_NS}font"):
                t = el.get("typeface")
                if t:
                    sig.fonts_raw.append(t)
    except (zipfile.BadZipFile, ET.ParseError):
        pass
    return sig


def _saturation(hex_: str) -> float:
    r, g, b = int(hex_[0:2], 16) / 255, int(hex_[2:4], 16) / 255, int(hex_[4:6], 16) / 255
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == 0:
        return 0.0
    return (mx - mn) / mx


def _luma(hex_: str) -> float:
    r, g, b = int(hex_[0:2], 16), int(hex_[2:4], 16), int(hex_[4:6], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b


def _unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def _is_brand_candidate(hex_: str) -> bool:
    if hex_ in {"FFFFFF", "000000", "808080", "C0C0C0", "F2F2F2", "D9D9D9"}:
        return False
    luma = _luma(hex_)
    return 20 <= luma <= 230


def aggregate_brand_signals(sigs: list[PptxThemeSignal]) -> BrandSignals:
    color_counter: Counter[str] = Counter()
    font_counter: Counter[str] = Counter()
    ordered_scheme_colors: list[str] = []
    custom_scheme_colors: list[str] = []
    for s in sigs:
        color_counter.update(s.colors_raw)
        font_counter.update(s.fonts_raw)
        ordered_scheme_colors.extend(s.scheme_colors_raw)
        if s.scheme_name and s.scheme_name.lower() != "office":
            custom_scheme_colors.extend(s.scheme_colors_raw)

    preferred_scheme_colors = custom_scheme_colors or ordered_scheme_colors
    scheme_candidates = [c for c in _unique_in_order(preferred_scheme_colors) if _is_brand_candidate(c)]
    ranked_candidates = [(c, n) for c, n in color_counter.items() if _is_brand_candidate(c)]
    ranked_candidates.sort(key=lambda x: -(x[1] * (0.5 + _saturation(x[0]))))
    ranked_unique = [c for c, _ in ranked_candidates]

    brand_colors = _unique_in_order(scheme_candidates + ranked_unique)
    if not brand_colors:
        raise RuntimeError("no usable brand colors found in any theme.xml")

    primary = "#" + brand_colors[0]
    secondary = "#" + (brand_colors[1] if len(brand_colors) > 1 else brand_colors[0])
    accents = ["#" + c for c in brand_colors[2:6]]
    if not accents:
        accents = [secondary]

    all_colors = sorted(color_counter, key=_luma)
    near_black = next((c for c in all_colors if _luma(c) < 40), "0A0011")
    near_white = next((c for c in reversed(all_colors) if _luma(c) > 215), "FFFFFF")
    neutrals = ["#" + near_black, "#" + near_white]

    fonts_ranked = [f for f, _ in font_counter.most_common()]
    heading = next(
        (f for f in fonts_ranked if any(s in f for s in ("Bold", "Semibold", "Medium"))),
        fonts_ranked[0] if fonts_ranked else "Arial",
    )
    heading_family = heading.split()[0] if heading else ""
    body = next(
        (
            f
            for f in fonts_ranked
            if f != heading and heading_family and (f == heading_family or f.startswith(f"{heading_family} "))
        ),
        next((f for f in fonts_ranked if f != heading), heading),
    )
    mono = next(
        (f for f in fonts_ranked if any(s in f.lower() for s in ("mono", "consolas", "courier"))),
        None,
    )

    return BrandSignals(
        primary=primary,
        secondary=secondary,
        accents=accents,
        neutrals=neutrals,
        heading_font=heading,
        body_font=body,
        mono_font=mono,
    )
