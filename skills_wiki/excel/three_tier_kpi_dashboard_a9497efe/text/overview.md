### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Tier KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Implements a standard financial reporting architecture using three distinct layers: Raw Data, Staging (Calculations), and Dashboard (Presentation). The dashboard utilizes a central Data Validation drop-down to drive dynamic `INDEX/MATCH` lookups against the staging sheet, presenting the selected period's metrics with oversized typography and target-aware conditional formatting.
* **Applicability**: Ideal for financial controllers, executive summaries, or performance reporting where period-over-period or actual-vs-budget metrics must be communicated quickly without overwhelming the audience with raw data tables.

### 2. Structural Breakdown

- **Data Layout**: Three distinct worksheets: `1) Data` (flat time-series data), `2) Staging` (calculated ratios/metrics per period), and `3) Dashboard` (styled presentation layer).
- **Formula Logic**: `=INDEX('2) Staging'!$B$2:$G$2, MATCH($C$4, '2) Staging'!$B$1:$G$1, 0))` to dynamically fetch the metric corresponding to the selected month.
- **Visual Design**: Gridlines removed. Minimalist layout using large fonts (Size 24+) for primary numbers. Heavy use of Conditional Formatting (Green/Red) directly on the primary value to instantly communicate status against targets.
- **Charts/Tables**: Standalone "KPI Cards" constructed from merged cells. Top row is a grey header, middle is the large dynamic value, bottom contains static/comparative targets.
- **Theme Hooks**: Primary headers use `theme.primary_bg` with white text. Neutral grey `theme.bg_alt` for KPI block titles. Standard Excel positive/negative fills (Green/Red) for conditional formatting.

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

