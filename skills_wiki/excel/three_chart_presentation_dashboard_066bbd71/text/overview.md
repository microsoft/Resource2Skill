### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Chart Presentation Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Generates a static, cleanly aligned dashboard canvas by hiding gridlines and injecting pre-aggregated metrics into hidden columns. It then accurately anchors and scales three `openpyxl` charts (one large primary, two smaller stacked secondary) into an organized layout grid, formatting the chart axes naturally via underlying cell `number_format` assignment.
* **Applicability**: Best used when generating high-level executive dashboards directly via Python. Because interactive elements (PivotTables/Slicers) cannot be reliably authored from scratch in standard openpyxl, this shell accepts pre-aggregated datasets and mimics the final, polished presentation layer.

### 2. Structural Breakdown

- **Data Layout**: Source data is injected into columns far to the right (starting at `AA`), which are then hidden (`ws.column_dimensions["AA"].hidden = True`) to keep the dashboard canvas pristine. 
- **Formula Logic**: No direct formulas are used; rather, relies on passing pre-calculated dictionaries. Axis scaling and labels are cleaned up by formatting the hidden source cells as currency (`"$#,##0"`) or comma-separated integers (`"#,##0"`).
- **Visual Design**: Turns off gridlines (`ws.sheet_view.showGridLines = False`), aligns a large, bold header in row 2, and strips legends off the secondary line charts to reduce visual clutter.
- **Charts/Tables**: 
  - Chart 1: Stacked Bar Chart (`grouping="stacked"`, `overlap=100`) showing performance by categories.
  - Charts 2 & 3: Standard Line Charts showing trends over time.
- **Theme Hooks**: Utilizes built-in openpyxl chart styles (e.g., `style = 11` or `13`) to rapidly skin the charts, while keeping header text neutral.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", data: dict = None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a clean, presentation-ready 3-chart dashboard shell.
    Injects source data into hidden columns (AA+) and aligns a primary bar chart 
    and two secondary line charts into a cohesive grid.
    """
    ws = wb.create_sheet(sheet_name)
    
    # Hide gridlines for a clean "dashboard" canvas look
    ws.sheet_view.showGridLines = False

    # Apply Dashboard Title
    ws["B2"] = title
    ws["B2"].font = Font(size=24, bold=True, color="333333")
    ws.row_dimensions[2].height = 35
    ws["B2"].alignment = Alignment(vertical="center")

    # Fallback pre-aggregated data matching the tutorial if none provided
    if not data:
        data = {
            "primary_stacked": [
                ["Market", "Fortune Cookie", "Sugar", "Snickerdoodle", "Oatmeal Raisin", "Chocolate Chip"],
                ["India", 4800, 18500, 25000, 21000, 62000],
                ["Philippines", 7000, 14900, 8300, 22000, 54000],
                ["United Kingdom", 1200, 19400, 14600, 11400, 46000],
                ["United States", 6300, 11700, 9900, 22200, 36000]
            ],
            "secondary_trend_1": [
                ["Month", "Units Sold"],
                ["Sep", 50600],
                ["Oct", 95600],
                ["Nov", 65400],
                ["Dec", 52900]
            ],
            "secondary_trend_2": [
                ["Month", "Profit"],
                ["Sep", 124800],
                ["Oct", 228200],
                ["Nov", 160200],
                ["Dec", 136300]
            ]
        }

    # Calculate dynamic boundaries based on the injected data length
    start_row_bar = 1
    max_row_bar = start_row_bar + len(data["primary_stacked"]) - 1
    max_col_bar = 27 + len(data["primary_stacked"][0]) - 1

    start_row_l1 = max_row_bar + 2
    max_row_l1 = start_row_l1 + len(data["secondary_trend_1"]) - 1

    start_row_l2 = max_row_l1 + 2
    max_row_l2 = start_row_l2 + len(data["secondary_trend_2"]) - 1

    # --- Inject Data into Hidden Columns (AA onwards) ---
    
    # 1. Primary Stacked Data (Format values as Currency)
    for row_idx, row_data in enumerate(data["primary_stacked"], start=start_row_bar):
        for col_idx, val in enumerate(row_data, start=27): # Col 27 = 'AA'
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            if row_idx > start_row_bar and col_idx > 27:
                cell.number_format = '"$"#,##0'
    
    # 2. Secondary Trend 1 Data (Format values as Comma Int)
    for row_idx, row_data in enumerate(data["secondary_trend_1"], start=start_row_l1):
        for col_idx, val in enumerate(row_data, start=27):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            if row_idx > start_row_l1 and col_idx == 28:
                cell.number_format = '#,##0'

    # 3. Secondary Trend 2 Data (Format values as Currency)
    for row_idx, row_data in enumerate(data["secondary_trend_2"], start=start_row_l2):
        for col_idx, val in enumerate(row_data, start=27):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            if row_idx > start_row_l2 and col_idx == 28:
                cell.number_format = '"$"#,##0'

    # Hide the source data columns from the dashboard view
    for col_idx in range(27, max_col_bar + 1):
        from openpyxl.utils import get_column_letter
        ws.column_dimensions[get_column_letter(col_idx)].hidden = True

    # --- Chart 1: Stacked Column (Main Left) ---
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.style = 11
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    
    data_bar = Reference(ws, min_col=28, min_row=start_row_bar, max_col=max_col_bar, max_row=max_row_bar)
    cats_bar = Reference(ws, min_col=27, min_row=start_row_bar+1, max_row=max_row_bar)
    bar_chart.add_data(data_bar, titles_from_data=True)
    bar_chart.set_categories(cats_bar)
    bar_chart.width = 18
    bar_chart.height = 14
    ws.add_chart(bar_chart, "B4")

    # --- Chart 2: Line Chart (Top Right) ---
    line_chart1 = LineChart()
    line_chart1.style = 13
    line_chart1.title = "Units sold each month"
    
    data_line1 = Reference(ws, min_col=28, min_row=start_row_l1, max_col=28, max_row=max_row_l1)
    cats_line1 = Reference(ws, min_col=27, min_row=start_row_l1+1, max_row=max_row_l1)
    line_chart1.add_data(data_line1, titles_from_data=True)
    line_chart1.set_categories(cats_line1)
    line_chart1.legend = None  # Remove legend for cleaner small-chart layout
    line_chart1.width = 14
    line_chart1.height = 6.8
    ws.add_chart(line_chart1, "K4")

    # --- Chart 3: Line Chart (Bottom Right) ---
    line_chart2 = LineChart()
    line_chart2.style = 13
    line_chart2.title = "Profit by month"
    
    data_line2 = Reference(ws, min_col=28, min_row=start_row_l2, max_col=28, max_row=max_row_l2)
    cats_line2 = Reference(ws, min_col=27, min_row=start_row_l2+1, max_row=max_row_l2)
    line_chart2.add_data(data_line2, titles_from_data=True)
    line_chart2.set_categories(cats_line2)
    line_chart2.legend = None
    line_chart2.width = 14
    line_chart2.height = 6.8
    ws.add_chart(line_chart2, "K11")
```