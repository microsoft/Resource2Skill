### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid-Based Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Simulates a modern, web-like dashboard UI using a purely cell-based grid. It disables gridlines, applies a subdued background fill to the entire visible worksheet, and creates "cards" by filling specific ranges with white and applying thin borders. KPI text and charts are then anchored onto these fixed card regions.
* **Applicability**: Use when building executive dashboards that require a clean, segmented UI. It avoids the brittleness of using floating shape rectangles for layout containers, ensuring charts and KPIs stay perfectly aligned with columns and rows when the sheet is viewed or printed.

### 2. Structural Breakdown

- **Data Layout**: Defines a tightly controlled column grid (margins, gaps, and equal-width card columns) to create a structured 4-column layout for KPIs and a 2-column layout for larger charts.
- **Formula Logic**: Static values are injected in this shell, though typically the KPI value cells would reference sumifs or pivot tables on a hidden calculation sheet.
- **Visual Design**: Uses a light gray sheet background (`F3F4F6`) to make white (`FFFFFF`) cards pop. KPI values use bold, large fonts, accented with smaller colored variance indicators (green/red).
- **Charts/Tables**: Empty charts (Line, Doughnut) are configured to specific cm dimensions so they sit exactly inside the lower card ranges without overlapping the card borders.
- **Theme Hooks**: Background colors, text colors, and chart palettes can be parameterized by standard theme tokens (e.g., `theme.bg_primary`, `theme.text_secondary`).

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import LineChart, DoughnutChart

def draw_card(ws, start_row, start_col, end_row, end_col, bg_color="FFFFFF", border_color="CCCCCC"):
    """Fills a range of cells to look like a UI card."""
    fill = PatternFill("solid", fgColor=bg_color)
    thin_border = Side(border_style="thin", color=border_color)
    
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            cell = ws.cell(row=row, column=col)
            cell.fill = fill
            
            # Apply borders only to the outer edges of the card block
            top = thin_border if row == start_row else None
            bottom = thin_border if row == end_row else None
            left = thin_border if col == start_col else None
            right = thin_border if col == end_col else None
            
            cell.border = Border(top=top, bottom=bottom, left=left, right=right)

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", data: dict = None, **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    if not data:
        data = {
            "kpis": [
                {"title": "TOTAL REVENUE", "value": 213983614, "format": "£#,##0", "var": "1.8% ▲", "var_color": "008800"},
                {"title": "TOTAL PROFIT", "value": 56429310, "format": "£#,##0", "var": "0.5% ▼", "var_color": "CC0000"},
                {"title": "PROFIT MARGIN", "value": 0.2637, "format": "0.00%", "var": "1.2% ▲", "var_color": "008800"},
                {"title": "UNITS SOLD", "value": 1350956, "format": "#,##0", "var": "4.5% ▲", "var_color": "008800"}
            ]
        }
        
    bg_fill = PatternFill("solid", fgColor="F3F4F6")
    
    # 1. Fill background for the visible dashboard area
    for row in range(1, 40):
        for col in range(1, 18):
            ws.cell(row=row, column=col).fill = bg_fill
            
    # 2. Configure Grid Widths (Columns B-P used for content)
    col_widths = {
        'A': 2, 'E': 2, 'I': 2, 'M': 2, 'Q': 2,    # Margins & Vertical Gaps
        'B': 10, 'C': 10, 'D': 10,                 # Card 1 block
        'F': 10, 'G': 10, 'H': 10,                 # Card 2 block
        'J': 10, 'K': 10, 'L': 10,                 # Card 3 block
        'N': 10, 'O': 10, 'P': 10                  # Card 4 block
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width
        
    # 3. Draw Header Container
    draw_card(ws, 2, 2, 3, 16)
    header_cell = ws.cell(row=2, column=2, value=title)
    header_cell.font = Font(size=18, bold=True, color="333333")
    header_cell.alignment = Alignment(vertical="center")
    ws.merge_cells(start_row=2, start_column=2, end_row=3, end_column=16)
    
    # 4. Draw KPI Cards
    col_starts = [2, 6, 10, 14]
    for i, kpi in enumerate(data.get("kpis", [])):
        if i > 3: break
        start_col = col_starts[i]
        draw_card(ws, 5, start_col, 8, start_col + 2)
        
        # KPI Title
        t_cell = ws.cell(row=5, column=start_col, value=kpi["title"])
        t_cell.font = Font(size=9, bold=True, color="666666")
        ws.merge_cells(start_row=5, start_column=start_col, end_row=5, end_column=start_col + 2)
        
        # KPI Value
        v_cell = ws.cell(row=6, column=start_col, value=kpi["value"])
        v_cell.number_format = kpi["format"]
        v_cell.font = Font(size=16, bold=True, color="111111")
        ws.merge_cells(start_row=6, start_column=start_col, end_row=7, end_column=start_col + 2)
        
        # KPI Variance
        var_cell = ws.cell(row=8, column=start_col, value=kpi["var"])
        var_cell.font = Font(size=9, bold=True, color=kpi.get("var_color", "008800"))
        var_cell.alignment = Alignment(horizontal="right")
        ws.merge_cells(start_row=8, start_column=start_col, end_row=8, end_column=start_col + 2)
        
    # 5. Draw Chart Card Containers
    draw_card(ws, 10, 2, 22, 8)   # Chart 1 area (spans across card block 1 & 2)
    draw_card(ws, 10, 10, 22, 16) # Chart 2 area (spans across card block 3 & 4)
    draw_card(ws, 24, 2, 36, 8)   # Chart 3 area
    draw_card(ws, 24, 10, 36, 16) # Chart 4 area
    
    # 6. Place Charts onto Cards
    # In a real scenario, Series() data would be injected here from a hidden pivot/calculation sheet.
    chart1 = LineChart()
    chart1.title = "Revenue Trend vs Budget"
    chart1.height = 6.5
    chart1.width = 12.5 # Sized to nest neatly inside the drawn borders
    chart1.legend = None
    ws.add_chart(chart1, "B10")
    
    chart2 = DoughnutChart()
    chart2.title = "Profit by Segment"
    chart2.height = 6.5
    chart2.width = 12.5
    ws.add_chart(chart2, "J10")
```