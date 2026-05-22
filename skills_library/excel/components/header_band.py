"""
header_band component
---------------------
Renders a full-width title band + column header row at a given anchor.

Tier: component
Inputs:
    title (str)         — band title (e.g. "Q1 2026 Sales Performance")
    headers (list[str]) — column header labels
    theme (str)         — palette name (default: corporate_blue)
    width (int)         — number of columns the band spans (default: len(headers))
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    Alignment, fill, header_font, load_theme, title_font, write_header_row,
)


def render(ws, anchor: str, *, title: str, headers: list[str],
           theme: str = "corporate_blue", width: int | None = None) -> None:
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

    col_letter, row = coordinate_from_string(anchor)
    start_col = column_index_from_string(col_letter)
    end_col = start_col + (width or len(headers)) - 1

    th = load_theme(theme)

    # Title band
    ws.merge_cells(start_row=row, start_column=start_col,
                   end_row=row, end_column=end_col)
    cell = ws.cell(row=row, column=start_col, value=title)
    cell.font = title_font(th)
    cell.fill = fill(th["body_bg"])
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 30

    # Column header row
    write_header_row(ws, row=row + 1, headers=headers, theme=th,
                     start_col=start_col)
