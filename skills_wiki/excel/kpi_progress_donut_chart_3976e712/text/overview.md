### 1. High-level Skill Pattern Extraction

> **Skill Name**: KPI Progress Donut Chart

* **Tier**: component
* **Core Mechanism**: Builds a two-slice Doughnut Chart to visualize a percentage metric against its remainder (100% - x). Customizes the doughnut hole size to 65% to match modern dashboard aesthetics. Hides the legend and title to maximize the chart area, allowing it to be paired closely with a bold textual KPI callout.
* **Applicability**: Best used in executive and sales dashboards to visualize metrics like "Customer Satisfaction", "% of Target Achieved", or "Project Completion". Requires a single percentage metric (between 0.0 and 1.0).

### 2. Structural Breakdown

- **Data Layout**: Writes an offset helper table (typically outside the print area) holding `["Actual", percentage]` and `["Remainder", 1.0 - percentage]`.
- **Formula Logic**: Derives the remainder slice inline using `1.0 - percentage`.
- **Visual Design**: The textual KPI value is styled with a large, bold font to simulate the "text box in the center" look when placed near the chart.
- **Charts/Tables**: `DoughnutChart` initialized with `holeSize = 65`. The slices are explicitly colored—a dark primary fill for the actual value and a muted/light fill for the remainder to establish visual contrast.
- **Theme Hooks**: The title font color, actual percentage font color, and the `solidFill` properties of the chart slices should ideally hook into the theme's primary and accent palettes (e.g., `theme.primary_dark` and `theme.background_alt`).

### 3. Reproduction Code

```python
from openpyxl.chart import DoughnutChart, Reference, Series
from openpyxl.chart.series import DataPoint
from openpyxl.styles import Font, Alignment
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter

def render(ws, anchor: str, *, title: str, percentage: float, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a KPI Progress Donut Chart and its textual callouts.
    """
    col_str, row_idx = coordinate_from_string(anchor)
    col_idx = column_index_from_string(col_str)
    
    # 1. Render textual callouts (Title and Value)
    title_cell = ws[anchor]
    title_cell.value = title
    title_cell.font = Font(bold=True, size=12, color="333333")
    title_cell.alignment = Alignment(horizontal="center")
    
    pct_cell = ws.cell(row=row_idx + 1, column=col_idx)
    pct_cell.value = percentage
    pct_cell.number_format = "0%"
    pct_cell.font = Font(bold=True, size=20, color="003366")
    pct_cell.alignment = Alignment(horizontal="center")
    
    # 2. Write chart backing data to an offset area (hidden or out of print area)
    data_col = col_idx + 15
    ws.cell(row=row_idx, column=data_col, value="Actual")
    ws.cell(row=row_idx + 1, column=data_col, value="Remainder")
    ws.cell(row=row_idx, column=data_col + 1, value=percentage)
    ws.cell(row=row_idx + 1, column=data_col + 1, value=1.0 - percentage)
    
    # 3. Create the Doughnut Chart
    chart = DoughnutChart()
    chart.title = None
    chart.legend = None
    chart.holeSize = 65  # Key visual tweak for modern dashboards
    chart.width = 6.0    # Compact size for a KPI card
    chart.height = 6.0
    
    # 4. Bind data and configure series
    data_ref = Reference(ws, min_col=data_col + 1, min_row=row_idx, max_row=row_idx + 1)
    series = Series(data_ref)
    
    # Color the slices: Primary for actual, muted for remainder
    try:
        dp_actual = DataPoint(idx=0)
        dp_actual.graphicalProperties.solidFill = "003366"  # Dark Blue
        
        dp_remainder = DataPoint(idx=1)
        dp_remainder.graphicalProperties.solidFill = "D9E1E8"  # Light Blue
        
        series.dPt = [dp_actual, dp_remainder]
    except AttributeError:
        pass  # Graceful fallback if the specific openpyxl version lacks deep graphicalProperties support
        
    chart.append(series)
    
    # 5. Position the chart below the text callouts
    chart_anchor = f"{get_column_letter(col_idx)}{row_idx + 2}"
    ws.add_chart(chart, chart_anchor)
```