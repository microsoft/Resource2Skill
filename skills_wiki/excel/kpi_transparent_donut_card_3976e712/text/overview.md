### 1. High-level Skill Pattern Extraction

> **Skill Name**: KPI Transparent Donut Card

* **Tier**: component
* **Core Mechanism**: Simulates a dynamic text box inside a donut chart by rendering a transparent-background `DoughnutChart` directly over a styled, enlarged cell containing the KPI value. The chart's hole size is dialed to 65% and custom slice colors are applied.
* **Applicability**: Perfect for high-level dashboard summaries where you need to show percentage completion towards a goal. This bypasses brittle Shape/Textbox XML manipulation by leveraging pure cell formatting and chart transparency.

### 2. Structural Breakdown

- **Data Layout**: Stores the raw "Complete" and "Remainder" values in an off-screen row to feed the chart without cluttering the view area.
- **Formula Logic**: Calculates the remainder slice automatically inline (`1 - percentage`).
- **Visual Design**: Sheet gridlines are hidden. The anchor cell is expanded, and the text is sized up, bolded, and centered to perfectly sit inside the donut hole.
- **Charts/Tables**: `DoughnutChart` with `holeSize=65`. The `legend` and `title` are removed. Plot area and chart area use `noFill` to achieve a transparent center. 
- **Theme Hooks**: The primary theme color is applied to the central text and the "Complete" slice. A muted gray is applied to the "Remainder" slice.

### 3. Reproduction Code

```python
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.colors import ColorChoice
from openpyxl.styles import Font, Alignment
from openpyxl.chart.series import DataPoint

def render(ws, anchor: str, *, percentage: float = 0.85, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a KPI donut chart centered cleanly over a dynamic cell value.
    """
    # 1. Hide gridlines for a clean dashboard look
    ws.sheet_view.showGridLines = False

    # 2. Place the large percentage text in the anchor cell
    anchor_cell = ws[anchor]
    anchor_cell.value = percentage
    anchor_cell.number_format = '0%'
    
    # In a full framework, resolve via theme palette. Hardcoding for the component logic.
    primary_color = "1F4E78" 
    bg_color = "D9D9D9"
    
    anchor_cell.font = Font(size=24, bold=True, color=primary_color)
    anchor_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Resize the row and column to frame the donut chart perfectly around the cell text
    ws.row_dimensions[anchor_cell.row].height = 160
    ws.column_dimensions[anchor_cell.column_letter].width = 25
    
    # 3. Write chart data far out of the print/view area
    data_row = anchor_cell.row + 100
    ws.cell(row=data_row, column=1, value="Complete")
    ws.cell(row=data_row, column=2, value=percentage)
    ws.cell(row=data_row+1, column=1, value="Remainder")
    ws.cell(row=data_row+1, column=2, value=1 - percentage)
    
    # 4. Create and configure Doughnut Chart
    chart = DoughnutChart()
    data = Reference(ws, min_col=2, min_row=data_row, max_row=data_row+1)
    labels = Reference(ws, min_col=1, min_row=data_row, max_row=data_row+1)
    
    chart.add_data(data)
    chart.set_categories(labels)
    
    # Customize the donut ring
    chart.holeSize = 65
    chart.legend = None
    chart.title = None
    
    # Size chart to align proportionally with the expanded cell dimensions
    chart.width = 3.5
    chart.height = 3.5
    
    # 5. Make chart and plot area transparent so the cell value shows through the hole
    transparent_props = GraphicalProperties(noFill=True)
    transparent_props.ln = LineProperties(noFill=True)
    
    chart.graphical_properties = transparent_props
    chart.plot_area.graphical_properties = transparent_props
    
    # 6. Apply custom slice colors to match the theme
    series = chart.series[0]
    
    dp0 = DataPoint(idx=0)
    dp0.spPr = GraphicalProperties(solidFill=ColorChoice(srgbClr=primary_color))
    
    dp1 = DataPoint(idx=1)
    dp1.spPr = GraphicalProperties(solidFill=ColorChoice(srgbClr=bg_color))
    
    series.dPt = [dp0, dp1]
    
    # 7. Add chart to overlay the text cell
    ws.add_chart(chart, anchor)
```