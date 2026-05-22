### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Financial Scenario Selector

*   **Tier**: sheet_shell
*   **Core Mechanism**: This skill constructs a complete Excel worksheet for financial forecasting, including an Income Statement and multiple sets of assumptions. It then implements a dynamic scenario selection feature using the `CHOOSE` formula, linked to a Data Validation dropdown. This allows users to instantly switch between different assumption sets (e.g., optimistic, pessimistic) and see their real-time impact on the financial projections.
*   **Applicability**: Ideal for financial analysts, business planners, or anyone building robust financial models where sensitivity analysis and scenario planning are crucial. It can be applied to any forecast-driven model (e.g., revenue, cost, budget) where multiple underlying assumptions need to be toggled for comparative analysis.

### 2. Structural Breakdown

-   **Data Layout**:
    -   **Income Statement (Rows 1-25)**: Lists financial line items (Revenue, COGS, Gross Profit, Operating Expenses, Operating Profit, Tax, Profit/Loss) with 5 years of projections (Columns D-H).
    -   **Live Case Assumptions (Rows 28-44)**: This block contains the currently active assumptions, populated dynamically by `CHOOSE` formulas.
    -   **Scenario 1 (Upper Case) Assumptions (Rows 46-62)**: A static block of assumptions representing an "optimistic" or "base" case.
    -   **Scenario 2 (Lower Case) Assumptions (Rows 64-80)**: A static block of assumptions representing a "pessimistic" or "alternative" case.
    -   **Scenario Selector (Cell K4)**: A single cell that acts as a dropdown to choose between scenarios (1 or 2).
-   **Formula Logic**:
    -   **Live Case Assumptions**: Each cell in the "Live Case" assumption block uses a `CHOOSE` formula: `=CHOOSE($K$4, [Scenario 1 Cell], [Scenario 2 Cell])`. For example, `D30` (Live Case Number of Orders) would be `=CHOOSE($K$4, D48, D66)`. This dynamically pulls values from either Scenario 1 or Scenario 2 based on the selection in `K4`.
    -   **Income Statement Calculations**:
        -   `Revenue`: `=[Live Case Number of Orders] * [Live Case Average Order Value]` (e.g., `=D30*D32`)
        -   `Manufacturing/Order Fulfillment`: `=[Live Case Number of Orders] * [Live Case Per-Order Cost]` (e.g., `=D30*D35`)
        -   `Total COGS`: `SUM([Manufacturing]:[Order Fulfillment])`
        -   `Gross Profit`: `[Revenue] - [Total COGS]`
        -   `Gross Profit Margin`: `[Gross Profit] / [Revenue]`
        -   `Total Operating Expenses`: `SUM([Warehouse Rent]:[Other])`
        -   `Operating Profit`: `[Gross Profit] - [Total Operating Expenses]`
        -   `Operating Profit Margin`: `[Operating Profit] / [Revenue]`
        -   `Corporate Tax`: `=IF([Operating Profit]<0, "NA", [Operating Profit]*[Live Case Corporate Tax Rate])`
        -   `Profit / (Loss)`: `=IFERROR([Operating Profit]-[Corporate Tax], [Operating Profit])` (handles "NA" errors from tax calculation)
