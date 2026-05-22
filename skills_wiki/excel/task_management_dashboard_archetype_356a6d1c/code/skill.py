def render_workbook(wb, *, title: str = "Task Management Tracker", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.worksheet.table import Table, TableStyleInfo
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.label import DataLabelList

    # Colors
    primary_color = "1F4E78"   # Dark Blue
    secondary_color = "DDEBF7" # Light Blue
    accent_red = "C00000"      # Red

    # 1. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_supp = wb.create_sheet("Support")
    
    # 2. Add Reference Data to Support Sheet
    statuses = ["Completed", "In Progress", "Not Started"]
    owners = ["Sarah Johnson", "David Kim", "James Miller", "Alex Chen", "Emily Davis"]
    teams = ["Finance", "Strategy", "HR", "Marketing"]
    
    # Status Counts
    ws_supp["A1"], ws_supp["B1"] = "Status", "Count"
    for i, st in enumerate(statuses, 2):
        ws_supp[f"A{i}"] = st
        ws_supp[f"B{i}"] = f'=COUNTIF(Tasks[Status], A{i})'
    ws_supp[f"A{len(statuses)+2}"] = "Total"
    ws_supp[f"B{len(statuses)+2}"] = f'=SUM(B2:B{len(statuses)+1})'
        
    # Owner Counts
    ws_supp["D1"], ws_supp["E1"] = "Owners", "Count"
    for i, own in enumerate(owners, 2):
        ws_supp[f"D{i}"] = own
        ws_supp[f"E{i}"] = f'=COUNTIF(Tasks[Task Owner], D{i})'
        
    # Team Counts
    ws_supp["G1"], ws_supp["H1"] = "Team", "Count"
    for i, tm in enumerate(teams, 2):
        ws_supp[f"G{i}"] = tm
        ws_supp[f"H{i}"] = f'=COUNTIF(Tasks[Team], G{i})'
        
    # Overdue Check
    ws_supp["J1"], ws_supp["K1"] = "Overdue?", "Count"
    ws_supp["J2"] = "TRUE"
    ws_supp["K2"] = '=COUNTIF(Tasks[Overdue?], TRUE)'

    # 3. Setup Dashboard KPIs Header
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Title
    ws_dash.merge_cells("A1:J2")
    ws_dash["A1"] = title
    ws_dash["A1"].font = Font(size=20, bold=True, color="FFFFFF")
    ws_dash["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["A1"].fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")
    
    # KPI 1: Status Counts
    fill_kpi = PatternFill(start_color=secondary_color, end_color=secondary_color, fill_type="solid")
    ws_dash["A4"], ws_dash["B4"] = "Completed", "Not Started"
    ws_dash["A5"], ws_dash["B5"] = "=Support!B2", "=Support!B4"
    ws_dash["A7"], ws_dash["B7"] = "In Progress", "Total Tasks"
    ws_dash["A8"], ws_dash["B8"] = "=Support!B3", "=Support!B5"
    
    for row in [4, 5, 7, 8]:
        for col in ["A", "B"]:
            cell = ws_dash[f"{col}{row}"]
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.fill = fill_kpi
            if row in [4, 7]:
                cell.font = Font(bold=True, size=12)
            else:
                cell.font = Font(bold=True, size=18, color=primary_color)
    
    # KPI 2: Overdue Tasks
    ws_dash.merge_cells("I4:J5")
    ws_dash["I4"] = "Overdue Tasks"
    ws_dash["I4"].font = Font(bold=True, size=14)
    ws_dash["I4"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws_dash.merge_cells("I6:J9")
    ws_dash["I6"] = "=Support!K2"
    ws_dash["I6"].font = Font(bold=True, size=36, color=accent_red)
    ws_dash["I6"].alignment = Alignment(horizontal="center", vertical="center")
    
    for row in range(4, 10):
        for col in ["I", "J"]:
            ws_dash[f"{col}{row}"].fill = fill_kpi

    # 4. Charts
    chart_owner = BarChart()
    chart_owner.type = "bar" # Horizontal bars
    chart_owner.title = "# of Tasks by Owner"
    chart_owner.legend = None
    chart_owner.gapWidth = 70
    chart_owner.dataLabels = DataLabelList()
    chart_owner.dataLabels.showVal = True
    chart_owner.add_data(Reference(ws_supp, min_col=5, min_row=1, max_row=len(owners)+1), titles_from_data=True)
    chart_owner.set_categories(Reference(ws_supp, min_col=4, min_row=2, max_row=len(owners)+1))
    chart_owner.width, chart_owner.height = 10, 6
    ws_dash.add_chart(chart_owner, "C3")
    
    chart_team = BarChart()
    chart_team.type = "bar"
    chart_team.title = "# of Tasks by Team"
    chart_team.legend = None
    chart_team.gapWidth = 70
    chart_team.dataLabels = DataLabelList()
    chart_team.dataLabels.showVal = True
    chart_team.add_data(Reference(ws_supp, min_col=8, min_row=1, max_row=len(teams)+1), titles_from_data=True)
    chart_team.set_categories(Reference(ws_supp, min_col=7, min_row=2, max_row=len(teams)+1))
    chart_team.width, chart_team.height = 10, 6
    ws_dash.add_chart(chart_team, "F3")
    
    # 5. Table Data & Formatting
    headers = ["Task ID", "Task Name", "Team", "Task Owner", "Start Date", "Due Date", "Task Duration", "Status", "Overdue?", "Comments"]
    ws_dash.append([]) # Row 13
    ws_dash.append([]) # Row 14
    ws_dash.append(headers) # Row 15
    
    sample_data = [
        ["T001", "Prepare Q4 Financial Report", "Finance", "Sarah Johnson", "2025-09-02", "2025-09-20", "", "Completed", "", "Submitted to CFO."],
        ["T002", "Conduct Market Research", "Strategy", "David Kim", "2025-09-05", "2025-09-25", "", "In Progress", "", "Draft findings ready."],
        ["T003", "Redesign Website Homepage", "Marketing", "Emily Davis", "2025-07-10", "2025-08-05", "", "Not Started", "", "Waiting for design approval."],
    ]
    
    for r, row in enumerate(sample_data, start=16):
        ws_dash.append(row)
        ws_dash[f"G{r}"] = '=[@[Due Date]]-[@[Start Date]]'
        ws_dash[f"G{r}"].number_format = '0 "Days"'
        ws_dash[f"I{r}"] = '=AND([@Status]<>"Completed", [@[Due Date]]<TODAY())'
        ws_dash[f"E{r}"].number_format = "yyyy-mm-dd"
        ws_dash[f"F{r}"].number_format = "yyyy-mm-dd"
        
    tab = Table(displayName="Tasks", ref=f"A15:J{15 + len(sample_data)}")
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws_dash.add_table(tab)
    
    # Layout adjustments
    col_widths = {"A": 10, "B": 28, "C": 15, "D": 20, "E": 14, "F": 14, "G": 15, "H": 15, "I": 12, "J": 30}
    for col, width in col_widths.items():
        ws_dash.column_dimensions[col].width = width
        
    # 6. Data Validation
    dv_team = DataValidation(type="list", formula1="=Support!$G$2:$G$5", allow_blank=True)
    dv_owner = DataValidation(type="list", formula1="=Support!$D$2:$D$6", allow_blank=True)
    dv_status = DataValidation(type="list", formula1='="Completed,In Progress,Not Started"', allow_blank=True)
    
    ws_dash.add_data_validation(dv_team)
    ws_dash.add_data_validation(dv_owner)
    ws_dash.add_data_validation(dv_status)
    dv_team.add("C16:C1000")
    dv_owner.add("D16:D1000")
    dv_status.add("H16:H1000")
    
    # 7. Conditional Formatting
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    green_font = Font(color="006100")
    yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    yellow_font = Font(color="9C6500")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    red_font = Font(color="9C0006")
    
    ws_dash.conditional_formatting.add("H16:H1000", CellIsRule(operator="equal", formula=['"Completed"'], fill=green_fill, font=green_font))
    ws_dash.conditional_formatting.add("H16:H1000", CellIsRule(operator="equal", formula=['"In Progress"'], fill=yellow_fill, font=yellow_font))
    ws_dash.conditional_formatting.add("H16:H1000", CellIsRule(operator="equal", formula=['"Not Started"'], fill=red_fill, font=red_font))
    ws_dash.conditional_formatting.add("I16:I1000", CellIsRule(operator="equal", formula=['TRUE'], fill=red_fill, font=red_font))
    
    # 8. Freeze Panes
    ws_dash.freeze_panes = "A16"
