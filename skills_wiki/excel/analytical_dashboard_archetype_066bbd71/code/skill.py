from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup Dashboard Sheet
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    
    # Hide gridlines for a clean, application-like feel
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Banner
    ws_dash.merge_cells("A1:U3")
    banner = ws_dash["A1"]
    banner.value = title
    banner.font = Font(size=24, bold=True, color="FFFFFF")
    # In a full framework, this hex would pull from a theme dictionary (e.g., theme.primary_bg)
    banner.fill = PatternFill("solid", fgColor="203764") 
    banner.alignment = Alignment(horizontal="center", vertical="center")
    
    # 2. Setup Hidden Calculation Sheet (Simulating Pivot Caches)
    ws_calc = wb.create_sheet("Calc")
    ws_calc.sheet_state = "hidden"
    
    # Inject aggregated data for Chart 1: Profit by Market & Cookie
    cookies = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar"]
    ws_calc.append(["Market"] + cookies)
    data_t1 = [
        ["India", 62000, 4800, 21000, 25000, 18000],
        ["Philippines", 54000, 7000, 22000, 8000, 14000],
        ["United Kingdom", 46000, 5200, 11000, 14000, 19000],
        ["Malaysia", 46000, 5500, 17000, 20000, 10000],
        ["United States", 36000, 6300, 22000, 9000, 9000]
    ]
    for row in data_t1:
        ws_calc.append(row)
        
    # Inject aggregated data for Charts 2 & 3: Monthly Trends
    ws_calc.append([]) # Spacer row
    offset = ws_calc.max_row + 1
    ws_calc.append(["Month", "Units Sold", "Profit"])
    monthly_data = [
        ["Sep", 50000, 124000],
        ["Oct", 95000, 228000],
        ["Nov", 65000, 160000],
        ["Dec", 52000, 136000]
    ]
    for row in monthly_data:
        ws_calc.append(row)
        
    # 3. Create Charts on Dashboard
    # Chart 1: Stacked Column (Main KPI Breakdown)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1.style = 10 # Applies a built-in clean palette
    
    cats1 = Reference(ws_calc, min_col=1, min_row=2, max_row=6)
    data1 = Reference(ws_calc, min_col=2, min_row=1, max_col=6, max_row=6)
    c1.add_data(data1, titles_from_data=True)
    c1.set_categories(cats1)
    
    c1.width = 16
    c1.height = 12
    ws_dash.add_chart(c1, "B5") # Left panel anchor
    
    # Chart 2: Line Chart (Units Trend)
    c2 = LineChart()
    c2.title = "Units sold each month"
    c2.style = 13
    
    cats2 = Reference(ws_calc, min_col=1, min_row=offset+1, max_row=offset+4)
    data2 = Reference(ws_calc, min_col=2, min_row=offset, max_row=offset+4)
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats2)
    c2.legend = None # Remove legend to save space and reduce clutter
    
    c2.width = 12
    c2.height = 5.8
    ws_dash.add_chart(c2, "K5") # Top right anchor
    
    # Chart 3: Line Chart (Profit Trend)
    c3 = LineChart()
    c3.title = "Profit by month"
    c3.style = 13
    
    data3 = Reference(ws_calc, min_col=3, min_row=offset, max_row=offset+4)
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(cats2)
    c3.legend = None 
    
    c3.width = 12
    c3.height = 5.8
    ws_dash.add_chart(c3, "K15") # Bottom right anchor (aligned under C2)
    
    # 4. Setup Raw Data Sheet
    ws_data = wb.create_sheet("Data")
    headers = ["Date", "Market", "Product", "Units Sold", "Revenue", "Cost", "Profit"]
    ws_data.append(headers)
    
    sample_data = [
        ["2019-09-01", "India", "Chocolate Chip", 1725, 8625, 3450, 5175],
        ["2019-10-01", "United States", "Sugar", 1200, 4800, 1200, 3600],
        ["2019-11-01", "Philippines", "Snickerdoodle", 2200, 11000, 4000, 7000]
    ]
    for row in sample_data:
        ws_data.append(row)
        
    tab = Table(displayName="SalesData", ref=f"A1:G4")
    tab.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium9", 
        showFirstColumn=False,
        showLastColumn=False, 
        showRowStripes=True, 
        showColumnStripes=False
    )
    ws_data.add_table(tab)
