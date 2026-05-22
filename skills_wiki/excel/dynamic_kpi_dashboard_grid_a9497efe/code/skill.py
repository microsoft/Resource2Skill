def render_sheet(wb, sheet_name: str, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a dynamic KPI Dashboard with color-coded metric cards and a period selector.
    """
    ws = wb.create_sheet(sheet_name)
    
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.worksheet.datavalidation import DataValidation
    
    # Theme palette fallback
    palette = kwargs.get("palette", {
        "primary": "4A86E8",       # Category 2 Header
        "secondary": "F28E2B",     # Category 1 Header
        "good_bg": "C6EFCE",
        "good_fg": "006100",
        "bad_bg": "FFC7CE",
        "bad_fg": "9C0006",
        "card_header_bg": "E7E6E6",
        "text_main": "333333",
        "text_muted": "595959",
        "border": "D9D9D9"
    })
    
    # Common Styles
    title_font = Font(bold=True, size=11, color=palette["text_main"])
    val_font = Font(bold=True, size=24, color="000000")
    sub_label_font = Font(size=9, color=palette["text_muted"], bold=True)
    sub_val_font = Font(size=9, color="000000")
    
    green_fill = PatternFill(start_color=palette["good_bg"], end_color=palette["good_bg"], fill_type="solid")
    green_font = Font(color=palette["good_fg"], bold=True, size=24)
    red_fill = PatternFill(start_color=palette["bad_bg"], end_color=palette["bad_bg"], fill_type="solid")
    red_font = Font(color=palette["bad_fg"], bold=True, size=24)
    
    kpi_header_fill = PatternFill(start_color=palette["card_header_bg"], end_color=palette["card_header_bg"], fill_type="solid")
    
    # Setup standard column widths for the grid
    for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        ws.column_dimensions[col].width = 16
        
    # Build Top Controls (Month Dropdown)
    ws['B2'] = "For the month of:"
    ws['B2'].font = title_font
    ws['B2'].alignment = Alignment(horizontal="right")
    
    ws['C2'] = "Jul-20"
    ws['C2'].font = title_font
    ws['C2'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    ws['C2'].border = Border(bottom=Side(style="thick", color="F2C80F"))
    ws['C2'].alignment = Alignment(horizontal="center")
    
    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20,Apr-20,May-20,Jun-20,Jul-20"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(ws['C2'])
    
    def render_kpi(start_col: str, row: int, kpi_title: str, value: float, target: float, prior: float, good_direction: str = "less", num_format: str = "#,##0"):
        """Helper to stamp a modular 2x4 cell KPI Card onto the sheet."""
        c1 = start_col
        c2 = chr(ord(start_col) + 1)
        
        # 1. Card Title
        ws.merge_cells(f"{c1}{row}:{c2}{row}")
        hdr_cell = ws[f"{c1}{row}"]
        hdr_cell.value = kpi_title
        hdr_cell.font = title_font
        hdr_cell.fill = kpi_header_fill
        hdr_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[row].height = 20
        
        # 2. Main Large Value
        ws.merge_cells(f"{c1}{row+1}:{c2}{row+1}")
        val_cell = ws[f"{c1}{row+1}"]
        val_cell.value = value
        val_cell.font = val_font
        val_cell.number_format = num_format
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[row+1].height = 40
        
        # 3. Sub-metrics (Target & Prior Period)
        ws[f"{c1}{row+2}"] = "Vs. Target"
        ws[f"{c1}{row+2}"].font = sub_label_font
        
        ws[f"{c2}{row+2}"] = target
        ws[f"{c2}{row+2}"].font = sub_val_font
        ws[f"{c2}{row+2}"].number_format = num_format
        ws[f"{c2}{row+2}"].alignment = Alignment(horizontal="right")
        
        ws[f"{c1}{row+3}"] = "Vs. Prior Month"
        ws[f"{c1}{row+3}"].font = sub_label_font
        
        ws[f"{c2}{row+3}"] = prior
        ws[f"{c2}{row+3}"].font = sub_val_font
        ws[f"{c2}{row+3}"].number_format = num_format
        ws[f"{c2}{row+3}"].alignment = Alignment(horizontal="right")
        
        # 4. Conditional Formatting (Dynamic highlighting against the target cell)
        target_ref = f"${c2}${row+2}"
        if good_direction == "less":
            op_good, op_bad = 'lessThan', 'greaterThanOrEqual'
        else:
            op_good, op_bad = 'greaterThanOrEqual', 'lessThan'
            
        ws.conditional_formatting.add(
            f"{c1}{row+1}:{c2}{row+1}",
            CellIsRule(operator=op_good, formula=[target_ref], fill=green_fill, font=green_font)
        )
        ws.conditional_formatting.add(
            f"{c1}{row+1}:{c2}{row+1}",
            CellIsRule(operator=op_bad, formula=[target_ref], fill=red_fill, font=red_font)
        )
        
        # 5. Outer Box Border
        thin = Side(style="thin", color=palette["border"])
        for r in range(row, row+4):
            for c in [c1, c2]:
                cell = ws[f"{c}{r}"]
                left = thin if c == c1 else None
                right = thin if c == c2 else None
                top = thin if r == row else None
                bottom = thin if r == row+3 else None
                cell.border = Border(left=left, right=right, top=top, bottom=bottom)

    # --- Render Section 1: Working Capital ---
    ws.merge_cells('B4:G4')
    ws['B4'] = "Working Capital Efficiency"
    ws['B4'].fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
    ws['B4'].font = Font(color="FFFFFF", bold=True, size=14)
    ws['B4'].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[4].height = 25
    
    render_kpi('B', 6, "DSO (Days Sales Out)", 31, 45, 41, good_direction="less", num_format="0")
    render_kpi('D', 6, "DPO (Days Payables)", 89, 90, 90, good_direction="greater", num_format="0")
    render_kpi('F', 6, "Non-Current AR %", 0.12, 0.03, 0.11, good_direction="less", num_format="0%")
    
    # --- Render Section 2: Sales ---
    ws.merge_cells('B12:G12')
    ws['B12'] = "Sales KPIs"
    ws['B12'].fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    ws['B12'].font = Font(color="FFFFFF", bold=True, size=14)
    ws['B12'].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[12].height = 25
    
    render_kpi('B', 14, "CAC (Acquisition Cost)", 26319, 15000, 17725, good_direction="less", num_format="$#,##0")
    render_kpi('D', 14, "Sales vs. Budget", 1.62, 1.00, 1.27, good_direction="greater", num_format="0%")
    render_kpi('F', 14, "Gross Margin", 0.20, 0.38, 0.26, good_direction="greater", num_format="0%")
    
    # Hide gridlines for clean dashboard look
    ws.sheet_view.showGridLines = False
