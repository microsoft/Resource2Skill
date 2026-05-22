### 1. High-level Skill Pattern Extraction

> **Skill Name**: Executive Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a modern, grid-based dashboard layout using cell background fills, disabled gridlines, and a dedicated navigation sidebar. It programmatically places stylized charts (Line and Doughnut) into designated "panel" areas defined by merged and formatted cell blocks.
* **Applicability**: Best for high-level executive summaries or sales dashboards where visual structure, clear separation of KPIs, trend analysis, and completion metrics are required natively within Excel (without relying heavily on floating shape objects).

### 2. Structural Breakdown

- **Data Layout**: Dedicated data ranges injected into a hidden or remote area (simulated here in column Z onwards) to drive the charts seamlessly. Column A serves as a persistent navigation sidebar.
- **Formula Logic**: Relies on structured coordinate mapping for drawing panels and linking chart references securely to backing data.
- **Visual Design**: Gridlines are disabled globally. The background is set to a subtle light gray. Dashboard panels are defined with white backgrounds and crisp, light gray borders to simulate floating UI cards. The sidebar uses a stark dark blue fill with white text to anchor the navigation.
- **Charts/Tables**: `LineChart` for historical trends placed in the bottom-left panel. `DoughnutChart` (with enlarged hole size) for target completion placed in the bottom-right panel.
- **Theme Hooks**: Uses local palette mappings for `sidebar_bg`, `panel_bg`, `bg`, and `text` to construct the dashboard grid cohesively.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference, DoughnutChart

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Theme color definitions (fallback to modern corporate style)
    colors = {
        "sidebar_bg": "1E3A8A",   # Dark Blue
        "sidebar_fg": "FFFFFF",   # White
        "bg": "F3F4F6",           # Light Gray
        "panel_bg": "FFFFFF",     # White
        "panel_border": "E5E7EB", # Light Gray Border
        "text": "111827",         # Dark Gray/Black
        "text_muted": "6B7280"    # Medium Gray
    }
    
    # 1. Setup Base Background
    fill_bg = PatternFill("solid", fgColor=colors["bg"])
    for row in ws.iter_rows(min_row=1, max_row=30, min_col=2, max_col=15):
        for cell in row:
            cell.fill = fill_bg
            
    # 2. Setup Navigation Sidebar (Column A)
    fill_sidebar = PatternFill("solid", fgColor=colors["sidebar_bg"])
    font_sidebar = Font(color=colors["sidebar_fg"], bold=True, size=16)
    align_center = Alignment(horizontal="center", vertical="center")
    
    ws.column_dimensions['A'].width = 8
    for r in range(1, 31):
        ws.cell(row=r, column=1).fill = fill_sidebar
    
    # Sidebar navigation icons/links
    nav_items = ["🏠", "📊", "⚙️", "❓"]
    for i, item in enumerate(nav_items):
        cell = ws.cell(row=5 + i*3, column=1, value=item)
        cell.font = font_sidebar
        cell.alignment = align_center

    # 3. Header Area
    ws.cell(row=2, column=3, value=title).font = Font(size=20, bold=True, color=colors["text"])
    ws.cell(row=3, column=3, value="Figures in millions of USD").font = Font(size=11, color=colors["text_muted"], italic=True)

    # 4. Helper: Create Dashboard Panel Layout
    def create_panel(min_col, min_row, max_col, max_row, title_text):
        fill_panel = PatternFill("solid", fgColor=colors["panel_bg"])
        border_side = Side(border_style="thin", color=colors["panel_border"])
        
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_panel
                
                # Apply borders to the outer edges of the panel
                l = border_side if c == min_col else None
                r_side = border_side if c == max_col else None
                t = border_side if r == min_row else None
                b = border_side if r == max_row else None
                cell.border = Border(left=l, right=r_side, top=t, bottom=b)
                
        # Panel Title styling
        title_cell = ws.cell(row=min_row, column=min_col, value=title_text)
        title_cell.font = Font(bold=True, size=12, color=colors["text"])
        title_cell.alignment = Alignment(vertical="top")
        
        # Add slight padding row below title
        ws.row_dimensions[min_row].height = 25

    # 5. Define Grid & Create Panels
    # Adjust column widths for uniform KPI spacing
    for col in ['C', 'D', 'F', 'G', 'I', 'J']:
        ws.column_dimensions[col].width = 15
    for spacer in ['E', 'H']:
        ws.column_dimensions[spacer].width = 2

    # Top KPI Panels
    create_panel(3, 5, 4, 8, "Sales")
    ws.cell(row=7, column=3, value="$2,544").font = Font(size=24, bold=True, color=colors["text"])
    
    create_panel(6, 5, 7, 8, "Profit")
    ws.cell(row=7, column=6, value="$890").font = Font(size=24, bold=True, color=colors["text"])
    
    create_panel(9, 5, 10, 8, "# of Customers")
    ws.cell(row=7, column=9, value="87.0").font = Font(size=24, bold=True, color=colors["text"])

    # Bottom Chart Panels
    create_panel(3, 10, 7, 26, "2021-2022 Sales Trend")
    create_panel(9, 10, 13, 26, "Customer Satisfaction")

    # 6. Inject Backing Data (Hidden in columns Z+)
    data_start_col = 26
    
    # Line chart data setup
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    sales_2021 = [201.9, 204.2, 198.6, 199.2, 206.4, 200.1, 195.3]
    sales_2022 = [215.3, 217.6, 220.1, 206.4, 204.3, 215.0, 202.1]
    
    ws.cell(row=1, column=data_start_col, value="Month")
    ws.cell(row=1, column=data_start_col+1, value="2021")
    ws.cell(row=1, column=data_start_col+2, value="2022")
    
    for i, m in enumerate(months):
        ws.cell(row=2+i, column=data_start_col, value=m)
        ws.cell(row=2+i, column=data_start_col+1, value=sales_2021[i])
        ws.cell(row=2+i, column=data_start_col+2, value=sales_2022[i])
        
    # Doughnut chart data setup
    ws.cell(row=10, column=data_start_col, value="Metric")
    ws.cell(row=10, column=data_start_col+1, value="Value")
    ws.cell(row=11, column=data_start_col, value="Complete")
    ws.cell(row=11, column=data_start_col+1, value=0.87)
    ws.cell(row=12, column=data_start_col, value="Remaining")
    ws.cell(row=12, column=data_start_col+1, value=0.13)
    
    # 7. Embed Line Chart
    line_chart = LineChart()
    line_chart.title = None
    line_chart.style = 13
    line_chart.y_axis.title = "Sales ($M)"
    line_chart.x_axis.title = "Month"
    line_chart.width = 14
    line_chart.height = 7.5
    
    data = Reference(ws, min_col=data_start_col+1, min_row=1, max_col=data_start_col+2, max_row=8)
    cats = Reference(ws, min_col=data_start_col, min_row=2, max_row=8)
    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(cats)
    
    ws.add_chart(line_chart, "C12")

    # 8. Embed Doughnut Chart
    donut = DoughnutChart()
    donut.title = "Satisfaction Score"
    donut.style = 10
    donut.width = 7.5
    donut.height = 7.5
    donut.holeSize = 65
    
    data = Reference(ws, min_col=data_start_col+1, min_row=11, max_row=12)
    cats = Reference(ws, min_col=data_start_col, min_row=11, max_row=12)
    donut.add_data(data, titles_from_data=False)
    donut.set_categories(cats)
    
    ws.add_chart(donut, "I12")
```