### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Financial Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a financial projection where downstream calculations (like an Income Statement) are driven by a central "Live Case" assumptions block. The Live Case uses the `CHOOSE` function to dynamically pull values from multiple pre-defined hardcoded scenarios (Base, Upper, Lower) based on a Data Validation dropdown toggle. 
* **Applicability**: Essential for any FP&A or financial modeling task where users need to instantly switch between different assumption sets (e.g., Optimistic vs. Pessimistic) to immediately see the impact on revenue and profit metrics without overwriting data.

### 2. Structural Breakdown

- **Data Layout**: 
  - A Scenario Toggle control cell situated at the top right.
  - A summary calculation section (Income Statement) mapping columns to years (Year 1 to 5).
  - A "Live Case" assumptions block that drives the calculations.
  - Distinct blocks for each hardcoded scenario (Base, Upper, Lower), spaced evenly below the Live Case.
- **Formula Logic**: 
  - `=CHOOSE($H$2, C16, C21, C26)`: Dynamically routes the cell reference to the active scenario based on the index value (1, 2, or 3) selected in the toggle cell.
- **Visual Design**: 
  - The toggle cell uses a yellow fill (`FFF2CC`) to signal it is a control input.
  - Hardcoded assumption values use a blue font (`0000FF`), adhering to the universal financial modeling convention that differentiates raw inputs from black formula text.
- **Charts/Tables**: N/A (Standard modeled grid layout).
- **Theme Hooks**: Employs standard primary header backgrounds, utilizing conventions for financial inputs over strict theme overrides.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Scenario Model", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Standard Financial Modeling Color Tokens
    header_bg = "1F4E78"   # Dark blue
    header_fg = "FFFFFF"   # White
    input_bg = "FFF2CC"    # Light yellow for the control toggle
    hardcode_fg = "0000FF" # Blue font indicating hardcoded input
    
    f_header = Font(color=header_fg, bold=True)
    f_bold = Font(bold=True)
    f_input = Font(color=hardcode_fg)
    fill_header = PatternFill("solid", fgColor=header_bg)
    fill_toggle = PatternFill("solid", fgColor=input_bg)
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'), 
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # 1. Setup Column Widths
    ws.column_dimensions['B'].width = 25
    for c in range(3, 9):
        ws.column_dimensions[get_column_letter(c)].width = 15

    # 2. Scenario Toggle Mechanism
    ws["G2"] = "Active Scenario:"
    ws["G2"].font = f_bold
    ws["G2"].alignment = Alignment(horizontal="right")
    
    ws["H2"] = 1
    ws["H2"].fill = fill_toggle
    ws["H2"].border = thin_border
    ws["H2"].alignment = Alignment(horizontal="center")
    
    # Data validation for the toggle (1=Base, 2=Upper, 3=Lower)
    dv = DataValidation(type="list", formula1='"1,2,3"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws["H2"])
    
    ws["I2"] = "<- 1:Base, 2:Upper, 3:Lower"
    ws["I2"].font = Font(italic=True, color="595959")
    
    # 3. Output Section (Simplified Income Statement)
    headers = ["Line Item", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    for col_idx, header in enumerate(headers, start=2):
        cell = ws.cell(row=4, column=col_idx, value=header)
        cell.font = f_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")
        
    ws["B5"] = "Revenue"
    ws["B6"] = "Cost of Goods Sold"
    ws["B7"] = "Gross Profit"
    ws["B7"].font = f_bold
    
    for c in range(3, 8):
        col_let = get_column_letter(c)
        # Revenue = Orders * AOV
        ws.cell(row=5, column=c, value=f"={col_let}11*{col_let}12").number_format = '"$"#,##0'
        # COGS = Orders * Cost per Order
        ws.cell(row=6, column=c, value=f"={col_let}11*{col_let}13").number_format = '"$"#,##0'
        # Gross Profit
        gp = ws.cell(row=7, column=c, value=f"={col_let}5-{col_let}6")
        gp.number_format = '"$"#,##0'
        gp.font = f_bold
        gp.border = Border(top=Side(style='thin'), bottom=Side(style='double'))
        
    # 4. Live Case Assumptions (Driven by CHOOSE formula)
    ws["B10"] = "Live Case Assumptions"
    ws["B10"].font = f_bold
    
    assumptions_labels = ["Orders (#)", "Avg Order Value ($)", "Cost per Order ($)"]
    for r_idx, label in enumerate(assumptions_labels, start=11):
        ws.cell(row=r_idx, column=2, value=label)
        
        for c in range(3, 8):
            col_let = get_column_letter(c)
            # Calculate dynamic offsets to the hardcoded scenarios below
            # Base (+5 rows), Upper (+10 rows), Lower (+15 rows)
            r_base, r_up, r_down = r_idx + 5, r_idx + 10, r_idx + 15
            
            formula = f"=CHOOSE($H$2, {col_let}{r_base}, {col_let}{r_up}, {col_let}{r_down})"
            cell = ws.cell(row=r_idx, column=c, value=formula)
            cell.number_format = '"$"#,##0.00' if "($)" in label else '#,##0'

    # 5. Hardcoded Scenarios Data (Blue Font)
    scenarios = [
        ("Scenario 1: Base Case", 15, [
            [3000, 3600, 4320, 5184, 6220],
            [39.95, 39.95, 39.95, 39.95, 39.95],
            [8.75, 8.50, 8.25, 8.00, 7.75]
        ]),
        ("Scenario 2: Upper Case", 20, [
            [3000, 4500, 6750, 10125, 15187],
            [44.95, 44.95, 44.95, 44.95, 44.95],
            [8.00, 7.50, 7.00, 6.50, 6.00]
        ]),
        ("Scenario 3: Lower Case", 25, [
            [3000, 3150, 3307, 3472, 3646],
            [34.95, 34.95, 34.95, 34.95, 34.95],
            [9.50, 9.75, 10.00, 10.25, 10.50]
        ])
    ]
    
    for title, start_row, data in scenarios:
        ws.cell(row=start_row, column=2, value=title).font = f_bold
        for i, label in enumerate(assumptions_labels):
            ws.cell(row=start_row+1+i, column=2, value=label)
            for j, val in enumerate(data[i]):
                cell = ws.cell(row=start_row+1+i, column=3+j, value=val)
                cell.font = f_input  # Blue font signifies hardcoded assumption
                cell.number_format = '"$"#,##0.00' if "($)" in label else '#,##0'
```