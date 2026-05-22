def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard South America", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an app-like dashboard shell using background fills to create 'cards' 
    and a left-hand navigation sidebar with clickable hyperlinks.
    """
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    
    # Theme palette mappings (fallback to defaults)
    bg_color = "F3F4F6"         # Light gray canvas
    sidebar_color = "1E3A8A"    # Dark blue sidebar
    card_bg = "FFFFFF"          # White cards
    text_color = "111827"       # Dark text
    border_color = "D1D5DB"     # Light gray border to mimic shadow
    
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    fill_bg = PatternFill("solid", fgColor=bg_color)
    fill_sidebar = PatternFill("solid", fgColor=sidebar_color)
    fill_card = PatternFill("solid", fgColor=card_bg)
    
    # 1. Paint the entire visible canvas with the background color
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=18):
        for cell in row:
            cell.fill = fill_bg
            
    # 2. Build the Navigation Sidebar (Column A)
    ws.column_dimensions['A'].width = 8
    for r in range(1, 41):
        ws.cell(row=r, column=1).fill = fill_sidebar
        
    # Inject navigation icons with internal hyperlinks
    # Note: Requires the target sheets to exist for hyperlinks to work perfectly in Excel
    sidebar_items = [
        (3, "🏠", f"#'{sheet_name}'!A1"),
        (6, "📊", f"#'Inputs'!A1"),
        (9, "✉️", f"#'Contacts'!A1"),
        (12, "❓", f"#'Help'!A1")
    ]
    sidebar_font = Font(name="Segoe UI Emoji", size=16, color="FFFFFF")
    for row_idx, icon, link in sidebar_items:
        cell = ws.cell(row=row_idx, column=1, value=icon)
        cell.font = sidebar_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.hyperlink = link

    # 3. Setup Gutters and Column Widths for the Dashboard Grid
    for col in ['B', 'G', 'L']:
        ws.column_dimensions[col].width = 2  # Gutters
    for col in ['C','D','E','F', 'H','I','J','K', 'M','N','O','P']:
        ws.column_dimensions[col].width = 11 # Card content areas

    # Helper function to "draw" a card out of cells
    thin_side = Side(border_style="thin", color=border_color)
    title_font = Font(name="Calibri", size=14, bold=True, color=text_color)
    
    def make_card(min_r: int, min_c: int, max_r: int, max_c: int, card_title: str):
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_card
                
                # Apply outer border to simulate panel edges
                top = thin_side if r == min_r else None
                bottom = thin_side if r == max_r else None
                left = thin_side if c == min_c else None
                right = thin_side if c == max_c else None
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)
        
        # Inject Card Title
        if card_title:
            t_cell = ws.cell(row=min_r + 1, column=min_c + 1, value=card_title)
            t_cell.font = title_font
            t_cell.alignment = Alignment(vertical="top")

    # 4. Render Dashboard Cards
    # Main Header Card
    make_card(2, 3, 4, 16, "") 
    ws.cell(row=2, column=4, value=title).font = Font(name="Calibri", size=22, bold=True, color=text_color)
    ws.cell(row=3, column=4, value="Figures in millions of USD").font = Font(size=11, italic=True, color="6B7280")

    # Top Row: KPI Cards
    make_card(6, 3, 11, 6, "Sales")
    make_card(6, 8, 11, 11, "Profit")
    make_card(6, 13, 11, 16, "# of Customers")

    # Bottom Row: Chart Container Cards
    make_card(13, 3, 26, 11, "2021-2022 Sales Trend (in millions)")
    make_card(13, 13, 26, 16, "Customer Satisfaction")
