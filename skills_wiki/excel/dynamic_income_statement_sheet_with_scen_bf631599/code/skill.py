from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

def _load_theme_palette(theme_name: str):
    """Loads a simplified theme palette for demonstration."""
    palettes = {
        "corporate_blue": {
            "header_bg_dark": "002060",  # Dark Blue
            "header_fg_light": "FFFFFF",  # White
            "accent_blue_light": "D9E1F2",  # Light Blue
            "accent_blue_medium": "A6BFE6", # Medium Blue
            "input_fg": "0000FF",  # Blue for inputs
            "formula_fg": "000000", # Black for formulas
            "subtotal_fg": "000000", # Black for subtotals
            "warning_fill": "FFFF00", # Yellow for highlights
            "border_thin": "000000", # Black thin border
        }
    }
    return palettes.get(theme_name, palettes["corporate_blue"])

def render_sheet(wb, sheet_name: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a dynamic Income Statement sheet with scenario analysis.

    Args:
        wb: The Openpyxl workbook object.
        sheet_name: The name for the new worksheet.
        theme: The name of the theme to use for styling.
        **kwargs: Additional arguments (not used in this simplified example).
    """
    palette = _load_theme_palette(theme)
    ws = wb.create_sheet(title=sheet_name)

    # --- 1. Setup Column Widths ---
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 35
    for col_idx in range(ord('C'), ord('L')): # C to K
        ws.column_dimensions[chr(col_idx)].width = 15

    # --- 2. Headers & Years ---
    ws.cell(row=1, column=2, value="Income Statement of Nike").font = Font(bold=True, size=16)

    years_start_col = 4 # Column D
    start_year = 2023
    num_historical_years = 3
    num_forecast_years = 5
    total_years = num_historical_years + num_forecast_years

    # Year row formatting
    year_font = Font(bold=True, color=palette['header_fg_light'])
    header_fill = PatternFill(start_color=palette['header_bg_dark'], end_color=palette['header_bg_dark'], fill_type="solid")
    actual_fill = PatternFill(start_color=palette['accent_blue_light'], end_color=palette['accent_blue_light'], fill_type="solid")
    forecast_fill = PatternFill(start_color=palette['accent_blue_medium'], end_color=palette['accent_blue_medium'], fill_type="solid")

    for i in range(total_years):
        col = years_start_col + i
        year_cell = ws.cell(row=3, column=col)
        
        if i == 0:
            year_cell.value = start_year
        else:
            year_cell.value = f'={ws.cell(row=3, column=col-1).coordinate}+1'
        
        # Apply custom number format and fill
        if i < num_historical_years:
            year_cell.number_format = '# "A"'
            year_cell.fill = actual_fill
            year_cell.font = year_font
            year_cell.protection.locked = True # Historical years are locked
        else:
            year_cell.number_format = '# "E"'
            year_cell.fill = forecast_fill
            year_cell.font = year_font
            year_cell.protection.locked = True # Forecast year labels are locked

    # --- 3. Income Statement Line Items ---
    line_items = [
        "Revenue", "COGS", "Gross Profit",
        "Selling, general & administrative", "Research & development", "Operating Income",
        "Other income / (expense), net", "Pre-tax income", "Taxes", "Net Income"
    ]
    for r_idx, item in enumerate(line_items):
        ws.cell(row=4+r_idx, column=2, value=item).font = Font(bold=False) # Not bold initially

    # Bold and border key subtotals
    bold_font = Font(bold=True)
    thin_border = Border(top=Side(style='thin', color=palette['border_thin']), bottom=Side(style='thin', color=palette['border_thin']))
    double_bottom_border = Border(top=Side(style='thin', color=palette['border_thin']), bottom=Side(style='double', color=palette['border_thin']))

    ws.cell(row=6, column=2).font = bold_font
    ws.cell(row=9, column=2).font = bold_font
    ws.cell(row=11, column=2).font = bold_font
    ws.cell(row=13, column=2).font = bold_font
    
    # Apply borders to subtotal rows across all relevant columns (B to K)
    for r in [6, 9, 11]:
        for c in range(2, years_start_col + total_years):
            ws.cell(row=r, column=c).border = thin_border
    
    # Net Income gets double bottom border and yellow fill
    for c in range(2, years_start_col + total_years):
        ws.cell(row=13, column=c).border = double_bottom_border
        ws.cell(row=13, column=c).fill = PatternFill(start_color=palette['warning_fill'], end_color=palette['warning_fill'], fill_type="solid")

    # --- 4. Historical Data (Hardcoded - Blue font) ---
    historical_data = {
        (4,4): 5210, (4,5): 5435, (4,6): 5710,
        (5,4): 3345, (5,5): 3350, (5,6): 3551,
        (7,4): 850, (7,5): 870, (7,6): 900,
        (8,4): 400, (8,5): 420, (8,6): 400,
        (10,4): 50, (10,5): 50, (10,6): 50,
        (12,4): 228, (12,5): 186, (12,6): 147
    }
    input_font = Font(color=palette['input_fg'])
    for (r,c), val in historical_data.items():
        cell = ws.cell(row=r, column=c, value=val)
        cell.font = input_font
        cell.number_format = '#,##0'
        cell.protection.locked = False # Unlock inputs

    # Calculate historical Gross Profit, Operating Income, Pre-tax Income, Net Income
    for c in range(years_start_col, years_start_col + num_historical_years):
        # Gross Profit
        ws.cell(row=6, column=c).value = f'={ws.cell(row=4, column=c).coordinate}-{ws.cell(row=5, column=c).coordinate}'
        # Operating Income
        ws.cell(row=9, column=c).value = f'={ws.cell(row=6, column=c).coordinate}-{ws.cell(row=7, column=c).coordinate}-{ws.cell(row=8, column=c).coordinate}'
        # Pre-tax Income
        ws.cell(row=11, column=c).value = f'={ws.cell(row=9, column=c).coordinate}-{ws.cell(row=10, column=c).coordinate}'
        # Net Income
        ws.cell(row=13, column=c).value = f'={ws.cell(row=11, column=c).coordinate}-{ws.cell(row=12, column=c).coordinate}'

    # Apply number format to all value cells
    for r in range(4, 14):
        for c in range(years_start_col, years_start_col + total_years):
            ws.cell(row=r, column=c).number_format = '#,##0'
            if ws.cell(row=r, column=c).font.color is None: # Only apply black if not already colored blue
                ws.cell(row=r, column=c).font = Font(color=palette['formula_fg'])

    # --- 5. Income Statement Assumptions (Manual & Calculated) ---
    ws.cell(row=16, column=2, value="Income Statement Assumptions").font = Font(bold=True, color=palette['header_fg_light'])
    ws.cell(row=16, column=2).fill = header_fill
    ws.cell(row=16, column=2).protection.locked = True

    assumption_items = [
        "Revenue Growth Rate", "COGS as a % of Revenue", "SG&A as a % of Revenue",
        "R&D as a % of Revenue", "Other income / (expense), net", "Tax Rate"
    ]
    for r_idx, item in enumerate(assumption_items):
        ws.cell(row=17+r_idx, column=2, value=item)
        ws.cell(row=17+r_idx, column=2).protection.locked = True # Assumption labels are locked

    # Calculate historical assumption percentages
    for c in range(years_start_col, years_start_col + num_historical_years):
        # Revenue Growth Rate (C17, D17, E17)
        if c > years_start_col: # Skip first historical year for growth rate
            ws.cell(row=17, column=c).value = f'=({ws.cell(row=4, column=c).coordinate}/{ws.cell(row=4, column=c-1).coordinate})-1'
        # COGS as % of Revenue
        ws.cell(row=18, column=c).value = f'={ws.cell(row=5, column=c).coordinate}/{ws.cell(row=4, column=c).coordinate}'
        # SG&A as % of Revenue
        ws.cell(row=19, column=c).value = f'={ws.cell(row=7, column=c).coordinate}/{ws.cell(row=4, column=c).coordinate}'
        # R&D as % of Revenue
        ws.cell(row=20, column=c).value = f'={ws.cell(row=8, column=c).coordinate}/{ws.cell(row=4, column=c).coordinate}'
        # Other income / (expense), net (just link the previous value for consistency)
        ws.cell(row=21, column=c).value = f'={ws.cell(row=10, column=c).coordinate}'
        # Tax Rate (just link the previous value for consistency)
        ws.cell(row=22, column=c).value = f'={ws.cell(row=12, column=c).coordinate}/{ws.cell(row=11, column=c).coordinate}'
    
    # Set number format for assumption rows (percentages and numbers)
    for c in range(years_start_col, years_start_col + total_years):
        for r in [17, 18, 19, 20, 22]: # Percentages
            ws.cell(row=r, column=c).number_format = '0.0%'
        ws.cell(row=21, column=c).number_format = '#,##0' # Other income / (expense), net

    # --- 6. Revenue Scenario Analysis (for CHOOSE function) ---
    ws.cell(row=25, column=2, value="Revenue Scenarios").font = Font(bold=True, color=palette['header_fg_light'])
    ws.cell(row=25, column=2).fill = header_fill
    ws.cell(row=25, column=2).protection.locked = True

    scenario_labels = ["Best Case", "Base Case", "Worst Case"]
    scenario_data = { # Example data, assuming it's for 2026E onwards
        "Best Case": [0.067, 0.067, 0.067, 0.067, 0.067], # Example growth rate 6.7%
        "Base Case": [0.047, 0.047, 0.047, 0.047, 0.047], # Example growth rate 4.7%
        "Worst Case": [0.027, 0.027, 0.027, 0.027, 0.027]  # Example growth rate 2.7%
    }

    for r_idx, label in enumerate(scenario_labels):
        row_num = 26 + r_idx
        ws.cell(row=row_num, column=2, value=label).font = bold_font
        ws.cell(row=row_num, column=2).protection.locked = True # Scenario labels are locked
        
        # Scenario values (manual input, blue font)
        for c_idx, val in enumerate(scenario_data[label]):
            col_num = years_start_col + num_historical_years + c_idx # Start from 2026E column G
            cell = ws.cell(row=row_num, column=col_num, value=val)
            cell.number_format = '0.0%'
            cell.font = input_font
            cell.protection.locked = False # Unlock scenario inputs

    # --- 7. Forecast Assumptions (linked to CHOOSE) ---
    # Assume Cover!C6 holds the scenario index (1, 2, or 3)
    cover_scenario_cell = 'Cover!$C$6'

    for c in range(years_start_col + num_historical_years, years_start_col + total_years): # From 2026E (col G)
        # Revenue Growth Rate
        ws.cell(row=17, column=c).value = f'=CHOOSE({cover_scenario_cell}, {ws.cell(row=26, column=c).coordinate}, {ws.cell(row=27, column=c).coordinate}, {ws.cell(row=28, column=c).coordinate})'
        # COGS as % of Revenue (using average of historical actuals as Base Case)
        ws.cell(row=18, column=c).value = f'=AVERAGE(D18:F18)'
        # SG&A as % of Revenue (using average of historical actuals as Base Case)
        ws.cell(row=19, column=c).value = f'=AVERAGE(D19:F19)'
        # R&D as % of Revenue (using average of historical actuals as Base Case)
        ws.cell(row=20, column=c).value = f'=AVERAGE(D20:F20)'
        # Other income / (expense), net (always 50)
        ws.cell(row=21, column=c).value = f'={ws.cell(row=21, column=c-1).coordinate}' # Link to previous cell
        # Tax Rate (manual input, blue font)
        ws.cell(row=22, column=c).value = 0.25 # Assuming 25% tax rate
        ws.cell(row=22, column=c).font = input_font
        ws.cell(row=22, column=c).number_format = '0.0%'
        ws.cell(row=22, column=c).protection.locked = False # Unlock tax rate input

    # --- 8. Grouping Rows and Columns ---
    # Group assumption rows
    ws.row_dimensions.group(17, 22, hidden=True)

    # Group forecast columns
    ws.column_dimensions.group(chr(years_start_col + num_historical_years), chr(years_start_col + total_years -1), hidden=True)

    # --- 9. Sheet Protection ---
    ws.protection.sheet = True # Protect the sheet
    ws.protection.selectCellsLocked = True
    ws.protection.selectCellsUnlocked = True

    # Assume a minimal 'Cover' sheet exists with a scenario selector
    if 'Cover' not in wb.sheetnames:
        cover_ws = wb.create_sheet("Cover", 0)
        cover_ws.cell(row=6, column=3, value=1).font = input_font
        cover_ws.cell(row=6, column=3).protection.locked = False # Unlock scenario selector
        cover_ws.cell(row=5, column=3, value="Live Scenario").font = bold_font
        cover_ws.column_dimensions['C'].width = 15
        cover_ws.protection.sheet = True
        cover_ws.protection.selectCellsLocked = True
        cover_ws.protection.selectCellsUnlocked = True
