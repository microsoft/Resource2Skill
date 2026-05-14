### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Create a sleek dashboard canvas by disabling gridlines, applying a two-tone structural background fill, and using merged cells with thick left-borders to simulate floating KPI shape cards (bypassing openpyxl's lack of support for drawing auto-shapes).
* **Applicability**: Essential foundation for any executive dashboard or summary report. Provides a clean, modern frame to hold data tables, charts, and high-level metric readouts.

### 2. Structural Breakdown

- **Data Layout**: Wide padding column A. Header region spans rows 1-8. Body region spans rows 9-40. 
- **Formula Logic**: Static text values for layout framework; designed to be populated by downstream component rendering.
- **Visual Design**: Gridlines off. Dark primary color for the header block, light pastel fill for the body block. 
- **Charts/Tables**: Employs cell merging (`F2:H4`, etc.) and selective `Border(left=Side(style='thick'))` to mimic the look of floating rounded rectangles shown in the UI.
- **Theme Hooks**: Consumes `header_bg`, `body_bg`, `text`, and `accent` to color coordinate the background regions, typography, and KPI card accents.

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", subtitle: str = "Evaluating Sales Agent Performance", theme: str = "purple_sleek", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # 1. Theme Configuration
    theme_colors = {
        "purple_sleek": {"header_bg": "FF4B286D", "body_bg": "FFF3E5F5", "text": "FFFFFFFF", "accent": "FFFFC000"},
        "corporate_blue": {"header_bg": "FF003366", "body_bg": "FFF0F4F8", "text": "FFFFFFFF", "accent": "FFFFD700"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    # 2. Paint Dashboard Canvas
    header_fill = PatternFill(fill_type="solid", fgColor=palette["header_bg"])
    body_fill = PatternFill(fill_type="solid", fgColor=palette["body_bg"])
    
    for row in range(1, 9):
        for col in range(1, 25):
            ws.cell(row=row, column=col).fill = header_fill
            
    for row in range(9, 41):
        for col in range(1, 25):
            ws.cell(row=row, column=col).fill = body_fill
            
    # 3. Add Typography
    ws.column_dimensions['A'].width = 3.0
    ws.column_dimensions['B'].width = 40.0
    
    t_cell = ws.cell(row=2, column=2, value=title)
    t_cell.font = Font(name="Aptos Narrow", size=32, color=palette["text"], bold=True)
    
    s_cell = ws.cell(row=4, column=2, value=subtitle)
    s_cell.font = Font(name="Aptos Narrow", size=14, color=palette["accent"])
    
    # 4. KPI Card Generator (Simulating floating Shapes via Cell Merges)
    def build_kpi_card(start_row, start_col, value, label):
        end_row = start_row + 3
        end_col = start_col + 2
        
        # Merge top 3 rows for the metric value, bottom row for the label
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row+2, end_column=end_col)
        ws.merge_cells(start_row=end_row, start_column=start_col, end_row=end_row, end_column=end_col)
        
        val_cell = ws.cell(row=start_row, column=start_col, value=value)
        val_cell.font = Font(size=22, color=palette["header_bg"], bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        lbl_cell = ws.cell(row=end_row, column=start_col, value=label)
        lbl_cell.font = Font(size=11, color=palette["header_bg"], bold=True)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Apply white background and structural borders to mimic a card
        accent_edge = Side(border_style="thick", color=palette["accent"])
        thin_edge = Side(border_style="thin", color="FFE0E0E0")
        white_fill = PatternFill(fill_type="solid", fgColor="FFFFFFFF")
        
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = white_fill
                
                # Apply the thick accent color strictly to the left edge of the block
                cell.border = Border(
                    left=accent_edge if c == start_col else None,
                    right=thin_edge if c == end_col else None,
                    top=thin_edge if r == start_row else None,
                    bottom=thin_edge if r == end_row else None
                )

    # 5. Place KPI Cards in the Header Area
    # Standardize column widths for an even KPI grid
    for col_letter in ['F', 'G', 'H', 'J', 'K', 'L', 'N', 'O', 'P']:
        ws.column_dimensions[col_letter].width = 6.0
    for spacer in ['I', 'M']:
        ws.column_dimensions[spacer].width = 3.0
        
    build_kpi_card(2, 6, "16,749", "TOTAL CALLS")
    build_kpi_card(2, 10, "3,328", "REACHED")
    build_kpi_card(2, 14, "1,203", "DEALS CLOSED")
```