from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.formatting.rule import CellIsRule

def render(ws: Worksheet, anchor: str, metrics: list[dict] = None, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a horizontal strip of KPI cards using cell formatting to simulate floating shapes.
    """
    if not metrics:
        metrics = [
            {"title": "TOTAL REVENUE", "value": 213983614, "format": "£#,##0", "var": 0.018},
            {"title": "TOTAL PROFIT", "value": 56429310, "format": "£#,##0", "var": 0.2637},
            {"title": "PROFIT %", "value": 0.2637, "format": "0.00%", "var": -0.051},
            {"title": "TOTAL UNITS SOLD", "value": 1350956, "format": "#,##0", "var": 0.042},
        ]

    # Theme token resolution (hardcoded to match typical modern dashboard defaults)
    card_bg = "FFFFFF"
    text_main = "000000"
    text_muted = "595959"
    pos_color = "008A00" # Green
    neg_color = "E51400" # Red
    border_color = "D9D9D9"

    col_idx = column_index_from_string(anchor.upper())
    row_idx = int(''.join(filter(str.isdigit, anchor)))

    card_fill = PatternFill("solid", fgColor=card_bg)
    thin_edge = Side(style='thin', color=border_color)

    # Set row heights for the 3 rows that make up the card
    ws.row_dimensions[row_idx].height = 25     # Row 1: Title
    ws.row_dimensions[row_idx+1].height = 35   # Row 2: Main Value
    ws.row_dimensions[row_idx+2].height = 25   # Row 3: Variance Footer

    for i, metric in enumerate(metrics):
        # 3 columns per card + 1 gap column = 4 columns per metric
        base_col = col_idx + (i * 4)

        # Define column widths for the card's internal layout
        ws.column_dimensions[get_column_letter(base_col)].width = 12    # Variance % Box
        ws.column_dimensions[get_column_letter(base_col+1)].width = 20  # Variance Label
        ws.column_dimensions[get_column_letter(base_col+2)].width = 5   # Right Padding
        ws.column_dimensions[get_column_letter(base_col+3)].width = 3   # Exterior Gap between cards

        # Apply background and outer border to the card area (3x3 grid of cells)
        for r in range(row_idx, row_idx + 3):
            for c in range(base_col, base_col + 3):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Calculate outer border edges
                b_top = thin_edge if r == row_idx else None
                b_bottom = thin_edge if r == row_idx + 2 else None
                b_left = thin_edge if c == base_col else None
                b_right = thin_edge if c == base_col + 2 else None
                cell.border = Border(top=b_top, bottom=b_bottom, left=b_left, right=b_right)

        # Row 1: Title
        title_cell = ws.cell(row=row_idx, column=base_col)
        title_cell.value = metric["title"]
        title_cell.font = Font(name="Arial", size=9, bold=True, color=text_muted)
        title_cell.alignment = Alignment(vertical="center", indent=1)
        ws.merge_cells(start_row=row_idx, start_column=base_col, end_row=row_idx, end_column=base_col+1)

        # Row 2: Value
        val_cell = ws.cell(row=row_idx+1, column=base_col)
        val_cell.value = metric["value"]
        val_cell.number_format = metric["format"]
        val_cell.font = Font(name="Arial", size=20, bold=True, color=text_main)
        val_cell.alignment = Alignment(vertical="center", indent=1)
        ws.merge_cells(start_row=row_idx+1, start_column=base_col, end_row=row_idx+1, end_column=base_col+1)

        # Row 3: Variance Percent
        var_cell = ws.cell(row=row_idx+2, column=base_col)
        var_cell.value = metric["var"]
        var_cell.number_format = "0.0%"
        var_cell.font = Font(name="Arial", size=10, bold=True)
        var_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Add Conditional Formatting for the Variance Percent Cell
        col_let = get_column_letter(base_col)
        cf_range = f"{col_let}{row_idx+2}:{col_let}{row_idx+2}"
        ws.conditional_formatting.add(
            cf_range,
            CellIsRule(operator='greaterThan', formula=['0'], font=Font(color=pos_color, bold=True))
        )
        ws.conditional_formatting.add(
            cf_range,
            CellIsRule(operator='lessThan', formula=['0'], font=Font(color=neg_color, bold=True))
        )

        # Row 3: Variance Label
        var_lbl_cell = ws.cell(row=row_idx+2, column=base_col+1)
        var_lbl_cell.value = "COMPARE TO BUDGET"
        var_lbl_cell.font = Font(name="Arial", size=8, bold=True, color=text_muted)
        var_lbl_cell.alignment = Alignment(horizontal="left", vertical="center")
