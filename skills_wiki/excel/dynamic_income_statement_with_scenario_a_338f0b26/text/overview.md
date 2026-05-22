### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Income Statement with Scenario Analysis

*   **Tier**: sheet_shell
*   **Core Mechanism**: This skill constructs a complete Income Statement and an underlying Assumptions section on a single Excel sheet. It implements dynamic scenario analysis by creating multiple sets of assumptions (e.g., "Upper Case" and "Lower Case") and using the `CHOOSE` function, linked to a Data Validation dropdown, to dynamically select which set of assumptions drives the "Live Case" section and, consequently, the entire Income Statement.
*   **Applicability**: This is ideal for financial modeling, business planning, or any scenario where a report's outputs need to be viewed under different input conditions (e.g., optimistic vs. pessimistic sales forecasts, varying cost structures). It's suitable for multi-year financial forecasts for businesses of any size.

### 2. Structural Breakdown

-   **Data Layout**:
    *   **Income Statement**: Rows 3-26, Columns B-H. Includes Revenue, COGS (Manufacturing, Order Fulfillment, Total COGS), Gross Profit, Operating Expenses (Warehouse Rent, Salaries & Payroll, Marketing, Other, Total Operating Expenses), Operating Profit, Corporate Tax, and Profit/(Loss).
    *   **Live Case Assumptions**: Rows 29-44, Columns B-H. This block contains the currently selected assumptions, driven by `CHOOSE` formulas.
    *   **Upper Case (Scenario 1) Assumptions**: Rows 47-62, Columns B-H. Contains the optimistic hard-coded assumptions.
    *   **Lower Case (Scenario 2) Assumptions**: Rows 65-80, Columns B-H. Contains the pessimistic hard-coded assumptions.
    *   **Scenario Selector**: Cell J4. A single cell dropdown to select between "1" (Upper Case) and "2" (Lower Case).
-   **Formula Logic**:
    *   **Revenue (Live Case, D30)**: `=CHOOSE($J$4,D48,D66)` (and similarly for other dynamic assumption cells, adjusting cell references).
    *   **Number of Orders (Live Case, E30)**: `=D30*(1+E31)` (and drag across for growth).
    *   **Revenue (Income Statement, D5)**: `=D30*D32` (Number of Orders * Average Order Value from Live Case).
    *   **Manufacturing (Income Statement, D7)**: `=D30*D35` (Number of Orders * Manufacturing Cost from Live Case).
    *   **Total COGS (D10)**: `=SUM(D7:D8)`.
    *   **Gross Profit (D11)**: `=D5-D10`.
    *   **Gross Profit Margin (D12)**: `=D11/D5`.
    *   **Operating Expenses (D15:D18)**: Direct links to the respective cells in the Live Case Assumptions (e.g., `=D39` for Warehouse Rent).
    *   **Total Operating Expenses (D19)**: `=SUM(D15:D18)`.
    *   **Operating Profit (D21)**: `=D11-D19`.
    *   **Operating Profit Margin (D22)**: `=D21/D5`.
    *   **Corporate Tax (D24)**: `=IF(D21<0,"NA",D21*D44)`. This conditional formula ensures tax is only applied on positive profit.
    *   **Profit / (Loss) (D25)**: `=IFERROR(D21-D24,D21)`. Handles potential "#VALUE!" errors from "NA" in Corporate Tax.
-   **Visual Design**:
    *   **Headers (Income Statement, Assumptions)**: Dark blue background (`header_bg`), white font (`header_fg`), bold.
    *   **Years (2023-2027)**: Dark blue background, white font, bold.
    *   **Hard-coded inputs (Scenario 1 & 2 blocks)**: Blue font, no fill.
    *   **Dynamic inputs (Live Case block)**: Black font, no fill.
    *   **Values (Income Statement)**: Black font, no fill (except for yellow highlighting on "Profit/(Loss)").
    *   **Profit/(Loss) (Income Statement)**: Yellow background, bold.
    *   **Scenario Selector (J4)**: Yellow background, bold, all borders, centered.
    *   **Borders**: Thin gray borders for all tables.
