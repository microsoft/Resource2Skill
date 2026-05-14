### 1. High-level Skill Pattern Extraction

> **Skill Name**: Financial Model Income Statement Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Builds a standard 3-statement financial model shell featuring timeline columns split between historicals and forecasts. Uses custom number formats (`0"A"` for Actuals, `0"E"` for Estimates) to label years dynamically, applies standard color-coding (blue for hardcoded inputs, black for calculations), adds subtotal border rules, and groups an assumption driver block below the statement.
* **Applicability**: Essential for building robust financial models, valuations, and budget forecasts. This specific structure enforces clean separation of inputs vs. calculations and simplifies auditing.

### 2. Structural Breakdown

- **Data Layout**: Line items in Column B. Timeline stretching right from Column C. Includes an Income Statement section (Rows 4-10) and an Assumptions block below it.
- **Formula Logic**: Calculates historical margins and growth rates backwards. Forecasts step forward by referencing the assumption block (e.g., Forecast Revenue = `Prev Year * (1 + Growth Rate)`).
- **Visual Design**: 
  - Standard finance color-coding: `Font(color="0000FF")` for hardcoded assumptions/actuals, `Font(color="000000")` for formulas.
  - Custom number format: `0"A"` and `0"E"` automatically append "A" or "E" to year integer values.
  - Subtotals use bold fonts and top/bottom borders.
