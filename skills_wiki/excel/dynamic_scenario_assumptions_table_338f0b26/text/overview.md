### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Assumptions Table

*   **Tier**: component
*   **Core Mechanism**: This skill establishes a dynamic assumptions block that automatically updates its values based on a user-selected scenario. It achieves this by creating multiple static assumption tables (e.g., "Upper Case", "Lower Case") to represent different scenarios. A "Live Case" assumptions table then uses the `CHOOSE` Excel formula, driven by a dedicated "Scenario Selector" cell, to pull the corresponding values from the scenario-specific tables. This allows for instant, interactive scenario analysis within a financial model.
*   **Applicability**: This skill is ideal for financial modeling, business forecasting, and strategic planning where decision-makers need to evaluate the impact of various underlying assumptions (e.g., growth rates, costs, prices) on key financial outputs (like revenue, profit) without manually altering input cells. It's suitable for any Excel-based report that benefits from toggling between different input sets to observe outcome changes.

### 2. Structural Breakdown

-   **Data Layout**:
    *   **Scenario Selector Cell**: A single cell (e.g., J4) located outside the main model, containing a numeric value (e.g., 1 or 2) to select the active scenario.
    *   **Live Case Assumptions Table**: A block of cells (e.g., B28:H44, based on the provided code structure) that displays the currently active assumptions. Each data cell in this block contains a `CHOOSE` formula.
    *   **Scenario-Specific Assumptions Tables**: Multiple blocks of cells (e.g., "Upper Case (Scenario 1)" at B46:H62 and "Lower Case (Scenario 2)" at B64:H80) which are direct copies of the assumption structure, populated with fixed values specific to each scenario.
    *   **Income Statement**: A separate section (e.g., starting at B3) that directly references the values from the "Live Case" assumptions table to perform its calculations.
-   **Formula Logic**:
    *   **Scenario Selector**: The cell (J4 in the example) is populated with a numerical index (e.g., 1 or 2).
    *   **Live Case Assumption Cells**: For each assumption value (e.g., Number of Orders for Year 1, D30), the formula is `=CHOOSE($J$4, [Scenario1_Value_Cell], [Scenario2_Value_Cell])`.
        *   `$J$4`: The absolute reference to the Scenario Selector cell.
        *   `[Scenario1_Value_Cell]`: The cell containing the assumption value for Scenario 1 (e.g., D48 for Number of Orders, Year 1, Scenario 1).
        *   `[Scenario2_Value_Cell]`: The cell containing the assumption value for Scenario 2 (e.g., D66 for Number of Orders, Year 1, Scenario 2).
    *   **Derived Values (e.g., Number of Orders for Year 2 onwards)**: These cells within the "Live Case" assumption block use standard Excel formulas to calculate values based on the *previous year's live case assumption* and the *current year's live case growth rate*. For example, `D30` (Number of Orders, Year 1) is `=CHOOSE(...)`, then `E30` (Number of Orders, Year 2) is `=D30 * (1 + E31)`.
    *   **Income Statement Calculations**: Formulas for revenue, COGS, profit lines refer directly to the cells in the "Live Case" assumptions table.
    *   **Corporate Tax**: Uses an `IF` statement to apply tax only if `Operating Profit` is positive: `=IF(D21<0,"NA",D21*D44)`. D21 is Operating Profit, D44 is Corporate Tax Rate (from Live Case assumptions).
    *   **Profit / (Loss)**: Uses `IFERROR` to handle "NA" from corporate tax: `=IFERROR(D21-D24,D21)`.
-   **Visual Design**:
    *   **Headers**: Sections like "Income Statement" and "Assumptions" (for Live Case and Scenarios) have a distinct background color (e.g., light blue) and bold font.
    *   **Scenario Selector**: The cell is prominently highlighted (e.g., yellow fill) with bold, centered text.
    *   **Input Values (hard-coded in scenario tables)**: Formatted with a blue font to distinguish them from dynamic formula outputs.
    *   **Dynamic Values (in Live Case and Income Statement)**: Formatted with a black font.
    *   **Borders**: Thin gray borders delineate all cells and sections for clarity.
