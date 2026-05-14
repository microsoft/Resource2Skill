def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    
    # Hardcoded fallback theme colors representing "corporate_blue"
    banner_bg = "203764"  # Dark Blue
    banner_fg = "FFFFFF"  # White
    
    # 1. Prepare Dashboard Presentation Sheet
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    
    # Disable gridlines to create a clean "canvas" look
    ws_dash.sheet_view.showGridLines = False
    
    # Create Title Banner
    ws_dash.merge_cells("A1:T3")
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color=banner_fg)
    header_cell.fill = PatternFill(start_color=banner_bg, end_color=banner_bg, fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 2. Prepare Hidden Calculation Sheet
    # Because openpyxl cannot create PivotTables, we write pre-aggregated data here.
    ws_calc = wb.create_sheet("Calculation")
    ws_calc.sheet_state = "hidden"
    
    # Write aggregated data for Stacked Column Chart
    stacked_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"],
        ["India", 62349, 4872, 21028, 25085],
        ["Philippines", 54618, 7026, 22005, 8313],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["United States", 36657, 6368, 22260, 9937]
    ]
    for row in stacked_data:
        ws_calc.append(row)
        
    # Write aggregated data for Units Sold Line Chart
    ws_calc.append([])
    row_offset_units = ws_calc.max_row + 1
    units_data = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970]
    ]
    for row in units_data:
        ws_calc.append(row)
        
    # Write aggregated data for Profit Line Chart
    ws_calc.append([])
    row_offset_profit = ws_calc.max_row + 1
    profit_data = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337]
    ]
    for row in profit_data:
        ws_calc.append(row)
        
    # 3. Build Main Stacked Column Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.height = 14
    chart1.width = 16
    chart1.y_axis.number_format = '$#,##0'
    
    data_ref1 = Reference(ws_calc, min_col=2, min_row=1, max_col=5, max_row=5)
    cats_ref1 = Reference(ws_calc, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data_ref1, titles_from_data=True)
    chart1.set_categories(cats_ref1)
    
    # Place on Dashboard
    ws_dash.add_chart(chart1, "B5")
    
    # 4. Build Top Right Line Chart
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.height = 6.5
    chart2.width = 14
    chart2.legend = None  # Hide legend for a cleaner, single-metric look
    
    data_ref2 = Reference(ws_calc, min_col=2, min_row=row_offset_units, max_row=row_offset_units+4)
    cats_ref2 = Reference(ws_calc, min_col=1, min_row=row_offset_units+1, max_row=row_offset_units+4)
    chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(cats_ref2)
    
    # Place on Dashboard aligned to the right
    ws_dash.add_chart(chart2, "K5")
    
    # 5. Build Bottom Right Line Chart
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.height = 6.5
    chart3.width = 14
    chart3.legend = None
    chart3.y_axis.number_format = '$#,##0'
    
    data_ref3 = Reference(ws_calc, min_col=2, min_row=row_offset_profit, max_row=row_offset_profit+4)
    cats_ref3 = Reference(ws_calc, min_col=1, min_row=row_offset_profit+1, max_row=row_offset_profit+4)
    chart3.add_data(data_ref3, titles_from_data=True)
    chart3.set_categories(cats_ref3)
    
    # Place directly beneath the first line chart
    ws_dash.add_chart(chart3, "K16")
