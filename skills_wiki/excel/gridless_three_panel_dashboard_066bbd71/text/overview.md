### 1. High-level Skill Pattern Extraction

> **Skill Name**: Gridless Three-Panel Dashboard

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet workbook separating raw data from presentation. The dashboard sheet disables gridlines, establishes a unified title banner, and precisely positions a primary stacked column chart alongside two secondary line charts for a clean, executive-level layout.
* **Applicability**: Ideal for static or template-driven executive dashboards where multiple key metrics (e.g., categorical breakdown vs. time-series trends) must be presented together on a single, clutter-free canvas.

### 2. Structural Breakdown

- **Data Layout**: Data sits on a separate, hidden `DashboardData` sheet in simple tabular structures. The main dashboard sheet uses no cells for data entry, serving purely as a canvas for floating chart objects.
- **Formula Logic**: Relies on pre-aggregated data written to the hidden sheet (emulating Pivot Table outputs without the interactive overhead).
- **Visual Design**: Gridlines are disabled via `ws.sheet_view.showGridLines = False`. A prominent 3-row-high header banner anchors the top of the sheet, providing a professional presentation layer.
- **Charts/Tables**: Uses a `BarChart` (grouped as "stacked") for primary categorical comparisons and two `LineChart` objects for trend analysis. Single-series legends are explicitly removed to reduce chart clutter.
- **Theme Hooks**: Consumes `header_bg` and `header_fg` (or general primary/accent colors) to style the dashboard's unified title banner.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Font, PatternFill, Alignment

    # Fallback theme colors
    header_bg = "1F4E78"
    header_fg = "FFFFFF"

    # 1. Setup Data Sheet (Emulating aggregated Pivot data)
    ws_data = wb.create_sheet("DashboardData")
    ws_data.sheet_state = 'hidden'

    # Table 1: Profit by Market & Cookie Type
    data1 = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62000, 4800, 21000],
        ["Philippines", 54000, 7000, 22000],
        ["United Kingdom", 46000, 5000, 11000],
        ["United States", 36000, 6000, 22000]
    ]
    for row_idx, row in enumerate(data1, 1):
        for col_idx, val in enumerate(row, 1):
            ws_data.cell(row=row_idx, column=col_idx, value=val)

    # Table 2: Units Sold each Month
    data2 = [
        ["Month", "Units Sold"],
        ["Sep", 50000],
        ["Oct", 95000],
        ["Nov", 65000],
        ["Dec", 52000]
    ]
    for row_idx, row in enumerate(data2, 1):
        for col_idx, val in enumerate(row, 6): # Write to cols F, G
            ws_data.cell(row=row_idx, column=col_idx, value=val)

    # Table 3: Profit by Month
    data3 = [
        ["Month", "Profit"],
        ["Sep", 124000],
        ["Oct", 228000],
        ["Nov", 160000],
        ["Dec", 136000]
    ]
    for row_idx, row in enumerate(data3, 1):
        for col_idx, val in enumerate(row, 9): # Write to cols I, J
            ws_data.cell(row=row_idx, column=col_idx, value=val)

    # 2. Setup Dashboard Sheet
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False

    # Create Title Banner
    for row in ws_dash.iter_rows(min_row=1, max_row=3, min_col=1, max_col=16):
        for cell in row:
            cell.fill = PatternFill(fill_type="solid", start_color=header_bg)

    ws_dash.merge_cells("A1:P3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=header_fg)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Build & Position Charts
    # Chart 1: Stacked Column (Profit by Market & Cookie)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1.width = 18
    c1.height = 12.5
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    data_ref1 = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    c1.add_data(data_ref1, titles_from_data=True)
    c1.set_categories(cats1)
    ws_dash.add_chart(c1, "B5")

    # Chart 2: Line (Units sold each month)
    c2 = LineChart()
    c2.title = "Units sold each month"
    c2.width = 14
    c2.height = 6
    c2.legend = None # Remove single-series legend
    cats2 = Reference(ws_data, min_col=6, min_row=2, max_row=5)
    data_ref2 = Reference(ws_data, min_col=7, min_row=1, max_row=5)
    c2.add_data(data_ref2, titles_from_data=True)
    c2.set_categories(cats2)
    ws_dash.add_chart(c2, "J5")

    # Chart 3: Line (Profit by month)
    c3 = LineChart()
    c3.title = "Profit by month"
    c3.width = 14
    c3.height = 6
    c3.legend = None # Remove single-series legend
    cats3 = Reference(ws_data, min_col=9, min_row=2, max_row=5)
    data_ref3 = Reference(ws_data, min_col=10, min_row=1, max_row=5)
    c3.add_data(data_ref3, titles_from_data=True)
    c3.set_categories(cats3)
    ws_dash.add_chart(c3, "J16")
```