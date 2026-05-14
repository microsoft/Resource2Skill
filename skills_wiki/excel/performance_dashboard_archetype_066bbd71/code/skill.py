def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Font, PatternFill, Alignment

    # Realistic sample data (pre-aggregated since openpyxl does not generate PivotTables)
    stacked_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62349, 4872, 21028, 25085],
        ["Philippines", 54618, 7026, 22005, 8313],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["United States", 36657, 6369, 22260, 9938]
    ]

    line1_data = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970]
    ]

    line2_data = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337]
    ]

    # Theme handling fallback
    palette = {
        "corporate_blue": {"header_bg": "203764", "header_fg": "FFFFFF"},
        "emerald_green": {"header_bg": "005A36", "header_fg": "FFFFFF"},
        "slate_gray": {"header_bg": "2F353B", "header_fg": "FFFFFF"},
    }
    th = palette.get(theme, palette["corporate_blue"])

    # 1. Setup Hidden Data Sheet
    ws_data = wb.active
    ws_data.title = "ChartData"
    
    # Write Stacked Data (Format as Currency)
    for row in stacked_data:
        ws_data.append(row)
        
    for r in range(2, len(stacked_data) + 1):
        for c in range(2, len(stacked_data[0]) + 1):
            ws_data.cell(row=r, column=c).number_format = '"$"#,##0'
            
    ws_data.append([]) # spacer row
    
    # Write Line 1 Data (Format as integer with commas)
    start_line1 = ws_data.max_row + 1
    for row in line1_data:
        ws_data.append(row)
        
    for r in range(start_line1 + 1, start_line1 + len(line1_data)):
        ws_data.cell(row=r, column=2).number_format = '#,##0'

    ws_data.append([]) # spacer row
    
    # Write Line 2 Data (Format as Currency)
    start_line2 = ws_data.max_row + 1
    for row in line2_data:
        ws_data.append(row)

    for r in range(start_line2 + 1, start_line2 + len(line2_data)):
        ws_data.cell(row=r, column=2).number_format = '"$"#,##0'

    # Hide the data sheet to keep focus on the dashboard
    ws_data.sheet_state = 'hidden'

    # 2. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    # Header styling
    for row in ws_dash.iter_rows(min_row=1, max_row=3, min_col=1, max_col=16):
        for cell in row:
            cell.fill = PatternFill(start_color=th["header_bg"], end_color=th["header_bg"], fill_type="solid")
            
    ws_dash.merge_cells("A1:P3")
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color=th["header_fg"])
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Create Charts
    
    # Chart 1: Stacked Bar
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    data1 = Reference(ws_data, min_col=2, min_row=1, max_col=len(stacked_data[0]), max_row=len(stacked_data))
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=len(stacked_data))
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    chart1.width = 16
    chart1.height = 11
    ws_dash.add_chart(chart1, "B5")

    # Chart 2: Units Sold (Line)
    chart2 = LineChart()
    chart2.style = 10
    chart2.title = "Units sold each month"
    chart2.legend = None
    data2 = Reference(ws_data, min_col=2, min_row=start_line1, max_col=2, max_row=start_line1 + len(line1_data) - 1)
    cats2 = Reference(ws_data, min_col=1, min_row=start_line1 + 1, max_row=start_line1 + len(line1_data) - 1)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.width = 13
    chart2.height = 5.5
    ws_dash.add_chart(chart2, "J5")

    # Chart 3: Profit (Line)
    chart3 = LineChart()
    chart3.style = 10
    chart3.title = "Profit by month"
    chart3.legend = None
    data3 = Reference(ws_data, min_col=2, min_row=start_line2, max_col=2, max_row=start_line2 + len(line2_data) - 1)
    cats3 = Reference(ws_data, min_col=1, min_row=start_line2 + 1, max_row=start_line2 + len(line2_data) - 1)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    chart3.width = 13
    chart3.height = 5.5
    ws_dash.add_chart(chart3, "J17")

    # Set focus onto the dashboard for opening
    wb.active = ws_dash
