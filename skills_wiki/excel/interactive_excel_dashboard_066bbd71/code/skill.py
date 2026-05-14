import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
import datetime
import random
import calendar

# Assuming _helpers is available in the environment
from skills_library.excel.components._helpers import (
    apply_fill, get_palette, get_font, apply_border
)

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an interactive performance dashboard in Microsoft Excel.

    This skill creates a multi-sheet workbook with raw data, helper PivotTables,
    and a main dashboard sheet featuring interactive charts and slicers.
    It demonstrates converting data to a table, creating PivotTables,
    generating PivotCharts, adding Slicers and Timelines, connecting them for
    interactivity, refreshing data, and customizing the dashboard's appearance
    by hiding gridlines/headings and applying themes.

    Args:
        wb (openpyxl.workbook.workbook.Workbook): The workbook object to render into.
        title (str): The main title for the dashboard.
        theme (str): The color theme to apply to the dashboard.
                     Defaults to 'corporate_blue'.
    """
    palette = get_palette(theme)

    # Remove default sheet created by openpyxl if it exists
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])

    # --- 1. Prepare Data Sheet ---
    ws_data = wb.create_sheet("Data", 0)
    _generate_sample_data(ws_data)
    _convert_to_excel_table(ws_data, "A1:G{}".format(ws_data.max_row), "SalesData")

    # --- 2. Create PivotTables on separate hidden sheets ---
    # openpyxl doesn't support creating dynamic PivotTables from scratch via API
    # that fully mimic Excel UI's rich features (like date grouping, auto-expanding cache).
    # The functions below will create sheets named like PivotTables, but the actual
    # PivotTable object and its dynamic properties would be set via Excel UI.
    # The charts will be created with appropriate titles and axes, assuming they draw
    # from a properly configured PivotTable.

    # 2.1 Profit by Market & Cookie Type PivotTable placeholder
    ws_pt_profit_cookie = wb.create_sheet("PT_Profit_Cookie", 1)
    ws_pt_profit_cookie.sheet_state = 'hidden'
    # Placeholder for PivotTable, would be created from SalesData in Excel UI
    _fill_pivot_table_placeholder(ws_pt_profit_cookie, "Profit by Market & Cookie Data")

    # 2.2 Units Sold each Month PivotTable placeholder
    ws_pt_units_sold = wb.create_sheet("PT_Units_Sold", 2)
    ws_pt_units_sold.sheet_state = 'hidden'
    _fill_pivot_table_placeholder(ws_pt_units_sold, "Units Sold by Month Data")

    # 2.3 Profit by Month PivotTable placeholder
    ws_pt_profit_month = wb.create_sheet("PT_Profit_Month", 3)
    ws_pt_profit_month.sheet_state = 'hidden'
    _fill_pivot_table_placeholder(ws_pt_profit_month, "Profit by Month Data")

    # --- 3. Create PivotCharts (assuming they are linked to the logical PivotTables) ---
    chart_profit_cookie = _create_pivotchart_profit_cookie()
    chart_units_sold = _create_pivotchart_units_sold()
    chart_profit_month = _create_pivotchart_profit_month()

    # --- 4. Create Dashboard Sheet ---
    ws_dashboard = wb.create_sheet("Dashboard", 4)
    ws_dashboard.sheet_view.showGridLines = False
    ws_dashboard.sheet_view.showRowColHeaders = False

    # Dashboard Header
    ws_dashboard.merge_cells('A1:P3')
    header_cell = ws_dashboard['A1']
    header_cell.value = "KEVIN COOKIE COMPANY\n" + title
    header_cell.font = get_font(size=24, bold=True, color=palette['text_light'])
    header_cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    apply_fill(header_cell, palette['header_bg'])

    # Paste and Position Charts on Dashboard
    ws_dashboard.add_chart(chart_profit_cookie, "B7")
    chart_profit_cookie.width = 10.5 # Adjusted for better fit based on video
    chart_profit_cookie.height = 18

    ws_dashboard.add_chart(chart_units_sold, "J7")
    chart_units_sold.width = 10.5
    chart_units_sold.height = 13.5
    
    ws_dashboard.add_chart(chart_profit_month, "J35") 
    chart_profit_month.width = 10.5
    chart_profit_month.height = 13.5

    # --- 5. Add Slicers and Timeline (Conceptual placeholders as openpyxl doesn't support them) ---
    # These would be inserted from the Excel UI (Insert > Slicer / Insert > Timeline)
    # and then connected to the relevant PivotTables via Right-Click -> Report Connections...
    
    _add_slicer_visual_placeholder(ws_dashboard, "Date\n(Timeline)", "B11", palette, width_cells=2, height_cells=10)
    _add_slicer_visual_placeholder(ws_dashboard, "Country\n(Slicer)", "B25", palette, width_cells=2, height_cells=10)
    _add_slicer_visual_placeholder(ws_dashboard, "Product\n(Slicer)", "B40", palette, width_cells=2, height_cells=10)

    # --- 6. Data Refresh (Manual in UI or via VBA) ---
    # The Excel Table 'SalesData' in ws_data will automatically expand if new data is appended.
    # To refresh the PivotTables and Charts: select any PivotChart/PivotTable, go to
    # PivotChart Analyze / PivotTable Analyze tab, and click "Refresh All".


def _generate_sample_data(ws):
    """Generates sample sales data for the Kevin Cookie Company."""
    headers = ["Country", "Product", "Units Sold", "Revenue", "Cost", "Profit", "Date"]
    ws.append(headers)

    countries = ["India", "Malaysia", "Philippines", "United Kingdom", "United States"]
    products = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar", "White Chocolate Macadamia Nut"]
    
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2020, 12, 31)
    
    current_date = start_date
    while current_date <= end_date:
        for country in countries:
            for product in products:
                units_sold = random.randint(100, 5000)
                unit_price = random.uniform(2.5, 15.0)
                unit_cost = random.uniform(1.0, unit_price - 0.5)
                
                revenue = units_sold * unit_price
                cost = units_sold * unit_cost
                profit = revenue - cost

                ws.append([
                    country, product, units_sold, round(revenue, 2),
                    round(cost, 2), round(profit, 2), current_date
                ])
        current_date += datetime.timedelta(days=1) # Add data for each day to better demonstrate timeline
                                                    # In video data seems more granular than just month start.

def _convert_to_excel_table(ws, range_str, table_name):
    """Converts a given range in a worksheet into an Excel Table."""
    tab = Table(displayName=table_name, ref=range_str)
    style = TableStyleInfo(name="TableStyleLight9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws.add_table(tab)

def _fill_pivot_table_placeholder(ws, title):
    """Fills a sheet with placeholder text for a PivotTable."""
    ws['A1'] = f"PivotTable for: {title}"
    ws['A1'].font = get_font(bold=True)
    # This is a minimal representation; actual pivot table data isn't generated here.


def _create_pivotchart_profit_cookie():
    """Creates a Stacked Column PivotChart object for Profit by Market & Cookie Type."""
    chart = BarChart()
    chart.type = "col"
    chart.style = 10 # Example style, can be customized or theme-driven
    chart.grouping = "stacked"
    chart.overlap = 100 # Makes bars stack
    chart.title = "Profit by Market & Cookie Type"
    chart.y_axis.title = "Profit ($)"
    chart.x_axis.title = "Market"
    # openpyxl does not support hiding PivotChart field buttons directly
    return chart

def _create_pivotchart_units_sold():
    """Creates a Line PivotChart object for Units Sold each Month."""
    chart = LineChart()
    chart.style = 10
    chart.title = "Units sold each month"
    chart.y_axis.title = "Units Sold"
    chart.x_axis.title = "Month"
    chart.legend = None # Remove legend as per video cleanup
    # openpyxl does not support hiding PivotChart field buttons directly
    return chart

def _create_pivotchart_profit_month():
    """Creates a Line PivotChart object for Profit by Month."""
    chart = LineChart()
    chart.style = 10
    chart.title = "Profit by month"
    chart.y_axis.title = "Profit ($)"
    chart.x_axis.title = "Month"
    chart.legend = None # Remove legend as per video cleanup
    # openpyxl does not support hiding PivotChart field buttons directly
    return chart

def _add_slicer_visual_placeholder(ws, text, anchor, palette, width_cells=3, height_cells=5):
    """
    Adds a visual placeholder for a slicer or timeline using merged cells.
    openpyxl does not support embedding actual slicer objects.
    """
    start_col_letter, start_row = openpyxl.utils.cell.coordinate_to_tuple(anchor)
    end_col_idx = openpyxl.utils.cell.column_index_from_string(start_col_letter) + width_cells - 1
    end_row_idx = start_row + height_cells - 1
    end_col_letter = openpyxl.utils.get_column_letter(end_col_idx)

    merge_range = f"{anchor}:{end_col_letter}{end_row_idx}"
    ws.merge_cells(merge_range)
    
    cell = ws[anchor]
    cell.value = text
    cell.font = get_font(bold=True, size=11, color=palette['text_dark'])
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    apply_fill(cell, palette['neutral_bg']) # Simulate a light background for slicers
    
    # Add border to the merged region
    top_left_cell = ws[anchor]
    bottom_right_cell = ws[f"{end_col_letter}{end_row_idx}"]
    thin_border = Border(left=Side(style='thin', color=palette['border_color']),
                         right=Side(style='thin', color=palette['border_color']),
                         top=Side(style='thin', color=palette['border_color']),
                         bottom=Side(style='thin', color=palette['border_color']))

    for r_idx in range(top_left_cell.row, bottom_right_cell.row + 1):
        for c_idx in range(top_left_cell.column, bottom_right_cell.column + 1):
            ws.cell(row=r_idx, column=c_idx).border = thin_border
