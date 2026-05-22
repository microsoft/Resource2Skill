from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import PatternFill, Font, Alignment

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    palette = kwargs.get("palette", {})
    header_bg = palette.get("primary", "1F4E78").replace("#", "")
    header_fg = palette.get("text_on_primary", "FFFFFF").replace("#", "")
    
    # 1. Dashboard Sheet Setup
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False
    
    # Header Banner
    ws_dash.merge_cells("A1:R4")
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color=header_fg)
    header_cell.fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 2. Hidden Data Sheet Setup
    ws_data = wb.create_sheet("Data")
    ws_data.sheet_state = "hidden"
    
    # Table 1: Stacked Bar Data
    data1 = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62000, 23000, 21000],
        ["Philippines", 54000, 24000, 22000],
        ["United Kingdom", 46000, 26000, 11000],
        ["United States", 36000, 32000, 9000]
    ]
    for r_idx, row in enumerate(data1, start=1):
        for c_idx, val in enumerate(row, start=1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)
            
    # Table 2: Line Chart Data (Units)
    data2 = [
        ["Month", "Units Sold"],
        ["Sep", 50600],
        ["Oct", 95600],
        ["Nov", 65400],
        ["Dec", 52900]
    ]
    for r_idx, row in enumerate(data2, start=10):
        for c_idx, val in enumerate(row, start=1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)
            
    # Table 3: Line Chart Data (Profit)
    data3 = [
        ["Month", "Profit"],
        ["Sep", 124000],
        ["Oct", 228000],
        ["Nov", 160000],
        ["Dec", 136000]
    ]
    for r_idx, row in enumerate(data3, start=20):
        for c_idx, val in enumerate(row, start=1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)
            
    # 3. Create Charts on Dashboard
    # Chart 1: Stacked Column (Main KPIs)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.legend.position = "r"
    chart1.width = 14
    chart1.height = 10
    
    data_ref1 = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    cats_ref1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data_ref1, titles_from_data=True)
    chart1.set_categories(cats_ref1)
    ws_dash.add_chart(chart1, "B6")
    
    # Chart 2: Line (Units Sold Trend)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.legend = None
    chart2.width = 12
    chart2.height = 6
    
    data_ref2 = Reference(ws_data, min_col=2, min_row=10, max_col=2, max_row=14)
    cats_ref2 = Reference(ws_data, min_col=1, min_row=11, max_row=14)
    chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(cats_ref2)
    ws_dash.add_chart(chart2, "J6")
    
    # Chart 3: Line (Profit Trend)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.legend = None
    chart3.width = 12
    chart3.height = 6
    
    data_ref3 = Reference(ws_data, min_col=2, min_row=20, max_col=2, max_row=24)
    cats_ref3 = Reference(ws_data, min_col=1, min_row=21, max_row=24)
    chart3.add_data(data_ref3, titles_from_data=True)
    chart3.set_categories(cats_ref3)
    ws_dash.add_chart(chart3, "J17")
