from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils.datetime import ExcelOptionDate
from datetime import date, timedelta

# Assume _helpers.py is available for theme loading
try:
    from . import _helpers
except ImportError:
    # Fallback for direct execution/testing
    class _helpers:
        @staticmethod
        def load_theme_colors(theme_name):
            if theme_name == "corporate_blue":
                return {
                    "header_bg": "FF4F81BD", "header_fg": "FFFFFFFF",
                    "accent_bg": "FFC6E0B4", "accent_fg": "FF000000",
                    "light_bg": "FFD9D9D9", "text_fg": "FF000000",
                    "good_performance_bg": "FFC6EFCE", # Light Green
                    "bad_performance_bg": "FFFFC7CE",  # Light Red
                    "neutral_bg": "FFFFFFFF" # White
                }
            return {} # Default empty
        @staticmethod
        def set_fill(cell, hex_color):
            cell.fill = PatternFill(start_color=hex_color[2:], end_color=hex_color[2:], fill_type="solid")
        @staticmethod
        def set_font(cell, name=None, size=None, bold=None, italic=None, color=None):
            cell.font = Font(name=name, size=size, bold=bold, italic=italic, color=color)
        @staticmethod
        def set_border(cell, style="thin", color="FF000000"):
            side = Side(border_style=style, color=color[2:])
            cell.border = Border(top=side, bottom=side, left=side, right=side)

