### 1. High-level Skill Pattern Extraction

> **Skill Name**: Cell-Grid KPI Card Component

* **Tier**: component
* **Core Mechanism**: Adapts the concept of floating, shape-based KPI cards into a robust, cell-grid equivalent that is highly reliable for programmatic generation. Constructs a 3x2 merged cell block, applies thematic primary and accent background fills to distinct sections to simulate overlapping shapes, and injects formulas to dynamically link card values to source data cells.
* **Applicability**: Best used in automated dashboards where generating precise floating shapes with text links is fragile. Ideal for highlighting a primary metric alongside a secondary percentage metric (e.g., Revenue and Market Share) above or beside main data tables.

### 2. Structural Breakdown

- **Data Layout**: 3 rows by 2 columns. The top row is merged horizontally for the title. The bottom-right two cells are merged vertically to house the secondary accent metric.
- **Formula Logic**: Injects dynamic cell references (e.g., `={val_ref}`) into the value cells so the KPI card automatically updates when the source table changes, mirroring the formula-bar linking shown in the video.
- **Visual Design**: Uses a solid primary theme color for the main body and an accent color for the secondary metric block. Fonts are scaled up, bolded, and set to a high-contrast text color (white).
- **Charts/Tables**: None
- **Theme Hooks**: Consumes `primary` (main background), `accent` (secondary block background), `text` (font color), and `border` (card outline).

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, title: str, val_ref: str, sub_val_ref: str, val_label: str = "Revenue", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
    from openpyxl.utils import get_column_letter
    
    # Theme palette fallback
    palettes = {
        "corporate_blue": {"primary": "002060", "accent": "0070C0", "text": "FFFFFF", "border": "001030"},
        "emerald_green": {"primary": "004D40", "accent": "00897B", "text": "FFFFFF", "border": "00332A"},
        "slate_dark": {"primary": "333333", "accent": "555555", "text": "FFFFFF", "border": "111111"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    
    xy = coordinate_from_string(anchor)
    col = column_index_from_string(xy[0])
    row = xy[1]
    
    # 1. Title Row (Merged horizontally)
    title_cell = ws.cell(row=row, column=col)
    title_cell.value = title
    ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+1)
    
    # 2. Main Value Label
    label_cell = ws.cell(row=row+1, column=col)
    label_cell.value = val_label
    
    # 3. Main Value (Linked to source cell)
    val_cell = ws.cell(row=row+2, column=col)
    val_cell.value = f"={val_ref}"
    val_cell.number_format = '"$"#,##0'
    
    # 4. Secondary Metric (Linked to source cell & Merged vertically)
    sub_val_cell = ws.cell(row=row+1, column=col+1)
    sub_val_cell.value = f"={sub_val_ref}"
    sub_val_cell.number_format = '0%'
    ws.merge_cells(start_row=row+1, start_column=col+1, end_row=row+2, end_column=col+1)
    
    # --- Styling ---
    primary_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    accent_fill = PatternFill(start_color=palette["accent"], end_color=palette["accent"], fill_type="solid")
    
    white_font = Font(color=palette["text"])
    title_font = Font(color=palette["text"], bold=True, size=14)
    val_font = Font(color=palette["text"], bold=True, size=12)
    sub_font = Font(color=palette["text"], bold=True, size=16)
    
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center", indent=1)
    
    # Apply background fills and outer border
    thin_border = Side(border_style="thin", color=palette["border"])
    outer_border = Border(top=thin_border, left=thin_border, right=thin_border, bottom=thin_border)
    
    for r in range(row, row+3):
        for c in range(col, col+2):
            cell = ws.cell(row=r, column=c)
            # Use accent color for the secondary metric block to simulate the distinct oval shape
            if c == col+1 and r > row:
                cell.fill = accent_fill
            else:
                cell.fill = primary_fill
            cell.border = outer_border
                
    # Apply specific alignments and fonts
    title_cell.font = title_font
    title_cell.alignment = center_align
    
    label_cell.font = white_font
    label_cell.alignment = left_align
    
    val_cell.font = val_font
    val_cell.alignment = left_align
    
    sub_val_cell.font = sub_font
    sub_val_cell.alignment = center_align
    
    # Layout dimensions
    ws.column_dimensions[get_column_letter(col)].width = 16
    ws.column_dimensions[get_column_letter(col+1)].width = 12
    ws.row_dimensions[row].height = 25
    ws.row_dimensions[row+1].height = 18
    ws.row_dimensions[row+2].height = 18
```