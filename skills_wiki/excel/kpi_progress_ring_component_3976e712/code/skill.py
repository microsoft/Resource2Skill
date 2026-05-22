def render(ws, anchor: str, title: str = "Sales Revenue", actual: float = 2544, target: float = 3000, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font
    from openpyxl.chart import DoughnutChart, Reference
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter

    col_str, row = coordinate_from_string(anchor)
    col_idx = column_index_from_string(col_str)

    # 1. KPI Text Block
    ws.cell(row=row, column=col_idx, value=title).font = Font(bold=True, size=12, color="595959")
    
    val_cell = ws.cell(row=row+1, column=col_idx, value=actual)
    val_cell.font = Font(bold=True, size=24, color="1F4E78")
    val_cell.number_format = "$#,##0"

    pct_display = ws.cell(row=row+2, column=col_idx, value=f"={col_str}{row+1}/{target}")
    pct_display.font = Font(bold=True, size=14, color="1F4E78")
    pct_display.number_format = "0% Complete"

    tgt_cell = ws.cell(row=row+3, column=col_idx, value=f"Target: ${target:,.0f}")
    tgt_cell.font = Font(italic=True, size=10, color="808080")

    # 2. Progress Data (Hidden chart source data)
    data_row = row + 5
    ws.cell(row=data_row, column=col_idx, value="% Complete")
    ws.cell(row=data_row+1, column=col_idx, value="% Remainder")
    
    pct_calc = ws.cell(row=data_row, column=col_idx+1, value=f"={col_str}{row+2}")
    pct_calc.number_format = "0%"
    
    rem_calc = ws.cell(row=data_row+1, column=col_idx+1, value=f"=1-{get_column_letter(col_idx+1)}{data_row}")
    rem_calc.number_format = "0%"

    # Hide the calculation data by blending with the default white background
    for r in range(data_row, data_row+2):
        for c in range(col_idx, col_idx+2):
            ws.cell(row=r, column=c).font = Font(color="FFFFFF")

    # 3. Doughnut Chart for Progress Ring
    chart = DoughnutChart()
    chart.holeSize = 75  # Thick ring style
    chart.width = 4.0
    chart.height = 4.0
    
    labels = Reference(ws, min_col=col_idx, min_row=data_row, max_row=data_row+1)
    data = Reference(ws, min_col=col_idx+1, min_row=data_row, max_row=data_row+1)
    
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(labels)
    
    # Styling: Remove legend and border for seamless dashboard integration
    chart.legend = None
    chart.graphical_properties.line.noFill = True
    
    # Position the chart to the right of the text block
    chart_anchor = f"{get_column_letter(col_idx+2)}{row}"
    ws.add_chart(chart, chart_anchor)
