### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid-Based KPI Dashboard Card

* **Tier**: component
* **Core Mechanism**: Standard `openpyxl` does not natively support binding dynamic cell formulas to floating vector shapes or grouping them as seen in the Excel UI. To achieve the exact same visual dashboard effect programmatically, this skill constructs a "KPI Card" directly on the grid using a 2x2 merged cell block. It uses dark background fills, contrasting accent backgrounds for secondary metrics (emulating the floating circle badge), and thick borders to create the illusion of an isolated shape. 
* **Applicability**: Best used on dashboard summary sheets where executive metrics (like Revenue and Market Share) need to stand out as distinct "cards" above or beside the main data tables.

### 2. Structural Breakdown

- **Data Layout**: 2x2 cell grid. Left column holds the dimension/title (row 1) and the primary metric (row 2). Right column is merged vertically to hold the secondary metric (like a percentage).
- **Formula Logic**: Static values or formulas can be passed into the renderer.
- **Visual Design**: Navy/Dark background for the primary block, slightly lighter accent color for the right-hand badge block, bold white text for contrast, and external thick borders to separate the card from gridlines.
- **Charts/Tables**: None (UI Component).
- **Theme Hooks**: `bg` (primary card background), `accent` (secondary metric badge background), `fg` (text color).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import coordinate_from_string, column_index_from_string, get_column_letter

def render(ws, anchor: str, *, title: str, primary_value, secondary_value=None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a solid KPI card on the grid mimicking a grouped shape widget.
    
    :param ws: The openpyxl worksheet.
    :param anchor: Top-left coordinate (e.g. "E2").
    :param title: The title of the KPI (e.g. "Asia").
    :param primary_value: The main numerical value (e.g. 369989).
    :param secondary_value: Optional sub-metric, like a percentage (e.g. 0.05).
    :param theme: Theme dictating the card background and text colors.
    """
    # Standard theme fallback pattern
    theme_colors = {
        "corporate_blue": {"bg": "1F4E78", "fg": "FFFFFF", "accent": "2F75B5", "border": "FFFFFF"},
        "midnight": {"bg": "262626", "fg": "FFFFFF", "accent": "404040", "border": "000000"}
    }
    colors = theme_colors.get(theme, theme_colors["corporate_blue"])

    # Resolve coordinates
    col_str, row = coordinate_from_string(anchor)
    col = column_index_from_string(col_str)

    # Adjust dimensions for the card proportions
    ws.row_dimensions[row].height = 20
    ws.row_dimensions[row+1].height = 30
    ws.column_dimensions[col_str].width = 18
    ws.column_dimensions[get_column_letter(col+1)].width = 12

    # Styles
    bg_fill = PatternFill(start_color=colors["bg"], end_color=colors["bg"], fill_type="solid")
    accent_fill = PatternFill(start_color=colors["accent"], end_color=colors["accent"], fill_type="solid")
    
    title_font = Font(color=colors["fg"], size=11, bold=False)
    primary_font = Font(color=colors["fg"], size=16, bold=True)
    secondary_font = Font(color=colors["fg"], size=14, bold=True)
    
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center", indent=1)

    # Apply base background fill to the 2x2 grid
    for r in range(row, row + 2):
        for c in range(col, col + 2):
            cell = ws.cell(row=r, column=c)
            cell.fill = bg_fill

    # Render Title (Top-Left)
    title_cell = ws.cell(row=row, column=col)
    title_cell.value = title
    title_cell.font = title_font
    title_cell.alignment = left_align

    # Render Primary Value (Bottom-Left)
    val_cell = ws.cell(row=row+1, column=col)
    val_cell.value = primary_value
    val_cell.font = primary_font
    val_cell.alignment = left_align
    # Determine format dynamically or allow kwarg override
    val_cell.number_format = kwargs.get("primary_format", "$#,##0") 

    # Render Secondary Value as a "Badge" (Right Column, Merged)
    if secondary_value is not None:
        ws.merge_cells(start_row=row, start_column=col+1, end_row=row+1, end_column=col+1)
        sec_cell = ws.cell(row=row, column=col+1)
        sec_cell.value = secondary_value
        sec_cell.fill = accent_fill  # Contrasting background to simulate the circle
        sec_cell.font = secondary_font
        sec_cell.alignment = center_align
        sec_cell.number_format = kwargs.get("secondary_format", "0%")

    # Apply outer thick border to simulate an isolated shape
    thick_border = Side(border_style="thick", color=colors["border"])
    for r in range(row, row + 2):
        for c in range(col, col + 2):
            cell = ws.cell(row=r, column=c)
            top_side = thick_border if r == row else None
            bottom_side = thick_border if r == row + 1 else None
            left_side = thick_border if c == col else None
            right_side = thick_border if c == col + 1 else None
            cell.border = Border(top=top_side, bottom=bottom_side, left=left_side, right=right_side)
```