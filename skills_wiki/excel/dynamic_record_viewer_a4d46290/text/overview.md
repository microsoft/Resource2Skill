# Dynamic Record Viewer

## Applicability

Ideal for employee directories, product catalogs, invoice inspection, or adding a standalone interactive "search" pane to summary dashboards.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Record Viewer

* **Tier**: component
* **Core Mechanism**: Creates a mini-dashboard search widget that takes user input and uses a single `XLOOKUP` formula to return an entire array (full row of data) using Excel's dynamic array spilling. It includes a built-in fallback message for unfound records to prevent `#N/A` errors.
* **Applicability**: Ideal for employee directories, product catalogs, invoice inspection, or adding a standalone interactive "search" pane to summary dashboards.

### 2. Structural Breakdown

- **Data Layout**: Places a labeled input cell at the anchor, drops down two rows to generate formatted result headers, and places the `XLOOKUP` formula directly beneath the first header cell.
- **Formula Logic**: `=XLOOKUP({input_cell}, {lookup_range}, {return_range}, "{not_found_msg}")` - The key here is that `return_range` spans multiple columns, allowing the formula to natively spill the entire record across the styled cells.
- **Visual Design**: The search input cell receives a subtle highlight fill and bottom border to indicate it is editable. The result headers get a solid theme background with light text to frame the output data. 
- **Charts/Tables**: N/A
- **Theme Hooks**: Consumes `primary` for header backgrounds, `header_text` for header font colors, and `accent` for the interactive input cell highlight.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter

def render(ws, anchor: str, *, 
           search_label: str = "Search ID:", 
           headers: list[str] = ["Name", "Job Title", "Salary"], 
           lookup_range: str = "Data!E2:E100", 
           return_range: str = "Data!A2:C100", 
           not_found_msg: str = "No such person", 
           theme: str = "corporate_blue", 
           **kwargs) -> None:
    
    # 1. Theme configuration
    palettes = {
        "corporate_blue": {"primary": "4F81BD", "accent": "EBF1DE", "text": "000000", "header_text": "FFFFFF"},
        "modern_dark": {"primary": "262626", "accent": "D9D9D9", "text": "000000", "header_text": "FFFFFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    
    header_fill = PatternFill("solid", fgColor=palette["primary"])
    header_font = Font(color=palette["header_text"], bold=True)
    input_fill = PatternFill("solid", fgColor=palette["accent"])
    thin_bottom = Border(bottom=Side(style="thin", color="A6A6A6"))
    
    col_str, row_str = coordinate_from_string(anchor)
    start_col = column_index_from_string(col_str)
    start_row = int(row_str)
    
    # 2. Search Box Setup
    search_label_cell = ws.cell(row=start_row, column=start_col)
    search_label_cell.value = search_label
    search_label_cell.font = Font(bold=True, color=palette["text"])
    search_label_cell.alignment = Alignment(horizontal="right")
    
    input_cell = ws.cell(row=start_row, column=start_col + 1)
    input_cell.fill = input_fill
    input_cell.border = thin_bottom
    input_cell.value = "AC0016"  # Sample active input to show functionality
    input_cell_ref = input_cell.coordinate
    
    # 3. Results Header Setup
    header_start_row = start_row + 2
    for i, header in enumerate(headers):
        h_cell = ws.cell(row=header_start_row, column=start_col + i)
        h_cell.value = header
        h_cell.fill = header_fill
        h_cell.font = header_font
        h_cell.alignment = Alignment(horizontal="center", vertical="center")
        h_cell.border = Border(bottom=Side(style="medium", color=palette["primary"]))
        
    # 4. Dynamic XLOOKUP Array Formula
    formula_start_row = start_row + 3
    formula_cell = ws.cell(row=formula_start_row, column=start_col)
    
    # XLOOKUP returning an array of columns (spill dynamic array)
    formula = f'=XLOOKUP({input_cell_ref}, {lookup_range}, {return_range}, "{not_found_msg}")'
    formula_cell.value = formula
    
    # Pre-format the spill area alignment
    for i in range(len(headers)):
        d_cell = ws.cell(row=formula_start_row, column=start_col + i)
        d_cell.alignment = Alignment(horizontal="center")
        d_cell.font = Font(color=palette["text"])
        
    # Adjust column widths for better readability
    ws.column_dimensions[get_column_letter(start_col)].width = 15
    for i in range(1, len(headers)):
        ws.column_dimensions[get_column_letter(start_col + i)].width = 20
```