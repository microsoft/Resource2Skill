### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Assumptions with CHOOSE and Data Validation

*   **Tier**: component
*   **Core Mechanism**: This skill constructs a dynamic assumption section within an Excel worksheet. It enables users to seamlessly switch between predefined scenarios (e.g., "Upper Case," "Lower Case") by interacting with a data validation dropdown. The `CHOOSE` function dynamically fetches the relevant assumption values from hidden scenario tables, causing the associated financial model (or any dependent calculations) to update in real-time based on the selected scenario.
*   **Applicability**: This component is ideal for financial modeling, business forecasting, and analytical reports where the impact of varying input assumptions (e.g., best-case, worst-case, base-case scenarios) needs to be visualized instantly. It requires at least two distinct, pre-defined sets of input assumptions to operate effectively.

### 2. Structural Breakdown

-   **Data Layout**:
    *   **Live Case Assumptions**: A block of cells (e.g., B29:H44 in the video) where the actual formulas reside. These cells reference the chosen scenario.
    *   **Scenario Selector**: A single cell (e.g., J4 in the video) houses a data validation dropdown for selecting scenario numbers (e.g., 1 or 2).
    *   **Scenario Tables (Upper/Lower Case)**: Two separate blocks of cells (e.g., B46:H61 and B64:H80 in the video) contain the hard-coded assumption values for each specific scenario. These tables are typically placed out of view or below the main model.
-   **Formula Logic**:
    *   **`CHOOSE` function**: Each dynamic assumption cell in the "Live Case" block contains a formula like `=CHOOSE($J$4, D48, D66)`. `$J$4` is the scenario selector, `D48` is the value from Scenario 1, and `D66` is the value from Scenario 2.
    *   **Data Validation**: Applied to the scenario selector cell to create a dropdown list, restricting input to valid scenario numbers (e.g., 1, 2).
    *   **`IF` and `IFERROR` functions (demonstrated in Income Statement output)**: The video also shows using `IF` for conditional taxation (e.g., `=IF(D21<0, "NA", D21*D44)`) and `IFERROR` (e.g., `=IFERROR(D21-D24, D21)`) to gracefully handle errors, particularly when trying to perform arithmetic on non-numeric results like "NA".
-   **Visual Design**:
    *   **Scenario Selector Cell**: Yellow fill, bold black text, centered, with borders.
    *   **Live Case Assumptions**: Black text, no fill, with borders. Number formats (currency, percentage, number) are applied as appropriate.
    *   **Scenario Tables (Upper/Lower Case)**: Headers typically have a light background fill with bold text. Hard-coded values within the tables are formatted with a blue font to distinguish them from dynamic (black) values, with borders.
-   **Charts/Tables**: The skill does not directly render charts or tables, but it provides the dynamic input data that would drive an income statement or other financial models.
-   **Theme Hooks**: `header_bg` (for block headers), `header_fg` (for block headers), `text_color` (for dynamic outputs), `hardcoded_input_fg` (for hard-coded inputs), `highlight_bg` (for scenario selector), `border_color`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter, column_letters

