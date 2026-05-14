from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str, kpis: list, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a two-tone dashboard shell with a header area and a row of cell-based KPI cards.
    
    :param kpis: list of dicts, e.g. [{"label": "Total Calls", "value": "16,749"}, {"label": "Reached", "value": "3,328"}]
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Theme palette fallback (Aspect theme inspired)
    colors = {
        "header_bg": "533A71",   # Deep Purple
        "body_bg": "F2EFF5",     # Light Purple Gray
        "accent": "E5B842",      # Gold
        "card_bg": "FFFFFF",     # White
        "text_light": "FFFFFF",
        "text_dark": "333333"
    }
    
    fill_header = PatternFill("solid", fgColor=colors["header_bg"])
    fill_body = PatternFill("solid", fgColor=colors["body_bg"])
    fill_card = PatternFill("solid", fgColor=colors["card_bg"])
    fill_accent = PatternFill("solid", fgColor=colors["accent"])
    
    # 1. Paint the Canvas
    for row in range(1, 50):
        for col in range(1, 30):
            cell = ws.cell(row=row, column=col)
            if row <= 8:
                cell.fill = fill_header
            else:
                cell.fill = fill_body
                
    # 2. Set Column Widths for a finer layout grid
    for col in range(1, 30):
        ws.column_dimensions[get_column_letter(col)].width = 4.0
        
    # 3. Add Header Text
    ws["B2"] = title
    ws["B2"].font = Font(color=colors["text_light"], size=28, bold=True)
    ws["B3"] = subtitle
    ws["B3"].font = Font(color=colors["accent"], size=14, italic=True)
    
    # 4. Render Cell-based KPI Cards
    if kpis:
        start_col = 2
        kpi_row = 6
        thin = Side(border_style="thin", color="D9D9D9")
        
        for kpi in kpis:
            # Card Dimensions: 6 columns wide, 4 rows high
            end_col = start_col + 5
            end_row = kpi_row + 3
            
            # Fill Card Background
            for r in range(kpi_row, end_row + 1):
                for c in range(start_col, end_col + 1):
                    ws.cell(row=r, column=c).fill = fill_card
            
            # Left Accent Strip (first column of the card)
            for r in range(kpi_row, end_row + 1):
                ws.cell(row=r, column=start_col).fill = fill_accent
                
            # Merge and set Value
            val_cell = ws.cell(row=kpi_row, column=start_col + 1, value=kpi.get("value", ""))
            ws.merge_cells(start_row=kpi_row, start_column=start_col+1, end_row=kpi_row+2, end_column=end_col)
            val_cell.font = Font(size=22, bold=True, color=colors["header_bg"])
            val_cell.alignment = Alignment(horizontal="center", vertical="center")
            
            # Merge and set Label
            lbl_cell = ws.cell(row=kpi_row+3, column=start_col + 1, value=kpi.get("label", "").upper())
            ws.merge_cells(start_row=kpi_row+3, start_column=start_col+1, end_row=kpi_row+3, end_column=end_col)
            lbl_cell.font = Font(size=10, bold=True, color=colors["text_dark"])
            lbl_cell.alignment = Alignment(horizontal="center", vertical="center")
            
            # Apply outer border to the card
            for r in range(kpi_row, end_row + 1):
                for c in range(start_col, end_col + 1):
                    b_top = thin if r == kpi_row else None
                    b_bottom = thin if r == end_row else None
                    b_left = thin if c == start_col else None
                    b_right = thin if c == end_col else None
                    
                    ws.cell(row=r, column=c).border = Border(top=b_top, bottom=b_bottom, left=b_left, right=b_right)
            
            # Advance start_col for next KPI (6 cols for card + 1 col gap)
            start_col += 7
