```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Doughnut Card

* **Tier**: component
* **Core Mechanism**: Builds a modular KPI card containing a title, raw metric, and a minimalist doughnut chart showing percentage completion. Uses `openpyxl.chart.marker.DataPoint` to explicitly color individual "actual" and "remaining" chart slices, removes standard chart furniture (legends/titles), and sets `holeSize` to 65% for a modern dashboard aesthetic.
* **Applicability**: Ideal for high-level executive dashboards to show metrics against targets (e.g., Sales vs Target, Budget Utilized, Quota Attainment). Fits well in a grid layout across the top of a report.

### 2. Structural Breakdown

- **Data Layout**: Places the visible Title and Value at the anchor cell, and writes the background percentage calculations (`actual/target` and `1 - actual/target`) far off-screen (e.g., 20 columns to the right) to keep the dashboard sheet clean.
- **Formula Logic**: Calculates `pct_complete` and `pct_remain` in Python before injecting them into the hidden data columns. 
- **Visual Design**: Uses a distinct theme color for the title, value, and the "actual" chart slice, while using a muted gray for the "remaining" slice to draw the eye to the completion rate.
- **Charts/Tables**: `DoughnutChart` sized down to 4.5x4.5 cm with `holeSize=65`, `legend=None`, and `title=None`.
- **Theme Hooks**: Consumes `primary_color` (for the metric and filled slice), `muted_color` (for the empty slice), and `text_color` (for the label).

### 3. Reproduction Code

```python
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.marker import DataPoint
from openpyxl.styles import Font

def render(ws, anchor: str, *, title: str = "Sales Revenue", actual: float = 2544.0, target: float = 3000.0, value_format: str = "$#,##0", theme: str = "corporate_blue", **kwargs) -> None:
    row, col = coordinate_to_tuple(anchor)

    # In a full framework, these would be loaded from a theme helper using the `theme` kwarg
    primary_hex = "2F5597"  # Dark blue
    muted_hex = "D9D9D9"    # Light gray
    text_hex = "1F3864"     # Darker text

    # Calculate metrics bounds (capped at 100%)
    pct_complete = min(actual / target, 1.0) if target > 0 else 0
    pct_remain = 1.0 - pct_complete

    # 1. Render Labels (Title and Primary Value)
    title_cell = ws.cell(row=row, column=col, value=title)
    title_cell.font = Font(name="Arial", size=12, color=text_hex, bold=True)

    val_cell = ws.cell(row=row + 1, column=col, value=actual)
    val_cell.font = Font(name="Arial", size=18, color=primary_hex, bold=True)
    val_cell.number_format = value_format

    # Render percentage text block immediately to the right of the raw number
    pct_cell = ws.cell(row=row + 1, column=col + 1, value=pct_complete)
    pct_cell.font = Font(name="Arial", size=14, color=primary_hex, bold=True)
    pct_cell.number_format = "0%"

    # 2. Write Chart Data (offset safely to the right to hide from main dashboard view)
    data_col = col + 20
    ws.cell(row=row, column=data_col, value=pct_complete)
    ws.cell(row=row + 1, column=data_col, value=pct_remain)

    # 3. Create & Format Doughnut Chart
    chart = DoughnutChart()
    chart.width = 4.5
    chart.height = 4.5
    chart.holeSize = 65  # Creates the modern, thin-ring dashboard look

    # Remove clutter
    chart.legend = None
    chart.title = None

    # Add data
    data_ref = Reference(ws, min_col=data_col, min_row=row, max_row=row + 1)
    chart.add_data(data_ref)

    # 4. Target and color the specific slices using DataPoint index
    series = chart.series[0]

    # Slice 0: Actual completion (Themed Color)
    dp_actual = DataPoint(idx=0)
    dp_actual.graphicalProperties.solidFill = primary_hex
    series.dPt.append(dp_actual)

    # Slice 1: Remaining (Muted Background Color)
    dp_remain = DataPoint(idx=1)
    dp_remain.graphicalProperties.solidFill = muted_hex
    series.dPt.append(dp_remain)

    # 5. Position Chart
    # Place the chart slightly to the right of the KPI text block
    chart_anchor = f"{get_column_letter(col + 2)}{row}"
    ws.add_chart(chart, chart_anchor)
```
```