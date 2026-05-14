```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Line Chart

* **Tier**: component
* **Core Mechanism**: Constructs a highly stylized line chart optimized for custom dashboards. It strips away default backgrounds, borders, and gridlines to blend seamlessly with the underlying sheet. Data markers are styled with a fill matching the line color and a border matching the dashboard background, creating a professional "cutout" effect. Y-axis numbers are formatted to show "K" for thousands.
* **Applicability**: Use when integrating trend lines into a custom-designed dashboard where standard Excel chart containers look out of place. Perfect for monthly performance metrics like sales, visitors, or customer rates.

### 2. Structural Breakdown

- **Data Layout**: Time-series data in adjacent columns (e.g., Month, Value), typically placed on a hidden calculation sheet or drawn directly from a PivotTable.
- **Formula Logic**: N/A (Chart rendering relies on openpyxl `Reference` objects pointing to the data).
- **Visual Design**: Transparent chart and plot areas to allow the dashboard background to show through. Smooth lines with elevated thickness for modern aesthetics.
- **Charts/Tables**: `LineChart` with custom markers (`circle` symbol, color-matched fill, background-matched border). Removed legend, title, and gridlines.
- **Theme Hooks**: Consumes a background color (`bg_hex`) for the marker borders (to simulate transparency) and an accent color (`accent_hex`) for the primary line and marker fill.

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import LineChart, Reference
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.line import LineProperties
    from openpyxl.chart.marker import Marker
    
    # Colors (Simulating a dark dashboard theme palette)
    # In a full framework, these would be injected via the 'theme' parameter
    bg_hex = "1E1E1E"     # Dashboard background color
    accent_hex = "5B9BD5" # Primary line color
    
    # 1. Setup sample data (typically placed on a separate calculation sheet)
    data = [
        ["Month", "Sales"],
        ["Jan", 4500], ["Feb", 5200], ["Mar", 4800], ["Apr", 6100],
        ["May", 5900], ["Jun", 7500], ["Jul", 8200], ["Aug", 7900],
        ["Sep", 8500], ["Oct", 9100], ["Nov", 9800], ["Dec", 10500],
    ]
    
    data_start_row = 100
    data_start_col = 26 # Column Z
    for r_idx, row_data in enumerate(data, start=data_start_row):
        for c_idx, value in enumerate(row_data, start=data_start_col):
            ws.cell(row=r_idx, column=c_idx, value=value)
            
    # 2. Create Chart
    chart = LineChart()
    chart.title = None  # Clean look; titles are usually handled via external stylized text boxes
    chart.legend = None # Remove legend for single-series KPI charts
    chart.width = 14
    chart.height = 5
    
    data_ref = Reference(ws, min_col=data_start_col+1, min_row=data_start_row, max_row=data_start_row+12)
    cats_ref = Reference(ws, min_col=data_start_col, min_row=data_start_row+1, max_row=data_start_row+12)
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    
    # 3. Apply Custom Dashboard Formatting
    
    # Remove chart area background and border
    chart.graphical_properties = GraphicalProperties(noFill=True)
    chart.graphical_properties.line = LineProperties(noFill=True)
    
    # Remove plot area background and border
    chart.plot_area.graphicalProperties = GraphicalProperties(noFill=True)
    chart.plot_area.graphicalProperties.line = LineProperties(noFill=True)
    
    # Remove gridlines for a cleaner look
    chart.y_axis.majorGridlines = None
    
    # Custom Number Formatting for Y Axis (e.g., "5K" instead of "5000")
    chart.y_axis.numFmt = '[>=1000]#,##0,"K";0'
    
    # 4. Style the Series
    s1 = chart.series[0]
    
    # Set line color, thickness, and smoothing
    s1.graphicalProperties.line = LineProperties(solidFill=accent_hex, width=25000) # ~2 pt
    s1.smooth = True
    
    # Setup markers to create a 'cutout' effect
    s1.marker = Marker(symbol="circle", size=5)
    s1.marker.graphicalProperties.solidFill = accent_hex
    # The marker border matches the dashboard background to visually "cut" into the line
    s1.marker.graphicalProperties.line = LineProperties(solidFill=bg_hex, width=15000) # ~1.2 pt
    
    # Add chart to sheet
    ws.add_chart(chart, anchor)
```
```