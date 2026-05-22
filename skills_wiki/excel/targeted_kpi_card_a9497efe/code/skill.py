from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import coordinate_to_tuple, get_column_letter
from openpyxl.formatting.rule import CellIsRule

def render(ws, anchor: str, *, title: str, value, target, prior, format_str: str = "#,##0", is_lower_better: bool = False, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a standalone, conditionally formatted KPI card.
    
    :param title: The KPI metric name (e.g., "Gross Margin")
    :param value: The current period value
    :param target: The target goal value
    :param prior: The previous period value
    :param format_str: Excel number format (e.g., "0%", "$#,##0")
    :param is_lower_better: If True, values below target turn Green. If False, values above target turn Green.
    """
    row, col = coordinate_to_tuple(anchor)
    
    # 1. Write core text and values
    title_cell = ws.cell(row=row, column=col, value=title)
    value_cell = ws.cell(row=row+1, column=col, value=value)
    
    ws.cell(row=row+2, column=col, value="Vs. Target")
    val_target = ws.cell(row=row+2, column=col+1, value=target)
    
    ws.cell(row=row+2, column=col+2, value="Vs. Prior Month")
    val_prior = ws.cell(row=row+2, column=col+3, value=prior)
    
    # 2. Merge regions for the Title and oversized Value
    ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+3)
    ws.merge_cells(start_row=row+1, start_column=col, end_row=row+1, end_column=col+3)
    
    # 3. Base styles
    title_fill = PatternFill(start_color="EFEFEF", end_color="EFEFEF", fill_type="solid")
    title_font = Font(bold=True, size=11, color="333333")
    center_align = Alignment(horizontal="center", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")
    
    thin_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC")
    )

    # 4. Apply base styles across the 4x3 grid to ensure borders wrap merged cells
    for r in range(row, row+3):
        for c in range(col, col+4):
            cell = ws.cell(row=r, column=c)
            cell.border = thin_border
            if r == row:
                cell.fill = title_fill
    
    # Apply specific alignments and fonts
    title_cell.font = title_font
    title_cell.alignment = center_align
    
    value_cell.font = Font(size=24, bold=True)
    value_cell.alignment = center_align
    value_cell.number_format = format_str
    
    # Apply Row 3 benchmark formatting
    for c in range(col, col+4):
        cell = ws.cell(row=row+2, column=c)
        if c in (col+1, col+3):
            cell.number_format = format_str
            cell.alignment = center_align
            cell.font = Font(size=10, bold=True)
        else:
            cell.alignment = right_align
            cell.font = Font(size=9, color="555555")

    # 5. Dynamic Conditional Formatting for the Value
    # Note: Fonts must restate size/bold so they don't revert when the rule triggers
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    green_font = Font(color="006100", size=24, bold=True)
    
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    red_font = Font(color="9C0006", size=24, bold=True)
    
    # Absolute reference to the target cell (e.g., $B$3)
    target_ref = f"${get_column_letter(col+1)}${row+2}"
    
    if is_lower_better:
        good_op = "lessThanOrEqual"
        bad_op = "greaterThan"
    else:
        good_op = "greaterThanOrEqual"
        bad_op = "lessThan"

    value_range = f"{get_column_letter(col)}{row+1}:{get_column_letter(col+3)}{row+1}"
    
    ws.conditional_formatting.add(
        value_range,
        CellIsRule(operator=good_op, formula=[target_ref], stopIfTrue=True, fill=green_fill, font=green_font)
    )
    ws.conditional_formatting.add(
        value_range,
        CellIsRule(operator=bad_op, formula=[target_ref], stopIfTrue=True, fill=red_fill, font=red_font)
    )

    # 6. Dimensions / Spacing
    ws.row_dimensions[row].height = 20
    ws.row_dimensions[row+1].height = 45
    ws.row_dimensions[row+2].height = 18
    
    ws.column_dimensions[get_column_letter(col)].width = 14
    ws.column_dimensions[get_column_letter(col+1)].width = 10
    ws.column_dimensions[get_column_letter(col+2)].width = 16
    ws.column_dimensions[get_column_letter(col+3)].width = 10
