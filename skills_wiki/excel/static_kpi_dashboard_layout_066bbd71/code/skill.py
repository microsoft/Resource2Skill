from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", data: dict = None, **kwargs) -> None:
    """
    Builds a static dashboard with a clean presentation sheet and hidden calculation data.
    """
    # 1. Setup sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False
    
    ws_calc = wb.create_sheet("CalcData")
    ws_calc.sheet_state = 'hidden'

    # Mocking standard theme helper approach
    theme_colors = {
        "corporate_blue": {"bg": "1F4E78", "fg": "FFFFFF", "accent1": "4472C4"},
        "exec_dark": {"bg": "202020", "fg": "E2E2E2", "accent1": "0078D7"}
    }.get(theme, {"bg": "1F4E78", "fg": "FFFFFF", "accent1": "4472C4"})

    # 2. Dashboard Header Banner
    ws_dash.merge_cells("A1:R3")
    banner = ws_dash["A1"]
    banner.value = title
    banner.fill = PatternFill(start_color=theme_colors["bg"], end_color=theme_colors["bg"], fill_type="solid")
    banner.font = Font(color=theme_colors["fg"], size=24, bold=True)
    banner.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Default Data (Fallback)
    if not data:
        data = {
            "market_product": {
                "categories": ["India", "Philippines", "UK", "USA"],
                "series": {
                    "Choc Chip": [62349, 54618, 46530, 36657],
                    "Fortune Cookie": [4872, 7026, 5220, 6369],
                    "Oatmeal Raisin": [21028, 22005, 11497, 22260],
                    "Snickerdoodle": [25085, 8313, 14620, 9938]
                }
            },
            "monthly_units": {"months": ["Sep", "Oct", "Nov", "Dec"], "values": [50601, 95622, 65481, 52970]},
            "monthly_profit": {"months": ["Sep", "Oct", "Nov", "Dec"], "values": [124812, 228275, 160228, 136337]}
        }

    # 4. Write data to hidden calculation sheet
    # Chart 1 Data: Stacked Bar
    ws_calc["A1"] = "Market"
    col = 2
    for s_name in data["market_product"]["series"].keys():
        ws_calc.cell(row=1, column=col, value=s_name)
        col += 1
        
    for r_idx, cat in enumerate(data["market_product"]["categories"], start=2):
        ws_calc.cell(row=r_idx, column=1, value=cat)
        c_idx = 2
        for s_name, s_vals in data["market_product"]["series"].items():
            ws_calc.cell(row=r_idx, column=c_idx, value=s_vals[r_idx-2])
            c_idx += 1
            
    # Chart 2 Data: Monthly Units
    mu_start_row = len(data["market_product"]["categories"]) + 3
    ws_calc.cell(row=mu_start_row, column=1, value="Month")
    ws_calc.cell(row=mu_start_row, column=2, value="Units")
    for r_idx, (m, v) in enumerate(zip(data["monthly_units"]["months"], data["monthly_units"]["values"]), start=mu_start_row+1):
        ws_calc.cell(row=r_idx, column=1, value=m)
        ws_calc.cell(row=r_idx, column=2, value=v)
        
    # Chart 3 Data: Monthly Profit
    mp_start_row = mu_start_row + len(data["monthly_units"]["months"]) + 2
    ws_calc.cell(row=mp_start_row, column=1, value="Month")
    ws_calc.cell(row=mp_start_row, column=2, value="Profit")
    for r_idx, (m, v) in enumerate(zip(data["monthly_profit"]["months"], data["monthly_profit"]["values"]), start=mp_start_row+1):
        ws_calc.cell(row=r_idx, column=1, value=m)
        ws_calc.cell(row=r_idx, column=2, value=v)

    # 5. Construct Charts
    # Stacked Column Chart
    bc = BarChart()
    bc.type = "col"
    bc.grouping = "stacked"
    bc.overlap = 100
    bc.title = "Profit by Market & Cookie Type"
    bc.width = 16
    bc.height = 14
    
    cats_bc = Reference(ws_calc, min_col=1, min_row=2, max_row=1+len(data["market_product"]["categories"]))
    for c_idx in range(2, 2+len(data["market_product"]["series"])):
        s_data = Reference(ws_calc, min_col=c_idx, min_row=1, max_row=1+len(data["market_product"]["categories"]))
        bc.add_data(s_data, titles_from_data=True)
    bc.set_categories(cats_bc)
    ws_dash.add_chart(bc, "B5")
    
    # Line Chart 1 (Units)
    lc1 = LineChart()
    lc1.title = "Units sold each month"
    lc1.width = 14
    lc1.height = 6.5
    lc1.legend = None # Remove legend for single-series clarity
    cats_lc1 = Reference(ws_calc, min_col=1, min_row=mu_start_row+1, max_row=mu_start_row+len(data["monthly_units"]["months"]))
    data_lc1 = Reference(ws_calc, min_col=2, min_row=mu_start_row, max_row=mu_start_row+len(data["monthly_units"]["months"]))
    lc1.add_data(data_lc1, titles_from_data=True)
    lc1.set_categories(cats_lc1)
    ws_dash.add_chart(lc1, "K5")
    
    # Line Chart 2 (Profit)
    lc2 = LineChart()
    lc2.title = "Profit by month"
    lc2.width = 14
    lc2.height = 6.5
    lc2.legend = None
    cats_lc2 = Reference(ws_calc, min_col=1, min_row=mp_start_row+1, max_row=mp_start_row+len(data["monthly_profit"]["months"]))
    data_lc2 = Reference(ws_calc, min_col=2, min_row=mp_start_row, max_row=mp_start_row+len(data["monthly_profit"]["months"]))
    lc2.add_data(data_lc2, titles_from_data=True)
    lc2.set_categories(cats_lc2)
    ws_dash.add_chart(lc2, "K13")
