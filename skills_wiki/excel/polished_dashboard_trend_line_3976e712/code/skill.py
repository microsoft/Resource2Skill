from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.fill import NoFillProperties

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a highly polished, modern trend line chart.
    Features smooth lines, transparent background, custom markers, and a dynamic Y-axis baseline.
    """
    # 1. Inject Sample Data (Monthly Sales Trend 2021 vs 2022)
    data = [
        ["Month", "2021", "2022"],
        ["Jan", 201.9, 215.3],
        ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1],
        ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3],
        ["Jun", 195.1, 203.0],
        ["Jul", 192.4, 201.5],
        ["Aug", 186.3, 200.6],
        ["Sep", 194.2, 210.6],
        ["Oct", 201.5, 218.4],
        ["Nov", 205.2, 222.3],
        ["Dec", 204.3, 225.8]
    ]
    
    # Place data dynamically based on current sheet usage
    start_row = ws.max_row + 2 if ws.max_row > 1 else 1
    start_col = 1
    
    for r_idx, row in enumerate(data, start=start_row):
        for c_idx, val in enumerate(row, start=start_col):
            ws.cell(row=r_idx, column=c_idx, value=val)

    # 2. Initialize and Configure Chart
    chart = LineChart()
    chart.title = None  # Rely on external dashboard container for the title
    chart.legend.position = "t" # Move legend to top to save horizontal space
    chart.width = 16
    chart.height = 8
    
    # Emphasize variance by lifting the Y-axis baseline (min 180 instead of 0)
    chart.y_axis.scaling.min = 180
    chart.y_axis.scaling.max = 230
    chart.y_axis.majorGridlines = None # Clean look, removing default gridlines
    
    # 3. Strip Chart Background & Border (Make Transparent)
    chart.graphical_properties = GraphicalProperties(
        solidFill=NoFillProperties(),
        line=LineProperties(noFill=True)
    )

    # 4. Attach Data References
    cats = Reference(ws, min_col=start_col, min_row=start_row+1, max_row=start_row+len(data)-1)
    data_ref = Reference(ws, min_col=start_col+1, max_col=start_col+2, min_row=start_row, max_row=start_row+len(data)-1)
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats)

    # 5. Apply Polished Series Formatting
    # Hardcoded to video's aesthetic, but designed to accept theme colors
    colors = ["C00000", "002060"] # Red, Dark Blue
    
    for i, series in enumerate(chart.series):
        color_hex = colors[i % len(colors)]
        
        # Smooth line interpolation
        series.smooth = True
        
        # Bold line width and color
        series.graphicalProperties.line.solidFill = color_hex
        series.graphicalProperties.line.width = 25000  # ~2pt thickness
        
        # Custom "Hollow" Markers
        series.marker.symbol = "circle"
        series.marker.size = 6
        series.marker.graphicalProperties.solidFill = "FFFFFF" # White inner fill
        series.marker.graphicalProperties.line.solidFill = color_hex # Border matches line color
        series.marker.graphicalProperties.line.width = 15000  # ~1.2pt border thickness

    # Inject chart at target anchor
    ws.add_chart(chart, anchor)
