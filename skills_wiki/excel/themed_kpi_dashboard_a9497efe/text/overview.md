```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Employs a "4-column split and merge" layout pattern to build structured KPI cards. The top rows of each card (Title and large Value) are merged across 4 columns to permit oversized fonts and spacious color blocks. The bottom row uses the 4 unmerged columns to align detailed comparative metrics ("Vs. Target" and "Vs. Prior") without forcing unnatural column widths on the rest of the sheet. `CellIsRule` conditional formatting is applied to the merged value area to indicate performance.
* **Applicability**: Best used for executive summaries or high-level status reports where you need to display dense comparative metrics (actuals vs targets/priors) in a highly readable, card-based visual format.

### 2. Structural Breakdown

- **Data Layout**: 4 columns allocated per KPI. Row 1 (Section Title) merges across all KPIs in the group. Row 2 (KPI Name) and Row 3 (KPI Value) merge across the 4 allocated columns. Row 4 splits into 4 individual cells for comparison labels and values.
- **Formula Logic**: Relative evaluation within Conditional Formatting (`CellIsRule`), comparing the merged value block against an absolute reference to the adjacent target cell.
- **Visual Design**: Gridlines disabled. Section headers use theme primary background with bold white text. KPI Names use theme secondary background. Value cells use a large font (size 24) and conditional fills (Light Green for favorable, Light Red for unfavorable).
- **Charts/Tables**: Pure cell-based card layout simulating visual "blocks" with uniform thin grey outer borders.
- **Theme Hooks**: Consumes `primary` (section headers, main title), `secondary` (sub-headers, active filters), and `text` (labels).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "KPI Dashboard", dashboard_data: dict = None, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    if not dashboard_data:
        dashboard_data = {
            "period": "Aug-20",
            "sections": [
                {
                    "title": "Working Capital Efficiency",
                    "kpis": [
                        {"name": "DSO (Days Sales Outstanding)", "value": 31, "target": 45, "prior": 41, "format": "0", "better": "lower"},
                        {"name": "DPO (Days Payables Outstanding)", "value": 89, "target": 90, "prior": 90, "format": "0", "better": "higher"},
                        {"name": "Non-Current AR %", "value": 0.12, "target": 0.03, "prior": 0.12, "format": "0%", "better": "lower"}
                    ]
                },
                {
                    "title": "Sales KPIs",
                    "kpis": [
                        {"name": "CAC (Customer Acq. Cost)", "value": 26319, "target": 15000, "prior": 17725, "format": "$#,##0", "better": "lower"},
                        {"name": "Sales vs. Budget %", "value": 1.62, "target": 1.00, "prior": 1.27, "format": "0%", "better": "higher"},
                        {"name": "Gross Margin", "value": 0.20, "target": 0.38, "prior": 0.26, "format": "0%", "better": "higher"}
                    ]
                }
            ]
        }
        
    themes = {
        "corporate_blue": {"primary": "4F81BD", "secondary": "DCE6F1", "text": "000000"},
        "exec_dark": {"primary": "203764", "secondary": "D9E1F2", "text": "000000"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # Dashboard Header
    ws.cell(row=2, column=2, value=title).font = Font(size=20, bold=True, color=palette["primary"])
    ws.cell(row=3, column=2, value="For the month of:").font = Font(bold=True)
    ws.cell(row=3, column=3, value=dashboard_data["period"]).fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
    
    current_row = 5
    
    thin_border = Border(
        left=Side(style='thin', color="BFBFBF"),
        right=Side(style='thin', color="BFBFBF"),
        top=Side(style='thin', color="BFBFBF"),
        bottom=Side(style='thin', color="BFBFBF")
    )
    
    for section in dashboard_data["sections"]:
        kpis = section["kpis"]
        start_col = 2
        total_cols = len(kpis) * 4
        
        # Section Title
        title_cell = ws.cell(row=current_row, column=start_col, value=section["title"])
        title_cell.font = Font(size=14, bold=True, color="FFFFFF")
        title_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells(start_row=current_row, start_column=start_col, end_row=current_row, end_column=start_col + total_cols - 1)
        
        current_row += 1
        
        for i, kpi in enumerate(kpis):
            col = start_col + (i * 4)
            
            # Set explicit column widths to force the 4-column grid layout
            ws.column_dimensions[get_column_letter(col)].width = 14
            ws.column_dimensions[get_column_letter(col+1)].width = 10
            ws.column_dimensions[get_column_letter(col+2)].width = 16
            ws.column_dimensions[get_column_letter(col+3)].width = 10
            
            # KPI Name (Merged)
            name_cell = ws.cell(row=current_row, column=col, value=kpi["name"])
            name_cell.font = Font(bold=True, color=palette["text"])
            name_cell.fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
            name_cell.alignment = Alignment(horizontal="center", vertical="center")
            ws.merge_cells(start_row=current_row, start_column=col, end_row=current_row, end_column=col+3)
            
            # KPI Value (Merged)
            val_cell = ws.cell(row=current_row+1, column=col, value=kpi["value"])
            val_cell.font = Font(size=24, bold=True)
            val_cell.alignment = Alignment(horizontal="center", vertical="center")
            val_cell.number_format = kpi["format"]
            ws.merge_cells(start_row=current_row+1, start_column=col, end_row=current_row+1, end_column=col+3)
            
            # Comparisons (Split across the 4 localized columns)
            lbl_tgt = ws.cell(row=current_row+2, column=col, value="Vs. Target")
            lbl_tgt.font = Font(size=9, color="595959")
            lbl_tgt.alignment = Alignment(horizontal="right")
            
            val_tgt = ws.cell(row=current_row+2, column=col+1, value=kpi["target"])
            val_tgt.font = Font(size=10, bold=True)
            val_tgt.number_format = kpi["format"]
            
            lbl_prior = ws.cell(row=current_row+2, column=col+2, value="Vs. Prior Month")
            lbl_prior.font = Font(size=9, color="595959")
            lbl_prior.alignment = Alignment(horizontal="right")
            
            val_prior = ws.cell(row=current_row+2, column=col+3, value=kpi["prior"])
            val_prior.font = Font(size=10, bold=True)
            val_prior.number_format = kpi["format"]
            
            # Apply borders around the entire KPI block
            for r in range(current_row, current_row+3):
                for c in range(col, col+4):
                    ws.cell(row=r, column=c).border = thin_border
            
            # Conditional Formatting for the Value range based on Target
            target_coord = f"${get_column_letter(col+1)}${current_row+2}"
            val_range = f"{get_column_letter(col)}{current_row+1}:{get_column_letter(col+3)}{current_row+1}"
            
            green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
            red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
            
            if kpi["better"] == "lower":
                ws.conditional_formatting.add(val_range, CellIsRule(operator='lessThanOrEqual', formula=[target_coord], fill=green_fill))
                ws.conditional_formatting.add(val_range, CellIsRule(operator='greaterThan', formula=[target_coord], fill=red_fill))
            else:
                ws.conditional_formatting.add(val_range, CellIsRule(operator='greaterThanOrEqual', formula=[target_coord], fill=green_fill))
                ws.conditional_formatting.add(val_range, CellIsRule(operator='lessThan', formula=[target_coord], fill=red_fill))
                
        # Advance row for the next section, plus a spacer row
        current_row += 4
```