### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Financial Model with Scenario Control

* **Tier**: archetype
* **Core Mechanism**: Builds a multi-sheet financial forecasting template. Establishes a central "Cover" sheet with a Data Validated scenario toggle (Best/Base/Worst) that drives calculation states on an "Income Statement" sheet using the `CHOOSE` formula. Implements dynamic timeline headers with custom formatting (`0"A"` for actuals, `0"E"` for estimates), table of contents hyperlinking, row grouping for assumptions, and frozen panes. 
* **Applicability**: Financial planning & analysis (FP&A), three-statement modeling, and reporting scenarios where business assumptions need to be centrally toggled to stress-test financial outcomes.

### 2. Structural Breakdown

- **Data Layout**: Two sheets: `Cover` (Control Panel) and `Income Statement` (P&L schedule). The P&L separates historical actuals from projected years, splitting calculations between core line items (rows 4-12) and forecasting assumptions (rows 15-24).
- **Formula Logic**: Uses `=CHOOSE('Cover'!$B$5, [Best], [Base], [Worst])` to pipe the selected scenario index into the active Revenue Growth assumption. Subsequent line items (COGS, SG&A) scale as a `% of Revenue`.
- **Visual Design**: Uses thematic fills for headers, specific input text colors (blue) to distinguish hard-coded assumptions from formulas, subtotal/total border layers, and dynamic custom number formats (`0"A"` / `0"E"`) on the timeline.
- **Charts/Tables**: Employs structural row grouping (`row_dimensions.group`) to collapse assumption blocks and scenario rate tables, keeping the core P&L uncluttered.
- **Theme Hooks**: Consumes `primary` for headers, `primary_text` for header fonts, `bg_accent` for the live scenario input toggle, and `input_text` for hardcoded driving values.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, company_name: str = "Sample Inc.", start_year: int = 2023, hist_years: int = 2, forecast_years: int = 5, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Generates a foundational financial model archetype featuring a central 
    scenario control cover page and a dynamic forecasting income statement.
    """
    
    # Mock palette (Framework will inject actual theme dictionary)
    palette = {
        "primary": "1F4E78",
        "primary_text": "FFFFFF",
        "bg_accent": "FFF2CC",
        "input_text": "0000FF",
        "group_bg": "F2F2F2",
        "link": "0563C1"
    }

    # 1. Initialize Sheets
    if "Sheet" in wb.sheetnames:
        cover_ws = wb["Sheet"]
        cover_ws.title = "Cover"
    else:
        cover_ws = wb.create_sheet("Cover")
        
    is_ws = wb.create_sheet("Income Statement")
    
    # 2. Shared Styles
    header_fill = PatternFill(start_color=palette["primary"], fill_type="solid")
    header_font = Font(color=palette["primary_text"], bold=True)
    bold_font = Font(bold=True)
    title_font = Font(size=16, bold=True)
    input_font = Font(color=palette["input_text"])
    link_font = Font(color=palette["link"], underline="single")
    
    subtotal_border = Border(top=Side(style="thin"))
    total_border = Border(top=Side(style="thin"), bottom=Side(style="double"))
    
    # ==========================================
    # SHEET 1: COVER (CONTROL PANEL)
    # ==========================================
    cover_ws["A1"] = f"{company_name} Financial Model"
    cover_ws["A1"].font = title_font
    
    # Scenario Analysis Setup
    cover_ws["A4"] = "Scenario Analysis"
    cover_ws["A4"].font = header_font
    cover_ws["A4"].fill = header_fill
    cover_ws["B4"].fill = header_fill
    cover_ws.merge_cells("A4:B4")
    
    cover_ws["A5"] = "Live Scenario"
    cover_ws["B5"] = 2  # Default to Base Case (2)
    cover_ws["B5"].fill = PatternFill(start_color=palette["bg_accent"], fill_type="solid")
    cover_ws["B5"].font = input_font
    cover_ws["B5"].alignment = Alignment(horizontal="center")
    
    # Data Validation for Scenario Dropdown
    dv = DataValidation(type="list", formula1='"1,2,3"', showDropDown=True)
    dv.errorTitle = 'Invalid Entry'
    dv.error = 'Select a scenario index: 1 (Best), 2 (Base), or 3 (Worst)'
    cover_ws.add_data_validation(dv)
    dv.add(cover_ws["B5"])
    
    cover_ws["A6"] = "1 = Best Case, 2 = Base Case, 3 = Worst Case"
    cover_ws["A6"].font = Font(italic=True, size=9)
    
    # Table of Contents
    cover_ws["D4"] = "Table of Contents"
    cover_ws["D4"].font = header_font
    cover_ws["D4"].fill = header_fill
    cover_ws["E4"].fill = header_fill
    cover_ws.merge_cells("D4:E4")
    
    cover_ws["D5"] = "Cover Page"
    cover_ws["D5"].hyperlink = "#'Cover'!A1"
    cover_ws["D5"].font = link_font
    
    cover_ws["D6"] = "Income Statement"
    cover_ws["D6"].hyperlink = "#'Income Statement'!A1"
    cover_ws["D6"].font = link_font
    
    cover_ws.column_dimensions['A'].width = 20
    cover_ws.column_dimensions['D'].width = 20
    
    # ==========================================
    # SHEET 2: INCOME STATEMENT
    # ==========================================
    is_ws["A1"] = f"{company_name} Income Statement"
    is_ws["A1"].font = title_font
    is_ws["A3"] = "($ in millions)"
    is_ws["A3"].font = Font(italic=True)
    
    total_years = hist_years + forecast_years
    start_col = 3  # Start in Column C
    
    # Build Dynamic Timeline
    for i in range(total_years):
        col_letter = get_column_letter(start_col + i)
        cell = is_ws[f"{col_letter}3"]
        cell.value = start_year + i
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        
        # Format "A" for Actuals, "E" for Estimates
        if i < hist_years:
            cell.number_format = '0"A"'
        else:
            cell.number_format = '0"E"'
            
    # Stub out Line Items
    labels = [
        (4, "Revenue"), (5, "Cost of Goods Sold (COGS)"), (6, "Gross Profit"),
        (7, "Selling, General & Admin (SG&A)"), (8, "Research & Development"),
        (9, "Operating Income"), (10, "Pre-tax Income"), (11, "Taxes"), (12, "Net Income"),
        (14, "Model Assumptions"), (15, "Revenue Growth Rate"), (16, "COGS % of Rev"),
        (17, "SG&A % of Rev"), (18, "R&D % of Rev"), (19, "Effective Tax Rate"),
        (21, "Revenue Scenarios"), (22, "Best Case"), (23, "Base Case"), (24, "Worst Case")
    ]
    
    for r, label in labels:
        is_ws.cell(row=r, column=2, value=label)
        if r in (6, 9, 10, 12, 14, 21):
            is_ws.cell(row=r, column=2).font = bold_font
        if r in (14, 21):
            fill = PatternFill(start_color=palette["group_bg"], fill_type="solid")
            for c in range(2, start_col + total_years):
                is_ws.cell(row=r, column=c).fill = fill
                
    is_ws.column_dimensions['B'].width = 30
    
    # Group assumption rows
    is_ws.row_dimensions.group(15, 19, hidden=False)
    is_ws.row_dimensions.group(22, 24, hidden=True)
    
    # Lock Panes for scrolling
    is_ws.freeze_panes = "C4"
    
    # Historical Data Payload
    hist_data = {
        0: {"Rev": 5210, "COGS": 3345, "SGA": 850, "RD": 400, "Tax": 0.25},
        1: {"Rev": 5435, "COGS": 3350, "SGA": 870, "RD": 420, "Tax": 0.25}
    }
    
    # Calculate Core Model
    for i in range(total_years):
        c_let = get_column_letter(start_col + i)
        p_let = get_column_letter(start_col + i - 1) if i > 0 else ""
        
        # Base Formats
        for r in [15, 16, 17, 18, 19, 22, 23, 24]:
            is_ws[f"{c_let}{r}"].number_format = "0.0%"
        for r in range(4, 13):
            is_ws[f"{c_let}{r}"].number_format = "#,##0"
        
        # Historical Population
        if i < hist_years:
            is_ws[f"{c_let}4"] = hist_data[i]["Rev"]
            is_ws[f"{c_let}5"] = hist_data[i]["COGS"]
            is_ws[f"{c_let}7"] = hist_data[i]["SGA"]
            is_ws[f"{c_let}8"] = hist_data[i]["RD"]
            is_ws[f"{c_let}19"] = hist_data[i]["Tax"]
            
            for r in (4, 5, 7, 8, 19):
                is_ws[f"{c_let}{r}"].font = input_font
            
            # Historical Derived Metrics
            is_ws[f"{c_let}15"] = f"=({c_let}4/{p_let}4)-1" if i > 0 else "-"
            is_ws[f"{c_let}16"] = f"={c_let}5/{c_let}4"
            is_ws[f"{c_let}17"] = f"={c_let}7/{c_let}4"
            is_ws[f"{c_let}18"] = f"={c_let}8/{c_let}4"
            
        # Forecast Population
        else:
            # Inputs
            is_ws[f"{c_let}16"] = 0.616
            is_ws[f"{c_let}17"] = 0.160
            is_ws[f"{c_let}18"] = 0.075
            is_ws[f"{c_let}19"] = 0.250
            
            is_ws[f"{c_let}22"] = 0.067
            is_ws[f"{c_let}23"] = 0.047
            is_ws[f"{c_let}24"] = 0.027
            
            for r in (16, 17, 18, 19, 22, 23, 24):
                is_ws[f"{c_let}{r}"].font = input_font
            
            # THE CORE SKILL: CHOOSE driven by the control panel scenario index
            is_ws[f"{c_let}15"] = f"=CHOOSE('Cover'!$B$5, {c_let}22, {c_let}23, {c_let}24)"
            
            # Forecast Statement Logic
            is_ws[f"{c_let}4"] = f"={p_let}4*(1+{c_let}15)"
            is_ws[f"{c_let}5"] = f"={c_let}4*{c_let}16"
            is_ws[f"{c_let}7"] = f"={c_let}4*{c_let}17"
            is_ws[f"{c_let}8"] = f"={c_let}4*{c_let}18"
            
        # Standard P&L Math & Styling
        is_ws[f"{c_let}6"] = f"={c_let}4-{c_let}5"
        is_ws[f"{c_let}9"] = f"={c_let}6-{c_let}7-{c_let}8"
        is_ws[f"{c_let}10"] = f"={c_let}9"
        is_ws[f"{c_let}11"] = f"={c_let}10*{c_let}19"
        is_ws[f"{c_let}12"] = f"={c_let}10-{c_let}11"
        
        is_ws[f"{c_let}6"].border = subtotal_border
        is_ws[f"{c_let}9"].border = subtotal_border
        is_ws[f"{c_let}10"].border = subtotal_border
        is_ws[f"{c_let}12"].border = total_border
```