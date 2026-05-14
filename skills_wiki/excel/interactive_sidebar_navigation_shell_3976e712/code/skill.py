from openpyxl.styles import PatternFill, Font, Alignment

def render_workbook(wb, *, sheets=None, theme="corporate_blue", **kwargs) -> None:
    """
    Creates a multi-sheet dashboard shell with an interactive sidebar navigation.
    """
    if sheets is None:
        sheets = ["Dashboard", "Inputs", "Contacts"]
        
    # Standardize workbook sheets (ensure target sheets exist, remove defaults)
    existing_sheets = wb.sheetnames
    for sheet_name in sheets:
        if sheet_name not in existing_sheets:
            wb.create_sheet(sheet_name)
    for existing in existing_sheets:
        if existing not in sheets:
            wb.remove(wb[existing])
            
    # Define theme colors (fallback to standard hex if palette integration is absent)
    # Sidebar Background: Dark Blue, Active: Lighter Blue
    sidebar_bg = "1F4E78"
    sidebar_active = "2E75B6"
    sidebar_fg = "FFFFFF"
    
    # Map common sheet names to Unicode icons/emojis
    icon_map = {
        "Dashboard": "🏠",
        "Inputs": "⚙️",
        "Data": "📊",
        "Contacts": "👥",
        "Settings": "🔧"
    }
    
    # Common styles
    fill_normal = PatternFill(start_color=sidebar_bg, end_color=sidebar_bg, fill_type="solid")
    fill_active = PatternFill(start_color=sidebar_active, end_color=sidebar_active, fill_type="solid")
    font_nav = Font(color=sidebar_fg, bold=True, size=16)
    align_nav = Alignment(horizontal="center", vertical="center")
    
    for current_sheet in sheets:
        ws = wb[current_sheet]
        
        # Hide gridlines for a clean, app-like interface
        ws.sheet_view.showGridLines = False
        
        # Configure layout dimensions
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 2
        
        # Paint the sidebar background down to row 50
        for row in range(1, 51):
            ws.cell(row=row, column=1).fill = fill_normal
            
        # Place navigation icons and hyperlinks
        start_row = 4
        spacing = 4
        
        for idx, target_sheet in enumerate(sheets):
            icon_row = start_row + (idx * spacing)
            cell = ws.cell(row=icon_row, column=1)
            
            cell.value = icon_map.get(target_sheet, "🔗")
            cell.font = font_nav
            cell.alignment = align_nav
            
            # Create internal hyperlink to the target sheet
            cell.hyperlink = f"#'{target_sheet}'!A1"
            
            # Highlight the active sheet in the sidebar
            if target_sheet == current_sheet:
                # Apply active background to the cell and its immediate neighbors for a larger hit-area effect
                for r in range(icon_row - 1, icon_row + 2):
                    ws.cell(row=r, column=1).fill = fill_active
                    
        # Add a prominent page title in the main content area
        title_cell = ws.cell(row=2, column=3)
        title_cell.value = current_sheet
        title_cell.font = Font(size=24, bold=True, color=sidebar_bg)
