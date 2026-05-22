import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Helper function to load theme colors (simplified for self-containment)
def _load_theme_colors(theme_name: str):
    if theme_name == "corporate_blue":
        return {
            "header_bg_dark": "FF2E4A77",
            "header_fg": "FFFFFFFF",
            "input_fg_blue": "FF0000FF", # Vivid blue from video #0000FF -> R:0 G:0 B:255
            "formula_fg_black": "FF000000",
            "subtotal_bg": "FFD9D9D9",
            "subtotal_fg": "FF000000",
            "net_income_bg": "FFFFFF00",
        }
    # Default to corporate_blue if theme_name not recognized
    return {
        "header_bg_dark": "FF2E4A77",
        "header_fg": "FFFFFFFF",
        "input_fg_blue": "FF0000FF",
        "formula_fg_black": "FF000000",
        "subtotal_bg": "FFD9D9D9",
        "subtotal_fg": "FF000000",
        "net_income_bg": "FFFFFF00",
    }

def render(ws: openpyxl.worksheet.worksheet.Worksheet, anchor: str, *, theme: str = "corporate_blue", 
           scenario_control_cell: str = "Cover!$C$6", 
           base_case_growth_rates: list = None, 
           best_case_offset: float = 0.02, 
           worst_case_offset: float = -0.02,
           num_historical_years: int = 3,
           num_forecast_years: int = 5) -> None:
    """
    Renders a dynamic revenue scenario analysis block for a financial model.
    This component includes predefined best, base, and worst-case forecast values
    for revenue growth rate, and uses Excel's CHOOSE function to dynamically
    select one of these scenarios based on a control cell.

    Args:
        ws: The worksheet to render on.
        anchor: The top-left cell for the 'Revenue Growth Rate' assumption line
                (e.g., "C17" for the example in the video).
        theme: The name of the color theme to use.
        scenario_control_cell: A string reference to the cell containing the
                                scenario index (1 for best, 2 for base, 3 for worst).
                                Assumes this cell is on a sheet named 'Cover'.
        base_case_growth_rates: A list of base case forecast growth rates (e.g., [0.047, 0.047, 0.047, 0.047, 0.047]).
                                Defaults to 5 years of 4.7% if not provided.
        best_case_offset: The percentage to add to the base case for the best scenario (e.g., 0.02 for +2%).
        worst_case_offset: The percentage to add (negative value) or subtract from the base case for the worst scenario (e.g., -0.02 for -2%).
        num_historical_years: Number of historical years for the main assumption row display.
        num_forecast_years: Number of forecast years for the main assumption row and scenarios.
    """
    if base_case_growth_rates is None:
        base_case_growth_rates = [0.047] * num_forecast_years
    elif len(base_case_growth_rates) != num_forecast_years:
        raise ValueError("Length of base_case_growth_rates must match num_forecast_years.")

    colors = _load_theme_colors(theme)

    # Convert anchor to row and column indices
    start_row = ws[anchor].row
    start_col = ws[anchor].column

    # --- Setup Revenue Growth Rate (main assumption line) ---
    ws.cell(row=start_row, column=start_col, value="Revenue Growth Rate").font = Font(bold=True)

    # Historical values (dummy values for illustration, copied from video example 0:05)
    historical_rates = [0.043, 0.051, 0.047] # These are example values from the video
    for i in range(min(num_historical_years, len(historical_rates))):
        col_offset = i
        cell = ws.cell(row=start_row, column=start_col + 1 + col_offset, value=historical_rates[i])
        cell.number_format = '0.0%'
        cell.font = Font(color=colors["input_fg_blue"])

    # --- Setup Revenue Scenarios Header and Labels ---
    # Based on video layout, the scenario block starts 9 rows below the main assumption.
    scenario_header_row = start_row + 9 
    scenario_block_start_col = start_col # Column 'B' in video example
    
    scenario_header_cell = ws.cell(row=scenario_header_row, column=scenario_block_start_col, value="Revenue Scenarios")
    scenario_header_cell.font = Font(bold=True, color=colors["header_fg"])
    scenario_header_cell.fill = PatternFill(start_color=colors["header_bg_dark"], end_color=colors["header_bg_dark"], fill_type="solid")
    
    # Merge cells for the scenario header
    ws.merge_cells(start_row=scenario_header_row, 
                   start_column=scenario_block_start_col, 
                   end_row=scenario_header_row, 
                   end_column=scenario_block_start_col + num_historical_years + num_forecast_years) # Extends across all year columns

    # Scenario Labels
    ws.cell(row=scenario_header_row + 1, column=scenario_block_start_col, value="Best Case")
    ws.cell(row=scenario_header_row + 2, column=scenario_block_start_col, value="Base Case")
    ws.cell(row=scenario_header_row + 3, column=scenario_block_start_col, value="Worst Case")

    # --- Calculate and Populate Scenario Values ---
    # Forecast years start after historical years + 1 (for the label column)
    forecast_col_offset_start = num_historical_years + 1 # G column if anchor is C
    
    for i in range(num_forecast_years):
        col_idx = start_col + forecast_col_offset_start + i # Current column for forecast year
        
        # Base Case Forecast Values
        base_val_cell = ws.cell(row=scenario_header_row + 2, column=col_idx)
        base_val_cell.value = base_case_growth_rates[i]
        base_val_cell.number_format = '0.0%'
        base_val_cell.font = Font(color=colors["input_fg_blue"])

        # Best Case Forecast Values
        best_val_cell = ws.cell(row=scenario_header_row + 1, column=col_idx)
        best_val_cell.value = base_case_growth_rates[i] + best_case_offset
        best_val_cell.number_format = '0.0%'
        best_val_cell.font = Font(color=colors["input_fg_blue"])
        
        # Worst Case Forecast Values
        worst_val_cell = ws.cell(row=scenario_header_row + 3, column=col_idx)
        worst_val_cell.value = base_case_growth_rates[i] + worst_case_offset
        worst_val_cell.number_format = '0.0%'
        worst_val_cell.font = Font(color=colors["input_fg_blue"])

        # --- Populate CHOOSE formula for main assumption row (Forecast Part) ---
        choose_formula_cell = ws.cell(row=start_row, column=col_idx)
        
        # Construct references to scenario values on the current sheet
        best_case_ref_in_formula = f"{ws.title}!${get_column_letter(col_idx)}${scenario_header_row + 1}"
        base_case_ref_in_formula = f"{ws.title}!${get_column_letter(col_idx)}${scenario_header_row + 2}"
        worst_case_ref_in_formula = f"{ws.title}!${get_column_letter(col_idx)}${scenario_header_row + 3}"
        
        # CHOOSE formula links to scenario_control_cell on the 'Cover' sheet
        # and to the scenario values on the current sheet (ws.title)
        choose_formula_cell.value = (
            f'=CHOOSE({scenario_control_cell},'
            f'{best_case_ref_in_formula},'
            f'{base_case_ref_in_formula},'
            f'{worst_case_ref_in_formula})'
        )
        choose_formula_cell.number_format = '0.0%'
        choose_formula_cell.font = Font(color=colors["formula_fg_black"])

    # --- Grouping for Scenario Rows (Rows 27-29 in video) ---
    # These rows are hidden initially as shown in the video
    ws.row_dimensions.group(scenario_header_row + 1, scenario_header_row + 3, hidden=True)

