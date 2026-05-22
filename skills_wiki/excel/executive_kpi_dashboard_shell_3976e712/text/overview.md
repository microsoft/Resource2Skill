### 1. High-level Skill Pattern Extraction

> **Skill Name**: Executive KPI Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Generates a modern dashboard layout by using formatted cell ranges to emulate CSS-like "panels", populating them with multiple chart types (Doughnut for KPI percentages, Line for Trends, Radar for distributions). Chart borders are hidden to seamlessly blend into the white panel backgrounds.
* **Applicability**: Best for high-level management reports requiring a clean, web-like UI in Excel without relying on fragile floating shapes. Suitable when multiple KPIs and dimensional breakdowns need to be digested at a glance.

### 2. Structural Breakdown

- **Data Layout**: Raw data is structured horizontally and written to an off-screen area (columns AA:AE) to keep the presentation layer clean.
- **Formula Logic**: Charts reference static coordinate ranges linking back to the hidden data.
- **Visual Design**: 
  - **Canvas**: Entire active sheet background is filled with a soft gray (`#F3F4F6`), and gridlines are turned off.
  - **Sidebar**: Column A uses a dark slate fill (`#1F2937`) to emulate a navigation pane.
  - **Panels**: Specific ranges are filled with white (`#FFFFFF`) and given a subtle light gray border (`#E5E7EB`) to mimic floating card UI elements.
- **Charts/Tables**: 
  - **Doughnut Charts** (Hole size 65%, no borders) for progress against targets.
  - **Line Chart** (Style 13, no borders) for monthly trends.
  - **Radar Chart** (Standard, no borders) for qualitative satisfaction scores.
  - **Bar Chart** (Horizontal, no borders) for country-level performance.
