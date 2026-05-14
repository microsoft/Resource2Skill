def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference

    # Load theme (with fallback for standard properties)
    try:
        from skills_library.excel.components._helpers import get_theme
        theme_colors = get_theme(theme)
    except ImportError:
        theme_colors = {
            "primary": "4F81BD",
            "text_light": "FFFFFF"
        }

    # Create Dashboard Sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    # Hide gridlines for a clean software-like dashboard appearance
    ws.sheet_view.showGridLines = False

    # Title Banner (Spans A1 to O3)
    ws.merge_cells('A1:O3')
    banner_fill = PatternFill(
        start_color=theme_colors.get("primary", "4F81BD").replace("#", ""), 
        end_color=theme_colors.get("primary", "4F81BD").replace("#", ""), 
        fill_type="solid"
    )
    
    # Ensure all cells in merged range have the fill so it renders perfectly
    for row in ws['A1:O3']:
        for cell in row:
            cell.fill = banner_fill

    title_cell = ws['A1']
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=theme_colors.get("text_light", "FFFFFF").replace("#", ""))
    title_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # Data Sheet for Charts (Separating Data from Presentation)
    data_sheet_name = f"{sheet_name}_Data"
    if data_sheet_name in wb.sheetnames:
        data_ws = wb[data_sheet_name]
    else:
        data_ws = wb.create_sheet(data_sheet_name)
    data_ws.sheet_state = 'hidden'

    # --- Seed Aggregated Data ---
    
    # 1. Profit by Market & Product
    market_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62000, 23000, 21000, 25000],
        ["Philippines", 54000, 24000, 22000, 8000],
        ["United Kingdom", 46000, 26000, 11000, 14000],
        ["United States", 36000, 32000, 22000, 9000],
    ]
    for r_idx, row in enumerate(market_data, 1):
        for c_idx, val in enumerate(row, 1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # 2. Units Sold by Month
    units_data = [
        ["Month", "Units Sold"],
        ["Sep", 50000],
        ["Oct", 95000],
        ["Nov", 65000],
        ["Dec", 52000],
    ]
    for r_idx, row in enumerate(units_data, 10):
        for c_idx, val in enumerate(row, 1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # 3. Profit by Month
    profit_data = [
        ["Month", "Profit"],
        ["Sep", 124000],
        ["Oct", 228000],
        ["Nov", 160000],
        ["Dec", 136000],
    ]
    for r_idx, row in enumerate(profit_data, 20):
        for c_idx, val in enumerate(row, 1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # --- Generate & Position Charts ---

    # Chart 1: Stacked Column (Profit by Market & Cookie Type)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.style = 11

    data1 = Reference(data_ws, min_col=2, min_row=1, max_col=5, max_row=5)
    cats1 = Reference(data_ws, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    chart1.width = 18
    chart1.height = 10
    ws.add_chart(chart1, "B5") # Anchor main chart left

    # Chart 2: Line (Units Sold)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.style = 12
    data2 = Reference(data_ws, min_col=2, min_row=10, max_col=2, max_row=14)
    cats2 = Reference(data_ws, min_col=1, min_row=11, max_row=14)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.width = 14
    chart2.height = 7
    ws.add_chart(chart2, "I5") # Anchor secondary chart top-right

    # Chart 3: Line (Profit)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.style = 12
    data3 = Reference(data_ws, min_col=2, min_row=20, max_col=2, max_row=24)
    cats3 = Reference(data_ws, min_col=1, min_row=21, max_row=24)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    chart3.width = 14
    chart3.height = 7
    ws.add_chart(chart3, "I16") # Anchor tertiary chart bottom-right
