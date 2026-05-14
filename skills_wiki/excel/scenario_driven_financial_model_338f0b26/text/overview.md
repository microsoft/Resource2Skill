### 1. High-level Skill Pattern Extraction

> **Skill Name**: Scenario-Driven Financial Model

* **Tier**: sheet_shell
* **Core Mechanism**: Uses a Data Validation dropdown and the `CHOOSE` function to route selected scenario data into a dedicated "Live Assumptions" block. The main calculation engine (Income Statement) references only the live block, allowing instant scenario toggling without duplicating business logic.
* **Applicability**: Best used for financial projections, sensitivity analysis, or driver-based forecasts where you need to toggle between distinct assumption sets (e.g., Base, Best, Worst case) cleanly on a single sheet.

### 2. Structural Breakdown

- **Data Layout**: An output block (Income Statement) sits at the top, fed by a "Live Assumptions" block in the middle. Distinct hardcoded scenario tables (Optimistic, Pessimistic) reside at the bottom. Column B holds labels; Columns C-G represent forecast periods (Years 1-5).
- **Formula Logic**: Features `=CHOOSE($G$2, C18, C24)` to pull values from Scenario 1 (Row 18) or Scenario 2 (Row 24) dynamically into the live row based on the toggle. Standard calculation links (`=Orders * AOV`) drive the output block.
- **Visual Design**: Themed header backgrounds visually separate the data regions. The toggle cell stands out with a bright warning/accent fill and border. Summary rows like Gross Profit and Operating Profit use bold font styling.
- **Charts/Tables**: Clean tabular layout relying on uniform column widths (Width 15 for data columns, 25 for labels).
- **Theme Hooks**: Primary palette color injected directly as `header_fill` to stylize the section dividers.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Financial Model", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a dynamic Income Statement driven by togglable assumption scenarios.
    """
    ws = wb.create_sheet(sheet_name)
    
    # Setup styles
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    bold_font = Font(bold=True)
    toggle_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    border_thin = Border(outline=Side(style="thin", color="000000"))
    
    # 1. Title & Scenario Toggle Setup
    ws["B2"] = title
    ws["B2"].font = Font(size=14, bold=True)
    
    ws["F2"] = "Scenario:"
    ws["F2"].font = bold_font
    ws["F2"].alignment = Alignment(horizontal="right")
    
    ws["G2"] = 1
    ws["G2"].fill = toggle_fill
    ws["G2"].border = border_thin
    ws["G2"].alignment = Alignment(horizontal="center")
    
    # Add Data Validation for the toggle (1 = Optimistic, 2 = Pessimistic)
    dv = DataValidation(type="list", formula1='"1,2"', allowBlank=False)
    ws.add_data_validation(dv)
    dv.add(ws["G2"])
    
    years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    
    # Helper to build block headers
    def write_section_header(row, text):
        c_label = ws.cell(row=row, column=2, value=text)
        c_label.font = header_font
        c_label.fill = header_fill
        for i, year in enumerate(years, start=3):
            c_yr = ws.cell(row=row, column=i, value=year)
            c_yr.font = header_font
            c_yr.fill = header_fill
            c_yr.alignment = Alignment(horizontal="center")
            
    # Section 1: Income Statement (Output)
    write_section_header(4, "Income Statement")
    is_labels = ["Revenue", "COGS", "Gross Profit", "Operating Expenses", "Operating Profit"]
    for i, label in enumerate(is_labels, start=5):
        ws.cell(row=i, column=2, value=label)
        if label in ["Gross Profit", "Operating Profit"]:
            ws.cell(row=i, column=2).font = bold_font
            
    # Section 2: Live Assumptions (Dynamic Feed)
    write_section_header(11, "Live Assumptions")
    assump_labels = ["Number of Orders", "Average Order Value", "COGS per Order", "Fixed OpEx"]
    for i, label in enumerate(assump_labels, start=12):
        ws.cell(row=i, column=2, value=label)
        
    # Section 3: Scenario 1 (Hardcoded)
    write_section_header(17, "Scenario 1 (Optimistic)")
    for i, label in enumerate(assump_labels, start=18):
        ws.cell(row=i, column=2, value=label)
        
    # Section 4: Scenario 2 (Hardcoded)
    write_section_header(23, "Scenario 2 (Pessimistic)")
    for i, label in enumerate(assump_labels, start=24):
        ws.cell(row=i, column=2, value=label)

    # Populate Scenario 1 Data
    scen1_data = [
        [3000, 6000, 10500, 15750, 21263],
        [40, 40, 40, 40, 40],
        [8.75, 8.75, 8.75, 8.75, 8.75],
        [20000, 20000, 30000, 30000, 30000]
    ]
    for row_offset, data in enumerate(scen1_data):
        for col_offset, val in enumerate(data):
            ws.cell(row=18 + row_offset, column=3 + col_offset, value=val)
            
    # Populate Scenario 2 Data
    scen2_data = [
        [2000, 4000, 7000, 10500, 14175],
        [35, 35, 35, 35, 35],
        [8.75, 8.75, 8.75, 8.75, 8.75],
        [20000, 25000, 25000, 30000, 30000]
    ]
    for row_offset, data in enumerate(scen2_data):
        for col_offset, val in enumerate(data):
            ws.cell(row=24 + row_offset, column=3 + col_offset, value=val)
            
    # Inject Formulas (Live routing and logic)
    for c in range(3, 8):
        col_let = get_column_letter(c)
        
        # CHOOSE formulas for Live Assumptions
        for r in range(12, 16):
            s1_row = r + 6
            s2_row = r + 12
            ws[f"{col_let}{r}"] = f"=CHOOSE($G$2, {col_let}{s1_row}, {col_let}{s2_row})"
            
        # Calculation Engine (Income Statement)
        ws[f"{col_let}5"] = f"={col_let}12*{col_let}13"      # Revenue = Orders * AOV
        ws[f"{col_let}6"] = f"={col_let}12*{col_let}14"      # COGS = Orders * COGS/Order
        ws[f"{col_let}7"] = f"={col_let}5-{col_let}6"        # Gross Profit
        ws[f"{col_let}7"].font = bold_font
        ws[f"{col_let}8"] = f"={col_let}15"                  # OpEx
        ws[f"{col_let}9"] = f"={col_let}7-{col_let}8"        # Operating Profit
        ws[f"{col_let}9"].font = bold_font
        
    # Standardize column widths
    for col in range(3, 8):
        ws.column_dimensions[get_column_letter(col)].width = 15
    ws.column_dimensions['B'].width = 25
```