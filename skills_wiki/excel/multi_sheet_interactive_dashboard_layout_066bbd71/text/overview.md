### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Sheet Interactive Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Builds a modular dashboard architecture by separating concerns across three sheets: a `Raw Data` sheet holding an Excel Table, a hidden `ChartData` sheet for aggregations, and a polished `Dashboard` sheet. The dashboard utilizes floating charts and a designated sidebar container for user controls (Slicers/Timelines), while turning off gridlines for a clean, app-like appearance.
* **Applicability**: Ideal for business performance reports, KPI tracking, and analytical overviews where data needs to be separated from the presentation layer. Simulates the structure of a PivotTable-driven dashboard.

### 2. Structural Breakdown

- **Data Layout**: 
  - `Raw Data`: Contains a structured Excel Table.
  - `ChartData` (Hidden): Contains summarized metric tables.
  - `Dashboard`: Row 2-4 is a merged title banner. Column B-C is a merged sidebar panel.
- **Formula Logic**: Aggregations are represented as hard values in the `ChartData` sheet, establishing the necessary contiguous ranges for the charts to reference.
- **Visual Design**: Gridlines are disabled on the Dashboard. The banner uses the theme's `primary` color with large bold text. The sidebar uses the `accent` color with a custom thin outer border.
- **Charts/Tables**: 
  - Contains a `BarChart` (stacked column) and two `LineChart`s anchored seamlessly onto the dashboard layout.
  - Uses `Table` with `TableStyleMedium9` for the raw data ingest.
- **Theme Hooks**: Consumes `primary` (Banner), `accent` (Sidebar), `text_light` (Banner text), and `text_dark` (Sidebar instruction text).

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.worksheet.table import Table, TableStyleInfo
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

    # 1. Setup Theme Fallbacks
    themes = {
        "corporate_blue": {"primary": "003366", "secondary": "4F81BD", "accent": "F2F2F2", "text_light": "FFFFFF", "text_dark": "000000"},
        "emerald_green": {"primary": "006633", "secondary": "339966", "accent": "EAF5F0", "text_light": "FFFFFF", "text_dark": "000000"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Raw Data Sheet
    ws_data = wb.active
    ws_data.title = "Raw Data"
    raw_data = [
        ["Date", "Market", "Product", "Units Sold", "Profit"],
        ["2020-09-01", "India", "Chocolate Chip", 1500, 3200],
        ["2020-10-01", "USA", "Oatmeal Raisin", 2100, 4100],
        ["2020-11-01", "UK", "Snickerdoodle", 1800, 3500],
        ["2020-12-01", "Philippines", "Fortune Cookie", 3000, 6000],
    ]
    for row in raw_data:
        ws_data.append(row)
    
    tab = Table(displayName="PerformanceData", ref=f"A1:E{len(raw_data)}")
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    ws_data.add_table(tab)

    # 3. Hidden Chart Data Sheet
    ws_chart = wb.create_sheet("ChartData")
    
    summary_data_1 = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62000, 4800, 21000, 25000],
        ["Philippines", 54000, 7000, 22000, 8000],
        ["UK", 46000, 5200, 11000, 14000],
        ["USA", 36000, 6300, 22000, 9000],
    ]
    start_row_1 = 1
    for row in summary_data_1: 
        ws_chart.append(row)
    end_row_1 = ws_chart.max_row
    ws_chart.append([])

    summary_data_2 = [
        ["Month", "Units Sold"],
        ["Sep", 50000], ["Oct", 95000], ["Nov", 65000], ["Dec", 52000],
    ]
    start_row_2 = ws_chart.max_row + 1
    for row in summary_data_2: 
        ws_chart.append(row)
    end_row_2 = ws_chart.max_row
    ws_chart.append([])

    summary_data_3 = [
        ["Month", "Profit"],
        ["Sep", 124000], ["Oct", 228000], ["Nov", 160000], ["Dec", 136000],
    ]
    start_row_3 = ws_chart.max_row + 1
    for row in summary_data_3: 
        ws_chart.append(row)
    end_row_3 = ws_chart.max_row

    ws_chart.sheet_state = 'hidden'

    # Build chart data references
    data1 = Reference(ws_chart, min_col=2, min_row=start_row_1, max_col=5, max_row=end_row_1)
    cats1 = Reference(ws_chart, min_col=1, min_row=start_row_1+1, max_row=end_row_1)
    
    data2 = Reference(ws_chart, min_col=2, min_row=start_row_2, max_col=2, max_row=end_row_2)
    cats2 = Reference(ws_chart, min_col=1, min_row=start_row_2+1, max_row=end_row_2)
    
    data3 = Reference(ws_chart, min_col=2, min_row=start_row_3, max_col=2, max_row=end_row_3)
    cats3 = Reference(ws_chart, min_col=1, min_row=start_row_3+1, max_row=end_row_3)

    # 4. Dashboard Presentation Sheet
    ws_dash = wb.create_sheet("Dashboard", 0)
    ws_dash.sheet_view.showGridLines = False
    
    # Render Banner
    ws_dash.merge_cells("B2:P4")
    banner = ws_dash["B2"]
    banner.value = title
    banner.font = Font(color=palette["text_light"], size=24, bold=True)
    banner.alignment = Alignment(vertical="center", horizontal="left", indent=1)
    fill_primary = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    for row in ws_dash.iter_rows(min_col=2, max_col=16, min_row=2, max_row=4):
        for cell in row: 
            cell.fill = fill_primary

    # Render Slicer/Control Sidebar
    ws_dash.merge_cells("B6:C35")
    sidebar = ws_dash["B6"]
    sidebar.value = "Control Panel\n\n(Add Slicers & Timelines Here)"
    sidebar.font = Font(color=palette["text_dark"], italic=True)
    sidebar.alignment = Alignment(vertical="top", horizontal="center", wrap_text=True)
    fill_accent = PatternFill(start_color=palette["accent"], end_color=palette["accent"], fill_type="solid")
    thin_edge = Side(style="thin", color="CCCCCC")
    
    # Apply precise outer border to the merged sidebar region
    for r_idx in range(6, 36):
        for c_idx in range(2, 4):
            cell = ws_dash.cell(row=r_idx, column=c_idx)
            cell.fill = fill_accent
            cell.border = Border(
                top=thin_edge if r_idx == 6 else None,
                bottom=thin_edge if r_idx == 35 else None,
                left=thin_edge if c_idx == 2 else None,
                right=thin_edge if c_idx == 3 else None
            )

    # Adjust Key Column Widths
    ws_dash.column_dimensions['A'].width = 2
    ws_dash.column_dimensions['B'].width = 20
    ws_dash.column_dimensions['C'].width = 5
    ws_dash.column_dimensions['D'].width = 2

    # Attach Charts
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    chart1.legend.position = 'b'
    chart1.width = 15
    chart1.height = 12
    ws_dash.add_chart(chart1, "E6")

    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.legend = None
    chart2.width = 15
    chart2.height = 7.5
    ws_dash.add_chart(chart2, "K6")

    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    chart3.legend = None
    chart3.width = 15
    chart3.height = 7.5
    ws_dash.add_chart(chart3, "K20")
```