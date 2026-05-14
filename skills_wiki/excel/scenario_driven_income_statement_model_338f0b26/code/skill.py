from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Dynamic Model", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Theme configuration
    theme_colors = {
        "corporate_blue": "1F4E78",
        "emerald_green": "27AE60",
        "midnight_purple": "5B2C6F",
        "slate_gray": "47525E"
    }
    primary_color = theme_colors.get(theme, "1F4E78")
    
    header_fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")
    section_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    yellow_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    header_font = Font(color="FFFFFF", bold=True)
    bold_font = Font(bold=True)
    blue_font = Font(color="0054A6") # Modeling convention for hardcoded inputs
    
    thin_top = Border(top=Side(style='thin'))
    double_bottom = Border(bottom=Side(style='double'), top=Side(style='thin'))
    
    # 1. Setup Scenario Toggle
    ws['I2'] = "Scenario"
    ws['I2'].font = bold_font
    ws['I2'].alignment = Alignment(horizontal="right")
    ws['J2'] = 1
    ws['J2'].fill = yellow_fill
    ws['J2'].alignment = Alignment(horizontal="center")
    ws['J2'].border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    
    # Data Validation Dropdown for Scenario
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws['J2'])
    
    # 2. Setup Headers
    headers = ["Figures in USD", "Unit", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    ws.append([]) # Row 1 blank for spacing
    ws.append(headers) # Row 2
    for col_idx, cell in enumerate(ws[2], start=1):
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx > 1 else "left")
        
    # 3. Income Statement Layout
    labels_is = [
        ("Revenue", "$"),
        ("Cost of Goods Sold", "$"),
        ("Gross Profit", "$"),
        ("Operating Expenses", "$"),
        ("Operating Profit", "$"),
        ("Corporate Tax", "$"),
        ("Net Income", "$")
    ]
    for r_idx, (item, unit) in enumerate(labels_is, start=3):
        ws.cell(row=r_idx, column=1, value=item)
        ws.cell(row=r_idx, column=2, value=unit).alignment = Alignment(horizontal="center")
        
    for r in [5, 7, 9]:
        ws.cell(row=r, column=1).font = bold_font

    # 4. Assumptions Layout
    sections = [
        (11, "LIVE CASE ASSUMPTIONS"),
        (19, "CASE 1 (BASE / UPPER)"),
        (27, "CASE 2 (DOWNSIDE)")
    ]
    
    assump_labels = [
        ("Orders", "#"),
        ("Order Growth Rate", "%"),
        ("Average Order Value", "$"),
        ("COGS per order", "$"),
        ("Fixed OpEx", "$"),
        ("Tax Rate", "%")
    ]
    
    for r_start, sec_title in sections:
        ws.cell(row=r_start, column=1, value=sec_title).font = bold_font
        ws.cell(row=r_start, column=1).fill = section_fill
        for i, (item, unit) in enumerate(assump_labels):
            ws.cell(row=r_start + 1 + i, column=1, value=item)
            ws.cell(row=r_start + 1 + i, column=2, value=unit).alignment = Alignment(horizontal="center")

    # 5. Populate Hardcoded Assumptions (Case 1)
    ws.cell(row=20, column=3, value=3000).font = blue_font
    for c, val in enumerate([1.0, 0.75, 0.50, 0.35], start=4):
        ws.cell(row=21, column=c, value=val).font = blue_font
        ws.cell(row=21, column=c).number_format = "0%"
    for c in range(3, 8):
        ws.cell(row=22, column=c, value=39.95).font = blue_font
        ws.cell(row=23, column=c, value=8.75).font = blue_font
        ws.cell(row=24, column=c, value=50000).font = blue_font
        ws.cell(row=25, column=c, value=0.20).font = blue_font
        ws.cell(row=25, column=c).number_format = "0%"
        
    # 6. Populate Hardcoded Assumptions (Case 2)
    ws.cell(row=28, column=3, value=2000).font = blue_font
    for c, val in enumerate([0.50, 0.30, 0.20, 0.10], start=4):
        ws.cell(row=29, column=c, value=val).font = blue_font
        ws.cell(row=29, column=c).number_format = "0%"
    for c in range(3, 8):
        ws.cell(row=30, column=c, value=34.95).font = blue_font
        ws.cell(row=31, column=c, value=9.50).font = blue_font
        ws.cell(row=32, column=c, value=50000).font = blue_font
        ws.cell(row=33, column=c, value=0.25).font = blue_font
        ws.cell(row=33, column=c).number_format = "0%"

    # 7. Live Case Routing & Projection Formulas
    for c in range(3, 8):
        col_let = get_column_letter(c)
        
        # Orders: Y1 uses CHOOSE, Y2+ scales from Y-1
        if c == 3:
            ws.cell(row=12, column=c, value=f"=CHOOSE($J$2, {col_let}20, {col_let}28)")
        else:
            prev_col = get_column_letter(c-1)
            ws.cell(row=12, column=c, value=f"={prev_col}12*(1+{col_let}13)")
            
        # Growth Rate Routing
        if c > 3:
            ws.cell(row=13, column=c, value=f"=CHOOSE($J$2, {col_let}21, {col_let}29)")
            ws.cell(row=13, column=c).number_format = "0%"
            
        # Pricing, Cost, and Macro Routing
        ws.cell(row=14, column=c, value=f"=CHOOSE($J$2, {col_let}22, {col_let}30)")
        ws.cell(row=15, column=c, value=f"=CHOOSE($J$2, {col_let}23, {col_let}31)")
        ws.cell(row=16, column=c, value=f"=CHOOSE($J$2, {col_let}24, {col_let}32)")
        ws.cell(row=17, column=c, value=f"=CHOOSE($J$2, {col_let}25, {col_let}33)")
        ws.cell(row=17, column=c).number_format = "0%"

    # 8. Income Statement Calculation Engine
    for c in range(3, 8):
        col_let = get_column_letter(c)
        ws.cell(row=3, column=c, value=f"={col_let}12*{col_let}14")
        ws.cell(row=4, column=c, value=f"={col_let}12*{col_let}15")
        ws.cell(row=5, column=c, value=f"={col_let}3-{col_let}4")
        ws.cell(row=6, column=c, value=f"={col_let}16")
        ws.cell(row=7, column=c, value=f"={col_let}5-{col_let}6")
        ws.cell(row=8, column=c, value=f'=IF({col_let}7<0, "NA", {col_let}7*{col_let}17)')
        ws.cell(row=9, column=c, value=f'=IFERROR({col_let}7-{col_let}8, {col_let}7)')
        
        # Line item formatting & borders
        for r in range(3, 10):
            ws.cell(row=r, column=c).number_format = "#,##0"
            
        ws.cell(row=5, column=c).border = thin_top
        ws.cell(row=7, column=c).border = thin_top
        ws.cell(row=9, column=c).border = double_bottom

    # 9. Clean up column widths & localized number formatting
    ws.column_dimensions['A'].width = 25
    for c in ["B", "C", "D", "E", "F", "G", "I", "J"]:
        ws.column_dimensions[c].width = 13

    for r in [12, 20, 28, 14, 22, 30, 15, 23, 31, 16, 24, 32]:
        for c in range(3, 8):
            cell = ws.cell(row=r, column=c)
            if cell.value:
                if r in [12, 20, 28]:
                    cell.number_format = "#,##0"
                else:
                    cell.number_format = "$#,##0.00" if r not in [16, 24, 32] else "$#,##0"
