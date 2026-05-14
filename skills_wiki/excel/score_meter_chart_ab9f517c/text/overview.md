# Score Meter Chart

## Applicability

Perfect for executive dashboards or KPI reporting where a single metric needs to be contextualized against quality bands (e.g., poor, average, good).

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Score Meter Chart
* **Tier**: component
* **Core Mechanism**: Creates a gauge/bullet chart by overlaying a secondary stacked bar chart on top of a primary stacked color-scale chart. The secondary chart uses a transparent base and a thin contrasting bar to act as a slider/indicator marking the KPI value.
* **Applicability**: Perfect for executive dashboards or KPI reporting where a single metric needs to be contextualized against quality bands (e.g., poor, average, good).

### 2. Structural Breakdown

- **Data Layout**: Generates a set of hidden configuration rows containing the 5 background scale intervals (20% each), a dynamically calculated transparent base value (`Actual - Indicator Width / 2`), and the indicator width (e.g., 2%).
- **Formula Logic**: Base value = `MAX(0, Actual Value - (Indicator Width / 2))` to correctly center the visual indicator directly over the raw percentage.
- **Visual Design**: The primary chart's gap width is set wider (150%) than the secondary chart's gap width (50%) so the indicator bar vertically overhangs the color scale, naturally mimicking a cursor.
- **Charts/Tables**: Two horizontal stacked `BarCharts` combined. Both X-axes are strictly fixed from 0.0 to 1.0. The primary Y-axis (category labels) and both secondary axes are hidden to yield a clean, seamless single-bar design.
- **Theme Hooks**: Uses a custom Red-to-Green traffic light palette by default, designed to contrast with a pure black indicator. 

### 3. Reproduction Code

```python
def render(ws, anchor: str, actual_value: float = 0.73, *, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, Reference, Series
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.line import LineProperties
    from openpyxl.utils.cell import coordinate_to_tuple
    
    # 1. Setup Data Layout
    # Place hidden calculation data 20 rows below the anchor
    row, col = coordinate_to_tuple(anchor)
    data_row = row + 20
    data_col = col
    
    intervals = [0.2, 0.2, 0.2, 0.2, 0.2]
    # Traffic light color scale: Red -> Orange -> Yellow -> Light Green -> Dark Green
    colors = ["FF0000", "ED7D31", "FFC000", "92D050", "00B050"] 
    
    # Write scale intervals
    for i, val in enumerate(intervals):
        ws.cell(row=data_row + i, column=data_col, value=f"Scale {i+1}")
        ws.cell(row=data_row + i, column=data_col + 1, value=val)
        
    # Calculate indicator dimensions to center it exactly on the actual_value
    indicator_width = 0.02
    base_val = max(0, actual_value - (indicator_width / 2))
    
    ws.cell(row=data_row + 5, column=data_col, value="Base")
    ws.cell(row=data_row + 5, column=data_col + 1, value=base_val)
    
    ws.cell(row=data_row + 6, column=data_col, value="Indicator")
    ws.cell(row=data_row + 6, column=data_col + 1, value=indicator_width)
    
    # 2. Build Primary Chart (Background Scale)
    chart1 = BarChart()
    chart1.type = "bar"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.gapWidth = 150  # Thinner bar to let the indicator overhang
    chart1.title = "Score Meter"
    chart1.legend = None
    chart1.width = 16
    chart1.height = 4
    
    for i in range(5):
        val_ref = Reference(ws, min_col=data_col+1, min_row=data_row+i, max_col=data_col+1, max_row=data_row+i)
        series = Series(val_ref, title=f"Scale {i+1}")
        series.graphicalProperties = GraphicalProperties()
        series.graphicalProperties.solidFill = colors[i]
        series.graphicalProperties.line = LineProperties(solidFill="FFFFFF") # Crisp white border
        chart1.series.append(series)
        
    chart1.x_axis.scaling.min = 0.0
    chart1.x_axis.scaling.max = 1.0
    chart1.x_axis.majorGridlines = None
    chart1.y_axis.delete = True  # Hide primary category labels (the "1" on the left)
    
    # 3. Build Secondary Chart (Indicator Overlay)
    chart2 = BarChart()
    chart2.type = "bar"
    chart2.grouping = "stacked"
    chart2.overlap = 100
    chart2.gapWidth = 50  # Thicker bar forcing the indicator to protrude vertically
    
    # Base series (Transparent buffer pushing the indicator to the right)
    base_ref = Reference(ws, min_col=data_col+1, min_row=data_row+5, max_col=data_col+1, max_row=data_row+5)
    s_base = Series(base_ref, title="Base")
    s_base.graphicalProperties = GraphicalProperties()
    s_base.graphicalProperties.noFill = True
    s_base.graphicalProperties.line = LineProperties(noFill=True)
    chart2.series.append(s_base)
    
    # Indicator series (Black cursor)
    ind_ref = Reference(ws, min_col=data_col+1, min_row=data_row+6, max_col=data_col+1, max_row=data_row+6)
    s_ind = Series(ind_ref, title="Indicator")
    s_ind.graphicalProperties = GraphicalProperties()
    s_ind.graphicalProperties.solidFill = "000000"
    s_ind.graphicalProperties.line = LineProperties(noFill=True)
    chart2.series.append(s_ind)
    
    # Configure secondary axes mappings
    chart2.x_axis.axId = 200
    chart2.y_axis.axId = 201
    chart2.x_axis.crosses = "max"
    chart2.y_axis.crosses = "max"
    
    chart2.x_axis.scaling.min = 0.0
    chart2.x_axis.scaling.max = 1.0
    chart2.x_axis.delete = True  # Hide secondary X axis (top axis)
    chart2.y_axis.delete = True  # Hide secondary Y axis
    
    # Combine and place
    chart1 += chart2
    ws.add_chart(chart1, anchor)
```