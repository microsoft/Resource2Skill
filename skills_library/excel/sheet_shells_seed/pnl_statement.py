"""
pnl_statement sheet shell
-------------------------
Profit & Loss statement layout: revenue → COGS → gross profit → opex →
operating income → net income, with % of revenue column.

Tier: sheet_shell
Inputs:
    title (str)
    period_label (str): "Q1 2026" / "Year 2025" / etc.
    line_items (list[dict]):
        [{"label": "Revenue", "amount": 1200000, "kind": "revenue"|"cogs"|"opex"|"other_income"|"tax"}, ...]
        Order matters; section subtotals are computed automatically.
    theme (str)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    Alignment, Font, apply_zebra, auto_width, body_font, bottom_border,
    fill, hex_to_argb, header_font, load_theme, thin_border, title_font,
    write_header_row,
)


def render_sheet(wb, sheet_name: str, *, title: str, period_label: str,
                 line_items: list[dict], theme: str = "corporate_blue") -> None:
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    elif (len(wb.sheetnames) == 1 and wb.active.max_row <= 1
          and wb.active.max_column <= 1):
        ws = wb.active
        ws.title = sheet_name
    else:
        ws = wb.create_sheet(sheet_name)

    th = load_theme(theme)
    border = thin_border(th["border_color"])
    body_f = body_font(th)

    # Title
    ws.merge_cells("A1:D1")
    t = ws.cell(row=1, column=1,
                value=f"{title}  ·  {period_label}")
    t.font = title_font(th, size=th.get("font_size_title", 16) + 2)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:D2")
    band = ws.cell(row=2, column=1)
    band.fill = fill(th["accent"])
    ws.row_dimensions[2].height = 4

    # Headers row 4
    headers = ["Line Item", "Amount", "% of Revenue", "Notes"]
    write_header_row(ws, row=4, headers=headers, theme=th)

    # Locate revenue rows for % of revenue formula base
    revenue_rows: list[int] = []
    cur_row = 5
    section_color_map = {
        "revenue": th["good"],
        "cogs":    th["bad"],
        "opex":    th["warn"],
        "tax":     th["bad"],
        "other_income": th["good"],
    }

    # Place items
    for item in line_items:
        label = item["label"]
        amount = item["amount"]
        kind = item.get("kind", "other")
        ws.cell(row=cur_row, column=1, value=label).font = body_f
        amt_cell = ws.cell(row=cur_row, column=2, value=amount)
        amt_cell.number_format = "#,##0;[Red](#,##0)"
        if kind == "revenue":
            revenue_rows.append(cur_row)

        if kind in section_color_map:
            ws.cell(row=cur_row, column=1).font = Font(
                name=th.get("font_body", "Calibri"),
                size=th.get("font_size_body", 11),
                color=hex_to_argb(section_color_map[kind]),
                bold=False,
            )

        # % of revenue formula (filled after revenue row(s) discovered)
        if revenue_rows:
            rev_ref = f"$B${revenue_rows[0]}"
            ws.cell(
                row=cur_row, column=3,
                value=f"=IFERROR(B{cur_row}/{rev_ref},0)",
            ).number_format = "0.0%"

        for c in range(1, 5):
            ws.cell(row=cur_row, column=c).border = border
        cur_row += 1

    # Net total row
    ws.cell(row=cur_row, column=1, value="NET TOTAL").font = Font(
        name=th.get("font_body", "Calibri"), bold=True,
        size=th.get("font_size_body", 11) + 1,
        color=hex_to_argb(th["title_fg"]),
    )
    nt_cell = ws.cell(row=cur_row, column=2,
                      value=f"=SUM(B5:B{cur_row-1})")
    nt_cell.font = Font(name=th.get("font_body", "Calibri"), bold=True,
                        color=hex_to_argb(th["title_fg"]),
                        size=th.get("font_size_body", 11) + 1)
    nt_cell.number_format = "#,##0;[Red](#,##0)"
    if revenue_rows:
        rev_ref = f"$B${revenue_rows[0]}"
        ws.cell(row=cur_row, column=3,
                value=f"=IFERROR(B{cur_row}/{rev_ref},0)").number_format = "0.0%"
    for c in range(1, 5):
        ws.cell(row=cur_row, column=c).fill = fill(th["zebra_bg"])
        ws.cell(row=cur_row, column=c).border = bottom_border(
            th["accent"], weight="medium")
    apply_zebra(ws, 5, cur_row - 1, 1, 4, th)

    auto_width(ws, 1, 4, padding=3, hard_max=32)
    ws.column_dimensions["A"].width = 28
