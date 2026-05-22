### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Split-Background KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Formats the worksheet with a split-color layout (dark header band, light body) to frame the canvas. Simulates interactive metric "cards" using strategically merged, bordered cell regions with large fonts and Unicode icons. Renders a summary table featuring inline `DataBarRule` conditional formatting to visually compare multiple metrics at a glance, paired with a complementary column chart.
* **Applicability**: Ideal for executive summaries and performance dashboards. Works best when you have 3-4 top-level aggregate KPIs, alongside a categorical dataset (e.g., performance by agent, region, or product) containing multiple numeric columns that benefit from inline visual benchmarking.

### 2. Structural Breakdown

- **Data Layout**: 
  - Canvas: Rows 1-8 dark colored header; Rows 9-40 light colored body.
  - KPI Cards: Anchored at Row 5, spanning 3 columns each (B:D, F:H, etc.), utilizing merged cells for separate icon and value/label regions.
  - Data Table: Anchored at B11, extending downward.
- **Formula Logic**: Primarily relies on injected static values or processed aggregations, offloading the visual heavy-lifting to conditional formatting.
- **Visual Design**: Hides default gridlines. Employs thick accent borders on the left edge of KPI cards to mimic a modern UI component.
- **Charts/Tables**: Applies categorical Data Bars to numeric columns. Integrates an OpenPyXL `BarChart` bound dynamically to the table's dimensions.
- **Theme Hooks**: Consumes `primary` (header bg), `primary_light` (body bg), `accent` (borders/icons), `card_bg`, and a suite of `bar_N` colors for the data bars.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule
from openpyxl.chart import BarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str, kpis: list, table_headers: list, table_rows: list, theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme and Palette Setup
    THEMES = {
        "corporate_blue": {
            "primary": "2F5597",
            "primary_light": "F0F4FA",
            "accent": "FFC000",
            "card_bg": "FFFFFF",
            "text_light": "FFFFFF",
            "text_dark": "000000",
            "bar_1": "5B9BD5",
            "bar_2": "ED7D31",
            "bar_3": "A5A5A5",
            "bar_4": "FFC000"
        },
        "purple_gold": {
            "primary": "4B286D",
            "primary_light": "F2EFF5",
            "accent": "FFD700",
            "card_bg": "FFFFFF",
            "text_light": "FFFFFF",
            "text_dark": "333333",
            "bar_1": "9B59B6",
            "bar_2": "F1C40F",
            "bar_3": "8E44AD",
            "bar_4": "E67E22"
        }
    }
    
    colors = THEMES.get(theme, THEMES["corporate_blue"])
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # 2. Canvas Painting (Split Background)
    fill_primary = PatternFill("solid", fgColor=colors["primary"])
    fill_light = PatternFill("solid", fgColor=colors["primary_light"])
    
    for row in range(1, 41):
        for col in range(1, 20):
            cell = ws.cell(row=row, column=col)
            if row <= 8:
                cell.fill = fill_primary
            else:
                cell.fill = fill_light
                
    # 3. Dashboard Titles
    ws["B2"] = title
    ws["B2"].font = Font(size=28, color=colors["text_light"], bold=True)
    ws["B3"] = subtitle
    ws["B3"].font = Font(size=14, color=colors["accent"], italic=True)
    
    # 4. UI KPI Cards (Built using cells and borders)
    card_cols = [2, 6, 10, 14] # Anchors: B, F, J, N
    card_fill = PatternFill("solid", fgColor=colors["card_bg"])
    accent_side = Side(style="thick", color=colors["accent"])
    
    for idx, kpi in enumerate(kpis):
        if idx >= len(card_cols): break
        c_col = card_cols[idx]
        
        # Merge regions for icon (left) and text (right)
        ws.merge_cells(start_row=5, start_column=c_col, end_row=7, end_column=c_col)
        ws.merge_cells(start_row=5, start_column=c_col+1, end_row=6, end_column=c_col+2)
        ws.merge_cells(start_row=7, start_column=c_col+1, end_row=7, end_column=c_col+2)
        
        icon_cell = ws.cell(row=5, column=c_col)
        icon_cell.value = kpi.get("icon", "◉")
        icon_cell.font = Font(size=24, color=colors["accent"])
        icon_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        val_cell = ws.cell(row=5, column=c_col+1)
        val_cell.value = kpi.get("value", "")
        val_cell.font = Font(size=20, color=colors["primary"], bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        lbl_cell = ws.cell(row=7, column=c_col+1)
        lbl_cell.value = kpi.get("label", "")
        lbl_cell.font = Font(size=11, color=colors["text_dark"], bold=True)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Border mapping logic to wrap the merged boundary
        for r in range(5, 8):
            for c in range(c_col, c_col+3):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                left = accent_side if c == c_col else None
                right = Side(style="thin", color="CCCCCC") if c == c_col+2 else None
                top = Side(style="thin", color="CCCCCC") if r == 5 else None
                bottom = Side(style="thin", color="CCCCCC") if r == 7 else None
                
                cell.border = Border(left=left, right=right, top=top, bottom=bottom)
                
    # 5. Data Table
    start_row, start_col = 11, 2
    header_fill = PatternFill("solid", fgColor=colors["primary"])
    header_font = Font(color=colors["text_light"], bold=True)
    
    for i, header in enumerate(table_headers):
        cell = ws.cell(row=start_row, column=start_col + i)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        
    for r_idx, row_data in enumerate(table_rows):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=start_row + 1 + r_idx, column=start_col + c_idx)
            cell.value = val
            if isinstance(val, (int, float)):
                if c_idx == len(row_data) - 1:
                    cell.number_format = '"$"#,##0'
                else:
                    cell.number_format = '#,##0'
                
    # 6. Inline Data Bars
    num_rows = len(table_rows)
    bar_colors = [colors["bar_1"], colors["bar_2"], colors["bar_3"], colors["bar_4"]]
    
    for i in range(1, len(table_headers)):
        col_letter = get_column_letter(start_col + i)
        range_str = f"{col_letter}{start_row + 1}:{col_letter}{start_row + num_rows}"
        bar_color = bar_colors[(i - 1) % len(bar_colors)]
        
        rule = DataBarRule(start_type='min', end_type='max', color=f"FF{bar_color}")
        ws.conditional_formatting.add(range_str, rule)
        
    # Set uniform column widths
    for c in range(2, 20):
        ws.column_dimensions[get_column_letter(c)].width = 16

    # 7. Accompanying Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Performance Overview"
    chart.y_axis.title = table_headers[-1]
    chart.legend = None

    data_ref = Reference(ws, min_col=start_col + len(table_headers) - 1, min_row=start_row, max_row=start_row + num_rows)
    cats_ref = Reference(ws, min_col=start_col, min_row=start_row + 1, max_row=start_row + num_rows)
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.width = 17
    chart.height = 12
    
    chart_col = get_column_letter(start_col + len(table_headers) + 1)
    ws.add_chart(chart, f"{chart_col}11")
```