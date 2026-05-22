### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Chart Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Generates a dedicated 'ChartData' sheet with summary tables, then builds a clean 'Dashboard' presentation sheet. Disables sheet gridlines, adds a bold title, and places a large main categorical chart (e.g., Stacked Bar) alongside two smaller vertically-stacked trend charts (Line).
* **Applicability**: Best for executive summaries where a categorical breakdown (e.g., market share by product) must be viewed alongside time-series trends (e.g., monthly volume and profit). Acts as a robust static alternative to Slicer-driven dashboards when generating reports programmatically.

### 2. Structural Breakdown

- **Data Layout**: Source data is isolated on a "ChartData" worksheet containing pre-aggregated tables (simulating Pivot Tables). 
- **Formula Logic**: None required; relies on structured source data blocks feeding directly into chart references.
- **Visual Design**: Gridlines are hidden (`showGridLines = False`) on the Dashboard sheet to create a web-like application feel. A prominent title sits at `B2`.
- **Charts/Tables**: 
  - Chart 1: Stacked Bar Chart for composition analysis, anchored to `B4`.
  - Chart 2 & 3: Line Charts for time-series trends, hiding legends to save space, anchored to `I4` and `I11` respectively.
- **Theme Hooks**: The title font color falls back to `1F497D` for a corporate blue look or `333333` for neutral depending on the theme parameter.

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font

def render_workbook(wb: Workbook, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # Set up theme fallback colors
    title_color = "1F497D" if theme == "corporate_blue" else "333333"

    # 1. Setup Source Data Sheet
    data_ws = wb.active
    data_ws.title = "ChartData"
    
    # Table 1: Profit by Market & Cookie Type (Row 1-6)
    data_ws.append(["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"])
    data_ws.append(["India", 62000, 23000, 21000, 25000])
    data_ws.append(["Philippines", 54000, 24000, 22000, 8000])
    data_ws.append(["United Kingdom", 46000, 26000, 11000, 14000])
    data_ws.append(["Malaysia", 46000, 20000, 17000, 20000])
    data_ws.append(["United States", 36000, 32000, 22000, 9000])
    
    # Leave space
    data_ws.append([])
    data_ws.append([])
    data_ws.append([])
    
    # Table 2: Monthly Trends (Row 10-14)
    data_ws.append(["Month", "Units Sold", "Profit"])
    months = ["Sep", "Oct", "Nov", "Dec"]
    units = [50601, 95622, 65481, 52970]
    profits = [124812, 228275, 160228, 136337]
    for m, u, p in zip(months, units, profits):
        data_ws.append([m, u, p])
        
    # 2. Setup Dashboard Sheet
    dash_ws = wb.create_sheet(title="Dashboard")
    
    # Hide gridlines for a clean "software UI" feel
    dash_ws.sheet_view.showGridLines = False
    
    # Add Title
    dash_ws["B2"] = title
    dash_ws["B2"].font = Font(size=24, bold=True, color=title_color)
    
    # 3. Chart 1: Stacked Bar Chart (Composition)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    
    bar_data_ref = Reference(data_ws, min_col=2, max_col=5, min_row=1, max_row=6)
    bar_cats_ref = Reference(data_ws, min_col=1, min_row=2, max_row=6)
    bar_chart.add_data(bar_data_ref, titles_from_data=True)
    bar_chart.set_categories(bar_cats_ref)
    
    # Position and size main chart
    dash_ws.add_chart(bar_chart, "B4")
    bar_chart.width = 16  # Approx 8.5 columns
    bar_chart.height = 12 # Approx 24 rows
    
    # 4. Chart 2: Top Line Chart (Units Sold Trend)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1_data_ref = Reference(data_ws, min_col=2, max_col=2, min_row=10, max_row=14)
    line_cats_ref = Reference(data_ws, min_col=1, min_row=11, max_row=14)
    line1.add_data(line1_data_ref, titles_from_data=True)
    line1.set_categories(line_cats_ref)
    line1.legend = None  # Hide legend since the title is self-explanatory
    
    dash_ws.add_chart(line1, "J4")
    line1.width = 13.5
    line1.height = 6
    
    # 5. Chart 3: Bottom Line Chart (Profit Trend)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2_data_ref = Reference(data_ws, min_col=3, max_col=3, min_row=10, max_row=14)
    line2.add_data(line2_data_ref, titles_from_data=True)
    line2.set_categories(line_cats_ref)
    line2.legend = None  # Hide legend since the title is self-explanatory
    
    dash_ws.add_chart(line2, "J15")
    line2.width = 13.5
    line2.height = 6
    
    # Activate the dashboard as the default view
    wb.active = dash_ws
```