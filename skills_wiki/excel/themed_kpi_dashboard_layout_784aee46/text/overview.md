```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Sets up a clean presentation canvas by turning off gridlines, merging cells for a prominent themed header, building a left-hand contextual filter pane, and arranging charts loaded from a hidden background data sheet into a structured grid.
* **Applicability**: Use when aggregating multiple charts into a complete, standalone visual dashboard interface intended for management review or presentations. 

### 2. Structural Breakdown

- **Data Layout**: Dashboard source metrics are centralized on a dedicated "DashboardData" sheet which is then hidden (`ws.sheet_state = "hidden"`) to keep the user focused entirely on the visual canvas.
- **Formula Logic**: Replaces tabular data layouts with `openpyxl.chart.Reference` ranges pulling directly from the hidden backend sheet.
- **Visual Design**: Gridlines disabled (`showGridLines = False`). A bold primary-colored header banner spans across the top (`A1:M3`). A secondary-colored left sidebar (`A5:B27`) emulates the spacing and context of interactive slicers.
- **Charts/Tables**: Employs a hero Line Chart (full width) over two supporting Clustered Bar Charts (half width each), forming a classic dashboard hierarchy. Single-series legends are removed to maximize data-ink ratio.
- **Theme Hooks**: Consumes `primary`, `secondary`, and `bg` token colors to ensure the dashboard instantly adapts to branding palettes without manual adjustments.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Heroic Insights Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import LineChart, BarChart, Reference
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

    # 1. Theme Palette Definitions
    themes = {
        "corporate_blue": {"primary": "003366", "secondary": "4F81BD", "bg": "F2F2F2"},
        "executive_dark": {"primary": "2B2B2B", "secondary": "595959", "bg": "E6E6E6"},
        "emerald_green": {"primary": "385723", "secondary": "548235", "bg": "E2EFDA"}
    }
    colors = themes.get(theme, themes["corporate_blue"])

    # 2. Prepare Data Sheet (Hidden Backend)
    ws_data = wb.active
    ws_data.title = "DashboardData"

    data_trend = [
        ["Month", "Revenue"],
        ["Jan", 15000], ["Feb", 16500], ["Mar", 18000], ["Apr", 17500],
        ["May", 19000], ["Jun", 21000], ["Jul", 22000], ["Aug", 21500],
        ["Sep", 23000], ["Oct", 24000], ["Nov", 25000], ["Dec", 27000]
    ]
    data_cat = [
        ["Category", "Units Sold"],
        ["T-shirts", 15200],
        ["Hoodies", 12400]
    ]
    data_state = [
        ["State", "Profit"],
        ["California", 45000],
        ["Texas", 38000],
        ["New York", 32000],
        ["Florida", 28000],
        ["Washington", 25000]
    ]

    for r, row in enumerate(data_trend, 1):
        ws_data.cell(row=r, column=1, value=row[0])
        ws_data.cell(row=r, column=2, value=row[1])

    for r, row in enumerate(data_cat, 1):
        ws_data.cell(row=r, column=4, value=row[0])
        ws_data.cell(row=r, column=5, value=row[1])

    for r, row in enumerate(data_state, 1):
        ws_data.cell(row=r, column=7, value=row[0])
        ws_data.cell(row=r, column=8, value=row[1])

    # Hide the data processing sheet to create an app-like feel
    ws_data.sheet_state = "hidden"

    # 3. Prepare Dashboard Canvas
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    ws_dash.column_dimensions['A'].width = 12
    ws_dash.column_dimensions['B'].width = 12

    # 4. Create Prominent Title Banner
    ws_dash.merge_cells("A1:M3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color=colors["primary"], end_color=colors["primary"], fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 5. Create Filter / Context Pane (Visual Setup)
    ws_dash.merge_cells("A5:B5")
    slicer_header = ws_dash["A5"]
    slicer_header.value = "Filters Applied"
    slicer_header.font = Font(bold=True, color="FFFFFF")
    slicer_header.fill = PatternFill(start_color=colors["secondary"], end_color=colors["secondary"], fill_type="solid")
    slicer_header.alignment = Alignment(horizontal="center")

    filters = ["Year: All", "Month: All", "State: All", "Category: All"]
    for i, f in enumerate(filters):
        row_idx = 6 + i
        ws_dash.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)
        cell = ws_dash.cell(row=row_idx, column=1)
        cell.value = f
        cell.font = Font(color="333333")
        cell.fill = PatternFill(start_color=colors["bg"], end_color=colors["bg"], fill_type="solid")
        cell.border = Border(bottom=Side(style="thin", color="CCCCCC"))
        cell.alignment = Alignment(horizontal="left", indent=1)

    # 6. Build and Arrange Charts into a Grid Layout
    # Hero Chart: Revenue Trend (Full Width)
    c1 = LineChart()
    c1.title = "Monthly Revenue Trend"
    c1.style = 13
    data1 = Reference(ws_data, min_col=2, min_row=1, max_row=13)
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=13)
    c1.add_data(data1, titles_from_data=True)
    c1.set_categories(cats1)
    c1.width = 18
    c1.height = 8
    c1.legend = None # Clean look
    ws_dash.add_chart(c1, "D5")

    # Sub Chart 1: Category Split (Half Width)
    c2 = BarChart()
    c2.title = "Units Sold by Category"
    c2.style = 10
    data2 = Reference(ws_data, min_col=5, min_row=1, max_row=3)
    cats2 = Reference(ws_data, min_col=4, min_row=2, max_row=3)
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats2)
    c2.width = 9
    c2.height = 8
    c2.legend = None
    ws_dash.add_chart(c2, "D20")

    # Sub Chart 2: State Performance (Half Width)
    c3 = BarChart()
    c3.title = "Top States by Profit"
    c3.style = 10
    data3 = Reference(ws_data, min_col=8, min_row=1, max_row=6)
    cats3 = Reference(ws_data, min_col=7, min_row=2, max_row=6)
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(cats3)
    c3.width = 9
    c3.height = 8
    c3.legend = None
    ws_dash.add_chart(c3, "I20")

    # Present user with the dashboard directly on open
    wb.active = wb['Dashboard']
```
```