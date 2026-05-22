### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Performance Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Transforms a blank worksheet into a presentation canvas by removing gridlines, creating a bold merged header banner, and orchestrating multiple Openpyxl charts (stacked column and line charts) into a multi-pane layout.
* **Applicability**: Best for summarizing organizational KPIs where a clean, non-spreadsheet visual presentation is required. Acts as a programmatic alternative to interactive PivotChart dashboards when generating static, formatted reports.

### 2. Structural Breakdown

- **Data Layout**: Consolidates raw metrics into a separate "Data" worksheet, structuring it for straightforward chart ingestion (categories in the first column, series in subsequent columns).
- **Visual Design**: Turns off `showGridLines` on the dashboard canvas. Creates a thick header strip (A1:Q3) using horizontal/vertical center alignment and a solid fill applied across all merged cells.
- **Charts/Tables**: Places a prominent `BarChart` (`grouping="stacked"`) on the left and two vertically stacked `LineChart` objects on the right, simulating a standard BI dashboard layout. 
- **Theme Hooks**: The dashboard banner relies on a primary brand background (`header_bg`) and contrasting text (`header_fg`).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Fallback Palette Setup
    palettes = {
        "corporate_blue": {"header_bg": "203764", "header_fg": "FFFFFF"},
        "modern_green": {"header_bg": "2CA02C", "header_fg": "FFFFFF"},
        "dark_slate": {"header_bg": "2F4F4F", "header_fg": "FFFFFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # 2. Setup Sheets
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
    
    ws_dash = wb.create_sheet("Dashboard", 0)
    ws_data = wb.create_sheet("Data", 1)

    # 3. Configure Dashboard Canvas
    ws_dash.sheet_view.showGridLines = False
    
    # Create Header Banner
    ws_dash.merge_cells("A1:Q3")
    header_fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    
    for row in ws_dash["A1:Q3"]:
        for cell in row:
            cell.fill = header_fill
            
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=28, bold=True, color=palette["header_fg"])
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 4. Populate Backend Data Sheet
    stacked_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62349, 4872, 21028, 25085],
        ["Philippines", 54618, 7026, 22005, 8313],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["Malaysia", 46587, 5538, 17536, 20555],
        ["United States", 36657, 6369, 22260, 9938]
    ]
    
    for row in stacked_data:
        ws_data.append(row)
        
    ws_data.append([]) # Spacer row
    
    trend_data_start = ws_data.max_row + 1
    trend_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337]
    ]
    
    for row in trend_data:
        ws_data.append(row)

    # 5. Create Dashboard Charts
    # Chart 1: Stacked Column (Profit by Market & Product)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.height = 14.0
    bar_chart.width = 16.0
    
    data_ref = Reference(ws_data, min_col=2, min_row=1, max_col=5, max_row=6)
    cats_ref = Reference(ws_data, min_col=1, min_row=2, max_row=6)
    bar_chart.add_data(data_ref, titles_from_data=True)
    bar_chart.set_categories(cats_ref)
    
    ws_dash.add_chart(bar_chart, "B5")

    # Chart 2: Line Chart (Units Sold)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.height = 6.5
    line1.width = 14.0
    
    data_ref1 = Reference(ws_data, min_col=2, min_row=trend_data_start, max_row=trend_data_start+4)
    cats_ref1 = Reference(ws_data, min_col=1, min_row=trend_data_start+1, max_row=trend_data_start+4)
    line1.add_data(data_ref1, titles_from_data=True)
    line1.set_categories(cats_ref1)
    
    ws_dash.add_chart(line1, "J5")

    # Chart 3: Line Chart (Profit)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.height = 6.5
    line2.width = 14.0
    
    data_ref2 = Reference(ws_data, min_col=3, min_row=trend_data_start, max_row=trend_data_start+4)
    line2.add_data(data_ref2, titles_from_data=True)
    line2.set_categories(cats_ref1)
    
    ws_dash.add_chart(line2, "J19")
```