from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
import openpyxl.comments

def render_sheet(wb, sheet_name: str, *, company_name: str = "Sample Inc.", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)

    # Load theme colors
    from ._helpers import get_theme_colors, apply_border
    colors = get_theme_colors(theme)

    # --- Setup Years Header ---
    start_year = 2023
    num_actual_years = 3 # 2023, 2024, 2025
    num_forecast_years = 6 # 2026-2031 (as per video's final example)
    total_years = num_actual_years + num_forecast_years

    # Populate years
    ws.cell(row=3, column=4, value=start_year)
    for i in range(1, total_years):
        year = start_year + i
        ws.cell(row=3, column=4 + i, value=year)

    # Apply custom number format for Actuals and Estimates
    for col_idx in range(4, 4 + num_actual_years):
        ws.cell(row=3, column=col_idx).number_format = '#"A"'
    for col_idx in range(4 + num_actual_years, 4 + total_years):
        ws.cell(row=3, column=col_idx).number_format = '#"E"'

    # Style years header
    header_fill = PatternFill(start_color=colors.header_bg, end_color=colors.header_bg, fill_type="solid")
    header_font = Font(color=colors.header_fg, bold=True)
    for col_idx in range(4, 4 + total_years):
        cell = ws.cell(row=3, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # --- Income Statement Line Items ---
    line_items = [
        "Revenue", "COGS", "Gross Profit", "Selling, general & administrative",
        "Research & development", "Operating Income", "Other income / (expense), net",
        "Pre-tax income", "Taxes", "Net Income"
    ]
    for i, item in enumerate(line_items):
        ws.cell(row=4 + i, column=2, value=item)

    # Data for historical actuals (example values from video)
    # Note: Using example data from the video's initial populated table (0:04)
    # These are hardcoded inputs and should be in the input_font color
    historical_data = {
        "Revenue": [5210, 5435, 5710],
        "COGS": [3345, 3350, 3551],
        "Selling, general & administrative": [850, 870, 900],
        "Research & development": [400, 420, 400],
        "Other income / (expense), net": [50, 50, 50],
        "Taxes": [228, 186, 147]
    }

    input_font = Font(color=colors.input_fg)
    for row_idx, item in enumerate(line_items):
        if item in historical_data:
            for i, value in enumerate(historical_data[item]):
                cell = ws.cell(row=4 + row_idx, column=4 + i, value=value)
                cell.font = input_font
                cell.number_format = '#,##0'

    # Calculate historical Gross Profit, Operating Income, Pre-Tax Income, Net Income
    for year_offset in range(num_actual_years):
        col = 4 + year_offset
        # Gross Profit (R4-R5)
        ws.cell(row=6, column=col, value=f'={ws.cell(row=4, column=col).coordinate}-{ws.cell(row=5, column=col).coordinate}').number_format = '#,##0'
        # Operating Income (R6-R7-R8)
        ws.cell(row=9, column=col, value=f'={ws.cell(row=6, column=col).coordinate}-{ws.cell(row=7, column=col).coordinate}-{ws.cell(row=8, column=col).coordinate}').number_format = '#,##0'
        # Pre-Tax Income (R9+R10)
        ws.cell(row=11, column=col, value=f'={ws.cell(row=9, column=col).coordinate}+{ws.cell(row=10, column=col).coordinate}').number_format = '#,##0'
        # Net Income (R11-R12)
        ws.cell(row=13, column=col, value=f'={ws.cell(row=11, column=col).coordinate}-{ws.cell(row=12, column=col).coordinate}').number_format = '#,##0'

    # --- Income Statement Formatting ---
    bold_font = Font(bold=True)
    subtotal_border = apply_border(top_style='thin')
    net_income_fill = PatternFill(start_color=colors.accent_bg, end_color=colors.accent_bg, fill_type="solid")
    net_income_border = apply_border(top_style='thin', bottom_style='double')

    # Apply bold and top border to subtotals
    subtotal_rows = [6, 9, 11]
    for row_idx in subtotal_rows:
        for col_idx in range(2, 4 + total_years):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = bold_font
            cell.border = subtotal_border
        
    # Apply special formatting to Net Income
    for col_idx in range(2, 4 + total_years):
        cell = ws.cell(row=13, column=col_idx)
        cell.font = bold_font
        cell.fill = net_income_fill
        cell.border = net_income_border

    # --- Income Statement Assumptions ---
    assumption_items = [
        "Revenue Growth Rate", "COGS as a % of Revenue", "SG&A as a % of Revenue",
        "R&D as a % of Revenue", "Other income / (expense), net", "Tax Rate"
    ]
    for i, item in enumerate(assumption_items):
        ws.cell(row=17 + i, column=2, value=item)

    # Style assumptions header
    assumptions_header_fill = PatternFill(start_color=colors.header_bg, end_color=colors.header_bg, fill_type="solid")
    assumptions_header_font = Font(color=colors.header_fg, bold=True)
    header_cell = ws.cell(row=16, column=2, value="Income Statement Assumptions")
    header_cell.fill = assumptions_header_fill
    header_cell.font = assumptions_header_font
    ws.merge_cells(start_row=16, start_column=2, end_row=16, end_column=3)

    # Calculate historical assumptions
    for year_offset in range(num_actual_years):
        col = 4 + year_offset
        # Revenue Growth Rate
        if year_offset > 0: # Can't calculate for the very first year (2023)
            ws.cell(row=17, column=col, value=f'=(D4/{ws.cell(row=4, column=col-1).coordinate})-1').number_format = '0.0%'
        else:
            ws.cell(row=17, column=col, value="").number_format = '0.0%' # No 2022 data

        # COGS as % of Revenue
        ws.cell(row=18, column=col, value=f'={ws.cell(row=5, column=col).coordinate}/{ws.cell(row=4, column=col).coordinate}').number_format = '0.0%'
        # SG&A as % of Revenue
        ws.cell(row=19, column=col, value=f'={ws.cell(row=7, column=col).coordinate}/{ws.cell(row=4, column=col).coordinate}').number_format = '0.0%'
        # R&D as % of Revenue
        ws.cell(row=20, column=col, value=f'={ws.cell(row=8, column=col).coordinate}/{ws.cell(row=4, column=col).coordinate}').number_format = '0.0%'
        # Other income / (expense), net (linked to actuals)
        ws.cell(row=21, column=col, value=ws.cell(row=10, column=col).coordinate).number_format = '#,##0'
        # Tax Rate (hardcoded for historical, as it's an input)
        ws.cell(row=22, column=col, value=0.25).number_format = '0.0%'
        ws.cell(row=22, column=col).font = input_font

    # --- Scenario Values for Revenue Growth Rate ---
    ws.cell(row=26, column=2, value="Revenue Scenarios").fill = assumptions_header_fill
    ws.cell(row=26, column=2).font = assumptions_header_font
    ws.merge_cells(start_row=26, start_column=2, end_row=26, end_column=3)
    
    ws.cell(row=27, column=2, value="Best Case")
    ws.cell(row=28, column=2, value="Base Case")
    ws.cell(row=29, column=2, value="Worst Case")

    # Example scenario values (consistent with video's final dynamic output)
    best_case_rev_growth = 0.067 # 6.7%
    base_case_rev_growth = 0.047 # 4.7%
    worst_case_rev_growth = 0.027 # 2.7%

    # Populate scenario values for forecast years
    for i in range(num_forecast_years):
        col = 4 + num_actual_years + i
        ws.cell(row=27, column=col, value=best_case_rev_growth).number_format = '0.0%'
        ws.cell(row=28, column=col, value=base_case_rev_growth).number_format = '0.0%'
        ws.cell(row=29, column=col, value=worst_case_rev_growth).number_format = '0.0%'
        
    # --- Forecasted Assumptions (using CHOOSE for scenario analysis) ---
    # Scenario control cell is assumed to be on 'Cover' sheet, cell C6
    scenario_control_cell_ref = "Cover!$C$6"

    for year_offset in range(num_actual_years, total_years):
        col = 4 + year_offset

        # Revenue Growth Rate (Dynamic)
        choose_formula_rev_growth = f'=CHOOSE({scenario_control_cell_ref}, {ws.cell(row=27, column=col).coordinate}, {ws.cell(row=28, column=col).coordinate}, {ws.cell(row=29, column=col).coordinate})'
        ws.cell(row=17, column=col, value=choose_formula_rev_growth).number_format = '0.0%'
        ws.cell(row=17, column=col).font = input_font # Assumption input is blue (output of CHOOSE is an input to the model logic)

        # COGS, SG&A, R&D as % of Revenue (using AVERAGE of historical, then +/- 2% for best/worst)
        # We need to evaluate the historical average within the CHOOSE formula for robustness
        for assump_row_idx in [18, 19, 20]:
            hist_avg_formula = f'=AVERAGE({ws.cell(row=assump_row_idx, column=4).coordinate}:{ws.cell(row=assump_row_idx, column=4+num_actual_years-1).coordinate})'
            # Note: For simplicity, embedding values directly in the CHOOSE string.
            # In a real model, intermediate cells for scenario-specific percentages would be preferred.
            choose_formula_percent = f'=CHOOSE({scenario_control_cell_ref}, {hist_avg_formula}+0.02, {hist_avg_formula}, {hist_avg_formula}-0.02)'
            ws.cell(row=assump_row_idx, column=col, value=choose_formula_percent).number_format = '0.0%'
            ws.cell(row=assump_row_idx, column=col).font = input_font

        # Other income / (expense), net (forecasted as constant from last actual)
        ws.cell(row=21, column=col, value=ws.cell(row=10, column=num_actual_years+3).coordinate).number_format = '#,##0'
        ws.cell(row=21, column=col).font = input_font

        # Tax Rate (forecasted as constant from last actual)
        ws.cell(row=22, column=col, value=ws.cell(row=22, column=num_actual_years+3).coordinate).number_format = '0.0%'
        ws.cell(row=22, column=col).font = input_font

    # --- Forecasted Income Statement Calculations (using updated dynamic assumptions) ---
    for year_offset in range(num_actual_years, total_years):
        col = 4 + year_offset
        prev_col = col - 1
        
        # Revenue
        ws.cell(row=4, column=col, value=f'={ws.cell(row=4, column=prev_col).coordinate}*(1+{ws.cell(row=17, column=col).coordinate})').number_format = '#,##0'
        # COGS
        ws.cell(row=5, column=col, value=f'={ws.cell(row=18, column=col).coordinate}*{ws.cell(row=4, column=col).coordinate}').number_format = '#,##0'
        # Gross Profit
        ws.cell(row=6, column=col, value=f'={ws.cell(row=4, column=col).coordinate}-{ws.cell(row=5, column=col).coordinate}').number_format = '#,##0'
        # Selling, general & administrative
        ws.cell(row=7, column=col, value=f'={ws.cell(row=19, column=col).coordinate}*{ws.cell(row=4, column=col).coordinate}').number_format = '#,##0'
        # Research & development
        ws.cell(row=8, column=col, value=f'={ws.cell(row=20, column=col).coordinate}*{ws.cell(row=4, column=col).coordinate}').number_format = '#,##0'
        # Operating Income
        ws.cell(row=9, column=col, value=f'={ws.cell(row=6, column=col).coordinate}-{ws.cell(row=7, column=col).coordinate}-{ws.cell(row=8, column=col).coordinate}').number_format = '#,##0'
        # Other income / (expense), net (linking to assumption row)
        ws.cell(row=10, column=col, value=ws.cell(row=21, column=col).coordinate).number_format = '#,##0'
        # Pre-tax income
        ws.cell(row=11, column=col, value=f'={ws.cell(row=9, column=col).coordinate}+{ws.cell(row=10, column=col).coordinate}').number_format = '#,##0'
        # Taxes
        ws.cell(row=12, column=col, value=f'={ws.cell(row=11, column=col).coordinate}*{ws.cell(row=22, column=col).coordinate}').number_format = '#,##0'
        # Net Income
        ws.cell(row=13, column=col, value=f'={ws.cell(row=11, column=col).coordinate}-{ws.cell(row=12, column=col).coordinate}').number_format = '#,##0'

    # Set column widths
    ws.column_dimensions['B'].width = 35
    for col_idx in range(4, 4 + total_years):
        ws.column_dimensions[chr(65 + col_idx)].width = 12

    # --- Sheet Protection ---
    # Unlock blue cells (manual inputs/assumptions)
    for r in range(4, 14): # Income Statement historical values
        for c in range(4, 4 + num_actual_years):
            if ws.cell(row=r, column=c).font.color and ws.cell(row=r, column=c).font.color.rgb == colors.input_fg.rgb:
                ws.cell(row=r, column=c).protection.locked = False
    
    for r in range(17, 23): # Assumptions section
        for c in range(4, 4 + total_years):
             if ws.cell(row=r, column=c).font.color and ws.cell(row=r, column=c).font.color.rgb == colors.input_fg.rgb:
                ws.cell(row=r, column=c).protection.locked = False

    # Protect the sheet (no password for simplicity, but can be added)
    ws.protection.sheet = True

    # --- Outline Groups ---
    # Group assumption rows
    # Note: openpyxl's group indices are 1-based and exclusive for end_row.
    # The actual data in rows 17-22 means group 17 to 22.
    ws.row_dimensions.group(17, 22, hidden=True) 
    
    # Group forecast columns
    # Group from the first forecast column (e.g., G) to the last (e.g., K)
    ws.column_dimensions.group(4 + num_actual_years, 4 + total_years -1, hidden=True)

    # --- Dynamic Title for the Sheet (from Cover page) ---
    # Assuming Cover!F6 holds the company name
    ws.cell(row=1, column=2).value = f'="Income Statement of "&Cover!F6'
    ws.cell(row=1, column=2).font = Font(size=14, bold=True)
    ws.merge_cells(start_row=1, start_column=2, end_row=1, end_column=4)
    ws.cell(row=1, column=2).protection.locked = True # Lock the title cell

    # Freeze panes below the header
    ws.freeze_panes = ws['C4']


# Example Cover sheet setup (for testing purposes)
def setup_cover_sheet(wb, company_name: str = "Nike"):
    ws_cover = wb.create_sheet("Cover", 0) # Create as the first sheet
    from ._helpers import get_theme_colors, apply_border
    colors = get_theme_colors("corporate_blue")

    ws_cover.column_dimensions['C'].width = 20
    ws_cover.column_dimensions['F'].width = 20
    ws_cover.column_dimensions['H'].width = 20

    header_fill = PatternFill(start_color=colors.header_bg, end_color=colors.header_bg, fill_type="solid")
    header_font = Font(color=colors.header_fg, bold=True)
    input_font = Font(color=colors.input_fg)

    # Scenario Analysis section
    ws_cover.cell(row=4, column=2, value="Scenario Analysis").fill = header_fill
    ws_cover.cell(row=4, column=2).font = header_font
    ws_cover.cell(row=4, column=2).alignment = Alignment(horizontal='center')
    ws_cover.merge_cells(start_row=4, start_column=2, end_row=4, end_column=3)

    ws_cover.cell(row=5, column=2, value="Live Scenario")
    ws_cover.cell(row=6, column=3, value=1).font = input_font # Scenario selector input (1, 2, or 3)
    ws_cover.cell(row=6, column=3).protection.locked = False # Unlock for input

    # Add data validation to scenario selector
    dv = DataValidation(type="list", formula1='"1,2,3"', allow_blank=False, showDropDown=True)
    ws_cover.add_data_validation(dv)
    dv.add(ws_cover.cell(row=6, column=3))
    
    # Add comment to scenario selector
    ws_cover.cell(row=6, column=3).comment = openpyxl.comments.Comment('1 = Best Case\n2 = Base Case\n3 = Worst Case', 'Career Principles')

    ws_cover.cell(row=8, column=2, value="Alerts").fill = header_fill
    ws_cover.cell(row=8, column=2).font = header_font
    ws_cover.cell(row=8, column=2).alignment = Alignment(horizontal='center')
    ws_cover.merge_cells(start_row=8, start_column=2, end_row=8, end_column=3)

    ws_cover.cell(row=9, column=2, value="Balance Sheet Balances?")

    # General Settings section
    ws_cover.cell(row=4, column=5, value="General Settings").fill = header_fill
    ws_cover.cell(row=4, column=5).font = header_font
    ws_cover.cell(row=4, column=5).alignment = Alignment(horizontal='center')
    ws_cover.merge_cells(start_row=4, start_column=5, end_row=4, end_column=6)

    ws_cover.cell(row=5, column=5, value="Company Name")
    ws_cover.cell(row=6, column=6, value=company_name).font = input_font # Company name input
    ws_cover.cell(row=6, column=6).protection.locked = False # Unlock for input

    ws_cover.cell(row=7, column=5, value="Company Ticker")
    ws_cover.cell(row=8, column=6, value="ABC")
    ws_cover.cell(row=9, column=5, value="Currency")
    ws_cover.cell(row=10, column=6, value="USD")
    ws_cover.cell(row=11, column=5, value="Last Update")
    ws_cover.cell(row=12, column=6, value="01/08/2025")
    ws_cover.cell(row=13, column=5, value="Contact")
    ws_cover.cell(row=14, column=6, value="Johnson")

    # Table of Contents section
    ws_cover.cell(row=4, column=8, value="Table of Contents").fill = header_fill
    ws_cover.cell(row=4, column=8).font = header_font
    ws_cover.cell(row=4, column=8).alignment = Alignment(horizontal='center')
    ws_cover.merge_cells(start_row=4, start_column=8, end_row=4, end_column=9)

    ws_cover.cell(row=5, column=8, value="Cover Page")
    ws_cover.cell(row=6, column=8, value="Income Statement").hyperlink = f"#'{sheet_name}'!A1"
    ws_cover.cell(row=6, column=8).font = Font(color="0000FF", underline="single")
    ws_cover.cell(row=7, column=8, value="Balance Sheet")
    ws_cover.cell(row=8, column=8, value="Cash Flow Statement")
    ws_cover.cell(row=9, column=8, value="Assumptions & Drivers")

    # Protect the cover sheet
    ws_cover.protection.sheet = True

