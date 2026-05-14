```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Flat-Design Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Simulates floating UI shapes (KPI cards and seamless charts) using cell formatting. Uses `PatternFill` to create a two-tone background, merges cells with an accent-color column to create "cards", and strips borders/gridlines from charts so they blend directly into the background layer.
* **Applicability**: Best for executive summaries and static dashboards where you want a modern, web-like aesthetic without relying on fragile floating shape objects or text boxes.

### 2. Structural Breakdown

- **Data Layout**: Data for the charts is sequestered far below the visible dashboard area (e.g., row 35+) to keep the top view clean.
- **Formula Logic**: Static layout generation; no complex formulas required for the shell itself.
- **Visual Design**: Gridlines are disabled sheet-wide. Rows 1-4 use a dark primary fill, while rows 5+ use a light background fill. KPI cards use a white fill block flanked by a single-column accent fill to mimic a card border/ribbon. 
- **Charts/Tables**: `BarChart` configured with `overlap`, `gapWidth = 50`, legend repositioned to the top, and `graphical_properties.line.noFill = True` to remove the outer frame.
- **Theme Hooks**: `header_bg` (top banner), `body_bg` (main background), `card_bg` (KPI block), `accent1` (KPI ribbon), `text_light`, `text_dark`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str, kpi_data: list, chart_data: list, theme: str = "purple_gold", **kwargs) -> None:
    """
    Renders a flat-design dashboard layout with a two-tone background, KPI card strip, and embedded chart.
    
    :param kpi_data: List of dicts, e.g., [{"label": "CALLS", "value": "16,749"}, ...]
    :param chart_data: List of lists, e.g., [["Jan", 301, 115], ["Feb", 311, 110], ...]
    """
    themes = {
        "corporate_blue": {
            "header_bg": "1F4E78", "body_bg": "D9E1F2", "card_bg": "FFFFFF", 
            "accent1": "F4B084", "text_light": "FFFFFF", "text_dark": "000000"
        },
        "purple_gold": { 
            "header_bg": "4B2E83", "body_bg": "F2F0F6", "card_bg": "FFFFFF", 
            "accent1": "FFD700", "text_light": "FFFFFF", "text_dark": "333333"
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Define Fills & Fonts
    header_fill = PatternFill("solid", fgColor=palette["header_bg"])
    body_fill = PatternFill("solid", fgColor=palette["body_bg"])
    card_fill = PatternFill("solid", fgColor=palette["card_bg"])
    accent_fill = PatternFill("solid", fgColor=palette["accent1"])
    
    title_font = Font(name="Calibri", size=24, bold=True, color=palette["text_light"])
    subtitle_font = Font(name="Calibri", size=14, color=palette["text_light"])
    kpi_val_font = Font(name="Calibri", size=20, bold=True, color=palette["text_dark"])
    kpi_lbl_font = Font(name="Calibri", size=12, bold=True, color=palette["text_dark"])

    # 1. Apply Background Canvas Fills
    for row in range(1, 5):
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = header_fill
            
    for row in range(5, 30):
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = body_fill

    # 2. Header Text
    ws["B2"] = title
    ws["B2"].font = title_font
    ws["B3"] = subtitle
    ws["B3"].font = subtitle_font

    # 3. Simulate KPI Cards using Cell Blocks
    start_col = 2
    for kpi in kpi_data:
        # Merge cells for the value and label text
        ws.merge_cells(start_row=6, start_column=start_col+1, end_row=7, end_column=start_col+3)
        ws.merge_cells(start_row=8, start_column=start_col+1, end_row=8, end_column=start_col+3)
        
        # Color the left-most column as an accent ribbon, the rest white
        for r in range(6, 9):
            ws.cell(row=r, column=start_col).fill = accent_fill
            for c in range(start_col+1, start_col+4):
                ws.cell(row=r, column=c).fill = card_fill
                
        # Populate Value
        val_cell = ws.cell(row=6, column=start_col+1)
        val_cell.value = kpi["value"]
        val_cell.font = kpi_val_font
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Populate Label
        lbl_cell = ws.cell(row=8, column=start_col+1)
        lbl_cell.value = kpi["label"]
        lbl_cell.font = kpi_lbl_font
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        start_col += 5  # Step right, leaving a 1-column gap between cards

    # 4. Inject hidden/reference data for the chart (placed below the viewable area)
    data_start_row = 35
    headers = ["Month", "Metric A", "Metric B"]
    for col, header in enumerate(headers, start=2):
        ws.cell(row=data_start_row, column=col, value=header)
        
    for i, row_data in enumerate(chart_data, start=1):
        for j, val in enumerate(row_data, start=2):
            ws.cell(row=data_start_row + i, column=j, value=val)

    # 5. Configure & Embed Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Monthly Performance"
    chart.height = 10
    chart.width = 20
    
    # Clean up standard chart chrome to fit the flat aesthetic
    chart.legend.position = "t"
    chart.y_axis.majorGridlines = None
    chart.x_axis.majorGridlines = None
    chart.graphical_properties.line.noFill = True  # Removes outer border
    
    # Adjust bar proportions
    chart.gapWidth = 50
    chart.overlap = -10
    
    data = Reference(ws, min_col=3, max_col=4, min_row=data_start_row, max_row=data_start_row + len(chart_data))
    cats = Reference(ws, min_col=2, min_row=data_start_row + 1, max_row=data_start_row + len(chart_data))
    
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "B10")
    
    # 6. Normalize column widths for layout grid consistency
    for col in range(1, 20):
        ws.column_dimensions[get_column_letter(col)].width = 8
```
```