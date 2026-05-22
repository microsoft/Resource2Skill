### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Chart Dashboard Shell

* **Tier**: archetype
* **Core Mechanism**: Construct a standalone presentation dashboard by hiding gridlines/headers, establishing a prominent themed banner, positioning charts relative to the grid, and separating the clean visual front-end from hidden data aggregation sheets.
* **Applicability**: Ideal for executive summaries and KPI reporting. Provides a professional "app-like" interactive look in Excel. Perfect for presenting chart grids alongside a fixed control pane (like slicers).

### 2. Structural Breakdown

- **Data Layout**: A hidden `Summary` sheet holds structured aggregation tables (simulating PivotTable outputs) separated by blank rows to feed the charts.
- **Visual Design**: 
  - `sheet_view.showGridLines = False` and `showRowColHeaders = False` to create a blank canvas.
  - Control pane placeholders (mock slicers) on the left side with soft grey borders and fills to imply interactivity.
  - Large merged-cell top banner with corporate background coloring and bold, high-contrast text.
- **Charts/Tables**: A main Stacked Bar Chart for categorical mix, and two Line Charts for time-series trends. Charts are cleanly anchored to specific cells (e.g., `D5`, `M5`) to mimic Excel's "Snap to Grid" (`Alt` key) alignment.
- **Theme Hooks**: Consumes `primary` background for the header banner, `text` for banner font, and structural greys for the UI borders.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme Configuration
    themes = {
        "corporate_blue": {
            "primary": "203764",    # Dark Blue Header
            "text": "FFFFFF",       # White Text
            "slicer_hdr": "D9D9D9", # Light Grey
            "border": "A6A6A6"      # Medium Grey
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_summary = wb.create_sheet("Summary")
    
    # 3. Clean Dashboard Canvas
    ws_dash.sheet_view.showGridLines = False
    ws_dash.sheet_view.showRowColHeaders = False
    
    ws_dash.column_dimensions['A'].width = 3
    ws_dash.column_dimensions['B'].width = 18
    ws_dash.column_dimensions['C'].width = 3
    
    # 4. Top Title Banner
    ws_dash.merge_cells("A1:U3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["text"])
    title_cell.fill = PatternFill("solid", fgColor=palette["primary"])
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 5. Build Hidden Summary Data (Simulated PivotTables)
    # 5a. Profit by Market & Product
    ws_summary.append(["Country", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"])
    ws_summary.append(["India", 62000, 5000, 21000, 25000])
    ws_summary.append(["United Kingdom", 46000, 7000, 22000, 14000])
    ws_summary.append(["United States", 36000, 6000, 11000, 9000])
    ws_summary.append(["Philippines", 54000, 7000, 22000, 8000])
    
    # 5b. Units Sold by Month
    ws_summary.append([]) # row 6
    ws_summary.append(["Month", "Units Sold"]) # row 7
    ws_summary.append(["Sep", 50601]) # row 8
    ws_summary.append(["Oct", 95622])
    ws_summary.append(["Nov", 65481])
    ws_summary.append(["Dec", 52970]) # row 11
    
    # 5c. Profit by Month
    ws_summary.append([]) # row 12
    ws_summary.append(["Month", "Profit"]) # row 13
    ws_summary.append(["Sep", 124812]) # row 14
    ws_summary.append(["Oct", 228275])
    ws_summary.append(["Nov", 160228])
    ws_summary.append(["Dec", 136337]) # row 17
    
    # 6. Build Charts
    # Chart 1: Stacked Bar
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.style = 10
    chart1.legend.position = "b"
    
    data1 = Reference(ws_summary, min_col=2, min_row=1, max_col=5, max_row=5)
    cats1 = Reference(ws_summary, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    
    ws_dash.add_chart(chart1, "D5")
    chart1.width = 16
    chart1.height = 10.5

    # Chart 2: Line (Units Sold)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.style = 13
    chart2.legend = None 
    
    data2 = Reference(ws_summary, min_col=2, min_row=7, max_col=2, max_row=11)
    cats2 = Reference(ws_summary, min_col=1, min_row=8, max_row=11)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    
    ws_dash.add_chart(chart2, "M5")
    chart2.width = 12
    chart2.height = 7

    # Chart 3: Line (Profit)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.style = 13
    chart3.legend = None
    
    data3 = Reference(ws_summary, min_col=2, min_row=13, max_col=2, max_row=17)
    cats3 = Reference(ws_summary, min_col=1, min_row=14, max_row=17)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    
    ws_dash.add_chart(chart3, "M13")
    chart3.width = 12
    chart3.height = 7

    # 7. Construct Control Pane (Mock Slicers)
    thin_border = Border(
        left=Side(style='thin', color=palette["border"]),
        right=Side(style='thin', color=palette["border"]),
        top=Side(style='thin', color=palette["border"]),
        bottom=Side(style='thin', color=palette["border"])
    )
    
    # Date Slicer
    ws_dash["B6"] = "Date"
    ws_dash["B6"].fill = PatternFill("solid", fgColor=palette["slicer_hdr"])
    ws_dash["B6"].font = Font(bold=True)
    ws_dash["B7"] = "  2019"
    ws_dash["B8"] = "  2020"
    
    # Country Slicer
    ws_dash["B10"] = "Country"
    ws_dash["B10"].fill = PatternFill("solid", fgColor=palette["slicer_hdr"])
    ws_dash["B10"].font = Font(bold=True)
    ws_dash["B11"] = "  India"
    ws_dash["B12"] = "  United Kingdom"
    ws_dash["B13"] = "  United States"
    ws_dash["B14"] = "  Philippines"
    
    for row in [6, 7, 8, 10, 11, 12, 13, 14]:
        ws_dash[f"B{row}"].border = thin_border
        
    # 8. Finalize Workbook
    ws_summary.sheet_state = 'hidden'
```