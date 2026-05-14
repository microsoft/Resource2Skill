### 1. High-level Skill Pattern Extraction

> **Skill Name**: Modern UI Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Emulates a web-app interface using cell background colors (`PatternFill`) and selective borders to create floating "cards" on a muted canvas. Positions mini-charts (Doughnut, Line, Radar) precisely within these visual containers, stripping away default chart backgrounds to blend them seamlessly.
* **Applicability**: Perfect for high-level executive summaries and KPI tracking where visual polish, clean separation of metrics, and a modern "application" aesthetic are prioritized over dense tabular data.

### 2. Structural Breakdown

- **Data Layout**: Stores all raw chart inputs (KPI targets, trend series, radar metrics) on a separate hidden sheet (`_Data`) to keep the presentation layer pristine.
- **Formula Logic**: Structures KPI data as pairs of `[Actual, Remainder]` to easily feed the two-slice Doughnut charts.
- **Visual Design**: Uses a minimalist web palette—slate blue sidebar (`1E293B`), light gray canvas (`F3F4F6`), and white cards (`FFFFFF`) with soft gray borders (`E5E7EB`). Gridlines are disabled.
- **Charts/Tables**: Employs `DoughnutChart` for KPI completion rings, `LineChart` for trends, and `RadarChart` for multi-axis satisfaction scoring. 
- **Theme Hooks**: Hardcoded here to a modern "Slate" palette to guarantee contrast, but perfectly suited to mapping against `theme.surface_bg`, `theme.canvas_bg`, and `theme.primary`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import DoughnutChart, LineChart, RadarChart, Reference
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = 'hidden'
    
    # -------------------------------------------------------------------------
    # 1. SETUP DATA LAYER
    # -------------------------------------------------------------------------
    # KPI Doughnut Data (Actual vs Remainder to target)
    kpi_data = [
        ["KPI", "Actual", "Remainder"],
        ["Sales", 2544, 456],
        ["Profit", 890, 110],
        ["Customers", 87, 13]
    ]
    for r_idx, row in enumerate(kpi_data, start=1):
        for c_idx, val in enumerate(row, start=1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # Trend Chart Data
    trend_data = [
        ["Month", "2021", "2022"],
        ["Jan", 201, 215], ["Feb", 204, 217],
        ["Mar", 198, 220], ["Apr", 199, 206],
        ["May", 206, 204], ["Jun", 192, 203]
    ]
    for r_idx, row in enumerate(trend_data, start=10):
        for c_idx, val in enumerate(row, start=1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # Radar Chart Data
    radar_data = [
        ["Metric", "Score"],
        ["Speed", 54],
        ["Quality", 86],
        ["Hygiene", 93],
        ["Service", 53],
        ["Availability", 95]
    ]
    for r_idx, row in enumerate(radar_data, start=20):
        for c_idx, val in enumerate(row, start=1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # -------------------------------------------------------------------------
    # 2. DESIGN CANVAS & SIDEBAR
    # -------------------------------------------------------------------------
    ws.sheet_view.showGridLines = False
    
    bg_canvas = "F3F4F6"    # Tailwind Gray-100
    bg_sidebar = "1E293B"   # Tailwind Slate-800
    bg_card = "FFFFFF"
    border_card = "E5E7EB"
    text_dark = "0F172A"

    # Paint Main Canvas
    canvas_fill = PatternFill(start_color=bg_canvas, end_color=bg_canvas, fill_type="solid")
    for r in range(1, 25):
        for c in range(2, 18): # B to Q
            ws.cell(row=r, column=c).fill = canvas_fill

    # Paint Sidebar
    sidebar_fill = PatternFill(start_color=bg_sidebar, end_color=bg_sidebar, fill_type="solid")
    for r in range(1, 25):
        ws.cell(row=r, column=1).fill = sidebar_fill

    # Sidebar Navigation Icons (Simulated via Emojis)
    icons = ["🍔", "📊", "⚙️", "❓"]
    for idx, icon in enumerate(icons):
        cell = ws.cell(row=5 + (idx * 3), column=1, value=icon)
        cell.font = Font(size=18)
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Set structural column widths and row heights
    ws.column_dimensions['A'].width = 6
    ws.column_dimensions['B'].width = 2
    ws.column_dimensions['G'].width = 2
    ws.column_dimensions['L'].width = 2
    ws.column_dimensions['Q'].width = 2
    for col in ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P']:
        ws.column_dimensions[col].width = 6
        
    ws.row_dimensions[1].height = 10
    ws.row_dimensions[4].height = 10
    ws.row_dimensions[10].height = 10

    # -------------------------------------------------------------------------
    # 3. CREATE CARDS (UI COMPONENTS)
    # -------------------------------------------------------------------------
    def create_card(min_col, min_row, max_col, max_row, card_title):
        white_fill = PatternFill(start_color=bg_card, end_color=bg_card, fill_type="solid")
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = white_fill
                
                # Draw outer borders for the card
                top = Side(style='thin', color=border_card) if r == min_row else None
                bottom = Side(style='thin', color=border_card) if r == max_row else None
                left = Side(style='thin', color=border_card) if c == min_col else None
                right = Side(style='thin', color=border_card) if c == max_col else None
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)
        
        # Inject Title
        title_cell = ws.cell(row=min_row, column=min_col, value=f"  {card_title}")
        title_cell.font = Font(name="Calibri", size=12, bold=True, color=text_dark)
        title_cell.alignment = Alignment(vertical="center")

    # Layout Execution
    create_card(3, 2, 16, 3, title)
    ws.cell(row=2, column=3).font = Font(name="Calibri", size=16, bold=True, color=text_dark)
    ws.cell(row=3, column=3, value="  Figures in millions of USD").font = Font(color="64748B", italic=True)

    create_card(3, 5, 6, 9, "Sales")
    ws.cell(row=7, column=3, value=f"  ${kpi_data[1][1]:,}").font = Font(size=22, bold=True, color=text_dark)
    
    create_card(8, 5, 11, 9, "Profit")
    ws.cell(row=7, column=8, value=f"  ${kpi_data[2][1]:,}").font = Font(size=22, bold=True, color=text_dark)

    create_card(13, 5, 16, 9, "# of Customers")
    ws.cell(row=7, column=13, value=f"  {kpi_data[3][1]:,}").font = Font(size=22, bold=True, color=text_dark)

    create_card(3, 11, 9, 23, "2021-2022 Sales Trend")
    create_card(11, 11, 16, 23, "Customer Satisfaction")

    # -------------------------------------------------------------------------
    # 4. INJECT CHARTS
    # -------------------------------------------------------------------------
    # KPI Doughnuts
    for i, col_offset in enumerate([3, 8, 13], start=1):
        donut = DoughnutChart()
        lbls = Reference(data_ws, min_col=2, min_row=1, max_col=3, max_row=1)
        data = Reference(data_ws, min_col=2, min_row=i+1, max_col=3, max_row=i+1)
        
        donut.add_data(data, from_rows=True)
        donut.set_categories(lbls)
        donut.width = 4.5
        donut.height = 3.0
        donut.legend = None
        donut.graphical_properties.line.noFill = True  # Hide border to blend into card
        
        ws.add_chart(donut, f"{get_column_letter(col_offset+2)}5")

    # Line Chart
    line_chart = LineChart()
    data = Reference(data_ws, min_col=2, min_row=10, max_col=3, max_row=16)
    cats = Reference(data_ws, min_col=1, min_row=11, max_row=16)
    
    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(cats)
    line_chart.title = None
    line_chart.width = 11.5
    line_chart.height = 6.5
    line_chart.legend.position = 'b'
    line_chart.graphical_properties.line.noFill = True
    
    ws.add_chart(line_chart, "C13")

    # Radar Chart
    radar = RadarChart()
    radar.type = "filled"
    labels = Reference(data_ws, min_col=1, min_row=21, max_row=25)
    data = Reference(data_ws, min_col=2, min_row=20, max_row=25)
    
    radar.add_data(data, titles_from_data=True)
    radar.set_categories(labels)
    radar.title = None
    radar.width = 9.5
    radar.height = 6.5
    radar.legend = None
    radar.graphical_properties.line.noFill = True
    
    ws.add_chart(radar, "K13")
```