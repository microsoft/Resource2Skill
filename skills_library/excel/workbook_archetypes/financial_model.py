"""
financial_model archetype
-------------------------
3-sheet financial model:
  - Assumptions  — driver inputs (growth %, margin %, headcount cost)
  - Calculations — formulas referencing Assumptions cells
  - Output       — KPI strip + revenue trend chart

Tier: archetype
Inputs:
    title (str)
    base_revenue (float)
    growth_pct (float) e.g. 0.12
    gross_margin_pct (float) e.g. 0.55
    opex_pct (float) e.g. 0.30
    months (int) default 12
    theme (str)
"""
from __future__ import annotations

import importlib.util as _ilu
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    Alignment, Font, apply_zebra, auto_width, body_font, fill, hex_to_argb,
    header_font, load_theme, thin_border, title_font, write_header_row,
)

_DOMAIN_DIR = Path(__file__).resolve().parents[1]


def _load_shell(shell_id: str):
    spec = _ilu.spec_from_file_location(
        f"_excel_shell_{shell_id}",
        _DOMAIN_DIR / "sheet_shells_seed" / f"{shell_id}.py")
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def _build_assumptions(wb, theme: str, base_revenue: float, growth_pct: float,
                       gross_margin_pct: float, opex_pct: float) -> None:
    if "Assumptions" in wb.sheetnames:
        ws = wb["Assumptions"]
    elif (len(wb.sheetnames) == 1 and wb.active.max_row <= 1
          and wb.active.max_column <= 1):
        ws = wb.active
        ws.title = "Assumptions"
    else:
        ws = wb.create_sheet("Assumptions")

    th = load_theme(theme)
    ws.merge_cells("A1:D1")
    t = ws.cell(row=1, column=1, value="Model Assumptions")
    t.font = title_font(th, size=th.get("font_size_title", 16) + 2)
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:D2")
    ws.cell(row=2, column=1).fill = fill(th["accent"])
    ws.row_dimensions[2].height = 4

    write_header_row(ws, row=4, headers=["Driver", "Value", "Unit", "Notes"],
                     theme=th)

    rows = [
        ("Base monthly revenue", base_revenue, "USD", "Starting point for month 1"),
        ("Monthly growth rate", growth_pct, "%", "Compounded month-over-month"),
        ("Gross margin", gross_margin_pct, "%", "Revenue minus COGS"),
        ("Opex as % of revenue", opex_pct, "%", "Sales, G&A, R&D combined"),
    ]
    border = thin_border(th["border_color"])
    body_f = body_font(th)
    for i, (label, val, unit, note) in enumerate(rows):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = body_f
        v = ws.cell(row=r, column=2, value=val)
        v.font = Font(name=th.get("font_body", "Calibri"),
                      size=th.get("font_size_body", 11), bold=True,
                      color=hex_to_argb(th["title_fg"]))
        if unit == "%":
            v.number_format = "0.0%"
        else:
            v.number_format = "#,##0"
        ws.cell(row=r, column=3, value=unit).font = body_f
        ws.cell(row=r, column=4, value=note).font = body_f
        for c in range(1, 5):
            ws.cell(row=r, column=c).border = border
    apply_zebra(ws, 5, 5 + len(rows) - 1, 1, 4, th)
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 8
    ws.column_dimensions["D"].width = 36


def _build_calculations(wb, theme: str, months: int) -> None:
    ws = wb.create_sheet("Calculations") if "Calculations" not in wb.sheetnames else wb["Calculations"]
    th = load_theme(theme)

    ws.merge_cells("A1:F1")
    t = ws.cell(row=1, column=1, value="Monthly Projections")
    t.font = title_font(th, size=th.get("font_size_title", 16) + 2)
    ws.row_dimensions[1].height = 30
    ws.merge_cells("A2:F2")
    ws.cell(row=2, column=1).fill = fill(th["accent"])
    ws.row_dimensions[2].height = 4

    headers = ["Month", "Revenue", "Gross Profit", "Opex", "Operating Income", "Margin"]
    write_header_row(ws, row=4, headers=headers, theme=th)

    border = thin_border(th["border_color"])
    body_f = body_font(th)
    for i in range(months):
        r = 5 + i
        ws.cell(row=r, column=1, value=f"M{i+1:02d}").font = body_f
        if i == 0:
            ws.cell(row=r, column=2, value="=Assumptions!B5")
        else:
            ws.cell(row=r, column=2, value=f"=B{r-1}*(1+Assumptions!$B$6)")
        ws.cell(row=r, column=2).number_format = "#,##0"
        ws.cell(row=r, column=3, value=f"=B{r}*Assumptions!$B$7").number_format = "#,##0"
        ws.cell(row=r, column=4, value=f"=B{r}*Assumptions!$B$8").number_format = "#,##0"
        ws.cell(row=r, column=5, value=f"=C{r}-D{r}").number_format = "#,##0;[Red](#,##0)"
        ws.cell(row=r, column=6, value=f"=IFERROR(E{r}/B{r},0)").number_format = "0.0%"
        for c in range(1, 7):
            ws.cell(row=r, column=c).border = border
            if c > 1:
                ws.cell(row=r, column=c).font = body_f
    apply_zebra(ws, 5, 5 + months - 1, 1, 6, th)
    auto_width(ws, 1, 6, padding=3, hard_max=20)


def render_workbook(wb, *, title: str = "Financial Model",
                    base_revenue: float = 100000.0,
                    growth_pct: float = 0.05,
                    gross_margin_pct: float = 0.55,
                    opex_pct: float = 0.30,
                    months: int = 12,
                    theme: str = "dark_finance") -> None:
    _build_assumptions(wb, theme, base_revenue, growth_pct,
                       gross_margin_pct, opex_pct)
    _build_calculations(wb, theme, months)

    # Output dashboard
    kpi_shell = _load_shell("kpi_dashboard")
    metrics = [
        {"label": "Title", "value": title},
        {"label": "Months", "value": str(months)},
        {"label": "Base Revenue", "value": f"${base_revenue:,.0f}"},
        {"label": "Growth", "value": f"{growth_pct:+.1%}", "delta_kind": "good"},
        {"label": "Gross Margin", "value": f"{gross_margin_pct:.1%}"},
    ]
    detail_headers = ["Month", "Revenue", "Operating Income"]
    detail_rows = []
    rev = base_revenue
    for i in range(months):
        gm = rev * gross_margin_pct
        opex_v = rev * opex_pct
        op_inc = gm - opex_v
        detail_rows.append([f"M{i+1:02d}", round(rev), round(op_inc)])
        rev = rev * (1 + growth_pct)
    kpi_shell.render_sheet(
        wb, sheet_name="Output", title=f"{title} — Output",
        metrics=metrics, detail_headers=detail_headers,
        detail_rows=detail_rows,
        chart_title="Revenue & Operating Income Projection",
        chart_template="line_trend", theme=theme,
    )
