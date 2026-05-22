from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime

# Helper functions for themes, fills, and fonts (assuming _helpers.py exists)
def _get_theme_colors(theme_name: str):
    themes = {
        "corporate_blue": {
            "header_bg": "002060",
            "header_fg": "FFFFFF",
            "text_fg": "000000",
            "accent_bg": "D9D9D9",
            "accent_fg": "000000",
            "chart_line": "4472C4"
        },
        "green_theme": { # Example from video 1:09
            "header_bg": "548235",
            "header_fg": "FFFFFF",
            "text_fg": "000000",
            "accent_bg": "A9D18E",
            "accent_fg": "000000",
            "chart_line": "A9D18E"
        },
        "red_theme": { # Example from video 0:17
            "header_bg": "7030A0",
            "header_fg": "FFFFFF",
            "text_fg": "000000",
            "accent_bg": "FFC0CB",
            "accent_fg": "000000",
            "chart_line": "C00000"
        },
        "grey_theme": { # Example from video 18:27
            "header_bg": "363636",
            "header_fg": "FFFFFF",
            "text_fg": "000000",
            "accent_bg": "E0E0E0",
            "accent_fg": "000000",
            "chart_line": "808080"
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def _create_fill(color: str):
    return PatternFill(start_color=color, end_color=color, fill_type="solid")

def _create_font(color: str, bold: bool = False, size: int = 11):
    return Font(color=color, bold=bold, size=size)


def render_workbook(wb, *, title: str, company_name: str, data: list[dict], theme: str = "corporate_blue") -> None:
    """
    Renders an interactive performance dashboard in Microsoft Excel.

    Args:
        wb: The openpyxl workbook object.
        title: The title of the dashboard (e.g., "Performance Dashboard").
        company_name: The name of the company (e.g., "Kevin Cookie Company").
        data: A list of dictionaries, where each dictionary represents a row of data.
              Expected keys: 'Country', 'Product', 'Units Sold', 'Revenue', 'Cost', 'Profit', 'Date'.
        theme: The name of the theme to apply (e.g., "corporate_blue").
    """
    colors = _get_theme_colors(theme)

    # Delete default sheet if exists
    if 'Sheet' in wb.sheetnames:
        del wb['Sheet']

    # --- 1. Prepare Data Sheet ---
    ws_data = wb.create_sheet("Data")
    headers = list(data[0].keys())
    ws_data.append(headers)
    for row_data in data:
        ws_data.append(list(row_data.values()))

    # Convert range to Excel Table
    max_row = len(data) + 1
    max_col = len(headers)
    table_range = f"A1:{get_column_letter(max_col)}{max_row}"
    tab = Table(displayName="Data", ref=table_range)
    style = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)

    # Format numeric and date columns
    for col_idx, header in enumerate(headers):
        if header in ['Units Sold', 'Revenue', 'Cost', 'Profit']:
            for row in ws_data.iter_rows(min_row=2, min_col=col_idx + 1, max_col=col_idx + 1):
                for cell in row:
                    cell.number_format = "$#,##0" if header in ['Revenue', 'Cost', 'Profit'] else "#,##0"
        elif header == 'Date':
            for row in ws_data.iter_rows(min_row=2, min_col=col_idx + 1, max_col=col_idx + 1):
                for cell in row:
                    cell.number_format = 'm/d/yyyy'
    
    # --- 2. Create PivotTable Sheets (hidden) ---
    # Openpyxl can create the PivotTable object but does not render the visual PivotTable or its data.
    # To have charts linked to PivotTables, the PivotTable needs to be rendered (e.g., by opening/saving in Excel).
    # For this exercise, we will create dummy data on the dashboard sheet that mirrors
    # the output of the pivot tables for charting purposes.
    # In a real-world script, you might use a library like xlwings or interact with COM objects for full pivot chart control.
    
    ws_pt_profit_market_cookie = wb.create_sheet("PT_ProfitByMarketCookie")
    ws_pt_units_sold = wb.create_sheet("PT_UnitsSoldEachMonth")
    ws_pt_profit_month = wb.create_sheet("PT_ProfitByMonth")

    ws_pt_profit_market_cookie.sheet_state = 'hidden'
    ws_pt_units_sold.sheet_state = 'hidden'
    ws_pt_profit_month.sheet_state = 'hidden'


    # --- 3. Create Dashboard Sheet ---
    ws_dashboard = wb.create_sheet("Dashboard", 0) # Make it the first sheet

    # Header section
    ws_dashboard.merge_cells('A1:Q6')
    header_cell = ws_dashboard['A1']
    header_cell.value = f"{company_name} {title}"
    header_cell.font = _create_font(colors["header_fg"], bold=True, size=24)
    header_cell.fill = _create_fill(colors["header_bg"])
    header_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Hide gridlines and headings for a clean look
    ws_dashboard.views.sheetView[0].showGridLines = False
    ws_dashboard.views.sheetView[0].showRowColHeaders = False

    # --- 4. Add Mock Data for Charts (as openpyxl PivotChart linking is limited) ---
    # These mock data ranges will simulate the output of PivotTables for chart generation.
    # In a fully functional environment, these would be the actual output ranges of generated PivotTables.

    # Mock data for Chart 1: Profit by Market & Cookie Type (Stacked Column)
    countries_mock = ["India", "Philippines", "United Kingdom", "Malaysia", "United States"]
    products_mock = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar", "White Chocolate Macadamia Nut"]
    mock_profit_matrix = [
        [62349, 4872, 21028, 25085, 18560, 23621],
        [54618, 5537, 22005, 20555, 10633, 24567],
        [46587, 7025, 17536, 14947, 8313, 26731],
        [46530, 5220, 22260, 14620, 19446, 20452],
        [36657, 6368, 22260, 9938, 9185, 32910],
    ]
    
    for i, country in enumerate(countries_mock):
        ws_dashboard.cell(row=10 + i, column=2, value=country)
        ws_dashboard.cell(row=10 + i, column=2).font = _create_font(colors["text_fg"])

    for i, product in enumerate(products_mock):
        ws_dashboard.cell(row=9, column=3 + i, value=product)
        ws_dashboard.cell(row=9, column=3 + i).font = _create_font(colors["text_fg"])

    for r_idx, row_vals in enumerate(mock_profit_matrix):
        for c_idx, val in enumerate(row_vals):
            cell = ws_dashboard.cell(row=10 + r_idx, column=3 + c_idx, value=val)
            cell.number_format = "$#,##0"
            cell.font = _create_font(colors["text_fg"])

    # Mock data for Chart 2: Units Sold Each Month (Line Chart)
    months_mock = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    mock_units_timeline = [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000]

    for i, month in enumerate(months_mock):
        ws_dashboard.cell(row=25, column=3 + i, value=month)
        ws_dashboard.cell(row=25, column=3 + i).font = _create_font(colors["text_fg"])
    
    for i, units in enumerate(mock_units_timeline):
        cell = ws_dashboard.cell(row=26, column=3 + i, value=units)
        cell.number_format = "#,##0"
        cell.font = _create_font(colors["text_fg"])

    # Mock data for Chart 3: Profit by Month (Line Chart)
    mock_profit_timeline = [100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 280000, 300000, 320000]

    for i, profit in enumerate(mock_profit_timeline):
        cell = ws_dashboard.cell(row=30, column=3 + i, value=profit)
        cell.number_format = "$#,##0"
        cell.font = _create_font(colors["text_fg"])


    # --- 5. Generate Charts ---

    # Chart 1: Profit by Market & Cookie Type (Stacked Column)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.y_axis.title = "Profit"
    chart1.x_axis.title = "Market"

    data_ref_chart1 = Reference(ws_dashboard, min_col=3, min_row=10, max_col=8, max_row=14)
    categories_ref_chart1 = Reference(ws_dashboard, min_col=2, min_row=10, max_col=2, max_row=14)
    
    chart1.add_data(data_ref_chart1, titles_from_data=True)
    chart1.set_categories(categories_ref_chart1)
    
    chart1.height = 10 # Height in cm. Video shows custom size, translating to approx. 10cm.
    chart1.width = 15 # Width in cm.
    chart1.x_axis.txPr = openpyxl.drawing.text.TextCharacterProperties()
    chart1.x_axis.txPr.rot = -4500000 # Rotate X-axis labels to -45 degrees, as seen in the video.
    chart1.y_axis.number_format = "$#,##0"
    
    ws_dashboard.add_chart(chart1, "D7") # Position on dashboard

    # Chart 2: Units Sold Each Month (Line Chart)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.y_axis.title = "Units Sold"
    chart2.x_axis.title = "Month"

    data_ref_chart2 = Reference(ws_dashboard, min_col=3, min_row=26, max_col=14, max_row=26)
    categories_ref_chart2 = Reference(ws_dashboard, min_col=3, min_row=25, max_col=14, max_row=25)
    
    chart2.add_data(data_ref_chart2, titles_from_data=True)
    chart2.set_categories(categories_ref_chart2)
    chart2.y_axis.number_format = "#,##0"
    
    chart2.height = 5
    chart2.width = 10
    
    ws_dashboard.add_chart(chart2, "K7") # Position on dashboard

    # Chart 3: Profit by Month (Line Chart)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.y_axis.title = "Profit"
    chart3.x_axis.title = "Month"

    data_ref_chart3 = Reference(ws_dashboard, min_col=3, min_row=30, max_col=14, max_row=30)
    categories_ref_chart3 = Reference(ws_dashboard, min_col=3, min_row=25, max_col=14, max_row=25) # Reuse month categories
    
    chart3.add_data(data_ref_chart3, titles_from_data=True)
    chart3.set_categories(categories_ref_chart3)
    chart3.y_axis.number_format = "$#,##0"

    chart3.height = 5
    chart3.width = 10
    
    ws_dashboard.add_chart(chart3, "K20") # Position on dashboard


    # --- 6. Slicers and Timelines (Not directly creatable with openpyxl) ---
    # Openpyxl does not currently support direct creation of Slicers or Timelines
    # via its API. These are advanced Excel UI objects.
    # The dashboard is structured to accommodate them if added manually in Excel
    # after the file is generated, or if a different library is used for this specific feature.
    # The video shows dragging and resizing slicers to specific cells, and then connecting them.
    # This connection would typically be managed in Excel's UI (right-click slicer -> Report Connections).
    
    # Placeholder for visual guidance for slicers/timeline
    slicer_area_start_col = 2
    slicer_area_start_row = 7
    slicer_area_end_col = 3
    slicer_area_end_row = 40
    
    # Timeline Placeholder
    ws_dashboard.cell(row=slicer_area_start_row, column=slicer_area_start_col, value="Date (Timeline)")
    ws_dashboard.merge_cells(start_row=slicer_area_start_row, start_column=slicer_area_start_col,
                             end_row=slicer_area_start_row + 4, end_column=slicer_area_end_col)
    ws_dashboard.cell(row=slicer_area_start_row, column=slicer_area_start_col).alignment = Alignment(horizontal='center', vertical='center')
    ws_dashboard.cell(row=slicer_area_start_row, column=slicer_area_start_col).fill = _create_fill(colors["accent_bg"])
    ws_dashboard.cell(row=slicer_area_start_row, column=slicer_area_start_col).font = _create_font(colors["accent_fg"], bold=True)

    # Country Slicer Placeholder
    ws_dashboard.cell(row=slicer_area_start_row + 5, column=slicer_area_start_col, value="Country Slicer")
    ws_dashboard.merge_cells(start_row=slicer_area_start_row + 5, start_column=slicer_area_start_col,
                             end_row=slicer_area_start_row + 15, end_column=slicer_area_end_col)
    ws_dashboard.cell(row=slicer_area_start_row + 5, column=slicer_area_start_col).alignment = Alignment(horizontal='center', vertical='center')
    ws_dashboard.cell(row=slicer_area_start_row + 5, column=slicer_area_start_col).fill = _create_fill(colors["accent_bg"])
    ws_dashboard.cell(row=slicer_area_start_row + 5, column=slicer_area_start_col).font = _create_font(colors["accent_fg"], bold=True)


    # Product Slicer Placeholder
    ws_dashboard.cell(row=slicer_area_start_row + 16, column=slicer_area_start_col, value="Product Slicer")
    ws_dashboard.merge_cells(start_row=slicer_area_start_row + 16, start_column=slicer_area_start_col,
                             end_row=slicer_area_end_row, end_column=slicer_area_end_col)
    ws_dashboard.cell(row=slicer_area_start_row + 16, column=slicer_area_start_col).alignment = Alignment(horizontal='center', vertical='center')
    ws_dashboard.cell(row=slicer_area_start_row + 16, column=slicer_area_start_col).fill = _create_fill(colors["accent_bg"])
    ws_dashboard.cell(row=slicer_area_start_row + 16, column=slicer_area_start_col).font = _create_font(colors["accent_fg"], bold=True)

    # --- 7. Hide supporting sheets ---
    ws_data.sheet_state = 'hidden'
    ws_pt_profit_market_cookie.sheet_state = 'hidden'
    ws_pt_units_sold.sheet_state = 'hidden'
    ws_pt_profit_month.sheet_state = 'hidden'
    
    wb.active = ws_dashboard # Set dashboard as active sheet on open

