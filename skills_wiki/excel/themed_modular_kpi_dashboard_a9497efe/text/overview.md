```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Modular KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Renders a modular grid of 4x3 KPI cards with dynamic conditional formatting rules pointing to an inline target cell. The shell configures column widths, removes gridlines, and establishes a visual hierarchy with bold, solid-fill section headers above isolated data blocks.
* **Applicability**: When building executive summaries, balanced scorecards, or top-level dashboards where stakeholders need to see absolute figures immediately alongside performance status (green/red background) and context (target/prior period).

### 2. Structural Breakdown

- **Data Layout**: Each KPI card occupies a 3-row by 4-column block. Row 1 is the merged header; Row 2 is the merged oversized value; Row 3 holds the comparison metrics ("Vs Target" and "Vs Prior").
- **Formula Logic**: Uses standard openpyxl `CellIsRule` with absolute cell references to drive the background color of the main value cell based on the neighboring target value.
- **Visual Design**: Gridlines are hidden for a clean dashboard look. Section headers span the dashboard width. Cards use large fonts (size 24) for the focal metric. Good/Bad statuses use standard Excel green (`C6EFCE`) and red (`FFC7CE`) fills.
- **Charts/Tables**: Dropdown implemented via `DataValidation` to simulate a dynamic period selector.
- **Theme Hooks**: Utilizes `primary` for section headers and the dashboard title, and `text` for the large KPI figures.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", dashboard_data: dict = None, **kwargs) -> None:
    """
    Renders a clean, modular KPI Dashboard.
    Each KPI card is a 3x4 cell block, automatically formatted with conditional color statuses.
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    # 1. Theme Configuration
    theme_colors = {
        "corporate_blue": {"primary": "4F81BD", "text": "000000"},
        "modern_green": {"primary": "9BBB59", "text": "000000"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    # Hide gridlines for an application-like feel
    ws.sheet_view.showGridLines = False

    # 2. Example Data Payload
    if not dashboard_data:
        dashboard_data = {
            "Working Capital Efficiency": [
                {"name": "DSO (Days Sales Outstanding)", "value": 31, "target": 45, "prior": 41, "good_direction": "down", "format": "0"},
                {"name": "DPO (Days Payables Outstanding)", "value": 89, "target": 90, "prior": 90, "good_direction": "up", "format": "0"},
                {"name": "Non-Current AR %", "value": 0.12, "target": 0.03, "prior": 0.12, "good_direction": "down", "format": "0%"}
            ],
            "Sales KPIs": [
                {"name": "CAC (Customer Acq. Cost)", "value": 26319, "target": 15000, "prior": 17725, "good_direction": "down", "format": "$#,##0"},
                {"name": "Sales vs. Budget %", "value": 1.62, "target": 1.00, "prior": 1.27, "good_direction": "up", "format": "0%"},
                {"name": "Gross Margin", "value": 0.20, "target": 0.38, "prior": 0.26, "good_direction": "up", "format": "0%"}
            ]
        }

    # 3. Build Header and Month Selector
    ws.merge_cells("F1:J2")
    title_cell = ws.cell(1, 6, title)
    title_cell.font = Font(size=20, bold=True, color=palette["primary"])
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.cell(2, 2, "For the month of:").font = Font(bold=True)
    month_cell = ws.cell(2, 3, "Aug-20")
    month_cell.fill = PatternFill("solid", fgColor="FFF2CC")
    month_cell.alignment = Alignment(horizontal="center")
    
    # Add simple data validation for interaction
    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20,Apr-20,May-20,Jun-20,Jul-20,Aug-20"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(month_cell)

    # 4. Standard Component Styles
    section_fill = PatternFill("solid", fgColor=palette["primary"])
    section_font = Font(color="FFFFFF", bold=True, size=14)
    header_fill = PatternFill("solid", fgColor="F2F2F2")
    header_font = Font(bold=True)
    thin_border = Border(left=Side(style="thin", color="D9D9D9"), right=Side(style="thin", color="D9D9D9"), 
                         top=Side(style="thin", color="D9D9D9"), bottom=Side(style="thin", color="D9D9D9"))

    green_fill = PatternFill("solid", fgColor="C6EFCE")
    green_font = Font(color="006100")
    red_fill = PatternFill("solid", fgColor="FFC7CE")
    red_font = Font(color="9C0006")

    # Lock column widths for structural consistency
    for col_idx in range(2, 17):
        ws.column_dimensions[get_column_letter(col_idx)].width = 13

    # 5. Render Sections and KPI Cards dynamically
    current_row = 4
    
    for section_name, kpis in dashboard_data.items():
        # Draw Section Banner
        ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=15)
        sec_cell = ws.cell(current_row, 2, section_name)
        sec_cell.fill = section_fill
        sec_cell.font = section_font
        sec_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        current_row += 2
        start_col = 2
        
        for kpi in kpis:
            # Layout boundaries (3 rows x 4 columns)
            for r in range(current_row, current_row + 3):
                for c in range(start_col, start_col + 4):
                    ws.cell(r, c).border = thin_border
            
            # KPI Header Layer
            ws.merge_cells(start_row=current_row, start_column=start_col, end_row=current_row, end_column=start_col+3)
            hdr_cell = ws.cell(current_row, start_col, kpi["name"])
            hdr_cell.fill = header_fill
            hdr_cell.font = header_font
            hdr_cell.alignment = Alignment(horizontal="center", vertical="center")
            
            # KPI Large Value Layer
            ws.merge_cells(start_row=current_row+1, start_column=start_col, end_row=current_row+1, end_column=start_col+3)
            val_cell = ws.cell(current_row+1, start_col, kpi["value"])
            val_cell.font = Font(size=24, bold=True, color=palette["text"])
            val_cell.alignment = Alignment(horizontal="center", vertical="center")
            val_cell.number_format = kpi["format"]
            
            # Context Metrics Layer
            ws.cell(current_row+2, start_col, "Vs. Target").alignment = Alignment(horizontal="left")
            target_cell = ws.cell(current_row+2, start_col+1, kpi["target"])
            target_cell.number_format = kpi["format"]
            
            ws.cell(current_row+2, start_col+2, "Vs. Prior").alignment = Alignment(horizontal="left")
            ws.cell(current_row+2, start_col+3, kpi["prior"]).number_format = kpi["format"]
            
            # Apply Conditional Formatting to the focal metric
            target_addr = f"${get_column_letter(start_col+1)}${current_row+2}"
            val_range = f"{get_column_letter(start_col)}{current_row+1}:{get_column_letter(start_col+3)}{current_row+1}"
            
            if kpi["good_direction"] == "down":
                ws.conditional_formatting.add(val_range, CellIsRule(operator="lessThan", formula=[target_addr], fill=green_fill, font=green_font))
                ws.conditional_formatting.add(val_range, CellIsRule(operator="greaterThanOrEqual", formula=[target_addr], fill=red_fill, font=red_font))
            else:
                ws.conditional_formatting.add(val_range, CellIsRule(operator="greaterThanOrEqual", formula=[target_addr], fill=green_fill, font=green_font))
                ws.conditional_formatting.add(val_range, CellIsRule(operator="lessThan", formula=[target_addr], fill=red_fill, font=red_font))
                
            start_col += 5 # Move right by 1 card block + 1 spacing column
            
        current_row += 4 # Move down for the next section array
```
```