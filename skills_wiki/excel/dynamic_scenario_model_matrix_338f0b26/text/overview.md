```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Model Matrix

* **Tier**: sheet_shell
* **Core Mechanism**: Employs a data validation dropdown linked to `CHOOSE` formulas to dynamically switch an active "Live Case" assumptions block between multiple predefined scenario blocks (Base, Downside, etc.). The Live Case then natively drives the dependent calculations (e.g., an Income Statement).
* **Applicability**: Highly applicable for financial modeling, multi-year forecasting, budgeting, or any analytical spreadsheet requiring robust multi-scenario/sensitivity analysis without the use of complex macros or hidden sheets.

### 2. Structural Breakdown

- **Data Layout**: Built in vertical tiers. Top section: Core calculated output (Income Statement). Middle section: "Live Case" assumptions linking to the active scenario. Bottom section: Matrix of distinct, hardcoded scenario blocks (Scenario 1, Scenario 2).
- **Formula Logic**: Uses `=CHOOSE($toggle_cell, C21, C28)` populated across the entire Live Case block, redirecting the calculation pointer dynamically. Output section strictly references the Live Case cells.
- **Visual Design**: Uses conventional financial modeling formatting: Blue text (`0000FF`) for hardcoded assumptions, Black text for formulas, and Yellow fill (`FFF2CC`) for the primary user input/toggle cell to signal interactivity. 
- **Charts/Tables**: Standalone data grid design using themed header bands and selective double-bottom borders for margin totals.
- **Theme Hooks**: Consumes `header_bg` and `header_fg` for the master timeline header, and uses `accent` for the Live Assumptions subheader band.

### 3. Reproduction Code

```python
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Scenario Forecast", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Theme palette (fallback to corporate_blue style)
    theme_colors = {
        "corporate_blue": {"header_bg": "1F4E78", "header_fg": "FFFFFF", "accent": "D9E1F2"},
        "startup_green": {"header_bg": "27AE60", "header_fg": "FFFFFF", "accent": "EAFAF1"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    header_fill = PatternFill("solid", fgColor=palette["header_bg"])
    header_font = Font(color=palette["header_fg"], bold=True)
    bold_font = Font(bold=True)
    
    # Financial Modeling conventions
    input_font = Font(color="0000FF") # Blue text for hardcoded inputs
    input_fill = PatternFill("solid", fgColor="FFF2CC") # Yellow background for control toggles
    thin_border = Border(
        top=Side(style='thin'), bottom=Side(style='thin'), 
        left=Side(style='thin'), right=Side(style='thin')
    )
    
    # --- Title & Scenario Toggle ---
    ws["A1"] = title
    ws["A1"].font = Font(size=14, bold=True)
    
    ws["G2"] = "Active Scenario:"
    ws["G2"].font = bold_font
    ws["G2"].alignment = Alignment(horizontal="right")
    
    ws["H2"] = 1
    ws["H2"].fill = input_fill
    ws["H2"].font = input_font
    ws["H2"].border = thin_border
    ws["H2"].alignment = Alignment(horizontal="center")
    
    # Data Validation for Toggle (1 or 2)
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws["H2"])
    
    # --- Headers ---
    headers = ["Figures in USD", "Unit", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=col_idx)
        cell.value = h
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        
    # --- Section 1: Income Statement ---
    ws["A5"] = "Income Statement"
    ws["A5"].font = bold_font
    
    labels = [
        ("Revenue", "$"), 
        ("Cost of Goods Sold", "$"), 
        ("Gross Profit", "$"), 
        ("Operating Expenses", "$"), 
        ("Operating Profit", "$")
    ]
    
    for i, (label, unit) in enumerate(labels, start=6):
        ws[f"A{i}"] = label
        ws[f"B{i}"] = unit
        ws[f"B{i}"].alignment = Alignment(horizontal="center")
    
    # Dependent Output Formulas (Driven strictly by the Live Case)
    for col in range(3, 8):
        c = get_column_letter(col)
        # Revenue = Volume * Price
        ws[f"{c}6"] = f"={c}14*{c}15"
        # COGS = Volume * Unit Cost
        ws[f"{c}7"] = f"={c}14*{c}16"
        # Gross Profit = Revenue - COGS
        ws[f"{c}8"] = f"={c}6-{c}7"
        ws[f"{c}8"].font = bold_font
        ws[f"{c}8"].border = Border(top=Side(style='thin'), bottom=Side(style='double'))
        # Opex = Fixed Opex
        ws[f"{c}9"] = f"={c}17"
        # Operating Profit = GP - Opex
        ws[f"{c}10"] = f"={c}8-{c}9"
        ws[f"{c}10"].font = bold_font
        ws[f"{c}10"].border = Border(top=Side(style='thin'), bottom=Side(style='double'))

    # --- Section 2: Live Assumptions (Driven dynamically by CHOOSE) ---
    ws["A12"] = "Live Case Assumptions"
    ws["A12"].font = bold_font
    ws["A12"].fill = PatternFill("solid", fgColor=palette["accent"])
    
    assump_labels = [("Order Volume", "#"), ("Average Order Value", "$"), ("Unit COGS", "$"), ("Fixed Operations", "$")]
    for i, (label, unit) in enumerate(assump_labels, start=13):
        ws[f"A{i}"] = label
        ws[f"B{i}"] = unit
        ws[f"B{i}"].alignment = Alignment(horizontal="center")

    for row in range(14, 18): # Rows 14 to 17
        for col in range(3, 8):
            c = get_column_letter(col)
            # Scenario 1 mapping is offset 7 rows down, Scenario 2 is offset 14 rows down
            ws[f"{c}{row}"] = f"=CHOOSE($H$2, {c}{row+7}, {c}{row+14})"
            ws[f"{c}{row}"].fill = PatternFill("solid", fgColor="F2F2F2") # Subtle gray for dynamic cells

    # --- Section 3: Scenario Matrix (Hardcoded Inputs) ---
    # Scenario 1: Base Case
    ws["A20"] = "Scenario 1: Base Case (1)"
    ws["A20"].font = bold_font
    
    for i, (label, unit) in enumerate(assump_labels, start=21):
        ws[f"A{i}"] = label
        ws[f"B{i}"] = unit
        ws[f"B{i}"].alignment = Alignment(horizontal="center")
    
    base_data = [
        [3000, 6000, 10500, 15750, 21263],   # Volume
        [39.95, 39.95, 39.95, 39.95, 39.95], # Price
        [8.75, 8.75, 8.75, 8.75, 8.75],      # Unit Cost
        [20000, 20000, 30000, 30000, 30000]  # Opex
    ]
    for r_idx, row_data in enumerate(base_data, start=21):
        for c_idx, val in enumerate(row_data, start=3):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = input_font

    # Scenario 2: Downside
    ws["A27"] = "Scenario 2: Downside Case (2)"
    ws["A27"].font = bold_font
    
    for i, (label, unit) in enumerate(assump_labels, start=28):
        ws[f"A{i}"] = label
        ws[f"B{i}"] = unit
        ws[f"B{i}"].alignment = Alignment(horizontal="center")

    downside_data = [
        [2000, 4000, 7000, 10500, 14175],    # Volume
        [34.95, 34.95, 34.95, 34.95, 34.95], # Price
        [10.25, 10.25, 10.25, 10.25, 10.25], # Unit Cost
        [25000, 25000, 35000, 35000, 35000]  # Opex
    ]
    for r_idx, row_data in enumerate(downside_data, start=28):
        for c_idx, val in enumerate(row_data, start=3):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = input_font

    # --- Number Formatting & Polish ---
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 8
    for col in range(3, 9):
        ws.column_dimensions[get_column_letter(col)].width = 14
        
    # Standardize numerical layout
    num_format_rows = [6, 7, 8, 9, 10, 14, 15, 16, 17, 21, 22, 23, 24, 28, 29, 30, 31]
    for row in num_format_rows:
        for col in range(3, 8):
            ws.cell(row=row, column=col).number_format = '#,##0.00'
```
```