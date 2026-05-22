### 1. High-level Skill Pattern Extraction

> **Skill Name**: Cell-Based Dual KPI Card

* **Tier**: component
* **Core Mechanism**: Creates a visually distinct 3x2 cell block that acts as a styled KPI card, circumventing `openpyxl`'s limited support for data-linked drawing shapes. It merges cells for a clean layout, applies contrasting background fills (a primary card color and a darker accent block for the secondary metric), and directly displays or links formula values.
* **Applicability**: Best used on dashboard or summary sheets where high-level metrics (e.g., Regional Revenue and Market Share) need to stand out as distinct "cards" above or beside tabular data.

### 2. Structural Breakdown

- **Data Layout**: A 3x2 cell grid. Row 1 is merged horizontally for the title. Row 2-3 in Column 1 hold the metric label and primary value. Row 2-3 in Column 2 are merged vertically for the secondary metric (percentage).
- **Formula Logic**: Readily accepts cell references (e.g., `="=B2"`) or static values to populate the main and secondary metrics. 
- **Visual Design**: Uses a rich, solid background fill with a slightly darker accent for the percentage metric. Fonts are bold, white, and scaled up (size 14/16) to draw the eye, mimicking a floating shape UI.
- **Charts/Tables**: N/A (replaces the need for SmartArt/Shapes).
- **Theme Hooks**: Consumes `bg` (primary card color) and `accent` (secondary metric block color) palette tokens, falling back to corporate navy blues if a standard theme is unavailable.

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, title: str, metric_label: str, main_val: any, sub_val: any, main_format: str = '"$"#,##0', sub_format: str = '0%', theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import coordinate_to_tuple, get_column_letter

    row, col = coordinate_to_tuple(anchor)
    
    # Theme palette fallback
    palettes = {
        "corporate_blue": {"bg": "1F4E78", "accent": "112B43", "text": "FFFFFF"},
        "executive_dark": {"bg": "262626", "accent": "404040", "text": "FFFFFF"},
        "emerald": {"bg": "0F7B53", "accent": "0A593A", "text": "FFFFFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    
    fill_main = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    fill_accent = PatternFill(start_color=palette["accent"], end_color=palette["accent"], fill_type="solid")
    
    font_title = Font(color=palette["text"], size=14, bold=True)
    font_label = Font(color=palette["text"], size=10)
    font_main = Font(color=palette["text"], size=14, bold=True)
    font_sub = Font(color=palette["text"], size=16, bold=True)
    
    align_center = Alignment(horizontal="center", vertical="center")

    # 1. Title Row (Merged horizontally)
    ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+1)
    cell_title = ws.cell(row=row, column=col)
    cell_title.value = title
    cell_title.font = font_title
    cell_title.alignment = align_center

    # 2. Left Side: Label and Main Value
    cell_label = ws.cell(row=row+1, column=col)
    cell_label.value = metric_label
    cell_label.font = font_label
    cell_label.alignment = align_center

    cell_main = ws.cell(row=row+2, column=col)
    cell_main.value = main_val
    cell_main.font = font_main
    cell_main.alignment = align_center
    cell_main.number_format = main_format

    # 3. Right Side: Sub Value (Merged vertically)
    ws.merge_cells(start_row=row+1, start_column=col+1, end_row=row+2, end_column=col+1)
    cell_sub = ws.cell(row=row+1, column=col+1)
    cell_sub.value = sub_val
    cell_sub.font = font_sub
    cell_sub.alignment = align_center
    cell_sub.number_format = sub_format

    # Apply fills consistently across the block to cover gridlines
    for r in range(row, row+3):
        for c in range(col, col+2):
            cell = ws.cell(row=r, column=c)
            # Top row or left column gets the main background
            if r == row or c == col:
                cell.fill = fill_main
            else:
                # Bottom-right merged block gets the accent background
                cell.fill = fill_accent
                
    # Adjust sizing to give it a "card" proportion
    ws.column_dimensions[get_column_letter(col)].width = 18
    ws.column_dimensions[get_column_letter(col+1)].width = 12
    ws.row_dimensions[row].height = 25
    ws.row_dimensions[row+1].height = 15
    ws.row_dimensions[row+2].height = 25
```