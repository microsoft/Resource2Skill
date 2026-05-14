### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive KPI Dashboard Architecture

* **Tier**: archetype
* **Core Mechanism**: Separates data into a hidden `Staging` sheet and builds an interactive `Dashboard` using `INDEX/MATCH` to look up metrics based on a month dropdown. Applies dynamic `FormulaRule` conditional formatting to visually highlight performance versus targets.
* **Applicability**: Best for high-level executive summaries where users want to quickly toggle between reporting periods (months/quarters) to see big-picture health without sorting through raw data tables. 

### 2. Structural Breakdown

- **Data Layout**: `Staging` sheet holds horizontal time-series data (Months in row 1, KPIs and Targets in column A).
- **Formula Logic**: `=INDEX(Data, MATCH(kpi, KPIs, 0), MATCH(month, Months, 0))` fetches dynamic values. `MATCH(month) - 1` fetches the prior period, wrapped in an `IF` to handle the first period safely.
- **Visual Design**: Uses 4-cell merged blocks for large bold typography (Size 24). Grouped by category with themed header strips. Removes gridlines for a clean UI.
- **Charts/Tables**: Purely formula-driven card layout; relies on typography and color rather than charts.
- **Theme Hooks**: `primary` for section headers; `secondary` for card titles; `good`/`bad` for conditional formatting indicator backgrounds.

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

