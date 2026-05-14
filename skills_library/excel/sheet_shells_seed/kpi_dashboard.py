"""
kpi_dashboard sheet shell
-------------------------
Builds a single-sheet KPI dashboard:
  - Title band (rows 1-2)
  - KPI strip with up to 5 cards (rows 4-7)
  - Comparison chart (rows 9+, right side)
  - Detail data table (rows 9+, left side)

Tier: sheet_shell
Inputs:
    title (str)
    metrics (list[dict]) — for kpi_strip
    detail_headers (list[str])
    detail_rows (list[list]) — data rows aligned with detail_headers
    chart_data_range (str|None) — explicit range for chart; if None we infer
                                  numeric columns of detail data.
    chart_title (str)
    theme (str) — palette name (default: corporate_blue)
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

import importlib.util as _ilu

_DOMAIN_DIR = Path(__file__).resolve().parents[1]


def _load(component_id: str):
    spec = _ilu.spec_from_file_location(
        f"_excel_comp_{component_id}",
        _DOMAIN_DIR / "components" / f"{component_id}.py",
    )
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def render_sheet(wb, sheet_name: str, *, title: str,
                 metrics: list[dict], detail_headers: list[str],
                 detail_rows: list[list],
                 chart_title: str = "",
                 chart_data_range: str | None = None,
                 chart_template: str = "bar_compare",
                 theme: str = "corporate_blue") -> None:
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        # If only the default placeholder is left and unused, repurpose it
        if (len(wb.sheetnames) == 1
                and wb.active.max_row <= 1 and wb.active.max_column <= 1):
            ws = wb.active
            ws.title = sheet_name
        else:
            ws = wb.create_sheet(sheet_name)

    th = load_theme(theme)

    # --- title band rows 1-2 ---
    n_cols = max(len(detail_headers), 8)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n_cols)
    t = ws.cell(row=1, column=1, value=title)
    t.font = title_font(th, size=th.get("font_size_title", 16) + 4)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 36

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n_cols)
    sub = ws.cell(row=2, column=1, value="")
    sub.fill = fill(th["accent"])
    ws.row_dimensions[2].height = 4

    # --- KPI strip rows 4-7 ---
    if metrics:
        kpi_mod = _load("kpi_strip")
        kpi_mod.render(ws, "A4", metrics=metrics[:5], theme=theme,
                       card_width=3, card_height_rows=4)

    # --- Detail table starting row 10 ---
    table_start_row = 10
    write_header_row(ws, row=table_start_row, headers=detail_headers,
                     theme=th, start_col=1)
    border = thin_border(th["border_color"])
    body_f = body_font(th)
    for r_idx, row_data in enumerate(detail_rows):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=table_start_row + 1 + r_idx,
                           column=1 + c_idx, value=val)
            cell.font = body_f
            cell.border = border
            if c_idx > 0 and isinstance(val, (int, float)):
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right")
    last_row = table_start_row + len(detail_rows)
    apply_zebra(ws, table_start_row + 1, last_row, 1, len(detail_headers), th)

    # Summary row
    if detail_rows and len(detail_headers) > 1:
        sumrow_mod = _load("summary_row")
        sumrow_mod.render(
            ws, anchor=f"A{table_start_row + 1}",
            data_range=f"A{table_start_row}:"
                       f"{chr(64+len(detail_headers))}{last_row}",
            label="TOTAL", op="SUM",
            number_format="#,##0", theme=theme,
        )

    # --- Chart top-right ---
    if not chart_data_range:
        chart_data_range = (
            f"A{table_start_row}:"
            f"{chr(64+len(detail_headers))}{last_row}"
        )
    chart_mod = _load("compare_chart")
    chart_anchor_col = chr(ord("A") + len(detail_headers) + 1)
    chart_mod.render(
        ws, anchor=f"{chart_anchor_col}4",
        data_range=chart_data_range,
        title=chart_title or title,
        template=chart_template,
        theme=theme,
        sheet_name=sheet_name,
    )

    # Column widths
    auto_width(ws, min_col=1, max_col=len(detail_headers), padding=3, hard_max=22)
