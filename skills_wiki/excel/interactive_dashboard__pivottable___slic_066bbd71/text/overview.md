### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Dashboard (PivotTable & Slicer Based)

*   **Tier**: archetype
*   **Core Mechanism**: This skill constructs a fully interactive data dashboard in Microsoft Excel. It begins by structuring raw data into an Excel Table, which is then used as the source for multiple PivotTables and PivotCharts. The dashboard's interactivity is achieved by inserting Timeline and Slicer objects from the Excel UI and establishing "Report Connections" to link these filters to all underlying PivotTables, enabling dynamic filtering across all visuals. The final presentation is polished by hiding gridlines and headings and applying customizable Excel themes.
*   **Applicability**: This skill is ideal for creating dynamic, self-service reports from tabular datasets, such as sales performance, financial metrics, or project status. It allows users to easily filter and analyze data across various dimensions (e.g., date ranges, geographical regions, product categories) and automatically updates when new data is added to the source table.

### 2. Structural Breakdown

-   **Data Layout**:
    *   **"Data" Worksheet**: Contains the raw, tabular dataset with columns like `Country`, `Product`, `Units Sold`, `Revenue`, `Cost`, `Profit`, and `Date`. This data is converted into an Excel Table (e.g., "SalesData") which automatically expands when new data is pasted, ensuring PivotTables always reference the latest information.
    *   **Hidden PivotTable Worksheets**: Separate, hidden sheets are created for each PivotTable and its corresponding PivotChart. These sheets act as intermediary data processing layers for the dashboard.
    *   **"Dashboard" Worksheet**: The primary user-facing sheet that displays the PivotCharts, Slicers, and Timelines. It features a custom header for branding and has gridlines and column/row headings hidden for a clean, professional appearance.
