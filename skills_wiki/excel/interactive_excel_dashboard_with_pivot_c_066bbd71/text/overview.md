### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Excel Dashboard with Pivot Charts and Slicers

*   **Tier**: archetype
*   **Core Mechanism**: This skill constructs a dynamic and interactive performance dashboard using standard Excel features. It involves structuring raw data into an Excel Table, creating multiple pivot tables to summarize different data dimensions (e.g., profit by country/product, units/profit by month), and visualizing these summaries with various pivot charts. Interactivity is enabled by connecting multiple slicers (for categorical filters) and a timeline (for date filters) to all relevant pivot tables, allowing users to dynamically filter and analyze data.
*   **Applicability**: Ideal for business users to quickly build powerful, self-updating dashboards for reporting and analysis. Suitable for datasets with transactional records, time-series data, and multiple categorical dimensions where quick filtering, trend analysis, and comparative views are crucial for decision-making. Eliminates the need for VBA or add-ins.

### 2. Structural Breakdown

-   **Data Layout**:
    *   **`Data` Sheet**: Contains the raw transactional data in an Excel Table (e.g., "SalesData"). Columns include `Country`, `Product`, `Units Sold`, `Revenue`, `Cost`, `Profit`, `Date`. This table serves as the source for all pivot tables.
    *   **Hidden Pivot Table Sheets**: Separate worksheets are created (and subsequently hidden) for each pivot table. E.g., "Profit by country and cookie", "Units sold each month", "Profit by month". These sheets hold the pivot tables that feed the dashboard's charts.
    *   **`Dashboard` Sheet**: The main user interface, designed to present pivot charts, slicers, and timelines without Excel's default gridlines or headings.
-   **Formula Logic**: Primarily relies on Excel's native PivotTable calculations (e.g., SUM). Dates are grouped by 'Months' within the pivot tables for time-series analysis. No complex custom formulas are introduced directly on the dashboard.
-   **Visual Design**:
    *   **Dashboard Header**: A merged cell at the top of the `Dashboard` sheet acts as a prominent title, styled with a solid background color and contrasting bold text.
    *   **Theming**: The entire workbook's visual style (colors, fonts, effects) can be quickly changed using `Page Layout > Themes` to match organizational branding.
    *   **Clean Interface**: Gridlines and row/column headings are hidden on the `Dashboard` sheet for a professional, uncluttered look.
    *   **Number Formatting**: Currency and comma styles are applied to numeric values within pivot tables and charts, often with zero decimal places for readability.
-   **Charts/Tables**:
    *   **Pivot Table 1 (Profit by Market & Cookie Type)**: `Country` in Rows, `Product` in Columns, `SUM of Profit` in Values. Rows and Columns are sorted by Grand Total.
    *   **Pivot Chart 1**: Stacked Column Chart, linked to Pivot Table 1. Displays "Profit by Market & Cookie Type". Field buttons are hidden for cleaner presentation.
    *   **Pivot Table 2 (Units Sold Each Month)**: `Date` (grouped by Months) in Rows, `SUM of Units Sold` in Values.
    *   **Pivot Chart 2**: Line Chart, linked to Pivot Table 2. Displays "Units sold each month". Legend and field buttons are hidden.
    *   **Pivot Table 3 (Profit by Month)**: `Date` (grouped by Months) in Rows, `SUM of Profit` in Values.
    *   **Pivot Chart 3**: Line Chart, linked to Pivot Table 3. Displays "Profit by month". Legend and field buttons are hidden.
    *   **Slicers**: Interactive filter controls for `Country` and `Product`. Headers are hidden, and their sizes are adjusted to fit the available space.
    *   **Timeline**: An interactive date filter for the `Date` field, used to dynamically select time periods.
    *   **Alignment**: Charts and slicers are precisely aligned on the dashboard using Excel's alignment tools and specific height/width settings.
-   **Theme Hooks**: `header_bg` and `header_fg` for the dashboard title. `body_bg` and `body_fg` for general sheet background and text. `accent_1` (and others as needed) for slicer button fills and chart series colors, derived from the selected workbook theme.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.pivot.table import PivotTable, PivotCacheDefinition
from openpyxl.pivot.field import PivotField, DataField

# Helper function to get theme colors (simplified)
def _get_theme_colors(theme_name: str):
    # In a full openpyxl setup, this would load colors from a theme file.
    # For this skill, we provide a basic set of colors based on common Excel themes.
    palettes = {
        "corporate_blue": {
            "header_bg": "FF1E3F66", # Dark blue
            "header_fg": "FFFFFFFF", # White
            "body_bg": "FFFFFFFF",   # White
            "body_fg": "FF000000",   # Black
            "accent_1": "FF4F81BD",  # Blue
            "accent_2": "FFC0504D",  # Red
            "accent_3": "FF9BBB59",  # Green
            "accent_4": "FF8064A2",  # Purple
            "accent_5": "FFF79646",  # Orange
            "accent_6": "FF00B0F0",  # Light Blue
            "gridline": "FFD9D9D9",  # Light grey
        },
        "green_theme": { # Example based on a video theme variant
            "header_bg": "FF6AAA4C", # Green
            "header_fg": "FFFFFFFF", # White
            "body_bg": "FFFFFFFF",   # White
            "body_fg": "FF000000",   # Black
            "accent_1": "FF4F81BD",  # Blue (default chart color)
            "accent_2": "FFC0504D",
            "accent_3": "FF9BBB59",
            "accent_4": "FF8064A2",
            "accent_5": "FFF79646",
            "accent_6": "FF00B0F0",
            "gridline": "FFD9D9D9",
        },
        "maroon_theme": { # Example based on a video theme variant
            "header_bg": "FF800000", # Maroon
            "header_fg": "FFFFFFFF", # White
            "body_bg": "FFFFFFFF",   # White
            "body_fg": "FF000000",   # Black
            "accent_1": "FF4F81BD",  # Blue (default chart color)
            "accent_2": "FFC0504D",
            "accent_3": "FF9BBB59",
            "accent_4": "FF8064A2",
            "accent_5": "FFF79646",
            "accent_6": "FF00B0F0",
            "gridline": "FFD9D9D9",
        }
    }
    return palettes.get(theme_name, palettes["corporate_blue"])

