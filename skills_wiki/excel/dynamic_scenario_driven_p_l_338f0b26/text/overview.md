### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario-Driven P&L

* **Tier**: sheet_shell
* **Core Mechanism**: Build separate static data blocks for each scenario (Upper/Lower), then use a centralized `CHOOSE` function linked to a Data Validation dropdown to populate a "Live Case" block. The P&L calculations point exclusively to the Live Case.
* **Applicability**: Perfect for financial models, forecasting, or budgeting where users need to instantly toggle between Base/Best/Worst case assumptions without rewriting inputs.

### 2. Structural Breakdown

- **Data Layout**: 
  - Rows 4-11: Core Income Statement.
  - Rows 15-21: Live Case Assumptions (fully dynamic `CHOOSE` formulas).
  - Rows 24-30: Scenario 1 (Upper Case) hardcoded assumptions + internal growth formulas.
  - Rows 33-39: Scenario 2 (Lower Case) assumptions.
- **Formula Logic**: Central toggle `=CHOOSE($I$2, D25, D34)` routes the active scenario into the Live Case. Dependent revenue/COGS formulas rely purely on the Live Case.
- **Visual Design**: Hardcoded inputs receive a blue font (`0000FF`) to distinguish them from formulas (black), matching financial modeling conventions. Standard accounting borders (top single, bottom double) apply to profit lines.
- **Charts/Tables**: N/A - layout relies on cleanly spaced summary sections.
- **Theme Hooks**: Employs a primary header fill for the time-series labels and a warning/accent color to highlight the active scenario dropdown.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

