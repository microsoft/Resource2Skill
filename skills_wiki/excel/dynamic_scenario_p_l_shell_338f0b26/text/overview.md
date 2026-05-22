### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario P&L Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Drives a financial model using a central "Live Case" assumptions block, which dynamically pulls values from multiple scenario blocks (Base, Upside, Downside) using the `CHOOSE` function. A Data Validation dropdown acts as the scenario toggle switch. 
* **Applicability**: Best used for financial statements, budgets, or valuation models that require sensitivity analysis. It separates hard-coded inputs (blue font) from dynamic formula-driven inputs (black font) to maintain model integrity.

### 2. Structural Breakdown

- **Data Layout**: Top section contains the output Income Statement. Middle section contains the "Live Case" formula block. Bottom sections contain hard-coded scenario data blocks.
- **Formula Logic**: `=CHOOSE($I$2, C15, C27)` dynamically routes the cell reference to either the Base Case or Upside Case block based on the index selected in the dropdown cell (`I2`).
- **Visual Design**: Hard-coded inputs use a blue font convention standard in financial modeling. The active scenario toggle uses a prominent accent fill. Summary rows use top borders for standard accounting presentation.
- **Charts/Tables**: Clean cell layout with column width adjustments and numeric formatting (`#,##0` for units/currency).
- **Theme Hooks**: Uses `header_bg` and `header_fg` for section title bars, and `accent` for the interactive scenario dropdown cell.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

