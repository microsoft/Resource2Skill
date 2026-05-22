### 1. High-level Skill Pattern Extraction

> **Skill Name**: Staged KPI Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Implements a multi-sheet architecture where a "Dashboard" presentation layer is decoupled from a "Staging" data layer. It uses a data validation dropdown to select a reporting period, and drives all KPI cards simultaneously using `INDEX/MATCH` relative column lookups (including `MATCH - 1` to dynamically fetch the prior period).
* **Applicability**: Perfect for executive reporting, monthly metric tracking, or any scenario requiring a clean, low-clutter visual layer sitting on top of dense time-series data. 

### 2. Structural Breakdown

- **Data Layout**: Two sheets. `Staging` contains columns for months and rows for metric actuals and targets. `Dashboard` contains a period selector and spaced, 4-column-wide KPI cards.
- **Formula Logic**: 
  - *Current Period*: `=INDEX(Staging_Range, MATCH("KPI_Name", ...), MATCH(Selected_Month, ...))`
  - *Prior Period*: Utilizes relative position by subtracting 1 from the MATCH index: `=INDEX(..., MATCH(...) - 1)`. Includes an `IF` catch to display `"-"` if the selected month is the very first column of data.
- **Visual Design**: Uses color-coded backgrounds on large-font KPI numbers instead of text coloring to maximize salience. Green for favorable vs target, red/pink for unfavorable.
- **Charts/Tables**: Bypasses charts entirely in favor of distinct "KPI Cards" with prominent headers, a hero number, and small-font variance comparables below.
- **Theme Hooks**: Consumes `theme["primary"]` for the dashboard title and dropdown, and `theme["bg"]` for the KPI card headers. Conditional formatting relies on universal semantic red/green.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter

    # Theme setup (Fallback dictionary)
    themes = {
        "corporate_blue": {"primary": "2F5597", "secondary": "D9E1F2", "bg": "F2F2F2", "text": "000000"},
        "midnight_dark": {"primary": "203764", "secondary": "8FAADC", "bg": "E7E6E6", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # 1. Staging Sheet (Time-Series Data & Calcs)
    ws_stage = wb.active
    ws_stage.title = "Staging"
    
    staging_data = [
        ["Category", "Jan-24", "Feb-24", "Mar-24", "Apr-24", "May-24"],
        ["DSO", 45, 52, 41, 38, 44],
        ["DSO Target", 45, 45, 45, 45, 45],
        ["Sales", 15000, 16000, 14500, 17000, 18500],
        ["Sales Target", 15000, 15500, 16000, 16500, 17000],
        ["Gross Margin", 0.25, 0.26, 0.24, 0.28, 0.29],
        ["Gross Margin Target", 0.25, 0.25, 0.25, 0.25, 0.25]
    ]
    for row in staging_data:
        ws_stage.append(row)
        
    for cell in ws_stage[1]:
        cell.font = Font(bold=True)
    
    # 2. Dashboard Sheet (Presentation Layer)
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Header
    ws_dash.merge_cells("B2:O3")
    hdr = ws_dash["B2"]
    hdr.value = title
    hdr.font = Font(size=28, bold=True, color="FFFFFF")
    hdr.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    hdr.alignment = Alignment(horizontal="center", vertical="center")
    
    # Month Selector Dropdown
    ws_dash["B5"] = "For the month of:"
    ws_dash["B5"].font = Font(bold=True)
    ws_dash["B5"].alignment = Alignment(horizontal="right", vertical="center")
    
    month_cell = ws_dash["C5"]
    month_cell.value = "Apr-24"
    month_cell.font = Font(bold=True, color=palette["primary"])
    month_cell.fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
    month_cell.border = Border(bottom=Side(style="medium", color=palette["primary"]))
    month_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    dv = DataValidation(type="list", formula1="Staging!$B$1:$F$1", allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(month_cell)
    
    # Helper to draw an automated KPI Card
    def draw_kpi_card(ws, start_col, start_row, kpi_name, kpi_label, is_lower_better, num_format):
        col_ltr = get_column_letter(start_col)
        end_col_ltr = get_column_letter(start_col + 3)
        
        title_range = f"{col_ltr}{start_row}:{end_col_ltr}{start_row}"
        val_row = start_row + 1
        val_range = f"{col_ltr}{val_row}:{end_col_ltr}{val_row}"
        sub_row = start_row + 2
        
        ws.merge_cells(title_range)
        ws.merge_cells(val_range)
        
        # 1. Card Title
        t_cell = ws[f"{col_ltr}{start_row}"]
        t_cell.value = kpi_label
        t_cell.font = Font(bold=True, color="333333")
        t_cell.fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
        t_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # 2. Main Value (Dynamic Lookup)
        v_cell = ws[f"{col_ltr}{val_row}"]
        v_cell.formula = f'=INDEX(Staging!$A$1:$Z$100, MATCH("{kpi_name}", Staging!$A$1:$A$100, 0), MATCH($C$5, Staging!$A$1:$Z$1, 0))'
        v_cell.font = Font(size=24, bold=True, color="111111")
        v_cell.alignment = Alignment(horizontal="center", vertical="center")
        v_cell.number_format = num_format
        
        # 3. Sub Metrics Row
        ws[f"{col_ltr}{sub_row}"] = "Vs. Target:"
        tgt_col_ltr = get_column_letter(start_col + 1)
        tgt_cell = ws[f"{tgt_col_ltr}{sub_row}"]
        tgt_cell.formula = f'=INDEX(Staging!$A$1:$Z$100, MATCH("{kpi_name} Target", Staging!$A$1:$A$100, 0), MATCH($C$5, Staging!$A$1:$Z$1, 0))'
        tgt_cell.number_format = num_format
        
        pm_lbl_col = get_column_letter(start_col + 2)
        pm_val_col = get_column_letter(start_col + 3)
        ws[f"{pm_lbl_col}{sub_row}"] = "Vs. Prior:"
        
        pm_cell = ws[f"{pm_val_col}{sub_row}"]
        # Prevents hitting the row labels (Col A) if Jan is selected
        pm_formula = (
            f'=IF(MATCH($C$5, Staging!$A$1:$Z$1, 0)<=2, "-", '
            f'INDEX(Staging!$A$1:$Z$100, MATCH("{kpi_name}", Staging!$A$1:$A$100, 0), MATCH($C$5, Staging!$A$1:$Z$1, 0) - 1))'
        )
        pm_cell.formula = pm_formula
        pm_cell.number_format = num_format
        
        # 4. Style Sub Metrics
        for col_offset in range(4):
            c = ws.cell(row=sub_row, column=start_col + col_offset)
            c.font = Font(size=9, color="555555")
            if col_offset % 2 == 0:
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")
                
        # 5. Card Borders
        thin = Side(style="thin", color="D9D9D9")
        for row in ws.iter_rows(min_col=start_col, max_col=start_col+3, min_row=start_row, max_row=start_row+2):
            for cell in row:
                cell.border = Border(top=thin, bottom=thin, left=thin, right=thin)
                
        # 6. Target-Driven Conditional Formatting
        green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        
        tgt_ref = f"${tgt_col_ltr}${sub_row}"
        if is_lower_better:
            ws.conditional_formatting.add(val_range, CellIsRule(operator="lessThanOrEqual", formula=[tgt_ref], fill=green_fill))
            ws.conditional_formatting.add(val_range, CellIsRule(operator="greaterThan", formula=[tgt_ref], fill=red_fill))
        else:
            ws.conditional_formatting.add(val_range, CellIsRule(operator="greaterThanOrEqual", formula=[tgt_ref], fill=green_fill))
            ws.conditional_formatting.add(val_range, CellIsRule(operator="lessThan", formula=[tgt_ref], fill=red_fill))

    # Render Cards across the Dashboard
    draw_kpi_card(ws_dash, 2, 8, "DSO", "DSO (Days Sales Outstanding)", is_lower_better=True, num_format="0")
    draw_kpi_card(ws_dash, 7, 8, "Sales", "Total Sales", is_lower_better=False, num_format="$#,##0")
    draw_kpi_card(ws_dash, 12, 8, "Gross Margin", "Gross Margin %", is_lower_better=False, num_format="0%")
    
    # Adjust column widths for masonry layout
    ws_dash.column_dimensions['A'].width = 3
    for card_start in [2, 7, 12]:
        ws_dash.column_dimensions[get_column_letter(card_start)].width = 14
        ws_dash.column_dimensions[get_column_letter(card_start + 1)].width = 11
        ws_dash.column_dimensions[get_column_letter(card_start + 2)].width = 11
        ws_dash.column_dimensions[get_column_letter(card_start + 3)].width = 11
        
    ws_dash.column_dimensions['F'].width = 3
    ws_dash.column_dimensions['K'].width = 3
```