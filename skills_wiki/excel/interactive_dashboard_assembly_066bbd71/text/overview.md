### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Dashboard Assembly

*   **Tier**: archetype
*   **Core Mechanism**: This skill demonstrates how to assemble a comprehensive, interactive performance dashboard in Microsoft Excel. It leverages Excel Tables for structured data, PivotTables for data aggregation, PivotCharts for visual representation, and Slicers/Timelines for dynamic filtering. The mechanism focuses on integrating these elements into a clean, themed, and user-friendly interface.
*   **Applicability**: Ideal for business analysts, managers, or anyone needing to present key performance indicators (KPIs) and operational data in an accessible, dynamic, and easy-to-update format. Applicable to various datasets involving time series, categorical breakdowns, and numerical metrics.

### 2. Structural Breakdown

-   **Data Layout**: The raw data (sales records including Country, Product, Units Sold, Revenue, Cost, Profit, Date) is maintained on a dedicated "Data" sheet and formatted as an Excel Table. This ensures that new data automatically extends the table range, simplifying updates for derived PivotTables. Hidden sheets are used for each PivotTable instance that drives the dashboard charts.
-   **Formula Logic**: The core data aggregation and summarization are handled by Excel's built-in PivotTable functionality. No custom Excel formulas are explicitly shown for the dashboard visuals themselves, as PivotTables dynamically calculate sums and other aggregates based on chosen fields and filters.
-   **Visual Design**:
    *   **Header**: A prominent merged cell area at the top of the "Dashboard" sheet contains the company logo and "Performance Dashboard" title, styled with a solid background fill and contrasting text.
    *   **Sheet Aesthetics**: Gridlines and row/column headings are hidden on the "Dashboard" sheet to provide a clean, report-like appearance.
    *   **Themes**: Excel's "Page Layout" > "Themes" feature is used to quickly apply a consistent color scheme, fonts, and effects across all charts and slicers, ensuring a cohesive visual identity.
-   **Charts/Tables**:
    *   **Profit by Market & Cookie Type**: A stacked column chart visualizes profit breakdown by product type across different countries, ordered by overall market profitability.
    *   **Units Sold each month**: A line chart displays the trend of units sold over time (monthly).
    *   **Profit by month**: Another line chart illustrates the monthly profit trend.
    *   **Interactive Controls**: Slicers (for 'Country' and 'Product') and a Timeline (for 'Date') are used as interactive filters. These controls are positioned on the left side of the dashboard, connected to all underlying PivotTables to enable simultaneous filtering of all charts.
-   **Theme Hooks**: Header background (`header_bg`), text color (`header_fg`), chart series colors (`chart_series_colors`), and slicer styles (`accent_color`) are all derived from the chosen Excel theme.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

# Assume _helpers.py contains these functions for theme loading and styling
# from ._helpers import load_theme_colors, apply_fill, apply_font, apply_border
# For direct reproduction, I'll define mock helpers or direct styling where theme-dependent
# In a real setup, these would be imported from a standard helper module.

def _mock_apply_fill(cell_range, color):
    # Mock function to apply fill in openpyxl
    for row in ws[cell_range]:
        for cell in row:
            cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

def _mock_apply_font(cell_range, font_name="Calibri", size=11, bold=False, color="000000"):
    # Mock function to apply font in openpyxl
    for row in ws[cell_range]:
        for cell in row:
            cell.font = Font(name=font_name, size=size, bold=bold, color=color)

def _mock_load_theme_colors(theme_name):
    # Mock function to load theme colors. In a real scenario, this would parse a theme file.
    # For simplicity, returning a fixed set of colors.
    if theme_name == "corporate_blue":
        return {
            "header_bg": "002F6C",  # Dark Blue
            "header_fg": "FFFFFF",  # White
            "accent_color": "0070C0", # Medium Blue
            "chart_series_colors": ["0070C0", "ED7D31", "A5A5A5", "FFC000", "5B9BD5", "70AD47"]
        }
    elif theme_name == "dark_red":
        return {
            "header_bg": "800000",  # Dark Red
            "header_fg": "FFFFFF",  # White
            "accent_color": "C00000", # Medium Red
            "chart_series_colors": ["C00000", "FF6347", "8A2BE2", "DAA520", "4682B4", "3CB371"]
        }
    else: # Default theme
        return {
            "header_bg": "002F6C",
            "header_fg": "FFFFFF",
            "accent_color": "0070C0",
            "chart_series_colors": ["0070C0", "ED7D31", "A5A5A5", "FFC000", "5B9BD5", "70AD47"]
        }


