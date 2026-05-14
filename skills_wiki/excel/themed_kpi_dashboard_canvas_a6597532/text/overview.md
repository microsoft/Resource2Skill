### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Generates a complete executive dashboard layout using disabled gridlines, a unified deep-color header band, cell-merged KPI cards with thick accent borders, and data tables enhanced with inline conditional formatting (Data Bars).
* **Applicability**: Perfect for high-level summary reports or executive dashboards where metrics need to be presented cleanly alongside a summary table and visual charts, bypassing the need for complex shape objects by utilizing clever cell formatting.

### 2. Structural Breakdown

- **Data Layout**: Top header spans rows 1-4. KPI cards use merged cells in rows 6-8. Main data table begins at row 11 on the left, with an accompanying chart on the right.
- **Formula Logic**: Static layout generation (can be linked to data via external formulas or populated directly).
- **Visual Design**: Uses a deep colored background for the header (`header_bg`), contrasting white cards with thick left borders (`accent`) to mimic floating UI elements, and a pale sheet background (`sheet_bg`) for contrast.
- **Charts/Tables**: Includes a column chart with disabled gridlines and a summary table equipped with `DataBarRule` conditional formatting for instant visual comparison.
- **Theme Hooks**: Consumes `header_bg`, `sheet_bg`, `accent`, `text_light`, `text_dark`, and `bar_fill`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import DataBarRule

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str, kpis: list[dict], table_headers: list[str], table_data: list[list], theme: str = "executive_purple", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Theme Configuration
    themes = {
        "executive_purple": {"header_bg": "4B286D", "sheet_bg": "F4F2F7", "accent": "F2C811", "text_light": "FFFFFF", "text_dark": "333333", "bar_fill": "A38CCC"},
        "corporate_blue": {"header_bg": "1F4E78", "sheet_bg": "F2F5F8", "accent": "FFD966", "text_light": "FFFFFF", "text_dark": "222222", "bar_fill": "8EA9DB"}
    }
    t = themes.get(theme, themes["corporate_blue"])

    header_fill = PatternFill("solid", fgColor=t["header_bg"])
    sheet_fill = PatternFill("solid", fgColor=t["sheet_bg"])
    card_fill = PatternFill("solid", fgColor="FFFFFF")

    # 2. Paint Backgrounds
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=20):
        for cell in row:
            cell.fill = header_fill if cell.row <= 4 else sheet_fill

    # 3. Header Titles
    ws["B2"] = title
    ws["B2"].font = Font(size=26, color=t["text_light"], bold=True)
    ws["B3"] = subtitle
    ws["B3"].font = Font(size=14, color=t["accent"])

    # 4. KPI Cards
    start_col = 3 # Start at Column C
    thin_border = Side(style='thin', color="DDDDDD")
    
    for kpi in kpis:
        # Merge cells for structure
        ws.merge_cells(start_row=6, start_column=start_col, end_row=6, end_column=start_col+1)
        ws.merge_cells(start_row=7, start_column=start_col, end_row=7, end_column=start_col+1)
        ws.merge_cells(start_row=8, start_column=start_col, end_row=8, end_column=start_col+1)
        
        val_cell = ws.cell(row=6, column=start_col)
        lbl_cell = ws.cell(row=7, column=start_col)
        
        # Values
        val_cell.value = kpi["value"]
        val_cell.font = Font(size=20, color=t["header_bg"], bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="bottom")
        if isinstance(kpi["value"], (int, float)):
            val_cell.number_format = '#,##0' if kpi["value"] > 1000 else '0.0%' if isinstance(kpi["value"], float) and kpi["value"] <= 1 else '0'
                
        # Labels
        lbl_cell.value = str(kpi["label"]).upper()
        lbl_cell.font = Font(size=10, color=t["text_dark"])
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")
        
        # Apply Card Styling (Floating effect with accent left-border)
        for r in range(6, 9):
            for c in range(start_col, start_col+2):
                c_cell = ws.cell(row=r, column=c)
                c_cell.fill = card_fill
                
                b_top = thin_border if r == 6 else None
                b_bot = thin_border if r == 8 else None
                b_right = thin_border if c == start_col+1 else None
                b_left = Side(style='thick', color=t["accent"]) if c == start_col else None
                
                c_cell.border = Border(top=b_top, bottom=b_bot, left=b_left, right=b_right)

        start_col += 3

    # 5. Data Table
    table_start_row = 11
    table_start_col = 2
    
    # Write Headers
    for i, h in enumerate(table_headers):
        cell = ws.cell(row=table_start_row, column=table_start_col + i)
        cell.value = h
        cell.font = Font(bold=True, color=t["text_light"])
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    # Write Data
    for r_idx, row_data in enumerate(table_data, start=table_start_row + 1):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=r_idx, column=table_start_col + c_idx)
            cell.value = val
            if isinstance(val, (int, float)):
                cell.number_format = '#,##0'

    # Apply Data Bars to Numeric Columns
    data_end_row = table_start_row + len(table_data)
    rule = DataBarRule(start_type='min', end_type='max', color="FF" + t["bar_fill"])
    
    for col_offset in range(1, len(table_headers)):
        col_letter = openpyxl.utils.get_column_letter(table_start_col + col_offset)
        range_str = f"{col_letter}{table_start_row + 1}:{col_letter}{data_end_row}"
        ws.conditional_formatting.add(range_str, rule)

    # Clean up Column Widths
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 15
    for c in range(3, 15):
        ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = 12

    # 6. Complementary Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 11
    chart.title = "Core Metrics Comparison"
    
    # Plot first two numeric columns against the category labels
    data_ref = Reference(ws, min_col=table_start_col+1, min_row=table_start_row, max_col=table_start_col+2, max_row=data_end_row)
    cats_ref = Reference(ws, min_col=table_start_col, min_row=table_start_row+1, max_row=data_end_row)
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.shape = 4
    chart.y_axis.majorGridlines = None
    chart.legend = None

    ws.add_chart(chart, "H11")
```