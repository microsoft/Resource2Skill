```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: 3-Tier KPI Dashboard Architecture

* **Tier**: archetype
* **Core Mechanism**: Separates the workbook into three interconnected sheets: Raw Data (inputs), Staging (calculation formulas like Gross Margin or DSO), and Dashboard (presentation). Uses a dynamic Data Validation dropdown alongside `INDEX/MATCH` to filter metrics for the selected month, applying `CellIsRule` conditional formatting to highlight performance against targets.
* **Applicability**: Highly applicable to monthly periodic reporting packages or executive summaries. Use this architecture when you have expanding time-series raw data but need a pristine, single-page interactive view of the most important metrics that doesn't break as new months are added.

### 2. Structural Breakdown

- **Data Layout**: 
  - `1) Data`: Raw input metrics (Sales, COGS, AR) rows by Month columns.
  - `2) Staging`: Calculated metrics (Margins, Ratios, Targets) rows by Month columns.
  - `3) Dashboard`: Grid of visual "Cards", bounded by empty spacer rows/columns.
- **Formula Logic**: `=INDEX('2) Staging'!$B$2:$G$2, MATCH($C$3, '2) Staging'!$B$1:$G$1, 0))` grabs the staging value matching the dropdown's month in `C3`.
- **Visual Design**: Themed dark header background (`header_fill`) with gray card body (`card_fill`). Large KPI font sizes. Red/Green conditional formatting driven by the adjacent dynamic target cell.
- **Charts/Tables**: Pure cell-based card layout utilizing merged ranges (e.g., 3 columns wide x 3 rows high) with uniform borders.
- **Theme Hooks**: Utilizes `header_fill` (Primary Color) and standard traffic light colors (Red/Green) for indicator state.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str="KPI Dashboard", theme: str="corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter
    
    # 1. Setup Sheets
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
    ws_data = wb.create_sheet("1) Data")
    ws_staging = wb.create_sheet("2) Staging")
    ws_dash = wb.create_sheet("3) Dashboard")
    
    # Styling Palette
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)
    card_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    title_font = Font(size=24, bold=True)
    
    good_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    good_font = Font(color="006100", size=24, bold=True)
    bad_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    bad_font = Font(color="9C0006", size=24, bold=True)
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    center_align = Alignment(horizontal="center", vertical="center")
    
    # 2. Populate Raw Data (Inputs)
    months = ["Jan-20", "Feb-20", "Mar-20", "Apr-20", "May-20", "Jun-20"]
    ws_data.append(["Metric"] + months)
    data_rows = [
        ["Sales", 100000, 110000, 105000, 120000, 125000, 130000],
        ["COGS", 60000, 65000, 62000, 70000, 72000, 75000],
        ["AR Balance", 40000, 45000, 42000, 50000, 55000, 60000]
    ]
    for r in data_rows:
        ws_data.append(r)
        
    for col in ws_data.columns:
        ws_data.column_dimensions[col[0].column_letter].width = 12
        
    # 3. Populate Staging (Calculations)
    ws_staging.append(["Category"] + months)
    
    # Gross Margin Formula
    gm_row = ["Gross Margin"]
    for i in range(2, 8):
        c = get_column_letter(i)
        gm_row.append(f"=('1) Data'!{c}2-'1) Data'!{c}3)/'1) Data'!{c}2")
    ws_staging.append(gm_row)
    ws_staging.append(["Target GM"] + [0.35]*6)
    
    # DSO Formula
    dso_row = ["DSO"]
    for i in range(2, 8):
        c = get_column_letter(i)
        dso_row.append(f"=('1) Data'!{c}4/'1) Data'!{c}2)*30")
    ws_staging.append(dso_row)
    ws_staging.append(["Target DSO"] + [12]*6)

    for col in range(2, 8):
        ws_staging.cell(row=2, column=col).number_format = "0%"
        ws_staging.cell(row=3, column=col).number_format = "0%"
        ws_staging.cell(row=4, column=col).number_format = "0.0"
        ws_staging.cell(row=5, column=col).number_format = "0.0"

    for col in ws_staging.columns:
        ws_staging.column_dimensions[col[0].column_letter].width = 14

    # 4. Build Presentation Dashboard
    ws_dash.merge_cells("B1:G1")
    dash_title = ws_dash["B1"]
    dash_title.value = title
    dash_title.font = Font(size=18, bold=True, color="4F81BD")
    dash_title.alignment = center_align
    
    ws_dash["B3"] = "For the month of:"
    ws_dash["B3"].font = Font(bold=True)
    ws_dash["B3"].alignment = Alignment(horizontal="right", vertical="center")
    
    # Setup interactive Data Validation Dropdown
    ws_dash["C3"] = "Jun-20"
    dv = DataValidation(type="list", formula1=f'"{",".join(months)}"', allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash["C3"])
    ws_dash["C3"].fill = card_fill
    ws_dash["C3"].border = thin_border
    ws_dash["C3"].alignment = center_align

    # Reusable component to render a single KPI block
    def render_card(anchor_row, anchor_col, card_title, staging_val_row, staging_tgt_row, num_format, is_higher_better=True):
        # Base formatting across the merged cell block footprint
        for r in range(anchor_row, anchor_row+3):
            for c in range(anchor_col, anchor_col+3):
                cell = ws_dash.cell(row=r, column=c)
                cell.border = thin_border
                if r == anchor_row:
                    cell.fill = header_fill
                else:
                    cell.fill = card_fill

        # Merge blocks
        ws_dash.merge_cells(start_row=anchor_row, start_column=anchor_col, end_row=anchor_row, end_column=anchor_col+2)
        ws_dash.merge_cells(start_row=anchor_row+1, start_column=anchor_col, end_row=anchor_row+1, end_column=anchor_col+2)
        ws_dash.merge_cells(start_row=anchor_row+2, start_column=anchor_col, end_row=anchor_row+2, end_column=anchor_col+1)

        # Title Block
        t_cell = ws_dash.cell(row=anchor_row, column=anchor_col, value=card_title)
        t_cell.font = header_font
        t_cell.alignment = center_align

        # Main KPI Value (Dynamic based on selected dropdown month)
        v_cell = ws_dash.cell(row=anchor_row+1, column=anchor_col)
        v_cell.value = f"=INDEX('2) Staging'!$B${staging_val_row}:$G${staging_val_row}, MATCH($C$3, '2) Staging'!$B$1:$G$1, 0))"
        v_cell.font = title_font
        v_cell.alignment = center_align
        v_cell.number_format = num_format
        
        # Sub-labels for comparison
        lbl_cell = ws_dash.cell(row=anchor_row+2, column=anchor_col, value="Vs. Target:")
        lbl_cell.alignment = Alignment(horizontal="right", vertical="center")
        lbl_cell.font = Font(italic=True, color="595959")
        
        tgt_cell = ws_dash.cell(row=anchor_row+2, column=anchor_col+2)
        tgt_cell.value = f"=INDEX('2) Staging'!$B${staging_tgt_row}:$G${staging_tgt_row}, MATCH($C$3, '2) Staging'!$B$1:$G$1, 0))"
        tgt_cell.number_format = num_format
        tgt_cell.font = Font(bold=True, color="595959")
        tgt_cell.alignment = Alignment(horizontal="left", vertical="center")
        
        # Apply conditional format comparing main value to target value
        tgt_ref = f"${tgt_cell.column_letter}${tgt_cell.row}"
        v_ref = v_cell.coordinate
        
        if is_higher_better:
            rule_good = CellIsRule(operator='greaterThanOrEqual', formula=[tgt_ref], fill=good_fill, font=good_font)
            rule_bad = CellIsRule(operator='lessThan', formula=[tgt_ref], fill=bad_fill, font=bad_font)
        else:
            rule_good = CellIsRule(operator='lessThanOrEqual', formula=[tgt_ref], fill=good_fill, font=good_font)
            rule_bad = CellIsRule(operator='greaterThan', formula=[tgt_ref], fill=bad_fill, font=bad_font)
            
        ws_dash.conditional_formatting.add(v_ref, rule_good)
        ws_dash.conditional_formatting.add(v_ref, rule_bad)

    # Render The Cards
    render_card(5, 2, "Gross Margin", 2, 3, "0%", is_higher_better=True)
    render_card(5, 6, "DSO (Days Sales)", 4, 5, "0", is_higher_better=False)
    
    # Adjust aesthetic layout
    ws_dash.column_dimensions["A"].width = 5
    for c in ["B", "C", "D", "F", "G", "H"]:
        ws_dash.column_dimensions[c].width = 15
    ws_dash.column_dimensions["E"].width = 5  # Blank Spacer Col
    ws_dash.sheet_view.showGridLines = False
```
```