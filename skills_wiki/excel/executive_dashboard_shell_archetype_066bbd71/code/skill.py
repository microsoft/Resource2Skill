from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo

def render_workbook(wb: Workbook, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme Setup (Fallback mapping for common palettes)
    palettes = {
        "corporate_blue": {"primary": "2F5597", "bg_light": "F2F2F2", "text_light": "FFFFFF"},
        "midnight": {"primary": "203764", "bg_light": "E7E6E6", "text_light": "FFFFFF"},
        "forest": {"primary": "385723", "bg_light": "E2EFDA", "text_light": "FFFFFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # Remove default sheet
    for sheet in wb.sheetnames:
        del wb[sheet]
        
    # 2. Create Sheet Architecture
    ws_dash = wb.create_sheet("Dashboard")
    ws_data = wb.create_sheet("Raw Data")
    ws_calc = wb.create_sheet("ChartData")
    ws_calc.sheet_state = 'hidden'

    # 3. Populate Hidden ChartData (Simulating PivotTable Aggregations)
    # Chart 1 Data: Profit by Market & Product
    calc_data_1 = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62349, 23621, 21028],
        ["United States", 36657, 32910, 11731],
        ["United Kingdom", 46530, 26731, 11497],
        ["Philippines", 54618, 24567, 22005]
    ]
    for row in calc_data_1:
        ws_calc.append(row)
        
    # Chart 2 & 3 Data: Units & Profit by Month
    ws_calc.cell(row=1, column=6, value="Month")
    ws_calc.cell(row=1, column=7, value="Units Sold")
    ws_calc.cell(row=1, column=8, value="Profit")
    
    trend_data = [
        ["Jan", 40000, 120000], ["Feb", 45000, 130000], ["Mar", 60000, 150000],
        ["Apr", 55000, 140000], ["May", 70000, 170000], ["Jun", 75000, 180000],
        ["Jul", 80000, 200000], ["Aug", 90000, 220000], ["Sep", 50601, 124812],
        ["Oct", 95622, 228275], ["Nov", 65481, 160228], ["Dec", 52970, 136337]
    ]
    for i, row in enumerate(trend_data, start=2):
        ws_calc.cell(row=i, column=6, value=row[0])
        ws_calc.cell(row=i, column=7, value=row[1])
        ws_calc.cell(row=i, column=8, value=row[2])

    # Format numeric cells for cleaner chart axes
    for r in range(2, 6):
        for c in range(2, 5):
            ws_calc.cell(row=r, column=c).number_format = '"$"#,##0'
    for r in range(2, 14):
        ws_calc.cell(row=r, column=7).number_format = '#,##0'
        ws_calc.cell(row=r, column=8).number_format = '"$"#,##0'

    # 4. Dashboard Visual Formatting
    ws_dash.sheet_view.showGridLines = False
    
    # Render App Header
    ws_dash.merge_cells("A1:R3")
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color=palette["text_light"])
    header_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    header_cell.alignment = Alignment(vertical="center", indent=1)

    # Render Left Control Sidebar (Reserved for eventual Excel Slicers)
    sidebar_fill = PatternFill(start_color=palette["bg_light"], end_color=palette["bg_light"], fill_type="solid")
    for row in range(4, 30):
        for col in range(1, 4):
            ws_dash.cell(row=row, column=col).fill = sidebar_fill
            
    ctrl_header = ws_dash["A4"]
    ctrl_header.value = "Filters & Controls"
    ctrl_header.font = Font(bold=True, size=12, color=palette["primary"])
    ctrl_header.alignment = Alignment(indent=1)
    
    # 5. Dashboard Charts Generation
    # Stacked Column Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Product Type"
    chart1.add_data(Reference(ws_calc, min_col=2, min_row=1, max_row=5, max_col=4), titles_from_data=True)
    chart1.set_categories(Reference(ws_calc, min_col=1, min_row=2, max_row=5))
    chart1.width = 15
    chart1.height = 11
    ws_dash.add_chart(chart1, "E5")
    
    # Trend Line Chart (Units)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.add_data(Reference(ws_calc, min_col=7, min_row=1, max_row=13), titles_from_data=True)
    chart2.set_categories(Reference(ws_calc, min_col=6, min_row=2, max_row=13))
    chart2.width = 13
    chart2.height = 7.5
    ws_dash.add_chart(chart2, "M5")

    # Trend Line Chart (Profit)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.add_data(Reference(ws_calc, min_col=8, min_row=1, max_row=13), titles_from_data=True)
    chart3.set_categories(Reference(ws_calc, min_col=6, min_row=2, max_row=13))
    chart3.width = 13
    chart3.height = 7.5
    ws_dash.add_chart(chart3, "M15")

    # 6. Raw Data Table Construction
    headers = ["Date", "Market", "Product", "Units Sold", "Profit"]
    ws_data.append(headers)
    for i in range(15):
        ws_data.append([f"2020-01-{i+1:02d}", "India", "Chocolate Chip", 150 + i*10, 500 + i*50])
        
    tab = Table(displayName="RawData", ref=f"A1:E16")
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_data.add_table(tab)
    
    # Refine Column Widths
    for col in ["A", "B", "C"]:
        ws_dash.column_dimensions[col].width = 12
    ws_dash.column_dimensions["D"].width = 3 # Spacer
