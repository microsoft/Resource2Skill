### 1. High-level Skill Pattern Extraction

> **Skill Name**: Data Bar KPI Table

* **Tier**: component
* **Core Mechanism**: Renders a tabular dataset and applies a `DataBarRule` conditional formatting to all numeric columns. It automatically targets numeric fields and cycles through theme colors to generate in-cell bar charts for rapid visual comparison.
* **Applicability**: Best used for leaderboards, performance scorecards, or any summary table where multiple metrics need to be compared across categorical rows (e.g., Sales Reps, Regions, Products) without cluttering the sheet with multiple standalone charts.

### 2. Structural Breakdown

- **Data Layout**: Renders headers in the anchor row, followed by data rows. Auto-detects numeric fields based on the first record.
- **Formula Logic**: None (purely data mapping + conditional formatting).
- **Visual Design**: Headers receive a solid theme fill and bold white font. Numeric cells are formatted with comma or currency formats dynamically based on column names.
- **Charts/Tables**: Employs `DataBarRule` to create inline bar charts within the cells themselves.
- **Theme Hooks**: Uses `header_bg`, `header_fg`, and a cycle of accent colors (`bar_1` through `bar_4`) to style the data bars uniquely per column.

### 3. Reproduction Code

```python
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import coordinate_to_tuple, get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import DataBarRule

def render(ws: Worksheet, anchor: str, *, data: list[dict], theme: str = "purple_dusk", **kwargs) -> None:
    """
    Renders a table with inline Data Bars for all numeric columns.
    """
    # Standard theme fallbacks
    theme_colors = {
        "corporate_blue": {"header_bg": "203764", "header_fg": "FFFFFF", "bar_1": "4472C4", "bar_2": "ED7D31", "bar_3": "A5A5A5", "bar_4": "FFC000"},
        "purple_dusk": {"header_bg": "403151", "header_fg": "FFFFFF", "bar_1": "7030A0", "bar_2": "FFC000", "bar_3": "B2A1C7", "bar_4": "8064A2"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    start_row, start_col = coordinate_to_tuple(anchor)
    if not data:
        return
        
    headers = list(data[0].keys())
    
    header_fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    header_font = Font(color=palette["header_fg"], bold=True)
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    
    # 1. Render Headers
    for c_idx, header in enumerate(headers):
        cell = ws.cell(row=start_row, column=start_col + c_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center if c_idx > 0 else align_left
        
    # 2. Render Data Rows
    for r_idx, row_dict in enumerate(data, start=1):
        for c_idx, header in enumerate(headers):
            val = row_dict.get(header, 0)
            cell = ws.cell(row=start_row + r_idx, column=start_col + c_idx, value=val)
            
            # Smart number formatting
            if isinstance(val, (int, float)):
                if "value" in header.lower() or "$" in header:
                    cell.number_format = '$#,##0'
                elif isinstance(val, float):
                    cell.number_format = '#,##0.00'
                else:
                    cell.number_format = '#,##0'
                    
    # 3. Adjust Column Widths
    for c_idx, header in enumerate(headers):
        col_letter = get_column_letter(start_col + c_idx)
        ws.column_dimensions[col_letter].width = max(len(str(header)) + 4, 12)
        
    # 4. Apply Data Bars to Numeric Columns
    bar_colors = [palette["bar_1"], palette["bar_2"], palette["bar_3"], palette["bar_4"]]
    color_idx = 0
    end_row = start_row + len(data)
    
    for c_idx, header in enumerate(headers):
        # Sample first row to detect numeric columns
        sample_val = data[0].get(header)
        if isinstance(sample_val, (int, float)):
            col_letter = get_column_letter(start_col + c_idx)
            range_str = f"{col_letter}{start_row + 1}:{col_letter}{end_row}"
            
            bar_color = bar_colors[color_idx % len(bar_colors)]
            
            # DataBarRule requires an 8-character ARGB hex string, e.g., 'FF' + 6-char hex
            rule = DataBarRule(start_type='min', end_type='max', color=f"FF{bar_color}")
            ws.conditional_formatting.add(range_str, rule)
            
            color_idx += 1
```