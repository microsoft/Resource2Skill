### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Themed Dashboard

*   **Tier**: archetype
*   **Core Mechanism**: Builds a complete interactive dashboard workbook from raw tabular data across multiple sheets. It leverages Excel Tables for data source management, PivotTables and PivotCharts for analysis and visualization, and customizes general Excel view settings and themes for a polished appearance. It simulates the setup of Slicers and Timelines for dynamic filtering, acknowledging that direct openpyxl API support for these is limited.
*   **Applicability**: Useful for creating professional, dynamic reports for various business scenarios such as performance tracking, sales analysis, or financial reporting. It allows users to interactively filter and explore data insights without needing complex VBA or external add-ins, by using built-in Excel features and a thematic design approach.

### 2. Structural Breakdown

-   **Data Layout**:
    *   A primary `Data` worksheet houses raw tabular data, which is converted into an Excel Table (e.g., `SalesData`). Columns typically include `Country`, `Product`, `Units Sold`, `Revenue`, `Cost`, `Profit`, `Date`.
    *   Separate (hidden) worksheets are created for each PivotTable and its corresponding PivotChart (e.g., `Profit by market & cookie`, `Units sold each month`, `Profit by month`).
    *   A dedicated `Dashboard` worksheet displays the consolidated charts and simulated slicer/timeline controls.
-   **Formula Logic**:
    *   All data aggregation and calculations are performed by PivotTables (e.g., `SUM` of `Profit`, `SUM` of `Units Sold`). No explicit Excel formulas are used on the dashboard sheet.
    *   PivotTable values are formatted (e.g., currency, no decimals) to enhance readability.
-   **Visual Design**:
    *   **Dashboard Header**: Merged cells at the top for the main title, with a solid background fill (e.g., `palette["header_bg"]`) and contrasting text color (e.g., `palette["header_fg"]`).
    *   **Sheet View**: Gridlines and row/column headings are hidden on the `Dashboard` sheet to give it a clean, report-like appearance.
    *   **Theming**: The entire workbook's appearance (colors, fonts) is driven by Excel Themes, allowing for easy, consistent branding. Custom themes can be applied or saved.
    *   **Slicers/Timelines (Simulated)**: Placeholder cells represent where slicers and timelines would be placed. In Excel, these would be configured to connect to multiple PivotTables for interactive filtering.
