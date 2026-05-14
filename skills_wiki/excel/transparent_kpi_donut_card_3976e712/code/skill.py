def render(ws, anchor: str, *, kpi_name: str = "Sales Progress", actual: float = 85, target: float = 100, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import DoughnutChart, Reference
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.line import LineProperties
    from openpyxl.chart.series import DataPoint
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter
    from openpyxl.styles import Font, Alignment

    anchor_col_letter, anchor_row = coordinate_from_string(anchor)
    col_idx = column_index_from_string(anchor_col_letter)
    
    # 1. Setup the background cell for the center text
    # Merge a 3x6 area to serve as the chart's footprint
    end_col_letter = get_column_letter(col_idx + 2)
    end_row = anchor_row + 5
    ws.merge_cells(f"{anchor_col_letter}{anchor_row}:{end_col_letter}{end_row}")
    
    primary_color = "1F4E78" # Fallback primary; in a full system, pull from theme palette
    remainder_color = "D9D9D9"
    
    kpi_cell = ws[anchor]
    kpi_cell.value = actual / target if target else 0
    kpi_cell.number_format = "0%"
    kpi_cell.font = Font(size=18, bold=True, color=primary_color)
    kpi_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 2. Write chart data to hidden offset cells
    data_col = col_idx + 10
    data_row = anchor_row
    remainder = max(0, target - actual)
    
    ws.cell(row=data_row, column=data_col, value="Actual")
    ws.cell(row=data_row+1, column=data_col, value="Remainder")
    ws.cell(row=data_row, column=data_col+1, value=actual)
    ws.cell(row=data_row+1, column=data_col+1, value=remainder)

    # 3. Initialize and configure Doughnut Chart
    chart = DoughnutChart()
    chart.title = None
    chart.legend = None
    chart.holeSize = 65  # Enlarged hole for text visibility
    
    data = Reference(ws, min_col=data_col+1, min_row=data_row, max_row=data_row+1)
    labels = Reference(ws, min_col=data_col, min_row=data_row, max_row=data_row+1)
    
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(labels)
    
    # 4. Make chart and plot areas fully transparent
    chart.graphical_properties = GraphicalProperties(noFill=True)
    chart.graphical_properties.line = LineProperties(noFill=True)
    chart.plot_area.graphicalProperties = GraphicalProperties(noFill=True)
    chart.plot_area.graphicalProperties.line = LineProperties(noFill=True)
    
    # 5. Format slice colors
    dp0 = DataPoint(idx=0)
    dp0.graphicalProperties = GraphicalProperties(solidFill=primary_color)
    dp0.graphicalProperties.line = LineProperties(noFill=True)
    
    dp1 = DataPoint(idx=1)
    dp1.graphicalProperties = GraphicalProperties(solidFill=remainder_color)
    dp1.graphicalProperties.line = LineProperties(noFill=True)
    
    chart.series[0].dp = [dp0, dp1]
    
    # 6. Position chart over the merged background
    chart.anchor = anchor
    chart.width = 5   # cm
    chart.height = 5  # cm
    
    ws.add_chart(chart)
