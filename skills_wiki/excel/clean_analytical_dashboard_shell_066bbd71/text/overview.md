### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Analytical Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Builds a structured, presentation-ready dashboard layout on a single worksheet. Disables gridlines, constructs a prominent full-width header, reserves a shaded left pane for interactive controls (like slicers), and precisely anchors multiple charts into a defined center-and-right hierarchical grid.
* **Applicability**: Use for top-level report summaries, executive scorecards, and interactive dashboard templates. It provides a clean, app-like UI that transforms raw charts into a professional reporting surface.

### 2. Structural Breakdown

- **Data Layout**: Assumes aggregate/summary data exists. The shell builds a dedicated, hidden `_Data` sheet to hold the chart source values, keeping the main dashboard pristine.
- **Formula Logic**: Purely layout and presentation; no formulas. Charts reference the hidden data sheet.
- **Visual Design**: 
  - `sheet_view.showGridLines = False` is critical for the "app" look.
  - A merged header (A1:R3) with a deep background color provides grounding.
  - A subtle gray-shaded area (Columns A-C) acts as a side-rail for future Slicers or filter instruction text.
- **Charts/Tables**: Places a primary "hero" chart (Stacked Column) in the center, and stacks secondary contextual charts (Line Charts for time series) on the right side.
- **Theme Hooks**: `header_bg`, `header_fg`, and `panel_bg` dictate the main UI colors. 

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a complete, cleanly formatted dashboard shell.
    Includes a header, a left-side slicer panel, and a 3-chart layout.
    """
    
    # 1. Setup Main Dashboard Sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    # Disable gridlines for a clean, app-like interface
    ws.sheet_view.showGridLines = False

    # 2. Colors (Theme Fallbacks)
    # In a full framework, these are fetched dynamically via `theme`
    header_bg = "1F4E78" # Deep corporate blue
    header_fg = "FFFFFF" # White text
    panel_bg = "F3F4F6"  # Light gray for the control rail

    # 3. Header Construction
    ws.merge_cells("A1:R3")
    header_cell = ws["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color=header_fg)
    header_cell.fill = PatternFill("solid", fgColor=header_bg)
    header_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # 4. Slicer / Control Panel Rail
    # Widen columns to fit slicers comfortably
    for col in ["A", "B", "C"]:
        ws.column_dimensions[col].width = 12
    
    # Shade the left panel and give it a subtle right boundary
    panel_border = Border(right=Side(style="thin", color="D1D5DB"))
    for row in range(4, 32):
        for col in range(1, 4):
            cell = ws.cell(row=row, column=col)
            cell.fill = PatternFill("solid", fgColor=panel_bg)
            if col == 3:
                cell.border = panel_border
            
    ws["A4"].value = "Filters & Controls"
    ws["A4"].font = Font(bold=True, size=12, color="555555")
    ws["A4"].alignment = Alignment(indent=1)
    
    # 5. Create Hidden Data Sheet for Charts
    # This keeps the dashboard sheet strictly for visual elements
    data_ws_name = f"{sheet_name}_Data"
    if data_ws_name in wb.sheetnames:
        data_ws = wb[data_ws_name]
    else:
        data_ws = wb.create_sheet(data_ws_name)
    data_ws.sheet_state = 'hidden'

    # 6. Populate Mock Data into Hidden Sheet
    # Stacked Column Data (Market x Product Type)
    data_ws.append(["Market", "Choc Chip", "Fortune", "Oatmeal", "Sugar"]) # Row 1
    mock_profits = [
        ["India", 62000, 23000, 21000, 25000],
        ["Malaysia", 46000, 20000, 17000, 20000],
        ["Philippines", 54000, 24000, 22000, 8000],
        ["UK", 46000, 26000, 11000, 14000],
        ["USA", 36000, 32000, 9000, 9000]
    ]
    for r in mock_profits:
        data_ws.append(r) # Rows 2-6
        
    # Time Series Data
    data_ws.append([]) # Row 7 (Spacer)
    data_ws.append(["Month", "Units Sold", "Profit"]) # Row 8
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    units = [50, 60, 55, 80, 90, 85, 100, 110, 105, 120, 130, 150]
    for i, m in enumerate(months):
        data_ws.append([m, units[i]*1000, units[i]*12000]) # Rows 9-20

    # 7. Main Hero Chart: Stacked Column (Center anchored)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 11
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    
    data = Reference(data_ws, min_col=2, min_row=1, max_col=5, max_row=6)
    cats = Reference(data_ws, min_col=1, min_row=2, max_row=6)
    chart1.add_data(data, titles_from_data=True)
    chart1.set_categories(cats)
    
    # Sizing in cm
    chart1.height = 14.5
    chart1.width = 18.0
    ws.add_chart(chart1, "E5")

    # 8. Secondary Chart 1: Units Sold (Top Right anchored)
    chart2 = LineChart()
    chart2.title = "Units Sold Each Month"
    chart2.style = 13
    data2 = Reference(data_ws, min_col=2, min_row=8, max_row=20)
    cats2 = Reference(data_ws, min_col=1, min_row=9, max_row=20)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.height = 7.0
    chart2.width = 14.0
    chart2.legend = None  # Hide legend for a cleaner look
    ws.add_chart(chart2, "M5")

    # 9. Secondary Chart 2: Profit by Month (Bottom Right anchored)
    chart3 = LineChart()
    chart3.title = "Profit by Month"
    chart3.style = 13
    data3 = Reference(data_ws, min_col=3, min_row=8, max_row=20)
    # Reuse cats2 as the X-axis is identical
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats2)
    chart3.height = 7.0
    chart3.width = 14.0
    chart3.legend = None
    ws.add_chart(chart3, "M17")
```