- **Charts/Tables**: Freezes panes at `C4` so timeline headers and line item descriptions remain visible while scrolling. Groups assumption rows.
- **Theme Hooks**: Primary dark blue background for the timeline and section headers. 

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, start_year: int = 2023, actual_years: int = 3, forecast_years: int = 5, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Financial modeling standard formatting
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    input_font = Font(color="0000FF") # Blue for manual/hardcoded inputs
    calc_font = Font(color="000000")  # Black for formula calculations
    bold_calc_font = Font(color="000000", bold=True)
    
    tb_border = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    
    ws.column_dimensions['B'].width = 32
    for i in range(actual_years + forecast_years):
        ws.column_dimensions[get_column_letter(3 + i)].width = 13
        
    # --- TIMELINE HEADER ---
    ws.cell(row=3, column=2, value="Income Statement").fill = header_fill
    ws.cell(row=3, column=2).font = header_font
    
    for i in range(actual_years + forecast_years):
        col = 3 + i
        cell = ws.cell(row=3, column=col, value=start_year + i)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
        
        # Custom format: 0"A" for Actuals, 0"E" for Estimates
        if i < actual_years:
            cell.number_format = '0"A"'
        else:
            cell.number_format = '0"E"'
            
    # Freeze panes below header and right of line items
    ws.freeze_panes = "C4"
    
    # --- LINE ITEMS ---
    items = [
        ("Revenue", "line"),
        ("COGS", "line"),
        ("Gross Profit", "subtotal"),
        ("Operating Expenses", "line"),
        ("Operating Income", "subtotal"),
        ("Taxes", "line"),
        ("Net Income", "total")
    ]
    
    for r_idx, (item, itype) in enumerate(items, start=4):
        ws.cell(row=r_idx, column=2, value=item)
        if itype in ("subtotal", "total"):
            ws.cell(row=r_idx, column=2).font = bold_calc_font
            
    # --- ASSUMPTIONS BLOCK ---
    assump_start = 4 + len(items) + 2
    ws.cell(row=assump_start, column=2, value="Income Statement Assumptions").fill = header_fill
    ws.cell(row=assump_start, column=2).font = header_font
    
    assumptions = [
        "Revenue Growth Rate",
        "COGS as % of Revenue",
        "OpEx as % of Revenue",
        "Tax Rate"
    ]
    for r_idx, item in enumerate(assumptions, start=assump_start+1):
        ws.cell(row=r_idx, column=2, value=item)
        
    # Group assumption rows so they can be collapsed
    ws.row_dimensions.group(assump_start+1, assump_start+len(assumptions), hidden=False)
    
    # --- FILL MOCK DATA & FORMULAS ---
    # Setup Actuals
    for i in range(actual_years):
        col = 3 + i
        c_letter = get_column_letter(col)
        
        rev_cell = ws.cell(row=4, column=col, value=5000 * (1.08 ** i))
        rev_cell.font = input_font
        
        cogs_cell = ws.cell(row=5, column=col, value=2000 * (1.05 ** i))
        cogs_cell.font = input_font
        
        gp_cell = ws.cell(row=6, column=col, value=f"={c_letter}4-{c_letter}5")
        gp_cell.font = bold_calc_font
        gp_cell.border = tb_border
        
        opex_cell = ws.cell(row=7, column=col, value=1200 * (1.03 ** i))
        opex_cell.font = input_font
        
        oi_cell = ws.cell(row=8, column=col, value=f"={c_letter}6-{c_letter}7")
        oi_cell.font = bold_calc_font
        oi_cell.border = tb_border
        
        tax_cell = ws.cell(row=9, column=col, value=f"={c_letter}8*0.25")
        tax_cell.font = calc_font
        
        ni_cell = ws.cell(row=10, column=col, value=f"={c_letter}8-{c_letter}9")
        ni_cell.font = bold_calc_font
        ni_cell.border = tb_border
        
        # Calculate historical assumptions
        if i > 0:
            prev_col = get_column_letter(col - 1)
            ws.cell(row=assump_start+1, column=col, value=f"=({c_letter}4/{prev_col}4)-1").font = calc_font
        ws.cell(row=assump_start+2, column=col, value=f"={c_letter}5/{c_letter}4").font = calc_font
        ws.cell(row=assump_start+3, column=col, value=f"={c_letter}7/{c_letter}4").font = calc_font
        ws.cell(row=assump_start+4, column=col, value=0.25).font = input_font
        
        # Formatting formats
        for r in range(4, 11):
            ws.cell(row=r, column=col).number_format = '#,##0'
        for r in range(assump_start+1, assump_start+5):
            ws.cell(row=r, column=col).number_format = '0.0%'

    # Setup Estimates (Forecast)
    for i in range(forecast_years):
        col = 3 + actual_years + i
        c_letter = get_column_letter(col)
        prev_col = get_column_letter(col - 1)
        
        # Hardcode forward-looking assumptions (Blue)
        ws.cell(row=assump_start+1, column=col, value=0.10).font = input_font
        ws.cell(row=assump_start+2, column=col, value=0.40).font = input_font
        ws.cell(row=assump_start+3, column=col, value=0.22).font = input_font
        ws.cell(row=assump_start+4, column=col, value=0.25).font = input_font
        
        # Drive statements from assumptions (Black)
        ws.cell(row=4, column=col, value=f"={prev_col}4*(1+{c_letter}{assump_start+1})").font = calc_font
        ws.cell(row=5, column=col, value=f"={c_letter}4*{c_letter}{assump_start+2}").font = calc_font
        ws.cell(row=6, column=col, value=f"={c_letter}4-{c_letter}5").font = bold_calc_font
        ws.cell(row=6, column=col).border = tb_border
        
        ws.cell(row=7, column=col, value=f"={c_letter}4*{c_letter}{assump_start+3}").font = calc_font
        ws.cell(row=8, column=col, value=f"={c_letter}6-{c_letter}7").font = bold_calc_font
        ws.cell(row=8, column=col).border = tb_border
        
        ws.cell(row=9, column=col, value=f"={c_letter}8*{c_letter}{assump_start+4}").font = calc_font
        ws.cell(row=10, column=col, value=f"={c_letter}8-{c_letter}9").font = bold_calc_font
        ws.cell(row=10, column=col).border = tb_border
        
        # Formatting formats
        for r in range(4, 11):
            ws.cell(row=r, column=col).number_format = '#,##0'
        for r in range(assump_start+1, assump_start+5):
            ws.cell(row=r, column=col).number_format = '0.0%'
```