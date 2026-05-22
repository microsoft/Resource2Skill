from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a multi-sheet dashboard archetype separating Presentation, Calculation, and Data layers.
    """
    # 1. Sheet Setup
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False  # Clean presentation layer
    
    ws_calc = wb.create_sheet("Calculations")
    ws_calc.sheet_state = 'hidden'  # Hide intermediate summaries from the end user
    
    ws_data = wb.create_sheet("Data")
    
    # Theme setup
    palette = kwargs.get("palette", {})
    header_bg = palette.get("primary", "4F81BD")
    header_fg = palette.get("text_on_primary", "FFFFFF")
    
    # 2. Dashboard Header
    ws_dash['A1'] = title
    ws_dash['A1'].font = Font(size=24, bold=True, color=header_fg)
    ws_dash['A1'].fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")
    ws_dash.merge_cells('A1:T2')
    ws_dash['A1'].alignment = Alignment(horizontal="center", vertical="center")
    
    # 3. Populate Calculation Sheet (Simulating Pivot Table aggregations)
    calc_data_bar = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62000, 23000, 21000, 25000],
        ["United Kingdom", 46000, 24000, 22000, 8000],
        ["United States", 36000, 32000, 20000, 9000]
    ]
    for row in calc_data_bar:
        ws_calc.append(row)
        
    ws_calc.append([])
    start_row_line = ws_calc.max_row + 1
    
    calc_data_line = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50000, 124000],
        ["Oct", 95000, 228000],
        ["Nov", 65000, 160000],
        ["Dec", 52000, 136000]
    ]
    for row in calc_data_line:
        ws_calc.append(row)
        
    # 4. Create and Position Charts
    
    # Main Chart: Stacked Column for categorical breakdown
    chart_bar = BarChart()
    chart_bar.type = "col"
    chart_bar.grouping = "stacked"
    chart_bar.overlap = 100
    chart_bar.title = "Profit by Market & Product Type"
    chart_bar.width = 16
    chart_bar.height = 12
    
    data_ref_bar = Reference(ws_calc, min_col=2, max_col=5, min_row=1, max_row=4)
    cats_ref_bar = Reference(ws_calc, min_col=1, min_row=2, max_row=4)
    chart_bar.add_data(data_ref_bar, titles_from_data=True)
    chart_bar.set_categories(cats_ref_bar)
    ws_dash.add_chart(chart_bar, "B4")
    
    # Sub Chart 1: Line Chart for unit volume trend
    chart_line_units = LineChart()
    chart_line_units.title = "Units sold each month"
    chart_line_units.width = 14
    chart_line_units.height = 6.5
    
    data_ref_units = Reference(ws_calc, min_col=2, min_row=start_row_line, max_row=start_row_line+4)
    cats_ref_line = Reference(ws_calc, min_col=1, min_row=start_row_line+1, max_row=start_row_line+4)
    chart_line_units.add_data(data_ref_units, titles_from_data=True)
    chart_line_units.set_categories(cats_ref_line)
    ws_dash.add_chart(chart_line_units, "K4")
    
    # Sub Chart 2: Line Chart for profit trend
    chart_line_profit = LineChart()
    chart_line_profit.title = "Profit by month"
    chart_line_profit.width = 14
    chart_line_profit.height = 6.5
    
    data_ref_profit = Reference(ws_calc, min_col=3, min_row=start_row_line, max_row=start_row_line+4)
    chart_line_profit.add_data(data_ref_profit, titles_from_data=True)
    chart_line_profit.set_categories(cats_ref_line)
    ws_dash.add_chart(chart_line_profit, "K14")
    
    # 5. Populate Raw Data Sheet
    ws_data.append(["Date", "Market", "Product", "Units Sold", "Profit"])
    raw_data = [
        ["2019-09-01", "India", "Chocolate Chip", 1725, 5175],
        ["2019-09-02", "United Kingdom", "Oatmeal Raisin", 1400, 4200],
        ["2019-09-03", "United States", "Fortune Cookie", 800, 1600],
        ["2019-10-01", "India", "Snickerdoodle", 2200, 6600],
    ]
    for r in raw_data:
        ws_data.append(r)
        
    tab = Table(displayName="RawData", ref=f"A1:E{len(raw_data)+1}")
    tab.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, 
        showRowStripes=True, showColumnStripes=False
    )
    ws_data.add_table(tab)
