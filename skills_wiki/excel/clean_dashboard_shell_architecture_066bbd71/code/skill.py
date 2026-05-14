from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a clean, gridline-free dashboard sheet with a unified header and aligned charts.
    Data is stored in a hidden backend sheet.
    """
    # 1. Theme Setup (Fallback to corporate blue if external helper missing)
    theme_colors = {
        "corporate_blue": {"header_bg": "2F5597", "title_fg": "FFFFFF"},
        "executive_dark": {"header_bg": "262626", "title_fg": "E7E6E6"},
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    # 2. Setup Backend Data Sheet
    data_ws_name = f"{sheet_name}_Data"
    if data_ws_name in wb.sheetnames:
        data_ws = wb[data_ws_name]
    else:
        data_ws = wb.create_sheet(data_ws_name)
    data_ws.sheet_state = 'hidden'  # Hide the backend data

    # Mock Data: Categorical Breakdown (A1:D5)
    cat_data = [
        ["Market", "Choc Chip", "Fortune Cookie", "Sugar"],
        ["India", 62000, 4800, 18000],
        ["Philippines", 54000, 7000, 8000],
        ["United Kingdom", 46000, 5200, 14000],
        ["United States", 36000, 6300, 9000]
    ]
    for row in cat_data:
        data_ws.append(row)
        
    # Mock Data: Temporal Trends (F1:H5)
    time_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337]
    ]
    for r_idx, row in enumerate(time_data, start=1):
        for c_idx, val in enumerate(row, start=6):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # 3. Setup Frontend Dashboard Sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name, 0)
        
    # Clean UI: Hide Gridlines
    ws.sheet_view.showGridLines = False

    # 4. Create Themed Dashboard Header
    ws.merge_cells("A1:P3")
    header_cell = ws["A1"]
    header_cell.value = title
    header_cell.font = Font(name="Calibri", size=24, bold=True, color=palette["title_fg"])
    header_cell.fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 5. Build and Align Charts
    
    # Chart 1: Profit by Market & Cookie (Stacked Column)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.style = 2  # Standard clean Excel style
    chart1.title = "Profit by Market & Cookie Type"
    chart1.width = 16
    chart1.height = 11.5
    
    cat_data_ref = Reference(data_ws, min_col=2, min_row=1, max_col=4, max_row=5)
    cat_labels_ref = Reference(data_ws, min_col=1, min_row=2, max_row=5)
    chart1.add_data(cat_data_ref, titles_from_data=True)
    chart1.set_categories(cat_labels_ref)
    ws.add_chart(chart1, "B5")

    # Chart 2: Units Sold (Line)
    chart2 = LineChart()
    chart2.style = 2
    chart2.title = "Units sold each month"
    chart2.width = 14
    chart2.height = 5.5
    chart2.legend = None  # Clean look for single series
    
    units_data_ref = Reference(data_ws, min_col=7, min_row=1, max_col=7, max_row=5)
    time_labels_ref = Reference(data_ws, min_col=6, min_row=2, max_row=5)
    chart2.add_data(units_data_ref, titles_from_data=True)
    chart2.set_categories(time_labels_ref)
    ws.add_chart(chart2, "J5")

    # Chart 3: Profit by Month (Line)
    chart3 = LineChart()
    chart3.style = 2
    chart3.title = "Profit by month"
    chart3.width = 14
    chart3.height = 5.5
    chart3.legend = None
    
    profit_data_ref = Reference(data_ws, min_col=8, min_row=1, max_col=8, max_row=5)
    chart3.add_data(profit_data_ref, titles_from_data=True)
    chart3.set_categories(time_labels_ref)
    ws.add_chart(chart3, "J11")
