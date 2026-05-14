### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Layout & KPI Strip

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a sleek, dashboard-style worksheet layout without relying on floating shapes. Uses global background color fills to simulate a web-like canvas, a contrasting deep header block, and merged cell ranges with thick left-side borders to simulate standalone KPI cards. Applies Data Bar conditional formatting to inline tables for fast visual analysis.
* **Applicability**: Ideal for executive summaries, high-level reporting, and "landing pages" for workbooks where you need a polished, modern aesthetic that remains robust and purely cell-based.

### 2. Structural Breakdown

- **Data Layout**: Global background fill simulates a canvas. Rows 1-4 act as a full-width header. Rows 6-9 act as a KPI strip where pairs of columns form individual cards separated by a narrow spacer column.
- **Formula Logic**: Purely layout-driven in this shell, serving as an anchor for data injection.
- **Visual Design**: Uses structural borders (`left=Side(style="thick")`) to mimic the colored accent bars often seen on modern UI cards. Disables gridlines globally to clean the visual space.
- **Charts/Tables**: Injects a custom-styled table starting at row 12, adding an inline `DataBarRule` to visually rank the final numeric column (e.g., Revenue or Deal Value) directly within the grid.
- **Theme Hooks**: Consumes `bg`, `header`, `text_light`, `card_bg`, and multiple accents (`accent1`, `accent2`) to tie the canvas, headers, KPI accents, and data bars into a cohesive palette.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str = "", kpis: list = None, table_data: list = None, theme: str = "sleek_purple", **kwargs) -> None:
    """
    Renders a sleek dashboard shell with a header, KPI card strip, and a data table.
    
    :param kpis: List of dicts e.g., [{"label": "CALLS", "value": 16749, "format": "#,##0", "accent": "accent1"}]
    :param table_data: 2D list of data for the main table, where row 0 is headers.
    """
    # 1. Theme definitions (fallback included for self-containment)
    themes = {
        "corporate_blue": {
            "bg": "F0F4F8", "header": "102A43", "text_light": "FFFFFF", "text_sub": "BCCCDC", 
            "card_bg": "FFFFFF", "card_lbl": "829AB1", "accent1": "2680EB", "accent2": "486581"
        },
        "sleek_purple": {
            "bg": "F2EFF5", "header": "5E1F6B", "text_light": "FFFFFF", "text_sub": "E0D4E5", 
            "card_bg": "FFFFFF", "card_lbl": "8E44AD", "accent1": "D4AF37", "accent2": "8E44AD"
        },
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Canvas Setup
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    fill_bg = PatternFill("solid", fgColor=palette["bg"])
    fill_header = PatternFill("solid", fgColor=palette["header"])
    fill_card = PatternFill("solid", fgColor=palette["card_bg"])

    # Apply global background to a broad canvas area
    for row in ws.iter_rows(min_row=1, max_row=50, min_col=1, max_col=20):
        for cell in row:
            cell.fill = fill_bg

    # 3. Header Block (Rows 1-4)
    for row in ws.iter_rows(min_row=1, max_row=4, min_col=1, max_col=20):
        for cell in row:
            cell.fill = fill_header

    ws["B2"] = title
    ws["B2"].font = Font(size=24, bold=True, color=palette["text_light"])
    ws["B3"] = subtitle
    ws["B3"].font = Font(size=14, color=palette["text_sub"])

    # 4. KPI Strip Simulation (Using Cells as Cards)
    if kpis:
        start_row = 6
        start_col = 2 # B
        for i, kpi in enumerate(kpis):
            col = start_col + (i * 2) # Render cards in cols B, D, F, H...
            
            card_cells = [
                ws.cell(row=start_row, column=col),     # Top padding
                ws.cell(row=start_row+1, column=col),   # Value
                ws.cell(row=start_row+2, column=col),   # Label
                ws.cell(row=start_row+3, column=col)    # Bottom padding
            ]
            
            # Resolve accent color
            accent_key = kpi.get("accent", "accent1")
            accent_color = palette.get(accent_key, palette["accent1"])
            
            thick_left = Side(style="thick", color=accent_color)
            thin_edge = Side(style="thin", color="DCDCDC")
            
            # Format the cell block to look like a floating card
            for r_idx, cell in enumerate(card_cells):
                cell.fill = fill_card
                cell.alignment = Alignment(horizontal="center", vertical="center")
                
                # Apply borders to box the column, using thick left side for style
                if r_idx == 0:
                    cell.border = Border(left=thick_left, top=thin_edge, right=thin_edge)
                elif r_idx == 3:
                    cell.border = Border(left=thick_left, bottom=thin_edge, right=thin_edge)
                else:
                    cell.border = Border(left=thick_left, right=thin_edge)

            # Inject KPI Data
            val_cell, lbl_cell = card_cells[1], card_cells[2]
            
            val_cell.value = kpi.get("value", "")
            if "format" in kpi:
                val_cell.number_format = kpi["format"]
            val_cell.font = Font(size=20, bold=True, color=palette["header"])
            
            lbl_cell.value = str(kpi.get("label", "")).upper()
            lbl_cell.font = Font(size=10, bold=True, color=palette["card_lbl"])
            
            # Manage Column Widths
            ws.column_dimensions[val_cell.column_letter].width = 18
            spacer_col = ws.cell(row=1, column=col+1).column_letter
            ws.column_dimensions[spacer_col].width = 3

    # 5. Dashboard Data Table with Data Bars
    if table_data:
        t_start_row = 12
        t_start_col = 2
        num_cols = len(table_data[0])
        
        for r_idx, row_data in enumerate(table_data):
            for c_idx, val in enumerate(row_data):
                cell = ws.cell(row=t_start_row + r_idx, column=t_start_col + c_idx)
                cell.value = val
                
                if r_idx == 0:
                    # Table Header
                    cell.fill = fill_header
                    cell.font = Font(bold=True, color=palette["text_light"])
                    cell.alignment = Alignment(horizontal="center")
                else:
                    # Table Body
                    cell.fill = fill_card
                    cell.border = Border(bottom=Side(style="thin", color="E0E0E0"))
                    if isinstance(val, (int, float)):
                        # Simple format detection based on header name
                        header_name = str(table_data[0][c_idx]).lower()
                        cell.number_format = '"$"#,##0' if "value" in header_name or "revenue" in header_name else "#,##0"
                        
        # Ensure column widths fit the table
        for c_idx in range(num_cols):
            ws.column_dimensions[ws.cell(row=1, column=t_start_col + c_idx).column_letter].width = 16
            
        # Add Data Bars to the final numeric column
        if len(table_data) > 1 and num_cols > 1:
            last_col_letter = ws.cell(row=1, column=t_start_col + num_cols - 1).column_letter
            data_range = f"{last_col_letter}{t_start_row+1}:{last_col_letter}{t_start_row + len(table_data) - 1}"
            
            # Formatting ARGB color hex for the DataBar Rule
            accent_hex = palette["accent2"]
            if len(accent_hex) == 6:
                accent_hex = "FF" + accent_hex
                
            rule = DataBarRule(start_type='min', end_type='max', color=accent_hex)
            ws.conditional_formatting.add(data_range, rule)
```