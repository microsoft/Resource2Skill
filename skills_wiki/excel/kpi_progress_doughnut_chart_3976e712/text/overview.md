### 1. High-level Skill Pattern Extraction

> **Skill Name**: KPI Progress Doughnut Chart

* **Tier**: component
* **Core Mechanism**: Transforms standard metrics into a minimal progress gauge. It plots "Actual" vs "Remaining" using a doughnut chart, sets a wide hole size (65%) for a modern look, hides the legend, and applies high-contrast versus muted colors to specific slices.
* **Applicability**: Perfect for high-level dashboard summaries where you need to show completion percentage against a goal (e.g., Sales vs Target, Budget utilized, Customer Satisfaction).

### 2. Structural Breakdown

- **Data Layout**: Consumes two adjacent rows for Actual and Remaining values. In this automated component, the data is tucked underneath the chart's anchor footprint to keep the dashboard sheet clean.
- **Formula Logic**: Derives the hidden `Remaining = max(0, target - actual)` dynamically before rendering.
- **Visual Design**: The title acts dynamically as the percentage label (mimicking a centered text box). The legend is suppressed to keep the visual focused on the ring.
- **Charts/Tables**: An `openpyxl.chart.DoughnutChart` adjusted to `holeSize = 65`, typically sized at 6x4 cells.
- **Theme Hooks**: Uses the theme's `primary` color for the completed progress slice and a standard `muted` (light gray) color for the remaining track.

### 3. Reproduction Code

```python
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint

def render(ws, anchor: str, *, kpi_name: str, actual: float, target: float, theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Map theme palette to chart colors
    colors = {
        "corporate_blue": {"primary": "003366", "muted": "D9D9D9"},
        "modern_dark": {"primary": "4ECDC4", "muted": "444444"}
    }
    palette = colors.get(theme, colors["corporate_blue"])

    # 2. Write supporting data under the chart anchor footprint
    row = ws[anchor].row
    col = ws[anchor].column

    ws.cell(row=row, column=col, value="Actual")
    ws.cell(row=row, column=col+1, value=actual)

    ws.cell(row=row+1, column=col, value="Remaining")
    remaining = max(0, target - actual)
    ws.cell(row=row+1, column=col+1, value=remaining)

    # 3. Initialize Doughnut Chart
    chart = DoughnutChart()
    pct_complete = int((actual / target) * 100) if target else 0
    chart.title = f"{kpi_name} ({pct_complete}%)"
    
    # 4. Apply modern dashboard styling (wide hole, no legend)
    chart.holeSize = 65
    chart.legend = None  
    chart.width = 6
    chart.height = 4

    # 5. Bind Data & Categories
    data = Reference(ws, min_col=col+1, min_row=row, max_row=row+1)
    cats = Reference(ws, min_col=col, min_row=row, max_row=row+1)
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(cats)

    # 6. Style Individual Slices (Actual vs Remaining)
    series = chart.series[0]

    dp0 = DataPoint(idx=0)
    dp0.graphicalProperties.solidFill = palette["primary"]

    dp1 = DataPoint(idx=1)
    dp1.graphicalProperties.solidFill = palette["muted"]

    # Assign customized points back to the series
    series.dPt = [dp0, dp1]

    # 7. Mount chart
    ws.add_chart(chart, anchor)
```