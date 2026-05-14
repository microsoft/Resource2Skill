from openpyxl.styles import Font, PatternFill, Alignment

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a clean dashboard shell, turning off gridlines, adding a branded title banner,
    and arranging up to 3 provided charts into a standard asymmetrical grid.
    """
    # Create the dashboard sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(title=sheet_name)
    
    # 1. Canvas Setup: Hide gridlines for a cleaner dashboard aesthetic
    ws.sheet_view.showGridLines = False

    # 2. Theme Integration
    # Fallbacks for corporate_blue. In a standard framework, load from a palette helper.
    bg_color = "2F5597"  # primary
    fg_color = "FFFFFF"  # text_light

    # 3. Title Banner
    # Merging across A-R creates a full-width banner for standard monitor resolutions
    ws.merge_cells("A1:R3")
    title_cell = ws["A1"]
    title_cell.value = title
    title_cell.font = Font(name="Calibri", size=24, bold=True, color=fg_color)
    title_cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    title_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # 4. Auto-arrange Charts
    # Fetches pre-configured openpyxl chart objects passed by the caller
    charts = kwargs.get("charts", [])
    
    # Standard asymmetrical grid: 1 large main panel (left), 2 smaller stacked panels (right)
    grid_layout = [
        {"anchor": "B5", "width": 18, "height": 13},   # Primary visualization
        {"anchor": "K5", "width": 13, "height": 6},    # Secondary metric (top)
        {"anchor": "K16", "width": 13, "height": 6}    # Secondary metric (bottom)
    ]

    for i, chart in enumerate(charts):
        if i < len(grid_layout):
            pos = grid_layout[i]
            
            # Override chart dimensions to strictly snap to the predefined dashboard grid
            chart.width = pos["width"]
            chart.height = pos["height"]
            
            ws.add_chart(chart, pos["anchor"])
