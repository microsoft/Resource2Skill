### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Formats a worksheet to look like a modern web application by hiding gridlines, coloring a narrow left pane (Columns A-C) with a dark theme to act as a sidebar, and filling the main area (Columns D-T) with a light gray canvas. It injects large, bold KPI metrics into the sidebar and draws distinct white rectangular "cards" in the main canvas to act as structured containers for future charts.
* **Applicability**: Ideal for executive summaries, high-level business reviews, and KPI tracking where visual hierarchy, clean spatial organization, and an app-like navigation feel are more important than displaying raw data grids.

### 2. Structural Breakdown

- **Data Layout**: Employs columns A-C for sidebar navigation/KPIs (locked visual zone), and columns D-T for the main content.
- **Formula Logic**: Purely structural layout (assumes KPIs are passed in via Python, mimicking `GETPIVOTDATA` linking in Excel).
- **Visual Design**: Uses a dual-tone background approach (e.g., navy blue sidebar vs. off-white canvas) to simulate a web app interface. Gridlines are explicitly turned off.
- **Charts/Tables**: Pre-builds clean "card" areas using solid white `PatternFill` where line charts, bar charts, or maps can be inserted later.
- **Theme Hooks**: Uses a custom or fallback palette to define `sidebar` (dark), `text` (light/white), `canvas` (light gray), and `card` (white) backgrounds.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", kpis: list = None, **kwargs) -> None:
    """
    Creates a structural dashboard shell featuring a dark left sidebar for KPIs 
    and a light main canvas with pre-drawn 'card' zones for charts.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Standard theme fallback logic
    themes = {
        "corporate_blue": {"sidebar": "1E3A8A", "text": "FFFFFF", "canvas": "F3F4F6", "card": "FFFFFF"},
        "forest_green": {"sidebar": "064E3B", "text": "FFFFFF", "canvas": "ECFDF5", "card": "FFFFFF"},
        "dark_mode": {"sidebar": "111827", "text": "F9FAFB", "canvas": "1F2937", "card": "374151"},
        "viva_calif": {"sidebar": "2F4F4F", "text": "FFFFFF", "canvas": "E8F5E9", "card": "FFFFFF"} # Mimicking video
    }
    palette = themes.get(theme, themes["viva_calif"])

    fill_sidebar = PatternFill(start_color=palette["sidebar"], fill_type="solid")
    fill_canvas = PatternFill(start_color=palette["canvas"], fill_type="solid")
    fill_card = PatternFill(start_color=palette["card"], fill_type="solid")

    font_title = Font(color=palette["text"], size=22, bold=True)
    font_kpi_val = Font(color=palette["text"], size=24, bold=True)
    font_kpi_lbl = Font(color=palette["text"], size=11)
    font_card_hdr = Font(color=palette["sidebar"], size=14, bold=True)

    # 1. Structure the grid (Column widths)
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 22
    ws.column_dimensions['C'].width = 3
    for col in range(4, 21):
        ws.column_dimensions[get_column_letter(col)].width = 11

    # 2. Apply background zones (Sidebar vs Canvas)
    for row in range(1, 40):
        ws.row_dimensions[row].height = 18
        for col in range(1, 4):
            ws.cell(row=row, column=col).fill = fill_sidebar
        for col in range(4, 21):
            ws.cell(row=row, column=col).fill = fill_canvas

    # 3. Add Dashboard Title in Sidebar
    title_cell = ws['B2']
    title_cell.value = title.upper()
    title_cell.font = font_title
    title_cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[2].height = 30

    # 4. Render KPIs
    if kpis is None:
        # Realistic e-commerce metrics from the tutorial
        kpis = [
            {"label": "Total Orders", "value": 2400, "num_fmt": "#,##0"},
            {"label": "Total Revenue", "value": 649019, "num_fmt": "$#,##0"},
            {"label": "Avg. Rating", "value": 4.0, "num_fmt": "0.0"},
            {"label": "Days to Deliver", "value": 2.3, "num_fmt": "0.0"}
        ]

    start_row = 5
    for kpi in kpis:
        val_cell = ws.cell(row=start_row, column=2)
        val_cell.value = kpi["value"]
        val_cell.font = font_kpi_val
        val_cell.alignment = Alignment(horizontal="left", vertical="bottom")
        if "num_fmt" in kpi:
            val_cell.number_format = kpi["num_fmt"]

        lbl_cell = ws.cell(row=start_row + 1, column=2)
        lbl_cell.value = kpi["label"].upper()
        lbl_cell.font = font_kpi_lbl
        lbl_cell.alignment = Alignment(horizontal="left", vertical="top")
        
        start_row += 4

    # 5. Draw Chart "Cards" in the main canvas
    cards = [
        {"name": "Last 13 Week Trends - Qty & Amount", "r_start": 3, "r_end": 16, "c_start": 5, "c_end": 12},
        {"name": "How they like to buy?", "r_start": 3, "r_end": 16, "c_start": 13, "c_end": 19},
        {"name": "Which Products are Popular?", "r_start": 18, "r_end": 35, "c_start": 5, "c_end": 12},
        {"name": "Where do our customers live?", "r_start": 18, "r_end": 35, "c_start": 13, "c_end": 19}
    ]

    for card in cards:
        # Draw the card body
        for r in range(card["r_start"], card["r_end"] + 1):
            for c in range(card["c_start"], card["c_end"] + 1):
                ws.cell(row=r, column=c).fill = fill_card
        
        # Add the card header
        hdr_cell = ws.cell(row=card["r_start"], column=card["c_start"])
        hdr_cell.value = card["name"]
        hdr_cell.font = font_card_hdr
        # Create a tiny top-padding effect for the text
        hdr_cell.alignment = Alignment(vertical="center", indent=1)
```