### 1. High-level Skill Pattern Extraction

> **Skill Name**: Standard Income Statement Model

* **Tier**: sheet_shell
* **Core Mechanism**: Generates a standard financial modeling Income Statement with a split historical/forecast timeline, custom year formatting (`0"A"` vs `0"E"`), grouped sections for the main statement and assumptions, and strict modeling color conventions (blue font for hardcoded inputs, black for formulas).
* **Applicability**: Foundational for any financial model, valuation, or budgeting task requiring a projected income statement driven by margin and growth assumptions. 

### 2. Structural Breakdown

- **Data Layout**: Column A is a spacer. Column B contains line-item labels. Columns C onward contain the timeline (e.g., 2023-2027). The sheet is split into two vertical blocks: the Income Statement and the Assumptions/Drivers.
- **Formula Logic**: Standard financial subtotals (Gross Profit = Revenue - COGS; Operating Income = Gross Profit - OPEX). Forecast periods use driver-based formulas (e.g., `Prior Year Revenue * (1 + Growth Rate)` and `Current Year Revenue * Margin %`).
- **Visual Design**: Header rows use a solid background with bold white text. Subtotals use a thin top border with bold text. The "Net Income" line uses top and bottom borders (or double bottom). Hardcoded inputs are strictly colored blue (`#0000FF`), while formulas remain default black. Custom number formats `0"A"` and `0"E"` visually distinguish historical vs. estimated periods.
- **Charts/Tables**: Standard spreadsheet grid layout without Excel Tables (as is standard practice for dynamic financial models to allow flexible column-wise formulas).
- **Theme Hooks**: Uses `primary` or `dark` for the header background, and standard financial blue for input fonts. 

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Income Statement", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Generates a dynamic 5-year Income Statement model with historical and forecast periods.
    Separates inputs (blue font) from calculations (black font) and includes a driver assumptions section.
    """
    ws = wb.create_sheet(title=sheet_name)
    
    # Theme configuration
    # In a real framework, these would be loaded from a theme registry based on the 'theme' arg.
    theme_colors = {
        "corporate_blue": {"header_bg": "1F4E78", "header_fg": "FFFFFF", "accent": "D9E1F2"},
        "fintech_green": {"header_bg": "2E7D32", "header_fg": "FFFFFF", "accent": "E8F5E9"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    # Style Definitions
    header_fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    header_font = Font(color=palette["header_fg"], bold=True)
    bold_font = Font(bold=True)
    input_font = Font(color="0000FF") # Financial modeling standard for hardcoded inputs
    
    top_border = Border(top=Side(style='thin', color='000000'))
    bottom_border = Border(bottom=Side(style='thin', color='000000'))
    top_bottom_border = Border(top=Side(style='thin', color='000000'), bottom=Side(style='double', color='000000'))
    
    num_fmt_history = '0"A"'
    num_fmt_forecast = '0"E"'
    num_fmt_dollars = '#,##0'
    num_fmt_percent = '0.0%'
    
    # --- Layout Configuration ---
    hist_years = 2
    fcst_years = 3
    start_year = 2023
    total_years = hist_years + fcst_years
    
    # Configure Columns
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 35
    for i in range(total_years):
        col_letter = get_column_letter(3 + i)
        ws.column_dimensions[col_letter].width = 12

    # --- 1. Header & Timeline ---
    ws['B2'] = title
    ws['B2'].font = Font(size=14, bold=True)
    
    for i in range(total_years):
        col = 3 + i
        cell = ws.cell(row=3, column=col)
        cell.value = start_year + i
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        cell.number_format = num_fmt_history if i < hist_years else num_fmt_forecast
        
    ws['B3'].fill = header_fill

    # --- 2. Line Items Configuration ---
    # (Row index, Label, Is_Subtotal, Format, Input_Rows_History)
    is_structure = [
        (4, "Revenue", False, num_fmt_dollars, [5210, 5435]),
        (5, "Cost of Goods Sold (COGS)", False, num_fmt_dollars, [3345, 3350]),
        (6, "Gross Profit", True, num_fmt_dollars, []),
        (7, "Selling, General & Admin (SG&A)", False, num_fmt_dollars, [850, 870]),
        (8, "Research & Development (R&D)", False, num_fmt_dollars, [400, 420]),
        (9, "Operating Income", True, num_fmt_dollars, []),
        (10, "Other Income / (Expense)", False, num_fmt_dollars, [50, 50]),
        (11, "Pre-tax Income", True, num_fmt_dollars, []),
        (12, "Taxes", False, num_fmt_dollars, [228, 186]),
        (13, "Net Income", True, num_fmt_dollars, []),
    ]
    
    for row_idx, label, is_sub, fmt, hist_data in is_structure:
        ws.cell(row=row_idx, column=2, value=label)
        if is_sub:
            ws.cell(row=row_idx, column=2).font = bold_font
            
        # Insert historical data
        if not is_sub:
            for i, val in enumerate(hist_data):
                c = ws.cell(row=row_idx, column=3+i, value=val)
                c.number_format = fmt
                c.font = input_font # Blue for inputs
                
    # --- 3. Assumptions Section ---
    ws['B16'] = "Income Statement Assumptions"
    ws['B16'].font = bold_font
    ws['B16'].fill = PatternFill(start_color=palette["accent"], end_color=palette["accent"], fill_type="solid")
    
    assumptions = [
        (17, "Revenue Growth Rate", num_fmt_percent, [0.043], [0.051, 0.047, 0.047]),
        (18, "COGS as % of Revenue", num_fmt_percent, [0.642, 0.616], [0.622, 0.627, 0.627]),
        (19, "SG&A as % of Revenue", num_fmt_percent, [0.163, 0.160], [0.158, 0.160, 0.160]),
        (20, "R&D as % of Revenue", num_fmt_percent, [0.077, 0.077], [0.070, 0.075, 0.075]),
        (21, "Tax Rate", num_fmt_percent, [0.25, 0.25], [0.25, 0.25, 0.25])
    ]
    
    for row_idx, label, fmt, hist_data, fcst_data in assumptions:
        ws.cell(row=row_idx, column=2, value=label)
        
        # Hist inputs
        for i, val in enumerate(hist_data):
            # Only plug if we actually have a dummy value for that historical year
            col_idx = 3 + (hist_years - len(hist_data)) + i
            c = ws.cell(row=row_idx, column=col_idx, value=val)
            c.number_format = fmt
            c.font = input_font
            
        # Forecast inputs
        for i, val in enumerate(fcst_data):
            c = ws.cell(row=row_idx, column=3 + hist_years + i, value=val)
            c.number_format = fmt
            c.font = input_font

    # --- 4. Dynamic Formulas ---
    # Apply formulas across the entire timeline where applicable
    for i in range(total_years):
        col_idx = 3 + i
        col_let = get_column_letter(col_idx)
        prev_col_let = get_column_letter(col_idx - 1) if i > 0 else None
        
        # Gross Profit = Rev - COGS
        gp_cell = ws.cell(row=6, column=col_idx, value=f"={col_let}4-{col_let}5")
        gp_cell.font = bold_font
        gp_cell.border = top_border
        gp_cell.number_format = num_fmt_dollars
        
        # Operating Income = GP - SG&A - R&D
        op_cell = ws.cell(row=9, column=col_idx, value=f"={col_let}6-{col_let}7-{col_let}8")
        op_cell.font = bold_font
        op_cell.border = top_border
        op_cell.number_format = num_fmt_dollars
        
        # Pre-tax = OpInc + Other
        pt_cell = ws.cell(row=11, column=col_idx, value=f"={col_let}9+{col_let}10")
        pt_cell.font = bold_font
        pt_cell.border = top_border
        pt_cell.number_format = num_fmt_dollars
        
        # Net Income = Pre-tax - Taxes
        ni_cell = ws.cell(row=13, column=col_idx, value=f"={col_let}11-{col_let}12")
        ni_cell.font = bold_font
        ni_cell.border = top_bottom_border
        ni_cell.number_format = num_fmt_dollars
        
        # Apply forecast-specific driver formulas
        if i >= hist_years:
            # Revenue = Prev Rev * (1 + Growth)
            r_cell = ws.cell(row=4, column=col_idx, value=f"={prev_col_let}4*(1+{col_let}17)")
            r_cell.number_format = num_fmt_dollars
            
            # COGS = Rev * COGS%
            c_cell = ws.cell(row=5, column=col_idx, value=f"={col_let}4*{col_let}18")
            c_cell.number_format = num_fmt_dollars
            
            # SG&A = Rev * SG&A%
            s_cell = ws.cell(row=7, column=col_idx, value=f"={col_let}4*{col_let}19")
            s_cell.number_format = num_fmt_dollars
            
            # R&D = Rev * R&D%
            rd_cell = ws.cell(row=8, column=col_idx, value=f"={col_let}4*{col_let}20")
            rd_cell.number_format = num_fmt_dollars
            
            # Other Income stays flat (carry forward)
            o_cell = ws.cell(row=10, column=col_idx, value=f"={prev_col_let}10")
            o_cell.number_format = num_fmt_dollars
            
            # Taxes = Pre-tax * Tax Rate
            tx_cell = ws.cell(row=12, column=col_idx, value=f"={col_let}11*{col_let}21")
            tx_cell.number_format = num_fmt_dollars

    # Formatting refinements (freeze panes for easy scrolling)
    ws.freeze_panes = "C4"
```