def render_workbook(wb: Workbook, *, title: str = "Executive KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup staging sheet (calculates and holds values over time)
    ws_staging = wb.active
    ws_staging.title = "Staging"
    
    staging_data = [
        ["KPI", "Jan-20", "Feb-20", "Mar-20", "Apr-20"],
        ["DSO", 45, 42, 48, 41],
        ["DSO Target", 45, 45, 45, 45],
        ["DPO", 80, 85, 90, 88],
        ["DPO Target", 90, 90, 90, 90],
        ["Gross Margin", 0.25, 0.26, 0.24, 0.28],
        ["Gross Margin Target", 0.25, 0.25, 0.25, 0.25],
        ["OPEX", 12000, 12500, 11000, 11500],
        ["OPEX Target", 12000, 12000, 12000, 12000]
    ]
    for row in staging_data:
        ws_staging.append(row)
        
    # Format specific staging rows (optional, but good practice)
    for row in range(6, 8): 
        for col in range(2, 6):
            ws_staging.cell(row=row, column=col).number_format = "0%"
            
    # Hide staging sheet so users only interact with the dashboard
    ws_staging.sheet_state = 'hidden'
            
    # 2. Setup Dashboard sheet
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    themes = {
        "corporate_blue": {"primary": "4F81BD", "secondary": "DCE6F1", "text": "000000", "good": "C6EFCE", "good_text": "006100", "bad": "FFC7CE", "bad_text": "9C0006"},
        "modern_dark": {"primary": "203764", "secondary": "D9E1F2", "text": "000000", "good": "C6EFCE", "good_text": "006100", "bad": "FFC7CE", "bad_text": "9C0006"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # Dashboard Title
    ws_dash["B2"] = title
    ws_dash["B2"].font = Font(size=20, bold=True, color=palette["primary"])
    
    # Month Selector Dropdown
    ws_dash["C3"] = "For the month of:"
    ws_dash["C3"].font = Font(italic=True)
    ws_dash["C3"].alignment = Alignment(horizontal="right")
    
    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20,Apr-20"', allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash["D3"])
    ws_dash["D3"] = "Mar-20"
    ws_dash["D3"].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    ws_dash["D3"].border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    ws_dash["D3"].alignment = Alignment(horizontal="center")
    
    # Group Headers
    ws_dash.merge_cells("B5:J5")
    ws_dash["B5"] = "Working Capital Efficiency"
    ws_dash["B5"].fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    ws_dash["B5"].font = Font(color="FFFFFF", bold=True, size=12)
    ws_dash["B5"].alignment = Alignment(horizontal="center")
    
    ws_dash.merge_cells("B11:J11")
    ws_dash["B11"] = "Sales & Cost KPIs"
    ws_dash["B11"].fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    ws_dash["B11"].font = Font(color="FFFFFF", bold=True, size=12)
    ws_dash["B11"].alignment = Alignment(horizontal="center")
    
    # Initialize uniform column widths for identical card sizes
    for col in "BCDEGHIJ":
        ws_dash.column_dimensions[col].width = 12
    ws_dash.column_dimensions["F"].width = 4  # Spacer column
    ws_dash.column_dimensions["A"].width = 2  # Left margin
    
    # Helper to stamp dynamic formula cards
    def draw_kpi_card(ws, start_row, start_col, kpi_id, kpi_title, num_format, is_lower_better=True):
        col_letters = [get_column_letter(start_col + i) for i in range(4)]
        c1, c2, c3, c4 = col_letters
        
        # 1. Card Header
        ws.merge_cells(f"{c1}{start_row}:{c4}{start_row}")
        hdr = ws[f"{c1}{start_row}"]
        hdr.value = kpi_title
        hdr.fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
        hdr.font = Font(bold=True, color=palette["text"])
        hdr.alignment = Alignment(horizontal="center")

        # 2. Big Value Metric (INDEX/MATCH)
        val_row = start_row + 1
        ws.merge_cells(f"{c1}{val_row}:{c4}{val_row+1}")
        val = ws[f"{c1}{val_row}"]
        
        match_month = "MATCH($D$3, Staging!$B$1:$E$1, 0)"
        match_kpi = f'MATCH("{kpi_id}", Staging!$A$2:$A$10, 0)'
        
        val.value = f'=INDEX(Staging!$B$2:$E$10, {match_kpi}, {match_month})'
        val.font = Font(size=24, bold=True)
        val.alignment = Alignment(horizontal="center", vertical="center")
        val.number_format = num_format

        # 3. Footer comparisons
        foot_row = start_row + 3
        
        ws[f"{c1}{foot_row}"] = "Vs. Target"
        ws[f"{c1}{foot_row}"].font = Font(bold=True, size=9)
        ws[f"{c1}{foot_row}"].alignment = Alignment(horizontal="right")
        
        match_target = f'MATCH("{kpi_id} Target", Staging!$A$2:$A$10, 0)'
        ws[f"{c2}{foot_row}"] = f'=INDEX(Staging!$B$2:$E$10, {match_target}, {match_month})'
        ws[f"{c2}{foot_row}"].number_format = num_format
        ws[f"{c2}{foot_row}"].alignment = Alignment(horizontal="left")

        ws[f"{c3}{foot_row}"] = "Vs. Prior"
        ws[f"{c3}{foot_row}"].font = Font(bold=True, size=9)
        ws[f"{c3}{foot_row}"].alignment = Alignment(horizontal="right")
        
        # Index matches col-1 safely to grab the prior timeframe
        index_prior = f'INDEX(Staging!$B$2:$E$10, {match_kpi}, {match_month} - 1)'
        ws[f"{c4}{foot_row}"] = f'=IF({match_month}=1, "N/A", {index_prior})'
        ws[f"{c4}{foot_row}"].number_format = num_format
        ws[f"{c4}{foot_row}"].alignment = Alignment(horizontal="left")

        # 4. Conditional Formatting (Dynamic highlighting)
        target_ref = f"${c2}${foot_row}"
        big_val_cell = f"${c1}${val_row}"
        
        good_fill = PatternFill(start_color=palette["good"], end_color=palette["good"], fill_type="solid")
        good_font = Font(color=palette["good_text"])
        bad_fill = PatternFill(start_color=palette["bad"], end_color=palette["bad"], fill_type="solid")
        bad_font = Font(color=palette["bad_text"])

        # Determine threshold rules based on KPI type
        if is_lower_better:
            rule_good = FormulaRule(formula=[f'={big_val_cell}<={target_ref}'], fill=good_fill, font=good_font, stopIfTrue=True)
            rule_bad = FormulaRule(formula=[f'={big_val_cell}>{target_ref}'], fill=bad_fill, font=bad_font, stopIfTrue=True)
        else:
            rule_good = FormulaRule(formula=[f'={big_val_cell}>={target_ref}'], fill=good_fill, font=good_font, stopIfTrue=True)
            rule_bad = FormulaRule(formula=[f'={big_val_cell}<{target_ref}'], fill=bad_fill, font=bad_font, stopIfTrue=True)

        ws.conditional_formatting.add(f"{c1}{val_row}:{c4}{val_row+1}", rule_good)
        ws.conditional_formatting.add(f"{c1}{val_row}:{c4}{val_row+1}", rule_bad)

        # 5. Framing
        thin = Side(style='thin', color="A0A0A0")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)
        for r in range(start_row, foot_row + 1):
            for c in range(start_col, start_col + 4):
                ws.cell(row=r, column=c).border = border

    # Draw specific cards using the generator logic
    draw_kpi_card(ws_dash, 6, 2, "DSO", "DSO (Days Sales Outstanding)", "0", is_lower_better=True)
    draw_kpi_card(ws_dash, 6, 7, "DPO", "DPO (Days Payable Outstanding)", "0", is_lower_better=False)
    draw_kpi_card(ws_dash, 12, 2, "Gross Margin", "Gross Margin %", "0%", is_lower_better=False)
    draw_kpi_card(ws_dash, 12, 7, "OPEX", "Operating Expenses", "$#,##0", is_lower_better=True)

    # Bring dashboard to front
    wb.active = wb.index(ws_dash)
```