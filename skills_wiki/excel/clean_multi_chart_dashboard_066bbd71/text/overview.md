### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Multi-Chart Dashboard

* **Tier**: archetype
* **Core Mechanism**: Generates a multi-sheet workbook architecture by isolating aggregated metrics on a "Data" sheet and presenting them visually on a "Dashboard" sheet. The dashboard uses explicit cell anchoring to arrange multiple charts (stacked columns, lines) into a grid layout, while turning off standard Excel gridlines for a polished, app-like feel.
* **Applicability**: Best for executive summaries, performance overviews, and KPI reporting. Use this pattern when you need a structured, static snapshot of multiple metrics arranged cleanly without the clutter of raw tabular data.

### 2. Structural Breakdown

- **Data Layout**: Two distinct worksheets. A "Data" sheet holding distinct tabular regions (matrix and time-series), and a "Dashboard" sheet acting purely as a presentation layer.
- **Formula Logic**: Assumes aggregated metrics are fed directly into the Data sheet to bypass the need for complex, engine-dependent PivotTables.
- **Visual Design**: The dashboard features `showGridLines = False` and a merged, color-filled header block spanning the top rows to establish a strong visual hierarchy.
- **Charts/Tables**: Uses a `BarChart` configured with `grouping="stacked"` and `overlap=100` alongside multiple `LineChart` objects, all pulling from the `Reference` ranges on the Data sheet.
- **Theme Hooks**: `primary` color is consumed by the dashboard's main header background block, with text contrasting in white.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Define basic theme palette fallback
    themes = {
        "corporate_blue": {"primary": "2F5597", "bg": "FFFFFF", "text": "000000"},
        "forest_green": {"primary": "385723", "bg": "FFFFFF", "text": "000000"},
        "dark_mode": {"primary": "4472C4", "bg": "1E1E1E", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Setup worksheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_data = wb.create_sheet(title="Data")

    # -------------------------------------------------------------------------
    # 3. Populate Data Sheet (Hidden backend for charts)
    # -------------------------------------------------------------------------
    
    # Dataset A: Profit by Market & Product (Matrix for Stacked Bar)
    market_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"],
        ["India", 62349, 4872, 21028, 18560],
        ["United States", 36657, 6368, 22260, 9937],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["Philippines", 54618, 7026, 22005, 8313],
    ]
    
    for r_idx, row in enumerate(market_data, start=1):
        for c_idx, val in enumerate(row, start=1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)

    # Dataset B: Monthly Trends (Time-series for Line Charts)
    monthly_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337],
    ]
    
    start_r = len(market_data) + 3
    for r_idx, row in enumerate(monthly_data, start=start_r):
        for c_idx, val in enumerate(row, start=1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)

    # -------------------------------------------------------------------------
    # 4. Setup Dashboard Sheet Layout & Header
    # -------------------------------------------------------------------------
    
    # Turn off gridlines for a clean "application" look
    ws_dash.sheet_view.showGridLines = False
    
    # Create a prominent dashboard title banner
    ws_dash.merge_cells("A1:P2")
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color="FFFFFF")
    header_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # -------------------------------------------------------------------------
    # 5. Build and Anchor Charts
    # -------------------------------------------------------------------------
    
    # Chart 1: Stacked Bar Chart (Main left quadrant)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.height = 14
    chart1.width = 16
    
    data1 = Reference(ws_data, min_col=2, min_row=1, max_col=5, max_row=5)
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    ws_dash.add_chart(chart1, "B4")

    # Chart 2: Line Chart (Top right quadrant)
    chart2 = LineChart()
    chart2.title = "Units Sold Each Month"
    chart2.height = 7
    chart2.width = 13
    
    data2 = Reference(ws_data, min_col=2, min_row=start_r, max_row=start_r+4)
    cats2 = Reference(ws_data, min_col=1, min_row=start_r+1, max_row=start_r+4)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    ws_dash.add_chart(chart2, "I4")

    # Chart 3: Line Chart (Bottom right quadrant)
    chart3 = LineChart()
    chart3.title = "Profit by Month"
    chart3.height = 7
    chart3.width = 13
    
    data3 = Reference(ws_data, min_col=3, min_row=start_r, max_row=start_r+4)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats2)  # Share the same time-series categories
    ws_dash.add_chart(chart3, "I18")
```