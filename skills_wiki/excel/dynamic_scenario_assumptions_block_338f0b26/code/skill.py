def render(ws, anchor: str, *, assumptions: list[str] = None, scenarios: dict[str, list[float]] = None, formats: list[str] = None, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import coordinate_from_string, column_index_from_string, get_column_letter

    # Default realistic financial modeling data if none provided
    if assumptions is None:
        assumptions = ["Order Growth Rate", "Average Order Value", "Cost per Order"]
    if scenarios is None:
        scenarios = {
            "Base Case": [1.00, 39.95, 6.50],
            "Upside": [1.50, 44.95, 6.00],
            "Downside": [0.50, 34.95, 7.00]
        }
    if formats is None:
        formats = ["0%", "$0.00", "$0.00"]

    # Visual Standard Styles
    bold_font = Font(bold=True)
    blue_font = Font(color="0000FF") # Modeling standard: Blue = Hardcoded Input
    input_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    scen_header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    thin_border = Border(top=Side(style='thin'), bottom=Side(style='thin'), left=Side(style='thin'), right=Side(style='thin'))

    anchor_coord = coordinate_from_string(anchor)
    col = column_index_from_string(anchor_coord[0])
    row = anchor_coord[1]

    # 1. Scenario Selector & Data Validation
    ws.cell(row=row, column=col, value="Active Scenario").font = bold_font
    sel_cell = ws.cell(row=row, column=col + 1, value=1)
    sel_cell.font = blue_font
    sel_cell.fill = input_fill
    sel_cell.border = thin_border
    sel_cell.alignment = Alignment(horizontal="center")
    sel_ref = f"${get_column_letter(col+1)}${row}"

    num_scen = len(scenarios)
    dv = DataValidation(type="list", formula1='"' + ",".join(str(i+1) for i in range(num_scen)) + '"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(sel_cell)

    # 2. Layout Spacing Calculations
    live_start = row + 2
    block_size = len(assumptions) + 2
    scen_starts = [live_start + block_size * (i + 1) for i in range(num_scen)]

    # 3. Live Case Block (Calculated via CHOOSE)
    live_header = ws.cell(row=live_start, column=col, value="Live Case")
    live_header.font = bold_font
    live_header.fill = header_fill

    for i, assumption in enumerate(assumptions):
        r = live_start + 1 + i
        ws.cell(row=r, column=col, value=assumption)
        
        # Build =CHOOSE() referencing matching rows in the scenario blocks
        refs = [f"{get_column_letter(col+1)}{scen_starts[s_idx] + 1 + i}" for s_idx in range(num_scen)]
        formula = f"=CHOOSE({sel_ref}, {', '.join(refs)})"
        
        f_cell = ws.cell(row=r, column=col + 1, value=formula)
        f_cell.font = bold_font
        if i < len(formats):
            f_cell.number_format = formats[i]

    # 4. Scenario Blocks (Hardcoded Inputs)
    for s_idx, (scen_name, values) in enumerate(scenarios.items()):
        s_start = scen_starts[s_idx]
        s_header = ws.cell(row=s_start, column=col, value=f"{scen_name} (Scenario {s_idx+1})")
        s_header.font = bold_font
        s_header.fill = scen_header_fill

        for v_idx, val in enumerate(values):
            r = s_start + 1 + v_idx
            ws.cell(row=r, column=col, value=assumptions[v_idx])
            v_cell = ws.cell(row=r, column=col + 1, value=val)
            v_cell.font = blue_font # Indicate it's safe to type over
            if v_idx < len(formats):
                v_cell.number_format = formats[v_idx]
