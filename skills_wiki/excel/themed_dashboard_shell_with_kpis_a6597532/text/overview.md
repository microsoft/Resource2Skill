### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Shell with KPIs

* **Tier**: sheet_shell
* **Core Mechanism**: Translates a heavily shape-based dashboard layout into a robust, pure-cell structure. Uses horizontal color-blocking for a distinct header region, and uses precision cell-merging, fills, and borders to replicate modern KPI "cards" without the fragility of floating shapes.
* **Applicability**: Perfect starting point for management dashboards, sales trackers, or any report that needs a sleek, "web-app" aesthetic in native Excel.

### 2. Structural Breakdown

- **Data Layout**: Wide canvas layout (30 cols), with an explicit header zone (rows 1-6) and a distinct body zone (rows 7-40).
- **Formula Logic**: Static value assignment for the shell; naturally designed to be hydrated with Python variables or linked to Excel formulas in later steps.
- **Visual Design**: Gridlines disabled. Two-tone background layout. KPI cards use a 2-cell vertical merge for the left "accent block" and stacked cells for the "value" / "label", separated by a thin accent-colored border to simulate a split, floating UI card.
- **Charts/Tables**: N/A (structural layout).
- **Theme Hooks**: Utilizes `header_bg`, `body_bg`, `accent`, `card_bg`, `text_light`, `text_dark`, and `text_muted`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str = "", kpis: list = None, theme: str = "executive_purple", **kwargs) -> None:
    """
    Renders a modern, shape-free dashboard shell with a color-blocked header and cell-based KPI cards.
    """
    themes = {
        "executive_purple": {
            "header_bg": "5E3B76",
            "body_bg": "F2EFF5",
            "accent": "FFC000",
            "card_bg": "FFFFFF",
            "text_light": "FFFFFF",
            "text_dark": "20152B",
            "text_muted": "595959"
        },
        "corporate_blue": {
            "header_bg": "203764",
            "body_bg": "D9E1F2",
            "accent": "FFC000",
            "card_bg": "FFFFFF",
            "text_light": "FFFFFF",
            "text_dark": "000000",
            "text_muted": "595959"
        }
    }
    t = themes.get(theme, themes["executive_purple"])
    
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = t["header_bg"]
    
    header_fill = PatternFill(start_color=t["header_bg"], end_color=t["header_bg"], fill_type="solid")
    body_fill = PatternFill(start_color=t["body_bg"], end_color=t["body_bg"], fill_type="solid")
    card_fill = PatternFill(start_color=t["card_bg"], end_color=t["card_bg"], fill_type="solid")
    accent_fill = PatternFill(start_color=t["accent"], end_color=t["accent"], fill_type="solid")
    
    # 1. Apply two-tone background fills
    for row in range(1, 7):
        for col in range(1, 30):
            ws.cell(row=row, column=col).fill = header_fill
            
    for row in range(7, 40):
        for col in range(1, 30):
            ws.cell(row=row, column=col).fill = body_fill
            
    # 2. Render Title & Subtitle
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 25
    
    ws.merge_cells("B2:E2")
    title_cell = ws.cell(row=2, column=2, value=title)
    title_cell.font = Font(name="Calibri", size=24, color=t["text_light"], bold=True)
    title_cell.alignment = Alignment(vertical="center")
    
    if subtitle:
        ws.merge_cells("B3:E3")
        sub_cell = ws.cell(row=3, column=2, value=subtitle)
        sub_cell.font = Font(name="Calibri", size=12, color=t["accent"])
        sub_cell.alignment = Alignment(vertical="top")
        
    # 3. Render KPI Cards (mimicking floating shapes)
    if kpis is None:
        kpis = [
            {"label": "CALLS", "value": "16,749"},
            {"label": "REACHED", "value": "3,328"},
            {"label": "CLOSED", "value": "1,203"},
            {"label": "VALUE", "value": "$646,979"}
        ]
        
    start_col = 6  # Start cards at Column F
    start_row = 2
    
    divider_side = Side(style="thin", color=t["accent"])
    
    for kpi in kpis:
        value = kpi.get("value", "")
        label = kpi.get("label", "")
        
        # Left Accent Block
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row+1, end_column=start_col)
        for r in range(start_row, start_row+2):
            ws.cell(row=r, column=start_col).fill = accent_fill
        
        # Right Text Block (Value top, Label bottom)
        val_cell = ws.cell(row=start_row, column=start_col+1, value=value)
        val_cell.fill = card_fill
        val_cell.font = Font(size=16, color=t["text_dark"], bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="bottom")
        val_cell.border = Border(left=divider_side)
        
        lbl_cell = ws.cell(row=start_row+1, column=start_col+1, value=label)
        lbl_cell.fill = card_fill
        lbl_cell.font = Font(size=9, color=t["text_muted"], bold=True)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")
        lbl_cell.border = Border(left=divider_side)
        
        # Explicit widths to size the card & spacer
        ws.column_dimensions[get_column_letter(start_col)].width = 3      # Accent block width
        ws.column_dimensions[get_column_letter(start_col+1)].width = 14   # Text block width
        ws.column_dimensions[get_column_letter(start_col+2)].width = 2    # Background gap between cards
        
        start_col += 3
        
    # Structural row height tuning
    ws.row_dimensions[1].height = 10
    ws.row_dimensions[start_row].height = 20
    ws.row_dimensions[start_row+1].height = 20
    ws.row_dimensions[4].height = 15
```