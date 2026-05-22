### 1. High-level Skill Pattern Extraction

> **Skill Name**: Transparent KPI Donut Chart with Center Text

* **Tier**: component
* **Core Mechanism**: Calculates completion percentage, writes it to a merged center cell with a large font, and overlays a Doughnut chart with a 65% hole size and a transparent background (`noFill=True`). This creates a cohesive KPI widget without relying on finicky Excel text boxes inside the chart object.
* **Applicability**: Perfect for executive dashboards where KPIs need to be visualized as progress rings with dynamic text perfectly centered inside the hole.

### 2. Structural Breakdown

- **Data Layout**: Writes the calculation (`% Complete` and `% Remainder`) to a hidden data range specified by `data_anchor` (e.g., column AA) to keep the dashboard area clean.
- **Formula Logic**: Calculates `min(actual / target, 1.0)` to ensure the completion slice doesn't exceed 100% on over-performance.
- **Visual Design**: The visual anchor acts as a 3-column block. The title sits at the top, and the percentage is centered in a large merged block directly behind the transparent chart.
- **Charts/Tables**: `DoughnutChart` sized at 4.5x4.5 cm with a `holeSize` of 65. The legend, title, and borders are removed for a clean, modern widget look.
- **Theme Hooks**: Consumes the `accent` token for the completion progress slice and the `text` token for the labels.

### 3. Reproduction Code

```python
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.drawing.fill import SolidColorFillProperties
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.styles import Font, Alignment
from openpyxl.utils import coordinate_to_tuple, get_column_letter

def render(ws, anchor: str, kpi_name: str, actual: float, target: float, data_anchor: str = "AA1", theme: str = "corporate_blue", **kwargs) -> None:
    # Setup Theme Colors
    theme_colors = {
        "corporate_blue": {"accent": "4F81BD", "text": "1F497D"},
        "modern_dark": {"accent": "2CA02C", "text": "333333"},
        "warm_sunset": {"accent": "E26B0A", "text": "595959"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    accent_color = palette["accent"]
    remainder_color = "D9D9D9"  # Light gray
    text_color = palette["text"]

    # Calculate percentages
    pct_complete = min(actual / target, 1.0) if target else 0.0
    pct_remainder = max(1.0 - pct_complete, 0.0)

    # Write data to the designated off-screen data area
    dr, dc = coordinate_to_tuple(data_anchor)
    ws.cell(row=dr, column=dc, value="Complete")
    ws.cell(row=dr+1, column=dc, value="Remainder")
    ws.cell(row=dr, column=dc+1, value=pct_complete)
    ws.cell(row=dr+1, column=dc+1, value=pct_remainder)

    # Format the visual layout
    ar, ac = coordinate_to_tuple(anchor)
    
    # Title Header
    ws.merge_cells(start_row=ar, start_column=ac, end_row=ar, end_column=ac+2)
    title_cell = ws.cell(row=ar, column=ac)
    title_cell.value = kpi_name
    title_cell.font = Font(name="Calibri", size=14, bold=True, color=text_color)
    title_cell.alignment = Alignment(horizontal="center")

    # Center Text (Percentage) sitting behind the chart hole
    ws.merge_cells(start_row=ar+3, start_column=ac, end_row=ar+6, end_column=ac+2)
    center_cell = ws.cell(row=ar+3, column=ac)
    center_cell.value = pct_complete
    center_cell.number_format = "0%"
    center_cell.font = Font(name="Calibri", size=20, bold=True, color=text_color)
    center_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Create Doughnut Chart
    chart = DoughnutChart()
    chart.title = None
    chart.legend = None
    chart.width = 4.5   # cm
    chart.height = 4.5  # cm
    chart.holeSize = 65

    # Make chart background and border fully transparent to reveal the center cell text
    chart.graphical_properties = GraphicalProperties(
        noFill=True,
        ln=LineProperties(noFill=True)
    )

    # Add data
    data = Reference(ws, min_col=dc+1, min_row=dr, max_row=dr+1)
    chart.add_data(data, titles_from_data=False)

    # Style the specific slices
    series = chart.series[0]
    
    # Slice 0: Complete progress (Accent)
    pt_complete = DataPoint(idx=0)
    pt_complete.graphicalProperties = GraphicalProperties(
        solidFill=SolidColorFillProperties(srgbClr=accent_color),
        ln=LineProperties(noFill=True)
    )
    series.dPt.append(pt_complete)

    # Slice 1: Remaining progress (Gray)
    pt_remainder = DataPoint(idx=1)
    pt_remainder.graphicalProperties = GraphicalProperties(
        solidFill=SolidColorFillProperties(srgbClr=remainder_color),
        ln=LineProperties(noFill=True)
    )
    series.dPt.append(pt_remainder)

    # Position chart slightly below the title
    chart_anchor = f"{get_column_letter(ac)}{ar+1}"
    ws.add_chart(chart, chart_anchor)
```