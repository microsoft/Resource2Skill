from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter

def render(ws, anchor: str, *, title: str = "Asia", subtitle: str = "Revenue", value: float = 369989, highlight: float = 0.05, theme: str = "corporate_blue", **kwargs) -> None:
    theme_palettes = {
        "corporate_blue": {
            "primary": "002060",
            "text_light": "FFFFFF",
            "highlight_bg": "FFFFFF",
            "border": "D9D9D9"
        }
    }
    palette = theme_palettes.get(theme, theme_palettes["corporate_blue"])
    
    col_str, row = coordinate_from_string(anchor)
    start_col = column_index_from_string(col_str)
    
    def get_cell(c, r):
        return ws[f"{get_column_letter(c)}{r}"]
        
    end_col = start_col + 2
    end_row = row + 2
    
    # 1. Fill base card background
    main_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    for r in range(row, end_row + 1):
        for c in range(start_col, end_col + 1):
            cell = get_cell(c, r)
            cell.fill = main_fill
            cell.font = Font(color=palette["text_light"])
            cell.border = Border()
            
    # 2. Title Section (Top full width)
    ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
    title_cell = get_cell(start_col, row)
    title_cell.value = title
    title_cell.font = Font(color=palette["text_light"], bold=True, size=12)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 3. Subtitle Section (Middle-Left)
    ws.merge_cells(start_row=row+1, start_column=start_col, end_row=row+1, end_column=start_col+1)
    subtitle_cell = get_cell(start_col, row+1)
    subtitle_cell.value = subtitle
    subtitle_cell.font = Font(color=palette["text_light"], size=10)
    subtitle_cell.alignment = Alignment(horizontal="left", vertical="bottom")
    
    # 4. Main Value Section (Bottom-Left)
    ws.merge_cells(start_row=row+2, start_column=start_col, end_row=row+2, end_column=start_col+1)
    value_cell = get_cell(start_col, row+2)
    value_cell.value = value
    value_cell.number_format = '"$"#,##0'
    value_cell.font = Font(color=palette["text_light"], bold=True, size=16)
    value_cell.alignment = Alignment(horizontal="left", vertical="top")
    
    # 5. Highlight Section (Right side percentage)
    ws.merge_cells(start_row=row+1, start_column=start_col+2, end_row=row+2, end_column=start_col+2)
    
    hl_fill = PatternFill(start_color=palette["highlight_bg"], end_color=palette["highlight_bg"], fill_type="solid")
    hl_font = Font(color=palette["primary"], bold=True, size=14)
    hl_align = Alignment(horizontal="center", vertical="center")
    
    # Apply to all underlying cells in the merged area to ensure formatting renders correctly
    for r in range(row+1, row+3):
        c_cell = get_cell(start_col+2, r)
        c_cell.fill = hl_fill
        c_cell.font = hl_font
        c_cell.alignment = hl_align
        
    # Set the value to the top-left cell of the merge
    get_cell(start_col+2, row+1).value = highlight
    get_cell(start_col+2, row+1).number_format = '0%'
        
    # Highlight border outline to separate it from the main card visually
    thin_border = Side(border_style="medium", color=palette["border"])
    get_cell(start_col+2, row+1).border = Border(top=thin_border, left=thin_border, right=thin_border)
    get_cell(start_col+2, row+2).border = Border(bottom=thin_border, left=thin_border, right=thin_border)
    
    # 6. Dimensions and Sizing
    ws.column_dimensions[get_column_letter(start_col)].width = 12
    ws.column_dimensions[get_column_letter(start_col+1)].width = 8
    ws.column_dimensions[get_column_letter(start_col+2)].width = 12
    ws.row_dimensions[row].height = 20
    ws.row_dimensions[row+1].height = 18
    ws.row_dimensions[row+2].height = 22
