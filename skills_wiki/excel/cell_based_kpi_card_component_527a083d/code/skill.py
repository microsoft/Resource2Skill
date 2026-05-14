def render(ws, anchor: str, *, title: str, value_ref: str, pct_ref: str = None, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
    
    # Fallback theme palette
    palettes = {
        "corporate_blue": {"primary_bg": "002060", "primary_fg": "FFFFFF"}, # Navy/White
        "dark_mode": {"primary_bg": "333333", "primary_fg": "E2E2E2"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    bg_color = palette["primary_bg"]
    fg_color = palette["primary_fg"]

    col_str, row = coordinate_from_string(anchor)
    col_idx = column_index_from_string(col_str)

    card_width = 2
    card_height = 3

    # 1. Apply background to the entire block to simulate a cohesive "shape"
    fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    thick_border = Side(border_style="medium", color="FFFFFF")
    # Outer white border to separate the card from the grid
    border = Border(top=thick_border, left=thick_border, right=thick_border, bottom=thick_border)

    for r in range(row, row + card_height):
        for c in range(col_idx, col_idx + card_width):
            cell = ws.cell(row=r, column=c)
            cell.fill = fill
            cell.border = border

    # 2. Row 1: Title (Merged)
    ws.merge_cells(start_row=row, start_column=col_idx, end_row=row, end_column=col_idx + card_width - 1)
    title_cell = ws.cell(row=row, column=col_idx)
    title_cell.value = title
    title_cell.font = Font(color=fg_color, size=11, bold=False)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Row 2: Main Value (Merged)
    ws.merge_cells(start_row=row+1, start_column=col_idx, end_row=row+1, end_column=col_idx + card_width - 1)
    val_cell = ws.cell(row=row+1, column=col_idx)
    # Link to the data cell via formula (e.g. '=B2')
    val_cell.value = f"={value_ref}"
    val_cell.font = Font(color=fg_color, size=16, bold=True)
    val_cell.alignment = Alignment(horizontal="center", vertical="center")
    val_cell.number_format = '"$"#,##0'

    # 4. Row 3: Secondary Metric (Bottom Right corner)
    if pct_ref:
        pct_cell = ws.cell(row=row+2, column=col_idx + 1)
        pct_cell.value = f"={pct_ref}"
        pct_cell.font = Font(color=fg_color, size=12, bold=True)
        pct_cell.alignment = Alignment(horizontal="center", vertical="center")
        pct_cell.number_format = '0%'
        
        # Merge the remaining bottom-left cell to keep things clean
        ws.merge_cells(start_row=row+2, start_column=col_idx, end_row=row+2, end_column=col_idx)
