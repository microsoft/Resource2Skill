### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Canvas Chart Dashboard

* **Tier**: archetype
* **Core Mechanism**: Separates data processing from presentation by creating a clean "Dashboard" sheet with gridlines disabled. It positions multiple styled charts (e.g., a primary stacked column and secondary trend lines) in an aligned layout, reading from a hidden or separate "Data" sheet. *(Note: While the video uses Slicers and PivotTables for interactivity, `openpyxl` cannot natively generate these, so this archetype focuses on the structural and visual layout pattern of the dashboard).*
* **Applicability**: Perfect for high-level executive summaries, automated reporting distributions, or KPI dashboards where you want to present clean, aligned, and distraction-free visual metrics driven by backend aggregated data.

### 2. Structural Breakdown

- **Data Layout**: A background `Data` sheet containing pre-aggregated tabular matrices (e.g., Matrix for Market vs. Product, and Time-series for Trends).
- **Formula Logic**: N/A (Data is aggregated in Python before writing to the canvas).
- **Visual Design**: The dashboard worksheet has `showGridLines = False`. A bold, oversized header text provides context. Chart placement is aligned logically (primary metric large on the left, secondary trends stacked on the right).
- **Charts/Tables**: 
  - `BarChart` configured as `stacked` with `overlap=100` for part-to-whole comparisons.
  - Two `LineChart`s for monthly trends.
  - Legends and axes are customized to reduce clutter.
- **Theme Hooks**: Employs standard chart styles (`style=10`, `style=13`) which respect Excel's active palette, and standard font scaling for the dashboard title.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Generates a clean-canvas dashboard with aligned charts referencing a backend data sheet.
    """
    # 1. Setup Backend Data Sheet
    ws_data = wb.active
    ws_data.title = "Data"
    
    # Pre-aggregated Market vs Product matrix
    market_data = [
        ['Market', 'Chocolate Chip', 'Fortune Cookie', 'Oatmeal Raisin', 'Sugar'],
        ['India', 62349, 4872, 21028, 25085],
        ['Philippines', 54618, 7026, 22005, 8313],
        ['United Kingdom', 46530, 5220, 11497, 14620],
        ['United States', 36657, 6368, 22260, 9937]
    ]
    for row in market_data:
        ws_data.append(row)
        
    ws_data.append([]) # Spacer row
    
    # Pre-aggregated Trend data
    trend_start_row = ws_data.max_row + 1
    trend_data = [
        ['Month', 'Units Sold', 'Profit'],
        ['Sep', 50601, 124812],
        ['Oct', 95622, 228275],
        ['Nov', 65481, 160228],
        ['Dec', 52970, 136337]
    ]
    for row in trend_data:
        ws_data.append(row)

    # Hide the data sheet (optional, common practice for pure dashboards)
    ws_data.sheet_state = 'hidden'

    # 2. Setup Clean Canvas Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Header
    ws_dash["B2"] = title
    ws_dash["B2"].font = Font(size=24, bold=True, color="003366")
    
    # 3. Create Stacked Bar Chart (Primary Visual)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.height = 14
    chart1.width = 16
    
    # Link Data for Chart 1
    data1 = Reference(ws_data, min_col=2, min_row=1, max_col=5, max_row=5)
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    ws_dash.add_chart(chart1, "B5")

    # 4. Create Line Chart (Secondary Visual A - Units)
    chart2 = LineChart()
    chart2.title = "Units Sold Each Month"
    chart2.style = 13
    chart2.height = 7
    chart2.width = 14
    
    # Link Data for Chart 2
    data2 = Reference(ws_data, min_col=2, min_row=trend_start_row, max_col=2, max_row=trend_start_row+4)
    cats2 = Reference(ws_data, min_col=1, min_row=trend_start_row+1, max_row=trend_start_row+4)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.legend = None  # Remove legend for clean look
    ws_dash.add_chart(chart2, "I5")

    # 5. Create Line Chart (Secondary Visual B - Profit)
    chart3 = LineChart()
    chart3.title = "Profit by Month"
    chart3.style = 13
    chart3.height = 7
    chart3.width = 14
    
    # Link Data for Chart 3
    data3 = Reference(ws_data, min_col=3, min_row=trend_start_row, max_col=3, max_row=trend_start_row+4)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats2)
    chart3.legend = None  # Remove legend for clean look
    ws_dash.add_chart(chart3, "I19")
    
    # Ensure Dashboard is the active view when opening
    wb.active = ws_dash
```