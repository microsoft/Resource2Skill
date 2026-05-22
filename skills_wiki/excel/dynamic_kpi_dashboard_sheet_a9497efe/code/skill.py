from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

# Assume _helpers.py is available or copy relevant functions
from skills_library.excel._helpers import (
    load_theme_colors,
    apply_fill,
    apply_font,
    apply_border,
)

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a dynamic KPI dashboard sheet pulling data from 'Data' and 'Staging' sheets.

    Args:
        wb: The openpyxl workbook object.
        sheet_name: The name of the sheet to create for the dashboard.
        title: The main title for the dashboard.
        theme: The name of the theme to use for colors (e.g., "corporate_blue").
        **kwargs: Additional keyword arguments (not used in this skill but for compatibility).
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    ws.title = sheet_name

    theme_colors = load_theme_colors(theme)

    # --- Create Dummy Data and Staging Sheets for demonstration ---
    # In a real scenario, these would be populated from external sources or complex calculations.
    if 'Data' not in wb.sheetnames:
        data_ws = wb.create_sheet('Data', 0)
        data_ws.sheet_properties.tabColor = "0066CC" # Blue
        data_ws['A1'] = "Actual"
        data_ws['A2'] = "Category"
        months = ["Jan-20", "Feb-20", "Mar-20", "Apr-20", "May-20", "Jun-20", "Jul-20", "Aug-20", "Sep-20", "Oct-20", "Nov-20", "Dec-20"]
        for i, month in enumerate(months):
            data_ws.cell(row=2, column=i+2, value=month)
            data_ws.cell(row=3, column=i+2, value=f"=DATE(2020,{i+1},31)") # Date for INDEX MATCH

        data_rows = [
            ("Sales", [1_500_000, 1_685_000, 1_685_400, 1_798_524, 2_007_338, 2_338_892, 2_500_000, 2_632_274, 2_818_096, 3_000_000, 3_150_000, 3_200_000]),
            ("COGs", [900_000, 954_000, 1_030_320, 1_102_442, 1_168_589, 1_340_000, 1_453_000, 1_536_000, 1_620_000, 1_710_000, 1_790_000, 1_820_000]),
            ("Gross Profit", [600_000, 731_000, 655_080, 684_082, 725_126, 998_892, 1_047_000, 1_096_274, 1_198_096, 1_290_000, 1_360_000, 1_380_000]),
            ("Account Receivables Balance", [2_800_000, 2_940_000, 3_087_000, 3_241_350, 3_403_418, 3_573_588, 3_752_268, 3_939_881, 4_136_875, 4_343_719, 4_560_905, 4_789_000]),
            ("Credit Sales", [1_500_000, 1_590_000, 1_685_400, 1_786_524, 1_893_715, 2_007_338, 2_127_778, 2_255_445, 2_390_772, 2_534_218, 2_686_271, 2_847_447]),
            ("Accounts Payable Balance", [3_100_000, 3_255_000, 3_417_750, 3_588_638, 3_768_069, 3_956_473, 4_154_296, 4_362_011, 4_580_112, 4_809_118, 5_050_000, 5_300_000]),
            ("COGs (for DPO)", [900_000, 954_000, 1_030_320, 1_102_442, 1_168_589, 1_340_000, 1_453_000, 1_536_000, 1_620_000, 1_710_000, 1_790_000, 1_820_000]),
            ("Past Due Accounts Receivables", [150_000, 140_000, 122_500, 111_500, 105_000, 99_000, 88_000, 77_000, 66_000, 55_000, 44_000, 33_000]),
            ("Total Accounts Receivables", [2_800_000, 2_940_000, 3_087_000, 3_241_350, 3_403_418, 3_573_588, 3_752_268, 3_939_881, 4_136_875, 4_343_719, 4_560_905, 4_789_000]),
            ("Sales & Marketing Costs", [350_000, 369_000, 388_950, 409_450, 430_000, 451_000, 473_000, 496_000, 520_000, 545_000, 570_000, 590_000]),
            ("# of new customers", [40, 48, 50, 52, 55, 60, 65, 70, 75, 80, 85, 90]),
            ("OPEX (Operating Expenses)", [600_500, 630_000, 660_000, 690_000, 720_000, 750_000, 780_000, 810_000, 840_000, 870_000, 900_000, 930_000]),
            ("Full Time Employees", [44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77]),
            ("OPEX Budget", [550_000, 577_500, 606_375, 636_694, 668_529, 701_955, 737_053, 773_906, 812_601, 853_231, 895_893, 940_687]),
            ("Sales Budget", [1_680_000, 1_764_000, 1_852_200, 1_944_810, 2_042_051, 2_144_153, 2_251_361, 2_363_929, 2_482_125, 2_606_231, 2_736_542, 2_873_370])
        ]
        for r_idx, (kpi_name, values) in enumerate(data_rows, start=4):
            data_ws.cell(row=r_idx, column=1, value=kpi_name)
            for c_idx, value in enumerate(values, start=2):
                data_ws.cell(row=r_idx, column=c_idx, value=value)
        
        # Add target values to Data sheet for some KPIs
        data_ws.cell(row=4, column=16, value=45) # DSO Target
        data_ws.cell(row=6, column=16, value=90) # DPO Target
        data_ws.cell(row=8, column=16, value=0.03) # Non-Current AR Target
        data_ws.cell(row=11, column=16, value=15_000) # CAC Target
        data_ws.cell(row=13, column=16, value=0.38) # Gross Margin Target
        data_ws.cell(row=15, column=16, value=12_500) # CPFTE Target

    if 'Staging' not in wb.sheetnames:
        staging_ws = wb.create_sheet('Staging', 1)
        staging_ws.sheet_properties.tabColor = "00CCCC" # Teal
        # Header row for months
        staging_ws.cell(row=3, column=1, value="Category")
        for i in range(2, 14):
            staging_ws.cell(row=3, column=i, value=f"='Data'!{get_column_letter(i)}2")
            staging_ws.cell(row=4, column=i, value=f"='Data'!{get_column_letter(i)}3") # The actual date value

        # KPI Calculations and targets
        kpis_data = [
            # Working Capital Efficiency
            ("Account Receivables Balance", "=Data!C5"),
            ("Credit Sales (for DSO)", "=Data!C6"),
            ("# of days", "=DAY(C4)"), # Example: =DAY(date_cell)
            ("DSO (Days Sales Outstanding)", "=IFERROR((C5/C6)*C7,0)"),
            ("DSO Target", "=Data!P4"), # Linking to Data sheet for targets
            ("Accounts Payable Balance", "=Data!C7"),
            ("COGs (for DPO)", "=Data!C8"),
            ("DPO (Days Payables Outstanding)", "=IFERROR((C9/C10)*C7,0)"),
            ("DPO Target", "=Data!P6"),
            ("Past Due Accounts Receivables", "=Data!C9"),
            ("Total Accounts Receivables", "=Data!C10"),
            ("Non-Current AR %", "=IFERROR(C11/C12,0)"),
            ("Non-Current AR Target", "=Data!P8"),
            # Sales KPIs
            ("Sales & Marketing Costs", "=Data!C11"),
            ("# of new customers", "=Data!C12"),
            ("CAC (Customer Acquisition Cost)", "=IFERROR(C15/C16,0)"),
            ("CAC Target", "=Data!P11"),
            ("Sales Actual", "=Data!C4"),
            ("Sales Budget", "=Data!C16"),
            ("Sales vs. Budget%", "=IFERROR(C18/C19,0)"),
            ("Sales vs. Budget Target", "=1"), # 100%
            ("Gross Profit Actual", "=Data!C6"),
            ("Sales for Gross Margin", "=Data!C4"),
            ("Gross Margin", "=IFERROR(C22/C23,0)"),
            ("Gross Margin Target", "=Data!P13"),
            # Cost KPIs
            ("OPEX Actual", "=Data!C13"),
            ("OPEX Budget", "=Data!C15"),
            ("OPEX Actual vs. Budget", "=IFERROR(C26/C27,0)"),
            ("OPEX Target", "=1"), # 100%
            ("Full Time Employees", "=Data!C14"),
            ("CPFTE (Cost Per Full Time Employee)", "=IFERROR(C26/C29,0)"),
            ("CPFTE Target", "=Data!P15")
        ]

        row_offset = 5
        for kpi_row_name, formula in kpis_data:
            staging_ws.cell(row=row_offset, column=1, value=kpi_row_name)
            # Copy formula across all months
            for c_idx in range(2, 14): # From Jan-20 to Dec-20
                if isinstance(formula, str) and formula.startswith('='):
                    # Replace 'C' with dynamic column letter if it's a formula referring to the current month's column
                    current_col_letter = get_column_letter(c_idx)
                    # Adjust column references for formulas like IFERROR((C5/C6)*C7,0) where C refers to current month data
                    # This simplified replacement works for simple relative references like C5 -> D5, E5, etc.
                    dynamic_formula = formula.replace("C5", f"{current_col_letter}5").replace("C6", f"{current_col_letter}6").replace("C7", f"{current_col_letter}7").replace("C8", f"{current_col_letter}8").replace("C9", f"{current_col_letter}9").replace("C10", f"{current_col_letter}10").replace("C11", f"{current_col_letter}11").replace("C12", f"{current_col_letter}12").replace("C13", f"{current_col_letter}13").replace("C14", f"{current_col_letter}14").replace("C15", f"{current_col_letter}15").replace("C16", f"{current_col_letter}16").replace("C18", f"{current_col_letter}18").replace("C19", f"{current_col_letter}19").replace("C22", f"{current_col_letter}22").replace("C23", f"{current_col_letter}23").replace("C26", f"{current_col_letter}26").replace("C27", f"{current_col_letter}27").replace("C29", f"{current_col_letter}29").replace("C4", f"{current_col_letter}4").replace("C1", f"{current_col_letter}1").replace("P4", "$P$4").replace("P6", "$P$6").replace("P8", "$P$8").replace("P11", "$P$11").replace("P13", "$P$13").replace("P15", "$P$15")
                    staging_ws.cell(row=row_offset, column=c_idx, value=dynamic_formula)
                else:
                    staging_ws.cell(row=row_offset, column=c_idx, value=formula)
            row_offset += 1


    # --- Dashboard Sheet Design ---
    ws.sheet_properties.tabColor = theme_colors['accent_1_bg'].lstrip('FF') # Orange
    ws.column_dimensions['A'].width = 3 # Small left margin
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 18
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 18

    # Main Title
    ws.merge_cells('A1:F2')
    ws['A1'] = title.upper()
    apply_font(ws['A1'], size=24, bold=True, color=theme_colors['header_fg'], name='Montserrat')
    apply_fill(ws['A1'], theme_colors['header_bg'])
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    # Month Selector
    ws['B4'] = "For the month of"
    apply_font(ws['B4'], size=12, bold=True, name='Montserrat')
    ws['B4'].alignment = Alignment(horizontal='left', vertical='center')
    apply_fill(ws['B4'], theme_colors['neutral_bg'])

    ws['D4'].value = "=EOMONTH(TODAY(),-1)" # Default to last month
    ws['D4'].number_format = 'MMM-YY'
    apply_font(ws['D4'], size=12, bold=True, name='Montserrat')
    apply_fill(ws['D4'], theme_colors['primary_bg'])
    ws['D4'].alignment = Alignment(horizontal='center', vertical='center')

    # Data Validation for Month Selector
    dv = DataValidation(type="list", formula1="='Staging'!$B$4:$N$4")
    ws.add_data_validation(dv)
    dv.add('D4')

    # Define a helper to create KPI blocks
    def create_kpi_block(ws, start_cell: str, category_title: str, kpi_name: str, kpi_row: int, target_row: int, prior_month_row: int, is_percentage: bool, lower_is_better: bool = False, budget_vs_actual: bool = False, target_multiplier: int = 1):
        """
        Creates a formatted KPI block with dynamic data and conditional formatting.
        kpi_row, target_row, prior_month_row are the row numbers on the Staging sheet.
        """
        cell_range = f"{get_column_letter(ws.cell(start_cell).column)}:{get_column_letter(ws.cell(start_cell).column + 4)}"
        ws.merge_cells(f'{start_cell.split(":")[0]}:{get_column_letter(ws.cell(start_cell).column + 4)}7')
        ws[f'{start_cell.split(":")[0]}7'] = kpi_name
        apply_font(ws[f'{start_cell.split(":")[0]}7'], size=12, bold=True, color=theme_colors['primary_fg'], name='Montserrat')
        apply_fill(ws[f'{start_cell.split(":")[0]}7'], theme_colors['primary_bg'])
        ws[f'{start_cell.split(":")[0]}7'].alignment = Alignment(horizontal='center', vertical='center')

        # KPI Value (Current Month)
        kpi_val_cell = ws[f'{get_column_letter(ws.cell(start_cell).column + 2)}8']
        kpi_val_cell.value = f"=INDEX(Staging!$B${kpi_row}:$N${kpi_row}, MATCH($D$4, Staging!$B$4:$N$4, 0))"
        kpi_val_cell.number_format = '0%' if is_percentage else ('$#,##0' if '$' in kpi_name else '0')
        apply_font(kpi_val_cell, size=36, bold=True, name='Montserrat')
        kpi_val_cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells(f'{get_column_letter(ws.cell(start_cell).column+2)}8:{get_column_letter(ws.cell(start_cell).column+2)}8') # Main KPI Value

        # Conditional Formatting for main KPI value
        cf_rule_good = CellIsRule(operator="lessThanOrEqual" if lower_is_better else "greaterThanOrEqual",
                                  formula=[f"={get_column_letter(ws.cell(start_cell).column)}9*{target_multiplier}" if budget_vs_actual else f"={get_column_letter(ws.cell(start_cell).column)}9"],
                                  fill=PatternFill(start_color=theme_colors['good_indicator_bg'], end_color=theme_colors['good_indicator_bg'], fill_type="solid"))
        cf_rule_bad = CellIsRule(operator="greaterThan" if lower_is_better else "lessThan",
                                 formula=[f"={get_column_letter(ws.cell(start_cell).column)}9*{target_multiplier}" if budget_vs_actual else f"={get_column_letter(ws.cell(start_cell).column)}9"],
                                 fill=PatternFill(start_color=theme_colors['bad_indicator_bg'], end_color=theme_colors['bad_indicator_bg'], fill_type="solid"))

        ws.conditional_formatting.add(kpi_val_cell.coordinate, cf_rule_good)
        ws.conditional_formatting.add(kpi_val_cell.coordinate, cf_rule_bad)

        # Labels and Values for Target and Prior Month
        ws[f'{get_column_letter(ws.cell(start_cell).column)}9'] = "Vs. Target"
        ws[f'{get_column_letter(ws.cell(start_cell).column+1)}9'].value = f"=INDEX(Staging!$B${target_row}:$N${target_row}, MATCH($D$4, Staging!$B$4:$N$4, 0))"
        ws[f'{get_column_letter(ws.cell(start_cell).column+1)}9'].number_format = '0%' if is_percentage else ('$#,##0' if '$' in kpi_name else '0')
        ws[f'{get_column_letter(ws.cell(start_cell).column+1)}9'].alignment = Alignment(horizontal='center', vertical='center')

        ws[f'{get_column_letter(ws.cell(start_cell).column+3)}9'] = "Vs. Prior Month"
        ws[f'{get_column_letter(ws.cell(start_cell).column+4)}9'].value = f"=INDEX(Staging!$B${prior_month_row}:$N${prior_month_row}, MATCH(EOMONTH($D$4,-1), Staging!$B$4:$N$4, 0))"
        ws[f'{get_column_letter(ws.cell(start_cell).column+4)}9'].number_format = '0%' if is_percentage else ('$#,##0' if '$' in kpi_name else '0')
        ws[f'{get_column_letter(ws.cell(start_cell).column+4)}9'].alignment = Alignment(horizontal='center', vertical='center')

        for col_idx in [ws.cell(start_cell).column, ws.cell(start_cell).column+3]:
            apply_font(ws.cell(row=9, column=col_idx), size=8, bold=True, name='Montserrat')
        for col_idx in [ws.cell(start_cell).column+1, ws.cell(start_cell).column+4]:
            apply_font(ws.cell(row=9, column=col_idx), size=8, name='Montserrat')

        # Apply borders to the entire block
        thin_border = apply_border(Side(border_style="thin", color="000000"))
        for row in ws[f'{start_cell.split(":")[0]}7:{get_column_letter(ws.cell(start_cell).column + 4)}9'].rows:
            for cell in row:
                cell.border = thin_border

        return f'{get_column_letter(ws.cell(start_cell).column + 4)}' # Return end column for next KPI

    # Define a helper to create KPI Category headers
    def create_kpi_category_header(ws, start_row: int, text: str):
        ws.merge_cells(f'A{start_row}:F{start_row}')
        ws.cell(row=start_row, column=1, value=text.upper())
        apply_font(ws.cell(row=start_row, column=1), size=14, bold=True, color=theme_colors['category_fg'], name='Montserrat')
        apply_fill(ws.cell(row=start_row, column=1), theme_colors['category_bg'])
        ws.cell(row=start_row, column=1).alignment = Alignment(horizontal='center', vertical='center')

    # Working Capital Efficiency KPIs
    current_row = 6 # Starting row for KPI blocks after month selector
    create_kpi_category_header(ws, current_row, "Working Capital Efficiency")
    current_row += 1

    last_col = create_kpi_block(ws, f'B{current_row}', "Working Capital Efficiency", "DSO (Days Sales Outstanding)", 7, 8, 7, is_percentage=False, lower_is_better=True)
    last_col = create_kpi_block(ws, f'{get_column_letter(ws.cell(f'{last_col}{current_row}').column + 1)}{current_row}', "Working Capital Efficiency", "DPO (Days Payables Outstanding)", 10, 11, 10, is_percentage=False, lower_is_better=False)
    last_col = create_kpi_block(ws, f'{get_column_letter(ws.cell(f'{last_col}{current_row}').column + 1)}{current_row}', "Working Capital Efficiency", "Non-Current AR %", 13, 14, 13, is_percentage=True, lower_is_better=True)

    # Sales KPIs
    current_row += 5
    create_kpi_category_header(ws, current_row, "Sales KPIs")
    current_row += 1

    last_col = create_kpi_block(ws, f'B{current_row}', "Sales KPIs", "CAC (Customer Acquisition Cost)", 17, 18, 17, is_percentage=False, lower_is_better=True)
    last_col = create_kpi_block(ws, f'{get_column_letter(ws.cell(f'{last_col}{current_row}').column + 1)}{current_row}', "Sales KPIs", "Sales vs. Budget%", 20, 21, 20, is_percentage=True, lower_is_better=False)
    last_col = create_kpi_block(ws, f'{get_column_letter(ws.cell(f'{last_col}{current_row}').column + 1)}{current_row}', "Sales KPIs", "Gross Margin", 24, 25, 24, is_percentage=True, lower_is_better=False)

    # Cost KPIs
    current_row += 5
    create_kpi_category_header(ws, current_row, "Cost KPIs")
    current_row += 1

    last_col = create_kpi_block(ws, f'B{current_row}', "Cost KPIs", "OPEX Actual vs. Budget", 27, 28, 27, is_percentage=True, lower_is_better=True)
    last_col = create_kpi_block(ws, f'{get_column_letter(ws.cell(f'{last_col}{current_row}').column + 1)}{current_row}', "Cost KPIs", "CPFTE (Cost Per Full Time Employee)", 30, 31, 30, is_percentage=False, lower_is_better=True)

    # Freeze panes for better navigation
    ws.freeze_panes = 'A6'

