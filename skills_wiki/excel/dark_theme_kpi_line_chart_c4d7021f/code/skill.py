from openpyxl.chart import LineChart, Reference
from openpyxl.chart.marker import Marker
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a dark-theme ready Line Chart.
    The chart is made completely transparent to float over dark sheet backgrounds.
    """
    # 1. Inject sample data (Months and Sales)
    data = [
        ["Month", "Sales"],
        ["Jan", 124000],
        ["Feb", 145000],
        ["Mar", 132000],
        ["Apr", 168000],
        ["May", 155000],
        ["Jun", 192000],
        ["Jul", 205000]
    ]
    
    # Write data to a secluded area (e.g., columns AA:AB)
    start_row = 1
    start_col = 27 
    for r_idx, row_data in enumerate(data, start_row):
        for c_idx, val in enumerate(row_data, start_col):
            ws.cell(row=r_idx, column=c_idx, value=val)

    # 2. Initialize the Line Chart
    chart = LineChart()
    chart.title = None
    chart.legend = None
    chart.width = 12
    chart.height = 4.5

    # 3. Bind the Data
    vals = Reference(ws, min_col=start_col+1, min_row=start_row, max_row=start_row+len(data)-1)
    cats = Reference(ws, min_col=start_col, min_row=start_row+1, max_row=start_row+len(data)-1)
    chart.add_data(vals, titles_from_data=True)
    chart.set_categories(cats)

    # 4. Format Chart Area & Plot Area for Dark Theme 
    # (Removes the white background and border to float over dark cells)
    chart.graphical_properties = GraphicalProperties(noFill=True)
    chart.graphical_properties.line.noFill = True
    chart.plot_area.graphical_properties = GraphicalProperties(noFill=True)
    chart.plot_area.graphical_properties.line.noFill = True

    # 5. Clean up Axes and Gridlines
    chart.y_axis.majorGridlines = None
    chart.x_axis.majorGridlines = None
    
    # Remove the actual axis boundary lines (spines)
    chart.y_axis.spPr = GraphicalProperties(line=LineProperties(noFill=True))
    chart.x_axis.spPr = GraphicalProperties(line=LineProperties(noFill=True))

    # Apply custom K-formatting (Thousands) to the Y-axis to save space
    chart.y_axis.numFmt = '#,##0,"K"'

    # 6. Format the Data Series
    s1 = chart.series[0]
    
    # Add circular markers to the line points
    s1.marker = Marker(symbol="circle", size=4)
    # The line and marker colors can be customized via s1.graphicalProperties.line.solidFill 
    # but require deeper XML manipulation in openpyxl for exact hex matching.

    # 7. Anchor the chart to the dashboard
    ws.add_chart(chart, anchor)
