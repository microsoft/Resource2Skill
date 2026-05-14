from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", nav_items: list = None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an interactive, app-like dashboard shell featuring a sticky navigation sidebar,
    a contrasting background canvas, and structured KPI display cards.
    """
    if nav_items is None:
        nav_items = ["Dashboard", "Inputs", "Contacts"]

    ws = wb.create_sheet(sheet_name)
    
    # Hide gridlines to break the "spreadsheet" look
    ws.sheet_view.showGridLines = False

    # Theme definitions (Standard fallbacks mapping)
    primary_color = "1F4E78"    # Dark blue for sidebar/accents
    canvas_bg = "F2F2F2"        # Light gray for dashboard body
    card_bg = "FFFFFF"          # White for widget cards
    text_light = "FFFFFF"       # White text for sidebar
    text_muted = "595959"       # Muted gray for KPI headers

    # 1. Setup Navigation Sidebar (Column A)
    ws.column_dimensions['A'].width = 22
    sidebar_fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")

    for row in range(1, 45):
        ws.cell(row=row, column=1).fill = sidebar_fill

    nav_font = Font(color=text_light, bold=True, size=13)
    for idx, item in enumerate(nav_items):
        row_num = 6 + (idx * 3)
        cell = ws.cell(row=row_num, column=1, value=item)
        cell.font = nav_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        # Internal worksheet hyperlink
        cell.hyperlink = f"#'{item}'!A1"

    # 2. Setup Main Content Canvas Background
    for col_letter in ['C', 'E', 'G']:
        ws.column_dimensions[col_letter].width = 28
    
    # Padding columns
    ws.column_dimensions['B'].width = 4
    ws.column_dimensions['D'].width = 4
    ws.column_dimensions['F'].width = 4

    bg_fill = PatternFill(start_color=canvas_bg, end_color=canvas_bg, fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=45, min_col=2, max_col=10):
        for cell in row:
            cell.fill = bg_fill

    # 3. Dashboard Title
    title_cell = ws.cell(row=3, column=3, value=title)
    title_cell.font = Font(size=22, bold=True, color=primary_color)

    # 4. Construct KPI Cards Structure
    card_fill = PatternFill(start_color=card_bg, end_color=card_bg, fill_type="solid")
    
    kpis = [
        {"col": 3, "label": "Total Sales", "value": "$2,544,000"},
        {"col": 5, "label": "Net Profit", "value": "$890,000"},
        {"col": 7, "label": "Active Customers", "value": "87,040"}
    ]

    for kpi in kpis:
        col = kpi["col"]
        # Draw the card block (Rows 6 through 12)
        for row in range(6, 12):
            cell = ws.cell(row=row, column=col)
            cell.fill = card_fill
            
            # Apply perimeter borders to the card slice
            border_params = {
                'left': Side(style='thin', color='D9D9D9'), 
                'right': Side(style='thin', color='D9D9D9')
            }
            if row == 6: 
                border_params['top'] = Side(style='thin', color='D9D9D9')
            if row == 11: 
                border_params['bottom'] = Side(style='thin', color='D9D9D9')
                
            cell.border = Border(**border_params)

        # Insert KPI Header Label
        lbl_cell = ws.cell(row=7, column=col, value=kpi["label"])
        lbl_cell.font = Font(bold=True, color=text_muted, size=11)
        lbl_cell.alignment = Alignment(horizontal="center")

        # Insert KPI Value
        val_cell = ws.cell(row=9, column=col, value=kpi["value"])
        val_cell.font = Font(bold=True, size=22, color=primary_color)
        val_cell.alignment = Alignment(horizontal="center")

    # 5. Freeze panes to lock the sidebar horizontally and title vertically
    ws.freeze_panes = "B1"