def render_sheet(wb, sheet_name: str, *, title: str = "Financial Model", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Mock theme palette
    colors = {
        "header_bg": "2C3E50",
        "header_fg": "FFFFFF",
        "input_fg": "0000FF",  # Standard financial modeling convention for hard-coded inputs
        "accent": "F1C40F",    # Yellow/orange for interactive cells
        "border": "BDC3C7",
        "live_bg": "ECF0F1"
    }
    
    # Styles
    header_fill = PatternFill(start_color=colors["header_bg"], end_color=colors["header_bg"], fill_type="solid")
    header_font = Font(color=colors["header_fg"], bold=True)
    input_font = Font(color=colors["input_fg"])
    bold_font = Font(bold=True)
    dropdown_fill = PatternFill(start_color=colors["accent"], end_color=colors["accent"], fill_type="solid")
    live_case_fill = PatternFill(start_color=colors["live_bg"], end_color=colors["live_bg"], fill_type="solid")
    
    thin_side = Side(style="thin", color=colors["border"])
    top_border = Border(top=thin_side)
    
    # Column widths
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 5
    for col in ['C', 'D', 'E']:
        ws.column_dimensions[col].width = 15
        
    # --- Scenario Toggler ---
    ws['H2'] = "Scenario Selection:"
    ws['H2'].font = bold_font
    ws['H2'].alignment = Alignment(horizontal="right")
    
    ws['I2'] = 1
    ws['I2'].fill = dropdown_fill
    ws['I2'].alignment = Alignment(horizontal="center")
    ws['I2'].border = Border(top=thin_side, bottom=thin_side, left=thin_side, right=thin_side)
    
    # Add Data Validation for the dropdown
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws['I2'])
    
    # --- P&L Header ---
    ws['A4'] = title
    ws['A4'].font = header_font
    ws['A4'].fill = header_fill
    for i, col in enumerate(['B', 'C', 'D', 'E']):
        ws[f'{col}4'] = f"Year {i}" if i > 0 else "Unit"
        ws[f'{col}4'].font = header_font
        ws[f'{col}4'].fill = header_fill
        ws[f'{col}4'].alignment = Alignment(horizontal="center")
        
    # --- P&L Calculation Block ---
    ws['A5'] = "Revenue"
    ws['B5'] = "$"
    for col in ['C', 'D', 'E']:
        ws[f'{col}5'] = f"={col}21*{col}22" # Orders * AOV
        ws[f'{col}5'].number_format = '#,##0'
        
    ws['A6'] = "Cost of Goods Sold"
    ws['B6'] = "$"
    for col in ['C', 'D', 'E']:
        ws[f'{col}6'] = f"={col}21*{col}23" # Orders * COGS
        ws[f'{col}6'].number_format = '#,##0'
        
    ws['A7'] = "Gross Profit"
    ws['A7'].font = bold_font
    ws['B7'] = "$"
    for col in ['C', 'D', 'E']:
        ws[f'{col}7'] = f"={col}5-{col}6"
        ws[f'{col}7'].border = top_border
        ws[f'{col}7'].font = bold_font
        ws[f'{col}7'].number_format = '#,##0'
        
    ws['A8'] = "Operating Expenses"
    ws['B8'] = "$"
    for col in ['C', 'D', 'E']:
        ws[f'{col}8'] = f"={col}24"
        ws[f'{col}8'].number_format = '#,##0'
        
    ws['A9'] = "Operating Profit"
    ws['A9'].font = bold_font
    ws['B9'] = "$"
    for col in ['C', 'D', 'E']:
        ws[f'{col}9'] = f"={col}7-{col}8"
        ws[f'{col}9'].border = top_border
        ws[f'{col}9'].font = bold_font
        ws[f'{col}9'].number_format = '#,##0'
        
    # --- Assumptions Header ---
    ws['A12'] = "Assumptions"
    ws['A12'].font = header_font
    ws['A12'].fill = header_fill
    for col in ['B', 'C', 'D', 'E']:
        ws[f'{col}12'].fill = header_fill
    
    # --- Scenario 1: Base Case (Hardcoded inputs) ---
    ws['A14'] = "Base Case (Scenario 1)"
    ws['A14'].font = bold_font
    ws['A15'] = "Number of Orders"
    ws['A16'] = "Average Order Value"
    ws['A17'] = "COGS per order"
    ws['A18'] = "Fixed OPEX"
    
    base_data = [
        [3000, 6000, 10500],
        [39.95, 39.95, 39.95],
        [8.75, 8.75, 8.75],
        [20000, 30000, 30000]
    ]
    for r_idx, row_data in enumerate(base_data, start=15):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=r_idx, column=3+c_idx, value=val)
            cell.font = input_font
            cell.number_format = '#,##0.00' if r_idx in [16, 17] else '#,##0'

    # --- Live Case: CHOOSE Formulas ---
    ws['A20'] = "Live Case"
    ws['A20'].font = bold_font
    ws['A20'].fill = live_case_fill
    for col in ['B', 'C', 'D', 'E']:
        ws[f'{col}20'].fill = live_case_fill

    ws['A21'] = "Number of Orders"
    ws['A22'] = "Average Order Value"
    ws['A23'] = "COGS per order"
    ws['A24'] = "Fixed OPEX"
    
    for r_idx in range(21, 25):
        for c_idx, col in enumerate(['C', 'D', 'E']):
            base_ref = f"{col}{r_idx - 6}"
            upside_ref = f"{col}{r_idx + 6}"
            # Core Mechanism: CHOOSE switches the data source based on I2
            cell = ws.cell(row=r_idx, column=3+c_idx, value=f"=CHOOSE($I$2, {base_ref}, {upside_ref})")
            cell.number_format = '#,##0.00' if r_idx in [22, 23] else '#,##0'

    # --- Scenario 2: Upside Case (Hardcoded inputs) ---
    ws['A26'] = "Upside Case (Scenario 2)"
    ws['A26'].font = bold_font
    ws['A27'] = "Number of Orders"
    ws['A28'] = "Average Order Value"
    ws['A29'] = "COGS per order"
    ws['A30'] = "Fixed OPEX"
    
    upside_data = [
        [4000, 9000, 15000],
        [45.00, 45.00, 45.00],
        [8.00, 7.50, 7.00],
        [25000, 35000, 40000]
    ]
    for r_idx, row_data in enumerate(upside_data, start=27):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=r_idx, column=3+c_idx, value=val)
            cell.font = input_font
            cell.number_format = '#,##0.00' if r_idx in [28, 29] else '#,##0'
```