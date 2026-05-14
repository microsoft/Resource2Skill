def render(ws, anchor: str, *, kpi_name: str = "Sales Target", actual: float = 0.85, target: float = 1.0, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import DoughnutChart, Reference
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.line import LineProperties
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
    
    # Parse anchor coordinates
    xy = coordinate_from_string(anchor)
    col = column_index_from_string(xy[0])
    row = xy[1]
    
    # 1. Setup Data for the Doughnut (Actual vs Remainder)
    data_matrix = [
        ["Metric", "Value"],
        ["Actual", actual],
        ["Remainder", max(0, target - actual)]
    ]
    
    for r_idx, row_data in enumerate(data_matrix):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=row + r_idx, column=col + c_idx, value=val)
            if r_idx > 0 and c_idx == 1:
                cell.number_format = '0%'
                
    # 2. Configure the Doughnut Chart
    chart = DoughnutChart()
    chart.title = kpi_name
    chart.style = 10  # Standard clean style preset
    
    # Set modern ring thickness (lowering hole size makes the donut thicker)
    chart.holeSize = 65  
    
    # Clean up clutter for dashboard embedding
    chart.has_legend = False
    
    # Remove chart area borders/fills so it floats cleanly on the dashboard background
    chart.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    
    # 3. Bind Data
    cats = Reference(ws, min_col=col, min_row=row+1, max_row=row+2)
    data = Reference(ws, min_col=col+1, min_row=row, max_row=row+2)
    
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    
    # 4. Insert Chart slightly below the data matrix
    ws.add_chart(chart, f"{xy[0]}{row + 4}")
