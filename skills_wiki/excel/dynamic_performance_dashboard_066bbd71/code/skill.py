import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.axis import ChartLines

# Custom theme helper (simplified for demonstration based on common patterns)
class Theme:
    def __init__(self, theme_name="corporate_blue"):
        self.palette = {
            "corporate_blue": {
                "header_bg": "FF2E4057",
                "header_fg": "FFFFFFFF",
                "text_color": "FF000000",
                "accent_1": "FF4472C4",
                "accent_2": "FFED7D31",
                "accent_3": "FF70AD47",
                "accent_4": "FFFFC000",
                "accent_5": "FF5B9BD5",
                "accent_6": "FF8B8B8B",
            },
            # Add more themes if needed
        }.get(theme_name, self.palette["corporate_blue"])

    def get_color(self, key):
        return self.palette.get(key, "FF000000") # Default to black if key not found

    def get_font(self, size=12, bold=False, color="text_color"):
        return Font(name='Calibri', size=size, bold=bold, color=self.get_color(color))

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # Load theme colors
    current_theme = Theme(theme)

    # --- 1. Data Sheet ---
    data_ws = wb.active
    data_ws.title = "Data"

    # Sample Data
    headers = ["Country", "Product", "Units Sold", "Revenue", "Cost", "Profit", "Date"]
    data_ws.append(headers)
    sample_data = [
        ["India", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, datetime(2019, 11, 1)],
        ["India", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, datetime(2019, 12, 1)],
        ["India", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, datetime(2019, 9, 1)],
        ["India", "Fortune Cookie", 345, 345.00, 69.00, 276.00, datetime(2019, 10, 1)],
        ["India", "Oatmeal Raisin", 21028, 21028.00, 8411.20, 12616.80, datetime(2019, 11, 1)],
        ["India", "Snickerdoodle", 25085, 25085.00, 10034.00, 15051.00, datetime(2019, 12, 1)],
        ["Malaysia", "Chocolate Chip", 2299, 11495.00, 4598.00, 6897.00, datetime(2019, 11, 1)],
        ["Malaysia", "Fortune Cookie", 1611, 1611.00, 322.20, 1288.80, datetime(2019, 11, 1)],
        ["Malaysia", "Oatmeal Raisin", 22005, 22005.00, 8802.00, 13203.00, datetime(2019, 10, 1)],
        ["Malaysia", "Snickerdoodle", 8313, 8313.00, 3325.20, 4987.80, datetime(2019, 9, 1)],
        ["Philippines", "Chocolate Chip", 1404, 7020.00, 2808.00, 4212.00, datetime(2019, 10, 1)],
        ["Philippines", "Fortune Cookie", 2567, 2567.00, 513.40, 2053.60, datetime(2019, 9, 1)],
        ["Philippines", "Oatmeal Raisin", 17536, 17536.00, 7014.40, 10521.60, datetime(2019, 12, 1)],
        ["Philippines", "Snickerdoodle", 14947, 14947.00, 5978.80, 8968.20, datetime(2019, 11, 1)],
        ["United Kingdom", "Chocolate Chip", 2470, 12350.00, 4940.00, 7410.00, datetime(2019, 9, 1)],
        ["United Kingdom", "Fortune Cookie", 1010, 1010.00, 202.00, 808.00, datetime(2019, 10, 1)],
        ["United Kingdom", "Oatmeal Raisin", 20452, 20452.00, 8180.80, 12271.20, datetime(2019, 11, 1)],
        ["United Kingdom", "Snickerdoodle", 20555, 20555.00, 8222.00, 12333.00, datetime(2019, 12, 1)],
        ["United States", "Chocolate Chip", 1743, 8715.00, 3486.00, 5229.00, datetime(2019, 10, 1)],
        ["United States", "Fortune Cookie", 4872, 4872.00, 974.40, 3897.60, datetime(2019, 12, 1)],
        ["United States", "Oatmeal Raisin", 17536, 17536.00, 7014.40, 10521.60, datetime(2019, 9, 1)],
        ["United States", "Snickerdoodle", 78510, 78510.00, 31404.00, 47106.00, datetime(2019, 10, 1)],
        ["United States", "Sugar", 72772, 72772.00, 29108.80, 43663.20, datetime(2019, 11, 1)],
        # Add new data for 2020 as shown in the refresh section
        ["India", "Chocolate Chip", 292, 1460.00, 584.00, 876.00, datetime(2020, 2, 1)],
        ["India", "Chocolate Chip", 2518, 12590.00, 5036.00, 7554.00, datetime(2020, 6, 1)],
        ["India", "Chocolate Chip", 1817, 9085.00, 3634.00, 5451.00, datetime(2020, 12, 1)],
        ["United States", "White Chocolate Macadamia Nut", 2438, 14628.00, 6704.50, 7923.50, datetime(2020, 1, 1)],
        ["United States", "Sugar", 914, 5484.00, 2513.50, 2970.50, datetime(2020, 7, 1)],
    ]
    for row_data in sample_data:
        data_ws.append(row_data)

    # Convert data to Excel Table
    max_row = data_ws.max_row
    max_col = data_ws.max_column
    table_range = f"A1:{get_column_letter(max_col)}{max_row}"
    tab = Table(displayName="Table3", ref=table_range)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight10", showFirstColumn=False,
                                       showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    data_ws.add_table(tab)

    # Apply number formats to data columns
    for col_idx in range(3, 7): # Columns D to G for Revenue, Cost, Profit
        col_letter = get_column_letter(col_idx)
        for row_idx in range(2, max_row + 1):
            cell = data_ws[f"{col_letter}{row_idx}"]
            cell.number_format = "$#,##0.00"
    
    # Format Units Sold as Number with comma
    for row_idx in range(2, max_row + 1):
        data_ws[f"C{row_idx}"].number_format = "#,##0"


    # --- 2. Create PivotTables and Charts ---

    # Helper function to create PivotTable and Chart
    def create_pivot_and_chart(chart_type, pivot_name, sheet_name, row_fields, col_fields, value_field, chart_title, value_format, wb, data_table_name="Table3"):
        pivot_ws = wb.create_sheet(title=sheet_name)
        pivot_cache = wb.pivotCaches.create(source=data_table_name, sourceRef=data_ws.title, location=pivot_ws.title)
        pivot_table = pivot_cache.addPivotTable(name=pivot_name, locRef="A3")

        # Set row fields
        for field in row_fields:
            if isinstance(field, dict) and 'grouping' in field:
                pivot_table.rowFields.append(pivot_table.get_field(field['name']))
                pivot_ws.pivotTables[0].group_rows(field['name'], group_by=field['grouping'])
            else:
                pivot_table.rowFields.append(pivot_table.get_field(field))

        # Set column fields
        for field in col_fields:
            pivot_table.colFields.append(pivot_table.get_field(field))

        # Set value field
        value_pivot_field = pivot_table.get_field(value_field)
        value_pivot_field.showDropDown = False # Hide drop down button on chart
        value_pivot_field.numFmtId = 164 # Custom number format ID (e.g., currency without decimals)
        pivot_table.dataFields.append(value_pivot_field)

        # Apply value format
        for row_idx in range(2, pivot_ws.max_row + 1):
            for col_idx in range(2, pivot_ws.max_column + 1):
                cell = pivot_ws.cell(row=row_idx, column=col_idx)
                if isinstance(cell.value, (int, float)):
                    cell.number_format = value_format

        chart = None
        if chart_type == "StackedColumn":
            chart = BarChart()
            chart.type = "col"
            chart.style = 10 # Example style
            chart.grouping = "stacked"
            chart.overlap = 100
        elif chart_type == "Line":
            chart = LineChart()
            chart.style = 10
            chart.y_axis.crossAx = 500
            chart.x_axis.crossAx = 100
        
        if chart:
            chart.title = chart_title
            data_ref = Reference(pivot_ws, min_col=pivot_table.colPivot.firstDataCol, min_row=pivot_table.rowPivot.firstDataRow, 
                                 max_col=pivot_table.colPivot.lastDataCol, max_row=pivot_table.rowPivot.lastDataRow)
            chart.add_data(data_ref, titles_from_data=True)
            
            # Categories are the row labels in A column for pivot table
            categories_ref = Reference(pivot_ws, min_col=1, min_row=pivot_table.rowPivot.firstDataRow, max_row=pivot_table.rowPivot.lastDataRow)
            chart.set_categories(categories_ref)

            chart.x_axis.title = ""
            chart.y_axis.title = value_field
            chart.legend.position = 'r'
            chart.height = 7.5
            chart.width = 12
            pivot_ws.add_chart(chart, "I1")

            # Remove PivotChart Field Buttons (visual clean-up)
            # This is primarily a UI setting and not directly exposed in openpyxl for dynamic removal.
            # We'll rely on the user to disable them manually in Excel via right-click > Hide All Field Buttons on Chart
            
            return pivot_ws, chart
        return pivot_ws, None

    # PivotTable 1 & Chart: Profit by Market & Cookie Type
    profit_by_market_cookie_ws, profit_by_market_cookie_chart = create_pivot_and_chart(
        "StackedColumn", "PivotTable1", "Profit by Market & Cookie",
        row_fields=["Country"], col_fields=["Product"], value_field="Profit",
        chart_title="Profit by Market & Cookie Type", value_format="$#,##0", wb=wb
    )
    # The sorting in the video (largest to smallest) is a manual PivotTable UI operation in openpyxl.
    # It would involve applying auto-filter and sorting by grand total.
    
    # PivotTable 2 & Chart: Units Sold Each Month
    units_sold_ws, units_sold_chart = create_pivot_and_chart(
        "Line", "PivotTable2", "Units sold each month",
        row_fields=[{"name": "Date", "grouping": "months"}], col_fields=[], value_field="Units Sold",
        chart_title="Units sold each month", value_format="#,##0", wb=wb
    )

    # PivotTable 3 & Chart: Profit by Month
    profit_by_month_ws, profit_by_month_chart = create_pivot_and_chart(
        "Line", "PivotTable3", "Profit by month",
        row_fields=[{"name": "Date", "grouping": "months"}], col_fields=[], value_field="Profit",
        chart_title="Profit by month", value_format="$#,##0", wb=wb
    )

    # --- 3. Dashboard Sheet ---
    dashboard_ws = wb.create_sheet(title="Dashboard", index=0)

    # Header section
    dashboard_ws.merge_cells('A1:P6')
    header_cell = dashboard_ws['A1']
    header_cell.value = "KEVIN COOKIE COMPANY\nPerformance Dashboard"
    header_cell.font = current_theme.get_font(size=36, bold=True, color="header_fg")
    header_cell.alignment = Alignment(horizontal='center', vertical='center')
    header_cell.fill = PatternFill(start_color=current_theme.get_color("header_bg"), end_color=current_theme.get_color("header_bg"), fill_type="solid")

    # Position Charts on Dashboard
    # Use copy_worksheet and add_chart for proper embedding
    if profit_by_market_cookie_chart:
        dashboard_ws.add_chart(profit_by_market_cookie_chart, "D8")
        profit_by_market_cookie_chart.height = 10.5 # Adjust dimensions
        profit_by_market_cookie_chart.width = 15

    if units_sold_chart:
        dashboard_ws.add_chart(units_sold_chart, "K8")
        units_sold_chart.height = 4.5
        units_sold_chart.width = 15
        
    if profit_by_month_chart:
        dashboard_ws.add_chart(profit_by_month_chart, "K20")
        profit_by_month_chart.height = 4.5
        profit_by_month_chart.width = 15

    # Visual clean-up for Dashboard sheet
    dashboard_ws.sheet_view.showGridLines = False
    dashboard_ws.sheet_view.showRowColHeaders = False

    # --- 4. Hide PivotTable Sheets ---
    profit_by_market_cookie_ws.sheet_state = 'hidden'
    units_sold_ws.sheet_state = 'hidden'
    profit_by_month_ws.sheet_state = 'hidden'
    
    # --- Manual Steps for Slicers/Timelines and Connections (Not directly programmable with openpyxl) ---
    # To create interactive slicers and timelines as shown in the video:
    # 1. Select any PivotChart on the Dashboard sheet.
    # 2. Go to 'PivotChart Analyze' tab in the Excel Ribbon.
    # 3. Click 'Insert Timeline' and select the 'Date' field. Position it on the dashboard.
    # 4. Click 'Insert Slicer' and select 'Country'. Position it on the dashboard.
    # 5. Click 'Insert Slicer' and select 'Product'. Position it on the dashboard.
    # 6. For EACH slicer/timeline, right-click on it and select 'Report Connections...'.
    # 7. In the 'Report Connections' dialog, check all three PivotTables (PivotTable1, PivotTable2, PivotTable3)
    #    to ensure the slicers filter all charts simultaneously.
    # 8. Hide the headers of the slicers (right-click > Slicer Settings > uncheck Display Header) and adjust their size.

    # Applying workbook-level themes (like Page Layout > Themes in Excel) is not directly supported by openpyxl.
    # The chart styles and cell formatting uses theme colors defined above.
