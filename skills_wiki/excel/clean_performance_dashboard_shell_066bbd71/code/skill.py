from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a clean, grid-less dashboard sheet containing a stacked bar chart
    and two trend line charts based on the provided or default aggregate data.
    """
    # 1. Theme Configuration
    theme_colors = {
        "corporate_blue": {"primary": "003366", "accent": "4F81BD", "text": "000000"},
        "modern_green": {"primary": "2E7D32", "accent": "66BB6A", "text": "212121"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    ws = wb.create_sheet(sheet_name)
    
    # Disable gridlines for a clean dashboard canvas
    ws.sheet_view.showGridLines = False
    
    # 2. Add Dashboard Header
    ws['A1'] = title
    ws['A1'].font = Font(size=24, bold=True, color=palette["primary"])
    ws.merge_cells('A1:O2')
    ws['A1'].alignment = Alignment(vertical='center')
    
    # 3. Inject Hidden Aggregated Data (Out of view in Columns AA+)
    # Market Data for Stacked Bar Chart
    market_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"],
        ["India", 60000, 5000, 20000, 25000],
        ["Philippines", 50000, 6000, 15000, 8000],
        ["United States", 35000, 6000, 20000, 10000],
        ["United Kingdom", 45000, 5000, 10000, 14000]
    ]
    
    # Trend Data for Line Charts
    trend_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50000, 120000],
        ["Oct", 95000, 220000],
        ["Nov", 65000, 160000],
        ["Dec", 52000, 130000]
    ]
    
    # Write Market Data starting at AA1 (Col 27)
    for r_idx, row in enumerate(market_data, start=1):
        for c_idx, val in enumerate(row, start=27):
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    # Write Trend Data starting at AG1 (Col 33)
    for r_idx, row in enumerate(trend_data, start=1):
        for c_idx, val in enumerate(row, start=33):
            ws.cell(row=r_idx, column=c_idx, value=val)

    # 4. Create Stacked Bar Chart (Profit by Market & Cookie Type)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.y_axis.title = "Profit"
    chart1.legend.position = 'b'
    chart1.style = 10
    
    # Remove major gridlines for a cleaner look
    chart1.y_axis.majorGridlines = None
    
    c1_data = Reference(ws, min_col=28, min_row=1, max_col=31, max_row=len(market_data))
    c1_cats = Reference(ws, min_col=27, min_row=2, max_row=len(market_data))
    chart1.add_data(c1_data, titles_from_data=True)
    chart1.set_categories(c1_cats)
    
    # 5. Create Line Chart 1 (Units Sold by Month)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.style = 13
    chart2.y_axis.majorGridlines = None
    chart2.legend = None # Remove legend for single series
    
    c2_data = Reference(ws, min_col=34, min_row=1, max_row=len(trend_data))
    c2_cats = Reference(ws, min_col=33, min_row=2, max_row=len(trend_data))
    chart2.add_data(c2_data, titles_from_data=True)
    chart2.set_categories(c2_cats)
    
    # 6. Create Line Chart 2 (Profit by Month)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.style = 13
    chart3.y_axis.majorGridlines = None
    chart3.legend = None
    
    c3_data = Reference(ws, min_col=35, min_row=1, max_row=len(trend_data))
    c3_cats = Reference(ws, min_col=33, min_row=2, max_row=len(trend_data))
    chart3.add_data(c3_data, titles_from_data=True)
    chart3.set_categories(c3_cats)
    
    # 7. Position Charts on the Dashboard
    chart1.width = 16
    chart1.height = 12
    ws.add_chart(chart1, "B4")
    
    chart2.width = 12
    chart2.height = 6
    ws.add_chart(chart2, "K4")
    
    chart3.width = 12
    chart3.height = 6
    ws.add_chart(chart3, "K12")
