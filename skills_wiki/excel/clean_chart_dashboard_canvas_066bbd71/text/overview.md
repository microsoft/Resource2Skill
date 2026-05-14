### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Chart Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Transforms a blank sheet into a clean presentation canvas by disabling gridlines and UI headers, adding a full-bleed themed title bar, and arranging multiple pre-styled charts in a snapped grid layout connected to a hidden calculation sheet.
* **Applicability**: Best for executive summaries and visual KPI dashboards where data is pre-aggregated. Mimics the visual layout of interactive PivotTable dashboards when programmatic slicer generation is not available.

### 2. Structural Breakdown

- **Data Layout**: Source data is strictly separated and parked on a hidden `_Data` sheet to keep the presentation layer clean.
- **Formula Logic**: None (pure chart referencing).
- **Visual Design**: Gridlines and Row/Col headers disabled via `ws.sheet_view`. Full-bleed merged header cell with custom fill and centered text provides strong anchoring.
- **Charts/Tables**: One tall Stacked Column chart and two vertically-stacked Line charts arranged in a 2-column layout. Single-series line charts have their legends removed to maximize plot area and reduce clutter.
- **Theme Hooks**: The `theme` dictionary is parsed to extract a primary hex color for the dashboard header background.

### 3. Reproduction Code

```python
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import PatternFill, Font, Alignment

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Set up data sheet (hidden to mimic hidden PivotTable calc sheets)
    ws_data = wb.create_sheet(f"{sheet_name}_Data")
    ws_data.sheet_state = 'hidden'
    
    # Market & Cookie Data (for stacked column)
    ws_data.append(["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"])
    ws_data.append(["India", 62349, 4872, 21028])
    ws_data.append(["Philippines", 54618, 7026, 22005])
    ws_data.append(["United Kingdom", 46530, 5220, 11497])
    ws_data.append(["United States", 36657, 6368, 22260])
    
    for row in ws_data.iter_rows(min_row=2, max_row=5, min_col=2, max_col=4):
        for cell in row:
            cell.number_format = '#,##0'
            
    # Monthly Data (for line charts)
    ws_data.append([])
    ws_data.append(["Month", "Units Sold", "Profit"])
    ws_data.append(["Sep", 50601, 124812])
    ws_data.append(["Oct", 95622, 228275])
    ws_data.append(["Nov", 65481, 160228])
    ws_data.append(["Dec", 52970, 136337])
    
    for row in ws_data.iter_rows(min_row=8, max_row=11, min_col=2, max_col=3):
        row[0].number_format = '#,##0'
        row[1].number_format = '"$"#,##0'
        
    # 2. Set up Dashboard canvas
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
        
    # Hide gridlines and row/col headers to create a clean visual canvas
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False
    
    # Parse theme color (fallback to safe corporate blue)
    primary_color = "4472C4"
    if isinstance(theme, dict) and "primary" in theme:
        primary_color = theme["primary"].replace("#", "")
        
    # Full-bleed Dashboard Header
    ws.merge_cells("A1:R2")
    header_cell = ws["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color="FFFFFF")
    header_cell.fill = PatternFill(fill_type="solid", start_color=primary_color)
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 3. Create Stacked Column Chart (Left side, spanning full height)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.width = 14.5
    chart1.height = 11.5
    
    data1 = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    
    ws.add_chart(chart1, "B4")
    
    # 4. Create Line Chart 1 (Right side, top quadrant)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.width = 14.5
    chart2.height = 5.5
    chart2.legend = None  # Hide legend for a cleaner UI look
    
    data2 = Reference(ws_data, min_col=2, min_row=7, max_col=2, max_row=11)
    cats2 = Reference(ws_data, min_col=1, min_row=8, max_row=11)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    
    ws.add_chart(chart2, "J4")
    
    # 5. Create Line Chart 2 (Right side, bottom quadrant)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.width = 14.5
    chart3.height = 5.5
    chart3.legend = None
    
    data3 = Reference(ws_data, min_col=3, min_row=7, max_col=3, max_row=11)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats2)
    
    ws.add_chart(chart3, "J16")
```