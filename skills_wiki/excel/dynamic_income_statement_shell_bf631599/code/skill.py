from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Income Statement", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a fully dynamic Income Statement shell with historicals, forecasts, 
    and a working scenario analysis toggle.
    """
    if sheet_name not in wb.sheetnames:
        ws = wb.create_sheet(sheet_name)
    else:
        ws = wb[sheet_name]

    # Theme palette fallback
    palettes = {
        "corporate_blue": {"header_bg": "002060", "header_fg": "FFFFFF", "hardcode_fg": "0000FF", "subtotal_bg": "F2F2F2"},
        "emerald_green": {"header_bg": "004D40", "header_fg": "FFFFFF", "hardcode_fg": "0000FF", "subtotal_bg": "E8F5E9"}
    }
    theme_colors = palettes.get(theme, palettes["corporate_blue"])

    # Define Styles
    header_fill = PatternFill(start_color=theme_colors["header_bg"], end_color=theme_colors["header_bg"], fill_type="solid")
    header_font = Font(color=theme_colors["header_fg"], bold=True)
    bold_font = Font(bold=True)
    hardcode_font = Font(color=theme_colors["hardcode_fg"])
    subtotal_border = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    
    # 1. Setup Scenario Toggle
    ws['A2'] = "Live Scenario (1=Best, 2=Base, 3=Worst):"
    ws['A2'].font = bold_font
    ws['B2'] = 2 # Default to Base Case
    ws['B2'].font = hardcode_font
    ws['B2'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    ws['B2'].border = Border(outline=True, top=Side(style='thin'), bottom=Side(style='thin'), left=Side(style='thin'), right=Side(style='thin'))
    ws['B2'].alignment = Alignment(horizontal="center")
    
    # Add Data Validation for Scenario Toggle
    dv = DataValidation(type="list", formula1='"1,2,3"', allow_blank=False)
    dv.error = 'Your entry is not in the list'
    dv.errorTitle = 'Invalid Scenario'
    dv.prompt = 'Please select 1, 2, or 3'
    dv.promptTitle = 'Scenario Selection'
    ws.add_data_validation(dv)
    dv.add(ws['B2'])

    # 2. Setup Time Series Headers (Row 4)
    ws['B4'] = title
    ws['B4'].font = header_font
    ws['B4'].fill = header_fill
    
    years = [2023, 2024, 2025, 2026, 2027]
    for i, year in enumerate(years):
        col = i + 3 # Starting at column C
        cell = ws.cell(row=4, column=col, value=year)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")
        
        # Apply custom format: "A" for Historical (first 3), "E" for Forecast (last 2)
        if i < 3:
            cell.number_format = '0"A"'
        else:
            cell.number_format = '0"E"'

    # 3. Setup Income Statement Line Items
    line_items = [
        ("Revenue", 5),
        ("COGS", 6),
        ("Gross Profit", 7),
        ("SG&A", 8),
        ("Operating Income", 9),
        ("Taxes", 10),
        ("Net Income", 11)
    ]
    
    for item, row in line_items:
        ws.cell(row=row, column=2, value=item)
        if item in ["Gross Profit", "Operating Income", "Net Income"]:
            ws.cell(row=row, column=2).font = bold_font

    # Inject Historical Hardcodes (Cols C, D, E -> 2023A, 2024A, 2025A)
    historicals = {
        5: [5210, 5435, 5710], # Revenue
        6: [3345, 3350, 3551], # COGS
        8: [850, 870, 900],    # SG&A
        10: [228, 186, 147]    # Taxes
    }
    
    for row, vals in historicals.items():
        for i, val in enumerate(vals):
            cell = ws.cell(row=row, column=i+3, value=val)
            cell.font = hardcode_font # Blue font for hardcodes
            cell.number_format = '#,##0'

    # Inject Subtotal Formulas for Historicals & Forecasts
    for col_idx in range(3, 8): # C to G
        col_let = get_column_letter(col_idx)
        
        gp_cell = ws[f'{col_let}7']
        gp_cell.value = f'={col_let}5-{col_let}6'
        gp_cell.font = bold_font
        gp_cell.border = subtotal_border
        gp_cell.number_format = '#,##0'
        
        op_cell = ws[f'{col_let}9']
        op_cell.value = f'={col_let}7-{col_let}8'
        op_cell.font = bold_font
        op_cell.border = subtotal_border
        op_cell.number_format = '#,##0'
        
        ni_cell = ws[f'{col_let}11']
        ni_cell.value = f'={col_let}9-{col_let}10'
        ni_cell.font = bold_font
        ni_cell.border = subtotal_border
        ni_cell.number_format = '#,##0'

    # 4. Setup Assumptions Section
    ws['B14'] = "Income Statement Assumptions"
    ws['B14'].font = header_font
    ws['B14'].fill = header_fill
    
    assumptions = [
        ("Revenue Growth Rate", 15),
        ("COGS % of Revenue", 16),
        ("SG&A % of Revenue", 17),
        ("Effective Tax Rate", 18)
    ]
    
    for item, row in assumptions:
        ws.cell(row=row, column=2, value=item)

    # Active Assumption Formulas (Forecast Cols F, G)
    # Revenue Growth uses CHOOSE to pull from Scenario table
    ws['F15'] = '=CHOOSE($B$2, F23, F24, F25)'
    ws['G15'] = '=CHOOSE($B$2, G23, G24, G25)'
    
    # Flat assumptions for margins/taxes (linking to historical averages for simplicity in this shell)
    ws['F16'] = '=AVERAGE(C6:E6)/AVERAGE(C5:E5)'
    ws['G16'] = '=F16'
    ws['F17'] = '=AVERAGE(C8:E8)/AVERAGE(C5:E5)'
    ws['G17'] = '=F17'
    ws['F18'] = 0.25
    ws['F18'].font = hardcode_font
    ws['G18'] = '=F18'

    for row in range(15, 19):
        for col in [6, 7]:
            ws.cell(row=row, column=col).number_format = '0.0%'

    # 5. Inject Forecast Formulas into Income Statement (Cols F, G -> 2026E, 2027E)
    for i, col_let in enumerate(['F', 'G']):
        prev_col = 'E' if i == 0 else 'F'
        
        # Revenue = Prev Rev * (1 + Growth)
        ws[f'{col_let}5'] = f'={prev_col}5*(1+{col_let}15)'
        ws[f'{col_let}5'].number_format = '#,##0'
        
        # COGS = Rev * COGS Margin
        ws[f'{col_let}6'] = f'={col_let}5*{col_let}16'
        ws[f'{col_let}6'].number_format = '#,##0'
        
        # SG&A = Rev * SGA Margin
        ws[f'{col_let}8'] = f'={col_let}5*{col_let}17'
        ws[f'{col_let}8'].number_format = '#,##0'
        
        # Taxes = OpInc * Tax Rate
        ws[f'{col_let}10'] = f'={col_let}9*{col_let}18'
        ws[f'{col_let}10'].number_format = '#,##0'

    # 6. Setup Revenue Scenarios Matrix
    ws['B21'] = "Revenue Scenarios"
    ws['B21'].font = header_font
    ws['B21'].fill = header_fill
    
    scenarios = [
        ("1 - Best Case", 23, 0.067),
        ("2 - Base Case", 24, 0.047),
        ("3 - Worst Case", 25, 0.027)
    ]
    
    for item, row, rate in scenarios:
        ws.cell(row=row, column=2, value=item)
        # 2026E Hardcodes
        ws.cell(row=row, column=6, value=rate).font = hardcode_font
        ws.cell(row=row, column=6).number_format = '0.0%'
        # 2027E Hardcodes
        ws.cell(row=row, column=7, value=rate).font = hardcode_font
        ws.cell(row=row, column=7).number_format = '0.0%'

    # Formatting Cleanup
    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 30
    for col in ['C', 'D', 'E', 'F', 'G']:
        ws.column_dimensions[col].width = 12

    # Freeze Panes for easy scrolling
    ws.freeze_panes = 'C5'
