### 1. High-level Skill Pattern Extraction

> **Skill Name**: Cell-Based Split KPI Card

* **Tier**: component
* **Core Mechanism**: Simulates a shape-based KPI card using a formatted, merged cell grid. It splits the card into a main block (Title, Label, Value) and a secondary block (Sub-value/Market Share), using contrasting theme colors and distinct typography to create a cohesive visual container without relying on brittle floating shapes.
* **Applicability**: Executive summaries, dashboards, and automated report headers where high-visibility metrics and secondary comparative metrics (like % share or MoM change) need to be displayed side-by-side.

### 2. Structural Breakdown

- **Data Layout**: A 4-column by 3-row grid. The first 3 columns are merged horizontally per row for Title, Label, and Main Value. The 4th column is merged vertically across all 3 rows to hold the Secondary Value.
- **Formula Logic**: The `value` and `sub_value` parameters accept either literal numbers or dynamic formula strings (e.g., `"=Sheet1!B2"`) to link directly to data tables.
- **Visual Design**: The main block uses a dark themed fill with white text. The secondary block uses a lighter accent fill. Main numbers use bold, large typography (Size 14), while descriptive labels use smaller typography (Size 10-12). Center alignment is applied throughout.
- **Charts/Tables**: None (purely cell formatting).
- **Theme Hooks**: Consumes `main` (primary background), `accent` (secondary background), and `text` (font color) to ensure visual consistency across the dashboard.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter

def render(
    ws, 
    anchor: str, 
    *, 
    title: str = "Asia", 
    label: str = "Revenue", 
    value: float | str = 369989, 
    sub_value: float | str = 0.05, 
    value_format: str = "$#,##0", 
    sub_value_format: str = "0%", 
    theme: str = "corporate_blue", 
    **kwargs
) -> None:
    """
    Renders a visually striking, two-tone KPI card using merged cells.
    Values can be hardcoded numbers or formula strings (e.g., "=Data!B2").
    """
    
    # 1. Theme and Palette Setup
    themes = {
        "corporate_blue": {"main": "1F4E78", "accent": "2F75B5", "text": "FFFFFF"},
        "executive_dark": {"main": "262626", "accent": "595959", "text": "FFFFFF"},
        "emerald": {"main": "005826", "accent": "008A3C", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    main_fill = PatternFill(start_color=palette["main"], end_color=palette["main"], fill_type="solid")
    accent_fill = PatternFill(start_color=palette["accent"], end_color=palette["accent"], fill_type="solid")
    
    # Font Hierarchies
    text_color = palette["text"]
    title_font = Font(color=text_color, size=12, bold=True)
    label_font = Font(color=text_color, size=10)
    value_font = Font(color=text_color, size=14, bold=True)
    sub_font = Font(color=text_color, size=14, bold=True)
    
    center_align = Alignment(horizontal="center", vertical="center")
    
    # 2. Grid Math & Geometry (4 columns x 3 rows)
    match = coordinate_from_string(anchor)
    col_str, row_idx = match[0], match[1]
    col_idx = column_index_from_string(col_str)
    
    main_cols = [get_column_letter(col_idx + i) for i in range(3)]
    sub_col = get_column_letter(col_idx + 3)
    
    r1, r2, r3 = row_idx, row_idx + 1, row_idx + 2
    
    # 3. Structural Merges
    ws.merge_cells(f"{main_cols[0]}{r1}:{main_cols[-1]}{r1}") # Title Row
    ws.merge_cells(f"{main_cols[0]}{r2}:{main_cols[-1]}{r2}") # Label Row
    ws.merge_cells(f"{main_cols[0]}{r3}:{main_cols[-1]}{r3}") # Value Row
    ws.merge_cells(f"{sub_col}{r1}:{sub_col}{r3}")            # Sub-Value Side Block
    
    # 4. Inject Data
    ws[f"{main_cols[0]}{r1}"] = title
    ws[f"{main_cols[0]}{r2}"] = label
    ws[f"{main_cols[0]}{r3}"] = value
    ws[f"{sub_col}{r1}"] = sub_value
    
    # Number Formatting
    ws[f"{main_cols[0]}{r3}"].number_format = value_format
    ws[f"{sub_col}{r1}"].number_format = sub_value_format
    
    # 5. Apply Block Styling
    for row in range(r1, r3 + 1):
        # Paint Main Block
        for col_l in main_cols:
            cell = ws[f"{col_l}{row}"]
            cell.fill = main_fill
            cell.alignment = center_align
        
        # Paint Secondary Block
        sub_cell = ws[f"{sub_col}{row}"]
        sub_cell.fill = accent_fill
        sub_cell.alignment = center_align

    # 6. Apply Typography to Top-Left Anchors of Merged Regions
    ws[f"{main_cols[0]}{r1}"].font = title_font
    ws[f"{main_cols[0]}{r2}"].font = label_font
    ws[f"{main_cols[0]}{r3}"].font = value_font
    ws[f"{sub_col}{r1}"].font = sub_font
```