```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Minimalist KPI Trend Card

* **Tier**: component
* **Core Mechanism**: Constructs a self-contained KPI card pairing a bold summary metric with a minimalist, sparkline-style trend chart. It transforms a standard line chart by systematically stripping all default elements (axes, gridlines, legends, borders) and applying a thickened, smoothed line to maximize the data-ink ratio in tight spaces.
* **Applicability**: Ideal for executive dashboards and reports where multiple high-level trends (e.g., Monthly Sales, Conversion Rates, Traffic Sources) must be displayed compactly alongside their total values, without the visual clutter of full axes.

### 2. Structural Breakdown

- **Data Layout**: A single column of chronological values hosted on a backing data worksheet.
- **Formula Logic**: None required; relies on direct chart references to the data column.
- **Visual Design**: Uses a typographic hierarchy: a subdued, smaller font for the category title and a large, high-contrast font for the current KPI value, directly above the chart.
- **Charts/Tables**: `LineChart` configured with `x_axis.delete = True`, `y_axis.delete = True`, and `legend = None`. The series is customized with `smooth = True` and a heavy stroke width.
- **Theme Hooks**: Consumes `text` (KPI value), `subtext` (title), and `accent` (trend line color).

### 3. Reproduction Code

```python
from openpyxl.styles import Font
from openpyxl.chart import LineChart, Reference
from openpyxl.utils.cell import coordinate_to_tuple
from openpyxl.drawing.line import LineProperties

def render(ws, anchor: str, data_ws, data_min_col: int, data_min_row: int, data_max_row: int, title: str, kpi_value: float, kpi_format: str = "#,##0", *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a KPI card featuring a primary metric and a minimalist trend line (sparkline-style).
    
    :param ws: The worksheet to render the card onto.
    :param anchor: Top-left cell coordinate (e.g., "B2") for the card.
    :param data_ws: Worksheet containing the trend data.
    :param data_min_col: Column index of the trend values.
    :param data_min_row: Starting row of the trend values.
    :param data_max_row: Ending row of the trend values.
    :param title: The label for the KPI (e.g., "Social media advertising").
    :param kpi_value: The summary metric to display above the chart (e.g., 348).
    :param kpi_format: Number format for the KPI value.
    """
    r, c = coordinate_to_tuple(anchor)
    
    # Palette fallback (simulating theme hook extraction)
    themes = {
        "corporate_blue": {"text": "000000", "subtext": "595959", "accent": "205479"},
        "dark_dashboard": {"text": "FFFFFF", "subtext": "A6A6A6", "accent": "4A90E2"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # 1. Render KPI Title
    cell_title = ws.cell(row=r, column=c, value=title)
    cell_title.font = Font(name="Calibri", size=11, color=palette["subtext"], bold=True)
    
    # 2. Render KPI Value
    cell_kpi = ws.cell(row=r+1, column=c, value=kpi_value)
    cell_kpi.font = Font(name="Calibri", size=22, color=palette["text"], bold=True)
    cell_kpi.number_format = kpi_format
    
    # 3. Create Minimalist Trend Chart
    chart = LineChart()
    chart.height = 3.5  # Compact height for dashboard tile
    chart.width = 7.0
    
    # Add data series
    values = Reference(data_ws, min_col=data_min_col, min_row=data_min_row, max_row=data_max_row)
    chart.add_data(values, titles_from_data=False)
    
    # Strip standard chart clutter (axes, legend)
    chart.legend = None
    chart.x_axis.delete = True
    chart.y_axis.delete = True
    
    # Remove outer chart border
    chart.graphical_properties.line = LineProperties(noFill=True)
    
    # Format the trend line
    if chart.series:
        series = chart.series[0]
        series.smooth = True  # Apply smoothed line curve
        series.graphicalProperties.line.solidFill = palette["accent"]
        series.graphicalProperties.line.width = 25000  # Make line thicker (2.5 pt)
    
    # Position chart immediately below the KPI text
    chart_anchor = ws.cell(row=r+2, column=c).coordinate
    ws.add_chart(chart, chart_anchor)
```
```