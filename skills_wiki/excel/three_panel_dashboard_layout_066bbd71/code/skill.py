from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a 3-panel static dashboard. Data is sequestered in a hidden sheet.
    Accepts kwargs for data; falls back to realistic defaults if omitted.
    """
    # 1. Provide default data if not supplied via kwargs
    bar_data = kwargs.get("bar_data", [
        ["Region", "Chocolate Chip", "Oatmeal Raisin", "Sugar Cookie"],
        ["North America", 150000, 80000, 60000],
        ["Europe", 120000, 50000, 45000],
        ["Asia", 90000, 40000, 70000],
        ["South America", 40000, 25000, 30000]
    ])
    
    line1_data = kwargs.get("line1_data", [
        ["Month", "Units Sold"],
        ["Jan", 15000], ["Feb", 18000], ["Mar", 22000],
        ["Apr", 21000], ["May", 25000], ["Jun", 28000]
    ])
    
    line2_data = kwargs.get("line2_data", [
        ["Month", "Profit"],
        ["Jan", 45000], ["Feb", 52000], ["Mar", 61000],
        ["Apr", 59000], ["May", 70000], ["Jun", 82000]
    ])

    # 2. Setup the visible Dashboard sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    ws.sheet_view.showGridLines = False

    # Mocking basic theme resolution
    header_bg = "203764" if theme == "corporate_blue" else "333333"
    header_fg = "FFFFFF"

    # Format Banner
    ws.merge_cells("A1:P2")
    banner_cell = ws["A1"]
    banner_cell.value = title
    banner_cell.font = Font(size=24, bold=True, color=header_fg)
    banner_cell.fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")
    banner_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Setup the hidden Data sheet
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = 'hidden'

    # Write Data and track ranges
    bar_start_row = 1
    for r in bar_data:
        data_ws.append(r)
    bar_end_row = data_ws.max_row
    bar_col_count = len(bar_data[0])

    line1_start_row = bar_end_row + 2
    for r in line1_data:
        data_ws.append(r)
    line1_end_row = data_ws.max_row
    line1_col_count = len(line1_data[0])

    line2_start_row = line1_end_row + 2
    for r in line2_data:
        data_ws.append(r)
    line2_end_row = data_ws.max_row
    line2_col_count = len(line2_data[0])

    # 4. Construct Left Panel (Main Stacked Bar Chart)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.width = 16
    chart1.height = 14.5
    
    data1_ref = Reference(data_ws, min_col=2, min_row=bar_start_row, max_col=bar_col_count, max_row=bar_end_row)
    cats1_ref = Reference(data_ws, min_col=1, min_row=bar_start_row+1, max_row=bar_end_row)
    chart1.add_data(data1_ref, titles_from_data=True)
    chart1.set_categories(cats1_ref)
    ws.add_chart(chart1, "B4")

    # 5. Construct Top Right Panel (Line Chart 1)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.width = 14
    chart2.height = 7
    chart2.legend = None # Clean look for single series
    
    data2_ref = Reference(data_ws, min_col=2, min_row=line1_start_row, max_col=line1_col_count, max_row=line1_end_row)
    cats2_ref = Reference(data_ws, min_col=1, min_row=line1_start_row+1, max_row=line1_end_row)
    chart2.add_data(data2_ref, titles_from_data=True)
    chart2.set_categories(cats2_ref)
    ws.add_chart(chart2, "J4")

    # 6. Construct Bottom Right Panel (Line Chart 2)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.width = 14
    chart3.height = 7
    chart3.legend = None
    
    data3_ref = Reference(data_ws, min_col=2, min_row=line2_start_row, max_col=line2_col_count, max_row=line2_end_row)
    cats3_ref = Reference(data_ws, min_col=1, min_row=line2_start_row+1, max_row=line2_end_row)
    chart3.add_data(data3_ref, titles_from_data=True)
    chart3.set_categories(cats3_ref)
    ws.add_chart(chart3, "J12")
