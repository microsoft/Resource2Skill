from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a complete 3-sheet dashboard architecture (Dashboard, Calc Data, Raw Data)
    with styled charts aligned on a clean presentation canvas.
    """
    # 1. Fallback theme loading
    themes = {
        "corporate_blue": {"primary_bg": "003366", "primary_fg": "FFFFFF"},
        "emerald": {"primary_bg": "006644", "primary_fg": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Sheet Setup
    ws_raw = wb.active
    ws_raw.title = "Raw Data"
    ws_calc = wb.create_sheet("Calc Data")
    ws_dash = wb.create_sheet("Dashboard", 0)  # Move to front

    # 3. Build the Dashboard Canvas
    ws_dash.sheet_view.showGridLines = False
    
    # Title Banner
    ws_dash.merge_cells("A1:N3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["primary_fg"])
    title_cell.fill = PatternFill(start_color=palette["primary_bg"], fill_type="solid")
    title_cell.alignment = Alignment(vertical="center", horizontal="center")

    # 4. Populate Calc Data (Simulating PivotTable outputs)
    # Block 1: Profit by Market & Product (for Stacked Bar)
    ws_calc.append(["Market", "Chocolate Chip", "Sugar", "Oatmeal"])
    ws_calc.append(["India", 62349, 18560, 21028])
    ws_calc.append(["United Kingdom", 46530, 14620, 11497])
    ws_calc.append(["United States", 36657, 9938, 22260])
    
    # Block 2: Units Sold by Month (for Line Chart 1)
    ws_calc.append([])
    ws_calc.append(["Month", "Units Sold"])
    ws_calc.append(["Sep", 50601])
    ws_calc.append(["Oct", 95622])
    ws_calc.append(["Nov", 65481])
    ws_calc.append(["Dec", 52970])

    # Block 3: Profit by Month (for Line Chart 2)
    ws_calc.append([])
    ws_calc.append(["Month", "Profit"])
    ws_calc.append(["Sep", 124812])
    ws_calc.append(["Oct", 228275])
    ws_calc.append(["Nov", 160228])
    ws_calc.append(["Dec", 136337])

    # 5. Create & Align Charts on Dashboard
    # Chart A: Stacked Bar
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    
    data1 = Reference(ws_calc, min_col=2, max_col=4, min_row=1, max_row=4)
    cats1 = Reference(ws_calc, min_col=1, min_row=2, max_row=4)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    chart1.width = 16
    chart1.height = 14
    ws_dash.add_chart(chart1, "B5")

    # Chart B: Line Chart (Units)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.legend = None  # Remove legend for single-series
    
    data2 = Reference(ws_calc, min_col=2, min_row=7, max_row=11)
    cats2 = Reference(ws_calc, min_col=1, min_row=8, max_row=11)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.width = 13
    chart2.height = 7
    ws_dash.add_chart(chart2, "I5")

    # Chart C: Line Chart (Profit)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.legend = None
    
    data3 = Reference(ws_calc, min_col=2, min_row=14, max_row=18)
    cats3 = Reference(ws_calc, min_col=1, min_row=15, max_row=18)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    chart3.width = 13
    chart3.height = 7
    ws_dash.add_chart(chart3, "I12")

    # 6. Hide Calc Sheet (Best Practice)
    ws_calc.sheet_state = "hidden"

    # 7. Setup Raw Data Table
    headers = ["Date", "Market", "Product", "Units Sold", "Profit"]
    sample_data = [
        ["2020-09-01", "India", "Chocolate Chip", 1500, 4500],
        ["2020-10-01", "United Kingdom", "Sugar", 1200, 3600],
        ["2020-11-01", "United States", "Oatmeal", 1800, 5400]
    ]
    ws_raw.append(headers)
    for row in sample_data:
        ws_raw.append(row)
        
    table = Table(displayName="RawDataTab", ref=f"A1:E{len(sample_data)+1}")
    style = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    table.tableStyleInfo = style
    ws_raw.add_table(table)
    
    for col in ["A", "B", "C", "D", "E"]:
        ws_raw.column_dimensions[col].width = 15
