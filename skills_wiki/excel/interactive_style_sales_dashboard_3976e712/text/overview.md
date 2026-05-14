```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive-Style Sales Dashboard

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet workbook mimicking a modern, interactive web dashboard. It hides the raw calculation data on a backend sheet while using border/fill stylized cell blocks on a light gray grid to simulate floating shape "cards". It integrates Doughnut charts for KPIs, Line charts for trends, and Radar charts for categorical scores.
* **Applicability**: Best for executive summaries and high-level metric reporting where you want a clean, "UI-like" presentation format without dealing with finicky drawing shapes that can distort when rows/columns are adjusted.

### 2. Structural Breakdown

- **Data Layout**: An `Inputs` sheet structures data vertically. KPI targets are mapped into `Complete` vs `Remainder` rows (perfect for Doughnut charting). Trend lines use contiguous matrices, and satisfaction scores map category-to-float.
- **Formula Logic**: Standard percentage scaling for the KPI rings (`=Actual/Target` and `=1-Complete`).
- **Visual Design**: Uses a solid `1E3A8A` (Dark Blue) simulated side-nav bar. The worksheet background uses `F3F4F6` (Light Gray) to push white "Card" regions forward. Cards are bounded by thin `D1D5DB` borders.
- **Charts/Tables**: 
  - `DoughnutChart`: Sized down heavily with `holeSize=65` and `legend=None` to act as pure KPI micro-visuals.
  - `LineChart`: Employs a fixed y-axis scaling (min=180) to exaggerate trend movements.
  - `RadarChart`: Uses `type="filled"` to visually anchor the multiple dimensions of customer satisfaction.
- **Theme Hooks**: Background colors act as the main driver, leveraging corporate dark blue accents (`1E3A8A`) and crisp UI grays (`F3F4F6`, `6B7280`).

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import DoughnutChart, LineChart, RadarChart, Reference

def render_workbook(wb: Workbook, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup sheets
    ws_data = wb.active
    ws_data.title = "Inputs"
    ws_dash = wb.create_sheet("Dashboard")
    
    # 2. Populate Backend Data
    # KPIs for Doughnuts
    kpi_headers = ["Category", "Sales", "Profit", "Customers"]
    kpi_complete = ["Complete", 0.848, 0.89, 0.87]
    kpi_remain = ["Remainder", 0.152, 0.11, 0.13]
    for c, val in enumerate(kpi_headers, start=8): ws_data.cell(row=1, column=c, value=val)
    for c, val in enumerate(kpi_complete, start=8): ws_data.cell(row=2, column=c, value=val)
    for c, val in enumerate(kpi_remain, start=8): ws_data.cell(row=3, column=c, value=val)
    
    # Trend Data
    trend_data = [
        ["Month", "2021", "2022"],
        ["Jan", 201.9, 215.3], ["Feb", 204.2, 217.6], ["Mar", 198.6, 220.1],
        ["Apr", 199.2, 206.4], ["May", 206.4, 204.3], ["Jun", 195.1, 201.0],
        ["Jul", 192.4, 201.5], ["Aug", 189.3, 200.6], ["Sep", 194.2, 210.6],
        ["Oct", 186.5, 200.3], ["Nov", 205.2, 222.3], ["Dec", 204.3, 225.8]
    ]
    for r, row in enumerate(trend_data, start=6):
        for c, val in enumerate(row, start=1):
            ws_data.cell(row=r, column=c, value=val)
            
    # Radar Data
    radar_data = [
        ["Factor", "Score"],
        ["Speed", 0.54], ["Quality", 0.86], ["Hygiene", 0.93],
        ["Service", 0.53], ["Availability", 0.95]
    ]
    for r, row in enumerate(radar_data, start=20):
        for c, val in enumerate(row, start=5):
            ws_data.cell(row=r, column=c, value=val)

    # 3. Dashboard Shell Styling
    ws_dash.sheet_view.showGridLines = False
    
    # Grid column widths
    ws_dash.column_dimensions['A'].width = 8
    for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        ws_dash.column_dimensions[col].width = 11

    # Fills and borders
    bg_fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")
    card_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    sidebar_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    border_side = Side(border_style="thin", color="D1D5DB")

    # Apply background to grid
    for row in ws_dash.iter_rows(min_row=1, max_row=30, min_col=2, max_col=12):
        for cell in row:
            cell.fill = bg_fill
            
    # Apply simulated Sidebar
    for r in range(1, 31):
        ws_dash.cell(row=r, column=1).fill = sidebar_fill
    for r, icon in zip([4, 6, 8], ["🏠", "📊", "⚙️"]):
        c = ws_dash.cell(row=r, column=1, value=icon)
        c.font = Font(size=16)
        c.alignment = Alignment(horizontal="center", vertical="center")

    # Draw Card Helper
    def draw_card(min_row, max_row, min_col, max_col):
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws_dash.cell(row=r, column=c)
                cell.fill = card_fill
                cell.border = Border(
                    top=border_side if r == min_row else None,
                    bottom=border_side if r == max_row else None,
                    left=border_side if c == min_col else None,
                    right=border_side if c == max_col else None
                )
                
    # Create Layout Cards
    draw_card(4, 9, 2, 4)   # Sales KPI
    draw_card(4, 9, 5, 7)   # Profit KPI
    draw_card(4, 9, 8, 10)  # Customers KPI
    draw_card(11, 23, 2, 6) # Trend Area
    draw_card(11, 23, 7, 10) # Satisfaction Area

    # Title
    ws_dash["B2"] = title
    ws_dash["B2"].font = Font(size=20, bold=True, color="1E3A8A")

    # 4. Insert KPI Text & Micro Doughnut Charts
    def add_kpi(col_idx, label, val, val_format, data_col, anchor):
        # Header and Value rendering
        lbl_cell = ws_dash.cell(row=4, column=col_idx, value=label)
        lbl_cell.font = Font(bold=True, color="6B7280")
        val_cell = ws_dash.cell(row=6, column=col_idx, value=val)
        val_cell.number_format = val_format
        val_cell.font = Font(size=18, bold=True, color="1E3A8A")
        
        # Doughnut Generation
        chart = DoughnutChart()
        data = Reference(ws_data, min_col=data_col, max_col=data_col, min_row=1, max_row=3)
        cats = Reference(ws_data, min_col=8, max_col=8, min_row=2, max_row=3)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        
        # Shrink to micro-chart dimensions
        chart.width = 4.5
        chart.height = 3.0
        chart.legend = None
        chart.holeSize = 65
        chart.graphical_properties.line.noFill = True # Hide chart background boundary
        ws_dash.add_chart(chart, anchor)

    add_kpi(2, "Sales", 2544, "$#,##0", 9, "C5")
    add_kpi(5, "Profit", 890, "$#,##0", 10, "F5")
    add_kpi(8, "# of Customers", 87, "0", 11, "I5")

    # 5. Trend Line Chart
    trend_chart = LineChart()
    trend_chart.title = "2021-2022 Sales Trend (in millions)"
    t_data = Reference(ws_data, min_col=2, max_col=3, min_row=6, max_row=18)
    t_cats = Reference(ws_data, min_col=1, max_col=1, min_row=7, max_row=18)
    trend_chart.add_data(t_data, titles_from_data=True)
    trend_chart.set_categories(t_cats)
    
    trend_chart.width = 10.5
    trend_chart.height = 6.5
    trend_chart.y_axis.scaling.min = 180
    trend_chart.y_axis.scaling.max = 230
    trend_chart.graphical_properties.line.noFill = True
    ws_dash.add_chart(trend_chart, "B11")

    # 6. Radar Chart
    radar_chart = RadarChart()
    radar_chart.type = "filled"
    radar_chart.title = "Customer Satisfaction"
    r_data = Reference(ws_data, min_col=6, max_col=6, min_row=20, max_row=25)
    r_cats = Reference(ws_data, min_col=5, max_col=5, min_row=21, max_row=25)
    radar_chart.add_data(r_data, titles_from_data=True)
    radar_chart.set_categories(r_cats)
    
    radar_chart.width = 8.5
    radar_chart.height = 6.5
    radar_chart.legend = None
    radar_chart.graphical_properties.line.noFill = True
    ws_dash.add_chart(radar_chart, "G11")
    
    # Optional: Hide backing sheet to preserve application feel
    # ws_data.sheet_state = 'hidden'
```
```