- **Theme Hooks**: Utilizes explicit modern web hex colors for the structural elements, completely bypassing the native Excel color palette for a bespoke SaaS aesthetic. 

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Border, Side, Font
from openpyxl.chart import DoughnutChart, LineChart, RadarChart, BarChart, Reference, Series
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # 1. Visual Design: Colors and Fills
    gray_fill = PatternFill("solid", fgColor="F3F4F6")
    white_fill = PatternFill("solid", fgColor="FFFFFF")
    sidebar_fill = PatternFill("solid", fgColor="1F2937")
    
    # Hide gridlines for a clean canvas
    ws.sheet_view.showGridLines = False

    # Apply gray background to the main viewable area
    for row in ws.iter_rows(min_row=1, max_row=36, min_col=2, max_col=19):
        for cell in row:
            cell.fill = gray_fill

    # Apply dark sidebar
    ws.column_dimensions['A'].width = 8
    for row in ws.iter_rows(min_row=1, max_row=36, min_col=1, max_col=1):
        for cell in row:
            cell.fill = sidebar_fill

    # Define Panel block coordinates (min_row, min_col, max_row, max_col)
    panels = [
        (4, 2, 8, 6),    # Sales KPI
        (4, 8, 8, 12),   # Profit KPI
        (4, 14, 8, 18),  # Customer KPI
        (10, 2, 21, 12), # Trend Line
        (10, 14, 21, 18),# Radar
        (23, 2, 34, 12), # Country Bar
    ]

    light_border = Border(
        left=Side(style='thin', color='E5E7EB'),
        right=Side(style='thin', color='E5E7EB'),
        top=Side(style='thin', color='E5E7EB'),
        bottom=Side(style='thin', color='E5E7EB')
    )

    for r_min, c_min, r_max, c_max in panels:
        for row in ws.iter_rows(min_row=r_min, max_row=r_max, min_col=c_min, max_col=c_max):
            for cell in row:
                cell.fill = white_fill
                cell.border = light_border

    # 2. Header
    ws.merge_cells("B2:J2")
    title_cell = ws["B2"]
    title_cell.value = title or "Executive KPI Dashboard"
    title_cell.font = Font(size=20, bold=True, color="1F2937")

    # 3. Write Off-screen Data (Columns AA:AE)
    kpi_data = [
        ["KPI", "Actual", "Target", "Complete", "Remaining"],
        ["Sales", 2544, 3000, 0.848, 0.152],
        ["Profit", 890, 1000, 0.890, 0.110],
        ["Customers", 87, 100, 0.870, 0.130]
    ]
    for r_idx, row_data in enumerate(kpi_data, 1):
        for c_idx, val in enumerate(row_data, 27):
            ws.cell(row=r_idx, column=c_idx, value=val)

    trend_data = [
        ["Month", "2021", "2022"],
        ["Jan", 201.9, 215.3], ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1], ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3], ["Jun", 195.1, 203.0],
        ["Jul", 192.4, 201.5], ["Aug", 189.3, 200.6],
        ["Sep", 194.2, 210.6], ["Oct", 186.5, 200.3],
        ["Nov", 205.2, 222.3], ["Dec", 204.3, 225.8]
    ]
    for r_idx, row_data in enumerate(trend_data, 12):
        for c_idx, val in enumerate(row_data, 27):
            ws.cell(row=r_idx, column=c_idx, value=val)

    radar_data = [
        ["Factor", "Score"],
        ["Speed", 54], ["Quality", 96],
        ["Hygiene", 93], ["Service", 53],
        ["Availability", 95]
    ]
    for r_idx, row_data in enumerate(radar_data, 26):
        for c_idx, val in enumerate(row_data, 27):
            ws.cell(row=r_idx, column=c_idx, value=val)

    country_data = [
        ["Country", "Sales"],
        ["Argentina", 953.3], ["Brazil", 553.2],
        ["Colombia", 432.4], ["Ecuador", 445.1],
        ["Peru", 425.1], ["Bolivia", 387.5], ["Chile", 253.6]
    ]
    for r_idx, row_data in enumerate(country_data, 33):
        for c_idx, val in enumerate(row_data, 27):
            ws.cell(row=r_idx, column=c_idx, value=val)

    # 4. Helper to inject KPI Doughnuts
    no_line = GraphicalProperties(ln=LineProperties(noFill=True))
    
    def add_kpi(name, actual, data_row, anchor_chart, anchor_title, anchor_val):
        ws[anchor_title] = name
        ws[anchor_title].font = Font(size=12, color="6B7280", bold=True)
        ws[anchor_val] = actual
        ws[anchor_val].font = Font(size=22, bold=True, color="111827")
        if actual > 100:
            ws[anchor_val].number_format = "$#,##0"
        
        donut = DoughnutChart()
        donut.width = 2.0
        donut.height = 1.5
        donut.holeSize = 65
        donut.legend = None
        donut.spPr = no_line
        
        vals = Reference(ws, min_col=30, min_row=data_row, max_col=31, max_row=data_row)
        donut.add_data(vals, from_rows=True)
        ws.add_chart(donut, anchor_chart)

    add_kpi("Sales", 2544, 2, "D4", "B5", "B6")
    add_kpi("Profit", 890, 3, "J4", "H5", "H6")
    add_kpi("Customers", 87, 4, "P4", "N5", "N6")

    # 5. Add Line Chart
    line = LineChart()
    line.width = 8.5
    line.height = 2.8
    line.title = "2021-2022 Sales Trend (in millions)"
    line.style = 13
    line.spPr = no_line
    l_data = Reference(ws, min_col=28, min_row=12, max_col=29, max_row=24)
    l_cats = Reference(ws, min_col=27, min_row=13, max_row=24)
    line.add_data(l_data, titles_from_data=True)
    line.set_categories(l_cats)
    ws.add_chart(line, "B10")

    # 6. Add Radar Chart
    radar = RadarChart()
    radar.type = "standard"
    radar.width = 4.0
    radar.height = 2.8
    radar.title = "Customer Satisfaction"
    radar.legend = None
    radar.spPr = no_line
    r_data = Reference(ws, min_col=28, min_row=26, max_row=31)
    r_cats = Reference(ws, min_col=27, min_row=27, max_row=31)
    radar.add_data(r_data, titles_from_data=True)
    radar.set_categories(r_cats)
    ws.add_chart(radar, "N10")

    # 7. Add Bar Chart
    bar = BarChart()
    bar.type = "bar"
    bar.width = 8.5
    bar.height = 2.8
    bar.title = "Sales by Country"
    bar.legend = None
    bar.spPr = no_line
    b_data = Reference(ws, min_col=28, min_row=33, max_row=40)
    b_cats = Reference(ws, min_col=27, min_row=34, max_row=40)
    bar.add_data(b_data, titles_from_data=True)
    bar.set_categories(b_cats)
    ws.add_chart(bar, "B23")
```