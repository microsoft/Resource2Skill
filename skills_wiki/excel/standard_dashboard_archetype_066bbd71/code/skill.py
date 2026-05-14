from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a complete dashboard workbook featuring a gridless presentation layer 
    and separated data layer with multiple aligned charts.
    """
    # 1. Theme Setup
    theme_colors = {
        "corporate_blue": {"primary": "4F81BD", "text": "FFFFFF"},
        "emerald": {"primary": "00B050", "text": "FFFFFF"},
        "midnight": {"primary": "1F4E78", "text": "FFFFFF"}
    }
    colors = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    # 2. Data Sheet Setup (Hidden from final presentation)
    ws_data = wb.active
    ws_data.title = "Data"
    
    # Dataset 1: Profit by Market & Product (For Stacked Column)
    cat_data = [
        ["Market", "Fortune Cookie", "Sugar", "Oatmeal Raisin"],
        ["India", 62000, 23000, 21000],
        ["United States", 36000, 32000, 11000],
        ["United Kingdom", 46000, 26000, 14000],
        ["Philippines", 54000, 24000, 22000],
    ]
    for row in cat_data:
        ws_data.append(row)
        
    ws_data.append([]) # Spacer row
    trend_start_row = ws_data.max_row + 1
    
    # Dataset 2: Units Sold Trend (For Line Chart)
    trend_data = [
        ["Month", "Units Sold"],
        ["Sep", 50000],
        ["Oct", 95000],
        ["Nov", 65000],
        ["Dec", 52000],
    ]
    for row in trend_data:
        ws_data.append(row)
        
    # 3. Dashboard Sheet Setup (Presentation Canvas)
    ws_dash = wb.create_sheet(title="Dashboard")
    ws_dash.sheet_view.showGridLines = False
    
    # Top Dashboard Banner
    ws_dash.merge_cells("A1:P3")
    banner_cell = ws_dash["A1"]
    banner_cell.value = title
    banner_cell.font = Font(size=24, bold=True, color=colors["text"])
    banner_cell.fill = PatternFill(start_color=colors["primary"], end_color=colors["primary"], fill_type="solid")
    banner_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 4. Profit by Market Stacked Column Chart
    chart_col = BarChart()
    chart_col.type = "col"
    chart_col.style = 10
    chart_col.grouping = "stacked"
    chart_col.overlap = 100
    chart_col.title = "Profit by Market & Cookie Type"
    
    # Map data from the Data sheet
    data_ref = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    cats_ref = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart_col.add_data(data_ref, titles_from_data=True)
    chart_col.set_categories(cats_ref)
    chart_col.width = 16
    chart_col.height = 8
    
    # Anchor top-left corner
    ws_dash.add_chart(chart_col, "B5")
    
    # 5. Units Sold Line Chart
    chart_line = LineChart()
    chart_line.title = "Units Sold Each Month"
    chart_line.style = 13
    
    trend_end_row = trend_start_row + len(trend_data) - 1
    data_ref_line = Reference(ws_data, min_col=2, min_row=trend_start_row, max_row=trend_end_row)
    cats_ref_line = Reference(ws_data, min_col=1, min_row=trend_start_row+1, max_row=trend_end_row)
    chart_line.add_data(data_ref_line, titles_from_data=True)
    chart_line.set_categories(cats_ref_line)
    chart_line.width = 14
    chart_line.height = 8
    
    # Anchor alongside the column chart
    ws_dash.add_chart(chart_line, "J5")
    
    # Force Excel to open straight to the Dashboard
    wb.active = ws_dash