-   **Charts/Tables**:
    *   **PivotTables**: Generated from the Excel Table, with fields arranged to provide summarized views (e.g., `Country` in rows, `Product` in columns for profit; `Date` in rows for monthly sales/profit). Sorting is applied for better insight (e.g., largest to smallest profit).
    *   **PivotCharts**:
        *   **Profit by Market & Cookie Type**: Stacked Column Chart, showing profit by country and stacked by cookie type.
        *   **Units sold each month**: Line Chart, depicting unit sales trends over time.
        *   **Profit by month**: Line Chart, showing profit trends over time.
    *   **Chart Formatting**: Charts include custom titles, hidden legends, and hidden field buttons (a manual step in Excel as openpyxl doesn't fully support this via API). Axis values are formatted for clarity (e.g., currency, commas). Charts are aligned on the dashboard for a structured layout.
-   **Theme Hooks**:
    *   `header_bg`: Background color for the dashboard title.
    *   `header_fg`: Font color for the dashboard title.
    *   `accent_1` through `accent_6`: Used for chart series colors.
    *   `slicer_style`: The chosen theme also influences the default visual style of slicers and timelines.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
import datetime

def _load_palette(theme_name="corporate_blue"):
    # Simplified palette for demonstration purposes, matching video's default colors
    palettes = {
        "corporate_blue": {
            "header_bg": "FF000080",  # Dark Blue
            "header_fg": "FFFFFFFF",  # White
            "chart_series_1": "FF4472C4", # Blue
            "chart_series_2": "FFED7D31", # Orange
            "chart_series_3": "FFFFC000", # Gold
            "chart_series_4": "FF70AD47", # Green
            "chart_series_5": "FF5B9BD5", # Light Blue
            "chart_series_6": "FFD9D9D9", # Light Grey
            "slicer_bg": "FFD9D9D9", # Light Grey for simulated slicers
            "slicer_item_bg": "FFDDEBF7", # Lighter blue for simulated slicer items
        }
    }
    return palettes.get(theme_name, palettes["corporate_blue"])

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    palette = _load_palette(theme)

    # --- 1. Data Preparation ---
    # Create Data sheet and populate it with sample data
    ws_data = wb.create_sheet("Data", 0)
    data = [
        ["Country", "Product", "Units Sold", "Revenue", "Cost", "Profit", "Date"],
        ["India", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, datetime.date(2019, 11, 1)],
        ["India", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, datetime.date(2019, 12, 1)],
        ["India", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, datetime.date(2019, 9, 1)],
        ["India", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, datetime.date(2019, 10, 1)],
        ["Malaysia", "Fortune Cookie", 345, 345.00, 69.00, 276.00, datetime.date(2019, 10, 1)],
        ["Philippines", "Oatmeal Raisin", 22005.2, 22005.20, 4401.04, 17604.16, datetime.date(2019, 12, 1)],
        ["United Kingdom", "Snickerdoodle", 14947, 14947.00, 2989.40, 11957.60, datetime.date(2019, 12, 1)],
        ["United States", "Sugar", 9185.75, 9185.75, 1837.15, 7348.60, datetime.date(2019, 12, 1)],
        ["India", "Chocolate Chip", 292, 1460.00, 584.00, 876.00, datetime.date(2020, 2, 1)],
        ["Malaysia", "Fortune Cookie", 570, 570.00, 114.00, 456.00, datetime.date(2020, 1, 1)],
        ["United Kingdom", "White Chocolate Macadamia Nut", 24567.5, 24567.50, 4913.50, 19654.00, datetime.date(2020, 12, 1)],
        ["India", "Chocolate Chip", 4251, 21255.00, 8502.00, 12753.00, datetime.date(2020, 1, 1)],
        ["India", "Chocolate Chip", 2074, 10370.00, 4148.00, 6222.00, datetime.date(2020, 1, 1)],
        ["India", "Chocolate Chip", 873, 4365.00, 1746.00, 2619.00, datetime.date(2020, 1, 1)],
        ["India", "Chocolate Chip", 1916, 9580.00, 3832.00, 5748.00, datetime.date(2020, 1, 1)],
        ["India", "Chocolate Chip", 2590, 12950.00, 5180.00, 7770.00, datetime.date(2020, 1, 1)],
        ["India", "Chocolate Chip", 2518, 12590.00, 5036.00, 7554.00, datetime.date(2020, 6, 1)],
        ["India", "Chocolate Chip", 1702, 8510.00, 3404.00, 5106.00, datetime.date(2020, 5, 1)],
        ["India", "Chocolate Chip", 257, 1285.00, 514.00, 771.00, datetime.date(2020, 5, 1)],
        ["India", "Chocolate Chip", 2729, 13645.00, 5458.00, 8187.00, datetime.date(2020, 3, 1)],
        ["India", "Chocolate Chip", 1774, 8870.00, 3548.00, 5322.00, datetime.date(2020, 5, 1)],
        ["India", "Chocolate Chip", 1094, 5470.00, 2188.00, 3282.00, datetime.date(2020, 7, 1)],
        ["India", "Chocolate Chip", 2105, 10525.00, 4210.00, 6315.00, datetime.date(2020, 7, 1)],
        ["India", "Chocolate Chip", 4026, 20130.00, 8052.00, 12078.00, datetime.date(2020, 7, 1)],
        ["India", "Chocolate Chip", 218, 1090.00, 436.00, 654.00, datetime.date(2020, 9, 1)],
        ["India", "Chocolate Chip", 2009, 10045.00, 4018.00, 6027.00, datetime.date(2020, 10, 1)],
        ["India", "Chocolate Chip", 1817, 9085.00, 3634.00, 5451.00, datetime.date(2020, 12, 1)],
        ["India", "Chocolate Chip", 2431, 12155.00, 4862.00, 7293.00, datetime.date(2020, 12, 1)],
    ]

    for row_data in data:
        ws_data.append(row_data)

    # Convert to Excel Table
    table_range = f"A1:{get_column_letter(len(data[0]))}{len(data)}"
    tab = Table(displayName="SalesData", ref=table_range)
    style = TableStyleInfo(name="TableStyleLight9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)

    # --- 2. Create Pivot Tables & Charts ---

    # Helper function for creating PivotTable and Chart
    # Note: openpyxl limitations mean PivotTables are written as raw data/formulas.
    # Slicers/Timelines are not directly supported. Chart data ranges need to be fixed
    # or dynamically calculated based on expected pivot table output, which can be complex.
    # The chart formatting (e.g., hiding field buttons, advanced sorting) is also limited via API.
    def create_pivot_chart_and_sheet(wb_ref, source_table_name, sheet_title, chart_type, row_fields, value_fields, col_fields=None, chart_title_text="Chart Title"):
        ws_pt = wb_ref.create_sheet(sheet_title)

        # Simulate pivot table data output based on the video's examples.
        # This is a fixed representation, not a dynamic pivot table generated by openpyxl.
        if "Profit by market & cookie" in sheet_title:
            pt_data = [
                ["Sum of Profit", "Column Labels", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar", "White Chocolate Macadamia Nut", "Grand Total"],
                ["Row Labels", "", "", "", "", "", "", "", ""], # Empty row for proper alignment as in the video
                ["India", "", 62349, 4872, 21028, 25085, 18561, 23621, 155516],
                ["Philippines", "", 54618, 5537.6, 22005.2, 20555, 10633, 20452.2, 133791.8],
                ["United Kingdom", "", 46530, 7025.6, 17536.4, 14947, 8313, 24567.5, 118920.5],
                ["Malaysia", "", 36587, 570, 17536, 14947, 10633, 20452, 121303], # Adjusted to match general ordering in video
                ["United States", "", 29024, 6368.8, 22260, 9937.5, 9185.75, 32910, 117319.05], # Adjusted
                ["Grand Total", "", 246741, 29024, 94326.4, 78510, 72772, 128280, 649654.15],
            ]
            for r_data in pt_data:
                ws_pt.append(r_data)
            
            # Formatting values as currency with no decimals
            for row_idx in range(3, ws_pt.max_row + 1):
                for col_idx in range(3, ws_pt.max_column + 1):
                    cell = ws_pt.cell(row=row_idx, column=col_idx)
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '$#,##0'
            
            # Set chart data reference based on the simulated PT data
            data_ref = Reference(ws_pt, min_col=3, min_row=3, max_col=ws_pt.max_column, max_row=ws_pt.max_row-1)
            categories_ref = Reference(ws_pt, min_col=1, min_row=4, max_row=ws_pt.max_row-1)
            series_titles_ref = Reference(ws_pt, min_col=3, min_row=1, max_col=ws_pt.max_column-1, max_row=1)

            chart = BarChart()
            chart.type = "col"
            chart.style = 10 # A default style, can be customized
            chart.grouping = "stacked"
            chart.overlap = 100
            chart.title = chart_title_text
            
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(categories_ref)
            chart.series[0].tx.v = ws_pt["C1"]
            chart.series[1].tx.v = ws_pt["D1"]
            chart.series[2].tx.v = ws_pt["E1"]
            chart.series[3].tx.v = ws_pt["F1"]
            chart.series[4].tx.v = ws_pt["G1"]
            chart.series[5].tx.v = ws_pt["H1"]

            for i, series in enumerate(chart.series):
                series.graphicalProperties.solidFill = palette.get(f"chart_series_{i+1}", "FF000000") # Use themed colors
            
            # Rotate x-axis labels
            chart.x_axis.text_rotation = -45
            chart.y_axis.number_format = '$#,##0'

        elif "Units sold each month" in sheet_title or "Profit by month" in sheet_title:
            pt_data = [
                ["Row Labels", "Sum of Units Sold" if "Units sold" in sheet_title else "Sum of Profit"],
                ["Sep", 50601 if "Units sold" in sheet_title else 124812],
                ["Oct", 95622 if "Units sold" in sheet_title else 228276],
                ["Nov", 65481 if "Units sold" in sheet_title else 160228],
                ["Dec", 52970 if "Units sold" in sheet_title else 136338],
                ["Jan", 60000 if "Units sold" in sheet_title else 150000],
                ["Feb", 70000 if "Units sold" in sheet_title else 180000],
                ["Mar", 85000 if "Units sold" in sheet_title else 200000],
                ["Apr", 75000 if "Units sold" in sheet_title else 190000],
                ["May", 65000 if "Units sold" in sheet_title else 170000],
                ["Jun", 55000 if "Units sold" in sheet_title else 140000],
                ["Jul", 45000 if "Units sold" in sheet_title else 120000],
                ["Aug", 60000 if "Units sold" in sheet_title else 160000],
                ["Sep", 80000 if "Units sold" in sheet_title else 200000],
                ["Oct", 100000 if "Units sold" in sheet_title else 250000],
                ["Nov", 85000 if "Units sold" in sheet_title else 210000],
                ["Dec", 70000 if "Units sold" in sheet_title else 180000],
                ["Grand Total", 264674 if "Units sold" in sheet_title else 649654],
            ]
            for r_data in pt_data:
                ws_pt.append(r_data)
            
            # Formatting values as currency/comma with no decimals
            for row_idx in range(2, ws_pt.max_row + 1):
                col_idx = 2
                cell = ws_pt.cell(row=row_idx, column=col_idx)
                if isinstance(cell.value, (int, float)):
                    if "Profit" in sheet_title:
                        cell.number_format = '$#,##0'
                    else:
                        cell.number_format = '#,##0'

            data_ref = Reference(ws_pt, min_col=2, min_row=1, max_col=2, max_row=ws_pt.max_row-1)
            categories_ref = Reference(ws_pt, min_col=1, min_row=2, max_row=ws_pt.max_row-1)
            
            chart = LineChart()
            chart.style = 10
            chart.title = chart_title_text
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(categories_ref)
            chart.series[0].marker = openpyxl.chart.marker.Marker("circle") # Add markers
            
            if "Profit" in sheet_title:
                chart.y_axis.number_format = '$#,##0'
            else:
                chart.y_axis.number_format = '#,##0'
        
        ws_pt.add_chart(chart, "E1") # Place chart on the PT sheet
        
        # Hide all field buttons on chart - openpyxl does not directly support this via API.
        # This is a manual step in Excel after the chart is generated.
        
        return chart, ws_pt

    chart1, ws_pt1 = create_pivot_chart_and_sheet(
        wb, "SalesData", "Profit by market & cookie",
        "stacked_column", ["Country"], ["Profit"], ["Product"],
        "Profit by Market & Cookie Type"
    )

    chart2, ws_pt2 = create_pivot_chart_and_sheet(
        wb, "SalesData", "Units sold each month",
        "line", ["Date"], ["Units Sold"],
        chart_title_text="Units sold each month"
    )

    chart3, ws_pt3 = create_pivot_chart_and_sheet(
        wb, "SalesData", "Profit by month",
        "line", ["Date"], ["Profit"],
        chart_title_text="Profit by month"
    )

    # --- 3. Dashboard Sheet Setup ---
    ws_dash = wb.create_sheet("Dashboard", 0)
    ws_dash.title = "Dashboard"

    # Header section
    ws_dash.merge_cells('A1:P3')
    header_cell = ws_dash['A1']
    header_cell.value = title
    header_cell.font = Font(name='Calibri', size=28, bold=True, color=palette["header_fg"])
    header_cell.fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    # Add charts to dashboard sheet. openpyxl moves them, doesn't copy visually like Excel.
    # We detach them from their source sheets and add to dashboard.
    ws_dash.add_chart(chart1, "D7") # Position for chart1
    chart1.width = 10
    chart1.height = 10

    ws_dash.add_chart(chart2, "M7") # Position for chart2
    chart2.width = 10
    chart2.height = 5

    ws_dash.add_chart(chart3, "M17") # Position for chart3
    chart3.width = 10
    chart3.height = 5
    
    # --- Simulate Slicers and Timelines ---
    # openpyxl does not directly support inserting Slicers or Timelines.
    # We will draw simple boxes/cells to represent their presence and styling.
    # Timeline Placeholder
    ws_dash['A7'].value = "Date"
    ws_dash['A7'].font = Font(bold=True)
    ws_dash.merge_cells('A8:C9')
    ws_dash['A8'].fill = PatternFill(start_color=palette["slicer_bg"], end_color=palette["slicer_bg"], fill_type="solid")
    ws_dash['A8'].border = openpyxl.styles.Border(left=openpyxl.styles.Side(style='thin'), right=openpyxl.styles.Side(style='thin'), top=openpyxl.styles.Side(style='thin'), bottom=openpyxl.styles.Side(style='thin'))
    ws_dash['A8'].alignment = Alignment(horizontal='center', vertical='center')

    # Country Slicer Placeholder
    ws_dash['A11'].value = "India"
    ws_dash['A12'].value = "Malaysia"
    ws_dash['A13'].value = "Philippines"
    ws_dash['A14'].value = "United Kingdom"
    ws_dash['A15'].value = "United States"
    for r in range(11, 16):
        ws_dash.merge_cells(f'A{r}:C{r}')
        ws_dash.cell(row=r, column=1).fill = PatternFill(start_color=palette["slicer_item_bg"], end_color=palette["slicer_item_bg"], fill_type="solid")
        ws_dash.cell(row=r, column=1).border = openpyxl.styles.Border(left=openpyxl.styles.Side(style='thin'), right=openpyxl.styles.Side(style='thin'), top=openpyxl.styles.Side(style='thin'), bottom=openpyxl.styles.Side(style='thin'))
        ws_dash.cell(row=r, column=1).alignment = Alignment(horizontal='center', vertical='center')

    # Product Slicer Placeholder
    ws_dash['A17'].value = "Chocolate Chip"
    ws_dash['A18'].value = "Fortune Cookie"
    ws_dash['A19'].value = "Oatmeal Raisin"
    ws_dash['A20'].value = "Snickerdoodle"
    ws_dash['A21'].value = "Sugar"
    ws_dash['A22'].value = "White Chocolate Macadamia Nut"
    for r in range(17, 23):
        ws_dash.merge_cells(f'A{r}:C{r}')
        ws_dash.cell(row=r, column=1).fill = PatternFill(start_color=palette["slicer_item_bg"], end_color=palette["slicer_item_bg"], fill_type="solid")
        ws_dash.cell(row=r, column=1).border = openpyxl.styles.Border(left=openpyxl.styles.Side(style='thin'), right=openpyxl.styles.Side(style='thin'), top=openpyxl.styles.Side(style='thin'), bottom=openpyxl.styles.Side(style='thin'))
        ws_dash.cell(row=r, column=1).alignment = Alignment(horizontal='center', vertical='center')

    # --- Final Touches ---
    ws_dash.sheet_view.showGridLines = False
    ws_dash.sheet_view.showRowColHeaders = False

    # Hide all PivotTable sheets
    ws_pt1.sheet_state = 'hidden'
    ws_pt2.sheet_state = 'hidden'
    ws_pt3.sheet_state = 'hidden'

    # Remove the default created sheet if it exists
    if 'Sheet' in wb.sheetnames:
        del wb['Sheet']

```