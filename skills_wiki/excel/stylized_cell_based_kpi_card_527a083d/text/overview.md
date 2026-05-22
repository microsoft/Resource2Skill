```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Stylized Cell-Based KPI Card

* **Tier**: component
* **Core Mechanism**: Translates the tutorial's shape-based KPI approach into a robust, cell-based component that natively supports dynamic openpyxl formula linking. Constructs a unified visual "card" by merging a 3x2 grid of cells, applying heavy outer borders, and utilizing contrasting theme fills to create a distinct "badge" area for percentage metrics.
* **Applicability**: Ideal for executive dashboards and summary sheets where high-level metrics (e.g., Regional Revenue & Market Share) need to stand out as designed elements rather than raw tabular data. 

### 2. Structural Breakdown

- **Data Layout**: A 3-row by 2-column cell block. The top row (Cols 1-2) is merged for the Title. The bottom right (Rows 2-3, Col 2) is merged vertically for the percentage badge.
- **Formula Logic**: Accepts direct cell reference strings (e.g., `'Data'!B2`) and prepends `=` to ensure the card remains dynamically linked to the source data, mimicking shape formula links.
- **Visual Design**: Uses a dark primary fill for the main body and a lighter accent fill for the percentage badge. Text is bold and white (`#FFFFFF`) for maximum contrast. A medium outer border unifies the separate cells into a single "shape".
- **Charts/Tables**: N/A
- **Theme Hooks**: Consumes `primary` for the card body, `accent` for the badge background, and `text` (white) for typography. 

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, title: str, subtitle: str, value_ref: str, percent_ref: str, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import coordinate_to_tuple, get_column_letter

    # 1. Setup Theme Palette
    palettes = {
        "corporate_blue": {"primary": "1F4E78", "accent": "2F75B5", "text": "FFFFFF", "border": "000000"},
        "executive_dark": {"primary": "262626", "accent": "595959", "text": "FFFFFF", "border": "000000"},
        "emerald_green": {"primary": "0F52BA", "accent": "50C878", "text": "FFFFFF", "border": "000000"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    start_row, start_col = coordinate_to_tuple(anchor)
    
    # 2. Define Layout & Merges (3 rows x 2 cols)
    ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col+1)       # Title Header
    ws.merge_cells(start_row=start_row+1, start_column=start_col+1, end_row=start_row+2, end_column=start_col+1) # Percent Badge
    
    title_cell = ws.cell(row=start_row, column=start_col)
    subtitle_cell = ws.cell(row=start_row+1, column=start_col)
    value_cell = ws.cell(row=start_row+2, column=start_col)
    percent_cell = ws.cell(row=start_row+1, column=start_col+1)

    # 3. Inject Data / Formulas
    title_cell.value = title
    subtitle_cell.value = subtitle
    
    # Ensure references are treated as active formulas
    value_cell.value = f"={value_ref}" if not str(value_ref).startswith("=") else value_ref
    percent_cell.value = f"={percent_ref}" if not str(percent_ref).startswith("=") else percent_ref

    # 4. Styling Definitions
    main_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    badge_fill = PatternFill(start_color=palette["accent"], end_color=palette["accent"], fill_type="solid")
    
    title_font = Font(color=palette["text"], size=12, bold=True)
    sub_font = Font(color=palette["text"], size=10)
    val_font = Font(color=palette["text"], size=14, bold=True)
    
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center", indent=1)

    # 5. Apply Fills (Iterate full block to cover merged underlying cells)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 2):
            cell = ws.cell(row=r, column=c)
            if c == start_col + 1 and r > start_row:
                cell.fill = badge_fill
            else:
                cell.fill = main_fill

    # Apply Fonts and Alignment
    title_cell.font = title_font
    title_cell.alignment = center_align

    subtitle_cell.font = sub_font
    subtitle_cell.alignment = left_align

    value_cell.font = val_font
    value_cell.alignment = left_align
    value_cell.number_format = '"$"#,##0'

    percent_cell.font = val_font
    percent_cell.alignment = center_align
    percent_cell.number_format = '0%'

    # 6. Apply Outer Border to unify the "Card" shape
    thick = Side(border_style="medium", color=palette["border"])
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 2):
            cell = ws.cell(row=r, column=c)
            cell.border = Border(
                top=thick if r == start_row else None,
                bottom=thick if r == start_row + 2 else None,
                left=thick if c == start_col else None,
                right=thick if c == start_col + 1 else None
            )

    # 7. Shape Sizing Adjustments
    ws.column_dimensions[get_column_letter(start_col)].width = 18
    ws.column_dimensions[get_column_letter(start_col+1)].width = 12
    ws.row_dimensions[start_row].height = 20
    ws.row_dimensions[start_row+1].height = 15
    ws.row_dimensions[start_row+2].height = 25
```
```