-   **Charts/Tables**: No specific charts or Excel tables (as in `Table` object) are created by this skill, but the model outputs data suitable for charting.
-   **Theme Hooks**:
    *   `header_bg`: Used for main headers and year headers.
    *   `header_fg`: Used for main header and year header text.
    *   `highlight_bg`: Used for the scenario selector cell and profit/loss line.
    *   `border_color`: Used for table borders.
    *   `text_color_normal`: Used for dynamic formula results.
    *   `text_color_accent_1`: Used for hard-coded inputs in scenario blocks (representing blue).

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# Assuming _helpers.py is available for theme loading and basic styling
# For the purpose of this self-contained skill, I'll include necessary helper parts.

class Theme:
    def __init__(self, name="corporate_blue"):
        self.name = name
        self._palette = self._load_palette(name)

    def _load_palette(self, name):
        # Simplified palette loading, for a full implementation see _helpers.py
        if name == "corporate_blue":
            return {
                "header_bg": "FF2E4C6D",  # Dark Blue
                "header_fg": "FFFFFFFF",  # White
                "highlight_bg": "FFFFFF00", # Yellow
                "border_color": "FFD9D9D9", # Light Gray
                "text_color_normal": "FF000000", # Black
                "text_color_accent_1": "FF0000FF", # Blue (for hard-coded inputs)
                "text_color_negative": "FFFF0000" # Red
            }
        else: # Default or other themes can be added
            return {
                "header_bg": "FF2E4C6D",
                "header_fg": "FFFFFFFF",
                "highlight_bg": "FFFFFF00",
                "border_color": "FFD9D9D9",
                "text_color_normal": "FF000000",
                "text_color_accent_1": "FF0000FF",
                "text_color_negative": "FFFF0000"
            }

    def get_fill(self, key):
        hex_color = self._palette.get(key, "FFFFFFFF")
        return PatternFill(start_color=hex_color[2:], end_color=hex_color[2:], fill_type="solid")

    def get_font(self, key, bold=False):
        hex_color = self._palette.get(key, "FF000000")
        return Font(color=hex_color[2:], bold=bold)

    def get_border(self):
        side = Side(border_style="thin", color=self._palette.get("border_color")[2:])
        return Border(left=side, right=side, top=side, bottom=side)

    def get_outside_border(self):
        side = Side(border_style="medium", color=self._palette.get("border_color")[2:])
        return Border(left=side, right=side, top=side, bottom=side)

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", start_year: int = 2023, num_years: int = 5, **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    current_theme = Theme(theme)

    # --- Configuration ---
    YEARS = [start_year + i for i in range(num_years)]
    COL_START = 2 # Column B
    ROW_START = 1 # Row 1

    # --- Scenario Data ---
    # Optimistic Scenario 1 (Upper Case)
    scenario1_data = {
        "Number of Orders": 3000,
        "Order Growth Rate": [1.00, 0.75, 0.50, 0.35], # Year 2-5 growth rates
        "Average Order Value": 39.95,
        "Manufacturing": 6.50,
        "Order Fulfillment": 2.25,
        "Warehouse Rent": [20000, 30000, 30000, 30000, 30000],
        "Salaries & Payroll": [50000, 100000, 100000, 100000, 100000],
        "Marketing": [25000, 50000, 100000, 100000, 100000],
        "Other": 5000,
        "Corporate Tax Rate": 0.20
    }
    # Pessimistic Scenario 2 (Lower Case)
    scenario2_data = {
        "Number of Orders": 2000,
        "Order Growth Rate": [1.00, 0.75, 0.50, 0.35],
        "Average Order Value": 34.95,
        "Manufacturing": 8.00,
        "Order Fulfillment": 2.25,
        "Warehouse Rent": [20000, 30000, 30000, 30000, 30000],
        "Salaries & Payroll": [50000, 100000, 100000, 100000, 100000],
        "Marketing": [25000, 50000, 100000, 100000, 100000],
        "Other": 5000,
        "Corporate Tax Rate": 0.25
    }

    # --- Setup Headers and Years ---
    ws.cell(row=ROW_START + 2, column=COL_START).value = "Figures in USD"
    ws.cell(row=ROW_START + 2, column=COL_START).font = current_theme.get_font("header_fg", bold=True)
    ws.cell(row=ROW_START + 2, column=COL_START).fill = current_theme.get_fill("header_bg")
    ws.cell(row=ROW_START + 2, column=COL_START + 1).value = "Unit"
    ws.cell(row=ROW_START + 2, column=COL_START + 1).font = current_theme.get_font("header_fg", bold=True)
    ws.cell(row=ROW_START + 2, column=COL_START + 1).fill = current_theme.get_fill("header_bg")

    for i, year in enumerate(YEARS):
        col_idx = COL_START + 2 + i
        ws.cell(row=ROW_START + 2, column=col_idx).value = year
        ws.cell(row=ROW_START + 2, column=col_idx).font = current_theme.get_font("header_fg", bold=True)
        ws.cell(row=ROW_START + 2, column=col_idx).fill = current_theme.get_fill("header_bg")
        # For Income Statement Years (e.g., 2023, Year 1)
        ws.cell(row=ROW_START + 3, column=col_idx).value = f"Year {i+1}"
        ws.cell(row=ROW_START + 3, column=col_idx).font = current_theme.get_font("header_fg", bold=True)
        ws.cell(row=ROW_START + 3, column=col_idx).fill = current_theme.get_fill("header_bg")
    
    # Set column widths
    ws.column_dimensions[get_column_letter(COL_START)].width = 25
    for i in range(num_years + 1):
        ws.column_dimensions[get_column_letter(COL_START + 1 + i)].width = 15

    # --- Income Statement Structure ---
    is_start_row = ROW_START + 4 # Row 5

    income_statement_items = [
        {"label": "Income Statement", "row": is_start_row - 1, "style": "header"},
        {"label": "Revenue", "row": is_start_row, "unit": "$", "formula": "=D{order_num_row}*D{avg_order_val_row}"},
        {"label": "Cost of Goods Sold", "row": is_start_row + 1, "style": "subheader"},
        {"label": "Manufacturing", "row": is_start_row + 2, "unit": "$", "formula": "=D{order_num_row}*D{manufacturing_row}"},
        {"label": "Order Fulfillment", "row": is_start_row + 3, "unit": "$", "formula": "=D{order_num_row}*D{order_fulfillment_row}"},
        {"label": "Total COGS", "row": is_start_row + 5, "unit": "$", "formula": "=SUM(D{mf_row}:D{of_row})"},
        {"label": "Gross Profit", "row": is_start_row + 7, "unit": "$", "formula": "=D{revenue_row}-D{total_cogs_row}"},
        {"label": "Gross Profit Margin", "row": is_start_row + 8, "unit": "%", "formula": "=D{gross_profit_row}/D{revenue_row}"},
        {"label": "Operating Expenses", "row": is_start_row + 10, "style": "subheader"},
        {"label": "Warehouse Rent", "row": is_start_row + 11, "unit": "$", "formula": "=D{warehouse_rent_row}"},
        {"label": "Salaries & Payroll", "row": is_start_row + 12, "unit": "$", "formula": "=D{salaries_row}"},
        {"label": "Marketing", "row": is_start_row + 13, "unit": "$", "formula": "=D{marketing_row}"},
        {"label": "Other", "row": is_start_row + 14, "unit": "$", "formula": "=D{other_row}"},
        {"label": "Total Operating Expenses", "row": is_start_row + 16, "unit": "$", "formula": "=SUM(D{warehouse_rent_is}:D{other_is})"},
        {"label": "Operating Profit", "row": is_start_row + 18, "unit": "$", "formula": "=D{revenue_row}-D{total_cogs_row}-D{total_opex_row}"},
        {"label": "Operating Profit Margin", "row": is_start_row + 19, "unit": "%", "formula": "=D{operating_profit_row}/D{revenue_row}"},
        {"label": "Corporate Tax", "row": is_start_row + 21, "unit": "$", "formula": "=IF(D{operating_profit_row_val}<0,\"NA\",D{operating_profit_row_val}*D{corp_tax_rate_row})"},
        {"label": "Profit / (Loss)", "row": is_start_row + 22, "unit": "$", "formula": "=IFERROR(D{operating_profit_row_val_for_pl}-D{corporate_tax_row_val},D{operating_profit_row_val_for_pl})", "style": "highlight"}
    ]

    # Map assumptions rows in Live Case
    live_assumptions_row = ROW_START + 29 -1 # B29
    live_assumptions_map = {
        "Assumptions": live_assumptions_row,
        "Revenue": live_assumptions_row + 1,
        "Number of Orders": live_assumptions_row + 2,
        "Order Growth Rate": live_assumptions_row + 3,
        "Average Order Value": live_assumptions_row + 4,
        "Cost of Goods Sold": live_assumptions_row + 5,
        "Manufacturing": live_assumptions_row + 6,
        "Order Fulfillment": live_assumptions_row + 7,
        "Operating Expenses": live_assumptions_row + 8,
        "Warehouse Rent": live_assumptions_row + 9,
        "Salaries & Payroll": live_assumptions_row + 10,
        "Marketing": live_assumptions_row + 11,
        "Other": live_assumptions_row + 12,
        "Corporate Tax Rate": live_assumptions_row + 14
    }

    # Render Income Statement labels and units
    for item in income_statement_items:
        row = item["row"]
        col = COL_START
        ws.cell(row=row, column=col).value = item["label"]
        ws.cell(row=row, column=col).font = current_theme.get_font("text_color_normal", bold=(item.get("style") == "subheader" or item.get("style") == "highlight"))
        
        if item.get("unit"):
            ws.cell(row=row, column=col + 1).value = item["unit"]
            ws.cell(row=row, column=col + 1).font = current_theme.get_font("text_color_normal")
        
        if item.get("style") == "header":
            ws.cell(row=row, column=col).font = current_theme.get_font("header_fg", bold=True)
            ws.cell(row=row, column=col).fill = current_theme.get_fill("header_bg")
            ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + num_years + 1)
        if item.get("style") == "highlight":
            for c in range(col, col + num_years + 2):
                ws.cell(row=row, column=c).fill = current_theme.get_fill("highlight_bg")

    # --- Scenario Selector ---
    scenario_selector_col = COL_START + num_years + 2 # Column J
    scenario_selector_row = ROW_START + 3 # Row 4
    ws.cell(row=scenario_selector_row, column=scenario_selector_col - 1).value = "Scenario"
    ws.cell(row=scenario_selector_row, column=scenario_selector_col - 1).font = current_theme.get_font("text_color_normal", bold=True)
    ws.cell(row=scenario_selector_row, column=scenario_selector_col - 1).alignment = Alignment(horizontal='right')
    
    ws.cell(row=scenario_selector_row, column=scenario_selector_col).value = 1 # Default to Scenario 1
    ws.cell(row=scenario_selector_row, column=scenario_selector_col).font = current_theme.get_font("text_color_normal", bold=True)
    ws.cell(row=scenario_selector_row, column=scenario_selector_col).fill = current_theme.get_fill("highlight_bg")
    ws.cell(row=scenario_selector_row, column=scenario_selector_col).border = current_theme.get_border()
    ws.cell(row=scenario_selector_row, column=scenario_selector_col).alignment = Alignment(horizontal='center')

    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    dv.add(ws.cell(row=scenario_selector_row, column=scenario_selector_col))
    ws.add_data_validation(dv)
    
    # --- Assumption Blocks (Live Case, Scenario 1, Scenario 2) ---
    assumption_block_structure = [
        {"label": "Assumptions", "type": "header"},
        {"label": "Revenue", "type": "subheader"},
        {"label": "Number of Orders", "unit": "#", "scenario_data_key": "Number of Orders", "output_format": "number"},
        {"label": "Order Growth Rate", "unit": "%", "scenario_data_key": "Order Growth Rate", "output_format": "percentage_growth_rate", "offset_year": 1},
        {"label": "Average Order Value", "unit": "$", "scenario_data_key": "Average Order Value", "output_format": "currency"},
        {"label": "Cost of Goods Sold (per order)", "type": "subheader"},
        {"label": "Manufacturing", "unit": "$", "scenario_data_key": "Manufacturing", "output_format": "currency"},
        {"label": "Order Fulfillment", "unit": "$", "scenario_data_key": "Order Fulfillment", "output_format": "currency"},
        {"label": "Operating Expenses", "type": "subheader"},
        {"label": "Warehouse Rent", "unit": "$", "scenario_data_key": "Warehouse Rent", "output_format": "currency_no_decimal"},
        {"label": "Salaries & Payroll", "unit": "$", "scenario_data_key": "Salaries & Payroll", "output_format": "currency_no_decimal"},
        {"label": "Marketing", "unit": "$", "scenario_data_key": "Marketing", "output_format": "currency_no_decimal"},
        {"label": "Other", "unit": "$", "scenario_data_key": "Other", "output_format": "currency_no_decimal"},
        {"label": "Corporate Tax Rate", "unit": "%", "scenario_data_key": "Corporate Tax Rate", "output_format": "percentage"}
    ]

    # Define starting rows for each assumption block
    live_case_start_row = is_start_row + 24 # B29
    scenario1_start_row = live_case_start_row + len(assumption_block_structure) + 3 # B47
    scenario2_start_row = scenario1_start_row + len(assumption_block_structure) + 3 # B65

    assumption_blocks = [
        {"name": "Live Case", "start_row": live_case_start_row, "font_color": "text_color_normal", "dynamic": True},
        {"name": "Upper Case (Scenario 1)", "start_row": scenario1_start_row, "font_color": "text_color_accent_1", "data": scenario1_data},
        {"name": "Lower Case (Scenario 2)", "start_row": scenario2_start_row, "font_color": "text_color_accent_1", "data": scenario2_data}
    ]
    
    # Helper for formatting values
    def format_cell(cell, value, output_format):
        if output_format == "number":
            cell.value = value
            cell.number_format = '#,##0'
        elif output_format == "percentage":
            cell.value = value
            cell.number_format = '0%'
        elif output_format == "percentage_growth_rate":
            cell.value = value
            cell.number_format = '0%'
        elif output_format == "currency":
            cell.value = value
            cell.number_format = '$#,##0.00'
        elif output_format == "currency_no_decimal":
            cell.value = value
            cell.number_format = '$#,##0'


    for block_info in assumption_blocks:
        start_row = block_info["start_row"]
        ws.cell(row=start_row, column=COL_START).value = block_info["name"]
        ws.cell(row=start_row, column=COL_START).font = current_theme.get_font("header_fg", bold=True)
        ws.cell(row=start_row, column=COL_START).fill = current_theme.get_fill("header_bg")
        ws.merge_cells(start_row=start_row, start_column=COL_START, end_row=start_row, end_column=COL_START + num_years + 1)
        ws.cell(row=start_row, column=COL_START).border = current_theme.get_outside_border()

        current_row_offset = 0
        for item in assumption_block_structure[1:]: # Skip "Assumptions" header
            current_row_offset += 1
            row_idx = start_row + current_row_offset
            ws.cell(row=row_idx, column=COL_START).value = item["label"]
            ws.cell(row=row_idx, column=COL_START).font = current_theme.get_font(block_info["font_color"], bold=(item["type"] == "subheader"))
            ws.cell(row=row_idx, column=COL_START).border = current_theme.get_border()
            
            if item.get("unit"):
                ws.cell(row=row_idx, column=COL_START + 1).value = item["unit"]
                ws.cell(row=row_idx, column=COL_START + 1).font = current_theme.get_font(block_info["font_color"])
                ws.cell(row=row_idx, column=COL_START + 1).border = current_theme.get_border()
            
            if item["type"] == "subheader":
                ws.merge_cells(start_row=row_idx, start_column=COL_START, end_row=row_idx, end_column=COL_START + num_years + 1)
                ws.cell(row=row_idx, column=COL_START).font = current_theme.get_font("text_color_normal", bold=True)
                ws.cell(row=row_idx, column=COL_START).border = current_theme.get_outside_border()
                continue
            
            if block_info.get("dynamic"): # Live Case
                # Cell references for scenarios
                s1_cell_ref_base = f"{get_column_letter(COL_START + 2)}{scenario1_start_row + current_row_offset}"
                s2_cell_ref_base = f"{get_column_letter(COL_START + 2)}{scenario2_start_row + current_row_offset}"
                scenario_selector_ref = f"${get_column_letter(scenario_selector_col)}${scenario_selector_row}"

                # Fill for Year 1 (D column)
                formula_y1 = f"=CHOOSE({scenario_selector_ref},{s1_cell_ref_base},{s2_cell_ref_base})"
                ws.cell(row=row_idx, column=COL_START + 2).value = formula_y1
                ws.cell(row=row_idx, column=COL_START + 2).font = current_theme.get_font(block_info["font_color"])
                ws.cell(row=row_idx, column=COL_START + 2).border = current_theme.get_border()
                format_cell(ws.cell(row=row_idx, column=COL_START + 2), None, item["output_format"])

                # Handle growth rates for subsequent years in Live Case
                if item["output_format"] == "percentage_growth_rate":
                    for y_offset in range(1, num_years): # For Year 2 to Year 5
                        col = COL_START + 2 + y_offset
                        s1_cell_ref = f"{get_column_letter(COL_START + 2 + y_offset)}{scenario1_start_row + current_row_offset}"
                        s2_cell_ref = f"{get_column_letter(COL_START + 2 + y_offset)}{scenario2_start_row + current_row_offset}"
                        formula_growth = f"=CHOOSE({scenario_selector_ref},{s1_cell_ref},{s2_cell_ref})"
                        ws.cell(row=row_idx, column=col).value = formula_growth
                        ws.cell(row=row_idx, column=col).font = current_theme.get_font(block_info["font_color"])
                        ws.cell(row=row_idx, column=col).border = current_theme.get_border()
                        format_cell(ws.cell(row=row_idx, column=col), None, item["output_format"])
                elif item["output_format"] in ["currency", "currency_no_decimal", "number"]: # For fixed values dragged across
                    for y_offset in range(1, num_years):
                        col = COL_START + 2 + y_offset
                        s1_cell_ref = f"{get_column_letter(COL_START + 2 + y_offset)}{scenario1_start_row + current_row_offset}"
                        s2_cell_ref = f"{get_column_letter(COL_START + 2 + y_offset)}{scenario2_start_row + current_row_offset}"
                        formula_fixed = f"=CHOOSE({scenario_selector_ref},{s1_cell_ref},{s2_cell_ref})"
                        ws.cell(row=row_idx, column=col).value = formula_fixed
                        ws.cell(row=row_idx, column=col).font = current_theme.get_font(block_info["font_color"])
                        ws.cell(row=row_idx, column=col).border = current_theme.get_border()
                        format_cell(ws.cell(row=row_idx, column=col), None, item["output_format"])


            else: # Scenario 1 and Scenario 2 hard-coded values
                value = block_info["data"].get(item["scenario_data_key"])
                if isinstance(value, list): # For growth rates, opex that change per year
                    format_cell(ws.cell(row=row_idx, column=COL_START + 2), value[0], item["output_format"])
                    for y_offset in range(1, num_years):
                        format_cell(ws.cell(row=row_idx, column=COL_START + 2 + y_offset), value[y_offset], item["output_format"])
                else: # For single fixed values
                    for y_offset in range(num_years):
                        format_cell(ws.cell(row=row_idx, column=COL_START + 2 + y_offset), value, item["output_format"])
                
                # Apply blue font to hard-coded values
                for y_offset in range(num_years):
                    ws.cell(row=row_idx, column=COL_START + 2 + y_offset).font = current_theme.get_font(block_info["font_color"])
                    ws.cell(row=row_idx, column=COL_START + 2 + y_offset).border = current_theme.get_border()


    # --- Populate Income Statement Formulas ---
    for item in income_statement_items:
        if item.get("formula"):
            for i in range(num_years):
                col = COL_START + 2 + i
                formula_str = item["formula"]
                
                # Dynamic cell references based on Live Case Assumptions
                formula_str = formula_str.format(
                    revenue_row=is_start_row,
                    order_num_row=live_assumptions_map["Number of Orders"],
                    avg_order_val_row=live_assumptions_map["Average Order Value"],
                    manufacturing_row=live_assumptions_map["Manufacturing"],
                    order_fulfillment_row=live_assumptions_map["Order Fulfillment"],
                    total_cogs_row=is_start_row + 5,
                    gross_profit_row=is_start_row + 7,
                    operating_profit_row=is_start_row + 18,
                    operating_profit_row_val=is_start_row + 18,
                    operating_profit_row_val_for_pl=is_start_row + 18, # For profit/loss calculation
                    corporate_tax_row_val=is_start_row + 21,
                    warehouse_rent_row=live_assumptions_map["Warehouse Rent"],
                    salaries_row=live_assumptions_map["Salaries & Payroll"],
                    marketing_row=live_assumptions_map["Marketing"],
                    other_row=live_assumptions_map["Other"],
                    warehouse_rent_is=is_start_row + 11,
                    salaries_is=is_start_row + 12,
                    marketing_is=is_start_row + 13,
                    other_is=is_start_row + 14,
                    total_opex_row=is_start_row + 16,
                    corp_tax_rate_row=live_assumptions_map["Corporate Tax Rate"]
                )
                # Adjust column for formulas that reference previous year (e.g., growth)
                if formula_str.count("D{order_num_row}*") == 1 and i > 0:
                    formula_str = formula_str.replace(f"D{live_assumptions_map['Number of Orders']}", f"{get_column_letter(col-1)}{live_assumptions_map['Number of Orders']}")
                    
                # Fix all column letters for the current year
                for ref_col in range(COL_START + 2, COL_START + 2 + num_years):
                    formula_str = formula_str.replace(f"{get_column_letter(ref_col)}", f"{get_column_letter(col)}")

                ws.cell(row=item["row"], column=col).value = formula_str
                ws.cell(row=item["row"], column=col).font = current_theme.get_font("text_color_normal")
                ws.cell(row=item["row"], column=col).border = current_theme.get_border()

                # Apply number formats
                if item["unit"] == "$":
                    ws.cell(row=item["row"], column=col).number_format = '$#,##0'
                elif item["unit"] == "%":
                    ws.cell(row=item["row"], column=col).number_format = '0%'
                
                # Handle NA for Corporate Tax explicitly
                if item["label"] == "Corporate Tax":
                     ws.cell(row=item["row"], column=col).number_format = '#,##0;[RED]-#,##0;"NA"'

                # Conditional formatting for negative operating profit
                if item["label"] == "Operating Profit":
                    ws.conditional_formatting.add(f"{get_column_letter(col)}{item['row']}", 
                                                  CellIsRule(operator='lessThan', formula=[0], 
                                                             fill=PatternFill(start_color=current_theme.get_font("text_color_negative").color.rgb[2:], 
                                                                              end_color=current_theme.get_font("text_color_negative").color.rgb[2:], fill_type="solid"),
                                                             font=current_theme.get_font("text_color_negative")))


    # --- Final Touches ---
    ws.freeze_panes = ws.cell(row=ROW_START + 4, column=COL_START + 2) # Freeze panes below headers and year column
    
```