# Dark Mode Toggle Sheet

## Applicability

Best used in dashboards, large data tables, or reporting tools where users may prefer a low-glare dark theme for extended reading or aesthetic preference.

## Analysis

```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dark Mode Toggle Sheet

* **Tier**: sheet_shell
* **Core Mechanism**: Implements a UI toggle to switch a worksheet between light and dark modes. While the video uses a VBA/ActiveX Toggle Button, this implementation adapts the pattern to use pure-Excel Data Validation (a dropdown) linked to conditional formatting rules. This provides the exact same UX without requiring macros.
* **Applicability**: Best used in dashboards, large data tables, or reporting tools where users may prefer a low-glare dark theme for extended reading or aesthetic preference.

### 2. Structural Breakdown

- **Data Layout**: A dedicated "Theme Mode" toggle cell (e.g., `B2`) situated above the main data table. A title row that is excluded from the conditional formatting to maintain its distinct styling.
- **Formula Logic**: Conditional formatting uses the formula `=$B$2="Dark"` applied across the table ranges.
- **Visual Design**: Dark mode applies a deep blue/grey background (`#203764`) with white font for the table body, and a slightly lighter dark hue (`#2F5597`) for the headers to preserve visual hierarchy.
- **Charts/Tables**: Applies to standard cell ranges (simulating a table) to allow maximum formatting flexibility.
- **Theme Hooks**: Primary dark backgrounds, contrasting text colors, and an accent color for the static title bar.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

def render_sheet(wb, sheet_name: str, *, title: str = "Risk Register", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # 1. Setup Theme Toggle Control (Macro-free adaptation)
    ws["A2"] = "Theme Mode:"
    ws["A2"].font = Font(bold=True)
    ws["A2"].alignment = Alignment(horizontal="right")
    
    toggle_cell = "B2"
    ws[toggle_cell] = "Light"
    ws[toggle_cell].font = Font(bold=True)
    ws[toggle_cell].alignment = Alignment(horizontal="center")
    
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                         top=Side(style='thin'), bottom=Side(style='thin'))
    ws[toggle_cell].border = thin_border
    
    # Add Data Validation for the dropdown toggle
    dv = DataValidation(type="list", formula1='"Light,Dark"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws[toggle_cell])
    
    # 2. Add Static Title (Excluded from Conditional Formatting)
    ws["A1"] = title
    ws["A1"].font = Font(size=14, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill(start_color="D2492A", end_color="D2492A", fill_type="solid")
    ws.merge_cells("A1:G1")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 25
    
    # 3. Create Sample Data Table
    headers = ["Risk #", "Date Raised", "Risk Description", "Impact", "Likelihood", "Severity", "Status"]
    data = [
        [1, "2021-01-02", "Volcano eruption flight cancellation", "Major", "Unlikely", "High", "Open"],
        [2, "2021-01-02", "Train strikes in Paris", "Major", "Possible", "High", "Open"],
        [3, "2021-01-03", "Budget overrun", "Moderate", "Likely", "Medium", "Closed"],
        [4, "2021-01-04", "Key personnel sick", "Moderate", "Possible", "Medium", "Open"]
    ]
    
    header_row = 4
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=col_idx, value=h)
        cell.font = Font(bold=True)
        cell.border = thin_border
        cell.fill = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid")
        
    for r_idx, row_data in enumerate(data, start=header_row + 1):
        for c_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border

    # Adjust column widths
    ws.column_dimensions['C'].width = 35
    for col in ['A', 'B', 'D', 'E', 'F', 'G']:
        ws.column_dimensions[col].width = 15

    # 4. Apply Dark Mode Conditional Formatting
    dark_fill_body = PatternFill(start_color="203764", end_color="203764", fill_type="solid")
    dark_font_body = Font(color="FFFFFF")
    
    dark_fill_header = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    dark_font_header = Font(color="FFFFFF", bold=True)
    
    body_range = f"A{header_row + 1}:G{header_row + len(data)}"
    header_range = f"A{header_row}:G{header_row}"
    
    # Body Rule
    ws.conditional_formatting.add(
        body_range,
        FormulaRule(
            formula=[f'=${toggle_cell}="Dark"'], 
            stopIfTrue=True, 
            font=dark_font_body, 
            fill=dark_fill_body
        )
    )
    
    # Header Rule
    ws.conditional_formatting.add(
        header_range,
        FormulaRule(
            formula=[f'=${toggle_cell}="Dark"'], 
            stopIfTrue=True, 
            font=dark_font_header, 
            fill=dark_fill_header
        )
    )
```
```