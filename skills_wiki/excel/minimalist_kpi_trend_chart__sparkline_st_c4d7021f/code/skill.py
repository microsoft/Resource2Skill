from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties

def render(ws, anchor: str, *, theme: str = "dark_mode", **kwargs) -> None:
    """
    Renders a stripped-down, minimalist line chart intended to act as a stylized sparkline.
    Matches the dark aesthetic trend charts seen in high-end executive dashboards.
    """
    # Define a simple theme palette for demonstration
    palettes = {
        "dark_mode": {"bg": "1A1A1A", "accent": "4A90E2", "text": "FFFFFF"},
        "corporate_blue": {"bg": "FFFFFF", "accent": "0055A4", "text": "000000"}
    }
    palette = palettes.get(theme, palettes["dark_mode"])

    # 1. Write mock data out of view (simulating a dashboard data backend)
    data = [
        ["Month", "Returning Customers"],
        ["Jan", 120], ["Feb", 150], ["Mar", 130], ["Apr", 170],
        ["May", 210], ["Jun", 190], ["Jul", 230], ["Aug", 220],
        ["Sep", 250], ["Oct", 240], ["Nov", 280], ["Dec", 310]
    ]
    
    start_row = 100
    for r_idx, row in enumerate(data, start_row):
        for c_idx, val in enumerate(row, 26):  # Placed in cols Z and AA
            ws.cell(row=r_idx, column=c_idx, value=val)

    # 2. Initialize and size the Line Chart
    chart = LineChart()
    chart.width = 6.0   # Compact width for a KPI tile
    chart.height = 2.5  # Compact height
    chart.legend = None # Remove legend

    # 3. Add references
    dates = Reference(ws, min_col=26, min_row=start_row+1, max_row=start_row+len(data)-1)
    values = Reference(ws, min_col=27, min_row=start_row, max_row=start_row+len(data)-1)
    chart.add_data(values, titles_from_data=True)
    chart.set_categories(dates)

    # 4. Aggressively strip axes and gridlines for the "Sparkline" look
    chart.x_axis.delete = True
    chart.y_axis.delete = True
    chart.y_axis.majorGridlines = None
    chart.x_axis.majorGridlines = None

    # 5. Make chart background and borders transparent
    # This allows the dashboard's overarching dark background to show through
    transparent_props = GraphicalProperties(noFill=True)
    transparent_props.line = LineProperties(noFill=True)
    
    chart.graphical_properties = transparent_props
    chart.plot_area.graphicalProperties = transparent_props

    # 6. Style the data series (Accent line color + Circle markers)
    s1 = chart.series[0]
    
    # Line styling
    s1.graphicalProperties.line.solidFill = palette["accent"]
    s1.graphicalProperties.line.width = 20000  # Slightly thicker line (in EMUs)
    
    # Marker styling (Glowing dot effect)
    s1.marker.symbol = "circle"
    s1.marker.size = 5
    s1.marker.graphicalProperties.solidFill = palette["accent"]
    s1.marker.graphicalProperties.line.solidFill = palette["bg"] # Outline matches background

    # 7. Anchor chart to the dashboard canvas
    ws.add_chart(chart, anchor)
