from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import coordinate_to_tuple, get_column_letter

def render(ws, anchor: str, *, title: str = "Asia", primary_label: str = "Revenue", primary_value: float = 369989, secondary_value: float = 0.05, theme: str = "corporate_blue", **kwargs) -> None:
    # Basic theme palettes mapped to standard tokens
    themes = {
        "corporate_blue": {"bg": "1F4E78", "fg": "FFFFFF", "accent_bg": "FFFFFF", "accent_fg": "1F4E78"},
        "dark": {"bg": "262626", "fg": "FFFFFF", "accent_bg": "FFFFFF", "accent_fg": "262626"},
        "emerald": {"bg": "0F52BA", "fg": "FFFFFF", "accent_bg": "E6F0FA", "accent_fg": "0F52BA"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    start_row, start_col = coordinate_to_tuple(anchor)

    # Styling elements
    card_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    accent_fill = PatternFill(start_color=palette["accent_bg"], end_color=palette["accent_bg"], fill_type="solid")
    
    title_font = Font(color=palette["fg"], size=14, bold=True)
    label_font = Font(color=palette["fg"], size=10)
    value_font = Font(color=palette["fg"], size=12, bold=True)
    secondary_font = Font(color=palette["accent_fg"], size=14, bold=True)
    
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    
    # Outer border matching the card background to frame the white accent box
    card_border = Border(
        left=Side(style="medium", color=palette["bg"]),
        right=Side(style="medium", color=palette["bg"]),
        top=Side(style="medium", color=palette["bg"]),
        bottom=Side(style="medium", color=palette["bg"])
    )

    # 1. Initialize the 3x3 grid with the base card fill and border
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            cell = ws.cell(row=r, column=c)
            cell.fill = card_fill
            cell.border = card_border

    # 2. Set Title (Top Row, merged across 3 columns)
    ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col+2)
    title_cell = ws.cell(row=start_row, column=start_col)
    title_cell.value = title
    title_cell.font = title_font
    title_cell.alignment = center_align

    # 3. Set Primary Label (Middle Row, merged across first 2 columns)
    ws.merge_cells(start_row=start_row+1, start_column=start_col, end_row=start_row+1, end_column=start_col+1)
    p_label_cell = ws.cell(row=start_row+1, column=start_col)
    p_label_cell.value = primary_label
    p_label_cell.font = label_font
    p_label_cell.alignment = left_align

    # 4. Set Primary Value (Bottom Row, merged across first 2 columns)
    ws.merge_cells(start_row=start_row+2, start_column=start_col, end_row=start_row+2, end_column=start_col+1)
    p_val_cell = ws.cell(row=start_row+2, column=start_col)
    p_val_cell.value = primary_value
    p_val_cell.number_format = '"$"#,##0'
    p_val_cell.font = value_font
    p_val_cell.alignment = left_align

    # 5. Set Secondary Value (Middle & Bottom Rows, 3rd column)
    ws.merge_cells(start_row=start_row+1, start_column=start_col+2, end_row=start_row+2, end_column=start_col+2)
    s_val_cell = ws.cell(row=start_row+1, column=start_col+2)
    s_val_cell.value = secondary_value
    s_val_cell.number_format = '0%'
    s_val_cell.font = secondary_font
    s_val_cell.alignment = center_align
    s_val_cell.fill = accent_fill  # Override with accent color

    # 6. Adjust dimensions to shape the card
    ws.row_dimensions[start_row].height = 20
    ws.row_dimensions[start_row+1].height = 15
    ws.row_dimensions[start_row+2].height = 20
    
    ws.column_dimensions[get_column_letter(start_col)].width = 12
    ws.column_dimensions[get_column_letter(start_col+1)].width = 12
    ws.column_dimensions[get_column_letter(start_col+2)].width = 10
