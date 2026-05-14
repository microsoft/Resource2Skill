### 1. High-level Skill Pattern Extraction

> **Skill Name**: Financial Model Income Statement

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a standard 3-statement style Income Statement with a custom "A" (Actuals) and "E" (Estimates) timeline header. Builds hierarchical line items with formulas driving subtotals (Gross Profit, EBITDA, Net Income) and borders, paired with a separated Assumptions block that calculates historical margins/growth and drives the forecast periods via dynamic cell references.
* **Applicability**: Core corporate finance, budgeting, and forecasting. Best used when generating standard financial schedules where historical data drives future projections through margin and growth assumptions.

### 2. Structural Breakdown

- **Data Layout**: Column B holds the line item labels. Columns C onward represent the timeline (historical years followed by forecast years). The sheet is split into the "Income Statement" schedule above, and the "Income Statement Assumptions" block below.
- **Formula Logic**: 
  - Margins/Growth (e.g., `=D5/C5-1` for growth, `=D6/D5` for % of revenue).
  - Forecasts driven by base * assumption (e.g., `=E5*(1+F18)` for Revenue, `=F5*F19` for COGS).
  - Subtotals use basic arithmetic (`=D7-D8-D9` for Operating Income).
- **Visual Design**: Hardcoded inputs (Actuals, flat forecast assumptions) are colored blue (`#0000FF`) to indicate they can be overridden, while formulas remain black. Column headers are dark blue with bold white text. Panes are frozen to keep the timeline and line items visible while scrolling.
- **Charts/Tables**: Standard spreadsheet range (no explicit tables), with column B expanded for readability.
- **Theme Hooks**: `header_bg` for the timeline background, `header_text` for the timeline font, and a standard `0000FF` blue for input text.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Income Statement", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Theme settings
    header_bg = "002060" # Dark blue
    header_fg = "FFFFFF"
    input_fg = "0000FF"  # Blue for hardcoded inputs
    
    header_fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")
    header_font = Font(color=header_fg, bold=True)
    bold_font = Font(bold=True)
    input_font = Font(color=input_fg)
    
    top_border = Border(top=Side(style='thin'))
    top_bottom_border = Border(top=Side(style='thin'), bottom=Side(style='double'))
    
    # Title
    ws["B2"] = title
    ws["B2"].font = Font(bold=True, size=14)
    
    # Timeline Setup
    actual_years = [2023, 2024, 2025]
    forecast_years = [2026, 2027, 2028, 2029, 2030]
    years = actual_years + forecast_years
    
    start_row = 4
    start_col = 3 # Column C
    
    # Write Timeline Headers
    ws.cell(row=start_row, column=2).fill = header_fill
    for i, year in enumerate(years):
        col = start_col + i
        cell = ws.cell(row=start_row, column=col, value=year)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        
        # Custom number format for A (Actuals) vs E (Estimates)
        if year in actual_years:
            cell.number_format = '0"A"'
        else:
            cell.number_format = '0"E"'
            
    # Income Statement Line Items (Actuals data)
    line_items = [
        ("Revenue", [5210, 5435, 5710]),
        ("COGS", [3345, 3350, 3551]),
        ("Gross Profit", None),
        ("Selling, general & administrative", [850, 870, 900]),
        ("Research & development", [400, 420, 400]),
        ("Operating Income", None),
        ("Other income / (expense), net", [50, 50, 50]),
        ("Pre-tax Income", None),
        ("Taxes", [228, 186, 147]),
        ("Net Income", None)
    ]
    
    current_row = start_row + 1
    is_rows = {} # Cache row numbers for formula building
    
    for item, actuals in line_items:
        ws.cell(row=current_row, column=2, value=item)
        is_rows[item] = current_row
        
        is_subtotal = actuals is None
        if is_subtotal:
            ws.cell(row=current_row, column=2).font = bold_font
            
            for i in range(len(years)):
                col = start_col + i
                col_letter = get_column_letter(col)
                cell = ws.cell(row=current_row, column=col)
                cell.font = bold_font
                cell.number_format = "#,##0"
                
                # Dynamic subtotal formulas
                if item == "Gross Profit":
                    cell.value = f"={col_letter}{is_rows['Revenue']}-{col_letter}{is_rows['COGS']}"
                    cell.border = top_border
                elif item == "Operating Income":
                    cell.value = f"={col_letter}{is_rows['Gross Profit']}-{col_letter}{is_rows['Selling, general & administrative']}-{col_letter}{is_rows['Research & development']}"
                    cell.border = top_border
                elif item == "Pre-tax Income":
                    cell.value = f"={col_letter}{is_rows['Operating Income']}+{col_letter}{is_rows['Other income / (expense), net']}"
                    cell.border = top_border
                elif item == "Net Income":
                    cell.value = f"={col_letter}{is_rows['Pre-tax Income']}-{col_letter}{is_rows['Taxes']}"
                    cell.border = top_bottom_border
        else:
            # Write historical actuals
            for i, val in enumerate(actuals):
                col = start_col + i
                cell = ws.cell(row=current_row, column=col, value=val)
                cell.font = input_font
                cell.number_format = "#,##0"
                
        current_row += 1
        
    # --- Assumptions Section ---
    current_row += 2
    ws.cell(row=current_row, column=2, value="Income Statement Assumptions").font = Font(bold=True)
    current_row += 1
    
    # Re-write timeline for assumptions
    ws.cell(row=current_row, column=2).fill = header_fill
    for i, year in enumerate(years):
        col = start_col + i
        cell = ws.cell(row=current_row, column=col, value=year)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        cell.number_format = '0"A"' if year in actual_years else '0"E"'
            
    current_row += 1
    
    assump_items = [
        "Revenue Growth Rate",
        "COGS as % of Revenue",
        "SG&A as % of Revenue",
        "R&D as % of Revenue",
        "Other income / (expense), net",
        "Tax Rate"
    ]
    
    assump_rows = {}
    for item in assump_items:
        ws.cell(row=current_row, column=2, value=item)
        assump_rows[item] = current_row
        
        # Calculate historical margins/growth (starts year 2 for growth)
        for i in range(1, len(actual_years)):
            col = start_col + i
            col_letter = get_column_letter(col)
            prev_col_letter = get_column_letter(col - 1)
            
            cell = ws.cell(row=current_row, column=col)
            cell.number_format = "0.0%"
            
            if item == "Revenue Growth Rate":
                cell.value = f"=({col_letter}{is_rows['Revenue']}/{prev_col_letter}{is_rows['Revenue']})-1"
            elif item == "COGS as % of Revenue":
                cell.value = f"={col_letter}{is_rows['COGS']}/{col_letter}{is_rows['Revenue']}"
            elif item == "SG&A as % of Revenue":
                cell.value = f"={col_letter}{is_rows['Selling, general & administrative']}/{col_letter}{is_rows['Revenue']}"
            elif item == "R&D as % of Revenue":
                cell.value = f"={col_letter}{is_rows['Research & development']}/{col_letter}{is_rows['Revenue']}"
            elif item == "Other income / (expense), net":
                cell.value = f"={col_letter}{is_rows['Other income / (expense), net']}"
                cell.number_format = "#,##0"
            elif item == "Tax Rate":
                cell.value = 0.25
                cell.font = input_font
                
        # Project forecast assumptions
        for i in range(len(actual_years), len(years)):
            col = start_col + i
            col_letter = get_column_letter(col)
            cell = ws.cell(row=current_row, column=col)
            
            if item in ["Tax Rate", "Other income / (expense), net"]:
                # Flat carry forward
                cell.value = f"={get_column_letter(col-1)}{current_row}"
                cell.number_format = "#,##0" if item == "Other income / (expense), net" else "0.0%"
            else:
                # Average of historicals
                actuals_range = f"{get_column_letter(start_col+1)}{current_row}:{get_column_letter(start_col+len(actual_years)-1)}{current_row}"
                cell.value = f"=AVERAGE({actuals_range})"
                cell.number_format = "0.0%"
                
        current_row += 1
        
    # --- Link Forecast Periods ---
    for i in range(len(actual_years), len(years)):
        col = start_col + i
        col_letter = get_column_letter(col)
        prev_col = get_column_letter(col - 1)
        
        ws.cell(row=is_rows["Revenue"], column=col).value = f"={prev_col}{is_rows['Revenue']}*(1+{col_letter}{assump_rows['Revenue Growth Rate']})"
        ws.cell(row=is_rows["COGS"], column=col).value = f"={col_letter}{is_rows['Revenue']}*{col_letter}{assump_rows['COGS as % of Revenue']}"
        ws.cell(row=is_rows["Selling, general & administrative"], column=col).value = f"={col_letter}{is_rows['Revenue']}*{col_letter}{assump_rows['SG&A as % of Revenue']}"
        ws.cell(row=is_rows["Research & development"], column=col).value = f"={col_letter}{is_rows['Revenue']}*{col_letter}{assump_rows['R&D as % of Revenue']}"
        ws.cell(row=is_rows["Other income / (expense), net"], column=col).value = f"={col_letter}{assump_rows['Other income / (expense), net']}"
        ws.cell(row=is_rows["Taxes"], column=col).value = f"={col_letter}{is_rows['Pre-tax Income']}*{col_letter}{assump_rows['Tax Rate']}"
        
        # Apply standard number formatting to forecast outputs
        for row in [is_rows["Revenue"], is_rows["COGS"], is_rows["Selling, general & administrative"], 
                    is_rows["Research & development"], is_rows["Other income / (expense), net"], is_rows["Taxes"]]:
            ws.cell(row=row, column=col).number_format = "#,##0"
        
    # Sizing and Window Freezing
    ws.column_dimensions['B'].width = 36
    for i in range(len(years)):
        ws.column_dimensions[get_column_letter(start_col + i)].width = 13
        
    # Freeze panes below the timeline and right of the labels
    ws.freeze_panes = ws.cell(row=start_row+1, column=start_col)
```