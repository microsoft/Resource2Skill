from openpyxl.styles import Font, PatternFill, Alignment, numbers
from openpyxl.chart import LineChart, Reference, Series
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, title: str = "Scenario Model", theme: str = "corporate_blue", months: int = 24, **kwargs) -> None:
    # 1. Theme Configuration
    themes = {
        "corporate_blue": {
            "header_bg": "1F4E78", "header_fg": "FFFFFF", 
            "input_bg": "F2F2F2", "input_fg": "0000FF"
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    header_fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    header_font = Font(color=palette["header_fg"], bold=True)
    input_fill = PatternFill(start_color=palette["input_bg"], end_color=palette["input_bg"], fill_type="solid")
    input_font = Font(color=palette["input_fg"], bold=True)
    bold_font = Font(bold=True)

    # 2. Worksheet Setup
    if "Sheet" in wb.sheetnames:
        ws_assumptions = wb["Sheet"]
        ws_assumptions.title = "Assumptions"
    else:
        ws_assumptions = wb.create_sheet("Assumptions")
    ws_model = wb.create_sheet("Model")

    # --- 3. ASSUMPTIONS SHEET ---
    ws_assumptions.column_dimensions['A'].width = 25
    ws_assumptions.column_dimensions['B'].width = 15

    inputs = [
        ("Accessories", None, None),
        ("Average Price", 45, numbers.FORMAT_CURRENCY_USD_SIMPLE),
        ("Starting Volume", 2000, numbers.FORMAT_NUMBER_COMMA_SEPARATED1),
        ("MoM Growth", 0.06, numbers.FORMAT_PERCENTAGE_00),
        ("Gross Margin", 0.35, numbers.FORMAT_PERCENTAGE_00),
        ("", None, None),
        ("Devices", None, None),
        ("Average Price", 280, numbers.FORMAT_CURRENCY_USD_SIMPLE),
        ("Starting Volume", 500, numbers.FORMAT_NUMBER_COMMA_SEPARATED1),
        ("MoM Growth", 0.04, numbers.FORMAT_PERCENTAGE_00),
        ("Gross Margin", 0.22, numbers.FORMAT_PERCENTAGE_00),
        ("", None, None),
        ("General Assumptions", None, None),
        ("Marketing Spend (% of Rev)", 0.12, numbers.FORMAT_PERCENTAGE_00),
    ]

    row_idx = 2
    for label, val, num_fmt in inputs:
        ws_assumptions.cell(row=row_idx, column=1, value=label)
        if val is not None:
            c = ws_assumptions.cell(row=row_idx, column=2, value=val)
            c.number_format = num_fmt
            c.fill = input_fill
            c.font = input_font
        elif label != "":
            # Section Header formatting
            ws_assumptions.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)
            c = ws_assumptions.cell(row=row_idx, column=1)
            c.fill = header_fill
            c.font = header_font
            c.alignment = Alignment(horizontal="center")
        row_idx += 1

    # --- 4. MODEL SHEET ---
    ws_model.column_dimensions['A'].width = 15
    ws_model.column_dimensions['B'].width = 20

    # Build Projection Headers
    for col in range(3, 3 + months):
        col_letter = get_column_letter(col)
        c = ws_model.cell(row=2, column=col, value=f"Month {col-2}")
        c.fill = header_fill
        c.font = header_font
        c.alignment = Alignment(horizontal="center")
        ws_model.column_dimensions[col_letter].width = 15

    # Define Row Labels
    labels = [
        (3, "Accessories", True),
        (4, "Price", False),
        (5, "Volume", False),
        (6, "Revenue", False),
        (7, "Gross Profit", False),
        (8, "Devices", True),
        (9, "Price", False),
        (10, "Volume", False),
        (11, "Revenue", False),
        (12, "Gross Profit", False),
        (13, "Consolidated", True),
        (14, "Total Revenue", False),
        (15, "Total Gross Profit", False),
        (16, "Blended Margin", False),
        (17, "Marketing Spend", False),
        (18, "Contribution Margin", True)
    ]
    
    # Write Row Labels (Indent standard items into column B)
    for r, lbl, is_header in labels:
        target_col = 1 if is_header else 2
        c = ws_model.cell(row=r, column=target_col, value=lbl)
        if is_header:
            c.font = bold_font

    # Populate Projection Formulas
    for col in range(3, 3 + months):
        col_letter = get_column_letter(col)
        prev_col_letter = get_column_letter(col - 1) if col > 3 else None

        # Accessories Block
        ws_model[f"{col_letter}4"].value = "='Assumptions'!$B$3"
        ws_model[f"{col_letter}4"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        
        if col == 3:
            ws_model[f"{col_letter}5"].value = "='Assumptions'!$B$4"
        else:
            ws_model[f"{col_letter}5"].value = f"={prev_col_letter}5*(1+'Assumptions'!$B$5)"
        ws_model[f"{col_letter}5"].number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
        
        ws_model[f"{col_letter}6"].value = f"={col_letter}4*{col_letter}5"
        ws_model[f"{col_letter}6"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        
        ws_model[f"{col_letter}7"].value = f"={col_letter}6*'Assumptions'!$B$6"
        ws_model[f"{col_letter}7"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE

        # Devices Block
        ws_model[f"{col_letter}9"].value = "='Assumptions'!$B$9"
        ws_model[f"{col_letter}9"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        
        if col == 3:
            ws_model[f"{col_letter}10"].value = "='Assumptions'!$B$10"
        else:
            ws_model[f"{col_letter}10"].value = f"={prev_col_letter}10*(1+'Assumptions'!$B$11)"
        ws_model[f"{col_letter}10"].number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
        
        ws_model[f"{col_letter}11"].value = f"={col_letter}9*{col_letter}10"
        ws_model[f"{col_letter}11"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        
        ws_model[f"{col_letter}12"].value = f"={col_letter}11*'Assumptions'!$B$12"
        ws_model[f"{col_letter}12"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE

        # Consolidated Block
        ws_model[f"{col_letter}14"].value = f"={col_letter}6+{col_letter}11"
        ws_model[f"{col_letter}14"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        ws_model[f"{col_letter}14"].font = bold_font
        
        ws_model[f"{col_letter}15"].value = f"={col_letter}7+{col_letter}12"
        ws_model[f"{col_letter}15"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        
        ws_model[f"{col_letter}16"].value = f"=IF({col_letter}14>0, {col_letter}15/{col_letter}14, 0)"
        ws_model[f"{col_letter}16"].number_format = numbers.FORMAT_PERCENTAGE_00
        
        ws_model[f"{col_letter}17"].value = f"={col_letter}14*'Assumptions'!$B$14"
        ws_model[f"{col_letter}17"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        
        ws_model[f"{col_letter}18"].value = f"={col_letter}15-{col_letter}17"
        ws_model[f"{col_letter}18"].number_format = numbers.FORMAT_CURRENCY_USD_SIMPLE
        ws_model[f"{col_letter}18"].font = bold_font

    # --- 5. VISUALIZATION ---
    chart = LineChart()
    chart.title = "Monthly Revenue & Contribution Margin"
    chart.style = 13
    chart.y_axis.title = "USD"
    chart.x_axis.title = "Month"
    chart.width = 28
    chart.height = 14

    # Chart X-Axis Labels
    data_categories = Reference(ws_model, min_col=3, min_row=2, max_col=2 + months)

    # Adding Data Series
    s1_data = Reference(ws_model, min_col=3, min_row=6, max_col=2 + months)
    s1 = Series(s1_data, title="Accessories Revenue")
    chart.series.append(s1)

    s2_data = Reference(ws_model, min_col=3, min_row=11, max_col=2 + months)
    s2 = Series(s2_data, title="Devices Revenue")
    chart.series.append(s2)

    s3_data = Reference(ws_model, min_col=3, min_row=18, max_col=2 + months)
    s3 = Series(s3_data, title="Contribution Margin")
    chart.series.append(s3)

    chart.set_categories(data_categories)
    ws_model.add_chart(chart, "B20")
