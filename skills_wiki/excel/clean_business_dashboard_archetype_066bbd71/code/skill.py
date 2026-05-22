from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a two-sheet workbook: a Data backend and a cleanly formatted Dashboard frontend.
    """
    # Standard theme fallback dictionary
    colors = {
        "corporate_blue": {"bg": "1F4E78", "fg": "FFFFFF"},
        "executive_dark": {"bg": "262626", "fg": "F2F2F2"},
        "midnight_solid": {"bg": "000000", "fg": "FFFFFF"}
    }.get(theme, {"bg": "1F4E78", "fg": "FFFFFF"})

    ws_data = wb.active
    ws_data.title = "Data"

    # 1. Populate Backend Data
    # Stacked Column Data (Profit by Market & Cookie)
    data_market = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62000, 4800, 21000, 25000],
        ["United States", 36000, 6000, 22000, 9000],
        ["United Kingdom", 46000, 5000, 11000, 14000],
        ["Philippines", 54000, 7000, 22000, 8000],
        ["Malaysia", 46000, 5000, 17000, 20000]
    ]
    for r in data_market:
        ws_data.append(r)
        
    tab1 = Table(displayName="MarketData", ref=f"A1:E6")
    tab1.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    ws_data.add_table(tab1)

    # Line Chart 1 Data (Units Sold)
    ws_data.append([]) # spacer row 7
    data_units = [
        ["Month", "Units Sold"],
        ["Sep", 50000],
        ["Oct", 95000],
        ["Nov", 65000],
        ["Dec", 52000]
    ]
    for r in data_units:
        ws_data.append(r)
        
    tab2 = Table(displayName="UnitsData", ref=f"A8:B12")
    tab2.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    ws_data.add_table(tab2)

    # Line Chart 2 Data (Profit)
    ws_data.append([]) # spacer row 13
    data_profit = [
        ["Month", "Profit"],
        ["Sep", 124000],
        ["Oct", 228000],
        ["Nov", 160000],
        ["Dec", 136000]
    ]
    for r in data_profit:
        ws_data.append(r)
        
    tab3 = Table(displayName="ProfitData", ref=f"A14:B18")
    tab3.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    ws_data.add_table(tab3)

    # 2. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False

    # Title Banner
    ws_dash.merge_cells("A1:Q3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.fill = PatternFill(start_color=colors["bg"], end_color=colors["bg"], fill_type="solid")
    title_cell.font = Font(color=colors["fg"], size=24, bold=True)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Add Stacked Column Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Product Type"
    chart1.style = 10 
    
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=6)
    data1 = Reference(ws_data, min_col=2, min_row=1, max_col=5, max_row=6)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    
    # Size and position to act as the primary visual on the left
    chart1.height = 14
    chart1.width = 16
    ws_dash.add_chart(chart1, "C5")

    # 4. Add First Line Chart (Units)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.style = 13
    
    cats2 = Reference(ws_data, min_col=1, min_row=9, max_row=12)
    data2 = Reference(ws_data, min_col=2, min_row=8, max_col=2, max_row=12)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.legend = None # Remove legend to maximize the plot area
    
    # Size and position to stack neatly on the right
    chart2.height = 7
    chart2.width = 14
    ws_dash.add_chart(chart2, "K5")

    # 5. Add Second Line Chart (Profit)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.style = 13
    
    cats3 = Reference(ws_data, min_col=1, min_row=15, max_row=18)
    data3 = Reference(ws_data, min_col=2, min_row=14, max_col=2, max_row=18)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    chart3.legend = None
    
    chart3.height = 7
    chart3.width = 14
    ws_dash.add_chart(chart3, "K18")
