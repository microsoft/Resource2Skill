### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario-Driven Income Statement

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a financial model where a central "Live Case" block dynamically pulls data from multiple hardcoded scenario blocks (Upper/Lower case) using the `CHOOSE` function, driven by a Data Validation dropdown toggle. The Income Statement formulas then consume only the Live Case, ensuring a clean and switchable P&L.
* **Applicability**: Essential for any financial modeling, forecasting, or budgeting workbook where decision-makers need to toggle between different sets of assumptions (e.g., Base, Best, Worst cases) and immediately see the impact on downstream calculations.

### 2. Structural Breakdown

- **Data Layout**: 
  - **Rows 4-16**: The Income Statement (Revenue down to Net Profit).
  - **Rows 19-26**: "Live Case" Assumptions (dynamically populated).
  - **Rows 29+**: Hardcoded scenario blocks (Upper Case, Lower Case).
  - **Cell H1**: The Scenario Toggle control cell.
- **Formula Logic**: 
  - `CHOOSE($H$1, C30, C40)` drives the Live Case rows.
  - `={col}20*{col}21` style structured references dynamically scale the P&L across columns without complex absolute anchoring.
- **Visual Design**: Uses financial modeling standard conventions — blue font (`0000FF`) for hardcoded inputs and black font (`000000`) for calculations. Section headers are bolded with standard theme fills.
- **Charts/Tables**: Scenario toggle uses Data Validation (List: "1,2") combined with a bright input-fill (yellow) and outline border to indicate interactivity.
- **Theme Hooks**: Consumes `header_bg`, `header_fg`, and `sub_bg` for block demarcation.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Income Statement", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Theme handling fallback
    theme_colors = {
        "header_bg": "1F4E78",
        "header_fg": "FFFFFF",
        "sub_bg": "D9E1F2",
        "input_bg": "FFF2CC",
        "input_fg": "0000FF",
        "calc_fg": "000000"
    }
    
    header_fill = PatternFill(start_color=theme_colors["header_bg"], end_color=theme_colors["header_bg"], fill_type="solid")
    header_font = Font(color=theme_colors["header_fg"], bold=True)
    bold_font = Font(bold=True)
    sub_fill = PatternFill(start_color=theme_colors["sub_bg"], end_color=theme_colors["sub_bg"], fill_type="solid")
    
    # 1. Setup Header & Scenario Toggle
    ws["A1"] = title
    ws["A1"].font = Font(size=14, bold=True)
    
    ws["G1"] = "Scenario:"
    ws["G1"].font = bold_font
    ws["G1"].alignment = Alignment(horizontal="right")
    
    ws["H1"] = 1
    ws["H1"].fill = PatternFill(start_color=theme_colors["input_bg"], end_color=theme_colors["input_bg"], fill_type="solid")
    ws["H1"].border = Border(outline=Side(style="thin", color="000000"))
    ws["H1"].alignment = Alignment(horizontal="center")
    
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws["H1"])
    
    headers = ["Figures in USD", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        
    # 2. Income Statement P&L Block
    # {c} placeholder makes it robust to string replacement for column letters
    is_structure = [
        ("Revenue", "={c}20*{c}21"),
        ("Cost of Goods Sold", None),
        ("  Manufacturing", "={c}20*{c}22"),
        ("  Order Fulfillment", "={c}20*{c}23"),
        ("Total COGS", "=SUM({c}6:{c}7)", True),
        ("Gross Profit", "={c}4-{c}8", True),
        ("Operating Expenses", None),
        ("  Salaries & Payroll", "={c}24"),
        ("  Marketing", "={c}25"),
        ("Total Operating Expenses", "=SUM({c}11:{c}12)", True),
        ("Operating Profit", "={c}9-{c}13", True),
        ("Corporate Tax", "=MAX(0, {c}14*{c}26)"),
        ("Profit / (Loss)", "={c}14-{c}15", True)
    ]
    
    for row_offset, item in enumerate(is_structure):
        row = 4 + row_offset
        label = item[0]
        formula = item[1]
        is_total = item[2] if len(item) > 2 else False
        
        ws.cell(row=row, column=1, value=label)
        if formula:
            for col_offset in range(5):
                col_letter = get_column_letter(3 + col_offset)
                f = formula.format(c=col_letter)
                ws.cell(row=row, column=3+col_offset, value=f)
        
        if is_total:
            ws.cell(row=row, column=1).font = bold_font
            for c in range(1, 8):
                ws.cell(row=row, column=c).border = Border(top=Side(style="thin"), bottom=Side(style="double"))

    # 3. Dynamic Assumptions Block (Live Case)
    assump_labels = [
        "Number of Orders",
        "Average Order Value",
        "Mfg Cost per Order",
        "Fulfillment Cost per Order",
        "Salaries Expense",
        "Marketing Expense",
        "Tax Rate"
    ]
    
    ws.cell(row=19, column=1, value="Live Case (Driven by Scenario)").font = bold_font
    ws.cell(row=19, column=1).fill = sub_fill
    for r_idx, label in enumerate(assump_labels):
        row = 20 + r_idx
        ws.cell(row=row, column=1, value=label)
        for c_idx in range(5):
            col_letter = get_column_letter(3 + c_idx)
            s1_row = 30 + r_idx
            s2_row = 40 + r_idx
            # CHOOSE toggle formula
            formula = f"=CHOOSE($H$1, {col_letter}{s1_row}, {col_letter}{s2_row})"
            cell = ws.cell(row=row, column=3+c_idx, value=formula)
            cell.font = Font(color=theme_colors["calc_fg"])

    # 4. Hardcoded Scenario Blocks
    scenarios = [
        (29, "Scenario 1: Upper Case", [
            [3000, 6000, 10500, 15750, 21263],      # Orders
            [39.95, 39.95, 39.95, 39.95, 39.95],    # AOV
            [6.50, 6.50, 6.50, 6.50, 6.50],         # Mfg Cost
            [2.25, 2.25, 2.25, 2.25, 2.25],         # Fulfillment
            [50000, 50000, 100000, 100000, 100000], # Salaries
            [25000, 25000, 50000, 50000, 100000],   # Marketing
            [0.20, 0.20, 0.20, 0.20, 0.20]          # Tax Rate
        ]),
        (39, "Scenario 2: Lower Case", [
            [2000, 4000, 7000, 10500, 14175],       # Orders
            [34.95, 34.95, 34.95, 34.95, 34.95],    # AOV
            [8.00, 8.00, 8.00, 8.00, 8.00],         # Mfg Cost
            [2.25, 2.25, 2.25, 2.25, 2.25],         # Fulfillment
            [50000, 50000, 100000, 100000, 100000], # Salaries
            [25000, 25000, 50000, 50000, 100000],   # Marketing
            [0.25, 0.25, 0.25, 0.25, 0.25]          # Tax Rate
        ])
    ]

    for start_row, header_text, dataset in scenarios:
        ws.cell(row=start_row, column=1, value=header_text).font = bold_font
        ws.cell(row=start_row, column=1).fill = sub_fill
        
        for r_idx, (label, data_row) in enumerate(zip(assump_labels, dataset)):
            row = start_row + 1 + r_idx
            ws.cell(row=row, column=1, value=label)
            for c_idx, val in enumerate(data_row):
                cell = ws.cell(row=row, column=3+c_idx, value=val)
                # Hardcoded values conventionally styled in blue
                cell.font = Font(color=theme_colors["input_fg"])

    # 5. Formatting & Cleanup
    ws.column_dimensions["A"].width = 30
    for col in ["C", "D", "E", "F", "G"]:
        ws.column_dimensions[col].width = 13
        
    for row in range(4, 17):
        for col in range(3, 8):
            ws.cell(row=row, column=col).number_format = '#,##0'
            
    for row in range(20, 47):
        if row in [26, 36, 46]:  # Tax Rates
            format_str = '0%'
        elif row in [21, 22, 23, 31, 32, 33, 41, 42, 43]:  # Per-unit metrics
            format_str = '#,##0.00'
        else:  # Broad nominal values & Orders
            format_str = '#,##0'
            
        for col in range(3, 8):
            ws.cell(row=row, column=col).number_format = format_str
```