def _set_cell_style(cell, font_name="Calibri", font_size=11, bold=False, fill_color=None, font_color=None, alignment_h='left', alignment_v='center', wrap_text=False, number_format=None):
    cell.font = Font(name=font_name, size=font_size, bold=bold, color=font_color)
    if fill_color:
        cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    cell.alignment = Alignment(horizontal=alignment_h, vertical=alignment_v, wrap_text=wrap_text)
    if number_format:
        cell.number_format = number_format

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    colors = _get_theme_colors(theme)

    # Remove default sheet if it exists
    if 'Sheet' in wb.sheetnames:
        del wb['Sheet']

    # --- 1. Raw Data Sheet ---
    data_ws = wb.create_sheet("Data", 0) # Create as first sheet
    raw_data = [
        ["Country", "Product", "Units Sold", "Revenue", "Cost", "Profit", "Date"],
        ["India", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, "2019-11-01"],
        ["India", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, "2019-12-01"],
        ["India", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, "2019-09-01"],
        ["India", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, "2019-10-01"],
        ["India", "Chocolate Chip", 1389, 6945.00, 2778.00, 4167.00, "2019-10-01"],
        ["India", "Chocolate Chip", 1802, 9010.00, 3604.00, 5406.00, "2019-12-01"],
        ["India", "Chocolate Chip", 2299, 11495.00, 4598.00, 6897.00, "2019-11-01"],
        ["India", "Chocolate Chip", 1404, 7020.00, 2808.00, 4212.00, "2019-09-01"],
        ["India", "Chocolate Chip", 2470, 12350.00, 4940.00, 7410.00, "2019-10-01"],
        ["India", "Chocolate Chip", 1743, 8715.00, 3486.00, 5229.00, "2019-11-01"],
        ["India", "Chocolate Chip", 2222, 11110.00, 4444.00, 6666.00, "2019-11-01"],
        ["India", "Fortune Cookie", 345, 345.00, 69.00, 276.00, "2019-10-01"],
        ["India", "Fortune Cookie", 572, 572.00, 114.40, 457.60, "2019-11-01"],
        ["India", "Fortune Cookie", 1611, 1611.00, 322.20, 1288.80, "2019-10-01"],
        ["India", "Fortune Cookie", 1933, 1933.00, 386.60, 1546.40, "2019-09-01"],
        ["India", "Fortune Cookie", 1235, 1235.00, 247.00, 988.00, "2019-12-01"],
        ["India", "Fortune Cookie", 1523, 1523.00, 304.60, 1218.40, "2019-11-01"],
        ["India", "Oatmeal Raisin", 2128, 10640.00, 4256.00, 6384.00, "2019-12-01"],
        ["India", "Oatmeal Raisin", 425, 2125.00, 850.00, 1275.00, "2019-10-01"],
        ["India", "Oatmeal Raisin", 2200, 11000.00, 4400.00, 6600.00, "2019-09-01"],
        ["India", "Oatmeal Raisin", 1753, 8765.00, 3506.00, 5259.00, "2019-11-01"],
        ["India", "Oatmeal Raisin", 2102, 10510.00, 4204.00, 6306.00, "2019-10-01"],
        ["India", "Oatmeal Raisin", 1680, 8400.00, 3360.00, 5040.00, "2019-12-01"],
        ["India", "Snickerdoodle", 2508, 12540.00, 5016.00, 7524.00, "2019-11-01"],
        ["India", "Snickerdoodle", 2055, 10275.00, 4110.00, 6165.00, "2019-10-01"],
        ["India", "Snickerdoodle", 2567, 12835.00, 5134.00, 7701.00, "2019-12-01"],
        ["India", "Snickerdoodle", 831, 4155.00, 1662.00, 2493.00, "2019-09-01"],
        ["India", "Snickerdoodle", 1856, 9280.00, 3712.00, 5568.00, "2019-11-01"],
        ["India", "Snickerdoodle", 25085, 125425.00, 50170.00, 75255.00, "2019-11-01"],
        ["India", "Sugar", 18560, 92800.00, 37120.00, 55680.00, "2019-12-01"],
        ["India", "Sugar", 1063, 5315.00, 2126.00, 3189.00, "2019-10-01"],
        ["India", "Sugar", 1806, 9030.00, 3612.00, 5418.00, "2019-09-01"],
        ["India", "Sugar", 18561, 92805.00, 37122.00, 55683.00, "2019-11-01"],
        ["India", "Sugar", 14947, 74735.00, 29894.00, 44841.00, "2019-11-01"],
        ["India", "White Chocolate Macadamia Nut", 23621, 118105.00, 47242.00, 70863.00, "2019-12-01"],
        ["India", "White Chocolate Macadamia Nut", 20452, 102260.00, 40904.00, 61356.00, "2019-11-01"],
        ["India", "White Chocolate Macadamia Nut", 24567, 122835.00, 49134.00, 73701.00, "2019-09-01"],
        ["India", "White Chocolate Macadamia Nut", 26731, 133655.00, 53462.00, 80193.00, "2019-10-01"],
        ["India", "White Chocolate Macadamia Nut", 32910, 164550.00, 65820.00, 98730.00, "2019-11-01"],

        ["Malaysia", "Chocolate Chip", 2299, 11495.00, 4598.00, 6897.00, "2019-11-01"],
        ["Malaysia", "Chocolate Chip", 1802, 9010.00, 3604.00, 5406.00, "2019-12-01"],
        ["Malaysia", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, "2019-10-01"],
        ["Malaysia", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, "2019-09-01"],
        ["Malaysia", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, "2019-11-01"],
        ["Malaysia", "Fortune Cookie", 1235, 1235.00, 247.00, 988.00, "2019-10-01"],
        ["Malaysia", "Fortune Cookie", 1611, 1611.00, 322.20, 1288.80, "2019-09-01"],
        ["Malaysia", "Fortune Cookie", 345, 345.00, 69.00, 276.00, "2019-11-01"],
        ["Malaysia", "Fortune Cookie", 572, 572.00, 114.40, 457.60, "2019-12-01"],
        ["Malaysia", "Fortune Cookie", 1523, 1523.00, 304.60, 1218.40, "2019-11-01"],
        ["Malaysia", "Oatmeal Raisin", 2102, 10510.00, 4204.00, 6306.00, "2019-12-01"],
        ["Malaysia", "Oatmeal Raisin", 2200, 11000.00, 4400.00, 6600.00, "2019-11-01"],
        ["Malaysia", "Oatmeal Raisin", 1680, 8400.00, 3360.00, 5040.00, "2019-09-01"],
        ["Malaysia", "Oatmeal Raisin", 425, 2125.00, 850.00, 1275.00, "2019-10-01"],
        ["Malaysia", "Oatmeal Raisin", 2128, 10640.00, 4256.00, 6384.00, "2019-10-01"],
        ["Malaysia", "Snickerdoodle", 831, 4155.00, 1662.00, 2493.00, "2019-12-01"],
        ["Malaysia", "Snickerdoodle", 1856, 9280.00, 3712.00, 5568.00, "2019-11-01"],
        ["Malaysia", "Snickerdoodle", 2508, 12540.00, 5016.00, 7524.00, "2019-10-01"],
        ["Malaysia", "Snickerdoodle", 2055, 10275.00, 4110.00, 6165.00, "2019-09-01"],
        ["Malaysia", "Snickerdoodle", 2567, 12835.00, 5134.00, 7701.00, "2019-10-01"],
        ["Malaysia", "Sugar", 1063, 5315.00, 2126.00, 3189.00, "2019-12-01"],
        ["Malaysia", "Sugar", 1806, 9030.00, 3612.00, 5418.00, "2019-11-01"],
        ["Malaysia", "Sugar", 18560, 92800.00, 37120.00, 55680.00, "2019-10-01"],
        ["Malaysia", "Sugar", 14947, 74735.00, 29894.00, 44841.00, "2019-09-01"],
        ["Malaysia", "Sugar", 18561, 92805.00, 37122.00, 55683.00, "2019-11-01"],
        ["Malaysia", "White Chocolate Macadamia Nut", 24567, 122835.00, 49134.00, 73701.00, "2019-12-01"],
        ["Malaysia", "White Chocolate Macadamia Nut", 20452, 102260.00, 40904.00, 61356.00, "2019-11-01"],
        ["Malaysia", "White Chocolate Macadamia Nut", 26731, 133655.00, 53462.00, 80193.00, "2019-10-01"],
        ["Malaysia", "White Chocolate Macadamia Nut", 23621, 118105.00, 47242.00, 70863.00, "2019-09-01"],
        ["Malaysia", "White Chocolate Macadamia Nut", 32910, 164550.00, 65820.00, 98730.00, "2019-11-01"],

        ["Philippines", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, "2019-11-01"],
        ["Philippines", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, "2019-10-01"],
        ["Philippines", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, "2019-09-01"],
        ["Philippines", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, "2019-12-01"],
        ["Philippines", "Chocolate Chip", 1802, 9010.00, 3604.00, 5406.00, "2019-11-01"],
        ["Philippines", "Fortune Cookie", 345, 345.00, 69.00, 276.00, "2019-11-01"],
        ["Philippines", "Fortune Cookie", 572, 572.00, 114.40, 457.60, "2019-10-01"],
        ["Philippines", "Fortune Cookie", 1611, 1611.00, 322.20, 1288.80, "2019-09-01"],
        ["Philippines", "Fortune Cookie", 1933, 1933.00, 386.60, 1546.40, "2019-12-01"],
        ["Philippines", "Fortune Cookie", 1235, 1235.00, 247.00, 988.00, "2019-11-01"],
        ["Philippines", "Oatmeal Raisin", 2128, 10640.00, 4256.00, 6384.00, "2019-11-01"],
        ["Philippines", "Oatmeal Raisin", 425, 2125.00, 850.00, 1275.00, "2019-10-01"],
        ["Philippines", "Oatmeal Raisin", 2200, 11000.00, 4400.00, 6600.00, "2019-09-01"],
        ["Philippines", "Oatmeal Raisin", 1753, 8765.00, 3506.00, 5259.00, "2019-12-01"],
        ["Philippines", "Oatmeal Raisin", 2102, 10510.00, 4204.00, 6306.00, "2019-11-01"],
        ["Philippines", "Snickerdoodle", 2508, 12540.00, 5016.00, 7524.00, "2019-12-01"],
        ["Philippines", "Snickerdoodle", 2055, 10275.00, 4110.00, 6165.00, "2019-11-01"],
        ["Philippines", "Snickerdoodle", 2567, 12835.00, 5134.00, 7701.00, "2019-10-01"],
        ["Philippines", "Snickerdoodle", 831, 4155.00, 1662.00, 2493.00, "2019-09-01"],
        ["Philippines", "Snickerdoodle", 1856, 9280.00, 3712.00, 5568.00, "2019-10-01"],
        ["Philippines", "Sugar", 1063, 5315.00, 2126.00, 3189.00, "2019-11-01"],
        ["Philippines", "Sugar", 1806, 9030.00, 3612.00, 5418.00, "2019-10-01"],
        ["Philippines", "Sugar", 18560, 92800.00, 37120.00, 55680.00, "2019-09-01"],
        ["Philippines", "Sugar", 14947, 74735.00, 29894.00, 44841.00, "2019-12-01"],
        ["Philippines", "Sugar", 18561, 92805.00, 37122.00, 55683.00, "2019-11-01"],
        ["Philippines", "White Chocolate Macadamia Nut", 24567, 122835.00, 49134.00, 73701.00, "2019-11-01"],
        ["Philippines", "White Chocolate Macadamia Nut", 20452, 102260.00, 40904.00, 61356.00, "2019-10-01"],
        ["Philippines", "White Chocolate Macadamia Nut", 26731, 133655.00, 53462.00, 80193.00, "2019-09-01"],
        ["Philippines", "White Chocolate Macadamia Nut", 23621, 118105.00, 47242.00, 70863.00, "2019-12-01"],
        ["Philippines", "White Chocolate Macadamia Nut", 32910, 164550.00, 65820.00, 98730.00, "2019-11-01"],

        ["United Kingdom", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, "2019-12-01"],
        ["United Kingdom", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, "2019-11-01"],
        ["United Kingdom", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, "2019-10-01"],
        ["United Kingdom", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, "2019-09-01"],
        ["United Kingdom", "Chocolate Chip", 1802, 9010.00, 3604.00, 5406.00, "2019-12-01"],
        ["United Kingdom", "Fortune Cookie", 345, 345.00, 69.00, 276.00, "2019-12-01"],
        ["United Kingdom", "Fortune Cookie", 572, 572.00, 114.40, 457.60, "2019-11-01"],
        ["United Kingdom", "Fortune Cookie", 1611, 1611.00, 322.20, 1288.80, "2019-10-01"],
        ["United Kingdom", "Fortune Cookie", 1933, 1933.00, 386.60, 1546.40, "2019-09-01"],
        ["United Kingdom", "Fortune Cookie", 1235, 1235.00, 247.00, 988.00, "2019-12-01"],
        ["United Kingdom", "Oatmeal Raisin", 2128, 10640.00, 4256.00, 6384.00, "2019-12-01"],
        ["United Kingdom", "Oatmeal Raisin", 425, 2125.00, 850.00, 1275.00, "2019-11-01"],
        ["United Kingdom", "Oatmeal Raisin", 2200, 11000.00, 4400.00, 6600.00, "2019-10-01"],
        ["United Kingdom", "Oatmeal Raisin", 1753, 8765.00, 3506.00, 5259.00, "2019-09-01"],
        ["United Kingdom", "Oatmeal Raisin", 2102, 10510.00, 4204.00, 6306.00, "2019-12-01"],
        ["United Kingdom", "Snickerdoodle", 2508, 12540.00, 5016.00, 7524.00, "2019-11-01"],
        ["United Kingdom", "Snickerdoodle", 2055, 10275.00, 4110.00, 6165.00, "2019-10-01"],
        ["United Kingdom", "Snickerdoodle", 2567, 12835.00, 5134.00, 7701.00, "2019-09-01"],
        ["United Kingdom", "Snickerdoodle", 831, 4155.00, 1662.00, 2493.00, "2019-12-01"],
        ["United Kingdom", "Snickerdoodle", 1856, 9280.00, 3712.00, 5568.00, "2019-11-01"],
        ["United Kingdom", "Sugar", 1063, 5315.00, 2126.00, 3189.00, "2019-12-01"],
        ["United Kingdom", "Sugar", 1806, 9030.00, 3612.00, 5418.00, "2019-11-01"],
        ["United Kingdom", "Sugar", 18560, 92800.00, 37120.00, 55680.00, "2019-10-01"],
        ["United Kingdom", "Sugar", 14947, 74735.00, 29894.00, 44841.00, "2019-09-01"],
        ["United Kingdom", "Sugar", 18561, 92805.00, 37122.00, 55683.00, "2019-12-01"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 24567, 122835.00, 49134.00, 73701.00, "2019-10-01"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 20452, 102260.00, 40904.00, 61356.00, "2019-09-01"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 26731, 133655.00, 53462.00, 80193.00, "2019-12-01"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 23621, 118105.00, 47242.00, 70863.00, "2019-11-01"],
        ["United Kingdom", "White Chocolate Macadamia Nut", 32910, 164550.00, 65820.00, 98730.00, "2019-12-01"],

        ["United States", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, "2019-10-01"],
        ["United States", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, "2019-09-01"],
        ["United States", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, "2019-12-01"],
        ["United States", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, "2019-11-01"],
        ["United States", "Chocolate Chip", 1802, 9010.00, 3604.00, 5406.00, "2019-10-01"],
        ["United States", "Fortune Cookie", 345, 345.00, 69.00, 276.00, "2019-09-01"],
        ["United States", "Fortune Cookie", 572, 572.00, 114.40, 457.60, "2019-12-01"],
        ["United States", "Fortune Cookie", 1611, 1611.00, 322.20, 1288.80, "2019-11-01"],
        ["United States", "Fortune Cookie", 1933, 1933.00, 386.60, 1546.40, "2019-10-01"],
        ["United States", "Fortune Cookie", 1235, 1235.00, 247.00, 988.00, "2019-09-01"],
        ["United States", "Oatmeal Raisin", 2128, 10640.00, 4256.00, 6384.00, "2019-10-01"],
        ["United States", "Oatmeal Raisin", 425, 2125.00, 850.00, 1275.00, "2019-09-01"],
        ["United States", "Oatmeal Raisin", 2200, 11000.00, 4400.00, 6600.00, "2019-12-01"],
        ["United States", "Oatmeal Raisin", 1753, 8765.00, 3506.00, 5259.00, "2019-11-01"],
        ["United States", "Oatmeal Raisin", 2102, 10510.00, 4204.00, 6306.00, "2019-10-01"],
        ["United States", "Snickerdoodle", 2508, 12540.00, 5016.00, 7524.00, "2019-09-01"],
        ["United States", "Snickerdoodle", 2055, 10275.00, 4110.00, 6165.00, "2019-12-01"],
        ["United States", "Snickerdoodle", 2567, 12835.00, 5134.00, 7701.00, "2019-11-01"],
        ["United States", "Snickerdoodle", 831, 4155.00, 1662.00, 2493.00, "2019-10-01"],
        ["United States", "Snickerdoodle", 1856, 9280.00, 3712.00, 5568.00, "2019-09-01"],
        ["United States", "Sugar", 1063, 5315.00, 2126.00, 3189.00, "2019-10-01"],
        ["United States", "Sugar", 1806, 9030.00, 3612.00, 5418.00, "2019-09-01"],
        ["United States", "Sugar", 18560, 92800.00, 37120.00, 55680.00, "2019-12-01"],
        ["United States", "Sugar", 14947, 74735.00, 29894.00, 44841.00, "2019-11-01"],
        ["United States", "Sugar", 18561, 92805.00, 37122.00, 55683.00, "2019-10-01"],
        ["United States", "White Chocolate Macadamia Nut", 24567, 122835.00, 49134.00, 73701.00, "2019-09-01"],
        ["United States", "White Chocolate Macadamia Nut", 20452, 102260.00, 40904.00, 61356.00, "2019-12-01"],
        ["United States", "White Chocolate Macadamia Nut", 26731, 133655.00, 53462.00, 80193.00, "2019-11-01"],
        ["United States", "White Chocolate Macadamia Nut", 23621, 118105.00, 47242.00, 70863.00, "2019-10-01"],
        ["United States", "White Chocolate Macadamia Nut", 32910, 164550.00, 65820.00, 98730.00, "2019-09-01"],
        ["United States", "Chocolate Chip", 292, 1460.00, 584.00, 876.00, "2020-02-01"], # New Data for 2020
        ["United States", "Chocolate Chip", 2518, 12590.00, 5036.00, 7554.00, "2020-01-01"],
        ["United States", "Chocolate Chip", 1817, 9085.00, 3634.00, 5451.00, "2020-12-01"],
        ["United States", "Chocolate Chip", 2363, 11815.00, 4726.00, 7089.00, "2020-02-01"],
        ["United States", "Chocolate Chip", 1295, 6475.00, 2590.00, 3885.00, "2020-01-01"],
        ["United States", "Chocolate Chip", 2567, 7701.00, 3208.75, 4492.25, "2020-08-01"],
        ["United States", "Chocolate Chip", 1010, 3030.00, 1262.50, 1767.50, "2020-10-01"],
        ["United States", "Chocolate Chip", 1806, 5418.00, 2257.50, 3160.50, "2020-01-01"],
        ["United States", "Chocolate Chip", 2294, 6882.00, 2867.50, 4014.50, "2020-07-01"],
        ["United States", "Chocolate Chip", 267, 801.00, 333.75, 467.25, "2020-10-01"],
        ["United States", "Chocolate Chip", 663, 3978.00, 1657.50, 2320.50, "2020-03-01"],
        ["United States", "Chocolate Chip", 736, 4416.00, 1840.00, 2576.00, "2020-05-01"],
        ["United States", "Chocolate Chip", 1421, 8526.00, 3552.50, 4973.50, "2020-08-01"],
        ["United States", "Chocolate Chip", 2294, 13764.00, 5735.00, 8029.00, "2020-07-01"],
        ["United States", "Chocolate Chip", 1680, 10080.00, 4200.00, 5880.00, "2020-06-01"],
        ["United States", "Chocolate Chip", 2574, 15444.00, 6435.00, 9009.00, "2020-04-01"],
        ["United States", "Chocolate Chip", 2438, 14628.00, 6095.00, 8533.00, "2020-11-01"],
        ["United States", "Chocolate Chip", 1790, 8950.00, 3580.00, 5370.00, "2020-12-01"],
        ["United States", "Chocolate Chip", 986, 5916.00, 2465.00, 3451.00, "2020-01-01"],
        ["United States", "Chocolate Chip", 1596, 9576.00, 3990.00, 5586.00, "2020-07-01"],
        ["United States", "Chocolate Chip", 2907, 14535.00, 5814.00, 8721.00, "2020-12-01"],
        ["United States", "Chocolate Chip", 790, 3950.00, 1580.00, 2370.00, "2020-08-01"],
        ["United States", "Chocolate Chip", 606, 3030.00, 1212.00, 1818.00, "2020-06-01"],
        ["United States", "Chocolate Chip", 2460, 12300.00, 4920.00, 7380.00, "2020-05-01"],
        ["United States", "Chocolate Chip", 914, 4570.00, 1828.00, 2742.00, "2020-04-01"],
        ["United States", "Chocolate Chip", 290, 1450.00, 580.00, 870.00, "2020-03-01"],
        ["United States", "Fortune Cookie", 2567, 7701.00, 3208.75, 4492.25, "2020-11-01"],
        ["United States", "Fortune Cookie", 1010, 3030.00, 1262.50, 1767.50, "2020-10-01"],
        ["United States", "Fortune Cookie", 1806, 5418.00, 2257.50, 3160.50, "2020-01-01"],
        ["United States", "Fortune Cookie", 2294, 6882.00, 2867.50, 4014.50, "2020-07-01"],
        ["United States", "Fortune Cookie", 267, 801.00, 333.75, 467.25, "2020-10-01"],
        ["United States", "Fortune Cookie", 663, 3978.00, 1657.50, 2320.50, "2020-03-01"],
        ["United States", "Fortune Cookie", 736, 4416.00, 1840.00, 2576.00, "2020-05-01"],
        ["United States", "Fortune Cookie", 1421, 8526.00, 3552.50, 4973.50, "2020-08-01"],
        ["United States", "Fortune Cookie", 2294, 13764.00, 5735.00, 8029.00, "2020-07-01"],
        ["United States", "Fortune Cookie", 1680, 10080.00, 4200.00, 5880.00, "2020-06-01"],
        ["United States", "Fortune Cookie", 2574, 15444.00, 6435.00, 9009.00, "2020-04-01"],
        ["United States", "Fortune Cookie", 2438, 14628.00, 6095.00, 8533.00, "2020-11-01"],
        ["United States", "Oatmeal Raisin", 2567, 7701.00, 3208.75, 4492.25, "2020-11-01"],
        ["United States", "Oatmeal Raisin", 1010, 3030.00, 1262.50, 1767.50, "2020-10-01"],
        ["United States", "Oatmeal Raisin", 1806, 5418.00, 2257.50, 3160.50, "2020-01-01"],
        ["United States", "Oatmeal Raisin", 2294, 6882.00, 2867.50, 4014.50, "2020-07-01"],
        ["United States", "Oatmeal Raisin", 267, 801.00, 333.75, 467.25, "2020-10-01"],
        ["United States", "Oatmeal Raisin", 663, 3978.00, 1657.50, 2320.50, "2020-03-01"],
        ["United States", "Oatmeal Raisin", 736, 4416.00, 1840.00, 2576.00, "2020-05-01"],
        ["United States", "Oatmeal Raisin", 1421, 8526.00, 3552.50, 4973.50, "2020-08-01"],
        ["United States", "Oatmeal Raisin", 2294, 13764.00, 5735.00, 8029.00, "2020-07-01"],
        ["United States", "Oatmeal Raisin", 1680, 10080.00, 4200.00, 5880.00, "2020-06-01"],
        ["United States", "Oatmeal Raisin", 2574, 15444.00, 6435.00, 9009.00, "2020-04-01"],
        ["United States", "Oatmeal Raisin", 2438, 14628.00, 6095.00, 8533.00, "2020-11-01"],
        ["United States", "Snickerdoodle", 2567, 7701.00, 3208.75, 4492.25, "2020-11-01"],
        ["United States", "Snickerdoodle", 1010, 3030.00, 1262.50, 1767.50, "2020-10-01"],
        ["United States", "Snickerdoodle", 1806, 5418.00, 2257.50, 3160.50, "2020-01-01"],
        ["United States", "Snickerdoodle", 2294, 6882.00, 2867.50, 4014.50, "2020-07-01"],
        ["United States", "Snickerdoodle", 267, 801.00, 333.75, 467.25, "2020-10-01"],
        ["United States", "Snickerdoodle", 663, 3978.00, 1657.50, 2320.50, "2020-03-01"],
        ["United States", "Snickerdoodle", 736, 4416.00, 1840.00, 2576.00, "2020-05-01"],
        ["United States", "Snickerdoodle", 1421, 8526.00, 3552.50, 4973.50, "2020-08-01"],
        ["United States", "Snickerdoodle", 2294, 13764.00, 5735.00, 8029.00, "2020-07-01"],
        ["United States", "Snickerdoodle", 1680, 10080.00, 4200.00, 5880.00, "2020-06-01"],
        ["United States", "Snickerdoodle", 2574, 15444.00, 6435.00, 9009.00, "2020-04-01"],
        ["United States", "Snickerdoodle", 2438, 14628.00, 6095.00, 8533.00, "2020-11-01"],
        ["United States", "Sugar", 2567, 7701.00, 3208.75, 4492.25, "2020-11-01"],
        ["United States", "Sugar", 1010, 3030.00, 1262.50, 1767.50, "2020-10-01"],
        ["United States", "Sugar", 1806, 5418.00, 2257.50, 3160.50, "2020-01-01"],
        ["United States", "Sugar", 2294, 6882.00, 2867.50, 4014.50, "2020-07-01"],
        ["United States", "Sugar", 267, 801.00, 333.75, 467.25, "2020-10-01"],
        ["United States", "Sugar", 663, 3978.00, 1657.50, 2320.50, "2020-03-01"],
        ["United States", "Sugar", 736, 4416.00, 1840.00, 2576.00, "2020-05-01"],
        ["United States", "Sugar", 1421, 8526.00, 3552.50, 4973.50, "2020-08-01"],
        ["United States", "Sugar", 2294, 13764.00, 5735.00, 8029.00, "2020-07-01"],
        ["United States", "Sugar", 1680, 10080.00, 4200.00, 5880.00, "2020-06-01"],
        ["United States", "Sugar", 2574, 15444.00, 6435.00, 9009.00, "2020-04-01"],
        ["United States", "Sugar", 2438, 14628.00, 6095.00, 8533.00, "2020-11-01"],
        ["United States", "White Chocolate Macadamia Nut", 2567, 7701.00, 3208.75, 4492.25, "2020-11-01"],
        ["United States", "White Chocolate Macadamia Nut", 1010, 3030.00, 1262.50, 1767.50, "2020-10-01"],
        ["United States", "White Chocolate Macadamia Nut", 1806, 5418.00, 2257.50, 3160.50, "2020-01-01"],
        ["United States", "White Chocolate Macadamia Nut", 2294, 6882.00, 2867.50, 4014.50, "2020-07-01"],
        ["United States", "White Chocolate Macadamia Nut", 267, 801.00, 333.75, 467.25, "2020-10-01"],
        ["United States", "White Chocolate Macadamia Nut", 663, 3978.00, 1657.50, 2320.50, "2020-03-01"],
        ["United States", "White Chocolate Macadamia Nut", 736, 4416.00, 1840.00, 2576.00, "2020-05-01"],
        ["United States", "White Chocolate Macadamia Nut", 1421, 8526.00, 3552.50, 4973.50, "2020-08-01"],
        ["United States", "White Chocolate Macadamia Nut", 2294, 13764.00, 5735.00, 8029.00, "2020-07-01"],
        ["United States", "White Chocolate Macadamia Nut", 1680, 10080.00, 4200.00, 5880.00, "2020-06-01"],
        ["United States", "White Chocolate Macadamia Nut", 2574, 15444.00, 6435.00, 9009.00, "2020-04-01"],
        ["United States", "White Chocolate Macadamia Nut", 2438, 14628.00, 6095.00, 8533.00, "2020-11-01"],
    ]
    for row_data in raw_data:
        data_ws.append(row_data)

    # Convert raw data to an Excel Table
    table_ref = f"A1:{get_column_letter(len(raw_data[0]))}{len(raw_data)}"
    data_table = Table(displayName="SalesData", ref=table_ref)
    data_table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False,
                                            showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    data_ws.add_table(data_table)

    # --- 2. Create Pivot Table Sheets ---
    # Sheet for Profit by Market & Cookie Type
    pivot_sheet_profit_country_cookie = wb.create_sheet("Profit by country and cookie", 1)
    pt_cache = wb.create_pivot_cache(data_ws, data_table.ref)
    pt_pcc = PivotTable(
        cache=pt_cache,
        pivot_fields=[
            PivotField(compact=False, axis='row', field='Country', all_items_visible=False),
            PivotField(compact=False, axis='column', field='Product', all_items_visible=False)
        ],
        data_fields=[DataField(field='Profit', fld_fmt="$#,##0;($#,##0)", baseField='(none)', subtotal='sum', showDataAs='normal')],
        location="A3",
        name="PivotTablePCC"
    )
    pivot_sheet_profit_country_cookie.add_pivot(pt_pcc)

    # Sheet for Units Sold Each Month
    pivot_sheet_units_sold = wb.create_sheet("Units sold each month", 2)
    pt_cache_units = wb.create_pivot_cache(data_ws, data_table.ref)
    pt_units = PivotTable(
        cache=pt_cache_units,
        pivot_fields=[
            PivotField(compact=False, axis='row', field='Date', autoGroup=True, all_items_visible=False),
        ],
        data_fields=[DataField(field='Units Sold', fld_fmt="#,##0", baseField='(none)', subtotal='sum', showDataAs='normal')],
        location="A3",
        name="PivotTableUnits"
    )
    pivot_sheet_units_sold.add_pivot(pt_units)

    # Sheet for Profit by Month
    pivot_sheet_profit_month = wb.create_sheet("Profit by month", 3)
    pt_cache_profit = wb.create_pivot_cache(data_ws, data_table.ref)
    pt_profit = PivotTable(
        cache=pt_cache_profit,
        pivot_fields=[
            PivotField(compact=False, axis='row', field='Date', autoGroup=True, all_items_visible=False),
        ],
        data_fields=[DataField(field='Profit', fld_fmt="$#,##0;($#,##0)", baseField='(none)', subtotal='sum', showDataAs='normal')],
        location="A3",
        name="PivotTableProfit"
    )
    pivot_sheet_profit_month.add_pivot(pt_profit)

    # --- 3. Dashboard Sheet ---
    dashboard_ws = wb.create_sheet("Dashboard", 0) # Create as first sheet again, so it's active
    
    # Header section
    dashboard_ws.merge_cells('A1:Q6')
    header_cell = dashboard_ws['A1']
    _set_cell_style(header_cell, font_name="Calibri", font_size=24, bold=True,
                    fill_color=colors["header_bg"], font_color=colors["header_fg"],
                    alignment_h='center', alignment_v='center')
    header_cell.value = "KEVIN COOKIE COMPANY Performance Dashboard"

    # Placeholder for cookie image
    dashboard_ws['B3'].value = "🍪"
    _set_cell_style(dashboard_ws['B3'], font_size=36, alignment_h='center', alignment_v='center')
    
    # Chart 1: Profit by Market & Cookie Type (Stacked Column)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Profit by Market & Cookie Type"
    chart1.y_axis.title = "$"
    chart1.x_axis.delete = True
    chart1.y_axis.delete = True
    chart1.height = 4.18
    chart1.width = 6

    data_ref_pcc = Reference(pivot_sheet_profit_country_cookie, min_col=2, min_row=3, max_col=pivot_sheet_profit_country_cookie.max_column-1, max_row=pivot_sheet_profit_country_cookie.max_row-1)
    cats_ref_pcc = Reference(pivot_sheet_profit_country_cookie, min_col=1, min_row=4, max_row=pivot_sheet_profit_country_cookie.max_row-1)
    chart1.add_data(data_ref_pcc, titles_from_data=True)
    chart1.set_categories(cats_ref_pcc)
    
    dashboard_ws.add_chart(chart1, "D8")


    # Chart 2: Units Sold Each Month (Line Chart)
    chart2 = LineChart()
    chart2.style = 10
    chart2.title = "Units sold each month"
    chart2.y_axis.title = ""
    chart2.x_axis.title = ""
    chart2.height = 4.18
    chart2.width = 5.5

    data_ref_units = Reference(pivot_sheet_units_sold, min_col=2, min_row=3, max_col=2, max_row=pivot_sheet_units_sold.max_row-1)
    cats_ref_units = Reference(pivot_sheet_units_sold, min_col=1, min_row=4, max_row=pivot_sheet_units_sold.max_row-1)
    chart2.add_data(data_ref_units, titles_from_data=True)
    chart2.set_categories(cats_ref_units)
    
    dashboard_ws.add_chart(chart2, "K8")

    # Chart 3: Profit by Month (Line Chart)
    chart3 = LineChart()
    chart3.style = 10
    chart3.title = "Profit by month"
    chart3.y_axis.title = "$"
    chart3.x_axis.title = ""
    chart3.height = 4.18
    chart3.width = 5.5

    data_ref_profit = Reference(pivot_sheet_profit_month, min_col=2, min_row=3, max_col=2, max_row=pivot_sheet_profit_month.max_row-1)
    cats_ref_profit = Reference(pivot_sheet_profit_month, min_col=1, min_row=4, max_row=pivot_sheet_profit_month.max_row-1)
    chart3.add_data(data_ref_profit, titles_from_data=True)
    chart3.set_categories(cats_ref_profit)
    
    dashboard_ws.add_chart(chart3, "K20")

    # --- Slicers and Timelines (Represented as text/cells as openpyxl doesn't support them directly) ---
    dashboard_ws['A8'].value = "Date"
    dashboard_ws['A9'].value = "All Periods"
    dashboard_ws['A10'].value = "2019"
    dashboard_ws['A11'].value = "OCT  NOV  DEC"
    dashboard_ws['A13'].value = "India"
    dashboard_ws['A14'].value = "Malaysia"
    dashboard_ws['A15'].value = "Philippines"
    dashboard_ws['A16'].value = "United Kingdom"
    dashboard_ws['A17'].value = "United States"
    dashboard_ws['A19'].value = "Chocolate Chip"
    dashboard_ws['A20'].value = "Fortune Cookie"
    dashboard_ws['A21'].value = "Oatmeal Raisin"
    dashboard_ws['A22'].value = "Snickerdoodle"
    dashboard_ws['A23'].value = "Sugar"
    dashboard_ws['A24'].value = "White Chocolate Macadamia Nut"

    # Style slicer-like elements
    _set_cell_style(dashboard_ws['A8'], bold=True)
    for r_idx in range(13, 18):
        _set_cell_style(dashboard_ws[f'A{r_idx}'], fill_color=colors["accent_1"] + '66', font_color=colors["body_fg"])
    for r_idx in range(19, 25):
        _set_cell_style(dashboard_ws[f'A{r_idx}'], fill_color=colors["accent_1"] + '66', font_color=colors["body_fg"])
    
    # Set column widths for aesthetic appeal
    dashboard_ws.column_dimensions['A'].width = 15
    dashboard_ws.column_dimensions['B'].width = 3
    dashboard_ws.column_dimensions['C'].width = 3
    dashboard_ws.column_dimensions['D'].width = 10
    dashboard_ws.column_dimensions['E'].width = 10
    dashboard_ws.column_dimensions['F'].width = 10
    dashboard_ws.column_dimensions['G'].width = 10
    dashboard_ws.column_dimensions['H'].width = 10
    dashboard_ws.column_dimensions['I'].width = 10
    dashboard_ws.column_dimensions['J'].width = 10
    dashboard_ws.column_dimensions['K'].width = 10
    dashboard_ws.column_dimensions['L'].width = 10
    dashboard_ws.column_dimensions['M'].width = 10
    dashboard_ws.column_dimensions['N'].width = 10
    dashboard_ws.column_dimensions['O'].width = 10
    dashboard_ws.column_dimensions['P'].width = 10
    dashboard_ws.column_dimensions['Q'].width = 10


    # Hide gridlines and headings on the dashboard sheet
    dashboard_ws.sheet_view.showGridLines = False
    dashboard_ws.sheet_view.showHeadings = False

    # Hide pivot table source sheets
    data_ws.sheet_state = 'hidden'
    pivot_sheet_profit_country_cookie.sheet_state = 'hidden'
    pivot_sheet_units_sold.sheet_state = 'hidden'
    pivot_sheet_profit_month.sheet_state = 'hidden'

```