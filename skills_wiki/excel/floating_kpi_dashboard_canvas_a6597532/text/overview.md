### 1. High-level Skill Pattern Extraction

> **Skill Name**: Floating KPI Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Renders a split-tone background canvas (dark header, light body) with gridlines disabled. Generates a row of cell-based "floating" KPI cards that span the color boundary, using merged cells, solid fills, and colored top borders to emulate modern UI shapes without relying on fragile floating drawing objects.
* **Applicability**: Perfect as the base layer for executive dashboards. Used when you need a web-like, polished UI structure built purely from the standard Excel grid before laying out pivot tables or charts.

### 2. Structural Breakdown

- **Data Layout**: `B2` holds the Title, `B3` holds the Subtitle. KPIs start at row 5, with each card merging 3 columns and separated by 1 spacer column.
- **Formula Logic**: Cell-based emulation of shapes. `kpis` data is injected directly into the top-left cells of merged regions (`horizontal="center"`, `vertical="center"`).
- **Visual Design**: Gridlines are hidden. Rows 1-6 use a dark fill; rows 7-40 use a light pastel fill. The KPI cards occupy rows 5-9, meaning they physically overlap the background color boundary to create a "floating" effect. Cards feature a thick accent-colored top border.
- **Charts/Tables**: Lays out the spacing framework for charts to be added below row 11.
- **Theme Hooks**: Uses `header_bg`, `header_fg`, `canvas_bg`, `accent`, `card_bg`, and `card_fg` to create contrast.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str, kpis: list[dict], theme: str = "purple_dashboard", **kwargs) -> None:
    """
    Renders a clean, modern dashboard layout with a split-tone background and cell-based KPI cards.
    
    Example `kpis` structure:
    [
        {"label": "TOTAL CALLS", "value": "16,749"},
        {"label": "CALLS REACHED", "value": "3,328"},
        {"label": "DEALS CLOSED", "value": "1,203"},
        {"label": "TOTAL VALUE", "value": "$646,979"}
    ]
    """
    palettes = {
        "purple_dashboard": {
            "header_bg": "58335E", 
            "header_fg": "FFFFFF",
            "canvas_bg": "F2EFF5", 
            "accent": "FFC000",      # Gold
            "card_bg": "FFFFFF",
            "card_fg": "58335E"
        },
        "corporate_blue": {
            "header_bg": "2B579A",
            "header_fg": "FFFFFF",
            "canvas_bg": "F3F2F1",
            "accent": "D24726",      # Burnt Orange
            "card_bg": "FFFFFF",
            "card_fg": "2B579A"
        }
    }
    palette = palettes.get(theme, palettes["purple_dashboard"])

    ws = wb.create_sheet(sheet_name) if sheet_name not in wb.sheetnames else wb[sheet_name]
    ws.sheet_view.showGridLines = False
    
    header_fill = PatternFill(start_color=palette["header_bg"], fill_type="solid")
    canvas_fill = PatternFill(start_color=palette["canvas_bg"], fill_type="solid")
    
    # Paint Canvas background
    for r in range(1, 41):
        for c in range(1, 22):
            cell = ws.cell(row=r, column=c)
            cell.fill = header_fill if r <= 6 else canvas_fill
                
    # Set Title
    ws["B2"].value = title
    ws["B2"].font = Font(name="Arial", size=32, color=palette["header_fg"], bold=True)
    ws.row_dimensions[2].height = 45
    
    # Set Subtitle
    ws["B3"].value = subtitle
    ws["B3"].font = Font(name="Arial", size=14, color=palette["accent"])
    ws.row_dimensions[3].height = 25
    
    # Render KPI Strip (Cell-based emulation of floating shapes)
    card_fill = PatternFill(start_color=palette["card_bg"], fill_type="solid")
    start_col = 2  # Start at Column B
    
    for kpi in kpis:
        # Merge range for the card value (rows 5-7) and label (rows 8-9)
        ws.merge_cells(start_row=5, start_column=start_col, end_row=7, end_column=start_col+2)
        ws.merge_cells(start_row=8, start_column=start_col, end_row=9, end_column=start_col+2)
        
        # Apply fill and top accent border
        for r in range(5, 10):
            for c in range(start_col, start_col+3):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                if r == 5:
                    cell.border = Border(top=Side(style="medium", color=palette["accent"]))
                    
        # Set Value
        val_cell = ws.cell(row=5, column=start_col)
        val_cell.value = kpi.get("value", "")
        val_cell.font = Font(name="Arial", size=22, color=palette["card_fg"], bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Set Label
        lbl_cell = ws.cell(row=8, column=start_col)
        lbl_cell.value = kpi.get("label", "")
        lbl_cell.font = Font(name="Arial", size=11, color=palette["card_fg"])
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")
        
        start_col += 4  # Move to next card (3 cols for card + 1 spacer)
        
    # Layout adjustments
    ws.column_dimensions['A'].width = 3.0
    for c in range(2, start_col):
        # Spacers are columns where (c - 2) % 4 == 3
        is_spacer = (c - 2) % 4 == 3
        ws.column_dimensions[get_column_letter(c)].width = 3.0 if is_spacer else 7.0
```