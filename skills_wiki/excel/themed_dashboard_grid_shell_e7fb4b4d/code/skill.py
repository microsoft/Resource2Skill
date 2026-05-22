from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Performance Dashboard", theme: str = "dark_scifi", **kwargs) -> None:
    """
    Renders a stylized, grid-based dashboard shell with distinct panels for KPIs and charts.
    Supports "dark_scifi" (blue/cyan) and "purple_haze" (purple) themes seen in the video.
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    # Clean canvas
    ws.sheet_view.showGridLines = False

    # Theme definitions
    if theme == "purple_haze":
        bg_color = "4A235A"       # Dark purple
        panel_bg = "6C3483"       # Lighter purple
        accent_color = "F5B041"   # Orange/Gold accent
        text_main = "FFFFFF"
    else:
        # Default: dark_scifi
        bg_color = "050B14"       # Deep space blue
        panel_bg = "0D1B2A"       # Panel blue
        accent_color = "00FFFF"   # Cyan accent
        text_main = "FFFFFF"

    fill_bg = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    fill_panel = PatternFill(start_color=panel_bg, end_color=panel_bg, fill_type="solid")
    
    font_title = Font(name="Microsoft YaHei", size=22, bold=True, color=text_main)
    font_panel_title = Font(name="Microsoft YaHei", size=11, bold=True, color=text_main)
    font_kpi_val = Font(name="Arial", size=18, bold=True, color=accent_color)
    
    thin_accent = Side(border_style="thin", color=accent_color)
    align_center = Alignment(horizontal="center", vertical="center")

    # 1. Set global background canvas
    for r in range(1, 40):
        for c in range(1, 21):
            ws.cell(row=r, column=c).fill = fill_bg

    # 2. Main Title Area
    ws.merge_cells("B2:S3")
    title_cell = ws.cell(row=2, column=2, value=title)
    title_cell.font = font_title
    title_cell.alignment = align_center

    # Helper function to draw a stylized dashboard panel
    def create_panel(start_col: int, start_row: int, end_col: int, end_row: int, panel_name: str):
        # Apply fill and outer borders
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_panel
                
                # Determine border sides
                b_top = thin_accent if r == start_row else None
                b_bottom = thin_accent if r == end_row else None
                b_left = thin_accent if c == start_col else None
                b_right = thin_accent if c == end_col else None
                
                cell.border = Border(top=b_top, bottom=b_bottom, left=b_left, right=b_right)
        
        # Panel Title Header (merged across the top row of the panel)
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)
        pt_cell = ws.cell(row=start_row, column=start_col, value=f"  {panel_name}")
        pt_cell.font = font_panel_title
        pt_cell.alignment = Alignment(horizontal="left", vertical="center")

    # 3. Build Dashboard Layout Grids

    # Controls/Slicers Area
    create_panel(2, 5, 19, 7, "Time Filters & Controls")

    # KPI Row
    create_panel(2, 9, 7, 13, "Total Revenue")
    ws.merge_cells("B11:G12")
    ws.cell(row=11, column=2, value="¥ 401,412").font = font_kpi_val
    ws.cell(row=11, column=2).alignment = align_center

    create_panel(8, 9, 13, 13, "Total Profit")
    ws.merge_cells("H11:M12")
    ws.cell(row=11, column=8, value="¥ 68,908").font = font_kpi_val
    ws.cell(row=11, column=8).alignment = align_center

    create_panel(14, 9, 19, 13, "Profit Margin")
    ws.merge_cells("N11:S12")
    ws.cell(row=11, column=14, value="21.0%").font = font_kpi_val
    ws.cell(row=11, column=14).alignment = align_center

    # Main Chart Areas
    create_panel(2, 15, 12, 28, "Monthly Sales & Profit Trend")
    create_panel(13, 15, 19, 21, "Sales Type Breakdown")
    create_panel(13, 22, 19, 28, "Payment Methods")

    # Standardize column widths to form an even grid
    for i in range(1, 21):
        ws.column_dimensions[get_column_letter(i)].width = 7.5
