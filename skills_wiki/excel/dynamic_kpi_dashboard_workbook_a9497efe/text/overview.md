```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic KPI Dashboard Workbook

* **Tier**: archetype
* **Core Mechanism**: A three-sheet architecture separating raw inputs ("Data"), derived metrics/targets ("Staging"), and presentation ("Dashboard"). The dashboard uses `INDEX/MATCH` bound to a data validation dropdown to dynamically fetch metrics for a selected month, applying large typography and dynamic conditional formatting based on target thresholds.
* **Applicability**: Best used for recurring monthly/quarterly financial or operational reporting. This pattern cleanly abstracts calculation logic away from the end-user, providing a clean, interactive executive summary.

### 2. Structural Breakdown

- **Data Layout**: A 3-sheet structure:
  1. `1) Data`: Raw matrix of accounts/metrics (rows) by period (columns).
  2. `2) Staging`: Calculation layer computing final KPIs and mapping targets per period.
  3. `3) Dashboard`: Presentation layer with hidden gridlines and KPI "cards".
- **Formula Logic**: 
  - `INDEX/MATCH` looks up the selected month: `=INDEX('2) Staging'!$B$2:$D$2, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))`
  - IFERROR wrappers on the staging layer handle zero-division for early months.
- **Visual Design**: 
  - Clean card design with merged title headers.
  - Oversized font (size 24) for primary metrics to ensure readability.
  - `CellIsRule` Conditional Formatting dynamically applies green/red fills and fonts depending on whether the metric beats or misses the target.
- **Charts/Tables**: Not chart-based; relies entirely on localized KPI card clusters with inline conditional styling.
- **Theme Hooks**: Uses neutral borders and background fills for structure, but relies heavily on semantic green (`C6EFCE`) and red (`FFC7CE`) for performance indication.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Monthly KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.utils import get_column_letter

    # 1. Setup Tabs
    ws_data = wb.active
    ws_data.title = "1) Data"
    ws_staging = wb.create_sheet("2) Staging")
    ws_dashboard = wb.create_sheet("3) Dashboard")
    
    # 2. Populate Data Tab
    data = [
        ["Category", "Jan-20", "Feb-20", "Mar-20"],
        ["Accounts Receivable", 2800000, 2940000, 3087000],
        ["Credit Sales", 1500000, 1590000, 1685400],
        ["Days in Month", 31, 29, 31],
        ["Sales", 1500000, 1590000, 1685400],
        ["COGS", 900000, 954000, 1030320]
    ]
    for row in data:
        ws_data.append(row)
        
    for col in range(2, 5):
        col_letter = get_column_letter(col)
        for row in range(2, 7):
            if row != 4: # 'Days in Month' is not currency
                ws_data[f"{col_letter}{row}"].number_format = '"$"#,##0'
                
    for cell in ws_data[1]:
        cell.font = Font(bold=True)
    ws_data.column_dimensions["A"].width = 25

    # 3. Populate Staging Tab
    staging_data = [
        ["KPI", "Jan-20", "Feb-20", "Mar-20"],
        ["DSO Actual", "=IFERROR(('1) Data'!B2/'1) Data'!B3)*'1) Data'!B4, 0)", "=IFERROR(('1) Data'!C2/'1) Data'!C3)*'1) Data'!C4, 0)", "=IFERROR(('1) Data'!D2/'1) Data'!D3)*'1) Data'!D4, 0)"],
        ["DSO Target", 45, 45, 45],
        ["GM Actual", "=IFERROR(('1) Data'!B5-'1) Data'!B6)/'1) Data'!B5, 0)", "=IFERROR(('1) Data'!C5-'1) Data'!C6)/'1) Data'!C5, 0)", "=IFERROR(('1) Data'!D5-'1) Data'!D6)/'1) Data'!D5, 0)"],
        ["GM Target", 0.35, 0.38, 0.40]
    ]
    for row in staging_data:
        ws_staging.append(row)
        
    for col in range(2, 5):
        col_letter = get_column_letter(col)
        ws_staging[f"{col_letter}2"].number_format = '0'
        ws_staging[f"{col_letter}3"].number_format = '0'
        ws_staging[f"{col_letter}4"].number_format = '0%'
        ws_staging[f"{col_letter}5"].number_format = '0%'

    for cell in ws_staging[1]:
        cell.font = Font(bold=True)
    ws_staging.column_dimensions["A"].width = 20

    # 4. Populate Dashboard Tab
    ws_dashboard.sheet_view.showGridLines = False
    
    # Dashboard Header
    ws_dashboard["B2"] = title
    ws_dashboard["B2"].font = Font(size=20, bold=True, color="333333")
    
    # Dynamic Dropdown for Month Selection
    ws_dashboard["B4"] = "For the month of:"
    ws_dashboard["B4"].font = Font(bold=True)
    ws_dashboard["B4"].alignment = Alignment(horizontal="right")
    
    ws_dashboard["C4"] = "Jan-20"
    ws_dashboard["C4"].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    ws_dashboard["C4"].alignment = Alignment(horizontal="center")
    ws_dashboard["C4"].border = Border(bottom=Side(style="medium", color="B2B2B2"))
    
    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20"', allow_blank=False)
    ws_dashboard.add_data_validation(dv)
    dv.add(ws_dashboard["C4"])

    # Base Styling Tokens
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    header_font = Font(bold=True, color="333333")
    center_align = Alignment(horizontal="center", vertical="center")
    val_font = Font(size=24, bold=True)
    thin_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC")
    )
    
    # KPI 1: DSO (Days Sales Outstanding)
    ws_dashboard["B6"] = "DSO (Days Sales Outstanding)"
    ws_dashboard.merge_cells("B6:C6")
    ws_dashboard["B6"].fill = header_fill
    ws_dashboard["B6"].font = header_font
    ws_dashboard["B6"].alignment = center_align
    ws_dashboard["B6"].border = thin_border
    ws_dashboard["C6"].border = thin_border
    
    ws_dashboard["B7"] = "=INDEX('2) Staging'!$B$2:$D$2, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))"
    ws_dashboard.merge_cells("B7:C7")
    ws_dashboard["B7"].font = val_font
    ws_dashboard["B7"].alignment = center_align
    ws_dashboard["B7"].number_format = '0'
    ws_dashboard["B7"].border = thin_border
    ws_dashboard["C7"].border = thin_border
    
    ws_dashboard["B8"] = "Vs. Target"
    ws_dashboard["C8"] = "=INDEX('2) Staging'!$B$3:$D$3, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))"
    ws_dashboard["B8"].font = Font(size=10, italic=True)
    ws_dashboard["C8"].font = Font(size=10, bold=True)
    ws_dashboard["C8"].alignment = Alignment(horizontal="right")
    ws_dashboard["B8"].border = thin_border
    ws_dashboard["C8"].border = thin_border
    
    # KPI 2: Gross Margin
    ws_dashboard["E6"] = "Gross Margin"
    ws_dashboard.merge_cells("E6:F6")
    ws_dashboard["E6"].fill = header_fill
    ws_dashboard["E6"].font = header_font
    ws_dashboard["E6"].alignment = center_align
    ws_dashboard["E6"].border = thin_border
    ws_dashboard["F6"].border = thin_border
    
    ws_dashboard["E7"] = "=INDEX('2) Staging'!$B$4:$D$4, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))"
    ws_dashboard.merge_cells("E7:F7")
    ws_dashboard["E7"].font = val_font
    ws_dashboard["E7"].alignment = center_align
    ws_dashboard["E7"].number_format = '0%'
    ws_dashboard["E7"].border = thin_border
    ws_dashboard["F7"].border = thin_border
    
    ws_dashboard["E8"] = "Vs. Target"
    ws_dashboard["F8"] = "=INDEX('2) Staging'!$B$5:$D$5, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))"
    ws_dashboard["F8"].number_format = '0%'
    ws_dashboard["E8"].font = Font(size=10, italic=True)
    ws_dashboard["F8"].font = Font(size=10, bold=True)
    ws_dashboard["F8"].alignment = Alignment(horizontal="right")
    ws_dashboard["E8"].border = thin_border
    ws_dashboard["F8"].border = thin_border

    # Conditional Formatting Rules
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    green_font = Font(color="006100", size=24, bold=True)
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    red_font = Font(color="9C0006", size=24, bold=True)
    
    # Rule for DSO: Lower is better
    ws_dashboard.conditional_formatting.add(
        'B7:C7', CellIsRule(operator='lessThan', formula=['$C$8'], stopIfTrue=True, fill=green_fill, font=green_font)
    )
    ws_dashboard.conditional_formatting.add(
        'B7:C7', CellIsRule(operator='greaterThanOrEqual', formula=['$C$8'], stopIfTrue=True, fill=red_fill, font=red_font)
    )
    
    # Rule for GM: Higher is better
    ws_dashboard.conditional_formatting.add(
        'E7:F7', CellIsRule(operator='greaterThanOrEqual', formula=['$F$8'], stopIfTrue=True, fill=green_fill, font=green_font)
    )
    ws_dashboard.conditional_formatting.add(
        'E7:F7', CellIsRule(operator='lessThan', formula=['$F$8'], stopIfTrue=True, fill=red_fill, font=red_font)
    )
    
    # Column Sizing
    ws_dashboard.column_dimensions["A"].width = 3
    ws_dashboard.column_dimensions["B"].width = 16
    ws_dashboard.column_dimensions["C"].width = 16
    ws_dashboard.column_dimensions["D"].width = 5
    ws_dashboard.column_dimensions["E"].width = 16
    ws_dashboard.column_dimensions["F"].width = 16
```
```