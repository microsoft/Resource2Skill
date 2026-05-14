### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Creates a strong visual hierarchy by applying a dark background fill to a header region (rows 1-8) and a lighter contrasting fill to the body region. It then provisions a horizontal strip of KPI "widgets" built entirely out of merged, formatted cells (an accent color block adjacent to a white text block), which provides a stable, modern alternative to floating Excel shape objects.
* **Applicability**: Best for high-level summary dashboards or reports where aesthetics matter. Using cell-based widgets instead of shapes ensures the layout remains perfectly responsive and robust when rows/columns are resized or exported.

### 2. Structural Breakdown

- **Data Layout**: Global background overrides applied to rows 1-8 (header) and 9-40 (body). KPI cards are placed starting at row 5, each spanning 4 columns and 3 rows.
- **Formula Logic**: Static layout generation (designed to be updated via `GETPIVOTDATA` or direct cell references in a broader pipeline).
- **Visual Design**: Uses a custom theme palette. The title uses a large, light font; the subtitle uses the theme's accent color. KPI cards feature a thin left-border colored block, followed by a white background block for the numbers.
- **Charts/Tables**: Emulates "Card" visuals using cell merges and `Alignment(horizontal="center", vertical="center")`. 
- **Theme Hooks**: Consumes `primary`, `secondary` (or light background), `accent`, `text_light`, and `text_dark`. 

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, subtitle: str, kpis: list[dict], theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a stylized dashboard canvas with a dark header, light body, and cell-based KPI cards.
    
    Example `kpis` input:
    [
        {"label": "TOTAL CALLS", "value": 16749, "format": "#,##0"},
        {"label": "DEALS CLOSED", "value": 1203, "format": "#,##0"},
        {"label": "DEAL VALUE", "value": 646979, "format": "$#,##0"}
    ]
    """
    ws = wb.create_sheet(sheet_name)
    
    # Standard theme palette fallback
    palettes = {
        "corporate_blue": {"primary": "2F365F", "secondary": "E6E8F3", "accent": "FFC000", "text_light": "FFFFFF", "text_dark": "1F1F1F", "card_bg": "FFFFFF"},
        "purple_gold": {"primary": "5A3B7A", "secondary": "EAE1F5", "accent": "F2C811", "text_light": "FFFFFF", "text_dark": "333333", "card_bg": "FFFFFF"}
    }
    tc = palettes.get(theme, palettes["purple_gold"])
    
    primary_fill = PatternFill(start_color=tc["primary"], end_color=tc["primary"], fill_type="solid")
    secondary_fill = PatternFill(start_color=tc["secondary"], end_color=tc["secondary"], fill_type="solid")
    card_fill = PatternFill(start_color=tc["card_bg"], end_color=tc["card_bg"], fill_type="solid")
    accent_fill = PatternFill(start_color=tc["accent"], end_color=tc["accent"], fill_type="solid")
    
    # 1. Apply Background Canvas
    for row in range(1, 9):
        ws.row_dimensions[row].height = 20
        for col in range(1, 30):
            ws.cell(row=row, column=col).fill = primary_fill
            
    for row in range(9, 45):
        ws.row_dimensions[row].height = 16
        for col in range(1, 30):
            ws.cell(row=row, column=col).fill = secondary_fill
            
    # Adjust specific header row heights for typography
    ws.row_dimensions[2].height = 42
    ws.row_dimensions[3].height = 25
    
    # 2. Title & Subtitle
    title_cell = ws.cell(row=2, column=2, value=title)
    title_cell.font = Font(size=28, color=tc["text_light"], bold=True)
    
    subtitle_cell = ws.cell(row=3, column=2, value=subtitle)
    subtitle_cell.font = Font(size=14, color=tc["accent"], italic=True)
    
    # 3. KPI Strip (Starts Row 5, Col 4)
    start_row = 5
    start_col = 4
    
    for kpi in kpis:
        # Accent Edge (Leftmost column of the card)
        for r in range(start_row, start_row + 3):
            ws.cell(row=r, column=start_col).fill = accent_fill
            
        # Card Body (Next 3 columns)
        for r in range(start_row, start_row + 3):
            for c in range(start_col + 1, start_col + 4):
                ws.cell(row=r, column=c).fill = card_fill
                
        # Value Cell (Top 2 rows merged)
        ws.merge_cells(start_row=start_row, start_column=start_col+1, end_row=start_row+1, end_column=start_col+3)
        val_cell = ws.cell(row=start_row, column=start_col+1, value=kpi.get("value", ""))
        val_cell.font = Font(size=18, color=tc["primary"], bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        if "format" in kpi:
            val_cell.number_format = kpi["format"]
            
        # Label Cell (Bottom row merged)
        ws.merge_cells(start_row=start_row+2, start_column=start_col+1, end_row=start_row+2, end_column=start_col+3)
        lbl_cell = ws.cell(row=start_row+2, column=start_col+1, value=kpi.get("label", ""))
        lbl_cell.font = Font(size=10, color=tc["text_dark"], bold=True)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")
        
        # Adjust column widths for proportion
        ws.column_dimensions[get_column_letter(start_col)].width = 2      # Accent bar width
        for c in range(start_col + 1, start_col + 4):
            ws.column_dimensions[get_column_letter(c)].width = 5.5    # Card body width
            
        # Move to next KPI slot (4 cols for card + 1 for gap)
        start_col += 5
        
    # Hide gridlines for cleaner dashboard look
    ws.sheet_view.showGridLines = False
```