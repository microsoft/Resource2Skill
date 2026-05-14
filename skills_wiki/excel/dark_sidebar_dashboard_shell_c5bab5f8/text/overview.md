### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dark Sidebar Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Creates a professional, dual-pane dashboard layout by contrasting a dark, themed left sidebar (designed for global KPIs and slicers) against a light main content area. It disables gridlines and applies white-filled ranges with simulated drop-shadow borders to create distinct "widget cards" for placing charts and tables.
* **Applicability**: Highly applicable for executive summaries and interactive dashboards. The sidebar neatly anchors high-level metrics and filter controls, freeing up the main canvas for varied visual widgets without looking cluttered.

### 2. Structural Breakdown

- **Data Layout**: 
  - **Sidebar**: Columns A-C (A and C as margins, B as the main content column).
  - **Main Canvas**: Columns D onwards, utilized as a soft background.
- **Formula Logic**: Static layout generation (can be populated by values queried from other pivot sheets, as seen in the tutorial's `=Pivot!A1` logic).
- **Visual Design**: 
  - Gridlines hidden.
  - Sidebar: Solid dark theme color fill, with contrasting light, bold typography.
  - Canvas: Very light gray/tinted fill.
  - Cards: White fill with a standard top/left border and a thicker bottom/right border to simulate the tutorial's drop-shadow effect.
- **Charts/Tables**: Acts as a container/shell for subsequent chart insertions. 
- **Theme Hooks**: `primary` (sidebar), `bg` (canvas), `card_bg` (widget background), `text_light` (sidebar text), `border` and `border_shadow` (widget edges).

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import range_boundaries

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", kpis: list = None, card_ranges: list = None, **kwargs) -> None:
    """
    Renders a structural dashboard shell with a dark left sidebar for KPIs and 
    a light main canvas containing widget 'cards' with simulated drop-shadows.
    """
    if sheet_name not in wb.sheetnames:
        ws = wb.create_sheet(sheet_name)
    else:
        ws = wb[sheet_name]

    # Standardized palette fallback
    themes = {
        "corporate_blue": {
            "primary": "2B579A", "bg": "F3F4F6", "card_bg": "FFFFFF", 
            "text_light": "FFFFFF", "border": "D1D5DB", "border_shadow": "9CA3AF"
        },
        "forest_green": {
            "primary": "2E4E3F", "bg": "E9EFEC", "card_bg": "FFFFFF", 
            "text_light": "FFFFFF", "border": "CCD5D0", "border_shadow": "A0AAB2"
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 1. Turn off gridlines for a clean dashboard look
    ws.sheet_view.showGridLines = False

    # Define Fills
    sidebar_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    bg_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    card_fill = PatternFill(start_color=palette["card_bg"], end_color=palette["card_bg"], fill_type="solid")

    # Define Fonts
    title_font = Font(name="Calibri", size=22, bold=True, color=palette["text_light"])
    kpi_label_font = Font(name="Calibri", size=11, color=palette["text_light"])
    kpi_value_font = Font(name="Calibri", size=18, bold=True, color=palette["text_light"])

    # Define Borders (Standard thin + Medium for faux shadow)
    thin_side = Side(border_style="thin", color=palette["border"])
    shadow_side = Side(border_style="medium", color=palette["border_shadow"])

    # 2. Paint the main background area (approx. 50 rows, 30 columns)
    for row in ws.iter_rows(min_row=1, max_row=50, min_col=4, max_col=30):
        for cell in row:
            cell.fill = bg_fill

    # 3. Paint the Sidebar (Columns A to C)
    for row in ws.iter_rows(min_row=1, max_row=50, min_col=1, max_col=3):
        for cell in row:
            cell.fill = sidebar_fill

    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 24
    ws.column_dimensions['C'].width = 3

    # 4. Insert Dashboard Title
    title_cell = ws["B2"]
    title_cell.value = title
    title_cell.font = title_font
    title_cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[2].height = 35

    # 5. Render KPIs in the sidebar
    if not kpis:
        kpis = [
            {"label": "Total Orders", "value": "2,400"},
            {"label": "Total Revenue", "value": "$649.0k"},
            {"label": "Avg. Rating", "value": "4.0 / 5.0"},
            {"label": "Days to Deliver", "value": "2.3"}
        ]

    current_row = 5
    for kpi in kpis:
        lbl_cell = ws.cell(row=current_row, column=2, value=kpi["label"].upper())
        lbl_cell.font = kpi_label_font
        
        val_cell = ws.cell(row=current_row+1, column=2, value=kpi["value"])
        val_cell.font = kpi_value_font
        
        current_row += 3

    # 6. Render Widget Cards on the canvas
    if not card_ranges:
        card_ranges = ["E4:L14", "N4:U14", "E16:L28", "N16:U28"]

    for rng in card_ranges:
        min_col, min_row, max_col, max_row = range_boundaries(rng)
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply borders: medium on bottom/right to simulate the tutorial's shadow effect
                top = thin_side if r == min_row else None
                bottom = shadow_side if r == max_row else None
                left = thin_side if c == min_col else None
                right = shadow_side if c == max_col else None
                
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)
```