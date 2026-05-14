### 1. High-level Skill Pattern Extraction

> **Skill Name**: KPI Doughnut Chart

* **Tier**: component
* **Core Mechanism**: Generates a two-slice doughnut chart (Actual vs Remainder) representing progress toward a target. Sets a specific `holeSize` (e.g., 65%) to create a modern ring appearance, disables the legend, and turns off chart borders to blend seamlessly into dashboard backgrounds.
* **Applicability**: Best for high-level dashboard summaries where a single metric's completion percentage needs visual emphasis. Very commonly paired with text boxes or central cell values to display the percentage inside the ring.

### 2. Structural Breakdown

- **Data Layout**: Two rows by two columns (Actual and Remainder values) staged near the anchor.
- **Formula Logic**: Remainder is calculated dynamically as `Target - Actual`. 
- **Visual Design**: Chart area borders and fills are disabled (`noFill=True`) to avoid rigid white bounding boxes on gray or themed dashboard canvases. 
- **Charts/Tables**: `DoughnutChart` from openpyxl with `holeSize = 65` and `has_legend = False`.
- **Theme Hooks**: Employs `corporate_blue` for generic styling, relying on Excel's default palette preset (`chart.style = 10`) to color the slices.

### 3. Reproduction Code

```python
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
```