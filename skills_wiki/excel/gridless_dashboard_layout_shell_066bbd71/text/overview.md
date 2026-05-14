### 1. High-level Skill Pattern Extraction

> **Skill Name**: Gridless Dashboard Layout Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Disables sheet gridlines, constructs a full-width themed corporate banner, creates a shaded side-panel area for controls (like Slicers), and precisely anchors multiple Openpyxl charts into a clean, presentation-ready grid. 
* **Applicability**: Best used as the "front page" or executive summary of an Excel report. Transforms separate analytical outputs into a unified BI-style dashboard within standard Excel, guiding the user's eye to high-level KPIs and trends.

### 2. Structural Breakdown

- **Data Layout**: Employs an orchestration pattern where raw chart data is isolated on a secondary hidden sheet (`{sheet_name}_Data`), keeping the presentation layer completely clean.
- **Formula Logic**: Purely visualization-focused; aggregates are assumed to be pre-calculated in the hidden data sheet.
- **Visual Design**: Turns off `showGridLines`. Uses a heavy, high-contrast banner header (A1:T3). Paints a subtle gray/themed background for the "Controls" sidebar (B5:D35). 
- **Charts/Tables**: Integrates a primary Stacked Column chart and two secondary Line charts, manually adjusting width/height constraints so they snap into a clean masonry-style grid.
- **Theme Hooks**: Utilizes a local palette dict resolving the `theme` kwarg to drive `header_bg`, `header_fg`, `panel_bg`, and the main canvas `bg`.

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import PatternFill, Font, Alignment

    # 1. Theme palette fallback mapping
    palettes = {
        "corporate_blue": {"bg": "FFFFFF", "header_bg": "203764", "header_fg": "FFFFFF", "panel_bg": "F2F2F2"},
        "dark_mode": {"bg": "1E1E1E", "header_bg": "000000", "header_fg": "FFFFFF", "panel_bg": "2D2D2D"},
        "forest_green": {"bg": "FFFFFF", "header_bg": "2E4E3F", "header_fg": "FFFFFF", "panel_bg": "E9EFEA"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # 2. Setup Data Sheet (Hidden) to feed the dashboard
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = 'hidden'

    # Bar chart data (Rows 1-4)
    data_ws.append(["Market", "Chocolate Chip", "Oatmeal Raisin", "Sugar Cookie"])
    data_ws.append(["North America", 150000, 80000, 45000])
    data_ws.append(["Europe", 120000, 60000, 30000])
    data_ws.append(["Asia", 90000, 40000, 25000])
    data_ws.append([]) # Row 5 empty

    # Line chart data 1 - Units (Rows 6-12)
    data_ws.append(["Month", "Units Sold"])
    for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun"]):
        data_ws.append([m, 10000 + (i * 1500) + (i % 2 * -500)])
    data_ws.append([]) # Row 13 empty

    # Line chart data 2 - Profit (Rows 14-20)
    data_ws.append(["Month", "Total Profit"])
    for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun"]):
        data_ws.append([m, 50000 + (i * 8000) + (i % 2 * -2000)])

    # 3. Setup Dashboard Presentation Sheet
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Apply canvas background
    bg_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=22):
        for cell in row:
            cell.fill = bg_fill

    # Render Corporate Header Banner
    ws.merge_cells("A1:V3")
    header_cell = ws["A1"]
    header_cell.value = f"  {title}"
    header_cell.font = Font(color=palette["header_fg"], size=22, bold=True)
    header_cell.fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal="left", vertical="center")

    # Render Left Side Panel (Placeholder for interactive Slicers/Timelines)
    panel_fill = PatternFill(start_color=palette["panel_bg"], end_color=palette["panel_bg"], fill_type="solid")
    for row in ws.iter_rows(min_row=5, max_row=35, min_col=2, max_col=4):
        for cell in row:
            cell.fill = panel_fill
    ws["B5"] = "Controls / Slicers"
    ws["B5"].font = Font(bold=True, size=12)
    ws["B7"] = "[ Insert Country Slicer ]"
    ws["B12"] = "[ Insert Product Slicer ]"
    ws["B17"] = "[ Insert Date Timeline ]"

    # 4. Generate and Anchor Charts
    # Primary Visual: Stacked Bar Chart
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    data = Reference(data_ws, min_col=2, min_row=1, max_col=4, max_row=4)
    cats = Reference(data_ws, min_col=1, min_row=2, max_row=4)
    bar_chart.add_data(data, titles_from_data=True)
    bar_chart.set_categories(cats)
    bar_chart.height = 14
    bar_chart.width = 18
    # Turn off legend if desired, or let it sit on the right
    ws.add_chart(bar_chart, "F5")

    # Secondary Visual A: Trend Line (Units)
    line_chart1 = LineChart()
    line_chart1.title = "Units Sold per Month"
    data_l1 = Reference(data_ws, min_col=2, min_row=6, max_row=12)
    cats_l1 = Reference(data_ws, min_col=1, min_row=7, max_row=12)
    line_chart1.add_data(data_l1, titles_from_data=True)
    line_chart1.set_categories(cats_l1)
    line_chart1.height = 7
    line_chart1.width = 15
    line_chart1.legend = None # Clean up chart clutter
    ws.add_chart(line_chart1, "P5")

    # Secondary Visual B: Trend Line (Profit)
    line_chart2 = LineChart()
    line_chart2.title = "Profit per Month"
    data_l2 = Reference(data_ws, min_col=2, min_row=14, max_row=20)
    cats_l2 = Reference(data_ws, min_col=1, min_row=15, max_row=20)
    line_chart2.add_data(data_l2, titles_from_data=True)
    line_chart2.set_categories(cats_l2)
    line_chart2.height = 7
    line_chart2.width = 15
    line_chart2.legend = None
    ws.add_chart(line_chart2, "P19")
```