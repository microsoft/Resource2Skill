### 1. High-level Skill Pattern Extraction

> **Skill Name**: Side-Panel KPI Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Formats a worksheet as a dashboard canvas with a distinctive two-tone layout: a dark vertical left panel for primary KPI callouts and a lighter, spacious right canvas for charts and tables. While the tutorial uses floating shape text boxes for the KPIs, this programmatic equivalent achieves the exact same visual cleanly by turning off gridlines, applying band fills, and using precisely sized merged cells with inverted typography.
* **Applicability**: General-purpose dashboard landing pages. Perfect for executive summaries where 3-5 high-level metrics need to be anchored persistently on the left, supporting detailed interactive charts in the main viewing area.

### 2. Structural Breakdown

- **Data Layout**: Column A acts as a narrow padding margin. Columns B:C are widened to form the KPI sidebar. Columns D:N form the main chart canvas. 
- **Formula Logic**: Standard cell values are populated in the script, but in a full archetype, these would contain `=` links pointing back to a hidden `Pivot` calculation sheet (e.g., `=Pivots!B4`).
- **Visual Design**: Gridlines are completely disabled. The sidebar (Cols B-C) uses `theme.primary` (dark) with `theme.text_light` (white) for high-contrast visibility. The main canvas uses `theme.background` (off-white/light) for a clean chart backdrop.
- **Charts/Tables**: Leaves the main canvas area open for subsequent component rendering (like clustered column charts or trendlines).
- **Theme Hooks**: `primary` (sidebar background), `text_light` (KPI values), `background` (main canvas area), `primary` (Main title text).

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str = "Executive Summary", kpis: list = None, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    
    # Fallback theme palette - in a full implementation, this would be loaded via a theme helper
    themes = {
        "corporate_blue": {
            "primary": "1F4E78",      # Dark Blue
            "background": "F2F2F2",   # Off-white
            "text_light": "FFFFFF",   # White
            "text_muted": "A6A6A6",   # Light Grey
        },
        "forest_green": {
            "primary": "274E13",      # Dark Green (similar to the tutorial)
            "background": "EAF1E9",   # Very Light Green
            "text_light": "FFFFFF",
            "text_muted": "B6D7A8",
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # Define Fills and Fonts
    bg_sidebar = PatternFill("solid", fgColor=palette["primary"])
    bg_canvas = PatternFill("solid", fgColor=palette["background"])
    
    font_title = Font(name="Arial", size=22, bold=True, color=palette["primary"])
    font_kpi_label = Font(name="Arial", size=11, bold=True, color=palette["text_muted"])
    font_kpi_val = Font(name="Arial", size=20, bold=True, color=palette["text_light"])

    # Initialize Sheet
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Configure Layout Widths
    ws.column_dimensions['A'].width = 2    # Left margin padding
    ws.column_dimensions['B'].width = 14   # Sidebar left half
    ws.column_dimensions['C'].width = 14   # Sidebar right half
    for col in "DEFGHIJKLMN":
        ws.column_dimensions[col].width = 12 # Main canvas columns

    # Apply Dual-Tone Background Fills
    for row in range(1, 40):
        # Left Sidebar (Columns B and C)
        for col in range(2, 4): 
            ws.cell(row=row, column=col).fill = bg_sidebar
        # Main Canvas (Columns D through N)
        for col in range(4, 15): 
            ws.cell(row=row, column=col).fill = bg_canvas

    # Render Main Canvas Title
    title_cell = ws['D2']
    title_cell.value = title
    title_cell.font = font_title
    title_cell.alignment = Alignment(vertical="center")

    # Default KPIs if none provided
    if not kpis:
        kpis = [
            {"label": "Total Orders", "value": "2,400"},
            {"label": "Total Quantity", "value": "11,997"},
            {"label": "Total Revenue", "value": "$649.0K"},
            {"label": "Avg. Rating", "value": "4.0"},
            {"label": "Days to Deliver", "value": "2.3"}
        ]

    # Render Sidebar KPI Blocks
    start_row = 4
    for kpi in kpis:
        lbl_cell = ws.cell(row=start_row, column=2)
        val_cell = ws.cell(row=start_row+1, column=2)

        # Merge across columns B and C for wide text anchoring
        ws.merge_cells(start_row=start_row, start_column=2, end_row=start_row, end_column=3)
        ws.merge_cells(start_row=start_row+1, start_column=2, end_row=start_row+1, end_column=3)

        lbl_cell.value = kpi["label"].upper()
        lbl_cell.font = font_kpi_label
        lbl_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)

        val_cell.value = kpi["value"]
        val_cell.font = font_kpi_val
        val_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)

        start_row += 4 # Vertical spacing between KPI blocks
```