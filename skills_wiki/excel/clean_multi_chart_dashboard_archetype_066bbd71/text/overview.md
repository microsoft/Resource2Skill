### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Multi-Chart Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Separates data, aggregation, and presentation into distinct sheets. Converts the presentation sheet into a clean canvas by removing gridlines and carefully aligning multiple chart types (Stacked Columns for categorical comparison, Line charts for temporal trends) alongside a control panel area. 
* **Applicability**: Ideal for executive summaries, KPI reports, and performance tracking where multiple cuts of data (e.g., regional breakdown vs. time-series trends) must be digested simultaneously without the clutter of raw spreadsheet cells.

### 2. Structural Breakdown

- **Data Layout**: Employs a three-layer architecture:
  1. `Data` sheet (raw transactional tables).
  2. `Calc` sheet (aggregated matrices serving as chart data sources, mimicking PivotTables).
  3. `Dashboard` sheet (presentation only, gridlines disabled).
- **Formula Logic**: (Implicit in this code via static aggregations, but structurally represents `SUMIFS` or PivotTable aggregations).
- **Visual Design**: Gridlines off (`showGridLines = False`). A prominent, theme-colored dashboard title spans the top. A distinct left-hand column is reserved for controls (simulating slicers).
- **Charts/Tables**: 
  - Main categorical chart: `BarChart(grouping="stacked", type="col")` for multi-dimensional comparison.
  - Trend charts: `LineChart()` for time-series data.
- **Theme Hooks**: Utilizes `primary_bg` for the header banner and `primary_fg` for the text.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme setup (fallback to corporate blue)
    themes = {
        "corporate_blue": {"primary_bg": "003366", "primary_fg": "FFFFFF", "accent": "4F81BD"},
        "midnight_dark": {"primary_bg": "1E1E1E", "primary_fg": "E0E0E0", "accent": "007ACC"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # 2. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_calc = wb.create_sheet("Calc")
    ws_data = wb.create_sheet("Data")
    
    # --- CALC SHEET (Aggregated Data for Charts) ---
    # Stacked Bar Data (Profit by Market & Cookie Type)
    bar_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar"],
        ["India", 62349, 4872, 21028, 25085, 18561],
        ["Malaysia", 46587, 5537, 17536, 20555, 10633],
        ["Philippines", 54618, 7026, 22005, 8313, 14947],
        ["United Kingdom", 46530, 5220, 11497, 14620, 19446],
        ["United States", 36657, 6368, 22260, 9937, 9185]
    ]
    for row in bar_data:
        ws_calc.append(row)
        
    # Line Chart 1 Data (Units Sold by Month)
    ws_calc.append([])
    line1_start_row = ws_calc.max_row + 1
    line1_data = [
        ["Month", "Units Sold"],
        ["Sep", 50601], ["Oct", 95622], ["Nov", 65481], ["Dec", 52970]
    ]
    for row in line1_data:
        ws_calc.append(row)
        
    # Line Chart 2 Data (Profit by Month)
    ws_calc.append([])
    line2_start_row = ws_calc.max_row + 1
    line2_data = [
        ["Month", "Profit"],
        ["Sep", 124812], ["Oct", 228275], ["Nov", 160228], ["Dec", 136337]
    ]
    for row in line2_data:
        ws_calc.append(row)
        
    ws_calc.sheet_state = 'hidden' # Hide calculation sheet

    # --- DASHBOARD SHEET ---
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Header
    ws_dash.merge_cells("B2:P3")
    header_cell = ws_dash["B2"]
    header_cell.value = title
    header_cell.font = Font(name="Calibri", size=24, bold=True, color=palette["primary_fg"])
    header_cell.fill = PatternFill(fill_type="solid", start_color=palette["primary_bg"])
    header_cell.alignment = Alignment(vertical="center", indent=1)
    
    # Sidebar mockup (Placeholder for slicers)
    ws_dash.merge_cells("B5:C25")
    sidebar = ws_dash["B5"]
    sidebar.fill = PatternFill(fill_type="solid", start_color="F2F2F2")
    sidebar.font = Font(color="7F7F7F", italic=True)
    sidebar.value = "[ Controls / Slicers Area ]"
    sidebar.alignment = Alignment(horizontal="center", vertical="center")
    
    # Chart 1: Stacked Column (Profit by Market & Cookie)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.height = 10.5
    chart1.width = 16
    
    c1_data = Reference(ws_calc, min_col=2, min_row=1, max_col=6, max_row=6)
    c1_cats = Reference(ws_calc, min_col=1, min_row=2, max_row=6)
    chart1.add_data(c1_data, titles_from_data=True)
    chart1.set_categories(c1_cats)
    ws_dash.add_chart(chart1, "E5")
    
    # Chart 2: Line (Units Sold)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.height = 5
    chart2.width = 12
    chart2.legend = None
    
    c2_data = Reference(ws_calc, min_col=2, min_row=line1_start_row, max_row=line1_start_row+4)
    c2_cats = Reference(ws_calc, min_col=1, min_row=line1_start_row+1, max_row=line1_start_row+4)
    chart2.add_data(c2_data, titles_from_data=True)
    chart2.set_categories(c2_cats)
    ws_dash.add_chart(chart2, "M5")
    
    # Chart 3: Line (Profit)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.height = 5
    chart3.width = 12
    chart3.legend = None
    
    c3_data = Reference(ws_calc, min_col=2, min_row=line2_start_row, max_row=line2_start_row+4)
    c3_cats = Reference(ws_calc, min_col=1, min_row=line2_start_row+1, max_row=line2_start_row+4)
    chart3.add_data(c3_data, titles_from_data=True)
    chart3.set_categories(c3_cats)
    ws_dash.add_chart(chart3, "M15")
    
    # Set some column widths for aesthetics
    ws_dash.column_dimensions["A"].width = 2
    ws_dash.column_dimensions["B"].width = 12
    ws_dash.column_dimensions["C"].width = 12
    ws_dash.column_dimensions["D"].width = 2
```