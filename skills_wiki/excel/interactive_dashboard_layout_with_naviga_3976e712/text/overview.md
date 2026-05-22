### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Dashboard Layout with Navigation Sidebar

* **Tier**: sheet_shell
* **Core Mechanism**: Builds a modern, app-like dashboard interface using cell formatting techniques. A dark-filled leftmost column serves as a navigation sidebar with hyperlink menus to other sheets. The main canvas is set to a light gray, while specifically merged and bordered cell regions act as white "cards". These cards house specialized charts (Line with custom Y-bounds, Doughnut with a customized hole size, and Radar), effectively mimicking a floating UI container.
* **Applicability**: Perfect for high-level management reports, landing pages, or automated Excel tools requiring a polished user experience, visual segmentation of metrics, and intuitive sheet-to-sheet navigation.

### 2. Structural Breakdown

- **Data Layout**: Utilizes a dedicated `Inputs` sheet to isolate raw data (trend metrics, KPI completion percentages, radar factors) from the presentation layer, keeping the dashboard clean.
- **Formula Logic**: Employs cell-based hyperlinks (e.g., `#Inputs!A1`) in the sidebar to create clickable navigation buttons without needing shapes or macros.
- **Visual Design**: Gridlines are hidden. The sidebar uses a dark theme color (e.g., primary blue) while the canvas background uses light gray. UI "cards" are achieved by filling ranges with white and applying a thin outer border.
- **Charts/Tables**: Integrates a `LineChart` (Y-axis min/max bounded to emphasize variance), a `DoughnutChart` (hole size modified to 65% for a modern KPI look), and a `RadarChart` for multi-factor performance analysis. Charts blend into the white cards naturally.
- **Theme Hooks**: The sidebar and text headers consume the `primary` theme color. The main canvas background consumes `bg_light`. The cards consume `surface` (white).

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import LineChart, DoughnutChart, RadarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup Data on a separate Inputs sheet
    inputs_ws = wb.create_sheet("Inputs")
    
    # Trend Data (Rows 1-7)
    inputs_ws.append(["Month", "2021", "2022"])
    trend_data = [
        ["Jan", 201.9, 215.3], ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1], ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3], ["Jun", 195.1, 203.0]
    ]
    for row in trend_data: 
        inputs_ws.append(row)
    
    # KPI Data (Rows 8-11)
    inputs_ws.append([])
    inputs_ws.append(["Metric", "Target %"])
    inputs_ws.append(["Complete", 0.85])
    inputs_ws.append(["Remaining", 0.15])
    
    # Radar Data (Rows 12-18)
    inputs_ws.append([])
    inputs_ws.append(["Factor", "Score"])
    radar_data = [
        ["Speed", 0.54], ["Quality", 0.86], 
        ["Hygiene", 0.91], ["Service", 0.53], ["Availability", 0.95]
    ]
    for row in radar_data: 
        inputs_ws.append(row)

    # 2. Setup Dashboard Sheet
    ws = wb.create_sheet(sheet_name, 0)
    wb.active = ws
    ws.sheet_view.showGridLines = False
    
    primary_color = "1F4E78" # Dark blue sidebar
    bg_color = "F2F2F2"      # Light gray canvas
    card_color = "FFFFFF"    # White cards
    border_color = "D9D9D9"
    
    sidebar_fill = PatternFill("solid", fgColor=primary_color)
    canvas_fill = PatternFill("solid", fgColor=bg_color)
    
    ws.column_dimensions['A'].width = 12
    for r in range(1, 30):
        ws.cell(row=r, column=1).fill = sidebar_fill
        for c in range(2, 16):
            ws.cell(row=r, column=c).fill = canvas_fill
            
    # Sidebar Navigation Links
    nav_items = [("🏠 Dash", f"'{sheet_name}'!A1"), ("⚙️ Inputs", "'Inputs'!A1")]
    for idx, (label, link) in enumerate(nav_items):
        cell = ws.cell(row=4 + idx*3, column=1, value=label)
        cell.font = Font(color="FFFFFF", bold=True, underline="single")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.hyperlink = f"#{link}"

    # 3. Helper to create UI Cards
    def make_card(start_col, start_row, end_col, end_row, title_text):
        thin = Side(border_style="thin", color=border_color)
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = PatternFill("solid", fgColor=card_color)
                
                # Apply outer border mathematically
                top = thin if r == start_row else None
                bottom = thin if r == end_row else None
                left = thin if c == start_col else None
                right = thin if c == end_col else None
                if any([top, bottom, left, right]):
                    cell.border = Border(top=top, bottom=bottom, left=left, right=right)
        
        # Insert Card Title
        title_cell = ws.cell(row=start_row, column=start_col, value=title_text)
        title_cell.font = Font(bold=True, size=12, color=primary_color)

    # Header Card
    make_card(2, 2, 14, 3, title)
    ws.cell(row=3, column=2, value="Figures in millions of USD").font = Font(italic=True, color="7F7F7F")

    # KPI Target Card
    make_card(2, 5, 5, 12, "Sales Target Completion")
    
    # 4. KPI Doughnut Chart
    donut = DoughnutChart()
    donut.title = None
    data_ref = Reference(inputs_ws, min_col=2, min_row=10, max_row=11)
    donut.add_data(data_ref, titles_from_data=False)
    donut.holeSize = 65
    donut.width = 6
    donut.height = 4
    donut.legend = None
    ws.add_chart(donut, "B6")
    
    # Trend Card
    make_card(2, 14, 8, 28, "2021-2022 Sales Trend")
    
    # 5. Sales Trend Line Chart
    line_chart = LineChart()
    line_chart.title = None
    line_chart.style = 13 # Lines with markers preset
    l_data = Reference(inputs_ws, min_col=2, min_row=1, max_col=3, max_row=7)
    l_cats = Reference(inputs_ws, min_col=1, min_row=2, max_row=7)
    line_chart.add_data(l_data, titles_from_data=True)
    line_chart.set_categories(l_cats)
    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.scaling.max = 230
    line_chart.width = 12
    line_chart.height = 7
    line_chart.legend.position = "b"
    ws.add_chart(line_chart, "B15")
    
    # Radar Card
    make_card(9, 14, 14, 28, "Customer Satisfaction")
    
    # 6. Satisfaction Radar Chart
    radar = RadarChart()
    radar.type = "standard"
    radar.title = None
    r_labels = Reference(inputs_ws, min_col=1, min_row=14, max_row=18)
    r_data = Reference(inputs_ws, min_col=2, min_row=13, max_row=18)
    radar.add_data(r_data, titles_from_data=True)
    radar.set_categories(r_labels)
    radar.width = 10
    radar.height = 7
    radar.legend = None
    ws.add_chart(radar, "I15")
```