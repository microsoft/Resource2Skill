### 1. High-level Skill Pattern Extraction

> **Skill Name**: See-Through KPI Doughnut Chart

* **Tier**: component
* **Core Mechanism**: Builds a minimalist Doughnut chart for progress metrics where the chart background and border are completely transparent. This allows a nicely formatted percentage cell to show through the 65% hole in the center, overcoming the need for clunky, floating textboxes in Excel. 
* **Applicability**: Perfect for high-level KPI dashboard metrics representing completion, progress, utilization, or quotas where you want a clean, modern aesthetic.

### 2. Structural Breakdown

- **Data Layout**: The KPI title goes in the anchor cell. The data series (Complete vs. Remaining) is generated hidden off-screen (offset by +20 columns). The percentage text cell is located dead-center of the chart's physical footprint.
- **Formula Logic**: Dynamically calculates `pct_complete = min(actual / target, 1.0)` and `pct_remaining = 1.0 - pct_complete` within Python to plot the ring slices.
- **Visual Design**: The underlying cell uses a large, bold font with center alignment. The chart itself relies on `graphicalProperties.noFill = True` to render invisibly over the grid.
- **Charts/Tables**: Uses `DoughnutChart` with `holeSize=65`. Slices are styled directly via `DataPoint` injection to ensure a strong thematic contrast (e.g., solid dark blue for complete, light gray for remaining).
- **Theme Hooks**: Employs theme palette hooks (represented by hex codes) for the primary slice color and the center text color to keep the dashboard cohesive.

### 3. Reproduction Code

```python
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.styles import Font, Alignment
from openpyxl.utils import coordinate_from_string, column_index_from_string, get_column_letter

def render(ws, anchor: str, *, title: str, actual: float, target: float, theme: str = "corporate_blue", **kwargs) -> None:
    col_str, row = coordinate_from_string(anchor)
    col = column_index_from_string(col_str)
    
    # 1. Render KPI Title
    title_cell = ws.cell(row=row, column=col, value=title)
    title_cell.font = Font(size=12, bold=True, color="333333")
    
    # 2. Calculate progress portions
    pct_complete = min(actual / target, 1.0) if target > 0 else 0.0
    pct_remaining = 1.0 - pct_complete
    
    # 3. Render Percentage Text in the center of the chart footprint
    # A 4x4cm chart anchored at row+1, col spans approx rows (row+1 to row+8) and cols (col to col+1)
    # We place the text exactly in the middle so the doughnut hole frames it nicely.
    pct_cell = ws.cell(row=row+4, column=col+1, value=pct_complete)
    pct_cell.number_format = "0%"
    pct_cell.font = Font(size=16, bold=True, color="005082")
    pct_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 4. Write chart data securely off-screen (+20 columns away)
    data_col = col + 20
    ws.cell(row=row, column=data_col, value="Category")
    ws.cell(row=row, column=data_col+1, value="Value")
    
    ws.cell(row=row+1, column=data_col, value="Complete")
    ws.cell(row=row+1, column=data_col+1, value=pct_complete)
    
    ws.cell(row=row+2, column=data_col, value="Remaining")
    ws.cell(row=row+2, column=data_col+1, value=pct_remaining)
    
    # 5. Build Doughnut Chart
    chart = DoughnutChart()
    data = Reference(ws, min_col=data_col+1, min_row=row, max_row=row+2)
    cats = Reference(ws, min_col=data_col, min_row=row+1, max_row=row+2)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    
    # 6. Format Chart (No Title, No Legend, 65% Hole thickness)
    chart.title = None
    chart.legend = None
    chart.holeSize = 65
    
    # Size to 4x4 cm to fit nicely over the center cell footprint
    chart.width = 4.0
    chart.height = 4.0
    
    # 7. Make chart background and border perfectly transparent
    chart.graphicalProperties.noFill = True
    chart.graphicalProperties.line.noFill = True
    
    # 8. Color the slices (Complete = Primary Accent, Remaining = Light Gray)
    dp0 = DataPoint(idx=0)
    dp0.graphicalProperties.solidFill = "005082"
    
    dp1 = DataPoint(idx=1)
    dp1.graphicalProperties.solidFill = "D9D9D9"
    
    chart.series[0].dPt.append(dp0)
    chart.series[0].dPt.append(dp1)
    
    # 9. Mount chart directly below the title
    chart_anchor = f"{get_column_letter(col)}{row+1}"
    ws.add_chart(chart, chart_anchor)
```