-   **Formula Logic**:
    *   The core data aggregation and manipulation are handled by PivotTables using functions like "Sum of Profit" and "Sum of Units Sold." No direct cell formulas are used on the dashboard itself, ensuring maintainability and robustness.
    *   (Note: Openpyxl has limitations in fully replicating Excel's UI-driven PivotTable creation and dynamic date grouping within PivotTables via code. The code provides a simplified representation for charting.)
-   **Visual Design**:
    *   **Themes**: The entire dashboard's color scheme, fonts, and general aesthetic are managed by Excel's built-in "Themes" (`Page Layout > Themes`), allowing for quick, consistent branding customization.
    *   **Dashboard Header**: A merged cell at the top provides a prominent title and company logo/name, styled with theme-derived background and font colors (e.g., `header_bg`, `header_fg`).
    *   **Clean Interface**: Gridlines and sheet headings are hidden (`View` tab in Excel) to give the dashboard a polished, application-like feel.
    *   **Slicers/Timelines**: These interactive elements are styled with theme colors, and their default headers are removed to integrate seamlessly into the dashboard layout.
-   **Charts/Tables**:
    *   **Source Table**: The raw data is formatted as an Excel `Table` (`TableStyleLight9` preset is used in the video example), which is essential for dynamic data range updates.
    *   **PivotTables**:
        *   `Profit by Market & Cookie Type`: Aggregates `Profit` by `Country` (rows) and `Product` (columns). Rows and columns are sorted by total profit (largest to smallest).
        *   `Units sold each month`: Aggregates `Units Sold` by `Date` (grouped by months) in rows.
        *   `Profit by month`: Aggregates `Profit` by `Date` (grouped by months) in rows.
    *   **PivotCharts**:
        *   `Profit by Market & Cookie Type`: A Stacked Column Chart visualizes profits across markets and cookie types.
        *   `Units sold each month`: A Line Chart displays unit sales trends over time.
        *   `Profit by month`: A Line Chart shows profit trends over time.
        *   All charts have custom titles, hidden legends, and hidden field buttons (to declutter). They are precisely sized and aligned on the dashboard.
    *   **Slicers**: One Slicer each for `Country` and `Product`.
    *   **Timeline**: One Timeline for `Date`.
    *   **Report Connections**: All Slicers and Timelines are connected to all PivotTables on the hidden sheets via "Report Connections" (configured manually in Excel UI), ensuring that filtering any slicer updates all relevant charts.
-   **Theme Hooks**: `header_bg`, `header_fg`, `accent_colors` (for chart series and slicers), `text_color`, `neutral_colors`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Color
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta
import random

# Helper to load theme colors
def _get_theme_colors(theme_name):
    themes = {
        "corporate_blue": {
            "header_bg": "FF3366CC",  # Blue
            "header_fg": "FFFFFFFF",  # White
            "accent1": "FF4472C4",
            "accent2": "FFED7D31",
            "accent3": "FF70AD47",
            "accent4": "FFFFC000",
            "accent5": "FF5B9BD5",
            "chart_series_colors": ["FF4472C4", "FFED7D31", "FF70AD47", "FFFFC000", "FF5B9BD5", "FFA5A5A5", "FF255B9BD5"],
        },
        "green_scheme": {
            "header_bg": "FF008000", # Green
            "header_fg": "FFFFFFFF", # White
            "accent1": "FF00B050",
            "accent2": "FF92D050",
            "accent3": "FFC6E0B4",
            "accent4": "FFFFC000",
            "accent5": "FF5B9BD5",
            "chart_series_colors": ["FF00B050", "FF92D050", "FFC6E0B4", "FFFFC000", "FF5B9BD5", "FFA5A5A5", "FF008000"],
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    colors = _get_theme_colors(theme)

    # --- 1. Raw Data Sheet ---
    data_sheet_name = "Data"
    # Ensure sheet exists or create it, then remove content
    if data_sheet_name in wb.sheetnames:
        data_ws = wb[data_sheet_name]
        wb.remove(data_ws)
    data_ws = wb.create_sheet(data_sheet_name, 0) # Create as first sheet
    data_ws.title = data_sheet_name

    headers = ["Country", "Product", "Units Sold", "Revenue", "Cost", "Profit", "Date"]
    data_ws.append(headers)

    countries = ["India", "Malaysia", "Philippines", "United Kingdom", "United States"]
    products = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar", "White Chocolate Macadamia Nut"]
    start_date = datetime(2019, 1, 1)

    for _ in range(500): # Generate 500 rows of sample data
        country = random.choice(countries)
        product = random.choice(products)
        units_sold = random.randint(100, 5000)
        revenue = round(units_sold * random.uniform(2, 5), 2)
        cost = round(revenue * random.uniform(0.3, 0.7), 2)
        profit = round(revenue - cost, 2)
        date = start_date + timedelta(days=random.randint(0, 365*2)) # Data for 2 years
        data_ws.append([country, product, units_sold, revenue, cost, profit, date])

    # Convert data to an Excel Table
    table_ref = f"A1:{get_column_letter(len(headers))}{data_ws.max_row}"
    tab = Table(displayName="SalesData", ref=table_ref)
    style = TableStyleInfo(name="TableStyleLight9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    data_ws.add_table(tab)

    # Format Date and Currency columns
    for col_idx in [4, 5, 6]: # Revenue, Cost, Profit (D, E, F)
        col_letter = get_column_letter(col_idx)
        for row_idx in range(2, data_ws.max_row + 1): # Start from row 2 for data
            cell = data_ws[f"{col_letter}{row_idx}"]
            if isinstance(cell.value, (int, float)):
                cell.number_format = '"$"#,##0.00'
    for row_idx in range(2, data_ws.max_row + 1): # Date (G)
        cell = data_ws[f"G{row_idx}"]
        if isinstance(cell.value, datetime):
            cell.number_format = 'm/d/yyyy'

    # --- 2. Dashboard Sheet Setup ---
    dashboard_ws_name = "Dashboard"
    if dashboard_ws_name in wb.sheetnames:
        dashboard_ws = wb[dashboard_ws_name]
        wb.remove(dashboard_ws)
    dashboard_ws = wb.create_sheet(dashboard_ws_name, 1) # Create as second sheet
    dashboard_ws.title = dashboard_ws_name

    # Set up dashboard header
    dashboard_ws.merge_cells('D1:P3') # Adjusted range to leave space for cookie
    header_cell = dashboard_ws['D1']
    header_cell.value = "Performance Dashboard"
    header_cell.font = Font(name='Calibri', size=24, bold=True, color=colors["header_fg"][2:])
    header_cell.fill = PatternFill(start_color=colors["header_bg"][2:], end_color=colors["header_bg"][2:], fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Company Logo/Title placeholder
    dashboard_ws.merge_cells('A1:C3')
    company_cell = dashboard_ws['A1']
    company_cell.value = "KEVIN COOKIE COMPANY 🍪"
    company_cell.font = Font(name='Calibri', size=16, bold=True, color=colors["header_fg"][2:])
    company_cell.fill = PatternFill(start_color=colors["header_bg"][2:], end_color=colors["header_bg"][2:], fill_type="solid")
    company_cell.alignment = Alignment(horizontal="center", vertical="center")


    # Hide gridlines and headings for a clean look
    dashboard_ws.sheet_view.showGridLines = False
    dashboard_ws.sheet_view.showHeadings = False
    
    # --- 3. PivotTable/PivotChart Creation and Copying ---
    
    # Helper function to create sheets with chart data and chart.
    # Openpyxl does not natively create PivotTables from code in a fully flexible way (e.g., date grouping).
    # This helper simulates the *data output* a PivotTable would produce for charting purposes.
    # To make the dashboard fully functional, the user would need to manually create/refresh PivotTables
    # in Excel UI from the "SalesData" table.
    def _create_chart_source_sheet(wb, sheet_name, chart_title, chart_type, row_vals, col_vals, data_vals, series_colors, *, chart_sub_type=None, number_format=None):
        chart_source_ws_name = sheet_name.replace(" ", "")
        if chart_source_ws_name in wb.sheetnames:
            ws = wb[chart_source_ws_name]
            wb.remove(ws)
        ws = wb.create_sheet(chart_source_ws_name)
        ws.title = chart_source_ws_name
        
        # Manually populate data that simulates PivotTable output for charting
        # This is simplified and for demonstration only.
        if "Product" in col_vals: # Stacked column chart
            ws['A3'] = "Country"
            col_headers = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar", "White Chocolate Macadamia Nut"]
            for c_idx, prod_name in enumerate(col_headers):
                ws[f'{get_column_letter(2+c_idx)}3'] = prod_name
            ws[f'{get_column_letter(2+len(col_headers))}3'] = "Grand Total"
            
            countries_list = ["India", "Philippines", "United Kingdom", "Malaysia", "United States"] # Video's sorted order
            for r_idx, country in enumerate(countries_list):
                ws[f'A{4+r_idx}'] = country
                total_profit_country = 0
                for c_idx in range(len(col_headers)):
                    profit_val = random.randint(20000, 70000)
                    ws[f'{get_column_letter(2+c_idx)}{4+r_idx}'] = profit_val
                    total_profit_country += profit_val
                ws[f'{get_column_letter(2+len(col_headers))}{4+r_idx}'] = total_profit_country
            
            ws['A' + str(4 + len(countries_list))] = "Grand Total"
            for c_idx in range(2, 2+len(col_headers)+1): # Total columns
                 ws[f'{get_column_letter(c_idx)}{4+len(countries_list)}'] = random.randint(100000, 800000)

            # Apply number format
            for r in range(4, ws.max_row + 1):
                for c in range(2, ws.max_column + 1):
                    ws[f'{get_column_letter(c)}{r}'].number_format = number_format or '"$"#,##0'


        elif "Date" in row_vals and ("Units Sold" in data_vals or "Profit" in data_vals):
            ws['A3'] = "Months"
            ws['B3'] = data_vals[0] # "Units Sold" or "Profit"
            
            months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            
            for year in range(2019, 2021): # Data for 2019 and 2020
                for m_idx, month_name in enumerate(months_order):
                    row_idx = 4 + (year - 2019) * 12 + m_idx
                    ws[f'A{row_idx}'] = month_name
                    if "Units Sold" in data_vals:
                        val = random.randint(20000, 150000)
                    else: # Profit
                        val = random.randint(100000, 600000)
                    ws[f'B{row_idx}'] = val
                    ws[f'B{row_idx}'].number_format = number_format or '#,##0'

        # Insert Chart
        if chart_type == LineChart:
            chart = LineChart()
        else:
            chart = BarChart()
            if chart_sub_type == "stacked":
                chart.grouping = "stacked"
                chart.overlap = 100

        chart.title = chart_title
        
        # Chart data ranges based on the manually created data
        if "Product" in col_vals: # Stacked Column Chart
            data_start_col = 2
            data_end_col = 2 + len(col_headers) -1 # Exclude grand total col for series
            data_start_row = 3
            data_end_row = 3 + len(countries_list) # Exclude grand total row for categories
            cats_start_row = 4
            cats_end_row = 3 + len(countries_list)
        else: # Line Charts
            data_start_col = 2
            data_end_col = 2
            data_start_row = 3
            data_end_row = 3 + 2 * 12 # 2 years, 12 months per year
            cats_start_row = 4
            cats_end_row = 3 + 2 * 12


        # References for charting
        data_ref = Reference(ws, min_col=data_start_col, min_row=data_start_row,
                             max_col=data_end_col, max_row=data_end_row)
        cats_ref = Reference(ws, min_col=1, min_row=cats_start_row, max_row=cats_end_row)

        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        
        chart.legend = None # Hide legend (as in video)
        
        # Set chart series colors
        for i, series in enumerate(chart.series):
            if i < len(series_colors):
                series.graphicalProperties.solidFill = Color(rgb=colors["chart_series_colors"][i][2:])
                series.graphicalProperties.line.noFill = True # For bar charts, or set specific line colors for line charts

        ws.add_chart(chart, "J1")
        ws.sheet_state = 'hidden' # Hide this sheet
        
        return chart, ws

    # Chart 1: Profit by Market & Cookie Type (Stacked Column)
    chart1, _ = _create_chart_source_sheet(wb, "ProfitByMarketCookie",
                                              "Profit by Market & Cookie Type",
                                              BarChart, ["Country"], products, ["Profit"], colors["chart_series_colors"], chart_sub_type="stacked", number_format='"$"#,##0')
    dashboard_ws.add_chart(chart1, "E5")
    chart1.width = 10
    chart1.height = 10

    # Chart 2: Units Sold Each Month (Line Chart)
    chart2, _ = _create_chart_source_sheet(wb, "UnitsSoldEachMonth",
                                              "Units sold each month", LineChart, ["Date"], [], ["Units Sold"], colors["chart_series_colors"], number_format='#,##0')
    dashboard_ws.add_chart(chart2, "L5")
    chart2.width = 9.5
    chart2.height = 6

    # Chart 3: Profit by Month (Line Chart)
    chart3, _ = _create_chart_source_sheet(wb, "ProfitByMonth",
                                              "Profit by month", LineChart, ["Date"], [], ["Profit"], colors["chart_series_colors"], number_format='"$"#,##0')
    dashboard_ws.add_chart(chart3, "L18")
    chart3.width = 9.5
    chart3.height = 6
    
    # --- 4. Slicers and Timeline Placeholders (Requires manual Excel UI action) ---
    # Openpyxl does not support dynamic Slicers or Timelines natively.
    # The following text placeholders indicate where they would be placed and describe their purpose.
    # After generating the workbook, you would manually insert these from the Excel UI:
    # 1. Go to 'Insert' -> 'Slicer' and select 'Country' and 'Product'.
    # 2. Go to 'Insert' -> 'Timeline' and select 'Date'.
    # 3. Move these slicers/timeline to the Dashboard sheet (A5, A11, A18 approx).
    # 4. Right-click each slicer/timeline -> 'Report Connections...' and check all relevant PivotTables.
    #    (You'd first need to create actual PivotTables from the "Data" table on the hidden sheets).
    # 5. Adjust their size and remove headers via 'Slicer Settings' as shown in the video.

    # These are visual placeholders, not functional slicers
    # Timeline
    dashboard_ws['A5'] = "Date"
    dashboard_ws['A6'] = "All Periods"
    dashboard_ws['A7'] = "2019 - 2020"
    dashboard_ws['A8'] = "MONTHS"
    dashboard_ws['A9'] = "OCT NOV DEC"
    dashboard_ws['A10'] = "[Timeline Here]"
    
    # Country Slicer
    dashboard_ws['A12'] = "India"
    dashboard_ws['A13'] = "Malaysia"
    dashboard_ws['A14'] = "Philippines"
    dashboard_ws['A15'] = "United Kingdom"
    dashboard_ws['A16'] = "United States"
    dashboard_ws['A11'] = "Country Slicer (Manual)"
    
    # Product Slicer
    dashboard_ws['A19'] = "Chocolate Chip"
    dashboard_ws['A20'] = "Fortune Cookie"
    dashboard_ws['A21'] = "Oatmeal Raisin"
    dashboard_ws['A22'] = "Snickerdoodle"
    dashboard_ws['A23'] = "Sugar"
    dashboard_ws['A24'] = "White Chocolate Macadamia Nut"
    dashboard_ws['A18'] = "Product Slicer (Manual)"

    # Set default active sheet to Dashboard
    wb.active = dashboard_ws

    # Remove the default 'Sheet' if it exists and wasn't overwritten
    if "Sheet" in wb.sheetnames and len(wb["Sheet"]._cells) == 0:
        del wb["Sheet"]

```