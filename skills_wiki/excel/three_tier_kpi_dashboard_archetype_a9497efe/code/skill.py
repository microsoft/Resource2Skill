def render_workbook(wb, *, title: str = "Monthly KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a complete 3-tier KPI dashboard workbook.
    Sheet 1: Raw Data
    Sheet 2: Calculated Staging
    Sheet 3: Presentation Dashboard with dropdowns and Conditional Formatting
    """
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.formatting.rule import CellIsRule

    # Theme setup
    palettes = {
        "corporate_blue": {"primary": "2F5597", "secondary": "D9E1F2", "good": "C6EFCE", "bad": "FFC7CE", "bg": "FFF2CC"},
        "modern_teal": {"primary": "005D5D", "secondary": "E0F2F1", "good": "C6EFCE", "bad": "FFC7CE", "bg": "F0F4C3"}
    }
    colors = palettes.get(theme, palettes["corporate_blue"])

    # Clean default sheet and setup 3-tier structure
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
    
    ws_data = wb.create_sheet("1) Data")
    ws_staging = wb.create_sheet("2) Staging")
    ws_dash = wb.create_sheet("3) Dashboard")

    # -------------------------------------------------------------------------
    # 1. Populate Raw Data
    # -------------------------------------------------------------------------
    data_rows = [
        ['Category', 'Jan-20', 'Feb-20', 'Mar-20'],
        ['Account Receivables Balance', 2800000, 2940000, 3087000],
        ['Credit Sales', 1500000, 1590000, 1685400],
        ['# of days', 31, 29, 31],
        ['Sales Actual', 1500000, 1590000, 1685400],
        ['Sales Budget', 1650000, 1752500, 1829125]
    ]
    for row in data_rows:
        ws_data.append(row)
    
    # Auto-width for readability
    ws_data.column_dimensions['A'].width = 30

    # -------------------------------------------------------------------------
    # 2. Populate Staging (Calculated Metrics)
    # -------------------------------------------------------------------------
    # Formulas reference the Data tab to calculate DSO and Sales vs Budget
    staging_rows = [
        ['KPI', 'Jan-20', 'Feb-20', 'Mar-20'],
        ['DSO', "=('1) Data'!B2/'1) Data'!B3)*'1) Data'!B4", "=('1) Data'!C2/'1) Data'!C3)*'1) Data'!C4", "=('1) Data'!D2/'1) Data'!D3)*'1) Data'!D4"],
        ['DSO Target', 45, 45, 45],
        ['Sales vs. Budget %', "='1) Data'!B5/'1) Data'!B6", "='1) Data'!C5/'1) Data'!C6", "='1) Data'!D5/'1) Data'!D6"],
        ['Sales Target', 1, 1, 1]
    ]
    for row in staging_rows:
        ws_staging.append(row)
        
    ws_staging.column_dimensions['A'].width = 20

    # -------------------------------------------------------------------------
    # 3. Build Presentation Dashboard
    # -------------------------------------------------------------------------
    ws_dash.sheet_view.showGridLines = False

    header_fill = PatternFill(start_color=colors["primary"], end_color=colors["primary"], fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=14)
    card_header_fill = PatternFill(start_color=colors["secondary"], end_color=colors["secondary"], fill_type="solid")
    good_fill = PatternFill(start_color=colors["good"], end_color=colors["good"], fill_type="solid")
    bad_fill = PatternFill(start_color=colors["bad"], end_color=colors["bad"], fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color="A6A6A6"),
        right=Side(style='thin', color="A6A6A6"),
        top=Side(style='thin', color="A6A6A6"),
        bottom=Side(style='thin', color="A6A6A6")
    )

    # --- Dashboard Title ---
    ws_dash.merge_cells('B2:F3')
    title_cell = ws_dash['B2']
    title_cell.value = title
    title_cell.fill = header_fill
    title_cell.font = Font(color="FFFFFF", bold=True, size=20)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # --- Month Dropdown Selector ---
    ws_dash['B5'] = "For the month of:"
    ws_dash['B5'].font = Font(bold=True)
    ws_dash['B5'].alignment = Alignment(horizontal="right", vertical="center")
    
    ws_dash['C5'] = "Feb-20"  # Default selection
    ws_dash['C5'].fill = PatternFill(start_color=colors["bg"], end_color=colors["bg"], fill_type="solid")
    ws_dash['C5'].border = thin_border
    ws_dash['C5'].alignment = Alignment(horizontal="center", vertical="center")

    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20"', allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash['C5'])

    # --- Section Header ---
    ws_dash.merge_cells('B7:F7')
    sec_cell = ws_dash['B7']
    sec_cell.value = "Working Capital & Sales KPIs"
    sec_cell.fill = header_fill
    sec_cell.font = header_font
    sec_cell.alignment = Alignment(horizontal="center", vertical="center")

    # =========================================================================
    # KPI Card 1: DSO (Lower is better)
    # =========================================================================
    ws_dash.merge_cells('B9:C9')
    ws_dash['B9'] = "DSO (Days Sales Outstanding)"
    ws_dash['B9'].fill = card_header_fill
    ws_dash['B9'].alignment = Alignment(horizontal="center")
    ws_dash['B9'].font = Font(bold=True)

    # Main KPI Value
    ws_dash.merge_cells('B10:C11')
    kpi1_val = ws_dash['B10']
    kpi1_val.value = "=INDEX('2) Staging'!$B$2:$D$2, 1, MATCH($C$5, '2) Staging'!$B$1:$D$1, 0))"
    kpi1_val.font = Font(size=26, bold=True)
    kpi1_val.alignment = Alignment(horizontal="center", vertical="center")
    kpi1_val.number_format = '0'

    # Sub-metrics
    ws_dash['B12'] = "Vs. Target"
    ws_dash['B12'].font = Font(size=10, italic=True)
    ws_dash['C12'] = "=INDEX('2) Staging'!$B$3:$D$3, 1, MATCH($C$5, '2) Staging'!$B$1:$D$1, 0))"
    ws_dash['C12'].font = Font(size=10)
    ws_dash['C12'].alignment = Alignment(horizontal="right")

    # Apply borders
    for row in range(9, 13):
        for col in ['B', 'C']:
            ws_dash[f"{col}{row}"].border = thin_border

    # Conditional Formatting for DSO (<= Target is Good, > Target is Bad)
    ws_dash.conditional_formatting.add(
        'B10:C11', CellIsRule(operator='lessThanOrEqual', formula=['$C$12'], fill=good_fill)
    )
    ws_dash.conditional_formatting.add(
        'B10:C11', CellIsRule(operator='greaterThan', formula=['$C$12'], fill=bad_fill)
    )

    # =========================================================================
    # KPI Card 2: Sales vs Budget (Higher is better)
    # =========================================================================
    ws_dash.merge_cells('E9:F9')
    ws_dash['E9'] = "Sales vs. Budget %"
    ws_dash['E9'].fill = card_header_fill
    ws_dash['E9'].alignment = Alignment(horizontal="center")
    ws_dash['E9'].font = Font(bold=True)

    # Main KPI Value
    ws_dash.merge_cells('E10:F11')
    kpi2_val = ws_dash['E10']
    kpi2_val.value = "=INDEX('2) Staging'!$B$4:$D$4, 1, MATCH($C$5, '2) Staging'!$B$1:$D$1, 0))"
    kpi2_val.font = Font(size=26, bold=True)
    kpi2_val.alignment = Alignment(horizontal="center", vertical="center")
    kpi2_val.number_format = '0%'

    # Sub-metrics
    ws_dash['E12'] = "Vs. Target"
    ws_dash['E12'].font = Font(size=10, italic=True)
    ws_dash['F12'] = "=INDEX('2) Staging'!$B$5:$D$5, 1, MATCH($C$5, '2) Staging'!$B$1:$D$1, 0))"
    ws_dash['F12'].font = Font(size=10)
    ws_dash['F12'].alignment = Alignment(horizontal="right")
    ws_dash['F12'].number_format = '0%'

    # Apply borders
    for row in range(9, 13):
        for col in ['E', 'F']:
            ws_dash[f"{col}{row}"].border = thin_border

    # Conditional Formatting for Sales (>= Target is Good, < Target is Bad)
    ws_dash.conditional_formatting.add(
        'E10:F11', CellIsRule(operator='greaterThanOrEqual', formula=['$F$12'], fill=good_fill)
    )
    ws_dash.conditional_formatting.add(
        'E10:F11', CellIsRule(operator='lessThan', formula=['$F$12'], fill=bad_fill)
    )

    # -------------------------------------------------------------------------
    # Column Sizing
    # -------------------------------------------------------------------------
    ws_dash.column_dimensions['A'].width = 3
    ws_dash.column_dimensions['B'].width = 20
    ws_dash.column_dimensions['C'].width = 15
    ws_dash.column_dimensions['D'].width = 4   # Spacer column
    ws_dash.column_dimensions['E'].width = 20
    ws_dash.column_dimensions['F'].width = 15
