from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, RadarChart, Reference

def render_workbook(wb, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Generates a multi-sheet dashboard with a fixed sidebar navigation pane.
    """
    # 1. Theme Configuration
    themes = {
        "corporate_blue": {"sidebar_bg": "1F4E78", "sidebar_fg": "FFFFFF", "accent": "2F75B5", "bg": "F2F2F2"},
        "dark_mode": {"sidebar_bg": "262626", "sidebar_fg": "FFFFFF", "accent": "0070C0", "bg": "000000"}
    }
    colors = themes.get(theme, themes["corporate_blue"])

    sidebar_fill = PatternFill(start_color=colors["sidebar_bg"], end_color=colors["sidebar_bg"], fill_type="solid")
    sidebar_font = Font(color=colors["sidebar_fg"], bold=True, size=12, underline="none")
    sidebar_align = Alignment(horizontal="center", vertical="center")
    
    # 2. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_inputs = wb.create_sheet("Inputs")
    ws_contacts = wb.create_sheet("Contacts")
    
    sheets = [ws_dash, ws_inputs, ws_contacts]
    nav_links = [("🏠 Dash", "Dashboard"), ("📊 Inputs", "Inputs"), ("📞 Contacts", "Contacts")]

    # 3. Apply Navigation Sidebar to All Sheets
    for ws in sheets:
        ws.column_dimensions['A'].width = 15
        ws.sheet_view.showGridLines = False
        
        # Color the sidebar background
        for row in range(1, 40):
            ws.cell(row=row, column=1).fill = sidebar_fill
            
        # Insert Nav Links
        for idx, (label, target_sheet) in enumerate(nav_links):
            row_num = 4 + (idx * 3)  # Spaced out at rows 4, 7, 10
            cell = ws.cell(row=row_num, column=1, value=label)
            cell.hyperlink = f"#'{target_sheet}'!A1"
            cell.font = sidebar_font
            cell.alignment = sidebar_align

    # 4. Populate Inputs Data
    # Customer Satisfaction Data (Radar Chart)
    satisfaction_data = [
        ["Metric", "Score"],
        ["Speed", 54],
        ["Availability", 96],
        ["Service", 53],
        ["Hygiene", 93],
        ["Quality", 86]
    ]
    for r_idx, row_data in enumerate(satisfaction_data, 1):
        for c_idx, val in enumerate(row_data, 1):
            ws_inputs.cell(row=r_idx, column=2+c_idx, value=val)

    # Sales Trend Data (Line Chart)
    trend_data = [
        ["Month", "2021", "2022"],
        ["Jan", 201.9, 215.3],
        ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1],
        ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3]
    ]
    for r_idx, row_data in enumerate(trend_data, 1):
        for c_idx, val in enumerate(row_data, 1):
            ws_inputs.cell(row=r_idx, column=5+c_idx, value=val)

    # 5. Build Dashboard Content
    # Dashboard Title
    title_cell = ws_dash.cell(row=2, column=3, value=title)
    title_cell.font = Font(size=20, bold=True, color=colors["sidebar_bg"])

    # KPI Summary Cards (Simulated with Borders)
    card_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC")
    )
    
    kpis = [("Sales", "$2,544 M", 3), ("Profit", "$890 M", 6), ("Customers", "87.0 M", 9)]
    for label, val, col in kpis:
        lbl_cell = ws_dash.cell(row=4, column=col, value=label)
        val_cell = ws_dash.cell(row=5, column=col, value=val)
        
        lbl_cell.font = Font(color="595959", bold=True)
        val_cell.font = Font(size=18, bold=True, color=colors["accent"])
        
        for r in (4, 5):
            for c in range(col, col+2):
                ws_dash.cell(row=r, column=c).border = card_border

    # Line Chart: Sales Trend
    line_chart = LineChart()
    line_chart.title = "Sales Trend (in millions)"
    line_chart.style = 13
    line_chart.width = 14
    line_chart.height = 7
    data = Reference(ws_inputs, min_col=7, min_row=1, max_col=8, max_row=6)
    cats = Reference(ws_inputs, min_col=6, min_row=2, max_row=6)
    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(cats)
    ws_dash.add_chart(line_chart, "C8")

    # Radar Chart: Customer Satisfaction
    radar_chart = RadarChart()
    radar_chart.type = "filled"
    radar_chart.title = "Customer Satisfaction"
    radar_chart.width = 10
    radar_chart.height = 7
    r_data = Reference(ws_inputs, min_col=4, min_row=1, max_row=6)
    r_cats = Reference(ws_inputs, min_col=3, min_row=2, max_row=6)
    radar_chart.add_data(r_data, titles_from_data=True)
    radar_chart.set_categories(r_cats)
    ws_dash.add_chart(radar_chart, "I8")
