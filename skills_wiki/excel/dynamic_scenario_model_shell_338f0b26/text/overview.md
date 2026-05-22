### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Model Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Uses a central `CHOOSE` function linked to a Data Validation dropdown to dynamically toggle "Live Case" assumptions between multiple hard-coded scenario blocks. The financial calculation engine then feeds entirely off the Live Case block.
* **Applicability**: Perfect for financial models, budgeting, or forecasting templates where users need to compare base, best, and worst-case scenarios without duplicating the entire calculation engine.

### 2. Structural Breakdown

- **Data Layout**: Top section for calculations (Income Statement), middle section for Live Assumptions, and bottom sections for hard-coded scenario blocks (Scenario 1: Upper Case, Scenario 2: Lower Case). Scenario toggle cell is placed prominently at the top right.
- **Formula Logic**: `=CHOOSE($H$2, B15, B20)` dynamically pulls the right assumption based on the toggle index in cell H2. Standard arithmetic for P&L lines references the Live Assumptions block.
- **Visual Design**: Hard-coded inputs are styled blue (`#0000FF`) to indicate they are editable (a standard financial modeling convention). Formulas remain default black. The toggle cell is highlighted with a yellow fill.
- **Charts/Tables**: Standard spreadsheet ranges utilizing Number and Decimal formats to separate units from currency.
- **Theme Hooks**: Uses the standard financial formatting convention (blue for hard-coded inputs) alongside basic fills for headers.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

def render_sheet(wb, sheet_name: str, *, title: str = "Dynamic Scenario Model", theme: str = "corporate_blue", **kwargs) -> None:
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    # Standard Financial Modeling Styles
    bold_font = Font(bold=True)
    input_font = Font(color="0000FF")  # Blue indicates hard-coded inputs
    header_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    toggle_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    
    # 1. Setup Headers & Layout
    ws['A1'] = title
    ws['A1'].font = Font(bold=True, size=14)
    
    years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    for col_idx, year in enumerate(years, start=2):
        cell = ws.cell(row=2, column=col_idx, value=year)
        cell.font = bold_font
        cell.alignment = Alignment(horizontal="center")
        cell.fill = header_fill
        
    # Scenario Toggle Setup
    ws['G2'] = "Scenario:"
    ws['G2'].font = bold_font
    ws['G2'].alignment = Alignment(horizontal="right")
    
    ws['H2'] = 1
    ws['H2'].fill = toggle_fill
    ws['H2'].alignment = Alignment(horizontal="center")
    ws['H2'].font = input_font
    
    # Add Data Validation (Dropdown for 1 or 2)
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws['H2'])
    
    # 2. Income Statement (Calculation Engine)
    ws['A3'] = "Income Statement"
    ws['A3'].font = bold_font
    
    ws['A4'] = "Revenue"
    ws['A5'] = "Cost of Goods Sold"
    ws['A6'] = "Gross Profit"
    ws['A6'].font = bold_font
    
    for col in range(2, 7):
        col_letter = ws.cell(row=4, column=col).column_letter
        
        # Revenue = Orders * AOV
        ws.cell(row=4, column=col).value = f"={col_letter}10*{col_letter}11"
        # COGS = Orders * $6.50 manufacturing cost
        ws.cell(row=5, column=col).value = f"={col_letter}10*6.50"
        # Gross Profit = Revenue - COGS
        ws.cell(row=6, column=col).value = f"={col_letter}4-{col_letter}5"
        ws.cell(row=6, column=col).font = bold_font
        
        for r in [4, 5, 6]:
            ws.cell(row=r, column=col).number_format = '"$"#,##0'
            
    # 3. Live Case Assumptions (Dynamic Pull)
    ws['A9'] = "Live Case Assumptions"
    ws['A9'].font = bold_font
    ws['A10'] = "Number of Orders"
    ws['A11'] = "Average Order Value"
    
    for col in range(2, 7):
        col_letter = ws.cell(row=10, column=col).column_letter
        
        # CHOOSE formula dynamically selects between row 15 (Scenario 1) and row 20 (Scenario 2)
        ws.cell(row=10, column=col).value = f"=CHOOSE($H$2, {col_letter}15, {col_letter}20)"
        ws.cell(row=11, column=col).value = f"=CHOOSE($H$2, {col_letter}16, {col_letter}21)"
        
        ws.cell(row=10, column=col).number_format = "#,##0"
        ws.cell(row=11, column=col).number_format = '"$"#,##0.00'

    # 4. Scenario 1 (Upper Case - Hardcoded inputs)
    ws['A14'] = "Scenario 1: Upper Case"
    ws['A14'].font = bold_font
    ws['A15'] = "Number of Orders"
    ws['A16'] = "Average Order Value"
    
    s1_orders = [3000, 6000, 10500, 15750, 21263]
    s1_aov = [39.95, 39.95, 39.95, 39.95, 39.95]
    
    for i, (orders, aov) in enumerate(zip(s1_orders, s1_aov)):
        c1 = ws.cell(row=15, column=i+2, value=orders)
        c2 = ws.cell(row=16, column=i+2, value=aov)
        c1.font = input_font
        c2.font = input_font
        c1.number_format = "#,##0"
        c2.number_format = '"$"#,##0.00'
        
    # 5. Scenario 2 (Lower Case - Hardcoded inputs)
    ws['A19'] = "Scenario 2: Lower Case"
    ws['A19'].font = bold_font
    ws['A20'] = "Number of Orders"
    ws['A21'] = "Average Order Value"
    
    s2_orders = [2000, 4000, 7000, 10500, 14175]
    s2_aov = [34.95, 34.95, 34.95, 34.95, 34.95]
    
    for i, (orders, aov) in enumerate(zip(s2_orders, s2_aov)):
        c1 = ws.cell(row=20, column=i+2, value=orders)
        c2 = ws.cell(row=21, column=i+2, value=aov)
        c1.font = input_font
        c2.font = input_font
        c1.number_format = "#,##0"
        c2.number_format = '"$"#,##0.00'
        
    # 6. Final Polish
    ws.column_dimensions['A'].width = 25
    for col in ["B", "C", "D", "E", "F", "G", "H"]:
        ws.column_dimensions[col].width = 13
```