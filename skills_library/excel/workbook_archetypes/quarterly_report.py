"""
quarterly_report archetype
--------------------------
Multi-sheet quarterly business report:
  - Cover         — title, period, theme accent
  - Q1 / Q2 / Q3 / Q4 — populated via sales_report_quarterly shell when data
                        is provided per quarter; otherwise left as blank shells
  - Summary       — KPI strip + full-year revenue chart

Tier: archetype
Inputs:
    title (str)
    period (str): "FY 2025"
    quarters (dict): {"Q1": {"months": [...], "revenue": [...], "target": [...]}, ...}
                     Optional; missing quarters are seeded with placeholder data
    theme (str): palette name
"""
from __future__ import annotations

import importlib.util as _ilu
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    Alignment, fill, hex_to_argb, load_theme, title_font,
)

_DOMAIN_DIR = Path(__file__).resolve().parents[1]


def _load_shell(shell_id: str):
    spec = _ilu.spec_from_file_location(
        f"_excel_shell_{shell_id}",
        _DOMAIN_DIR / "sheet_shells_seed" / f"{shell_id}.py")
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def _build_cover(wb, *, title: str, period: str, theme: str) -> None:
    if "Cover" in wb.sheetnames:
        ws = wb["Cover"]
    elif (len(wb.sheetnames) == 1 and wb.active.max_row <= 1
          and wb.active.max_column <= 1):
        ws = wb.active
        ws.title = "Cover"
    else:
        ws = wb.create_sheet("Cover", 0)

    th = load_theme(theme)

    for r in range(1, 26):
        for c in range(1, 13):
            ws.cell(row=r, column=c).fill = fill(th["body_bg"])
        ws.row_dimensions[r].height = 18

    # Title block
    ws.merge_cells("B6:K8")
    t = ws.cell(row=6, column=2, value=title)
    t.font = title_font(th, size=36)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=2)

    ws.merge_cells("B9:K10")
    p = ws.cell(row=9, column=2, value=period)
    p.font = title_font(th, size=18)
    p.alignment = Alignment(horizontal="left", vertical="center", indent=2)

    # Accent stripe
    ws.merge_cells("B12:K12")
    ws.cell(row=12, column=2).fill = fill(th["accent"])
    ws.row_dimensions[12].height = 6

    # Subtle footer
    ws.merge_cells("B22:K22")
    f = ws.cell(row=22, column=2,
                value="Generated with VideoWorldSkills Excel Domain")
    f.font = title_font(th, size=10)
    f.alignment = Alignment(horizontal="left", indent=2)

    for col in "ABCDEFGHIJKL":
        ws.column_dimensions[col].width = 8


_DEFAULT_QUARTERS = {
    "Q1": {"months": ["Jan", "Feb", "Mar"],
           "revenue": [120000, 135000, 142000],
           "target":  [125000, 130000, 138000]},
    "Q2": {"months": ["Apr", "May", "Jun"],
           "revenue": [148000, 152000, 161000],
           "target":  [145000, 150000, 158000]},
    "Q3": {"months": ["Jul", "Aug", "Sep"],
           "revenue": [165000, 170000, 178000],
           "target":  [160000, 168000, 175000]},
    "Q4": {"months": ["Oct", "Nov", "Dec"],
           "revenue": [185000, 192000, 210000],
           "target":  [180000, 190000, 200000]},
}


def render_workbook(wb, *, title: str = "Quarterly Sales Report",
                    period: str = "FY 2025",
                    quarters: dict | None = None,
                    theme: str = "corporate_blue") -> None:
    quarters = quarters or _DEFAULT_QUARTERS

    _build_cover(wb, title=title, period=period, theme=theme)

    sales_shell = _load_shell("sales_report_quarterly")
    for q_name in ("Q1", "Q2", "Q3", "Q4"):
        q = quarters.get(q_name) or _DEFAULT_QUARTERS[q_name]
        sales_shell.render_sheet(
            wb, sheet_name=q_name,
            title=f"{q_name} {period}",
            months=q["months"],
            revenue=q["revenue"],
            target=q["target"],
            theme=theme,
        )

    # Summary sheet built with kpi_dashboard shell
    kpi_shell = _load_shell("kpi_dashboard")
    total_rev = sum(sum(quarters[q]["revenue"]) for q in ("Q1", "Q2", "Q3", "Q4"))
    total_tgt = sum(sum(quarters[q]["target"])  for q in ("Q1", "Q2", "Q3", "Q4"))
    variance = total_rev - total_tgt
    var_pct = variance / total_tgt if total_tgt else 0
    metrics = [
        {"label": "FY Revenue", "value": f"${total_rev:,.0f}"},
        {"label": "FY Target",  "value": f"${total_tgt:,.0f}"},
        {"label": "Variance",   "value": f"${variance:+,.0f}",
         "delta": f"{var_pct:+.1%}",
         "delta_kind": "good" if variance >= 0 else "bad"},
        {"label": "Best Q",
         "value": max(("Q1", "Q2", "Q3", "Q4"),
                      key=lambda q: sum(quarters[q]["revenue"]))},
        {"label": "Months Tracked", "value": "12"},
    ]
    detail_headers = ["Quarter", "Revenue", "Target", "Variance"]
    detail_rows = []
    for q in ("Q1", "Q2", "Q3", "Q4"):
        rev = sum(quarters[q]["revenue"])
        tgt = sum(quarters[q]["target"])
        detail_rows.append([q, rev, tgt, rev - tgt])
    kpi_shell.render_sheet(
        wb, sheet_name="Summary",
        title=f"{title} — Summary",
        metrics=metrics,
        detail_headers=detail_headers,
        detail_rows=detail_rows,
        chart_title=f"{period} Revenue vs Target by Quarter",
        chart_template="bar_compare",
        theme=theme,
    )

    # Make Cover the first/active sheet
    if "Cover" in wb.sheetnames:
        wb.move_sheet("Cover", offset=-len(wb.sheetnames) + 1)
        wb.active = wb.sheetnames.index("Cover")