# Helper function (similar to what would be in _helpers.py)
def get_theme_colors(theme_name):
    themes = {
        "corporate_blue": {
            "header_bg": "FFDDEBF7",  # Light blue
            "header_fg": "FF000000",  # Black
            "text_color": "FF000000", # Black (dynamic)
            "hardcoded_input_fg": "FF4472C4", # Blue (hardcoded)
            "highlight_bg": "FFFFFF00", # Yellow
            "border_color": "FF000000" # Black
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def apply_border(cell, style="thin", color="FF000000"):
    side = Side(border_style=style, color=color)
    cell.border = Border(left=side, right=side, top=side, bottom=side)

def apply_fill_and_font(cell, fill_color, font_color, bold=False, center=False):
    cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    cell.font = Font(color=font_color, bold=bold)
    if center:
        cell.alignment = Alignment(horizontal="center", vertical="center")

def render(ws, anchor: str = "B28", *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a dynamic scenario assumption section on an Excel worksheet, including:
    - A scenario selection dropdown.
    - 'Live Case' assumptions driven by CHOOSE formulas.
    - Underlying 'Upper Case' (Scenario 1) hard-coded assumptions.
    - Underlying 'Lower Case' (Scenario 2) hard-coded assumptions.

    Args:
        ws: The worksheet to render on.
        anchor: The top-left cell of the main 'Assumptions' header (e.g., "B28" as in the video).
        theme: The color theme to use (default "corporate_blue").
        **kwargs: Additional arguments (not used in this skill).
    """
    colors = get_theme_colors(theme)

    # Convert anchor to row and column
    anchor_col_letter = anchor[0]
    anchor_col_idx = column_letters.index(anchor_col_letter) + 1
    anchor_row = int(anchor[1:])

    # --- Scenario Selector Setup ---
    # In video, Scenario selector is at J4. Relative to B28 (anchor):
    # J is 8 cols right of B (J-B = 10-2 = 8)
    # 4 is 24 rows above 28 (4-28 = -24)
    scenario_selector_col_letter = get_column_letter(anchor_col_idx + 8) # J
    scenario_selector_row = anchor_row - 24 # 4

    ws[f'{scenario_selector_col_letter}{scenario_selector_row-1}'].value = "Scenario" # I4
    ws[f'{scenario_selector_col_letter}{scenario_selector_row-1}'].font = Font(bold=True)
    ws[f'{scenario_selector_col_letter}{scenario_selector_row-1}'].alignment = Alignment(horizontal="right", vertical="center")

    scenario_selector_cell = ws[f'{scenario_selector_col_letter}{scenario_selector_row}'] # J4
    scenario_selector_cell.value = 1 # Default to Scenario 1
    apply_fill_and_font(scenario_selector_cell, colors["highlight_bg"], colors["text_color"], bold=True, center=True)
    apply_border(scenario_selector_cell, color=colors["border_color"])

    # Add Data Validation for the scenario selector
    dv = DataValidation(type="list", formula1="1,2", allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(scenario_selector_cell)

    # --- Assumptions Structure Definition ---
    # These offsets are relative to the 'Assumptions' header (B28) as per video.
    # The actual data starts from D (col_idx = 4) to H (col_idx = 8) for 5 years.
    assumptions_info = [
        {"label_offset": 1, "value_col_offset": 2, "type": "header", "label": "Revenue"}, # B29
        {"label_offset": 2, "value_col_offset": 2, "type": "number", "label": "Number of Orders"}, # B30
        {"label_offset": 3, "value_col_offset": 2, "type": "percentage", "label": "Order Growth Rate"}, # B31
        {"label_offset": 4, "value_col_offset": 2, "type": "currency", "label": "Average Order Value"}, # B32
        {"label_offset": 5, "value_col_offset": 2, "type": "empty_row"}, # B33
        {"label_offset": 6, "value_col_offset": 2, "type": "header", "label": "Cost of Goods Sold (per order)"}, # B34
        {"label_offset": 7, "value_col_offset": 2, "type": "currency", "label": "Manufacturing"}, # B35
        {"label_offset": 8, "value_col_offset": 2, "type": "currency", "label": "Order Fulfillment"}, # B36
        {"label_offset": 9, "value_col_offset": 2, "type": "empty_row"}, # B37
        {"label_offset": 10, "value_col_offset": 2, "type": "header", "label": "Operating Expenses"}, # B38
        {"label_offset": 11, "value_col_offset": 2, "type": "currency", "label": "Warehouse Rent"}, # B39
        {"label_offset": 12, "value_col_offset": 2, "type": "currency", "label": "Salaries & Payroll"}, # B40
        {"label_offset": 13, "value_col_offset": 2, "type": "currency", "label": "Marketing"}, # B41
        {"label_offset": 14, "value_col_offset": 2, "type": "currency", "label": "Other"}, # B42
        {"label_offset": 15, "value_col_offset": 2, "type": "empty_row"}, # B43
        {"label_offset": 16, "value_col_offset": 2, "type": "percentage", "label": "Corporate Tax Rate"} # B44
    ]
    
    # --- Assumptions Header (B28) ---
    assumptions_header_cell = ws[anchor]
    assumptions_header_cell.value = "Assumptions"
    apply_fill_and_font(assumptions_header_cell, colors["header_bg"], colors["header_fg"], bold=True)
    ws.merge_cells(f"{anchor}:{get_column_letter(anchor_col_idx + 6)}{anchor}") # Merge B28:H28

    # --- Live Case Assumptions Block (driven by CHOOSE formulas) ---
    live_case_start_data_col_idx = anchor_col_idx + 2 # D
    num_years = 5 # Year 1 to Year 5
    
    for item in assumptions_info:
        current_label_row = anchor_row + item["label_offset"]
        current_label_cell = ws[f"{get_column_letter(anchor_col_idx)}{current_label_row}"]
        current_label_cell.value = item["label"]
        current_label_cell.font = Font(bold=True)
        apply_border(current_label_cell, color=colors["border_color"])

        if item["type"] == "header":
            # Merge header cells (e.g., B29:H29)
            ws.merge_cells(f"{get_column_letter(anchor_col_idx)}{current_label_row}:{get_column_letter(anchor_col_idx + 6)}{current_label_row}")
            apply_fill_and_font(current_label_cell, colors["header_bg"], colors["header_fg"], bold=True)
        elif item["type"] == "empty_row":
            # Just ensure cell is bordered if it's explicitly an empty row for spacing
            for col_offset in range(7): # B to H
                apply_border(ws[f"{get_column_letter(anchor_col_idx + col_offset)}{current_label_row}"], color=colors["border_color"])
        else:
            for year_offset in range(num_years):
                current_value_col_idx = live_case_start_data_col_idx + year_offset
                current_value_cell = ws[f"{get_column_letter(current_value_col_idx)}{current_label_row}"]

                # Calculate corresponding cells in Scenario 1 and Scenario 2 tables
                # Scenario 1 (Upper Case) starts its assumptions block label at B46 in video.
                # Scenario 2 (Lower Case) starts its assumptions block label at B64 in video.
                # The data values for each scenario start 2 rows below their respective block label.
                
                # These fixed rows must match the placement of the hardcoded scenario blocks below.
                # 'Number of Orders' is the first data row in assumptions_info (offset 2 from anchor_row for live case)
                # In Scenario 1 block, 'Number of Orders' is at row 48 (offset 2 from 46, which is scenario1_block_start_row)
                # So relative to the "Number of Orders" row (B30), the offsets are (48-30) for S1 and (66-30) for S2
                
                # Offset from the 'Number of Orders' row (B30) for S1 data
                s1_base_row_offset_from_live_data_start = (48 - 30) # This is 18
                s2_base_row_offset_from_live_data_start = (66 - 30) # This is 36

                # Calculate the exact row for the current item in the scenario blocks
                # current_label_row (e.g., 30 for Orders) - 30 (row of Orders in live case) + s1_base_row_offset_from_live_data_start + 30 (original live case orders row)
                # Simplified: s1_actual_row = (current_label_row - 30) + (48 for Orders) = current_label_row + 18
                s1_actual_value_row = current_label_row + s1_base_row_offset_from_live_data_start
                s2_actual_value_row = current_label_row + s2_base_row_offset_from_live_data_start
                
                # Ensure these values are linked dynamically from the correct columns (D to H)
                s1_val_col_letter = get_column_letter(current_value_col_idx)
                s2_val_col_letter = get_column_letter(current_value_col_idx)

                formula = f"=CHOOSE(${scenario_selector_col_letter}${scenario_selector_row},{s1_val_col_letter}{s1_actual_value_row},{s2_val_col_letter}{s2_actual_value_row})"
                current_value_cell.value = formula
                current_value_cell.font = Font(color=colors["text_color"]) # Dynamic values are black
                apply_border(current_value_cell, color=colors["border_color"])

                if item["type"] == "number":
                    current_value_cell.number_format = '#,##0'
                elif item["type"] == "percentage":
                    current_value_cell.number_format = '0%'
                elif item["type"] == "currency":
                    current_value_cell.number_format = '$#,##0.00'
        
            # Apply borders to empty cells between label and first data column (B to C)
            for col_offset in range(1, item["value_col_offset"]): # from col C
                apply_border(ws[f"{get_column_letter(anchor_col_idx + col_offset)}{current_label_row}"], color=colors["border_color"])


    # --- Hard-coded Scenario 1 (Upper Case) Assumptions ---
    scenario1_block_start_row = anchor_row + 18 # B46 (anchor is B28, 28+18 = 46)
    ws[f"{get_column_letter(anchor_col_idx)}{scenario1_block_start_row}"].value = "Upper Case (Scenario 1)"
    apply_fill_and_font(ws[f"{get_column_letter(anchor_col_idx)}{scenario1_block_start_row}"], colors["header_bg"], colors["header_fg"], bold=True)
    ws.merge_cells(f"{get_column_letter(anchor_col_idx)}{scenario1_block_start_row}:{get_column_letter(anchor_col_idx + 6)}{scenario1_block_start_row}")

    s1_data_values = {
        "Number of Orders": [3000, 6000, 10500, 15750, 21263],
        "Order Growth Rate": [1.00, 0.75, 0.50, 0.35, 0.35],
        "Average Order Value": [39.95, 39.95, 39.95, 39.95, 39.95],
        "Manufacturing": [6.50, 6.50, 6.50, 6.50, 6.50],
        "Order Fulfillment": [2.25, 2.25, 2.25, 2.25, 2.25],
        "Warehouse Rent": [20000, 20000, 30000, 30000, 30000],
        "Salaries & Payroll": [50000, 50000, 100000, 100000, 100000],
        "Marketing": [25000, 25000, 50000, 100000, 100000],
        "Other": [5000, 5000, 5000, 5000, 5000],
        "Corporate Tax Rate": [0.20, 0.20, 0.20, 0.20, 0.20]
    }

    current_s1_label_row_offset = 2 # Offset from scenario1_block_start_row for labels
    for item in assumptions_info:
        if item["type"] == "header":
            current_s1_label_row_offset += 1 # Skip headers in the data input loop for the data block itself
            continue
        if item["type"] == "empty_row":
            current_s1_label_row_offset += 1
            for col_offset in range(7):
                apply_border(ws[f"{get_column_letter(anchor_col_idx + col_offset)}{scenario1_block_start_row + current_s1_label_row_offset}"], color=colors["border_color"])
            continue
        
        current_s1_row = scenario1_block_start_row + current_s1_label_row_offset
        label_cell = ws[f"{get_column_letter(anchor_col_idx)}{current_s1_row}"]
        label_cell.value = item["label"]
        label_cell.font = Font(bold=True)
        apply_border(label_cell, color=colors["border_color"])

        for i, val in enumerate(s1_data_values[item["label"]]):
            current_value_col_idx = live_case_start_data_col_idx + i
            cell = ws[f"{get_column_letter(current_value_col_idx)}{current_s1_row}"]
            cell.value = val
            apply_border(cell, color=colors["border_color"])
            cell.font = Font(color=colors["hardcoded_input_fg"]) # Blue color for hard-coded inputs

            if item["type"] == "number":
                cell.number_format = '#,##0'
            elif item["type"] == "percentage":
                cell.number_format = '0%'
            elif item["type"] == "currency":
                cell.number_format = '$#,##0.00'
        current_s1_label_row_offset += 1
        
        # Apply borders to empty cells between label and first data column (B to C)
        for col_offset in range(1, item["value_col_offset"]): # from col C
            apply_border(ws[f"{get_column_letter(anchor_col_idx + col_offset)}{current_s1_row}"], color=colors["border_color"])


    # --- Hard-coded Scenario 2 (Lower Case) Assumptions ---
    scenario2_block_start_row = anchor_row + 36 # B64 (anchor is B28, 28+36 = 64)
    ws[f"{get_column_letter(anchor_col_idx)}{scenario2_block_start_row}"].value = "Lower Case (Scenario 2)"
    apply_fill_and_font(ws[f"{get_column_letter(anchor_col_idx)}{scenario2_block_start_row}"], colors["header_bg"], colors["header_fg"], bold=True)
    ws.merge_cells(f"{get_column_letter(anchor_col_idx)}{scenario2_block_start_row}:{get_column_letter(anchor_col_idx + 6)}{scenario2_block_start_row}")

    s2_data_values = {
        "Number of Orders": [2000, 4000, 7000, 10500, 14175],
        "Order Growth Rate": [1.00, 0.75, 0.50, 0.35, 0.35],
        "Average Order Value": [34.95, 34.95, 34.95, 34.95, 34.95],
        "Manufacturing": [8.00, 8.00, 8.00, 8.00, 8.00],
        "Order Fulfillment": [2.25, 2.25, 2.25, 2.25, 2.25],
        "Warehouse Rent": [20000, 20000, 30000, 30000, 30000],
        "Salaries & Payroll": [50000, 50000, 100000, 100000, 100000],
        "Marketing": [25000, 25000, 50000, 100000, 100000],
        "Other": [5000, 5000, 5000, 5000, 5000],
        "Corporate Tax Rate": [0.25, 0.25, 0.25, 0.25, 0.25]
    }

    current_s2_label_row_offset = 2 # Offset from scenario2_block_start_row for labels
    for item in assumptions_info:
        if item["type"] == "header":
            current_s2_label_row_offset += 1
            continue
        if item["type"] == "empty_row":
            current_s2_label_row_offset += 1
            for col_offset in range(7):
                apply_border(ws[f"{get_column_letter(anchor_col_idx + col_offset)}{scenario2_block_start_row + current_s2_label_row_offset}"], color=colors["border_color"])
            continue
        
        current_s2_row = scenario2_block_start_row + current_s2_label_row_offset
        label_cell = ws[f"{get_column_letter(anchor_col_idx)}{current_s2_row}"]
        label_cell.value = item["label"]
        label_cell.font = Font(bold=True)
        apply_border(label_cell, color=colors["border_color"])

        for i, val in enumerate(s2_data_values[item["label"]]):
            current_value_col_idx = live_case_start_data_col_idx + i
            cell = ws[f"{get_column_letter(current_value_col_idx)}{current_s2_row}"]
            cell.value = val
            apply_border(cell, color=colors["border_color"])
            cell.font = Font(color=colors["hardcoded_input_fg"]) # Blue color for hard-coded inputs

            if item["type"] == "number":
                cell.number_format = '#,##0'
            elif item["type"] == "percentage":
                cell.number_format = '0%'
            elif item["type"] == "currency":
                cell.number_format = '$#,##0.00'
        current_s2_label_row_offset += 1

        # Apply borders to empty cells between label and first data column (B to C)
        for col_offset in range(1, item["value_col_offset"]): # from col C
            apply_border(ws[f"{get_column_letter(anchor_col_idx + col_offset)}{current_s2_row}"], color=colors["border_color"])

    # Optionally adjust column widths for readability
    for col_letter in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        ws.column_dimensions[col_letter].width = 15
    ws.column_dimensions['B'].width = 25
```