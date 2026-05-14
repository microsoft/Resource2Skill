### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Tone Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a modern, sleek web-app style layout by disabling worksheet gridlines, painting a solid dark header block and a contrasting light background, and creating pseudo-shape KPI cards using merged cells and targeted cell fills. 
* **Applicability**: Best for high-level executive summaries or landing pages where you want Excel to feel like a compiled BI dashboard (like PowerBI) rather than a traditional spreadsheet. It completely avoids the unreliability of Excel Shapes in Python generation by mimicking cards with cell formatting.

### 2. Structural Breakdown

- **Data Layout**: Mock data is pushed down to row 50+ (or can be placed on a separate hidden sheet) to keep the visible viewport strictly clean for presentation.
- **Formula Logic**: Static layout shell designed to have data injected or linked.
- **Visual Design**: 
  - `ws.sheet_view.showGridLines = False` to hide the native grid.
  - Rows 1-8 receive a dark primary theme fill to create a hero header.
  - Rows 9-45 receive a light neutral fill to frame the cards and charts.
  - KPI cards mix merged cells with heavy contrast (an accent-colored icon column next to a white data column) to simulate floating dashboard widgets.
- **Charts/Tables**: Clean column and area charts are inserted with their legend moved to the top to match the horizontal aesthetic.
- **Theme Hooks**: Consumes `primary` for the header and value emphasis, `bg_light` for the canvas backdrop, and `accent` for icons and subtitles.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, AreaChart, Reference
from openpyxl.utils import get_column_letter

def render_sheet(wb: openpyxl.Workbook, sheet_name: str, *, title: str = "Sales Dashboard", subtitle: str = "Evaluating Agent Performance", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Hide native gridlines for a clean UI feel
    ws.sheet_view.showGridLines = False
    
    # Mock theme loader
    theme_palette = {
        "corporate_blue": {"primary": "003366", "bg_light": "F0F4F8", "accent": "FFC000", "text_dark": "333333"},
        "purple_gold": {"primary": "4F2B7B", "bg_light": "F2EFF5", "accent": "F2A900", "text_dark": "555555"}
    }
    palette = theme_palette.get(theme, theme_palette["purple_gold"])  # Defaulting to video's aesthetic
    
    primary = palette["primary"]
    bg_light = palette["bg_light"]
    accent = palette["accent"]
    text_dark = palette["text_dark"]
    white = "FFFFFF"
    
    fill_light = PatternFill("solid", fgColor=bg_light)
    fill_dark = PatternFill("solid", fgColor=primary)
    
    # Paint the two-tone background canvas
    for row in range(1, 45):
        for col in range(1, 23):
            ws.cell(row=row, column=col).fill = fill_dark if row <= 8 else fill_light
                
    # Insert Title & Subtitle
    title_cell = ws.cell(row=2, column=2, value=title)
    title_cell.font = Font(size=32, color=white, bold=True)
    
    sub_cell = ws.cell(row=3, column=2, value=subtitle)
    sub_cell.font = Font(size=14, color=accent)
    
    # Define KPI Strip Data
    kpis = kwargs.get("kpis", [
        ("📞", "16,749", "CALLS"),
        ("🎯", "3,328", "REACHED"),
        ("🏆", "1,203", "CLOSED"),
        ("💰", "$646k", "VALUE")
    ])
    
    # Build Pseudo-Shape KPI Cards using cells
    start_col = 2
    for icon, value, label in kpis:
        # Paint underlying cells white to prevent background bleeding on merges
        for r in range(5, 8):
            ws.cell(row=r, column=start_col).fill = PatternFill("solid", fgColor=accent)
            for c in range(start_col+1, start_col+4):
                ws.cell(row=r, column=c).fill = PatternFill("solid", fgColor=white)
                
        # 1. Icon block (Left side of card)
        ws.merge_cells(start_row=5, start_column=start_col, end_row=7, end_column=start_col)
        ic = ws.cell(row=5, column=start_col, value=icon)
        ic.font = Font(size=24, color=white)
        ic.alignment = Alignment(horizontal="center", vertical="center")
        
        # 2. Value block (Top right of card)
        ws.merge_cells(start_row=5, start_column=start_col+1, end_row=6, end_column=start_col+3)
        vc = ws.cell(row=5, column=start_col+1, value=value)
        vc.font = Font(size=20, color=primary, bold=True)
        vc.alignment = Alignment(horizontal="center", vertical="center")
        
        # 3. Label block (Bottom right of card)
        ws.merge_cells(start_row=7, start_column=start_col+1, end_row=7, end_column=start_col+3)
        lc = ws.cell(row=7, column=start_col+1, value=label)
        lc.font = Font(size=11, color=text_dark, bold=True)
        lc.alignment = Alignment(horizontal="center", vertical="center")
        
        start_col += 5

    # Refine column widths to shape the cards perfectly
    for c in [1, 6, 11, 16, 21]:
        ws.column_dimensions[get_column_letter(c)].width = 2   # Spacers
    for c in [2, 7, 12, 17]:
        ws.column_dimensions[get_column_letter(c)].width = 6   # Icon column
    for c in [3, 4, 5, 8, 9, 10, 13, 14, 15, 18, 19, 20]:
        ws.column_dimensions[get_column_letter(c)].width = 4.5 # Value/Label columns

    # Inject out-of-sight mock data for the charts
    data = [
        ["Month", "Total Sales", "Drop Rate"],
        ["Jan", 57863, 0.045],
        ["Feb", 59230, 0.050],
        ["Mar", 60127, 0.049],
        ["Apr", 58604, 0.048],
        ["May", 58261, 0.050],
        ["Jun", 59300, 0.041],
    ]
    
    data_start_row = 50
    for r_idx, row_data in enumerate(data, data_start_row):
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            if c_idx == 3 and r_idx > data_start_row:
                cell.number_format = '0.0%'
            
    cats_ref = Reference(ws, min_col=1, min_row=data_start_row+1, max_row=data_start_row+6)
                
    # Insert Chart 1: Total Sales (Column)
    sales_chart = BarChart()
    sales_chart.title = "Total Sales"
    sales_chart.style = 2
    sales_chart.y_axis.majorGridlines = None
    sales_chart.legend.position = 't'
    sales_chart.width = 15.5
    sales_chart.height = 8
    
    sales_data_ref = Reference(ws, min_col=2, min_row=data_start_row, max_row=data_start_row+6)
    sales_chart.add_data(sales_data_ref, titles_from_data=True)
    sales_chart.set_categories(cats_ref)
    
    # Color the chart series using the primary theme color
    sales_chart.series[0].graphicalProperties.solidFill = primary
    ws.add_chart(sales_chart, "B10")
    
    # Insert Chart 2: Drop Rate (Area)
    drop_chart = AreaChart()
    drop_chart.title = "Call Drop Rate %"
    drop_chart.style = 2
    drop_chart.y_axis.majorGridlines = None
    drop_chart.y_axis.number_format = '0%'
    drop_chart.legend.position = 't'
    drop_chart.width = 15.5
    drop_chart.height = 8
    
    drop_data_ref = Reference(ws, min_col=3, min_row=data_start_row, max_row=data_start_row+6)
    drop_chart.add_data(drop_data_ref, titles_from_data=True)
    drop_chart.set_categories(cats_ref)
    
    # Color the chart series using the accent theme color
    drop_chart.series[0].graphicalProperties.solidFill = accent
    ws.add_chart(drop_chart, "L10")
```