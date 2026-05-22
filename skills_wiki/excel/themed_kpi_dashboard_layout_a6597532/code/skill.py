from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str, kpis: list, table_data: list, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a themed KPI dashboard shell featuring a dark header strip,
    inline KPI cards, and a data table with conditional formatting data bars.
    
    Example Data Shapes:
        kpis = [
            {"label": "Total Calls", "value": "16,749"},
            {"label": "Reached", "value": "3,328"},
            {"label": "Deals Closed", "value": "1,203"}
        ]
        table_data = [
            ["Agent Name", "Total Calls", "Calls Reached", "Deals Closed"],
            ["Alice", 1031, 128, 49],
            ["Bob", 661, 73, 28],
            ["Charlie", 610, 86, 67]
        ]
    """
    if sheet_name not in wb.sheetnames:
        ws = wb.create_sheet(sheet_name)
    else:
        ws = wb[sheet_name]
        
    # Standardize theme colors (fallback to the video's purple/gold theme)
    # In a full framework, these would be loaded via the `theme` string parameter
    primary_bg = "4B286D" # Deep purple
    primary_fg = "FFFFFF" # White
    accent1 = "FFC000"    # Gold
    accent2 = "8E63A8"    # Lighter purple
    
    # 1. Header Background Strip
    header_fill = PatternFill(start_color=primary_bg, end_color=primary_bg, fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=8, min_col=1, max_col=20):
        for cell in row:
            cell.fill = header_fill
            
    # 2. Title and Subtitle
    ws['B2'] = title
    ws['B2'].font = Font(size=24, color=primary_fg, bold=True)
    ws['B3'] = subtitle
    ws['B3'].font = Font(size=12, color=accent1, italic=True)
    
    # 3. KPI Cards (Cell-based simulation of modern UI cards)
    col_idx = 4
    for kpi in kpis:
        start_col = col_idx
        end_col = col_idx + 2
        
        # Merge top row for value, bottom row for label
        ws.merge_cells(start_row=5, start_column=start_col, end_row=5, end_column=end_col)
        ws.merge_cells(start_row=6, start_column=start_col, end_row=6, end_column=end_col)
        
        val_cell = ws.cell(row=5, column=start_col)
        val_cell.value = kpi.get('value', '')
        val_cell.font = Font(size=18, bold=True, color="000000")
        val_cell.alignment = Alignment(horizontal="center", vertical="bottom")
        
        lbl_cell = ws.cell(row=6, column=start_col)
        lbl_cell.value = kpi.get('label', '').upper()
        lbl_cell.font = Font(size=9, color="595959", bold=True)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")
        
        # Apply card background and thick left accent border
        card_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        accent_side = Side(style="thick", color=accent1)
        thin_side = Side(style="thin", color="CCCCCC")
        
        for r in (5, 6):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply boundary borders to form the card shape
                top_border = thin_side if r == 5 else None
                bottom_border = thin_side if r == 6 else None
                left_border = accent_side if c == start_col else None
                right_border = thin_side if c == end_col else None
                cell.border = Border(top=top_border, bottom=bottom_border, left=left_border, right=right_border)
                
        col_idx += 4 # Move to the next card position (1 col gap)
        
    # 4. Agent Performance Table
    start_row = 10
    ws.cell(row=start_row, column=2, value="Agent Performance Rankings").font = Font(size=14, bold=True, color=primary_bg)
    
    table_start_row = 12
    if table_data:
        for i, row_data in enumerate(table_data):
            current_row = table_start_row + i
            for j, val in enumerate(row_data):
                cell = ws.cell(row=current_row, column=2+j, value=val)
                if i == 0:
                    # Header row formatting
                    cell.font = Font(bold=True, color=primary_fg)
                    cell.fill = header_fill
                    cell.alignment = Alignment(horizontal="center")
                else:
                    # Alternate row shading (Zebra striping)
                    if i % 2 == 0:
                        cell.fill = PatternFill(start_color="F9F9F9", end_color="F9F9F9", fill_type="solid")
                    if isinstance(val, (int, float)):
                        cell.number_format = '#,##0'

    # Set appropriate column widths
    ws.column_dimensions['A'].width = 2
    ws.column_dimensions['B'].width = 15
    if table_data:
        for c in range(3, 3 + len(table_data[0]) - 1):
            ws.column_dimensions[get_column_letter(c)].width = 14
        
    # 5. Apply Data Bars to the numeric columns
    if len(table_data) > 1:
        last_row = table_start_row + len(table_data) - 1
        
        # Gold data bars for the first metric column (Column D)
        rule_gold = DataBarRule(start_type="min", end_type="max", color=accent1)
        ws.conditional_formatting.add(f"D{table_start_row+1}:D{last_row}", rule_gold)
        
        # Purple data bars for the second metric column (Column E)
        rule_purple = DataBarRule(start_type="min", end_type="max", color=accent2)
        ws.conditional_formatting.add(f"E{table_start_row+1}:E{last_row}", rule_purple)

    # Clean UI: Hide gridlines
    ws.sheet_view.showGridLines = False
