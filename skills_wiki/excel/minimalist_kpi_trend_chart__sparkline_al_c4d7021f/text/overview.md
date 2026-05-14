### 1. High-level Skill Pattern Extraction

> **Skill Name**: Minimalist KPI Trend Chart (Sparkline Alternative)

* **Tier**: component
* **Core Mechanism**: Transforms a standard Excel line chart into a clean, noise-free trend visualization. Programmatically strips away structural elements (gridlines, X/Y axes, tick marks, legends, and chart borders) using `GraphicalProperties` and empty string properties. Enhances the bare line with theme-driven colors and circular markers to create a modern dashboard component.
* **Applicability**: Ideal for dense executive dashboards and KPI cards where visualizing the trend direction is critical, but a full coordinate system takes up too much space or visual weight.

### 2. Structural Breakdown

- **Data Layout**: References a 1D vertical array of continuous metric values (e.g., 12 months of sales data).
- **Formula Logic**: None required (relies purely on chart plotting logic).
- **Visual Design**: Uses dark mode styling (or light mode depending on theme) by filling the cells behind the chart to highlight the chart's structural transparency.
- **Charts/Tables**: `LineChart` configured with `legend = None`, `majorGridlines = None`, and `tickLblPos = "none"`. Custom `Marker` objects overlay the line data points.
- **Theme Hooks**: Consumes `accent` for the primary trend line and marker fill, `bg` for the underlying cell background, and `marker_border` for the contrast ring around data points.

### 3. Reproduction Code

```python
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import Line
from openpyxl.chart.marker import Marker
from openpyxl.styles import PatternFill

def render(ws, anchor: str, *, title: str = "Trend", data: list = None, theme: str = "dark_neon", **kwargs) -> None:
    # 1. Theme Configuration
    theme_palettes = {
        "corporate_blue": {"bg": "FFFFFF", "accent": "4F81BD", "marker_border": "FFFFFF"},
        "dark_neon": {"bg": "1A1A1A", "accent": "00FFCC", "marker_border": "1A1A1A"},
    }
    palette = theme_palettes.get(theme, theme_palettes["dark_neon"])

    # 2. Realistic Default Data
    if not data:
        data = [129129, 131450, 128000, 142000, 156000, 161200, 
                158000, 175000, 189000, 186500, 210000, 235000]

    # Write data to a safe, hidden column (e.g., column ZZ) so the chart is self-contained
    start_row = 1000
    start_col = 700 
    for i, val in enumerate(data):
        ws.cell(row=start_row + i, column=start_col, value=val)

    # 3. Chart Initialization
    chart = LineChart()
    chart.title = None
    chart.legend = None
    chart.height = 4.0  # cm (compact height for KPI cards)
    chart.width = 10.0  # cm

    # 4. Data Binding
    values = Reference(ws, min_col=start_col, min_row=start_row, max_row=start_row + len(data) - 1)
    chart.add_data(values)

    # 5. Line and Marker Styling
    s1 = chart.series[0]
    s1.graphicalProperties.line.solidFill = palette["accent"]
    s1.graphicalProperties.line.width = 25000  # Thicker line (measured in EMUs)

    s1.marker = Marker(symbol="circle", size=5)
    s1.marker.graphicalProperties.solidFill = palette["accent"]
    s1.marker.graphicalProperties.line.solidFill = palette["marker_border"]
    s1.marker.graphicalProperties.line.width = 15000

    # 6. Noise Removal (Axes & Gridlines)
    # Hide X Axis
    chart.x_axis.tickLblPos = "none"
    chart.x_axis.majorTickMark = "none"
    chart.x_axis.minorTickMark = "none"
    chart.x_axis.spPr = GraphicalProperties(ln=Line(noFill=True))

    # Hide Y Axis & Gridlines
    chart.y_axis.tickLblPos = "none"
    chart.y_axis.majorTickMark = "none"
    chart.y_axis.minorTickMark = "none"
    chart.y_axis.spPr = GraphicalProperties(ln=Line(noFill=True))
    chart.y_axis.majorGridlines = None

    # Remove chart border to make it float seamlessly
    chart.spPr = GraphicalProperties(ln=Line(noFill=True))

    # 7. Placement and Background Styling
    ws.add_chart(chart, anchor)

    # Optional: Fill the cells behind the chart to complete the component look
    anchor_cell = ws[anchor]
    bg_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    
    for r in range(anchor_cell.row, anchor_cell.row + 9):
        for c in range(anchor_cell.column, anchor_cell.column + 6):
            ws.cell(row=r, column=c).fill = bg_fill
```