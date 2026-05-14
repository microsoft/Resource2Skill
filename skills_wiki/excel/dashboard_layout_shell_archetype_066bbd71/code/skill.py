def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.worksheet.table import Table, TableStyleInfo

    # Mock Theme Colors
    header_bg = "1E3A8A"  # Dark Blue
    header_fg = "FFFFFF"  # White

    # 1. Setup Dashboard Sheet
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False

    # Create Header Banner
    for row in range(1, 4):
        for col in range(1, 20):
            ws_dash.cell(row=row, column=col).fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")

    title_cell = ws_dash['B2']
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=header_fg)
    ws_dash.merge_cells('B2:J3')
    title_cell.alignment = Alignment(vertical="center")

    # 2. Setup Raw Data Sheet
    ws_data = wb.create_sheet("Data")
    headers = ["Date", "Market", "Product", "Units Sold", "Profit"]
    ws_data.append(headers)
    
    raw_data = [
        ["2020-09-01", "India", "Chocolate Chip", 1200, 6000],
        ["2020-09-15", "USA", "Fortune Cookie", 800, 3200],
        ["2020-10-05", "India", "Chocolate Chip", 1500, 7500],
        ["2020-10-20", "UK", "Oatmeal Raisin", 950, 4100],
    ]
    for row in raw_data:
        ws_data.append(row)

    # Format as Excel Table
    tab = Table(displayName="RawData", ref=f"A1:E{len(raw_data) + 1}")
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)

    # 3. Setup Hidden Calc Sheet for Charts
    ws_calc = wb.create_sheet("CalcData")

    # Stacked Bar Data (Profit by Market & Cookie)
    calc_data_bar = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 60000, 20000, 15000],
        ["USA", 45000, 10000, 25000],
        ["UK", 30000, 15000, 10000],
    ]
    for row in calc_data_bar:
        ws_calc.append(row)

    ws_calc.append([]) # spacer

    # Line Chart Data (Units over time)
    calc_data_line = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50000, 124000],
        ["Oct", 95000, 228000],
        ["Nov", 65000, 160000],
        ["Dec", 52000, 136000],
    ]
    for row in calc_data_line:
        ws_calc.append(row)

    # Hide the calculation sheet
    ws_calc.sheet_state = 'hidden'

    # 4. Generate and Place Charts on Dashboard
    
    # Chart 1: Stacked Bar (Profit by Market)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.height = 10
    bar_chart.width = 15
    bar_chart.y_axis.majorGridlines = None # Clean look
    
    data_bar = Reference(ws_calc, min_col=2, max_col=4, min_row=1, max_row=4)
    cats_bar = Reference(ws_calc, min_col=1, min_row=2, max_row=4)
    bar_chart.add_data(data_bar, titles_from_data=True)
    bar_chart.set_categories(cats_bar)
    ws_dash.add_chart(bar_chart, "B5")

    # Chart 2: Line Chart (Units Sold)
    line_chart1 = LineChart()
    line_chart1.title = "Units sold each month"
    line_chart1.height = 7
    line_chart1.width = 12
    line_chart1.legend = None # Clean look
    line_chart1.y_axis.majorGridlines = None
    
    data_line1 = Reference(ws_calc, min_col=2, min_row=7, max_row=10)
    cats_line = Reference(ws_calc, min_col=1, min_row=8, max_row=10)
    line_chart1.add_data(data_line1, titles_from_data=True)
    line_chart1.set_categories(cats_line)
    ws_dash.add_chart(line_chart1, "J5")

    # Chart 3: Line Chart (Profit)
    line_chart2 = LineChart()
    line_chart2.title = "Profit by month"
    line_chart2.height = 7
    line_chart2.width = 12
    line_chart2.legend = None
    line_chart2.y_axis.majorGridlines = None
    
    data_line2 = Reference(ws_calc, min_col=3, min_row=7, max_row=10)
    line_chart2.add_data(data_line2, titles_from_data=True)
    line_chart2.set_categories(cats_line)
    ws_dash.add_chart(line_chart2, "J13")
