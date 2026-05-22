### 1. High-level Skill Pattern Extraction

> **Skill Name**: App-Like Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Constructs a gridless, presentation-ready dashboard by separating data into a backend sheet and charts into a frontend sheet. Hides gridlines and row/column headers to create an app-like feel. Generates charts bound to the backend data, arranges them alongside a reserved filter sidebar pane, and hides the backend sheet entirely.
* **Applicability**: Use for building self-contained, presentation-ready dashboards. Ideal when delivering reports directly to leadership where the standard Excel grid is distracting. Constraints: Interactive Slicers cannot be fully rendered via Python/openpyxl; this shell provides the layout and data binding, reserving a visual pane to prompt the user to insert Slicers manually in Excel if interactivity is required.

### 2. Structural Breakdown

- **Data Layout**: Separates concerns into a `Dashboard` sheet (frontend layout) and a `Dashboard Data` sheet (backend tables). Backend data is structured cleanly into named Excel Tables. The backend sheet is set to `hidden`.
- **Formula Logic**: N/A (Relies on exact chart `Reference` bindings to connect frontend visuals to backend tables).
- **Visual Design**: Turns off `showGridLines` and `showRowColHeaders` on the Dashboard sheet. Uses merged regions filled with a primary theme color for a prominent title banner. Employs a shaded, bordered left pane to guide manual Slicer insertion.
- **Charts/Tables**: Top-left stacked bar chart (Market & Category), top-right line chart (Units over Time), bottom-right line chart (Profit over Time). Removes the legend on single-series line charts for a cleaner UI.
- **Theme Hooks**: Uses `primary` for the main header banner background and `text` for the header text.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.worksheet.table import Table, TableStyleInfo

    # Load palette
    try:
        from skills_library.excel.components._helpers import get_theme_palette
        palette = get_theme_palette(theme)
    except ImportError:
        palette = {"primary": "203764", "text": "FFFFFF", "bg": "F2F2F2"}

    primary_color = palette.get("primary", "203764").replace("#", "")
    text_color = palette.get("text", "FFFFFF").replace("#", "")

    # 1. Setup Backend Data Sheet
    ws_data = wb.active
    ws_data.title = "Dashboard Data"
    
    table1_start_row = 1
    table1_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62349, 4872, 21028, 25085],
        ["Philippines", 54618, 7026, 22005, 8313],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["United States", 36657, 6368, 22260, 9937],
    ]
    for r_idx, row in enumerate(table1_data, table1_start_row):
        for c_idx, val in enumerate(row, 1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)

    tab1 = Table(displayName="ProfitByMarket", ref=f"A{table1_start_row}:E{table1_start_row+4}")
    tab1.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    ws_data.add_table(tab1)

    table2_start_row = 8
    table2_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337],
    ]
    for r_idx, row in enumerate(table2_data, table2_start_row):
        for c_idx, val in enumerate(row, 1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)

    tab2 = Table(displayName="MonthlyTrends", ref=f"A{table2_start_row}:C{table2_start_row+4}")
    tab2.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    ws_data.add_table(tab2)

    # Hide backend data to create an App-like feel
    ws_data.sheet_state = 'hidden'

    # 2. Setup Frontend Dashboard Sheet
    ws_dash = wb.create_sheet(title="Dashboard", index=0)
    ws_dash.sheet_view.showGridLines = False
    ws_dash.sheet_view.showRowColHeaders = False

    # Title Banner
    ws_dash.merge_cells("B2:V4")
    for row in ws_dash.iter_rows(min_row=2, max_row=4, min_col=2, max_col=22):
        for cell in row:
            cell.fill = PatternFill("solid", fgColor=primary_color)
            
    header_cell = ws_dash["B2"]
    header_cell.value = title
    header_cell.font = Font(name="Arial", size=24, bold=True, color=text_color)
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Slicer / Filters Sidebar Placeholder
    ws_dash.merge_cells("B6:B25")
    for row in ws_dash.iter_rows(min_row=6, max_row=25, min_col=2, max_col=2):
        for cell in row:
            cell.fill = PatternFill("solid", fgColor="F2F2F2")
            
    filter_cell = ws_dash["B6"]
    filter_cell.value = "Interactive Filters\n\n(Add Excel Slicers Here)"
    filter_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    filter_cell.font = Font(color="888888", italic=True)
    
    ws_dash.column_dimensions['B'].width = 22
    ws_dash.column_dimensions['A'].width = 2

    # Chart 1: Stacked Bar (Profit by Market)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1.height = 10
    c1.width = 16
    data1_ref = Reference(ws_data, min_col=2, max_col=5, min_row=table1_start_row, max_row=table1_start_row+4)
    cats1_ref = Reference(ws_data, min_col=1, min_row=table1_start_row+1, max_row=table1_start_row+4)
    c1.add_data(data1_ref, titles_from_data=True)
    c1.set_categories(cats1_ref)
    ws_dash.add_chart(c1, "D6")

    # Chart 2: Line Chart (Units Sold)
    c2 = LineChart()
    c2.title = "Units sold each month"
    c2.height = 7
    c2.width = 14
    data2_ref = Reference(ws_data, min_col=2, max_col=2, min_row=table2_start_row, max_row=table2_start_row+4)
    cats2_ref = Reference(ws_data, min_col=1, min_row=table2_start_row+1, max_row=table2_start_row+4)
    c2.add_data(data2_ref, titles_from_data=True)
    c2.set_categories(cats2_ref)
    c2.legend = None  # Clean UI per tutorial
    ws_dash.add_chart(c2, "M6")

    # Chart 3: Line Chart (Profit)
    c3 = LineChart()
    c3.title = "Profit by month"
    c3.height = 7
    c3.width = 14
    data3_ref = Reference(ws_data, min_col=3, max_col=3, min_row=table2_start_row, max_row=table2_start_row+4)
    c3.add_data(data3_ref, titles_from_data=True)
    c3.set_categories(cats2_ref)
    c3.legend = None
    ws_dash.add_chart(c3, "M15")

    # Ensure dashboard is the default view
    wb.active = ws_dash
```