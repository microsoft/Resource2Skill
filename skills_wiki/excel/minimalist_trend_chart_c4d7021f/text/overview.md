```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Minimalist Trend Chart

* **Tier**: component
* **Core Mechanism**: Converts a standard line chart into a sleek, UI-friendly "sparkline" by stripping away all traditional chart furniture (axes, legend, title, and chart area borders). It applies line smoothing, custom line weights, and tailored circular markers to emphasize the data trend.
* **Applicability**: Ideal for executive dashboards, KPI panels, and "small multiples" where screen real estate is limited and visual clutter must be minimized to focus purely on the trend trajectory. 

### 2. Structural Breakdown

- **Data Layout**: Requires a hidden or separate contiguous 2D range (categories and values).
- **Formula Logic**: None required; relies on direct chart references.
- **Visual Design**: Chart border is removed using `noFill=True` on `LineProperties`. Axes and legend are explicitly deleted.
- **Charts/Tables**: `LineChart` configured with `series.smooth = True` and circle markers with specific line/fill colors to contrast against a dashboard background.
- **Theme Hooks**: Primary accent color is applied to the series line and marker borders. Background color is applied to the marker fill for a "hollow" effect.

### 3. Reproduction Code

```python
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a sleek, borderless trend line chart stripped of axes and legends,
    perfect for KPI dashboard panels.
    """
    # 1. Inject sample trend data (typically hidden on a separate calc sheet)
    start_row = 100 
    data = [
        ("Jan", 154), ("Feb", 182), ("Mar", 168), 
        ("Apr", 215), ("May", 195), ("Jun", 240),
        ("Jul", 220), ("Aug", 260), ("Sep", 280)
    ]
    
    for i, (month, val) in enumerate(data):
        ws.cell(row=start_row + i, column=1, value=month)
        ws.cell(row=start_row + i, column=2, value=val)
        
    data_ref = Reference(ws, min_col=2, min_row=start_row, max_row=start_row + len(data) - 1)
    cats_ref = Reference(ws, min_col=1, min_row=start_row, max_row=start_row + len(data) - 1)
    
    # 2. Build the Line Chart
    chart = LineChart()
    chart.add_data(data_ref)
    chart.set_categories(cats_ref)
    
    # 3. Strip all standard UI elements for a minimalist look
    chart.title = None
    chart.legend = None
    chart.x_axis.delete = True
    chart.y_axis.delete = True
    
    # Remove the outer chart area border
    chart.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    
    # 4. Style the trend line and markers
    series = chart.series[0]
    series.smooth = True  # Creates a bezier-curve style smooth line
    
    # Theme hook: Primary Accent Color (e.g., Purple/Blue)
    accent_hex = "8E44AD"
    bg_hex = "1A1A1A" # Dashboard background color for marker fill
    
    series.graphicalProperties.line.solidFill = accent_hex
    series.graphicalProperties.line.width = 25000  # ~2.5 pt width
    
    # Add custom circular markers
    series.marker.symbol = "circle"
    series.marker.size = 5
    # Hollow effect: fill matches background, border matches line
    series.marker.graphicalProperties.solidFill = bg_hex
    series.marker.graphicalProperties.line.solidFill = accent_hex
    series.marker.graphicalProperties.line.width = 15000
    
    # 5. Compress dimensions to fit KPI card context
    chart.width = 8.0   # cm
    chart.height = 3.5  # cm
    
    ws.add_chart(chart, anchor)
```
```