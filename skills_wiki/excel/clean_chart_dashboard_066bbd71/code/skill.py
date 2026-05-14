def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    
    # Standard theme palette fallback
    themes = {
        "corporate_blue": {"primary": "203764", "text": "FFFFFF"},
        "executive_dark": {"primary": "262626", "text": "FFFFFF"},
        "forest_green": {"primary": "375623", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # 1. Setup Data Sheet
    ws_data = wb.active
    ws_data.title = "Data"
    
    headers = ["Month", "Revenue", "Profit", "Units"]
    data = [
        ["Jan", 120000, 30000, 5000],
        ["Feb", 135000, 35000, 5500],
        ["Mar", 150000, 42000, 6000],
        ["Apr", 145000, 38000, 5800],
        ["May", 160000, 48000, 6500],
        ["Jun", 180000, 55000, 7200],
        ["Jul", 175000, 52000, 7000],
        ["Aug", 190000, 60000, 7800],
        ["Sep", 210000, 68000, 8500],
        ["Oct", 205000, 65000, 8200],
        ["Nov", 230000, 75000, 9500],
        ["Dec", 250000, 85000, 10500]
    ]
    
    ws_data.append(headers)
    for row in data:
        ws_data.append(row)
        
    # 2. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    # Title Banner
    ws_dash.merge_cells("A1:R3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["text"])
    title_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Expand banner height to make it prominent
    for i in range(1, 4):
        ws_dash.row_dimensions[i].height = 20
        
    # Add a thin spacing margin on the left
    ws_dash.column_dimensions['A'].width = 4
    
    # 3. Create Aligned Charts
    cats_ref = Reference(ws_data, min_col=1, min_row=2, max_row=len(data)+1)
    
    # Chart A: Revenue & Profit (Clustered Bar)
    bar_chart = BarChart()
    bar_chart.title = "Revenue and Profit by Month"
    bar_chart.style = 10
    
    data_ref_financials = Reference(ws_data, min_col=2, max_col=3, min_row=1, max_row=len(data)+1)
    bar_chart.add_data(data_ref_financials, titles_from_data=True)
    bar_chart.set_categories(cats_ref)
    
    # Standardize dimensions for grid alignment
    bar_chart.height = 12
    bar_chart.width = 18
    ws_dash.add_chart(bar_chart, "B5")
    
    # Chart B: Units Sold (Line Chart)
    line_chart = LineChart()
    line_chart.title = "Units Sold Trend"
    line_chart.style = 13
    
    data_ref_units = Reference(ws_data, min_col=4, min_row=1, max_row=len(data)+1)
    line_chart.add_data(data_ref_units, titles_from_data=True)
    line_chart.set_categories(cats_ref)
    
    # Standardize dimensions for grid alignment
    line_chart.height = 12
    line_chart.width = 18
    ws_dash.add_chart(line_chart, "K5")