-   **Visual Design**:
    -   **Headers**: Years and "Year N" labels use a dark blue background with white, bold font (`header_bg`, `header_fg`).
    -   **Section Titles**: Main titles like "Income Statement", "Assumptions", "Live Case" are bolded.
    -   **Input/Output Distinction**: Hard-coded values within the static scenario blocks (Scenario 1 & 2) are displayed in blue font (`input_color`). Formula-driven values in the "Live Case" and "Income Statement" are in black font (`output_color`).
    -   **Borders**: All relevant data blocks (Income Statement, all Assumption blocks) have thin grey borders.
    -   **Scenario Selector**: Cell `K4` has a yellow fill (`scenario_bg`) and borders, with centered, bold text.
    -   **Number Formatting**: Currency ($#,##0), percentages (0%), and whole numbers are applied as appropriate.
-   **Charts/Tables**: No explicit charts or Excel tables are created by this skill, but the dynamic financial output is suitable for charting.
-   **Theme Hooks**: `header_bg`, `header_fg`, `section_bg`, `section_header_fg`, `border_color`, `input_color`, `output_color`, `scenario_bg`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# Helper functions for themes
def _get_theme_colors(theme_name):
    colors = {
        "corporate_blue": {
            "header_bg": "FF2E6A8A", # A shade of blue
            "header_fg": "FFFFFFFF", # White
            "section_bg": "FFD9D9D9", # Light grey
            "section_header_fg": "FF000000", # Black
            "border_color": "FFB0B0B0", # Grey border
            "input_color": "FF0000FF", # Blue for hard-coded input
            "output_color": "FF000000", # Black for formula output
            "scenario_bg": "FFFFFF00", # Yellow for scenario selector
        }
    }
    return colors.get(theme_name, colors["corporate_blue"])

def _create_font(name="Calibri", size=11, bold=False, italic=False, color="FF000000"):
    return Font(name=name, size=size, bold=bold, italic=italic, color=color)

def _create_fill(fgColor="FFFFFFFF"):
    return PatternFill(start_color=fgColor, end_color=fgColor, fill_type="solid")

def _create_border(color="FF000000", style="thin"):
    side = Side(border_style=style, color=color)
    return Border(left=side, right=side, top=side, bottom=side)

def _create_alignment(horizontal="general", vertical="bottom"):
    return Alignment(horizontal=horizontal, vertical=vertical)

class Theme:
    def __init__(self, name):
        self.colors = _get_theme_colors(name)
        self.header_font = _create_font(color=self.colors["header_fg"], bold=True)
        self.header_fill = _create_fill(fgColor=self.colors["header_bg"])
        self.section_header_font = _create_font(color=self.colors["section_header_fg"], bold=True)
        self.section_fill = _create_fill(fgColor=self.colors["section_bg"])
        self.border = _create_border(color=self.colors["border_color"])
        self.input_font = _create_font(color=self.colors["input_color"])
        self.output_font = _create_font(color=self.colors["output_color"])
        self.scenario_fill = _create_fill(fgColor=self.colors["scenario_bg"])
        self.center_align = _create_alignment(horizontal="center")
        self.right_align = _create_alignment(horizontal="right")

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(title=sheet_name)
    t = Theme(theme)

    # --- Setup Years ---
    start_year = 2023
    num_years = 5
    years = [start_year + i for i in range(num_years)]
    
    # --- Income Statement Header ---
    ws.cell(row=1, column=2, value=title).font = t.section_header_font
    ws.cell(row=3, column=2, value="Figures in USD").font = t.section_header_font
    ws.cell(row=3, column=3, value="Unit").font = t.section_header_font
    for i, year in enumerate(years):
        col_idx = 4 + i # D to H
        ws.cell(row=2, column=col_idx, value=year).font = t.header_font
        ws.cell(row=2, column=col_idx).fill = t.header_fill
        ws.cell(row=2, column=col_idx).alignment = t.center_align
        ws.cell(row=3, column=col_idx, value=f"Year {i+1}").font = t.header_font
        ws.cell(row=3, column=col_idx).fill = t.header_fill
        ws.cell(row=3, column=col_idx).alignment = t.center_align
        ws.column_dimensions[get_column_letter(col_idx)].width = 12 # Set width for year columns

    # --- Income Statement Layout & Basic Labels ---
    income_stmt_rows = {
        "Revenue": 5,
        "Cost of Goods Sold": 6,
        "Manufacturing": 7,
        "Order Fulfillment": 8,
        "Total COGS": 10,
        "Gross Profit": 11,
        "Gross Profit Margin": 12,
        "Operating Expenses": 14,
        "Warehouse Rent": 15,
        "Salaries & Payroll": 16,
        "Marketing": 17,
        "Other": 18,
        "Total Operating Expenses": 20,
        "Operating Profit": 21,
        "Operating Profit Margin": 22,
        "Corporate Tax": 24,
        "Profit / (Loss)": 25,
    }

    for label, row_idx in income_stmt_rows.items():
        ws.cell(row=row_idx, column=2, value=label).font = t.output_font
        if label in ["Manufacturing", "Order Fulfillment", "Warehouse Rent", "Salaries & Payroll", "Marketing", "Other"]:
            ws.cell(row=row_idx, column=3, value="$").font = t.output_font
        elif label in ["Revenue", "Total COGS", "Gross Profit", "Total Operating Expenses", "Operating Profit", "Corporate Tax", "Profit / (Loss)"]:
            ws.cell(row=row_idx, column=3, value="$").font = t.output_font
        elif label in ["Gross Profit Margin", "Operating Profit Margin"]:
            ws.cell(row=row_idx, column=3, value="%").font = t.output_font

    # Apply bolding to main sections
    for label in ["Cost of Goods Sold", "Operating Expenses"]:
        ws.cell(row=income_stmt_rows[label], column=2).font = t.section_header_font

    # Add borders to Income Statement area
    for r in range(1, income_stmt_rows["Profit / (Loss)"] + 1):
        for c in range(2, 4 + num_years):
            ws.cell(row=r, column=c).border = t.border

    # --- Assumptions Section Setup ---
    assumptions_start_row_live = 28
    assumptions_start_row_s1 = assumptions_start_row_live + 18 # Scenario 1
    assumptions_start_row_s2 = assumptions_start_row_s1 + 18   # Scenario 2

    assumption_labels = {
        "Revenue": 1,
        "Number of Orders": 2,
        "Order Growth Rate": 3,
        "Average Order Value": 4,
        "Cost of Goods Sold (per order)": 6,
        "Manufacturing": 7,
        "Order Fulfillment": 8,
        "Operating Expenses": 10,
        "Warehouse Rent": 11,
        "Salaries & Payroll": 12,
        "Marketing": 13,
        "Other": 14,
        "Corporate Tax Rate": 16,
    }

    # Helper to populate assumption block labels
    def setup_assumption_block(start_row, block_name):
        ws.cell(row=start_row, column=2, value=block_name).font = t.section_header_font
        for label, offset in assumption_labels.items():
            row_idx = start_row + offset
            ws.cell(row=row_idx, column=2, value=label).font = t.output_font
            if label == "Number of Orders":
                ws.cell(row=row_idx, column=3, value="#").font = t.output_font
            elif label in ["Manufacturing", "Order Fulfillment", "Warehouse Rent", "Salaries & Payroll", "Marketing", "Other", "Average Order Value"]:
                ws.cell(row=row_idx, column=3, value="$").font = t.output_font
            elif label in ["Order Growth Rate", "Corporate Tax Rate"]:
                ws.cell(row=row_idx, column=3, value="%").font = t.output_font

        for label_key in ["Revenue", "Cost of Goods Sold (per order)", "Operating Expenses"]:
            ws.cell(row=start_row + assumption_labels[label_key], column=2).font = t.section_header_font

        # Apply borders to assumption area
        for r in range(start_row, start_row + assumption_labels["Corporate Tax Rate"] + 1):
            for c in range(2, 4 + num_years):
                ws.cell(row=r, column=c).border = t.border

    setup_assumption_block(assumptions_start_row_live, "Live Case")
    setup_assumption_block(assumptions_start_row_s1, "Upper Case (Scenario 1)")
    setup_assumption_block(assumptions_start_row_s2, "Lower Case (Scenario 2)")

    # --- Populate Scenario 1 (Upper Case) Assumptions (Hard-coded inputs - blue text) ---
    s1_data = {
        "Number of Orders": [3000, 6000, 10500, 15750, 21263],
        "Order Growth Rate": [1.00, 0.75, 0.50, 0.35],
        "Average Order Value": 39.95,
        "Manufacturing": 6.50,
        "Order Fulfillment": 2.25,
        "Warehouse Rent": [20000, 20000, 20000, 20000, 20000], # Initial values, adjusted later in video
        "Salaries & Payroll": [50000, 50000, 50000, 50000, 50000], # Initial values, adjusted later in video
        "Marketing": [25000, 25000, 25000, 25000, 25000], # Initial values, adjusted later in video
        "Other": 5000,
        "Corporate Tax Rate": 0.20,
    }
    # Manually adjusted values during video for S1 from fixed to scaling
    s1_data["Warehouse Rent"][1:] = [30000, 30000, 30000, 30000]
    s1_data["Salaries & Payroll"][1:] = [100000, 100000, 100000, 100000]
    s1_data["Marketing"][1:] = [50000, 100000, 100000, 100000]

    for col_idx in range(num_years):
        col_letter = get_column_letter(4 + col_idx)
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Number of Orders"], column=4 + col_idx, value=s1_data["Number of Orders"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Number of Orders"], column=4 + col_idx).number_format = "#,##0"

        if col_idx < num_years - 1:
            ws.cell(row=assumptions_start_row_s1 + assumption_labels["Order Growth Rate"], column=5 + col_idx, value=s1_data["Order Growth Rate"][col_idx]).font = t.input_font
            ws.cell(row=assumptions_start_row_s1 + assumption_labels["Order Growth Rate"], column=5 + col_idx).number_format = "0%"

        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Average Order Value"], column=4 + col_idx, value=s1_data["Average Order Value"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Average Order Value"], column=4 + col_idx).number_format = "$#,##0.00"
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Manufacturing"], column=4 + col_idx, value=s1_data["Manufacturing"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Manufacturing"], column=4 + col_idx).number_format = "$#,##0.00"
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Order Fulfillment"], column=4 + col_idx, value=s1_data["Order Fulfillment"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Order Fulfillment"], column=4 + col_idx).number_format = "$#,##0.00"
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Warehouse Rent"], column=4 + col_idx, value=s1_data["Warehouse Rent"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Warehouse Rent"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Salaries & Payroll"], column=4 + col_idx, value=s1_data["Salaries & Payroll"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Salaries & Payroll"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Marketing"], column=4 + col_idx, value=s1_data["Marketing"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Marketing"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Other"], column=4 + col_idx, value=s1_data["Other"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Other"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Corporate Tax Rate"], column=4 + col_idx, value=s1_data["Corporate Tax Rate"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s1 + assumption_labels["Corporate Tax Rate"], column=4 + col_idx).number_format = "0%"

    # --- Populate Scenario 2 (Lower Case) Assumptions (Hard-coded inputs - blue text) ---
    s2_data = {
        "Number of Orders": [2000, 4000, 7000, 10500, 14175],
        "Order Growth Rate": [1.00, 0.75, 0.50, 0.35],
        "Average Order Value": 34.95,
        "Manufacturing": 8.00,
        "Order Fulfillment": 2.25,
        "Warehouse Rent": [20000, 20000, 20000, 20000, 20000],
        "Salaries & Payroll": [50000, 50000, 50000, 50000, 50000],
        "Marketing": [25000, 25000, 25000, 25000, 25000],
        "Other": 5000,
        "Corporate Tax Rate": 0.25,
    }
    # Manually adjusted values during video for S2 from fixed to scaling
    s2_data["Warehouse Rent"][1:] = [30000, 30000, 30000, 30000]
    s2_data["Salaries & Payroll"][1:] = [100000, 100000, 100000, 100000]
    s2_data["Marketing"][1:] = [50000, 100000, 100000, 100000]

    for col_idx in range(num_years):
        col_letter = get_column_letter(4 + col_idx)
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Number of Orders"], column=4 + col_idx, value=s2_data["Number of Orders"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Number of Orders"], column=4 + col_idx).number_format = "#,##0"

        if col_idx < num_years - 1:
            ws.cell(row=assumptions_start_row_s2 + assumption_labels["Order Growth Rate"], column=5 + col_idx, value=s2_data["Order Growth Rate"][col_idx]).font = t.input_font
            ws.cell(row=assumptions_start_row_s2 + assumption_labels["Order Growth Rate"], column=5 + col_idx).number_format = "0%"

        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Average Order Value"], column=4 + col_idx, value=s2_data["Average Order Value"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Average Order Value"], column=4 + col_idx).number_format = "$#,##0.00"
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Manufacturing"], column=4 + col_idx, value=s2_data["Manufacturing"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Manufacturing"], column=4 + col_idx).number_format = "$#,##0.00"
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Order Fulfillment"], column=4 + col_idx, value=s2_data["Order Fulfillment"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Order Fulfillment"], column=4 + col_idx).number_format = "$#,##0.00"
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Warehouse Rent"], column=4 + col_idx, value=s2_data["Warehouse Rent"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Warehouse Rent"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Salaries & Payroll"], column=4 + col_idx, value=s2_data["Salaries & Payroll"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Salaries & Payroll"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Marketing"], column=4 + col_idx, value=s2_data["Marketing"][col_idx]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Marketing"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Other"], column=4 + col_idx, value=s2_data["Other"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Other"], column=4 + col_idx).number_format = "$#,##0"
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Corporate Tax Rate"], column=4 + col_idx, value=s2_data["Corporate Tax Rate"]).font = t.input_font
        ws.cell(row=assumptions_start_row_s2 + assumption_labels["Corporate Tax Rate"], column=4 + col_idx).number_format = "0%"

    # --- Live Case Assumptions (CHOOSE formulas - black text) ---
    scenario_selector_cell_ref = 'K4' # Column K, Row 4 for scenario selector
    ws.cell(row=4, column=10, value="Scenario").font = t.output_font
    ws.cell(row=4, column=11, value=1).font = t.output_font
    ws.cell(row=4, column=11).fill = t.scenario_fill
    ws.cell(row=4, column=11).alignment = t.center_align
    ws.cell(row=4, column=11).border = t.border

    for label, offset in assumption_labels.items():
        row_idx_live = assumptions_start_row_live + offset
        row_idx_s1 = assumptions_start_row_s1 + offset
        row_idx_s2 = assumptions_start_row_s2 + offset

        for col_offset in range(num_years):
            col_idx = 4 + col_offset
            s1_cell_ref = f"{get_column_letter(col_idx)}{row_idx_s1}"
            s2_cell_ref = f"{get_column_letter(col_idx)}{row_idx_s2}"
            formula = f"=CHOOSE(${scenario_selector_cell_ref},{s1_cell_ref},{s2_cell_ref})"
            ws.cell(row=row_idx_live, column=col_idx, value=formula).font = t.output_font
            if label in ["Order Growth Rate", "Corporate Tax Rate"]:
                ws.cell(row=row_idx_live, column=col_idx).number_format = "0%"
            elif label in ["Average Order Value", "Manufacturing", "Order Fulfillment", "Warehouse Rent", "Salaries & Payroll", "Marketing", "Other"]:
                ws.cell(row=row_idx_live, column=col_idx).number_format = "$#,##0.00"
            elif label == "Number of Orders":
                ws.cell(row=row_idx_live, column=col_idx).number_format = "#,##0"

    # --- Income Statement Formulas (linking to Live Case Assumptions) ---
    # Initial column formulas (D)
    col_d_idx = 4
    ws.cell(row=income_stmt_rows["Revenue"], column=col_d_idx, value=f"=D{assumptions_start_row_live + assumption_labels['Number of Orders']}*D{assumptions_start_row_live + assumption_labels['Average Order Value']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Manufacturing"], column=col_d_idx, value=f"=D{assumptions_start_row_live + assumption_labels['Number of Orders']}*D{assumptions_start_row_live + assumption_labels['Manufacturing']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Order Fulfillment"], column=col_d_idx, value=f"=D{assumptions_start_row_live + assumption_labels['Number of Orders']}*D{assumptions_start_row_live + assumption_labels['Order Fulfillment']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Total COGS"], column=col_d_idx, value=f"=SUM(D{income_stmt_rows['Manufacturing']}:D{income_stmt_rows['Order Fulfillment']})").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Gross Profit"], column=col_d_idx, value=f"=D{income_stmt_rows['Revenue']}-D{income_stmt_rows['Total COGS']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Gross Profit Margin"], column=col_d_idx, value=f"=D{income_stmt_rows['Gross Profit']}/D{income_stmt_rows['Revenue']}").number_format = "0%"
    ws.cell(row=income_stmt_rows["Warehouse Rent"], column=col_d_idx, value=f"=D{assumptions_start_row_live + assumption_labels['Warehouse Rent']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Salaries & Payroll"], column=col_d_idx, value=f"=D{assumptions_start_row_live + assumption_labels['Salaries & Payroll']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Marketing"], column=col_d_idx, value=f"=D{assumptions_start_row_live + assumption_labels['Marketing']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Other"], column=col_d_idx, value=f"=D{assumptions_start_row_live + assumption_labels['Other']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Total Operating Expenses"], column=col_d_idx, value=f"=SUM(D{income_stmt_rows['Warehouse Rent']}:D{income_stmt_rows['Other']})").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Operating Profit"], column=col_d_idx, value=f"=D{income_stmt_rows['Gross Profit']}-D{income_stmt_rows['Total Operating Expenses']}").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Operating Profit Margin"], column=col_d_idx, value=f"=D{income_stmt_rows['Operating Profit']}/D{income_stmt_rows['Revenue']}").number_format = "0%"
    ws.cell(row=income_stmt_rows["Corporate Tax"], column=col_d_idx, value=f"=IF(D{income_stmt_rows['Operating Profit']}<0,\"NA\",D{income_stmt_rows['Operating Profit']}*D{assumptions_start_row_live + assumption_labels['Corporate Tax Rate']})").number_format = "$#,##0"
    ws.cell(row=income_stmt_rows["Profit / (Loss)"], column=col_d_idx, value=f"=IFERROR(D{income_stmt_rows['Operating Profit']}-D{income_stmt_rows['Corporate Tax']},D{income_stmt_rows['Operating Profit']})").number_format = "$#,##0"

    # Fill formulas across for Income Statement
    for r_label, r_idx in income_stmt_rows.items():
        if r_label not in ["Cost of Goods Sold", "Operating Expenses"]: # Skip category headers
            for c_offset in range(1, num_years): # Start from E (column 5)
                src_col_letter = get_column_letter(col_d_idx)
                target_col_letter = get_column_letter(col_d_idx + c_offset)
                
                src_cell = ws.cell(row=r_idx, column=col_d_idx)
                target_cell = ws.cell(row=r_idx, column=col_d_idx + c_offset)
                
                if src_cell.value is not None and isinstance(src_cell.value, str) and src_cell.value.startswith('='):
                    # Replace first column reference with target column reference
                    formula_str = src_cell.value.replace(f"{src_col_letter}{r_idx}", f"{target_col_letter}{r_idx}")
                    
                    # Special handling for assumption cells if they need to be fixed
                    # The video uses cell linking which auto-adjusts, but direct formula copy might need more precision
                    # The CHOOSE formula cells are already black and contain the dynamic logic.
                    
                    # Replace column references for live assumptions
                    for assumption_label_key, assumption_offset in assumption_labels.items():
                        live_assumption_row = assumptions_start_row_live + assumption_offset
                        old_ref = f"{src_col_letter}{live_assumption_row}"
                        new_ref = f"{target_col_letter}{live_assumption_row}"
                        formula_str = formula_str.replace(old_ref, new_ref)
                    
                    # Special handling for Corporate Tax Rate if it's outside the direct range
                    if r_label == "Corporate Tax":
                        tax_rate_row = assumptions_start_row_live + assumption_labels['Corporate Tax Rate']
                        formula_str = formula_str.replace(f"{src_col_letter}{tax_rate_row}", f"{target_col_letter}{tax_rate_row}")

                    target_cell.value = formula_str
                else:
                    target_cell.value = src_cell.value # Copy static value if not a formula

                target_cell.number_format = src_cell.number_format
                target_cell.font = t.output_font


    # --- Data Validation for Scenario Selector ---
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws.cell(row=4, column=11))

    # Autofit columns
    for col in ws.columns:
        max_length = 0
        column = col[0].column # Get the column letter/index
        for cell in col:
            try:
                if cell.value is not None and len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[get_column_letter(column)].width = adjusted_width

    # Set column B to a fixed width to prevent auto-fit from shrinking it too much
    ws.column_dimensions['B'].width = 25
```