def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an interactive performance dashboard in a multi-sheet Excel workbook.

    Args:
        wb (openpyxl.workbook.workbook.Workbook): The workbook object.
        title (str): The title of the dashboard.
        theme (str): The name of the color theme to apply (e.g., "corporate_blue").
    """
    theme_colors = _mock_load_theme_colors(theme)

    # --- 1. Data Sheet ---
    ws_data = wb.create_sheet("Data", 0)
    data = [
        ["Country", "Product", "Units Sold", "Revenue", "Cost", "Profit", "Date"],
        ["India", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, "11/1/2019"],
        ["India", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, "12/1/2019"],
        ["India", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, "9/1/2019"],
        ["India", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, "10/1/2019"],
        ["Malaysia", "Fortune Cookie", 345, 345.00, 69.00, 276.00, "10/1/2019"],
        ["Malaysia", "Sugar", 1611, 1611.00, 322.20, 1288.80, "11/1/2019"],
        ["United States", "Oatmeal Raisin", 2222, 11110.00, 4444.00, 6666.00, "11/1/2019"],
        ["United States", "Snickerdoodle", 2470, 12350.00, 4940.00, 7410.00, "9/1/2019"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 1743, 8715.00, 3486.00, 5229.00, "12/1/2019"],
        ["Philippines", "Chocolate Chip", 292, 1460.00, 584.00, 876.00, "1/1/2020"],
        ["India", "Sugar", 2518, 12590.00, 5036.00, 7554.00, "2/1/2020"],
        ["Malaysia", "Fortune Cookie", 2729, 13645.00, 5458.00, 8187.00, "3/1/2020"],
        ["United States", "Oatmeal Raisin", 4251, 21255.00, 8502.00, 12753.00, "4/1/2020"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 2074, 10370.00, 4148.00, 6222.00, "5/1/2020"],
        ["Philippines", "Chocolate Chip", 2431, 12155.00, 4862.00, 7293.00, "6/1/2020"],
        ["India", "Sugar", 1702, 8510.00, 3404.00, 5106.00, "7/1/2020"],
        ["Malaysia", "Fortune Cookie", 1094, 5470.00, 2188.00, 3282.00, "8/1/2020"],
        ["United States", "Oatmeal Raisin", 873, 4365.00, 1746.00, 2619.00, "9/1/2020"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 2105, 10525.00, 4210.00, 6315.00, "10/1/2020"],
        ["India", "Chocolate Chip", 4026, 20130.00, 8052.00, 12078.00, "11/1/2020"],
        ["India", "Sugar", 2567, 7701.00, 3208.75, 4492.25, "12/1/2020"],
        ["United States", "Snickerdoodle", 1806, 5418.00, 2257.50, 3160.50, "10/1/2020"],
        ["United States", "White Chocolate Macadamia Nut", 2821, 16926.00, 7575.75, 9168.25, "8/1/2020"],
        ["United Kingdom", "Sugar", 606, 3636.00, 1655.50, 1980.50, "7/1/2020"],
    ]
    for row_data in data:
        ws_data.append(row_data)

    # Convert data to a table
    table_ref = f"A1:{get_column_letter(len(data[0]))}{len(data)}"
    table = Table(displayName="SalesData", ref=table_ref)
    table.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showFirstColumn=False,
                                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    ws_data.add_table(table)

    # --- 2. Dashboard Sheet ---
    ws_dashboard = wb.create_sheet("Dashboard", 1)

    # Dashboard Header
    ws_dashboard.merge_cells('A1:P6')
    header_cell = ws_dashboard['A1']
    header_cell.value = "KEVIN COOKIE COMPANY Performance Dashboard"
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    _mock_apply_fill('A1:P6', theme_colors["header_bg"])
    _mock_apply_font('A1:P6', size=24, bold=True, color=theme_colors["header_fg"])

    # Hide gridlines and headings
    ws_dashboard.sheet_view.showGridLines = False
    ws_dashboard.sheet_view.showRowColHeaders = False

    # Simulate chart placement and add sample charts (actual data from source sheet)
    # Chart 1: Profit by Market & Cookie Type (Stacked Column Chart)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Profit by Market & Cookie Type"
    chart1.y_axis.title = "Profit"
    chart1.x_axis.title = "Country"
    chart1.height = 10 # cm
    chart1.width = 15 # cm

    # Example: Referencing data for a simplified chart (not fully pivoted in code)
    # In a full PivotChart setup, these references would point to pivot table output.
    data_ref_chart1 = Reference(ws_data, min_col=6, min_row=2, max_col=6, max_row=ws_data.max_row)
    categories_ref_chart1 = Reference(ws_data, min_col=1, min_row=2, max_col=1, max_row=ws_data.max_row)
    chart1.add_data(data_ref_chart1, titles_from_data=False)
    chart1.set_categories(categories_ref_chart1)
    chart1.series[0].graphicalProperties.solidFill = theme_colors["chart_series_colors"][0] # Example color
    ws_dashboard.add_chart(chart1, "C8") # Position the chart

    # Chart 2: Units Sold each month (Line Chart)
    chart2 = LineChart()
    chart2.style = 12
    chart2.title = "Units sold each month"
    chart2.y_axis.title = "Units Sold"
    chart2.x_axis.title = "Month"
    chart2.height = 6
    chart2.width = 12

    data_ref_chart2 = Reference(ws_data, min_col=3, min_row=2, max_col=3, max_row=ws_data.max_row)
    categories_ref_chart2 = Reference(ws_data, min_col=7, min_row=2, max_col=7, max_row=ws_data.max_row)
    chart2.add_data(data_ref_chart2, titles_from_data=False)
    chart2.set_categories(categories_ref_chart2)
    chart2.series[0].graphicalProperties.line.solidFill = theme_colors["chart_series_colors"][1]
    ws_dashboard.add_chart(chart2, "L8")

    # Chart 3: Profit by month (Line Chart)
    chart3 = LineChart()
    chart3.style = 12
    chart3.title = "Profit by month"
    chart3.y_axis.title = "Profit"
    chart3.x_axis.title = "Month"
    chart3.height = 6
    chart3.width = 12

    data_ref_chart3 = Reference(ws_data, min_col=6, min_row=2, max_col=6, max_row=ws_data.max_row)
    categories_ref_chart3 = Reference(ws_data, min_col=7, min_row=2, max_col=7, max_row=ws_data.max_row)
    chart3.add_data(data_ref_chart3, titles_from_data=False)
    chart3.set_categories(categories_ref_chart3)
    chart3.series[0].graphicalProperties.line.solidFill = theme_colors["chart_series_colors"][2]
    ws_dashboard.add_chart(chart3, "L22") # Adjust position

    # --- Slicer/Timeline Placeholder (OpenPyXL limitations) ---
    # OpenPyXL cannot directly insert Slicers or Timelines with full interactivity via code.
    # These elements are typically added via Excel's UI.
    # The following comments describe their intended placement and function as per the video.

    # Text box for Date Timeline: Positioned at A8.
    # Text box for Country Slicer: Positioned at A14.
    # Text box for Product Slicer: Positioned at A21.

    # To create actual Slicers and Timelines:
    # 1. Manually insert PivotTables on separate sheets for each chart's data.
    # 2. On the Dashboard sheet, go to "PivotChart Analyze" tab.
    # 3. Select "Insert Timeline" and choose the 'Date' field from any PivotTable.
    # 4. Select "Insert Slicer" and choose 'Country' and 'Product' fields.
    # 5. Right-click each Slicer/Timeline and select "Report Connections" to link them
    #    to all relevant PivotTables (e.g., Profit by Country/Cookie, Units sold each month, Profit by month).
    # 6. Customize Slicer/Timeline styles using "Slicer Tools" / "Timeline Tools" tabs to match the dashboard theme.

    # Final cleanup: Hide data sheets and pivot table sheets
    ws_data.sheet_state = 'hidden'
    # In a full implementation, sheets for pivot tables would also be hidden.

    # Remove the default created sheet if it's empty
    if 'Sheet' in wb.sheetnames and wb['Sheet'].max_row == 1 and wb['Sheet'].max_column == 1:
        wb.remove(wb['Sheet'])

```