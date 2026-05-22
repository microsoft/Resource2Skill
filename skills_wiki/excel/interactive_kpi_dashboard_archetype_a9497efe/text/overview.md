```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive KPI Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet architecture where a "Dashboard" presentation layer queries a hidden "Staging" data matrix using a Data Validation dropdown and `INDEX(MATCH())` combinations. Calculates prior periods natively by shifting the `MATCH` index by -1.
* **Applicability**: Perfect for high-level executive summaries, monthly reporting packages, or any scenario where you need to display "Big Number" metrics with variance to target and prior periods without relying on VBA or PivotTables.

### 2. Structural Breakdown

- **Data Layout**: Two-sheet system. A hidden `Staging` sheet holds targets and a matrix of time-series data. The `Dashboard` sheet acts as a grid of spatial "cards" separated by spacer columns.
- **Formula Logic**: Uses `=INDEX(Staging!$C$R:$F$R, MATCH(Selected_Month, Staging!$C$1:$F$1, 0))` to pull the current period value. Subtracting 1 from the `MATCH` result effortlessly grabs the prior period.
- **Visual Design**: Cards use an outer outline border, strong theme-driven header fills, and massive 20pt fonts for the primary metric.
- **Charts/Tables**: Employs spatial cell-merging to create a "Dashboard Tile" aesthetic rather than native charts.
- **Theme Hooks**: Consumes `primary` for section banners and active UI elements, `secondary` for card headers, and standard red/green semantics for conditional formatting based on target performance.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme Setup
    theme_colors = {
        "corporate_blue": {"primary": "2F5496", "secondary": "D9E1F2"},
        "executive_gray": {"primary": "404040", "secondary": "D9D9D9"},
        "emerald_green": {"primary": "385723", "secondary": "E2EFDA"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    primary_color = palette["primary"]
    secondary_color = palette["secondary"]

    # 2. Setup Sheets
    if "Sheet" in wb.sheetnames:
        dash_ws = wb["Sheet"]
        dash_ws.title = "Dashboard"
    else:
        dash_ws = wb.create_sheet("Dashboard")
    
    stage_ws = wb.create_sheet("Staging")
    
    # 3. Define KPI Data Model
    months = ["Dec-19", "Jan-20", "Feb-20", "Mar-20"]
    selectable_months = months[1:] # Dropdown hides the first month (used only for 'prior' lookups)
    
    kpi_sections = {
        "Working Capital Efficiency": [
            {"name": "DSO (Days)", "target": 45, "lower_better": True, "values": [54, 50, 48, 41], "fmt": "0"},
            {"name": "DPO (Days)", "target": 90, "lower_better": False, "values": [80, 85, 89, 100], "fmt": "0"},
            {"name": "Non-Current AR %", "target": 0.03, "lower_better": True, "values": [0.05, 0.04, 0.02, 0.01], "fmt": "0%"}
        ],
        "Sales KPIs": [
            {"name": "CAC ($)", "target": 15000, "lower_better": True, "values": [16500, 16000, 15500, 14000], "fmt": "$#,##0"},
            {"name": "Sales vs Budget %", "target": 1.0, "lower_better": False, "values": [0.95, 0.98, 1.05, 1.27], "fmt": "0%"},
            {"name": "Gross Margin %", "target": 0.38, "lower_better": False, "values": [0.35, 0.36, 0.38, 0.40], "fmt": "0%"}
        ]
    }
    
    # 4. Populate Staging Matrix
    stage_ws["A1"] = "KPI Name"
    stage_ws["B1"] = "Target"
    for c_idx, m in enumerate(months, start=3):
        stage_ws.cell(row=1, column=c_idx, value=m)
        
    staging_row = 2
    kpi_row_map = {}
    
    for sec_name, kpis in kpi_sections.items():
        for kpi in kpis:
            stage_ws.cell(row=staging_row, column=1, value=kpi["name"])
            stage_ws.cell(row=staging_row, column=2, value=kpi["target"])
            for c_idx, val in enumerate(kpi["values"], start=3):
                stage_ws.cell(row=staging_row, column=c_idx, value=val)
            kpi_row_map[kpi["name"]] = staging_row
            staging_row += 1
            
    # 5. Build Interactive Dashboard
    dash_ws["A1"] = title
    dash_ws["A1"].font = Font(size=24, bold=True, color="FFFFFF")
    dash_ws["A1"].fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")
    dash_ws.merge_cells("A1:O2")
    dash_ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    # Month Selector Dropdown
    dash_ws["B4"] = "For the month of:"
    dash_ws["B4"].font = Font(bold=True)
    dash_ws["B4"].alignment = Alignment(horizontal="right")
    
    dash_ws["C4"] = selectable_months[-1]
    dash_ws["C4"].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    dash_ws["C4"].border = Border(bottom=Side(style="thick", color=primary_color))
    
    dv = DataValidation(type="list", formula1=f'"{",".join(selectable_months)}"', allow_blank=False)
    dash_ws.add_data_validation(dv)
    dv.add(dash_ws["C4"])
    
    dash_row = 6
    
    # 6. Render KPI Cards
    for sec_name, kpis in kpi_sections.items():
        # Section Header
        sec_cell = dash_ws.cell(row=dash_row, column=2, value=sec_name)
        sec_cell.font = Font(size=14, bold=True, color="FFFFFF")
        sec_cell.fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")
        sec_cell.alignment = Alignment(horizontal="center")
        dash_ws.merge_cells(start_row=dash_row, start_column=2, end_row=dash_row, end_column=15)
        
        dash_row += 2
        
        # 3 Cards per row
        col_offsets = [2, 7, 12] 
        
        for kpi, col_start in zip(kpis, col_offsets):
            s_row = kpi_row_map[kpi["name"]]
            
            # Card Sub-header (KPI Name)
            name_cell = dash_ws.cell(row=dash_row, column=col_start, value=kpi["name"])
            name_cell.font = Font(bold=True)
            name_cell.fill = PatternFill(start_color=secondary_color, end_color=secondary_color, fill_type="solid")
            name_cell.alignment = Alignment(horizontal="center")
            dash_ws.merge_cells(start_row=dash_row, start_column=col_start, end_row=dash_row, end_column=col_start+3)
            
            # Main Metric Value (Dynamic INDEX/MATCH)
            val_cell = dash_ws.cell(row=dash_row+1, column=col_start)
            val_cell.value = f"=INDEX(Staging!$C${s_row}:$F${s_row}, MATCH($C$4, Staging!$C$1:$F$1, 0))"
            val_cell.font = Font(size=20, bold=True)
            val_cell.alignment = Alignment(horizontal="center", vertical="center")
            val_cell.number_format = kpi["fmt"]
            dash_ws.merge_cells(start_row=dash_row+1, start_column=col_start, end_row=dash_row+1, end_column=col_start+3)
            
            # Metadata: Vs Target
            dash_ws.cell(row=dash_row+2, column=col_start, value="Vs. Target").font = Font(size=9, color="595959")
            t_cell = dash_ws.cell(row=dash_row+2, column=col_start+1, value=f"=Staging!B{s_row}")
            t_cell.number_format = kpi["fmt"]
            t_cell.font = Font(size=9, bold=True)
            
            # Metadata: Vs Prior Month (Shift MATCH array index by -1)
            dash_ws.cell(row=dash_row+2, column=col_start+2, value="Vs. Prior").font = Font(size=9, color="595959")
            p_cell = dash_ws.cell(row=dash_row+2, column=col_start+3)
            p_cell.value = f"=INDEX(Staging!$C${s_row}:$F${s_row}, MATCH($C$4, Staging!$C$1:$F$1, 0) - 1)"
            p_cell.number_format = kpi["fmt"]
            p_cell.font = Font(size=9, bold=True)
            
            # Card Outline Borders
            thin = Side(border_style="thin", color="D9D9D9")
            for r in range(dash_row, dash_row+3):
                for c in range(col_start, col_start+4):
                    dash_ws.cell(row=r, column=c).border = Border(
                        top=thin if r == dash_row else None,
                        bottom=thin if r == dash_row+2 else None,
                        left=thin if c == col_start else None,
                        right=thin if c == col_start+3 else None
                    )
                    
            # Semantic Conditional Formatting
            green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
            green_font = Font(color="006100", size=20, bold=True)
            red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
            red_font = Font(color="9C0006", size=20, bold=True)
            
            target_ref = f"${get_column_letter(col_start+1)}${dash_row+2}" # Absolute ref to the card's target cell
            val_coord = val_cell.coordinate
            
            if kpi["lower_better"]:
                dash_ws.conditional_formatting.add(val_coord, CellIsRule(operator='lessThan', formula=[target_ref], fill=green_fill, font=green_font))
                dash_ws.conditional_formatting.add(val_coord, CellIsRule(operator='greaterThan', formula=[target_ref], fill=red_fill, font=red_font))
            else:
                dash_ws.conditional_formatting.add(val_coord, CellIsRule(operator='greaterThan', formula=[target_ref], fill=green_fill, font=green_font))
                dash_ws.conditional_formatting.add(val_coord, CellIsRule(operator='lessThan', formula=[target_ref], fill=red_fill, font=red_font))

        dash_row += 5
        
    # Formatting adjustments
    for col in [1, 6, 11]: # Spacer columns
        dash_ws.column_dimensions[get_column_letter(col)].width = 3
    for col in [2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 15]:
        dash_ws.column_dimensions[get_column_letter(col)].width = 11

    # Hide the data engine mechanics
    stage_ws.sheet_state = 'hidden'
```
```