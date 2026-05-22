### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Block Component

* **Tier**: component
* **Core Mechanism**: Constructs a multi-cell, highly-styled block that acts as a visual KPI "card". It uses merged cells to stack a region title and label, then splits the bottom row to display a primary absolute metric alongside a secondary percentage metric. Theme-driven background fills and font colors simulate the appearance of a floating shape.
* **Applicability**: Perfect for executive dashboards or top-level summary sheets where key numbers (e.g., Regional Revenue + Market Share) need to pop out visually from standard data tables.

### 2. Structural Breakdown

- **Data Layout**: A 3x2 grid of cells anchored at the specified location. Rows 1 and 2 are merged across both columns. Row 3 splits the primary value (col 1) and secondary percentage (col 2).
- **Formula Logic**: Static programmatic injection, though the values can easily be replaced with `=` formulas pointing to a data sheet.
- **Visual Design**: Solid colored background mimicking a shape. White, bold fonts with varying sizes for visual hierarchy (Title > Main Value > Subtitle).
- **Charts/Tables**: None.
- **Theme Hooks**: Utilizes `primary` for the main card background and `secondary` (or an accent) for the percentage metric background to create contrast similar to the video's secondary oval shape.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import coordinate_to_tuple, get_column_letter

def render(ws, anchor: str, *, region: str = "Asia", label: str = "Revenue", value: float = 369989.0, format_str: str = "$#,##0", percent_val: float = 0.05, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a distinct, colorful KPI block (simulating a shape-based card)
    using cell merges and theme colors.
    """
    # Self-contained theme palette fallback
    themes = {
        "corporate_blue": {"primary": "002060", "text": "FFFFFF", "secondary": "4F81BD"},
        "executive_dark": {"primary": "262626", "text": "FFFFFF", "secondary": "595959"},
        "emerald_green": {"primary": "0F5132", "text": "FFFFFF", "secondary": "198754"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    row, col = coordinate_to_tuple(anchor)

    # 1. Structure & Values
    ws.cell(row=row, column=col, value=region)
    ws.cell(row=row+1, column=col, value=label)
    
    v_cell = ws.cell(row=row+2, column=col, value=value)
    v_cell.number_format = format_str

    p_cell = None
    if percent_val is not None:
        # Merge top rows across 2 columns
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+1)
        ws.merge_cells(start_row=row+1, start_column=col, end_row=row+1, end_column=col+1)
        
        p_cell = ws.cell(row=row+2, column=col+1, value=percent_val)
        p_cell.number_format = "0%"
    else:
        # Merge all rows if no secondary metric
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+1)
        ws.merge_cells(start_row=row+1, start_column=col, end_row=row+1, end_column=col+1)
        ws.merge_cells(start_row=row+2, start_column=col, end_row=row+2, end_column=col+1)

    # 2. Formatting Definitions
    main_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    sec_fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
    
    center_align = Alignment(horizontal="center", vertical="center")
    
    title_font = Font(color=palette["text"], bold=True, size=16)
    label_font = Font(color=palette["text"], italic=True, size=11)
    val_font = Font(color=palette["text"], bold=True, size=14)
    pct_font = Font(color=palette["text"], bold=True, size=12)
    
    thin_border = Border(
        left=Side(style='thin', color="FFFFFF"),
        right=Side(style='thin', color="FFFFFF"),
        top=Side(style='thin', color="FFFFFF"),
        bottom=Side(style='thin', color="FFFFFF")
    )

    # 3. Apply Formats to Block
    for r in range(row, row+3):
        for c in range(col, col+2):
            cell = ws.cell(row=r, column=c)
            cell.fill = main_fill
            cell.alignment = center_align
            cell.border = thin_border

    # Target specific fonts
    ws.cell(row=row, column=col).font = title_font
    ws.cell(row=row+1, column=col).font = label_font
    v_cell.font = val_font
    
    if p_cell:
        p_cell.font = pct_font
        p_cell.fill = sec_fill # Differentiate the secondary metric like the overlay shape

    # 4. Dimension Sizing
    ws.column_dimensions[get_column_letter(col)].width = 16
    ws.column_dimensions[get_column_letter(col+1)].width = 10
    
    # Pad rows for breathing room
    ws.row_dimensions[row].height = 25
    ws.row_dimensions[row+1].height = 18
    ws.row_dimensions[row+2].height = 25
```