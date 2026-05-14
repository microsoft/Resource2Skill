### 1. High-level Skill Pattern Extraction

> **Skill Name**: Cell-Based KPI Card Component

* **Tier**: component
* **Core Mechanism**: Simulates the floating KPI shape widgets from the video by using a heavily styled, merged 3x2 block of cells. Because `openpyxl` lacks robust support for formula-linked floating shapes, this creates an equivalent dashboard-ready card component with a primary metric (e.g., Revenue) and an optional secondary inline metric (e.g., Market Share).
* **Applicability**: Perfect for executive dashboards and summary reports where top-level metrics need to stand out above or beside tabular data. 

### 2. Structural Breakdown

- **Data Layout**: A 3-row by 2-column cell block. Row 1 (merged) holds the title. Row 2 (merged) holds the primary value linked to a data cell. Row 3, Column 2 holds the secondary percentage indicator. 
- **Formula Logic**: Directly references source data cells using `=B2` or similar dynamic references to ensure the dashboard card updates automatically.
- **Visual Design**: Uses a solid background fill (e.g., Navy Blue) across the entire 3x2 grid. Text is white (`FFFFFF`), bold, and scaled up (14pt-16pt) to draw attention. Centered alignment is used for the main title and value.
- **Charts/Tables**: N/A (Formatting-based widget).
- **Theme Hooks**: Utilizes `primary_bg` for the card background and `primary_fg` for the text to maintain contrast.

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, title: str, value_ref: str, pct_ref: str = None, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
    
    # Fallback theme palette
    palettes = {
        "corporate_blue": {"primary_bg": "002060", "primary_fg": "FFFFFF"}, # Navy/White
        "dark_mode": {"primary_bg": "333333", "primary_fg": "E2E2E2"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    bg_color = palette["primary_bg"]
    fg_color = palette["primary_fg"]

    col_str, row = coordinate_from_string(anchor)
    col_idx = column_index_from_string(col_str)

    card_width = 2
    card_height = 3

    # 1. Apply background to the entire block to simulate a cohesive "shape"
    fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    thick_border = Side(border_style="medium", color="FFFFFF")
    # Outer white border to separate the card from the grid
    border = Border(top=thick_border, left=thick_border, right=thick_border, bottom=thick_border)

    for r in range(row, row + card_height):
        for c in range(col_idx, col_idx + card_width):
            cell = ws.cell(row=r, column=c)
            cell.fill = fill
            cell.border = border

    # 2. Row 1: Title (Merged)
    ws.merge_cells(start_row=row, start_column=col_idx, end_row=row, end_column=col_idx + card_width - 1)
    title_cell = ws.cell(row=row, column=col_idx)
    title_cell.value = title
    title_cell.font = Font(color=fg_color, size=11, bold=False)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Row 2: Main Value (Merged)
    ws.merge_cells(start_row=row+1, start_column=col_idx, end_row=row+1, end_column=col_idx + card_width - 1)
    val_cell = ws.cell(row=row+1, column=col_idx)
    # Link to the data cell via formula (e.g. '=B2')
    val_cell.value = f"={value_ref}"
    val_cell.font = Font(color=fg_color, size=16, bold=True)
    val_cell.alignment = Alignment(horizontal="center", vertical="center")
    val_cell.number_format = '"$"#,##0'

    # 4. Row 3: Secondary Metric (Bottom Right corner)
    if pct_ref:
        pct_cell = ws.cell(row=row+2, column=col_idx + 1)
        pct_cell.value = f"={pct_ref}"
        pct_cell.font = Font(color=fg_color, size=12, bold=True)
        pct_cell.alignment = Alignment(horizontal="center", vertical="center")
        pct_cell.number_format = '0%'
        
        # Merge the remaining bottom-left cell to keep things clean
        ws.merge_cells(start_row=row+2, start_column=col_idx, end_row=row+2, end_column=col_idx)
```