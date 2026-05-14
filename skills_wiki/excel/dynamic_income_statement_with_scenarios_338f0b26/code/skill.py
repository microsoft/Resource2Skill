from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

def render_sheet(wb, sheet_name: str, *, title: str = "Dynamic Financial Model", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    try:
        from skills_library.excel.components._helpers import get_theme_colors
        colors = get_theme_colors(theme)
    except ImportError:
        colors = {"primary": "2C3E50", "secondary": "18BC9C", "bg": "ECF0F1", "text": "2C3E50", "accent": "E74C3C"}

    header_fill = PatternFill("solid", fgColor=colors.get("primary", "2C3E50"))
    live_fill = PatternFill("solid", fgColor=colors.get("secondary", "18BC9C"))
    header_font = Font(color="FFFFFF", bold=True)
    bold_font = Font(bold=True)
    blue_font = Font(color="0000FF") # Standard financial convention for inputs

    # --- Setup Layout ---
    ws.column_dimensions['A'].width = 28
    for c in "BCDEFGH":
        ws.column_dimensions[c].width = 13

    # Title & Scenario Dropdown
    ws["A1"] = title
    ws["A1"].font = Font(size=14, bold=True, color=colors.get("primary", "2C3E50"))
    
    ws["I2"] = "Scenario:"
    ws["I2"].font = bold_font
    ws["J2"] = 1
    ws["J2"].fill = PatternFill("solid", fgColor="FFF2CC")
    ws["J2"].border = Border(outline=Side(style="thin", color="000000"))

    dv = DataValidation(type="list", formula1='"1,2,3"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws["J2"])

    # Headers
    ws.append([])
    ws.append([])
    ws.append(["Figures in USD", "Unit", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]) # Row 4
    for cell in ws[4]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        
    ws.freeze_panes = "D5"

    # --- Income Statement Engine ---
    ws.append(["Income Statement"]) # Row 5
    ws["A5"].font = bold_font

    def add_row(label, unit, formulas, bold=False):
        row_data = [label, unit] + formulas
        ws.append(row_data)
        current_row = ws.max_row
        if bold:
            ws[f"A{current_row}"].font = bold_font
            for col in "DEFGH":
                ws[f"{col}{current_row}"].font = bold_font
                ws[f"{col}{current_row}"].border = Border(top=Side(style="thin"), bottom=Side(style="double"))
        return current_row

    # P&L calculation referencing Live Case (Rows 27-37)
    add_row("Revenue", "$", [f"={c}27*{c}29" for c in "DEFGH"]) # Row 6
    ws.append(["Cost of Goods Sold"]) # Row 7
    add_row("  Manufacturing", "$", [f"={c}27*{c}31" for c in "DEFGH"]) # Row 8
    add_row("  Order Fulfillment", "$", [f"={c}27*{c}32" for c in "DEFGH"]) # Row 9
    add_row("Total COGS", "$", [f"=SUM({c}8:{c}9)" for c in "DEFGH"], bold=True) # Row 10
    ws.append([]) # Row 11
    add_row("Gross Profit", "$", [f"={c}6-{c}10" for c in "DEFGH"], bold=True) # Row 12
    add_row("Gross Profit Margin", "%", [f"={c}12/{c}6" for c in "DEFGH"]) # Row 13
    ws.append(["Operating Expenses"]) # Row 14
    add_row("  Warehouse Rent", "$", [f"={c}34" for c in "DEFGH"]) # Row 15
    add_row("  Salaries & Payroll", "$", [f"={c}35" for c in "DEFGH"]) # Row 16
    add_row("  Marketing", "$", [f"={c}36" for c in "DEFGH"]) # Row 17
    add_row("Total Operating Expenses", "$", [f"=SUM({c}15:{c}17)" for c in "DEFGH"], bold=True) # Row 18
    ws.append([]) # Row 19
    add_row("Operating Profit", "$", [f"={c}12-{c}18" for c in "DEFGH"], bold=True) # Row 20
    add_row("Operating Profit Margin", "%", [f"={c}20/{c}6" for c in "DEFGH"]) # Row 21
    ws.append([]) # Row 22
    add_row("Corporate Tax", "$", [f"=IF({c}20<0, NA(), {c}20*{c}37)" for c in "DEFGH"]) # Row 23
    add_row("Profit / (Loss)", "$", [f"=IFERROR({c}20-{c}23, {c}20)" for c in "DEFGH"], bold=True) # Row 24

    for r in range(6, 25):
        for c in "DEFGH":
            cell = ws[f"{c}{r}"]
            if r in [13, 21]: cell.number_format = "0%"
            elif r not in [7, 11, 14, 19, 22]: cell.number_format = '#,##0'

    # --- Live Case Assumptions Block ---
    ws.append([]) # Row 25
    ws.append(["Assumptions (Live Case)"]) # Row 26
    ws["A26"].font = header_font
    ws["A26"].fill = live_fill

    live_labels = [
        ("Number of Orders", "#"),              # 27
        ("Order Growth Rate", "%"),             # 28
        ("Average Order Value", "$"),           # 29
        ("Cost of Goods Sold (per order)", ""), # 30
        ("  Manufacturing", "$"),               # 31
        ("  Order Fulfillment", "$"),           # 32
        ("Operating Expenses", ""),             # 33
        ("  Warehouse Rent", "$"),              # 34
        ("  Salaries & Payroll", "$"),          # 35
        ("  Marketing", "$"),                   # 36
        ("Corporate Tax Rate", "%")             # 37
    ]

    for idx, (lbl, unit) in enumerate(live_labels):
        row_num = 27 + idx
        row_data = [lbl, unit]
        for c_idx, col in enumerate("DEFGH"):
            if row_num in [30, 33]: # Section Headers
                row_data.append("")
            elif row_num == 28 and col == 'D': # No Yr 1 Growth Rate
                row_data.append("")
            else:
                # Dynamically choose between the 3 Scenario blocks stacked below
                s1_r, s2_r, s3_r = row_num + 13, row_num + 26, row_num + 39
                row_data.append(f"=CHOOSE($J$2, {col}{s1_r}, {col}{s2_r}, {col}{s3_r})")
        ws.append(row_data)

    for r in range(27, 38):
        if r in [30, 33]: continue
        for c in "DEFGH":
            cell = ws[f"{c}{r}"]
            if r in [28, 37]: cell.number_format = "0%"
            elif r == 27: cell.number_format = "#,##0"
            else: cell.number_format = "#,##0.00"

    # --- Hardcoded Scenario Data Blocks ---
    scenarios = [
        {
            "title": "Scenario 1 (Base Case)",
            "orders_y1": 3000, "growth": [1.0, 0.75, 0.50, 0.35],
            "aov": [39.95]*5, "mfg": [6.50]*5, "fulfill": [2.25]*5,
            "rent": [20000, 20000, 30000, 30000, 30000],
            "salaries": [50000, 50000, 100000, 100000, 100000],
            "marketing": [25000, 50000, 50000, 100000, 100000],
            "tax": [0.20]*5
        },
        {
            "title": "Scenario 2 (Upper Case)",
            "orders_y1": 3000, "growth": [1.5, 1.0, 0.75, 0.50],
            "aov": [39.95]*5, "mfg": [6.00]*5, "fulfill": [2.00]*5,
            "rent": [20000, 20000, 30000, 30000, 30000],
            "salaries": [50000, 50000, 80000, 80000, 80000],
            "marketing": [25000, 25000, 50000, 50000, 50000],
            "tax": [0.20]*5
        },
        {
            "title": "Scenario 3 (Lower Case)",
            "orders_y1": 2000, "growth": [0.5, 0.25, 0.10, 0.05],
            "aov": [34.95]*5, "mfg": [8.00]*5, "fulfill": [2.50]*5,
            "rent": [20000]*5, "salaries": [50000]*5, "marketing": [25000]*5,
            "tax": [0.25]*5
        }
    ]

    sr = 39 # Scenario 1 starts exactly +13 rows from Live Case (Row 26)
    for s in scenarios:
        ws.append([]) # Spacer
        ws.append([s["title"]])
        ws[f"A{sr}"].font = bold_font
        
        for idx, (lbl, unit) in enumerate(live_labels):
            row_num = sr + 1 + idx
            row_data = [lbl, unit]
            for c_idx, col in enumerate("DEFGH"):
                if row_num in [sr+4, sr+7]: # Section headers
                    row_data.append("")
                    continue
                
                # Distribute Hardcoded Values vs Forecasting Formulas
                val = ""
                if row_num == sr+1: # Orders
                    if col == 'D': val = s["orders_y1"]
                    else: val = f"={'DEFGH'[c_idx-1]}{row_num}*(1+{col}{row_num+1})"
                elif row_num == sr+2: # Growth Rates
                    if col == 'D': val = ""
                    else: val = s["growth"][c_idx-1]
                elif row_num == sr+3: val = s["aov"][c_idx]
                elif row_num == sr+5: val = s["mfg"][c_idx]
                elif row_num == sr+6: val = s["fulfill"][c_idx]
                elif row_num == sr+8: val = s["rent"][c_idx]
                elif row_num == sr+9: val = s["salaries"][c_idx]
                elif row_num == sr+10: val = s["marketing"][c_idx]
                elif row_num == sr+11: val = s["tax"][c_idx]
                
                row_data.append(val)
            ws.append(row_data)
            
            # Format explicitly typed inputs in financial blue
            for c_idx, col in enumerate("DEFGH"):
                cell = ws[f"{col}{row_num}"]
                if type(cell.value) in [int, float]:
                    cell.font = blue_font
                
                if row_num in [sr+2, sr+11]: cell.number_format = "0%"
                elif row_num == sr+1: cell.number_format = "#,##0"
                elif type(cell.value) in [int, float] or str(cell.value).startswith("="): 
                    cell.number_format = "#,##0.00"
                
        sr += 13 # Fixed offset for the next scenario block
