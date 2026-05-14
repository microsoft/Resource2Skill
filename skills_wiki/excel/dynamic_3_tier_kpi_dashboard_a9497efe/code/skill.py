from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme Configuration
    theme_colors = {
        "corporate_blue": {"primary": "003366", "secondary": "4A90E2", "bg": "EAEAEA", "card": "FFFFFF"},
        "midnight": {"primary": "FFFFFF", "secondary": "34495E", "bg": "2C3E50", "card": "ECF0F1"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])

    # 2. Sheet Setup
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_staging = wb.create_sheet("Staging")
    ws_data = wb.create_sheet("Data")

    # 3. Populate Raw Data
    months = ["Jan-20", "Feb-20", "Mar-20", "Apr-20"]
    metrics = [
        # dir: -1 (lower is better), 1 (higher is better)
        {"category": "Working Capital", "name": "DSO (Days)", "target": 45, "dir": -1, "data": [56, 54, 41, 38]},
        {"category": "Working Capital", "name": "DPO (Days)", "target": 90, "dir": 1, "data": [85, 89, 92, 95]},
        {"category": "Sales", "name": "CAC ($)", "target": 15000, "dir": -1, "data": [17725, 16000, 14500, 14000]},
        {"category": "Sales", "name": "Gross Margin", "target": 0.35, "dir": 1, "data": [0.32, 0.34, 0.38, 0.40]}
    ]

    headers = ["Category", "Metric", "Target", "Direction"] + months
    ws_data.append(headers)
    for m in metrics:
        ws_data.append([m["category"], m["name"], m["target"], m["dir"]] + m["data"])

    # 4. Build Staging Layer (Calculations)
    ws_staging.append(["Metric", "Target", "Direction", "Current Value", "Prior Value"])
    for i, m in enumerate(metrics, start=2):
        ws_staging.cell(row=i, column=1, value=m["name"])
        
        # Static lookups for metric configuration
        ws_staging.cell(row=i, column=2, value=f'=INDEX(Data!$C$2:$C$10, MATCH(A{i}, Data!$B$2:$B$10, 0))')
        ws_staging.cell(row=i, column=3, value=f'=INDEX(Data!$D$2:$D$10, MATCH(A{i}, Data!$B$2:$B$10, 0))')
        
        # Dynamic lookups based on Dashboard Dropdown
        idx_match_cur = 'MATCH(Dashboard!$C$4, Data!$E$1:$Z$1, 0)'
        ws_staging.cell(row=i, column=4, value=f'=INDEX(Data!$E$2:$Z$10, MATCH(A{i}, Data!$B$2:$B$10, 0), {idx_match_cur})')
        
        idx_match_prior = 'MATCH(Dashboard!$C$4, Data!$E$1:$Z$1, 0)-1'
        ws_staging.cell(row=i, column=5, value=f'=IFERROR(INDEX(Data!$E$2:$Z$10, MATCH(A{i}, Data!$B$2:$B$10, 0), {idx_match_prior}), "N/A")')

    # 5. Build Dashboard Layer (Presentation)
    ws_dash.sheet_view.showGridLines = False
    
    # Paint canvas background
    bg_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    for row in ws_dash.iter_rows(min_row=1, max_row=25, min_col=1, max_col=12):
        for cell in row:
            cell.fill = bg_fill

    # Title & Controls
    title_cell = ws_dash["B2"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["primary"])

    ws_dash["B4"] = "For the month of:"
    ws_dash["B4"].font = Font(bold=True)
    
    dropdown_cell = ws_dash["C4"]
    dropdown_cell.value = "Mar-20"  # Default selected value
    dropdown_cell.fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    dropdown_cell.border = Border(outline=Side(style="thin", color="000000"))

    # Add Data Validation pointing to the dynamic timeline header in Data sheet
    dv = DataValidation(type="list", formula1="Data!$E$1:$H$1", allowBlank=False)
    ws_dash.add_data_validation(dv)
    dv.add(dropdown_cell)

    # 6. KPI Card Component Renderer
    def render_kpi_block(start_row: int, start_col: int, staging_row: int, metric_dict: dict):
        card_fill = PatternFill(start_color=palette["card"], end_color=palette["card"], fill_type="solid")
        
        # Header Row
        ws_dash.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col+3)
        header_cell = ws_dash.cell(row=start_row, column=start_col, value=metric_dict["name"])
        header_cell.fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
        header_cell.font = Font(color="FFFFFF", bold=True)
        header_cell.alignment = Alignment(horizontal="center")

        # Main KPI Value Row
        ws_dash.merge_cells(start_row=start_row+1, start_column=start_col, end_row=start_row+1, end_column=start_col+3)
        val_cell = ws_dash.cell(row=start_row+1, column=start_col, value=f'=Staging!D{staging_row}')
        val_cell.fill = card_fill
        val_cell.font = Font(size=22, bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        if "Margin" in metric_dict["name"]:
            val_cell.number_format = "0.0%"
        elif "$" in metric_dict["name"]:
            val_cell.number_format = "$#,##0"

        # Benchmarking / Context Row
        lbl_target = ws_dash.cell(row=start_row+2, column=start_col, value="Target:")
        val_target = ws_dash.cell(row=start_row+2, column=start_col+1, value=f'=Staging!B{staging_row}')
        lbl_prior = ws_dash.cell(row=start_row+2, column=start_col+2, value="Prior:")
        val_prior = ws_dash.cell(row=start_row+2, column=start_col+3, value=f'=Staging!E{staging_row}')

        for c in [lbl_target, val_target, lbl_prior, val_prior]:
            c.fill = card_fill
            c.font = Font(size=10, color="555555")
            if c.column in [start_col, start_col+2]:
                c.alignment = Alignment(horizontal="right")
            else:
                c.alignment = Alignment(horizontal="left")
            if "Margin" in metric_dict["name"] and c in [val_target, val_prior]:
                c.number_format = "0.0%"

        # Conditional Formatting for Main Value
        green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        green_font = Font(color="006100", size=22, bold=True)
        red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        red_font = Font(color="9C0006", size=22, bold=True)

        target_ref = f'Staging!$B${staging_row}'
        if metric_dict["dir"] == 1: # Higher is better
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='greaterThanOrEqual', formula=[target_ref], fill=green_fill, font=green_font))
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='lessThan', formula=[target_ref], fill=red_fill, font=red_font))
        else: # Lower is better
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='lessThanOrEqual', formula=[target_ref], fill=green_fill, font=green_font))
            ws_dash.conditional_formatting.add(val_cell.coordinate, CellIsRule(operator='greaterThan', formula=[target_ref], fill=red_fill, font=red_font))

    # Render layout grid
    render_kpi_block(7, 2, 2, metrics[0])  # DSO
    render_kpi_block(7, 7, 3, metrics[1])  # DPO
    render_kpi_block(11, 2, 4, metrics[2]) # CAC
    render_kpi_block(11, 7, 5, metrics[3]) # Gross Margin

    # Structure visual grid widths
    for col in ['A', 'F', 'K']:
        ws_dash.column_dimensions[col].width = 3
    for col in ['B', 'C', 'D', 'E', 'G', 'H', 'I', 'J']:
        ws_dash.column_dimensions[col].width = 12
