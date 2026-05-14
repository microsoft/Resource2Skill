### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Tier KPI Dashboard Architecture

* **Tier**: archetype
* **Core Mechanism**: Implements a robust separation of concerns using three worksheets: `1) Data` (raw inputs), `2) Staging` (metrics calculations and time-series alignment), and `3) Dashboard` (presentation layer). The presentation layer uses a data-validated dropdown to select the reporting period, which drives `INDEX/MATCH` formulas to dynamically update large-font KPI blocks with conditional formatting indicating performance against targets.
* **Applicability**: Essential for management and executive dashboards where data updates frequently. By separating raw data from the presentation UI, users can paste new monthly data into the backend sheets without breaking the highly-formatted dashboard views. 

### 2. Structural Breakdown

- **Data Layout**: 
  - `1) Data`: Flat raw data export.
  - `2) Staging`: Standardized columns for periods (Jan-20, Feb-20, etc.) and rows for metrics (Actual, Target, Prior).
  - `3) Dashboard`: Clean grid without gridlines. Uses multi-cell merged regions for KPI components (Title, Value, Variances).
- **Formula Logic**: 
  - Period Selector uses Data Validation list.
  - Dashboard values use `=INDEX('2) Staging'!$B$2:$D$2, 1, MATCH($C$3, '2) Staging'!$B$1:$D$1, 0))` to pull values dynamically based on the dropdown.
- **Visual Design**: Uses exceptionally large fonts (24pt+) for primary metrics to ensure at-a-glance readability. Section headers use bold background fills to segment the page.
- **Charts/Tables**: Replaces traditional charts with stylized grid "blocks" representing a single KPI's current state, target, and prior period.
- **Theme Hooks**: Utilizes `header_bg`, `header_fg`, `accent_bg` for structural blocks, and relies on semantic success/danger fills (`#C6EFCE` / `#FFC7CE`) for conditional formatting based on target thresholds.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup Three-Tier Architecture
    ws_data = wb.active
    ws_data.title = "1) Data"
    ws_staging = wb.create_sheet("2) Staging")
    ws_dash = wb.create_sheet("3) Dashboard")
    
    # Theme/Styling Setup
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    section_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    kpi_title_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    
    center_align = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style="thin", color="A6A6A6"),
        right=Side(style="thin", color="A6A6A6"),
        top=Side(style="thin", color="A6A6A6"),
        bottom=Side(style="thin", color="A6A6A6")
    )

    # 2. Populate Backend (Staging)
    # In a real app, 'Data' flows into 'Staging'. Here we populate 'Staging' directly for the UI to consume.
    staging_data = [
        ["Category", "Jan-20", "Feb-20", "Mar-20"],
        ["DSO_Actual", 58, 54, 41],
        ["DSO_Target", 45, 45, 45],
        ["DSO_Prior", 48, 58, 54],
        ["Margin_Actual", 0.38, 0.40, 0.42],
        ["Margin_Target", 0.40, 0.40, 0.40],
        ["Margin_Prior", 0.35, 0.38, 0.40]
    ]
    for row in staging_data:
        ws_staging.append(row)
        
    # 3. Build Dashboard UI
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Header
    ws_dash.merge_cells("A1:H2")
    title_cell = ws_dash["A1"]
    title_cell.value = title or "KPI Dashboard"
    title_cell.font = Font(size=20, bold=True, color="FFFFFF")
    title_cell.fill = header_fill
    title_cell.alignment = center_align
    
    # Time Period Selector
    ws_dash["B4"] = "For the month of:"
    ws_dash["B4"].font = Font(bold=True)
    ws_dash["B4"].alignment = Alignment(horizontal="right")
    
    ws_dash["C4"] = "Feb-20"  # Default
    ws_dash["C4"].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    ws_dash["C4"].border = thin_border
    
    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20"', allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash["C4"])

    # Section 1 Header
    ws_dash.merge_cells("A6:H6")
    ws_dash["A6"] = "Working Capital & Sales Efficiency"
    ws_dash["A6"].font = Font(size=14, bold=True)
    ws_dash["A6"].fill = section_fill
    ws_dash["A6"].alignment = center_align
    
    # Helper to generate stylized KPI blocks
    def render_kpi_block(ws, start_row, start_col, kpi_name, staging_rows, is_lower_better=True, is_pct=False):
        # Determine column letters for width adjustments
        c1 = ws.cell(row=start_row, column=start_col).column_letter
        c4 = ws.cell(row=start_row, column=start_col+3).column_letter
        
        # 1. Title Row
        ws.merge_cells(f"{c1}{start_row}:{c4}{start_row}")
        title_c = ws.cell(row=start_row, column=start_col)
        title_c.value = kpi_name
        title_c.fill = kpi_title_fill
        title_c.font = Font(bold=True)
        title_c.alignment = center_align
        title_c.border = thin_border
        
        # 2. Main Value Area (Huge Font)
        val_row = start_row + 1
        ws.merge_cells(f"{c1}{val_row}:{c4}{val_row+1}")
        val_c = ws.cell(row=val_row, column=start_col)
        
        # Dynamic INDEX/MATCH formula linked to C4 dropdown
        actual_row_num, target_row_num, prior_row_num = staging_rows
        val_c.value = f"=INDEX('2) Staging'!$B${actual_row_num}:$D${actual_row_num}, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))"
        val_c.font = Font(size=28, bold=True)
        val_c.alignment = center_align
        val_c.border = thin_border
        if is_pct:
            val_c.number_format = "0%"
            
        # 3. Footer Variances
        footer_row = start_row + 3
        ws.cell(row=footer_row, column=start_col, value="Vs. Target").font = Font(size=9, italic=True)
        
        tgt_c = ws.cell(row=footer_row, column=start_col+1)
        tgt_c.value = f"=INDEX('2) Staging'!$B${target_row_num}:$D${target_row_num}, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))"
        tgt_c.font = Font(size=10, bold=True)
        tgt_c.border = thin_border
        
        ws.cell(row=footer_row, column=start_col+2, value="Vs. Prior Month").font = Font(size=9, italic=True)
        
        prior_c = ws.cell(row=footer_row, column=start_col+3)
        prior_c.value = f"=INDEX('2) Staging'!$B${prior_row_num}:$D${prior_row_num}, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))"
        prior_c.font = Font(size=10, bold=True)
        prior_c.border = thin_border
        
        if is_pct:
            tgt_c.number_format = "0%"
            prior_c.number_format = "0%"
            
        # 4. Conditional Formatting on Main Value
        tgt_addr = tgt_c.coordinate
        val_addr = val_c.coordinate
        
        # If lower is better (like DSO): Value < Target = Green
        op_good = 'lessThan' if is_lower_better else 'greaterThan'
        op_bad = 'greaterThan' if is_lower_better else 'lessThan'
        
        ws.conditional_formatting.add(val_addr, CellIsRule(operator=op_good, formula=[tgt_addr], fill=green_fill))
        ws.conditional_formatting.add(val_addr, CellIsRule(operator=op_bad, formula=[tgt_addr], fill=red_fill))

    # Render KPI Blocks (Staging row indexes map to: Actual, Target, Prior)
    render_kpi_block(ws_dash, start_row=8, start_col=1, kpi_name="DSO (Days Sales Outstanding)", staging_rows=(2,3,4), is_lower_better=True)
    render_kpi_block(ws_dash, start_row=8, start_col=5, kpi_name="Gross Margin %", staging_rows=(5,6,7), is_lower_better=False, is_pct=True)

    # Adjust Column Widths for aesthetic spacing
    for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        ws_dash.column_dimensions[col].width = 15
```