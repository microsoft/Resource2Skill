# Interactive Two-Way Lookup

## Applicability

Best for dashboards, pricing matrices, and schedule tables where a specific value must be retrieved from a 2D cross-tab based on two user-selected parameters.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Two-Way Lookup

* **Tier**: component
* **Core Mechanism**: Combines an `INDEX` array with two `MATCH` functions (one for row position, one for column position) to pull a dynamic intersection from a matrix. Adds data validation dropdowns so the user can interactively change the lookup targets.
* **Applicability**: Best for dashboards, pricing matrices, and schedule tables where a specific value must be retrieved from a 2D cross-tab based on two user-selected parameters.

### 2. Structural Breakdown

- **Data Layout**: A 2D data matrix (row headers down the left, column headers across the top). Two empty rows below, followed by a vertically stacked 3-row "Interactive Lookup Tool" control block.
- **Formula Logic**: `=INDEX(C3:F7, MATCH(C10, B3:B7, 0), MATCH(C11, C2:F2, 0))` to resolve exact coordinates based on the respective dropdowns.
- **Visual Design**: Themed dark headers for the reference table, thin borders for readability, and distinct `accent` background fills to signal user-editable dropdowns.
- **Charts/Tables**: Standard spreadsheet grid mimicking a cross-tab data view.
- **Theme Hooks**: `header_bg` and `header_fg` for the matrix headers; `accent` for the interactive dropdown input cells.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter, column_index_from_string

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme configuration
    themes = {
        "corporate_blue": {"header_bg": "002060", "header_fg": "FFFFFF", "accent": "D9E1F2"},
        "green_energy": {"header_bg": "00502F", "header_fg": "FFFFFF", "accent": "E2EFDA"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    col_str = ''.join(filter(str.isalpha, anchor))
    row_num = int(''.join(filter(str.isdigit, anchor)))
    col_idx = column_index_from_string(col_str)
    
    # Mock data
    row_headers = ["Batman", "Ben Ten", "Bob The Builder", "Mr Maker", "Night Garden"]
    col_headers = ["East", "North", "South", "West"]
    values = [
        [102, 91, 87, 99],
        [107, 133, 125, 140],
        [91, 73, 85, 79],
        [49, 50, 59, 51],
        [57, 44, 37, 32]
    ]
    
    # Styles
    header_fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    header_font = Font(color=palette["header_fg"], bold=True)
    accent_fill = PatternFill(start_color=palette["accent"], end_color=palette["accent"], fill_type="solid")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # 2. Draw Table Headers
    top_left = ws.cell(row=row_num, column=col_idx, value="Program \\ Region")
    top_left.fill = header_fill
    top_left.font = header_font
    top_left.border = thin_border
    
    for i, h in enumerate(col_headers):
        cell = ws.cell(row=row_num, column=col_idx + 1 + i, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center")
        
    # 3. Draw Data Rows
    for r_i, row_label in enumerate(row_headers):
        r_cell = ws.cell(row=row_num + 1 + r_i, column=col_idx, value=row_label)
        r_cell.font = Font(bold=True)
        r_cell.border = thin_border
        for c_i, val in enumerate(values[r_i]):
            d_cell = ws.cell(row=row_num + 1 + r_i, column=col_idx + 1 + c_i, value=val)
            d_cell.border = thin_border
            d_cell.alignment = Alignment(horizontal="center")
            
    # 4. Lookup Tool UI Section
    lookup_start_row = row_num + len(row_headers) + 2
    
    title_cell = ws.cell(row=lookup_start_row, column=col_idx, value="Interactive Lookup Tool")
    title_cell.font = Font(bold=True, size=12)
    
    ws.cell(row=lookup_start_row + 1, column=col_idx, value="Select Program:")
    ws.cell(row=lookup_start_row + 2, column=col_idx, value="Select Region:")
    ws.cell(row=lookup_start_row + 3, column=col_idx, value="Total Views:")
    
    # 5. Connect Data Validation Rules
    dv_prog_range = f"${get_column_letter(col_idx)}${row_num+1}:${get_column_letter(col_idx)}${row_num+len(row_headers)}"
    dv_program = DataValidation(type="list", formula1=dv_prog_range, allow_blank=True)
    ws.add_data_validation(dv_program)
    
    dv_reg_range = f"${get_column_letter(col_idx+1)}${row_num}:${get_column_letter(col_idx+len(col_headers))}${row_num}"
    dv_region = DataValidation(type="list", formula1=dv_reg_range, allow_blank=True)
    ws.add_data_validation(dv_region)
    
    # 6. Apply UI cells
    prog_cell = ws.cell(row=lookup_start_row + 1, column=col_idx + 1)
    prog_cell.value = row_headers[0]
    prog_cell.fill = accent_fill
    prog_cell.border = thin_border
    dv_program.add(prog_cell)
    
    reg_cell = ws.cell(row=lookup_start_row + 2, column=col_idx + 1)
    reg_cell.value = col_headers[0]
    reg_cell.fill = accent_fill
    reg_cell.border = thin_border
    dv_region.add(reg_cell)
    
    # 7. Construct dynamic INDEX & MATCH formula
    index_range = f"{get_column_letter(col_idx+1)}{row_num+1}:{get_column_letter(col_idx+len(col_headers))}{row_num+len(row_headers)}"
    match_prog_range = f"{get_column_letter(col_idx)}{row_num+1}:{get_column_letter(col_idx)}{row_num+len(row_headers)}"
    match_reg_range = f"{get_column_letter(col_idx+1)}{row_num}:{get_column_letter(col_idx+len(col_headers))}{row_num}"
    
    formula = f"=INDEX({index_range}, MATCH({prog_cell.coordinate}, {match_prog_range}, 0), MATCH({reg_cell.coordinate}, {match_reg_range}, 0))"
    
    res_cell = ws.cell(row=lookup_start_row + 3, column=col_idx + 1)
    res_cell.value = formula
    res_cell.font = Font(bold=True, color=palette["header_bg"])
    res_cell.border = thin_border
    
    # Layout adjustments
    ws.column_dimensions[get_column_letter(col_idx)].width = 18
    for i in range(len(col_headers)):
        ws.column_dimensions[get_column_letter(col_idx + 1 + i)].width = 12
```