def create_kpi_dashboard_sheet_shell(wb, sheet_name: str = "3) Dashboard", *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a dynamic KPI dashboard sheet with conditional formatting.

    Args:
        wb: The openpyxl workbook object.
        sheet_name (str): The name of the dashboard sheet.
        title (str): The main title of the dashboard.
        theme (str): The name of the theme to use for colors.
    """
    ws = wb.create_sheet(sheet_name)
    colors = _helpers.load_theme_colors(theme)

    # --- Dashboard Layout ---
    ws.column_dimensions['A'].width = 1.8 # Small padding
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 14
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 14
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 14
    ws.column_dimensions['I'].width = 1.8 # Small padding

    # Main Title
    ws.merge_cells('B1:H2')
    title_cell = ws['B1']
    title_cell.value = title
    _helpers.set_font(title_cell, size=24, bold=True, color=colors["header_fg"])
    _helpers.set_fill(title_cell, colors["header_bg"])
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    _helpers.set_border(title_cell)

    # Month Selector
    ws['B4'] = "For the month of"
    _helpers.set_font(ws['B4'], bold=True)
    ws.merge_cells('D4:E4')
    month_selector_cell = ws['D4']
    month_selector_cell.value = date(2020, 8, 31) # Default month
    month_selector_cell.number_format = 'MMM-YY'
    month_selector_cell.alignment = Alignment(horizontal='center', vertical='center')
    _helpers.set_border(month_selector_cell)
    _helpers.set_fill(month_selector_cell, colors["accent_bg"])

    # Add Data Validation for Month Selector
    dv = DataValidation(type="list", formula1="='2) Staging'!$C$3:$N$3") # Assuming 12 months from C3 to N3
    ws.add_data_validation(dv)
    dv.add(month_selector_cell)

    # KPI Blocks Configuration (Name, KPI Row on Staging, Target Row on Staging, Conditional Formatting Rules)
    # Rules: (Value, Good_Is_LessThanOrEqualTo, Target_Value, Target_NumFormat_Percent_or_Dollar)
    kpi_configs = [
        # Working Capital Efficiency
        {"category_title": "Working Capital Efficiency", "category_row": 6, "color": "FF8497B1"},
        {"name": "DSO (Days Sales Outstanding)", "dashboard_row": 7, "staging_kpi_row": 8, "staging_target_row": 9,
         "cf_rule_config": {"target_value": 45, "good_if_less": True, "num_format": '#,##0'}},
        {"name": "DPO (Days Payables Outstanding)", "dashboard_row": 7, "staging_kpi_row": 12, "staging_target_row": 13,
         "cf_rule_config": {"target_value": 90, "good_if_less": False, "num_format": '#,##0'}},
        {"name": "Non-Current AR %", "dashboard_row": 7, "staging_kpi_row": 14, "staging_target_row": 15,
         "cf_rule_config": {"target_value": 0.03, "good_if_less": True, "num_format": '0%'}},

        # Sales KPIs
        {"category_title": "Sales KPIs", "category_row": 14, "color": "FF9DC3E6"},
        {"name": "CAC (Customer Acquisition Cost)", "dashboard_row": 15, "staging_kpi_row": 20, "staging_target_row": 21,
         "cf_rule_config": {"target_value": 15000, "good_if_less": True, "num_format": '$#,##0'}},
        {"name": "Sales vs. Budget%", "dashboard_row": 15, "staging_kpi_row": 22, "staging_target_row": 23,
         "cf_rule_config": {"target_value": 1.00, "good_if_less": False, "num_format": '0%'}},
        {"name": "Gross Margin", "dashboard_row": 15, "staging_kpi_row": 24, "staging_target_row": 25,
         "cf_rule_config": {"target_value": 0.38, "good_if_less": False, "num_format": '0%'}},

        # Cost KPIs
        {"category_title": "Cost KPIs", "category_row": 22, "color": "FFF1A5A5"},
        {"name": "OPEX Actual vs. Budget", "dashboard_row": 23, "staging_kpi_row": 28, "staging_target_row": 29,
         "cf_rule_config": {"target_value": 1.00, "good_if_less": True, "num_format": '0%'}},
        {"name": "CPFTE (Cost Per Full Time Employee)", "dashboard_row": 23, "staging_kpi_row": 30, "staging_target_row": 31,
         "cf_rule_config": {"target_value": 12500, "good_if_less": True, "num_format": '$#,##0'}},
    ]

    current_kpi_block_index = 0 # To track position of KPI blocks across row
    for config in kpi_configs:
        if "category_title" in config:
            ws.merge_cells(f'B{config["category_row"]}:H{config["category_row"]}')
            cat_cell = ws[f'B{config["category_row"]}']
            cat_cell.value = config["category_title"]
            _helpers.set_font(cat_cell, size=16, bold=True, color=colors["header_fg"])
            _helpers.set_fill(cat_cell, config["color"])
            cat_cell.alignment = Alignment(horizontal='center', vertical='center')
            _helpers.set_border(cat_cell)
            current_kpi_block_index = 0 # Reset block index for next category
            continue

        # Calculate column letters for this KPI block (e.g., B,C or D,E or F,G)
        kpi_start_col_letter = get_column_letter(ord('B') + current_kpi_block_index * 2)
        kpi_end_col_letter = get_column_letter(ord('B') + current_kpi_block_index * 2 + 1)

        # KPI Name Cell
        kpi_cell_row = config["dashboard_row"]
        kpi_name_cell_coord = f'{kpi_start_col_letter}{kpi_cell_row}'
        ws.merge_cells(f'{kpi_start_col_letter}{kpi_cell_row}:{kpi_end_col_letter}{kpi_cell_row}')
        kpi_name_cell = ws[kpi_name_cell_coord]
        kpi_name_cell.value = config["name"]
        _helpers.set_font(kpi_name_cell, size=12, bold=True, color=colors["header_fg"])
        _helpers.set_fill(kpi_name_cell, colors["light_bg"]) # Consistent background for KPI name cell
        kpi_name_cell.alignment = Alignment(horizontal='center', vertical='center')
        _helpers.set_border(kpi_name_cell)

        # Main KPI Value Cell
        kpi_value_cell_coord = f'{kpi_start_col_letter}{kpi_cell_row + 1}'
        ws.merge_cells(f'{kpi_start_col_letter}{kpi_cell_row + 1}:{kpi_end_col_letter}{kpi_cell_row + 1}')
        kpi_value_cell = ws[kpi_value_cell_coord]
        kpi_value_cell.value = f'=INDEX(\'2) Staging\'!$C${config["staging_kpi_row"]}:$N${config["staging_kpi_row"]},MATCH($D$4,\'2) Staging\'!$C$3:$N$3,0))'
        _helpers.set_font(kpi_value_cell, size=24, bold=True)
        kpi_value_cell.alignment = Alignment(horizontal='center', vertical='center')
        _helpers.set_border(kpi_value_cell)
        kpi_value_cell.number_format = config["cf_rule_config"]["num_format"]

        # Conditional Formatting for Main KPI Value
        if "cf_rule_config" in config:
            rule_config = config["cf_rule_config"]
            target_value = rule_config["target_value"]
            good_if_less = rule_config["good_if_less"]
            good_color = colors["good_performance_bg"]
            bad_color = colors["bad_performance_bg"]

            if good_if_less: # Smaller value is better
                # Green if less than or equal to target
                ws.conditional_formatting.add(kpi_value_cell.coordinate, CellIsRule(operator='lessThanOrEqual', formula=[str(target_value)], fill=PatternFill(start_color=good_color[2:], end_color=good_color[2:], fill_type="solid")))
                # Red if greater than target
                ws.conditional_formatting.add(kpi_value_cell.coordinate, CellIsRule(operator='greaterThan', formula=[str(target_value)], fill=PatternFill(start_color=bad_color[2:], end_color=bad_color[2:], fill_type="solid")))
            else: # Larger value is better
                # Green if greater than or equal to target
                ws.conditional_formatting.add(kpi_value_cell.coordinate, CellIsRule(operator='greaterThanOrEqual', formula=[str(target_value)], fill=PatternFill(start_color=good_color[2:], end_color=good_color[2:], fill_type="solid")))
                # Red if less than target
                ws.conditional_formatting.add(kpi_value_cell.coordinate, CellIsRule(operator='lessThan', formula=[str(target_value)], fill=PatternFill(start_color=bad_color[2:], end_color=bad_color[2:], fill_type="solid")))


        # Vs. Target and Vs. Prior Month Labels and Values
        labels_coords = [
            (f'{kpi_start_col_letter}{kpi_cell_row + 2}', f'{get_column_letter(ord(kpi_start_col_letter) + 1)}{kpi_cell_row + 2}', "Vs. Target"),
            (f'{kpi_end_col_letter}{kpi_cell_row + 2}', f'{get_column_letter(ord(kpi_end_col_letter) + 1)}{kpi_cell_row + 2}', "Vs. Prior Month")
        ]
        for label_cell_coord, value_cell_coord, label_text in labels_coords:
            label_cell = ws[label_cell_coord]
            label_cell.value = label_text
            _helpers.set_font(label_cell, size=9, bold=True)
            label_cell.alignment = Alignment(horizontal='center', vertical='center')
            _helpers.set_border(label_cell)
            _helpers.set_fill(label_cell, colors["neutral_bg"])

            value_cell = ws[value_cell_coord]
            if label_text == "Vs. Target":
                value_cell.value = f'=INDEX(\'2) Staging\'!$C${config["staging_target_row"]}:$N${config["staging_target_row"]},MATCH($D$4,\'2) Staging\'!$C$3:$N$3,0))'
            else: # Vs. Prior Month
                value_cell.value = f'=INDEX(\'2) Staging\'!$C${config["staging_kpi_row"]}:$N${config["staging_kpi_row"]},MATCH(EOMONTH($D$4,-1),\'2) Staging\'!$C$3:$N$3,0))'
            _helpers.set_font(value_cell, size=9)
            value_cell.alignment = Alignment(horizontal='center', vertical='center')
            _helpers.set_border(value_cell)
            _helpers.set_fill(value_cell, colors["neutral_bg"])
            value_cell.number_format = config["cf_rule_config"]["num_format"]

        current_kpi_block_index += 1


def _populate_mock_data_sheet(ws):
    """Populates a mock '1) Data' sheet with sample financial data."""
    ws.title = '1) Data'
    headers = ["Actual", "Jan-20", "Feb-20", "Mar-20", "Apr-20", "May-20", "Jun-20", "Jul-20", "Aug-20", "Sep-20", "Oct-20", "Nov-20", "Dec-20"]

    # Convert headers to actual dates (end of month for simplicity in formulas)
    month_dates = [date(2020, date.strptime(m.split('-')[0], '%b').month, 1).replace(day=1) for m in headers[1:]]
    for i, md in enumerate(month_dates):
        next_month = md.replace(day=28) + timedelta(days=4)
        month_dates[i] = next_month - timedelta(days=next_month.day) # End of month

    ws.cell(row=1, column=1, value=headers[0]) # "Actual" label
    for col_idx, md in enumerate(month_dates):
        cell = ws.cell(row=1, column=col_idx + 2, value=md)
        cell.number_format = 'M/D/YYYY' # Store as full date

    _helpers.set_font(ws.cell(row=1, column=1), bold=True)
    _helpers.set_fill(ws.cell(row=1, column=1), "FFD9D9D9")
    _helpers.set_border(ws.cell(row=1, column=1))
    for col_idx in range(2, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        _helpers.set_font(cell, bold=True)
        _helpers.set_fill(cell, "FFD9D9D9")
        _helpers.set_border(cell)
        cell.alignment = Alignment(horizontal='center', vertical='center')


    data_rows = [
        ["Sales", 1500000, 1590000, 1685400, 1786524, 1893716, 2007338, 2127780, 2255447, 2390774, 2534220, 2686873, 2849485],
        ["COGs", 900000, 954000, 1010320, 1070932, 1135198, 1203300, 1275498, 1352028, 1433090, 1519075, 1610010, 1706210],
        ["Gross Profit", "=B2-B3", "=C2-C3", "=D2-D3", "=E2-E3", "=F2-F3", "=G2-G3", "=H2-H3", "=I2-I3", "=J2-I3", "=K2-K3", "=L2-L3", "=M2-M3"],
        ["", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Account Receivables Balance", 2800000, 2940000, 3087000, 3241350, 3403418, 3573588, 3752268, 3939881, 4136875, 4343719, 4560905, 4788950],
        ["Credit Sales", 1500000, 1590000, 1685400, 1786524, 1893716, 2007338, 2127780, 2255447, 2390774, 2534220, 2686873, 2849485],
        ["Past due Accounts Receivables", 150000, 140000, 122500, 111500, 99500, 89000, 79000, 70000, 61000, 53000, 46000, 39000],
        ["Accounts Payable Balance", 3100000, 3255000, 3417750, 3588638, 3768069, 3956473, 4154296, 4362011, 4580112, 4809118, 5049574, 5301880],
        ["", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["OPEX", 600500, 612510, 624760, 637255, 649999, 663000, 676260, 689785, 703580, 717650, 732003, 746643],
        ["Full Time Employees", 44, 47, 49, 51, 53, 56, 58, 60, 62, 65, 67, 70],
        ["Sales & Marketing Costs", 550000, 569000, 589000, 609000, 629000, 649000, 669000, 689000, 709000, 729000, 749000, 769000],
        ["# of new customers", 40, 48, 52, 57, 62, 68, 75, 83, 92, 101, 112, 123],
        ["", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Sales Budget", 1680000, 1750000, 1820000, 1890000, 1960000, 2030000, 2100000, 2170000, 2240000, 2310000, 2380000, 2450000],
        ["COGS Budget", 1008000, 1050000, 1092000, 1134000, 1176000, 1218000, 1260000, 1302000, 1344000, 1386000, 1428000, 1470000],
        ["OPEX Budget", 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000]
    ]

    for r_idx, row_data in enumerate(data_rows):
        for c_idx, cell_value in enumerate(row_data):
            cell = ws.cell(row=r_idx + 2, column=c_idx + 1)
            cell.value = cell_value
            if c_idx > 0: # Only format data columns
                if r_idx in [0, 1, 4, 6, 7, 9, 11, 14, 15, 16]: # Dollar amounts
                    cell.number_format = '$#,##0'
                elif r_idx in [10, 12]: # Integers
                    cell.number_format = '#,##0'
            _helpers.set_fill(cell, "FFFFFFCC") # Yellow fill for data areas

    # Set column widths
    ws.column_dimensions['A'].width = 30
    for col_idx in range(2, ws.max_column + 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = 12

def _populate_mock_staging_sheet(ws, data_ws):
    """Populates a mock '2) Staging' sheet with calculated KPIs and targets."""
    ws.title = '2) Staging'
    
    # Copy headers (dates) from Data sheet
    for col_idx in range(2, data_ws.max_column + 1):
        cell = ws.cell(row=3, column=col_idx)
        cell.value = data_ws.cell(row=1, column=col_idx).value
        cell.number_format = 'M/D/YYYY' # Store as full date
        _helpers.set_font(cell, bold=True)
        _helpers.set_fill(cell, "FFD9D9D9")
        _helpers.set_border(cell)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    ws['A3'].value = "Category"
    _helpers.set_font(ws['A3'], bold=True)
    _helpers.set_fill(ws['A3'], "FFD9D9D9")
    _helpers.set_border(ws['A3'])
    ws['A3'].alignment = Alignment(horizontal='left')
    
    # Staging data rows start from row 4, first KPI category title in A4
    current_row = 4

    # Working Capital Efficiency KPIs
    ws[f'A{current_row}'].value = "Working Capital Efficiency"
    _helpers.set_font(ws[f'A{current_row}'], bold=True)
    current_row += 1 # A5

    # Link Account Receivables Balance from Data
    ws[f'A{current_row}'].value = "Account Receivables Balance"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}6,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    ar_balance_row = current_row
    current_row += 1 # A6

    # Link Credit Sales from Data
    ws[f'A{current_row}'].value = "Credit Sales"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}7,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    credit_sales_row = current_row
    current_row += 1 # A7

    # Link # of days in month from Data header row
    ws[f'A{current_row}'].value = "# of days"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=DAY(\'1) Data\'!{get_column_letter(col_idx)}1)'
        ws.cell(row=current_row, column=col_idx).number_format = '#,##0'
    days_in_month_row = current_row
    current_row += 1 # A8

    # DSO (Days Sales Outstanding) calculation
    ws[f'A{current_row}'].value = "DSO (Days Sales Outstanding)"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(ROUND((${get_column_letter(col_idx)}{ar_balance_row}/${get_column_letter(col_idx)}{credit_sales_row})*${get_column_letter(col_idx)}{days_in_month_row},0),0)'
        ws.cell(row=current_row, column=col_idx).number_format = '#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    dso_kpi_row = current_row
    current_row += 1 # A9

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 45 # Target value for DSO
        ws.cell(row=current_row, column=col_idx).number_format = '#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    dso_target_row = current_row
    current_row += 2 # A11 for next KPI category

    # Accounts Payable Balance (link from Data)
    ws[f'A{current_row}'].value = "Accounts Payable Balance"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}9,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    ap_balance_row = current_row
    current_row += 1 # A12

    # Link COGs from Data
    ws[f'A{current_row}'].value = "COGs"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}3,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    cogs_row = current_row
    current_row += 1 # A13

    # DPO (Days Payables Outstanding) calculation
    ws[f'A{current_row}'].value = "DPO (Days Payables Outstanding)"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(ROUND((${get_column_letter(col_idx)}{ap_balance_row}/${get_column_letter(col_idx)}{cogs_row})*${get_column_letter(col_idx)}{days_in_month_row},0),0)'
        ws.cell(row=current_row, column=col_idx).number_format = '#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    dpo_kpi_row = current_row
    current_row += 1 # A14

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 90 # Target value for DPO
        ws.cell(row=current_row, column=col_idx).number_format = '#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    dpo_target_row = current_row
    current_row += 2 # A16

    # Link Past due Accounts Receivables from Data
    ws[f'A{current_row}'].value = "Past due Accounts Receivables"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}8,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    past_due_ar_row = current_row
    current_row += 1 # A17

    # Non-Current AR % calculation
    ws[f'A{current_row}'].value = "Non-Current AR %"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(${get_column_letter(col_idx)}{past_due_ar_row}/${get_column_letter(col_idx)}{ar_balance_row},0)'
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    non_current_ar_kpi_row = current_row
    current_row += 1 # A18

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 0.03 # Target value for Non-Current AR %
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    non_current_ar_target_row = current_row
    current_row += 2 # A20

    # Sales KPIs
    ws[f'A{current_row}'].value = "Sales KPIs"
    _helpers.set_font(ws[f'A{current_row}'], bold=True)
    current_row += 1 # A21

    # Link Sales & Marketing Costs from Data
    ws[f'A{current_row}'].value = "Sales & Marketing Costs"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}12,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    s_m_costs_row = current_row
    current_row += 1 # A22

    # Link # of new customers from Data
    ws[f'A{current_row}'].value = "# of new customers"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}13,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    new_customers_row = current_row
    current_row += 1 # A23

    # CAC (Customer Acquisition Cost) calculation
    ws[f'A{current_row}'].value = "CAC (Customer Acquisition Cost)"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(ROUND(${get_column_letter(col_idx)}{s_m_costs_row}/${get_column_letter(col_idx)}{new_customers_row},0),0)'
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    cac_kpi_row = current_row
    current_row += 1 # A24

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 15000 # Target value for CAC
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    cac_target_row = current_row
    current_row += 2 # A26

    # Sales vs. Budget % calculation
    ws[f'A{current_row}'].value = "Sales vs. Budget%"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}2/\'1) Data\'!{get_column_letter(col_idx)}15,0)' # Sales Actual / Sales Budget
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    sales_vs_budget_kpi_row = current_row
    current_row += 1 # A27

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 1.00 # Target value for Sales vs. Budget %
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    sales_vs_budget_target_row = current_row
    current_row += 2 # A29

    # Gross Margin calculation
    ws[f'A{current_row}'].value = "Gross Margin"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}4/\'1) Data\'!{get_column_letter(col_idx)}2,0)' # Gross Profit / Sales Actual
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    gross_margin_kpi_row = current_row
    current_row += 1 # A31

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 0.38 # Target value for Gross Margin
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    gross_margin_target_row = current_row
    current_row += 2 # A33

    # Cost KPIs
    ws[f'A{current_row}'].value = "Cost KPIs"
    _helpers.set_font(ws[f'A{current_row}'], bold=True)
    current_row += 1 # A34

    # OPEX Actual vs. Budget calculation
    ws[f'A{current_row}'].value = "OPEX Actual vs. Budget"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}10/\'1) Data\'!{get_column_letter(col_idx)}17,0)' # OPEX Actual / OPEX Budget
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    opex_vs_budget_kpi_row = current_row
    current_row += 1 # A35

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 1.00 # Target value for OPEX Actual vs. Budget
        ws.cell(row=current_row, column=col_idx).number_format = '0%'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    opex_vs_budget_target_row = current_row
    current_row += 2 # A37

    # Link Full Time Employees from Data
    ws[f'A{current_row}'].value = "Full Time Employees"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(\'1) Data\'!{get_column_letter(col_idx)}11,0)'
        ws.cell(row=current_row, column=col_idx).number_format = '#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    fte_row = current_row
    current_row += 1 # A38

    # CPFTE (Cost Per Full Time Employee) calculation
    ws[f'A{current_row}'].value = "CPFTE (Cost Per Full Time Employee)"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = f'=IFERROR(ROUND(\'1) Data\'!{get_column_letter(col_idx)}10/${get_column_letter(col_idx)}{fte_row},0),0)' # OPEX / FTE
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    cpfte_kpi_row = current_row
    current_row += 1 # A39

    ws[f'A{current_row}'].value = "Target"
    for col_idx in range(2, data_ws.max_column + 1):
        ws.cell(row=current_row, column=col_idx).value = 12500 # Target value for CPFTE
        ws.cell(row=current_row, column=col_idx).number_format = '$#,##0'
        _helpers.set_fill(ws.cell(row=current_row, column=col_idx), "FFFFFFCC")
    cpfte_target_row = current_row
    current_row += 1


# Main rendering function for the dashboard sheet
def render_sheet(wb, sheet_name: str = "3) Dashboard", *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # Ensure Data and Staging sheets are populated before dashboard
    if '1) Data' not in wb.sheetnames:
        data_ws = wb.create_sheet('1) Data', 0)
        _populate_mock_data_sheet(data_ws)
    else:
        data_ws = wb['1) Data']

    if '2) Staging' not in wb.sheetnames:
        staging_ws = wb.create_sheet('2) Staging', 1)
        _populate_mock_staging_sheet(staging_ws, data_ws)
    else:
        staging_ws = wb['2) Staging']

    create_kpi_dashboard_sheet_shell(wb, sheet_name, title=title, theme=theme, **kwargs)