def render_sheet(wb, sheet_name: str, *, title: str = "Scenario Model", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Theme configuration
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    bold_font = Font(bold=True)
    input_font = Font(color="0000FF") # Blue for hardcoded inputs
    toggle_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    # Column widths
    ws.column_dimensions['A'].width = 2
    ws.column_dimensions['B'].width = 28
    ws.column_dimensions['C'].width = 8
    for c in range(4, 9):
        ws.column_dimensions[get_column_letter(c)].width = 14
        
    # Scenario Toggle
    ws['H2'] = "Scenario"
    ws['H2'].font = bold_font
    ws['H2'].alignment = Alignment(horizontal="right")
    ws['I2'] = 1
    ws['I2'].fill = toggle_fill
    ws['I2'].border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                             top=Side(style='thin'), bottom=Side(style='thin'))
    ws['I2'].alignment = Alignment(horizontal="center")
    
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws['I2'])
    
    # Headers
    ws['B3'] = "Figures in USD"
    ws['B3'].font = bold_font
    ws['C3'] = "Unit"
    for i in range(5):
        ws.cell(row=3, column=4+i, value=f"Year {i+1}")
        
    for c in range(2, 10): # Color across to scenario toggle
        cell = ws.cell(row=3, column=c)
        cell.fill = header_fill
        cell.font = header_font
        if c >= 3:
            cell.alignment = Alignment(horizontal="center")

    def set_format(cell, unit, label):
        if unit == "%":
            cell.number_format = "0%"
        elif unit == "$":
            if "Value" in label or "per order" in label:
                cell.number_format = "$#,##0.00"
            else:
                cell.number_format = "#,##0"
        elif unit == "#":
            cell.number_format = "#,##0"

    # --- Income Statement ---
    ws['B4'] = "Income Statement"
    ws['B4'].font = bold_font
    
    is_labels = [
        ("Revenue", "$"), ("Cost of Goods Sold", "$"), ("Gross Profit", "$"),
        ("Operating Expenses", "$"), ("Operating Profit", "$"),
        ("Corporate Tax", "$"), ("Net Income", "$")
    ]
    
    for idx, (label, unit) in enumerate(is_labels):
        r = 5 + idx
        ws.cell(row=r, column=2, value=label)
        ws.cell(row=r, column=3, value=unit).alignment = Alignment(horizontal="center")
        for c in range(4, 9):
            col = get_column_letter(c)
            if idx == 0:   # Rev
                form = f"={col}16*{col}18"
            elif idx == 1: # COGS
                form = f"={col}16*{col}19"
            elif idx == 2: # GP
                form = f"={col}5-{col}6"
            elif idx == 3: # Opex
                form = f"={col}20"
            elif idx == 4: # Op Profit
                form = f"={col}7-{col}8"
            elif idx == 5: # Tax
                form = f"=IF({col}9>0, {col}9*{col}21, 0)"
            elif idx == 6: # Net Income
                form = f"={col}9-{col}10"
                
            cell = ws.cell(row=r, column=c, value=form)
            set_format(cell, unit, label)

    # Styling Totals
    top_thin = Border(top=Side(style="thin"))
    double_bottom = Border(top=Side(style="thin"), bottom=Side(style="double"))
    for r, is_double in [(7, False), (9, False), (11, True)]:
        ws.cell(row=r, column=2).font = bold_font
        for c in range(4, 9):
            ws.cell(row=r, column=c).border = double_bottom if is_double else top_thin
            ws.cell(row=r, column=c).font = bold_font

    # --- Assumptions Config ---
    assumptions_labels = [
        ("Number of Orders", "#"), ("Order Growth Rate", "%"), 
        ("Average Order Value", "$"), ("COGS (per order)", "$"), 
        ("Total Operating Expenses", "$"), ("Corporate Tax Rate", "%")
    ]
    
    def write_block(start_row, title_text, data_func=None):
        ws.cell(row=start_row, column=2, value=title_text).font = bold_font
        for idx, (lbl, unit) in enumerate(assumptions_labels):
            r = start_row + 1 + idx
            ws.cell(row=r, column=2, value=lbl)
            ws.cell(row=r, column=3, value=unit).alignment = Alignment(horizontal="center")
            
            if data_func:
                for c in range(4, 9):
                    val = data_func(idx, c - 4)
                    cell = ws.cell(row=r, column=c, value=val)
                    set_format(cell, unit, lbl)
                    # Color hardcoded inputs blue
                    if not (isinstance(val, str) and val.startswith("=")):
                        cell.font = input_font

    # Scenario 1 Data (Starts Row 24)
    def upper_data(row_idx, yr_idx):
        if row_idx == 0: return 3000 if yr_idx == 0 else f"={get_column_letter(4+yr_idx-1)}25*(1+{get_column_letter(4+yr_idx)}26)"
        if row_idx == 1: return [0, 1.0, 0.75, 0.50, 0.35][yr_idx]
        if row_idx == 2: return 39.95
        if row_idx == 3: return 8.75
        if row_idx == 4: return 100000
        if row_idx == 5: return 0.20
    write_block(24, "Upper Case (Scenario 1)", upper_data)

    # Scenario 2 Data (Starts Row 33)
    def lower_data(row_idx, yr_idx):
        if row_idx == 0: return 2000 if yr_idx == 0 else f"={get_column_letter(4+yr_idx-1)}34*(1+{get_column_letter(4+yr_idx)}35)"
        if row_idx == 1: return [0, 0.50, 0.30, 0.15, 0.10][yr_idx]
        if row_idx == 2: return 34.95
        if row_idx == 3: return 9.50
        if row_idx == 4: return 120000
        if row_idx == 5: return 0.25
    write_block(33, "Lower Case (Scenario 2)", lower_data)

    # Live Case Data (CHOOSE logic - Starts Row 15)
    write_block(15, "Live Case")
    for idx, (lbl, unit) in enumerate(assumptions_labels):
        r = 16 + idx
        for c in range(4, 9):
            col = get_column_letter(c)
            upper_cell = f"{col}{25 + idx}"
            lower_cell = f"{col}{34 + idx}"
            cell = ws.cell(row=r, column=c, value=f"=CHOOSE($I$2, {upper_cell}, {lower_cell})")
            set_format(cell, unit, lbl)
```