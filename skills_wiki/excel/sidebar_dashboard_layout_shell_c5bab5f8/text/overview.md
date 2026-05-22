### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Dashboard Layout Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Configures a worksheet into a modern dashboard canvas by disabling gridlines, applying a full-height dark background to the leftmost columns to act as a sidebar (for slicers/navigation), and structuring a light-themed main area with a grid-aligned KPI card strip.
* **Applicability**: Use when scaffolding an interactive report or dashboard where you need a visually distinct control panel on the left (for Excel Slicers) and a clean, card-based canvas on the right for charts and summary metrics. 

### 2. Structural Breakdown

- **Data Layout**: Columns A and B form the left sidebar. Column C acts as a spacer. Columns D+ form the main content area. KPIs are placed in a horizontal strip across columns D, F, H, etc., starting at row 4.
- **Formula Logic**: Static assignment of KPI values and number formats (in a full application, these would map to pivot table data or `GETPIVOTDATA` references).
- **Visual Design**: Gridlines are hidden. The sidebar uses a dark theme color (e.g., dark green/blue) with white text. The main area uses a light gray/off-white background. KPI cards use a solid white fill, thin gray borders, and centered alignment to mimic floating shapes.
- **Charts/Tables**: Reserves space below the KPI strip (Rows 8+) as the designated layout zone for subsequent chart injection.
- **Theme Hooks**: Consumes `sidebar` (dark navigation fill), `bg` (main canvas background), `card` (KPI background), `text_main` (KPI values), and `text_light` (sidebar labels).

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    # 1. Theme and Palette Setup
    # Emulating the video's green aesthetic as an alternative to corporate blue
    palettes = {
        "corporate_blue": {"sidebar": "1F4E78", "bg": "F2F4F7", "card": "FFFFFF", "text_main": "000000", "text_light": "FFFFFF"},
        "california_green": {"sidebar": "2E4E3F", "bg": "E9F2E9", "card": "FFFFFF", "text_main": "1A1A1A", "text_light": "FFFFFF"} 
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # 2. Sheet Initialization
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    ws.sheet_view.showGridLines = False

    # 3. Apply Background Fills & Column Widths
    fill_sidebar = PatternFill(start_color=palette["sidebar"], fill_type="solid")
    fill_bg = PatternFill(start_color=palette["bg"], fill_type="solid")
    fill_card = PatternFill(start_color=palette["card"], fill_type="solid")

    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 4

    # Fill Sidebar (A-B) and Main BG (C-Z) up to row 50
    for row in range(1, 51):
        for col in range(1, 27):
            cell = ws.cell(row=row, column=col)
            if col <= 2:
                cell.fill = fill_sidebar
            else:
                cell.fill = fill_bg

    # 4. Header / Title Setup
    title_cell = ws.cell(row=2, column=4)
    title_cell.value = title
    title_cell.font = Font(name="Calibri", size=24, bold=True, color=palette["sidebar"])

    # 5. Sidebar Slicer/Filter Placeholder
    slicer_title = ws.cell(row=4, column=2)
    slicer_title.value = "Dashboard Filters"
    slicer_title.font = Font(name="Calibri", size=12, bold=True, color=palette["text_light"])
    slicer_title.alignment = Alignment(horizontal="left")

    # 6. KPI Card Strip Setup
    kpis = kwargs.get("kpis", [
        {"label": "Total Orders", "value": 2400, "format": "#,##0"},
        {"label": "Total Revenue", "value": 649019, "format": "$#,##0"},
        {"label": "Avg Rating", "value": 4.0, "format": "0.0"},
        {"label": "Days to Deliver", "value": 2.3, "format": "0.0"}
    ])

    start_col = 4  # Column D
    row_label = 4
    row_val = 5

    thin_border = Border(
        left=Side(style='thin', color="CCCCCC"),
        right=Side(style='thin', color="CCCCCC"),
        top=Side(style='thin', color="CCCCCC"),
        bottom=Side(style='thin', color="CCCCCC")
    )

    for kpi in kpis:
        # Size the KPI card column and the adjacent spacer column
        col_letter = get_column_letter(start_col)
        ws.column_dimensions[col_letter].width = 20
        ws.column_dimensions[get_column_letter(start_col + 1)].width = 2

        c_lbl = ws.cell(row=row_label, column=start_col)
        c_val = ws.cell(row=row_val, column=start_col)

        # KPI Label Cell
        c_lbl.value = kpi["label"]
        c_lbl.font = Font(name="Calibri", size=11, color="555555", bold=True)
        c_lbl.fill = fill_card
        c_lbl.alignment = Alignment(horizontal="center", vertical="center")
        c_lbl.border = Border(top=thin_border.top, left=thin_border.left, right=thin_border.right)

        # KPI Value Cell
        c_val.value = kpi["value"]
        c_val.number_format = kpi.get("format", "General")
        c_val.font = Font(name="Calibri", size=20, color=palette["text_main"], bold=True)
        c_val.fill = fill_card
        c_val.alignment = Alignment(horizontal="center", vertical="center")
        c_val.border = Border(bottom=thin_border.bottom, left=thin_border.left, right=thin_border.right)

        start_col += 2

    # 7. Chart Layout Zone
    chart_area = ws.cell(row=8, column=4)
    chart_area.value = "Chart Render Zone"
    chart_area.font = Font(name="Calibri", size=16, color="AAAAAA", italic=True)
    chart_area.alignment = Alignment(horizontal="left", vertical="center")
```