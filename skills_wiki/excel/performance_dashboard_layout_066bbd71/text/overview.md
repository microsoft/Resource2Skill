### 1. High-level Skill Pattern Extraction

> **Skill Name**: Performance Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Generates a clean, presentation-ready dashboard by disabling gridlines, adding a branded title banner, and carefully aligning multiple complementary charts (stacked columns and trend lines) into a unified grid. 
* **Applicability**: Ideal for generating automated executive summaries and KPI dashboards where a clean, "app-like" visual layout is required, serving as a robust static alternative to interactive slicer-based dashboards.

### 2. Structural Breakdown

- **Data Layout**: Places underlying data on a separate "Chart Data" worksheet, keeping the primary "Dashboard" sheet clean and strictly for presentation.
- **Formula Logic**: Relies on direct openpyxl `Reference` ranges for chart series rather than dynamic formulas.
- **Visual Design**: Hides gridlines via `sheet_view.showGridLines = False`. Implements a thick top title banner using merged cells, bold light-colored text, and a primary brand background color.
- **Charts/Tables**: Creates one `BarChart` (stacked columns for categorical composition) and two `LineChart`s (for time-series trends), manually configuring height and width to align flawlessly in a standard column grid.
- **Theme Hooks**: Utilizes `primary` for the top dashboard banner and `text_light` for the title text.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import PatternFill, Font, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference

    # 1. Self-contained theme fallback
    themes = {
        "corporate_blue": {"primary": "1F4E78", "text_light": "FFFFFF"},
        "emerald_green": {"primary": "215E39", "text_light": "FFFFFF"},
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # Clean up default sheet
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    # 2. Setup Data Sheet
    ws_data = wb.create_sheet("Chart Data")
    
    chart1_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62000, 23000, 21000],
        ["Philippines", 54000, 24000, 22000],
        ["United Kingdom", 46000, 26000, 11000],
        ["Malaysia", 46000, 20000, 17000],
        ["United States", 36000, 32000, 22000],
    ]
    for row in chart1_data:
        ws_data.append(row)
        
    chart2_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337],
    ]
    start_row = len(chart1_data) + 3
    for row in chart2_data:
        ws_data.append(row)

    # Format numbers
    for row in ws_data.iter_rows(min_row=2, max_row=6, min_col=2, max_col=4):
        for cell in row:
            cell.number_format = "$#,##0"
    for row in ws_data.iter_rows(min_row=start_row+1, max_row=start_row+4, min_col=2, max_col=2):
        for cell in row:
            cell.number_format = "#,##0"
    for row in ws_data.iter_rows(min_row=start_row+1, max_row=start_row+4, min_col=3, max_col=3):
        for cell in row:
            cell.number_format = "$#,##0"

    # 3. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard", 0)
    ws_dash.sheet_view.showGridLines = False

    # Title Banner
    ws_dash.merge_cells("A1:Q3")
    title_cell = ws_dash["A1"]
    title_cell.value = f"  {title}"
    title_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    title_cell.font = Font(color=palette["text_light"], size=28, bold=True)
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    
    # Set thin column A for padding
    ws_dash.column_dimensions['A'].width = 3

    # 4. Create Stacked Bar Chart
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.height = 14
    bar_chart.width = 15
    
    data = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=6)
    cats = Reference(ws_data, min_col=1, min_row=2, max_row=6)
    bar_chart.add_data(data, titles_from_data=True)
    bar_chart.set_categories(cats)
    ws_dash.add_chart(bar_chart, "B5")

    # 5. Create Line Chart 1 (Units)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.height = 6.8
    line1.width = 15
    line1.legend = None
    data1 = Reference(ws_data, min_col=2, min_row=start_row, max_row=start_row+4)
    cats_line = Reference(ws_data, min_col=1, min_row=start_row+1, max_row=start_row+4)
    line1.add_data(data1, titles_from_data=True)
    line1.set_categories(cats_line)
    ws_dash.add_chart(line1, "J5")

    # 6. Create Line Chart 2 (Profit)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.height = 6.8
    line2.width = 15
    line2.legend = None
    data2 = Reference(ws_data, min_col=3, min_row=start_row, max_row=start_row+4)
    line2.add_data(data2, titles_from_data=True)
    line2.set_categories(cats_line)
    ws_dash.add_chart(line2, "J19")
```