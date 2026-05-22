### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard Workbook

* **Tier**: archetype
* **Core Mechanism**: Uses a 'Staging' sheet to store monthly KPI actuals and targets. Generates a 'Dashboard' sheet featuring a data-validated month drop-down. Stylized KPI cards use dynamic `INDEX/MATCH` formulas to pull the selected month's value, compare it against the target, and apply traffic-light conditional formatting (green/red) based on performance.
* **Applicability**: Excellent for recurring executive reporting where multiple high-level metrics (e.g., Working Capital, Profitability) must be monitored against targets and prior periods on a single, clean screen.

### 2. Structural Breakdown

- **Data Layout**: Two sheets. `Staging` acts as the data warehouse (KPIs as rows, Months as columns). `Dashboard` acts as the presentation layer.
- **Formula Logic**: `INDEX(Staging!$B$2:$E$7, MATCH(KPI, Staging!$A$2:$A$7, 0), MATCH($D$5, Staging!$B$1:$E$1, 0))` fetches data dynamically based on the dropdown. A `-1` offset on the column match fetches the prior month.
- **Visual Design**: Large, bold fonts for main KPI numbers. Gray sectional header bands. Clean borders encapsulating each KPI card.
- **Charts/Tables**: Layout is purely grid-based using merged cells to create physical "cards". 
- **Theme Hooks**: Utilizes hex codes for success (green) and failure (red) directly, while falling back to standard palette colors (like `4F81BD` for headers) representing the `corporate_blue` theme.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme & Color Definitions
    # In a full framework, these would map to a theme provider.
    card_header_bg = "4F81BD"  # Default corporate blue
    card_header_fg = "FFFFFF"
    green_fill = "C6EFCE"
    green_font = "006100"
    red_fill = "FFC7CE"
    red_font = "9C0006"
    gray_bg = "F2F2F2"
    border_color = "D9D9D9"

    # 2. Setup Staging Sheet
    ws_staging = wb.active
    ws_staging.title = "Staging"
    
    headers = ["KPI", "Jan-20", "Feb-20", "Mar-20", "Apr-20"]
    ws_staging.append(headers)
    
    # Mock Data: Actual and Target rows
    kpi_data = [
        ["DSO Actual", 58, 54, 57, 54],
        ["DSO Target", 45, 45, 45, 45],
        ["DPO Actual", 107, 99, 90, 103],
        ["DPO Target", 90, 90, 90, 90],
        ["Gross Margin Actual", 0.38, 0.40, 0.35, 0.42],
        ["Gross Margin Target", 0.40, 0.40, 0.40, 0.40],
    ]
    for row in kpi_data:
        ws_staging.append(row)
        
    for cell in ws_staging[1]:
        cell.font = Font(bold=True)
        
    # 3. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Title
    ws_dash.merge_cells("B2:I3")
    title_cell = ws_dash["B2"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Month Selector Dropdown
    ws_dash["B5"] = "For the month of:"
    ws_dash["B5"].font = Font(bold=True)
    ws_dash["B5"].alignment = Alignment(horizontal="right")
    
    drop_cell = ws_dash["C5"]
    drop_cell.value = "Mar-20"  # Default selected month
    drop_cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    drop_cell.border = Border(bottom=Side(style="thin", color="000000"))
    drop_cell.alignment = Alignment(horizontal="center")
    
    # Add Data Validation for the dropdown
    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20,Apr-20"', allowBlank=True)
    ws_dash.add_data_validation(dv)
    dv.add(drop_cell)
    
    # Helper to render an individual KPI Card
    def render_card(start_row, start_col, kpi_name, title_label, format_type="0", higher_is_better=False):
        thin_border = Side(style="thin", color=border_color)
        card_border = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)
        
        # Header Row
        ws_dash.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col+3)
        hdr = ws_dash.cell(row=start_row, column=start_col)
        hdr.value = title_label
        hdr.fill = PatternFill(start_color=card_header_bg, end_color=card_header_bg, fill_type="solid")
        hdr.font = Font(color=card_header_fg, bold=True)
        hdr.alignment = Alignment(horizontal="center")
        
        # Main Value Row
        val_row = start_row + 1
        ws_dash.merge_cells(start_row=val_row, start_column=start_col, end_row=val_row, end_column=start_col+3)
        val = ws_dash.cell(row=val_row, column=start_col)
        
        # INDEX/MATCH fetching Actuals for the chosen month
        val.value = f'=INDEX(Staging!$B$2:$E$7, MATCH("{kpi_name} Actual", Staging!$A$2:$A$7, 0), MATCH($C$5, Staging!$B$1:$E$1, 0))'
        val.font = Font(size=22, bold=True)
        val.alignment = Alignment(horizontal="center")
        val.number_format = format_type
        
        # Sub-metrics Row
        sub_row = start_row + 2
        ws_dash.cell(row=sub_row, column=start_col, value="Vs. Target").font = Font(size=9, italic=True)
        
        tgt = ws_dash.cell(row=sub_row, column=start_col+1)
        tgt.value = f'=INDEX(Staging!$B$2:$E$7, MATCH("{kpi_name} Target", Staging!$A$2:$A$7, 0), MATCH($C$5, Staging!$B$1:$E$1, 0))'
        tgt.number_format = format_type
        tgt.font = Font(size=10, bold=True)
        tgt.alignment = Alignment(horizontal="left")
        
        ws_dash.cell(row=sub_row, column=start_col+2, value="Prior Mth").font = Font(size=9, italic=True)
        
        prv = ws_dash.cell(row=sub_row, column=start_col+3)
        # Safely grab prior month data by offsetting the MATCH column by -1. Handle Jan (index 1) with an IF.
        prv.value = f'=IF(MATCH($C$5, Staging!$B$1:$E$1, 0)=1, "-", INDEX(Staging!$B$2:$E$7, MATCH("{kpi_name} Actual", Staging!$A$2:$A$7, 0), MATCH($C$5, Staging!$B$1:$E$1, 0)-1))'
        prv.number_format = format_type
        prv.font = Font(size=10, bold=True)
        prv.alignment = Alignment(horizontal="left")
        
        # Apply borders to the card block
        for r in range(start_row, start_row+3):
            for c in range(start_col, start_col+4):
                ws_dash.cell(row=r, column=c).border = card_border
                
        # Conditional Formatting for Main Value
        tgt_ref = f"${tgt.column_letter}${tgt.row}"
        good_fill = PatternFill(start_color=green_fill, end_color=green_fill, fill_type="solid")
        bad_fill = PatternFill(start_color=red_fill, end_color=red_fill, fill_type="solid")
        good_font = Font(color=green_font, size=22, bold=True)
        bad_font = Font(color=red_font, size=22, bold=True)

        if higher_is_better:
            ws_dash.conditional_formatting.add(val.coordinate, CellIsRule(operator='greaterThanOrEqual', formula=[tgt_ref], fill=good_fill, font=good_font))
            ws_dash.conditional_formatting.add(val.coordinate, CellIsRule(operator='lessThan', formula=[tgt_ref], fill=bad_fill, font=bad_font))
        else:
            ws_dash.conditional_formatting.add(val.coordinate, CellIsRule(operator='lessThanOrEqual', formula=[tgt_ref], fill=good_fill, font=good_font))
            ws_dash.conditional_formatting.add(val.coordinate, CellIsRule(operator='greaterThan', formula=[tgt_ref], fill=bad_fill, font=bad_font))

    # Helper to render Section Headers
    def render_section_header(row, title_text):
        ws_dash.merge_cells(start_row=row, start_column=2, end_row=row, end_column=9)
        sec = ws_dash.cell(row=row, column=2)
        sec.value = title_text
        sec.fill = PatternFill(start_color=gray_bg, end_color=gray_bg, fill_type="solid")
        sec.font = Font(bold=True, size=14)
        sec.alignment = Alignment(horizontal="center")

    # 4. Construct Dashboard Layout
    render_section_header(7, "Working Capital Efficiency")
    render_card(9, 2, "DSO", "DSO (Days Sales Outstanding)", "0", higher_is_better=False)
    render_card(9, 6, "DPO", "DPO (Days Payables Outstanding)", "0", higher_is_better=False)
    
    render_section_header(13, "Profitability KPIs")
    render_card(15, 2, "Gross Margin", "Gross Margin %", "0%", higher_is_better=True)
    
    # Layout Spacing
    for col in ["B", "C", "D", "E", "F", "G", "H", "I"]:
        ws_dash.column_dimensions[col].width = 12
    ws_dash.column_dimensions["A"].width = 3 # Margin
```