def render_workbook(wb: Workbook, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # Colors (Simulating theme pallet)
    header_bg = "4F81BD"
    neutral_bg = "F2F2F2"
    good_fill = "C6EFCE"
    good_font = "006100"
    bad_fill = "FFC7CE"
    bad_font = "9C0006"

    # 1. Initialize 3-Tier Architecture
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    ws_data = wb.create_sheet("1) Data")
    ws_staging = wb.create_sheet("2) Staging")
    ws_dash = wb.create_sheet("3) Dashboard")

    months = ["Jan-20", "Feb-20", "Mar-20", "Apr-20", "May-20", "Jun-20"]

    # --- RAW DATA SHEET ---
    ws_data.append(["Category"] + months)
    raw_data = [
        ["Sales", 1500000, 1650000, 1800000, 1750000, 1900000, 2100000],
        ["COGS", 900000, 950000, 1000000, 980000, 1050000, 1150000],
        ["Accounts Receivable", 450000, 480000, 520000, 500000, 550000, 600000]
    ]
    for row in raw_data:
        ws_data.append(row)

    # --- STAGING SHEET ---
    ws_staging.append(["KPI"] + months)
    # Staging holds the final calculation values to keep Dashboard logic clean
    staging_data = [
        ["Gross Margin", 0.40, 0.42, 0.44, 0.44, 0.45, 0.45],
        ["DSO (Days Sales Outstanding)", 30, 29, 31, 30, 28, 27],
        ["Sales Growth", 0.05, 0.10, 0.09, -0.02, 0.08, 0.10]
    ]
    for row in staging_data:
        ws_staging.append(row)

    # --- DASHBOARD SHEET ---
    ws_dash.sheet_view.showGridLines = False

    # Main Header
    ws_dash["B2"] = title
    ws_dash["B2"].font = Font(size=20, bold=True, color="FFFFFF")
    ws_dash["B2"].fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")
    ws_dash.merge_cells("B2:J2")
    ws_dash["B2"].alignment = Alignment(horizontal="center", vertical="center")

    # Dynamic Month Selector
    ws_dash["B4"] = "For the month of:"
    ws_dash["B4"].font = Font(bold=True)
    ws_dash["B4"].alignment = Alignment(horizontal="right")
    
    ws_dash["C4"] = "Jan-20"  # Default
    ws_dash["C4"].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    ws_dash["C4"].border = Border(bottom=Side(style="medium", color="000000"))
    ws_dash["C4"].alignment = Alignment(horizontal="center")

    # Data Validation Drop-down
    dv = DataValidation(type="list", formula1=f'"{",".join(months)}"', allow_blank=True)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash["C4"])

    # KPI Layout Definitions
    kpis = [
        {"title": "Gross Margin", "staging_row": 2, "target": 0.42, "format": "0%", "good_higher": True, "col": 2},
        {"title": "DSO (Days)", "staging_row": 3, "target": 30, "format": "0", "good_higher": False, "col": 5},
        {"title": "Sales Growth", "staging_row": 4, "target": 0.05, "format": "0%", "good_higher": True, "col": 8}
    ]

    row_offset = 6
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # Generate KPI Cards
    for kpi in kpis:
        c = kpi["col"]
        
        # 1. KPI Title (Grey Header)
        title_cell = ws_dash.cell(row=row_offset, column=c)
        title_cell.value = kpi["title"]
        title_cell.fill = PatternFill(start_color=neutral_bg, end_color=neutral_bg, fill_type="solid")
        title_cell.font = Font(bold=True)
        title_cell.alignment = Alignment(horizontal="center")
        ws_dash.merge_cells(start_row=row_offset, start_column=c, end_row=row_offset, end_column=c+1)

        # 2. Dynamic Value (INDEX/MATCH)
        val_cell = ws_dash.cell(row=row_offset+1, column=c)
        staging_range = f"'2) Staging'!$B${kpi['staging_row']}:$G${kpi['staging_row']}"
        match_range = f"'2) Staging'!$B$1:$G$1"
        
        val_cell.value = f'=INDEX({staging_range}, MATCH($C$4, {match_range}, 0))'
        val_cell.font = Font(size=24, bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        val_cell.number_format = kpi["format"]
        ws_dash.merge_cells(start_row=row_offset+1, start_column=c, end_row=row_offset+2, end_column=c+1)

        # 3. Static Target Context
        ws_dash.cell(row=row_offset+3, column=c).value = "Vs. Target"
        ws_dash.cell(row=row_offset+3, column=c).font = Font(size=10, italic=True)
        ws_dash.cell(row=row_offset+3, column=c).alignment = Alignment(horizontal="right")

        tgt_val_cell = ws_dash.cell(row=row_offset+3, column=c+1)
        tgt_val_cell.value = kpi["target"]
        tgt_val_cell.number_format = kpi["format"]
        tgt_val_cell.font = Font(size=10, bold=True)
        tgt_val_cell.alignment = Alignment(horizontal="center")

        # Layout styling
        for r in range(row_offset, row_offset+4):
            for col in range(c, c+2):
                ws_dash.cell(row=r, column=col).border = thin_border

        # 4. Conditional Formatting Injection
        green_fill = PatternFill(start_color=good_fill, end_color=good_fill, fill_type="solid")
        green_font = Font(color=good_font, bold=True, size=24)
        red_fill = PatternFill(start_color=bad_fill, end_color=bad_fill, fill_type="solid")
        red_font = Font(color=bad_font, bold=True, size=24)

        if kpi["good_higher"]:
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='greaterThanOrEqual', formula=[str(kpi["target"])], fill=green_fill, font=green_font))
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='lessThan', formula=[str(kpi["target"])], fill=red_fill, font=red_font))
        else:
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='lessThanOrEqual', formula=[str(kpi["target"])], fill=green_fill, font=green_font))
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='greaterThan', formula=[str(kpi["target"])], fill=red_fill, font=red_font))

    # Grid alignment and spacing adjustments
    ws_dash.column_dimensions['A'].width = 2
    for col_letter in ['B', 'C', 'E', 'F', 'H', 'I']:
        ws_dash.column_dimensions[col_letter].width = 15
    for col_letter in ['D', 'G']:
        ws_dash.column_dimensions[col_letter].width = 4
```