-   **Charts/Tables**: The skill itself generates assumption tables and an income statement. No separate charts are demonstrated as part of this core skill.
-   **Theme Hooks**: `header_bg`, `header_fg`, `text_fg`, `input_fg`, `accent_bg`, `border_color`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

# Helper function (similar to _helpers.py)
def get_theme_colors(theme_name):
    # Simplified theme palette for demonstration
    if theme_name == "corporate_blue":
        return {
            "header_bg": "FFDDEBF7",  # Light blue
            "header_fg": "FF000000",  # Black
            "text_fg": "FF000000",    # Black
            "input_fg": "FF0000FF",    # Blue
            "accent_bg": "FFFFFF00",  # Yellow
            "border_color": "FF808080" # Gray
        }
    return get_theme_colors("corporate_blue") # Fallback

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a dynamic assumptions block linked to scenario tables and a scenario selector.

    Args:
        ws: The worksheet to render on.
        anchor: The top-left cell of the 'Live Case' assumptions block (e.g., 'B28').
        theme: The theme name to use for styling.
        **kwargs: Additional keyword arguments.
    """
    colors = get_theme_colors(theme)
    font_bold = Font(bold=True, color=colors["header_fg"])
    font_normal = Font(color=colors["text_fg"])
    font_input = Font(color=colors["input_fg"])
    header_fill = PatternFill(start_color=colors["header_bg"], end_color=colors["header_bg"], fill_type="solid")
    accent_fill = PatternFill(start_color=colors["accent_bg"], end_color=colors["accent_bg"], fill_type="solid")
    border_thin = Border(left=Side(style='thin', color=colors["border_color"]),
                         right=Side(style='thin', color=colors["border_color"]),
                         top=Side(style='thin', color=colors["border_color"]),
                         bottom=Side(style='thin', color=colors["border_color"]))

    # Parse anchor
    anchor_col = openpyxl.utils.column_index_from_string(anchor[0])
    anchor_row = int(anchor[1:])

    # --- Scenario Selector ---
    scenario_selector_cell_ref = ws.cell(row=4, column=10).coordinate # J4
    ws.cell(row=4, column=9).value = "Scenario" # I4
    ws.cell(row=4, column=9).font = font_bold
    ws.cell(row=4, column=10).value = 1 # Default scenario
    ws.cell(row=4, column=10).fill = accent_fill
    ws.cell(row=4, column=10).font = font_bold
    ws.cell(row=4, column=10).alignment = Alignment(horizontal='center')
    ws.cell(row=4, column=10).border = border_thin

    # Data Validation for Scenario Selector
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(scenario_selector_cell_ref)


    # --- Define Scenario Data (hardcoded for skill reproduction) ---
    # Scenario 1 (Upper Case) data based on video's optimistic values
    s1_num_orders_start = 3000
    s1_growth_rates = [1.00, 0.75, 0.50, 0.35]
    s1_avg_order_value = 39.95
    s1_manuf_cost = 6.50
    s1_order_fulfil_cost = 2.25
    s1_warehouse_rent = [20000, 20000, 30000, 30000, 30000]
    s1_salaries_payroll = [50000, 100000, 100000, 100000, 100000]
    s1_marketing = [25000, 50000, 100000, 100000, 100000]
    s1_other = 5000
    s1_corp_tax_rate = 0.20

    # Scenario 2 (Lower Case) data based on video's pessimistic adjustments
    s2_num_orders_start = 2000
    s2_growth_rates = [1.00, 0.75, 0.50, 0.35] # Growth rates shown as same in video's s2 block
    s2_avg_order_value = 34.95
    s2_manuf_cost = 8.00
    s2_order_fulfil_cost = 2.25
    s2_warehouse_rent = [20000, 20000, 30000, 30000, 30000] # Same as S1 in video's s2 block
    s2_salaries_payroll = [50000, 100000, 100000, 100000, 100000] # Same as S1 in video's s2 block
    s2_marketing = [25000, 50000, 100000, 100000, 100000] # Same as S1 in video's s2 block
    s2_other = 5000 # Same as S1 in video's s2 block
    s2_corp_tax_rate = 0.25 # Increased tax rate in video's s2 block

    # --- Assumptions Labels and Row Offsets from "Assumptions" header ---
    # These map to the structure shown in the video for assumptions.
    # Relative to the 'Assumptions' header row.
    assumption_structure = [
        ("Revenue", None, None), # Header, no actual values
        ("Number of Orders", "#", None),
        ("Order Growth Rate", "%", "0%"),
        ("Average Order Value", "$", "#,##0.00"),
        (None, None, None), # Empty row
        ("Cost of Goods Sold (per order)", None, None), # Header
        ("Manufacturing", "$", "#,##0.00"),
        ("Order Fulfillment", "$", "#,##0.00"),
        (None, None, None), # Empty row
        ("Operating Expenses", None, None), # Header
        ("Warehouse Rent", "$", "#,##0"),
        ("Salaries & Payroll", "$", "#,##0"),
        ("Marketing", "$", "#,##0"),
        ("Other", "$", "#,##0"),
        (None, None, None), # Empty row
        ("Corporate Tax Rate", "%", "0%")
    ]
    
    def create_assumption_block(start_row_idx, title, scenario_data, is_live_case=False):
        # Header for the block (e.g., "Live Case", "Upper Case (Scenario 1)")
        ws.cell(row=start_row_idx, column=anchor_col).value = title
        ws.cell(row=start_row_idx, column=anchor_col).font = font_bold
        ws.cell(row=start_row_idx, column=anchor_col).fill = header_fill
        ws.merge_cells(start_row=start_row_idx, end_row=start_row_idx, start_column=anchor_col, end_column=anchor_col+7) # Merge up to H column

        current_line_offset = 0
        for i, (label, unit, num_format) in enumerate(assumption_structure):
            if label is None: # Handle empty rows
                current_line_offset += 1
                continue

            current_row = start_row_idx + current_line_offset + 1
            
            # Label
            ws.cell(row=current_row, column=anchor_col).value = label
            if label in ["Revenue", "Cost of Goods Sold (per order)", "Operating Expenses"]: # Sub-headers
                ws.cell(row=current_row, column=anchor_col).font = font_bold
            else:
                ws.cell(row=current_row, column=anchor_col).font = font_normal

            # Unit
            if unit:
                ws.cell(row=current_row, column=anchor_col+1).value = unit
                ws.cell(row=current_row, column=anchor_col+1).font = font_normal

            # Values for Year 1 to Year 5
            for year_offset in range(5): # Year 1 to Year 5 (D to H columns)
                col = anchor_col + 2 + year_offset # D column
                cell = ws.cell(row=current_row, column=col)

                s1_ref = ws.cell(row=start_row_idx + 18 + current_line_offset + 1, column=col).coordinate
                s2_ref = ws.cell(row=start_row_idx + 36 + current_line_offset + 1, column=col).coordinate

                if is_live_case and label not in ["Revenue", "Cost of Goods Sold (per order)", "Operating Expenses"]:
                    # All actual data cells in Live Case use CHOOSE, referencing S1 and S2 blocks
                    cell.value = f'=CHOOSE({scenario_selector_cell_ref}, {s1_ref}, {s2_ref})'
                    cell.font = font_normal
                elif label == "Number of Orders":
                    if year_offset == 0:
                        cell.value = scenario_data['num_orders_start']
                    else:
                        prev_orders_cell_ref = ws.cell(row=current_row, column=col-1).coordinate
                        # Find the row for 'Order Growth Rate' within the current block structure
                        growth_rate_offset = 0
                        for idx, (lbl, _, _) in enumerate(assumption_structure):
                            if lbl == "Order Growth Rate":
                                growth_rate_offset = idx
                                break
                        growth_rate_row = start_row_idx + 1 + growth_rate_offset # (current_line_offset of Num Orders) + 1 from Num Orders
                        growth_rate_cell_ref = ws.cell(row=growth_rate_row, column=col).coordinate
                        cell.value = f'={prev_orders_cell_ref} * (1 + {growth_rate_cell_ref})'
                elif label == "Order Growth Rate":
                    cell.value = scenario_data['growth_rates'][year_offset]
                elif label == "Average Order Value":
                    cell.value = scenario_data['avg_order_value']
                elif label == "Manufacturing":
                    cell.value = scenario_data['manuf_cost']
                elif label == "Order Fulfillment":
                    cell.value = scenario_data['order_fulfil_cost']
                elif label == "Warehouse Rent":
                    cell.value = scenario_data['warehouse_rent'][year_offset]
                elif label == "Salaries & Payroll":
                    cell.value = scenario_data['salaries_payroll'][year_offset]
                elif label == "Marketing":
                    cell.value = scenario_data['marketing'][year_offset]
                elif label == "Other":
                    cell.value = scenario_data['other']
                elif label == "Corporate Tax Rate":
                    cell.value = scenario_data['corp_tax_rate']

                if not is_live_case and label not in ["Revenue", "Cost of Goods Sold (per order)", "Operating Expenses"] and ws.cell(row=current_row, column=col).value is not None and not isinstance(ws.cell(row=current_row, column=col).value, str) and not ws.cell(row=current_row, column=col).value.startswith('='):
                    cell.font = font_input # Hard-coded numbers in scenario tables are blue

                if num_format:
                    cell.number_format = num_format
            current_line_offset += 1 # Increment for the next line in the structure

    # --- Scenario Data Dictionaries ---
    scenario1_data = {
        'num_orders_start': s1_num_orders_start, 'growth_rates': s1_growth_rates, 'avg_order_value': s1_avg_order_value,
        'manuf_cost': s1_manuf_cost, 'order_fulfil_cost': s1_order_fulfil_cost,
        'warehouse_rent': s1_warehouse_rent, 'salaries_payroll': s1_salaries_payroll,
        'marketing': s1_marketing, 'other': s1_other, 'corp_tax_rate': s1_corp_tax_rate
    }
    scenario2_data = {
        'num_orders_start': s2_num_orders_start, 'growth_rates': s2_growth_rates, 'avg_order_value': s2_avg_order_value,
        'manuf_cost': s2_manuf_cost, 'order_fulfil_cost': s2_order_fulfil_cost,
        'warehouse_rent': s2_warehouse_rent, 'salaries_payroll': s2_salaries_payroll,
        'marketing': s2_marketing, 'other': s2_other, 'corp_tax_rate': s2_corp_tax_rate
    }

    # --- Render Assumption Blocks ---
    create_assumption_block(anchor_row, "Live Case", scenario1_data, is_live_case=True) # Data source is arbitrary here as formulas override

    s1_start_row = anchor_row + 18 # B46
    create_assumption_block(s1_start_row, "Upper Case (Scenario 1)", scenario1_data)

    s2_start_row = anchor_row + 36 # B64
    create_assumption_block(s2_start_row, "Lower Case (Scenario 2)", scenario2_data)

    # --- Basic Income Statement (Simplified for context) ---
    inc_stmt_start_row = 3
    ws.cell(row=inc_stmt_start_row, column=anchor_col).value = "Income Statement"
    ws.cell(row=inc_stmt_start_row, column=anchor_col).font = font_bold
    ws.cell(row=inc_stmt_start_row, column=anchor_col).fill = header_fill
    ws.merge_cells(start_row=inc_stmt_start_row, end_row=inc_stmt_start_row, start_column=anchor_col, end_column=anchor_col+7)

    # Years row
    years_row = inc_stmt_start_row + 1
    years = [2023, 2024, 2025, 2026, 2027]
    for i, year in enumerate(years):
        col = anchor_col + 2 + i
        ws.cell(row=years_row, column=col).value = year
        ws.cell(row=years_row, column=col).font = font_bold
        ws.cell(row=years_row, column=col).fill = header_fill
        ws.cell(row=years_row, column=col).alignment = Alignment(horizontal='center')

    # References to Live Case assumptions
    live_num_orders_row = anchor_row + 1 # B29:H29
    live_avg_order_value_row = anchor_row + 3 # B31:H31
    live_manuf_cost_row = anchor_row + 6 # B34:H34
    live_order_ful_cost_row = anchor_row + 7 # B35:H35
    live_warehouse_rent_row = anchor_row + 10 # B38:H38
    live_salaries_payroll_row = anchor_row + 11 # B39:H39
    live_marketing_row = anchor_row + 12 # B40:H40
    live_other_row = anchor_row + 13 # B41:H41
    live_corp_tax_rate_row = anchor_row + 15 # B43:H43

    # Revenue
    rev_row_is = years_row + 1
    ws.cell(row=rev_row_is, column=anchor_col).value = "Revenue"
    ws.cell(row=rev_row_is, column=anchor_col).font = font_normal
    for i in range(5):
        col = anchor_col + 2 + i # D to H
        ws.cell(row=rev_row_is, column=col).value = f'={ws.cell(row=live_num_orders_row, column=col).coordinate} * {ws.cell(row=live_avg_order_value_row, column=col).coordinate}'
        ws.cell(row=rev_row_is, column=col).number_format = '#,##0'

    # Manufacturing COGS
    manuf_cogs_row_is = rev_row_is + 2
    ws.cell(row=manuf_cogs_row_is, column=anchor_col).value = "Manufacturing"
    ws.cell(row=manuf_cogs_row_is, column=anchor_col).font = font_normal
    for i in range(5):
        col = anchor_col + 2 + i
        ws.cell(row=manuf_cogs_row_is, column=col).value = f'=${ws.cell(row=live_num_orders_row, column=col).coordinate} * {ws.cell(row=live_manuf_cost_row, column=col).coordinate}'
        ws.cell(row=manuf_cogs_row_is, column=col).number_format = '#,##0'

    # Order Fulfillment COGS
    order_ful_cogs_row_is = manuf_cogs_row_is + 1
    ws.cell(row=order_ful_cogs_row_is, column=anchor_col).value = "Order Fulfillment"
    ws.cell(row=order_ful_cogs_row_is, column=anchor_col).font = font_normal
    for i in range(5):
        col = anchor_col + 2 + i
        ws.cell(row=order_ful_cogs_row_is, column=col).value = f'=${ws.cell(row=live_num_orders_row, column=col).coordinate} * {ws.cell(row=live_order_ful_cost_row, column=col).coordinate}'
        ws.cell(row=order_ful_cogs_row_is, column=col).number_format = '#,##0'

    # Total COGS
    total_cogs_row_is = order_ful_cogs_row_is + 2
    ws.cell(row=total_cogs_row_is, column=anchor_col).value = "Total COGS"
    ws.cell(row=total_cogs_row_is, column=anchor_col).font = font_bold
    for i in range(5):
        col = anchor_col + 2 + i
        ws.cell(row=total_cogs_row_is, column=col).value = f'=SUM({ws.cell(row=manuf_cogs_row_is, column=col).coordinate}:{ws.cell(row=order_ful_cogs_row_is, column=col).coordinate})'
        ws.cell(row=total_cogs_row_is, column=col).number_format = '#,##0'

    # Gross Profit
    gross_profit_row_is = total_cogs_row_is + 2
    ws.cell(row=gross_profit_row_is, column=anchor_col).value = "Gross Profit"
    ws.cell(row=gross_profit_row_is, column=anchor_col).font = font_bold
    for i in range(5):
        col = anchor_col + 2 + i
        ws.cell(row=gross_profit_row_is, column=col).value = f'={ws.cell(row=rev_row_is, column=col).coordinate} - {ws.cell(row=total_cogs_row_is, column=col).coordinate}'
        ws.cell(row=gross_profit_row_is, column=col).number_format = '#,##0'

    # Operating Expenses - fixed (linked to Live Case assumptions)
    op_exp_start_row_is = gross_profit_row_is + 4
    op_exp_labels_is = ["Warehouse Rent", "Salaries & Payroll", "Marketing", "Other"]
    live_case_op_exp_rows = [live_warehouse_rent_row, live_salaries_payroll_row, live_marketing_row, live_other_row]

    for i, label in enumerate(op_exp_labels_is):
        current_row = op_exp_start_row_is + i
        ws.cell(row=current_row, column=anchor_col).value = label
        ws.cell(row=current_row, column=anchor_col).font = font_normal
        for j in range(5):
            col = anchor_col + 2 + j
            ws.cell(row=current_row, column=col).value = f'={ws.cell(row=live_case_op_exp_rows[i], column=col).coordinate}'
            ws.cell(row=current_row, column=col).number_format = '#,##0'

    # Total Operating Expenses
    total_op_exp_row_is = op_exp_start_row_is + len(op_exp_labels_is) + 1
    ws.cell(row=total_op_exp_row_is, column=anchor_col).value = "Total Operating Expenses"
    ws.cell(row=total_op_exp_row_is, column=anchor_col).font = font_bold
    for i in range(5):
        col = anchor_col + 2 + i
        ws.cell(row=total_op_exp_row_is, column=col).value = f'=SUM({ws.cell(row=op_exp_start_row_is, column=col).coordinate}:{ws.cell(row=op_exp_start_row_is + len(op_exp_labels_is) - 1, column=col).coordinate})'
        ws.cell(row=total_op_exp_row_is, column=col).number_format = '#,##0'

    # Operating Profit
    op_profit_row_is = total_op_exp_row_is + 2
    ws.cell(row=op_profit_row_is, column=anchor_col).value = "Operating Profit"
    ws.cell(row=op_profit_row_is, column=anchor_col).font = font_bold
    for i in range(5):
        col = anchor_col + 2 + i
        ws.cell(row=op_profit_row_is, column=col).value = f'={ws.cell(row=gross_profit_row_is, column=col).coordinate} - {ws.cell(row=total_op_exp_row_is, column=col).coordinate}'
        ws.cell(row=op_profit_row_is, column=col).number_format = '#,##0'

    # Corporate Tax
    corp_tax_row_is = op_profit_row_is + 3
    ws.cell(row=corp_tax_row_is, column=anchor_col).value = "Corporate Tax"
    ws.cell(row=corp_tax_row_is, column=anchor_col).font = font_normal
    for i in range(5):
        col = anchor_col + 2 + i
        op_profit_cell_ref = ws.cell(row=op_profit_row_is, column=col).coordinate
        tax_rate_cell_ref = ws.cell(row=live_corp_tax_rate_row, column=col).coordinate # Dynamic tax rate
        ws.cell(row=corp_tax_row_is, column=col).value = f'=IF({op_profit_cell_ref}<0,"NA",{op_profit_cell_ref}*{tax_rate_cell_ref})'
        ws.cell(row=corp_tax_row_is, column=col).number_format = '#,##0'

    # Profit / (Loss)
    profit_loss_row_is = corp_tax_row_is + 1
    ws.cell(row=profit_loss_row_is, column=anchor_col).value = "Profit / (Loss)"
    ws.cell(row=profit_loss_row_is, column=anchor_col).font = font_bold
    ws.cell(row=profit_loss_row_is, column=anchor_col).fill = accent_fill
    ws.merge_cells(start_row=profit_loss_row_is, end_row=profit_loss_row_is, start_column=anchor_col, end_column=anchor_col+1)
    for i in range(5):
        col = anchor_col + 2 + i
        op_profit_cell_ref = ws.cell(row=op_profit_row_is, column=col).coordinate
        corp_tax_cell_ref = ws.cell(row=corp_tax_row_is, column=col).coordinate
        ws.cell(row=profit_loss_row_is, column=col).value = f'=IFERROR({op_profit_cell_ref}-{corp_tax_cell_ref},{op_profit_cell_ref})'
        ws.cell(row=profit_loss_row_is, column=col).number_format = '#,##0'

    # Set column widths for readability
    ws.column_dimensions[openpyxl.utils.get_column_letter(anchor_col)].width = 25
    for col_offset in range(1, 8):
        ws.column_dimensions[openpyxl.utils.get_column_letter(anchor_col + col_offset)].width = 15

```