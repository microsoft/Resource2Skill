from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation

def _load_theme_colors(theme_name: str):
    """Loads a simplified theme palette for demonstration."""
    themes = {
        "corporate_blue": {
            "header_bg": "002B4C", "header_fg": "FFFFFF",
            "section_bg": "2A5576", "section_fg": "FFFFFF",
            "input_fg": "0000FF", "formula_fg": "000000",
            "accent": "FFD700" # Yellow for highlights
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_sheet(wb, sheet_name: str, *, title: str = "Financial Model", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a worksheet demonstrating dynamic scenario input with data validation and sheet protection.
    """
    colors = _load_theme_colors(theme)
    
    # Create Cover Sheet
    ws_cover = wb.create_sheet(title="Cover")
    ws_cover.title = "Cover" # Ensure correct name if it's the first sheet
    
    ws_cover.sheet_view.showGridLines = False

    # Title
    ws_cover['B2'] = title
    ws_cover.merge_cells('B2:E2')
    ws_cover['B2'].font = Font(name='Calibri', size=18, bold=True, color=colors["header_fg"])
    ws_cover['B2'].fill = PatternFill(start_color=colors["header_bg"], end_color=colors["header_bg"], fill_type="solid")
    ws_cover['B2'].alignment = Alignment(horizontal='center', vertical='center')

    # Scenario Analysis Section Header
    ws_cover['B4'] = 'Scenario Analysis'
    ws_cover.merge_cells('B4:C4')
    ws_cover['B4'].font = Font(name='Calibri', size=12, bold=True, color=colors["section_fg"])
    ws_cover['B4'].fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")

    # Scenario Selector Label
    ws_cover['B6'] = 'Live Scenario'
    ws_cover['B6'].font = Font(name='Calibri', size=11, bold=True)

    # Scenario Selector Input Cell
    scenario_cell = ws_cover['C6']
    scenario_cell.value = 2 # Default to Base Case
    scenario_cell.font = Font(name='Calibri', size=11, color=colors["input_fg"])
    scenario_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Add Data Validation to Scenario Selector
    dv = DataValidation(type="list", formula1='"1,2,3"', allow_blank=False)
    dv.error_title = 'Invalid Scenario'
    dv.error = 'Please enter 1 (Best Case), 2 (Base Case), or 3 (Worst Case).'
    ws_cover.add_data_validation(dv)
    dv.add(scenario_cell)

    # Add a comment to the scenario selector for instructions
    comment_text = "1 = Best Case\n2 = Base Case\n3 = Worst Case"
    scenario_cell.comment = Comment(comment_text, "Excel Expert")
    
    # General Settings Section Header
    ws_cover['E4'] = 'General Settings'
    ws_cover.merge_cells('E4:F4')
    ws_cover['E4'].font = Font(name='Calibri', size=12, bold=True, color=colors["section_fg"])
    ws_cover['E4'].fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")

    # Table of Contents Section Header
    ws_cover['H4'] = 'Table of Contents'
    ws_cover.merge_cells('H4:I4')
    ws_cover['H4'].font = Font(name='Calibri', size=12, bold=True, color=colors["section_fg"])
    ws_cover['H4'].fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")
    
    # Table of Contents Items (Hyperlinks)
    ws_cover['H6'] = 'Income Statement'
    ws_cover['H6'].hyperlink = "#'Forecast'!A1"
    ws_cover['H6'].font = Font(name='Calibri', size=11, color='0000FF', underline='single') # Blue, underlined for hyperlink

    ws_cover['H7'] = 'Cover Page'
    ws_cover['H7'].hyperlink = "#'Cover'!A1"
    ws_cover['H7'].font = Font(name='Calibri', size=11, color='0000FF', underline='single')

    # Create Forecast Sheet
    ws_forecast = wb.create_sheet(title="Forecast")
    ws_forecast.sheet_view.showGridLines = False

    # Income Statement Title (Dynamic)
    ws_forecast['B2'] = f"='Cover'!F6&\" Financial Model\"" # Dynamic title link
    ws_forecast.merge_cells('B2:K2')
    ws_forecast['B2'].font = Font(name='Calibri', size=18, bold=True, color=colors["header_fg"])
    ws_forecast['B2'].fill = PatternFill(start_color=colors["header_bg"], end_color=colors["header_bg"], fill_type="solid")
    ws_forecast['B2'].alignment = Alignment(horizontal='center', vertical='center')

    # Years Header
    years = [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
    year_suffixes = ["A", "A", "A", "E", "E", "E", "E", "E"] # A for Actual, E for Estimate

    for i, year in enumerate(years):
        col_letter = get_column_letter(i + 3) # Starting from column C
        ws_forecast[f'{col_letter}3'] = year
        ws_forecast[f'{col_letter}3'].number_format = f'# "{year_suffixes[i]}"'
        ws_forecast[f'{col_letter}3'].font = Font(name='Calibri', size=11, bold=True, color=colors["header_fg"])
        ws_forecast[f'{col_letter}3'].fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")
        ws_forecast.column_dimensions[col_letter].width = 10

    # Line Items
    line_items = [
        "Revenue", "COGS", "Gross Profit", "SG&A", "R&D", "Operating Income",
        "Other Income / (Expense), Net", "Pre-Tax Income", "Taxes", "Net Income"
    ]
    for r_idx, item in enumerate(line_items):
        ws_forecast[f'B{r_idx+4}'] = item
        ws_forecast[f'B{r_idx+4}'].font = Font(name='Calibri', size=11)
    
    # Financial Data (simplified hard-coded for Actuals, dynamic for Forecasts)
    # Revenue
    ws_forecast['C4'] = 5210
    ws_forecast['D4'] = 5435
    ws_forecast['E4'] = 5710
    ws_forecast['F4'] = f"=F4*(1+G17)" # Link to dynamic growth rate (placeholder)
    
    # COGS
    ws_forecast['C5'] = 3345
    ws_forecast['D5'] = 3350
    ws_forecast['E5'] = 3551
    ws_forecast['F5'] = f"=F4*G18" # Link to dynamic COGS %
    
    # SG&A
    ws_forecast['C7'] = 850
    ws_forecast['D7'] = 870
    ws_forecast['E7'] = 900
    ws_forecast['F7'] = f"=F4*G19" # Link to dynamic SG&A %

    # R&D
    ws_forecast['C8'] = 400
    ws_forecast['D8'] = 420
    ws_forecast['E8'] = 400
    ws_forecast['F8'] = f"=F4*G20" # Link to dynamic R&D %

    # Other Income / (Expense), Net
    ws_forecast['C10'] = 50
    ws_forecast['D10'] = 50
    ws_forecast['E10'] = 50
    ws_forecast['F10'] = "=E10" # Link to previous for forecasts

    # Tax Rate (Assumption)
    ws_forecast['C12'] = 228 # Example historical tax amounts
    ws_forecast['D12'] = 186
    ws_forecast['E12'] = 147
    ws_forecast['F12'] = f"=G11*G22" # Link to dynamic Tax Rate

    # Gross Profit Calculation
    ws_forecast['B6'].font = Font(name='Calibri', size=11, bold=True)
    ws_forecast['F6'] = f'=F4-F5'

    # Operating Income Calculation
    ws_forecast['B9'].font = Font(name='Calibri', size=11, bold=True)
    ws_forecast['F9'] = f'=F6-F7-F8'

    # Pre-Tax Income Calculation
    ws_forecast['B11'].font = Font(name='Calibri', size=11, bold=True)
    ws_forecast['F11'] = f'=F9-F10'

    # Net Income Calculation
    ws_forecast['B13'].font = Font(name='Calibri', size=11, bold=True)
    ws_forecast['B13'].fill = PatternFill(start_color=colors["accent"], end_color=colors["accent"], fill_type="solid")
    ws_forecast.merge_cells('B13:C13')
    ws_forecast['F13'] = f'=F11-F12'
    ws_forecast['F13'].fill = PatternFill(start_color=colors["accent"], end_color=colors["accent"], fill_type="solid")

    # Drag formulas to the right for forecasted years
    for row in range(4, 14): # From Revenue to Net Income
        if ws_forecast[f'F{row}'].value is not None:
            formula = ws_forecast[f'F{row}'].value
            for col_idx in range(7, len(years) + 3): # G to K
                target_cell = ws_forecast[f'{get_column_letter(col_idx)}{row}']
                # Adjust cell references dynamically if it's not a hardcoded value
                if isinstance(formula, str) and "=" in formula:
                    # Simple relative reference adjustment for direct links or basic ops
                    if formula.startswith("="):
                        if "=" in formula:
                            # Replace F with appropriate col_letter for relative linking
                            # This is a simplified approach, a real model uses more robust linking
                            adjusted_formula = formula.replace('F', get_column_letter(col_idx - 1)).replace('G', get_column_letter(col_idx))
                            target_cell.value = adjusted_formula
                        else:
                             target_cell.value = formula # Should not happen with "=" check
                elif isinstance(ws_forecast[f'F{row}'].value, (int, float)):
                    # For hard-coded numbers, we want to skip or link to the assumption row
                    # This is where the CHOOSE logic for scenario needs to be (see below)
                    pass # Handled by the CHOOSE function for assumptions.

    # Income Statement Assumptions Section
    ws_forecast['B16'] = 'Income Statement Assumptions'
    ws_forecast.merge_cells('B16:K16')
    ws_forecast['B16'].font = Font(name='Calibri', size=12, bold=True, color=colors["section_fg"])
    ws_forecast['B16'].fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")

    # Assumption Headers
    assumption_headers = [
        "Revenue Growth Rate", "COGS as a % of Revenue", "SG&A as a % of Revenue",
        "R&D as a % of Revenue", "Other Income / (Expense), Net (Value)", "Tax Rate"
    ]
    for r_idx, header in enumerate(assumption_headers):
        ws_forecast[f'B{r_idx+17}'] = header
        ws_forecast[f'B{r_idx+17}'].font = Font(name='Calibri', size=11)

    # Historical Assumption Calculations (e.g., Revenue Growth Rate)
    ws_forecast['D17'] = '=(D4/C4)-1'
    ws_forecast['E17'] = '=(E4/D4)-1'
    
    # Fill remaining historical assumption calculations
    ws_forecast['D18'] = '=D5/D4' # COGS %
    ws_forecast['E18'] = '=E5/E4'
    ws_forecast['D19'] = '=D7/D4' # SG&A %
    ws_forecast['E19'] = '=E7/E4'
    ws_forecast['D20'] = '=D8/D4' # R&D %
    ws_forecast['E20'] = '=E8/E4'
    ws_forecast['D21'] = '=D10' # Other Income (Value)
    ws_forecast['E21'] = '=E10'
    ws_forecast['D22'] = '=D12/D11' # Tax Rate (placeholder for historical EBT/Tax)
    ws_forecast['E22'] = '=E12/E11'

    # Apply percentage format and drag right for historical calculated assumptions
    for row in range(17, 23):
        for col_idx in range(4, 6): # Columns D and E
            cell = ws_forecast[f'{get_column_letter(col_idx)}{row}']
            cell.number_format = '0.0%'
            cell.font = Font(name='Calibri', size=11)
    
    # Scenario Values (Best, Base, Worst Cases)
    ws_forecast['B25'] = 'Revenue Scenarios'
    ws_forecast.merge_cells('B25:K25')
    ws_forecast['B25'].font = Font(name='Calibri', size=12, bold=True, color=colors["section_fg"])
    ws_forecast['B25'].fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")
    
    ws_forecast['B26'] = 'Best Case'
    ws_forecast['B27'] = 'Base Case'
    ws_forecast['B28'] = 'Worst Case'
    for row in range(26, 29):
        for col_idx in range(3, len(years) + 3): # From C to K
            cell = ws_forecast[f'{get_column_letter(col_idx)}{row}']
            cell.font = Font(name='Calibri', size=11, color=colors["input_fg"])
            cell.number_format = '0.0%'
            cell.value = 0.047 # Default value for Base Case
    
    # Adjust Best/Worst cases
    for col_idx in range(3, len(years) + 3):
        ws_forecast[f'{get_column_letter(col_idx)}26'].value = ws_forecast[f'{get_column_letter(col_idx)}27'].value + 0.02 # Best: Base + 2%
        ws_forecast[f'{get_column_letter(col_idx)}28'].value = ws_forecast[f'{get_column_letter(col_idx)}27'].value - 0.02 # Worst: Base - 2%

    # Apply CHOOSE to dynamic assumption cells on "Forecast" (e.g., Revenue Growth Rate)
    # These are the cells that were previously linked as '=AVERAGE(D17:F17)' or manually set
    # Now they depend on the scenario selector on the Cover sheet
    for col_idx in range(6, len(years) + 3): # From F to K
        col_letter = get_column_letter(col_idx)
        # Revenue Growth Rate (G17:K17)
        ws_forecast[f'{col_letter}17'].value = f'=CHOOSE(Cover!C6, Forecast!{col_letter}26, Forecast!{col_letter}27, Forecast!{col_letter}28)'
        ws_forecast[f'{col_letter}17'].number_format = '0.0%'
        ws_forecast[f'{col_letter}17'].font = Font(name='Calibri', size=11)

        # Other percentages (assuming constant or based on avg historical for simplicity)
        ws_forecast[f'{col_letter}18'].value = '=AVERAGE(D18:E18)'
        ws_forecast[f'{col_letter}19'].value = '=AVERAGE(D19:E19)'
        ws_forecast[f'{col_letter}20'].value = '=AVERAGE(D20:E20)'
        ws_forecast[f'{col_letter}21'].value = '=AVERAGE(D21:E21)' # Other income as value
        ws_forecast[f'{col_letter}22'].value = '=AVERAGE(D22:E22)' # Tax Rate
        
        for row in [18, 19, 20, 22]:
            ws_forecast[f'{col_letter}{row}'].number_format = '0.0%'
            ws_forecast[f'{col_letter}{row}'].font = Font(name='Calibri', size=11)
        ws_forecast[f'{col_letter}21'].font = Font(name='Calibri', size=11) # No percentage for Other Income value

    # Apply hardcoded color to inputs (blue) and formulas (black) on Forecast sheet
    # This needs to be done AFTER all formulas are set
    for row in range(4, ws_forecast.max_row + 1):
        for col_idx in range(3, ws_forecast.max_column + 1):
            cell = ws_forecast[f'{get_column_letter(col_idx)}{row}']
            if isinstance(cell.value, str) and cell.value.startswith('='):
                cell.font = Font(name='Calibri', size=11, color=colors["formula_fg"])
            else:
                cell.font = Font(name='Calibri', size=11, color=colors["input_fg"])

    # UNLOCK specific cells for user input before protection
    unlocked_cells_forecast = [f'{get_column_letter(col)}{row}' for col in range(3, len(years) + 3) for row in [26, 27, 28]] # Scenario values
    unlocked_cells_forecast.extend([f'C{r}' for r in [4, 5, 7, 8, 10, 12,]]) # Historical Hardcoded Values for Actuals

    for cell_ref in unlocked_cells_forecast:
        ws_forecast[cell_ref].protection.locked = False
    
    # UNLOCK the scenario selector on the Cover sheet
    ws_cover['C6'].protection.locked = False
    
    # Protect the Forecast sheet (leaving unlocked cells editable)
    ws_forecast.protection.sheet = True
    ws_forecast.protection.autoFilter = True # Allow autofilter if desired
    ws_forecast.protection.selectLockedCells = True
    ws_forecast.protection.selectUnlockedCells = True

    # Protect the Cover sheet (leaving unlocked cells editable)
    ws_cover.protection.sheet = True
    ws_cover.protection.selectLockedCells = True
    ws_cover.protection.selectUnlockedCells = True

    ws_forecast.freeze_panes = "C4" # Freeze panes at C4 as shown in video.

    # Set column widths for better readability
    ws_forecast.column_dimensions['B'].width = 30
    for col_idx in range(3, len(years) + 3):
        ws_forecast.column_dimensions[get_column_letter(col_idx)].width = 12

    ws_cover.column_dimensions['B'].width = 20
    ws_cover.column_dimensions['C'].width = 15
    ws_cover.column_dimensions['D'].width = 5
    ws_cover.column_dimensions['E'].width = 20
    ws_cover.column_dimensions['F'].width = 15
    ws_cover.column_dimensions['H'].width = 20
    ws_cover.column_dimensions['I'].width = 15
