```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Side-Panel Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Divides a worksheet into two distinct visual zones using `PatternFill` across column ranges: a dark, narrow sidebar on the left and a light, wide main content area on the right. It injects high-contrast KPI metric blocks into the sidebar, hides gridlines, and renders clean, white "card" regions in the main area to neatly house charts or tables.
* **Applicability**: Ideal for executive summaries, KPI scorecards, or high-level overview dashboards where 4-6 crucial top-level metrics must remain permanently visible alongside detailed charts. 

### 2. Structural Breakdown

- **Data Layout**: Accepts a `kpis` list containing dictionaries with `label` and `value` keys. The sidebar operates on fixed rows/columns, stacking these KPIs vertically.
- **Formula Logic**: Primarily structural; relies on pre-calculated values passed into the rendering function rather than sheet-level formulas.
- **Visual Design**: Two-tone layout (dark sidebar Columns A-C, light main area Columns D-N). Hides standard Excel gridlines. KPI values use large (size 20), bold typography. Chart areas use a solid white fill with thin, light-gray borders to mimic web UI "cards".
- **Charts/Tables**: Generates merged, styled placeholder cards indicating exactly where openpyxl charts (like LineCharts or BarCharts) should be anchored later in the generation pipeline.
- **Theme Hooks**: Consumes `sidebar_bg`, `main_bg`, `text_inv` (inverse text for the dark sidebar), and `text_main` to ensure the dashboard seamlessly adapts to corporate branding.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str, kpis: list = None, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Internal palette fallback for standalone execution
    themes = {
        "corporate_blue": {"sidebar_bg": "1F4E78", "main_bg": "F2F2F2", "text_inv": "FFFFFF", "text_main": "000000", "card_bg": "FFFFFF", "border": "D9D9D9"},
        "forest_green": {"sidebar_bg": "2E4E3F", "main_bg": "EAF0EC", "text_inv": "FFFFFF", "text_main": "1A1A1A", "card_bg": "FFFFFF", "border": "CCD5D0"},
        "dark_mode": {"sidebar_bg": "18181B", "main_bg": "2D2D30", "text_inv": "E0E0E0", "text_main": "FFFFFF", "card_bg": "3E3E42", "border": "555555"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    fill_sidebar = PatternFill(start_color=palette["sidebar_bg"], end_color=palette["sidebar_bg"], fill_type="solid")
    fill_main = PatternFill(start_color=palette["main_bg"], end_color=palette["main_bg"], fill_type="solid")
    fill_card = PatternFill(start_color=palette["card_bg"], end_color=palette["card_bg"], fill_type="solid")
    
    font_title = Font(name="Calibri", size=24, bold=True, color=palette["text_main"])
    font_kpi_label = Font(name="Calibri", size=12, color=palette["text_inv"])
    font_kpi_value = Font(name="Calibri", size=20, bold=True, color=palette["text_inv"])
    
    # 1. Apply Layout & Background Zones
    ws.column_dimensions['A'].width = 2
    ws.column_dimensions['B'].width = 22
    ws.column_dimensions['C'].width = 2
    for col in 'DEFGHIJKLMN':
        ws.column_dimensions[col].width = 12
        
    for row in range(1, 40):
        for col_idx in range(1, 4): # Cols A, B, C
            ws.cell(row=row, column=col_idx).fill = fill_sidebar
        for col_idx in range(4, 15): # Cols D through N
            ws.cell(row=row, column=col_idx).fill = fill_main
            
    # 2. Add Title in Main Area
    title_cell = ws['D2']
    title_cell.value = title
    title_cell.font = font_title
    
    # 3. Render KPIs in Sidebar
    if not kpis:
        kpis = [
            {"label": "Total Orders", "value": "2,400"},
            {"label": "Total Revenue", "value": "$649.0K"},
            {"label": "Avg. Rating", "value": "4.0"},
            {"label": "Avg. Days to Deliver", "value": "2.3"}
        ]
        
    current_row = 5
    for kpi in kpis:
        lbl_cell = ws.cell(row=current_row, column=2)
        lbl_cell.value = kpi["label"]
        lbl_cell.font = font_kpi_label
        lbl_cell.alignment = Alignment(horizontal="center")
        
        val_cell = ws.cell(row=current_row+1, column=2)
        val_cell.value = kpi["value"]
        val_cell.font = font_kpi_value
        val_cell.alignment = Alignment(horizontal="center")
        
        current_row += 4 # Vertical spacing between KPI blocks
        
    # 4. Create Web-style "Card" Placeholders in Main Panel
    border_thin = Side(border_style="thin", color=palette["border"])
    box_border = Border(top=border_thin, left=border_thin, right=border_thin, bottom=border_thin)
    
    def create_card(start_col, start_row, end_col, end_row, card_title):
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=end_row, end_column=end_col)
        top_left = ws.cell(row=start_row, column=start_col)
        top_left.value = card_title
        top_left.font = Font(name="Calibri", size=14, color=palette["text_main"])
        top_left.alignment = Alignment(horizontal="center", vertical="center")
        
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_card
                # Apply outline border to the merged region exterior
                if r == start_row: cell.border = Border(top=border_thin)
                if r == end_row: cell.border = Border(bottom=border_thin)
                if c == start_col: cell.border = Border(left=border_thin)
                if c == end_col: cell.border = Border(right=border_thin)
                # Fix corners
                if r == start_row and c == start_col: cell.border = Border(top=border_thin, left=border_thin)
                if r == start_row and c == end_col: cell.border = Border(top=border_thin, right=border_thin)
                if r == end_row and c == start_col: cell.border = Border(bottom=border_thin, left=border_thin)
                if r == end_row and c == end_col: cell.border = Border(bottom=border_thin, right=border_thin)

    create_card(5, 5, 9, 16, "Revenue Trend (Placeholder)")
    create_card(10, 5, 14, 16, "Purchase Platforms (Placeholder)")
    create_card(5, 18, 14, 29, "Geographic Distribution (Placeholder)")

    # 5. Hide standard gridlines for a clean dashboard look
    ws.sheet_view.showGridLines = False
```
```