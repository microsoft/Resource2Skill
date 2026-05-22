def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.chart import BarChart, LineChart, Reference

    # 1. Create or get Dashboard sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    # 2. Clean App-like Layout
    ws.sheet_view.showGridLines = False
    
    # Simple fallback theme configuration
    primary_color = "003366" if theme == "corporate_blue" else "2A4B7C"
    panel_bg = "F2F2F2"

    # 3. Header Banner (A1:O3)
    ws.merge_cells("A1:O3")
    header_cell = ws["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color="FFFFFF")
    header_cell.fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")
    header_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # 4. Slicer / Control Panel Layout (A5:C30)
    ws.merge_cells("A5:C25")
    panel = ws["A5"]
    panel.value = "Interactive Controls\n\n(Insert Slicers or Timelines Here)"
    panel.font = Font(italic=True, color="7F7F7F")
    panel.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    panel.fill = PatternFill(start_color=panel_bg, end_color=panel_bg, fill_type="solid")
    
    # Add a subtle right border to the panel
    thin_border = Side(border_style="thin", color="CCCCCC")
    for row in range(5, 26):
        ws.cell(row=row, column=3).border = Border(right=thin_border)

    # Set column widths for proper proportions
    for col in ["A", "B", "C"]:
        ws.column_dimensions[col].width = 12
    for col in ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]:
        ws.column_dimensions[col].width = 10

    # 5. Generate Hidden Aggregated Data Sheet
    data_sheet_name = f"{sheet_name}_Data"
    if data_sheet_name in wb.sheetnames:
        ws_data = wb[data_sheet_name]
    else:
        ws_data = wb.create_sheet(data_sheet_name)
    ws_data.sheet_state = 'hidden'

    # Populating Stacked Bar Data (Rows 1-5)
    ws_data.append(["Market", "Chocolate Chip", "Oatmeal Raisin", "Sugar Cookie"])
    ws_data.append(["India", 60000, 20000, 15000])
    ws_data.append(["United States", 35000, 22000, 18000])
    ws_data.append(["United Kingdom", 45000, 15000, 12000])
    ws_data.append(["Philippines", 50000, 18000, 10000])

    ws_data.append([]) # Spacer row 6

    # Populating Trend Line Data (Rows 7-14)
    ws_data.append(["Month", "Units Sold", "Profit"])
    trends = [
        ("Jan", 12000, 45000), ("Feb", 15000, 52000), ("Mar", 18000, 61000),
        ("Apr", 13000, 48000), ("May", 16000, 58000), ("Jun", 20000, 72000), ("Jul", 21000, 75000)
    ]
    for row_data in trends:
        ws_data.append(row_data)

    # 6. Build Stacked Column Chart
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.style = 11
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.height = 14
    bar_chart.width = 16

    bar_data = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    bar_cats = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    bar_chart.add_data(bar_data, titles_from_data=True)
    bar_chart.set_categories(bar_cats)

    # 7. Build Trend Line Chart 1 (Units)
    line_units = LineChart()
    line_units.title = "Units Sold Each Month"
    line_units.style = 13
    line_units.height = 7
    line_units.width = 14
    
    lu_data = Reference(ws_data, min_col=2, min_row=7, max_col=2, max_row=14)
    lu_cats = Reference(ws_data, min_col=1, min_row=8, max_row=14)
    line_units.add_data(lu_data, titles_from_data=True)
    line_units.set_categories(lu_cats)

    # 8. Build Trend Line Chart 2 (Profit)
    line_profit = LineChart()
    line_profit.title = "Profit By Month"
    line_profit.style = 13
    line_profit.height = 7
    line_profit.width = 14
    
    lp_data = Reference(ws_data, min_col=3, min_row=7, max_col=3, max_row=14)
    lp_cats = Reference(ws_data, min_col=1, min_row=8, max_row=14)
    line_profit.add_data(lp_data, titles_from_data=True)
    line_profit.set_categories(lp_cats)

    # 9. Arrange Charts on Dashboard Grid
    ws.add_chart(bar_chart, "E5")
    ws.add_chart(line_units, "K5")
    ws.add_chart(line_profit, "K14")
