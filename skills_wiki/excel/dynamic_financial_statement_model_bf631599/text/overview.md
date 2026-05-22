### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Financial Statement Model

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs an industry-standard financial projection shell. It enforces the "blue = hardcoded, black = formula" formatting convention, applies custom year formatting (`0"A"` for Actuals, `0"E"` for Estimates), and builds a dynamic projection engine driven by a `CHOOSE` function for scenario analysis (Best/Base/Worst case).
* **Applicability**: Best used for financial models, operating projections, DCF valuations, and budgeting templates where you need to cleanly separate historical data from scenario-driven future forecasts. 

### 2. Structural Breakdown

- **Data Layout**: Column A contains the line item labels. Columns B-C hold historical actuals, while Columns D-F hold forecasted periods. The sheet is horizontally split into the core statement (top) and the scenario/assumptions engine (bottom). 
- **Formula Logic**: 
  - Subtotals use basic arithmetic (`=B4-B5`).
  - Projections scale from the previous year (`=C4*(1+D16)`).
  - The Scenario Engine uses `=CHOOSE($B$10, D13, D14, D15)` to dynamically pull the selected scenario's growth rate into the forecast based on a master toggle switch.
- **Visual Design**: Uses dark themed header backgrounds with white text. Employs classic financial modeling font colors: standard black for calculations, pure blue (`#0000FF`) for manual inputs/assumptions. A yellow highlighted cell indicates the scenario toggle control.
- **Charts/Tables**: Standard unstructured data ranges (no rigid Excel Tables) to allow for flexible row insertions, which is standard practice in complex financial modeling.
- **Theme Hooks**: Utilizes `primary` for the main timeline header strip, relying on `text_light` for contrast.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Income Statement", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a dynamic financial statement sheet with historical actuals, 
    future estimates, and a CHOOSE-driven scenario analysis engine.
    """
    ws = wb.create_sheet(sheet_name)

    # Standard theme palette fallback
    theme_colors = {
        "corporate_blue": {"primary": "002060", "secondary": "4F81BD", "accent": "00B050", "text_light": "FFFFFF"},
    }.get(theme, {"primary": "002060", "secondary": "4F81BD", "accent": "00B050", "text_light": "FFFFFF"})

    # Styles
    header_fill = PatternFill(start_color=theme_colors["primary"], end_color=theme_colors["primary"], fill_type="solid")
    header_font = Font(color=theme_colors["text_light"], bold=True)
    subtotal_font = Font(bold=True)
    input_font = Font(color="0000FF")  # Financial standard: Blue for hardcoded assumptions/inputs
    calc_font = Font(color="000000")   # Financial standard: Black for formulas
    
    thin_border = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    toggle_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # 1. Title
    ws["A1"] = title
    ws["A1"].font = Font(size=14, bold=True)

    # 2. Headers (Years & Custom Formatting)
    headers = ["Line Item", 2023, 2024, 2025, 2026, 2027]
    for col_idx, val in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_idx, value=val)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

        # Custom number formats: append 'A' for actuals, 'E' for estimates
        if col_idx in [2, 3]:
            cell.number_format = '0"A"'
        elif col_idx >= 4:
            cell.number_format = '0"E"'

    # 3. Statement Structure
    line_items = ["Revenue", "COGS", "Gross Profit", "SG&A", "Operating Income"]
    for row_idx, item in enumerate(line_items, 4):
        ws.cell(row=row_idx, column=1, value=item)

    # Historical Data (Hardcoded)
    actuals = {
        4: [5210, 5435],  # Revenue
        5: [3345, 3350],  # COGS
        7: [850, 870]     # SG&A
    }

    for r, vals in actuals.items():
        for c_idx, val in enumerate(vals, 2):
            cell = ws.cell(row=r, column=c_idx, value=val)
            cell.font = input_font
            cell.number_format = '#,##0'

    # Historical Subtotals (Calculated)
    for c in ["B", "C"]:
        ws[f"{c}6"] = f"={c}4-{c}5"  # Gross Profit
        ws[f"{c}6"].font = subtotal_font
        ws[f"{c}6"].border = thin_border
        ws[f"{c}6"].number_format = '#,##0'

        ws[f"{c}8"] = f"={c}6-{c}7"  # Operating Income
        ws[f"{c}8"].font = subtotal_font
        ws[f"{c}8"].border = thin_border
        ws[f"{c}8"].number_format = '#,##0'

    # 4. Scenario Engine Setup
    ws["A10"] = "Scenario Selection (1=Best, 2=Base, 3=Worst)"
    ws["A10"].font = Font(bold=True)
    
    ws["B10"] = 2  # Default to Base Case
    ws["B10"].font = input_font
    ws["B10"].fill = toggle_fill
    ws["B10"].border = Border(outline=Side(style='medium'))
    ws["B10"].alignment = Alignment(horizontal="center")

    ws["A12"] = "Revenue Growth Scenarios"
    ws["A12"].font = Font(bold=True)
    ws["A13"] = "1 - Best Case"
    ws["A14"] = "2 - Base Case"
    ws["A15"] = "3 - Worst Case"
    ws["A16"] = "Applied Growth Rate"
    ws["A16"].font = Font(bold=True, italic=True)

    # Hardcoded Scenario Rates (Forecast Years)
    scenarios = {
        13: [0.067, 0.065, 0.060],  # Best
        14: [0.047, 0.047, 0.047],  # Base
        15: [0.027, 0.020, 0.015]   # Worst
    }
    for r, rates in scenarios.items():
        for c_idx, rate in enumerate(rates, 4):
            cell = ws.cell(row=r, column=c_idx, value=rate)
            cell.font = input_font
            cell.number_format = '0.0%'

    # CHOOSE function to dynamically select active scenario rate
    for c_idx, col_letter in enumerate(["D", "E", "F"], 4):
        formula = f"=CHOOSE($B$10, {col_letter}13, {col_letter}14, {col_letter}15)"
        cell = ws.cell(row=16, column=c_idx, value=formula)
        cell.font = calc_font
        cell.number_format = '0.0%'
        cell.border = thin_border

    # 5. Dynamic Forecast Projections
    for c_idx, col_letter in enumerate(["D", "E", "F"], 4):
        prev_col = get_column_letter(c_idx - 1)

        # Revenue = Prior Year * (1 + Applied Growth Rate)
        ws[f"{col_letter}4"] = f"={prev_col}4*(1+{col_letter}16)"
        ws[f"{col_letter}4"].number_format = '#,##0'

        # COGS = 62% of Revenue
        ws[f"{col_letter}5"] = f"={col_letter}4*0.62"
        ws[f"{col_letter}5"].number_format = '#,##0'

        # Gross Profit
        ws[f"{col_letter}6"] = f"={col_letter}4-{col_letter}5"
        ws[f"{col_letter}6"].font = subtotal_font
        ws[f"{col_letter}6"].border = thin_border
        ws[f"{col_letter}6"].number_format = '#,##0'

        # SG&A = 16% of Revenue
        ws[f"{col_letter}7"] = f"={col_letter}4*0.16"
        ws[f"{col_letter}7"].number_format = '#,##0'

        # Operating Income
        ws[f"{col_letter}8"] = f"={col_letter}6-{col_letter}7"
        ws[f"{col_letter}8"].font = subtotal_font
        ws[f"{col_letter}8"].border = thin_border
        ws[f"{col_letter}8"].number_format = '#,##0'

    # Column Width Polish
    ws.column_dimensions["A"].width = 35
    for col in ["B", "C", "D", "E", "F"]:
        ws.column_dimensions[col].width = 13
```