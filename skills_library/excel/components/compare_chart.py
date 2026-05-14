"""
compare_chart component
-----------------------
Insert a themed comparison chart (clustered bar/line) referencing a data
range. Anchored at a cell.

Tier: component
Inputs:
    data_range (str): full range incl. header row, e.g. "A1:C13"
    sheet_name (str): sheet that contains data_range (defaults to ws.title)
    title (str): chart title
    template (str): chart_templates name (default: bar_compare)
    theme (str): palette name (drives series colors)
    categories_in_first_col (bool): default True
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import hex_to_argb, load_theme  # noqa: E402

import json as _json


def _load_chart_template(name: str) -> dict:
    p = (Path(__file__).resolve().parents[1] / "chart_templates"
         / f"{name}.json")
    if not p.exists():
        p = (Path(__file__).resolve().parents[1] / "chart_templates"
             / "bar_compare.json")
    with p.open("r", encoding="utf-8") as f:
        return _json.load(f)


def render(ws, anchor: str, *, data_range: str, title: str = "",
           template: str = "bar_compare", theme: str = "corporate_blue",
           sheet_name: str | None = None,
           categories_in_first_col: bool = True) -> None:
    from openpyxl.chart import (
        BarChart, LineChart, AreaChart, PieChart, Reference,
    )
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.fill import ColorChoice
    from openpyxl.chart.label import DataLabelList
    from openpyxl.utils.cell import range_boundaries

    cfg = _load_chart_template(template)
    th = load_theme(theme)

    chart_type = cfg.get("chart_type", "BarChart")
    cls_map = {"BarChart": BarChart, "LineChart": LineChart,
               "AreaChart": AreaChart, "PieChart": PieChart}
    cls = cls_map.get(chart_type, BarChart)
    chart = cls()

    if "type" in cfg and hasattr(chart, "type"):
        chart.type = cfg["type"]
    if "grouping" in cfg and hasattr(chart, "grouping"):
        chart.grouping = cfg["grouping"]
    chart.style = cfg.get("style", 11)
    chart.title = title or None
    if cfg.get("show_legend", True):
        chart.legend.position = cfg.get("legend_position", "b")
    else:
        chart.legend = None

    src_sheet = sheet_name or ws.title
    sheet_obj = ws if sheet_name in (None, ws.title) else ws.parent[sheet_name]
    min_col, min_row, max_col, max_row = range_boundaries(data_range)

    if categories_in_first_col:
        data_ref = Reference(sheet_obj, min_col=min_col + 1, min_row=min_row,
                             max_col=max_col, max_row=max_row)
        cats_ref = Reference(sheet_obj, min_col=min_col,
                             min_row=min_row + 1, max_row=max_row)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
    else:
        data_ref = Reference(sheet_obj, min_col=min_col, min_row=min_row,
                             max_col=max_col, max_row=max_row)
        chart.add_data(data_ref, titles_from_data=True)

    accent_palette = [th["accent"], th["accent_alt"], th["good"], th["warn"],
                      th["bad"]]
    for idx, series in enumerate(chart.series):
        try:
            color_hex = accent_palette[idx % len(accent_palette)]
            gp = GraphicalProperties(solidFill=color_hex)
            series.graphicalProperties = gp
        except Exception:
            pass

    if cfg.get("data_labels"):
        chart.dataLabels = DataLabelList(
            showVal=not cfg.get("data_label_pct"),
            showPercent=cfg.get("data_label_pct", False),
        )

    size = cfg.get("default_size", {"width": 18, "height": 10})
    chart.width = size.get("width", 18)
    chart.height = size.get("height", 10)

    ws.add_chart(chart, anchor)
