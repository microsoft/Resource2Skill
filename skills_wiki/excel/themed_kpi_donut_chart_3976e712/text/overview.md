### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Donut Chart

* **Tier**: component
* **Core Mechanism**: Creates a Doughnut chart to visualize a single percentage KPI. It manipulates data points directly to apply contrasting colors (a theme primary color for "Actual", and a muted gray for "Remainder"). It expands the donut ring thickness (`holeSize=65`) and completely removes chart area backgrounds, borders, and legends to create a seamless, widget-like appearance.
* **Applicability**: Ideal for dashboard summary panels tracking completion rates, target progress, or satisfaction scores where you want a clean, minimalist visual instead of a standard bar or pie chart.

### 2. Structural Breakdown

- **Data Layout**: Places the Actual (e.g., 85%) and Remainder (15%) values in hidden cells underneath the chart's anchor position to keep the sheet layout clean.
- **Formula Logic**: Calculates the remainder automatically as `1 - actual_val`.
- **Visual Design**: Uses a solid, prominent color for the completed portion and a subtle gray for the remainder.
- **Charts/Tables**: `DoughnutChart` with custom `holeSize`, disabled legend, disabled chart area fill, and disabled border lines.
- **Theme Hooks**: Consumes the primary theme color for the "Actual" data point slice.

### 3. Reproduction Code

```python
from openpyxl.utils.cell import coordinate_to_tuple
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.marker import DataPoint
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.shapes import GraphicalProperties

def render(ws, anchor: str, kpi_name: str = "Customer Satisfaction", actual_val: float = 0.87, *, theme: str = "corporate_blue", **kwargs) -> None:
    r, c = coordinate_to_tuple(anchor)

    # Hide data underneath the chart area
    ws.cell(row=r, column=c, value=kpi_name)
    ws.cell(row=r+1, column=c, value="Actual")
    ws.cell(row=r+2, column=c, value="Remainder")

    ws.cell(row=r+1, column=c+1, value=actual_val).number_format = '0%'
    ws.cell(row=r+2, column=c+1, value=1 - actual_val).number_format = '0%'

    # Create the Doughnut Chart
    chart = DoughnutChart()
    chart.title = kpi_name
    chart.width = 6
    chart.height = 4.5
    
    # Expand the ring thickness per the tutorial
    chart.holeSize = 65 
    
    # Clean up the UI
    chart.legend = None

    data = Reference(ws, min_col=c+1, min_row=r+1, max_row=r+2)
    cats = Reference(ws, min_col=c, min_row=r+1, max_row=r+2)
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(cats)

    # Resolve theme colors
    primary_color = "1F497D" if theme == "corporate_blue" else "4F81BD"
    bg_color = "D9D9D9" # Muted light gray for the remainder track

    series = chart.series[0]

    # Style the "Actual" slice
    pt_actual = DataPoint(idx=0)
    pt_actual.graphicalProperties.solidFill = primary_color
    pt_actual.graphicalProperties.line = LineProperties(solidFill=primary_color)
    series.dPt.append(pt_actual)

    # Style the "Remainder" slice
    pt_remainder = DataPoint(idx=1)
    pt_remainder.graphicalProperties.solidFill = bg_color
    pt_remainder.graphicalProperties.line = LineProperties(solidFill=bg_color)
    series.dPt.append(pt_remainder)

    # Remove chart border and background fill for seamless dashboard integration
    chart.graphical_properties = GraphicalProperties(noFill=True)
    chart.graphical_properties.line = LineProperties(noFill=True)

    ws.add_chart(chart, anchor)
```