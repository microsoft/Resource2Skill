### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Interactive Sales Dashboard

*   **Tier**: archetype
*   **Core Mechanism**: This skill constructs a multi-sheet Excel workbook featuring a central dashboard sheet. It dynamically presents key performance indicators (KPIs) and trend visualizations by leveraging Excel Tables as dynamic data sources, multiple PivotTables for aggregation, and several PivotCharts for visual analysis. Interactive elements like slicers enable drill-down capabilities, while cohesive theme-based styling ensures a professional and unified aesthetic.
*   **Applicability**: This skill is ideal for creating comprehensive, user-friendly, and updateable dashboards for performance tracking in various domains like sales, marketing, and operations. It suits datasets with granular transaction-level detail that require aggregation by categories (e.g., sales agent, time period) and visualization of trends or comparative performance. The design prioritizes interactivity and ease of data refresh.

### 2. Structural Breakdown

-   **Data Layout**:
    -   **Raw Data Sheet (`SalesData`)**: A structured Excel Table (named "SalesData") serving as the data source. Columns include: `Name`, `Date`, `Total Calls`, `Calls Reached`, `Average Duration (sec)`, `Deals Closed`, `Call Conversion Rate (%)`, `Deal Value ($)`, `Call Drop Rate (%)`.
    -   **Analysis Sheet (`Analysis`)**: Houses multiple PivotTables that act as data sources for the dashboard's KPIs and charts.
        -   **PT1 (KPI Summary)**: Summarizes `Total Calls`, `Calls Reached`, `Deals Closed`, `Deal Value ($)` across all data, with values presented in rows (e.g., B4:B7). These cells are referenced by the dashboard's KPI text boxes.
        -   **PT2 (Calls/Deals by Month)**: Summarizes `Sum of Calls Reached` and `Sum of Deals Closed` by `Month` (Date field grouped by month), values in columns. Source for Stacked Column Chart.
        -   **PT3 (Total Sales by Month)**: Summarizes `Sum of Deal Value ($)` by `Month`. Source for Total Sales Column Chart.
        -   **PT4 (Avg Call Duration by Month)**: Summarizes `Average of Average Duration (sec)` by `Month`. Source for Average Call Duration Column Chart.
        -   **PT5 (Avg Call Drop Rate by Month)**: Summarizes `Average of Call Drop Rate (%)` by `Month`. Source for Call Drop Rate Area Chart.
        -   **PT6 (Selected Name)**: A simple PivotTable showing the `Name` selected in the slicer (e.g., Analysis!A11). Used for conditional formatting on the Sales Agent KPIs table.
        -   **PT7 (Sales Agent KPIs Table)**: Summarizes `Total Calls`, `Calls Reached`, `Deals Closed`, `Deal Value ($)` by `Name`, with conditional formatting applied.

-   **Formula Logic**:
    -   **KPI Text Box Values**: Text boxes on the Dashboard sheet are linked directly to cells in PT1 on the "Analysis" sheet (e.g., `='Analysis'!$B$4` for Total Calls value).
    -   **Conditional Formatting for Sales Agent KPIs Table**: A "Use a formula to determine which cells to format" rule is applied to the 'Name' column (e.g., cells D10:D40) of PT7 on the Dashboard. The formula is `=$D10='Analysis'!$A$11`, where D10 is the top-left cell of the 'Name' column, and Analysis!$A$11 contains the currently selected name from the slicer. This highlights the row corresponding to the selected sales agent.

-   **Visual Design**:
    -   **Workbook Theme**: "Aspect" theme is applied to the workbook for consistent color palettes and fonts.
    -   **Dashboard Sheet Layout**:
        -   **Header Area (Rows 1-8)**: Filled with a dark purple color (`#6F4F7C`).
        -   **Main Content Area (Rows 9-40)**: Filled with a lighter custom purple color (`#F2EFF5`).
        -   **Headings**: "Sales Dashboard" (Aptos Narrow, 36pt, white) and "Evaluating Sales Agent Performance" (Aptos Narrow, 16pt, yellow).
        -   **KPI Cards**: Four grouped shapes per KPI. Each group contains:
            -   A gold rounded-corner rectangle (left side).
            -   A white rounded-corner rectangle (right side).
            -   A thin gold vertical line as a divider.
            -   A purple icon representing the metric (phone, target, prize, money).
            -   Two text boxes: one for the numerical value (Aptos Narrow, 32pt, purple, linked to `Analysis` sheet), one for the label (Aptos Narrow, 18pt, purple, e.g., "CALLS"). Shapes have no fill/outline for the text boxes, and all shapes are set to "Don't move or size with cells".
        -   **Charts**: All charts have:
            -   No fill or outline for the chart area.
            -   Hidden field buttons.
            -   Vertical axes fixed to start at 0 (where applicable).
            -   No chart titles (legend or separate text box used instead), no gridlines.
            -   Shadow effect (Outer - Offset Bottom Right) applied to all chart areas.
            -   **Calls Reached / Deals Closed Chart**: Stacked Column. Yellow for Calls Reached, purple for Deals Closed. Series overlap 100%, Gap width 50%. Data labels (Inside End).
            -   **Total Sales Chart**: Column. Purple columns. Linear trendline (yellow, thick dashed).
            -   **Average Call Duration Chart**: Column. Yellow columns.
            -   **Average Call Drop Rate Chart**: Area. Gradient fill (yellow to transparent).
        -   **Sales Agent KPIs Table**: PivotTable with a custom purple style, conditional formatting (Data Bars - yellow for Total Calls/Calls Reached, light purple for Deals Closed, purple for Deal Value).
        -   **Slicer**: Purple themed style, adjusted height and button height to fit all names without a scrollbar.
    -   **Conditional Formatting for Sales Agent KPIs Table**: Formatted with a purple top and bottom border for the selected row.

-   **Charts/Tables**:
    -   **Sales Agent KPIs Table**: PivotTable (PT7) on the dashboard, displaying individual agent performance.
    -   **Sum of Calls Reached / Deals Closed**: PivotChart (linked to PT2), a 2D Stacked Column chart.
    -   **Total Sales**: PivotChart (linked to PT3), a 2D Column chart with a trendline.
    -   **Average Call Duration (seconds)**: PivotChart (linked to PT4), a 2D Column chart.
    -   **Average Call Drop Rate (%)**: PivotChart (linked to PT5), a 2D Area chart.

-   **Theme Hooks**:
    -   `header_bg_color`: For main header background.
    -   `dashboard_bg_color`: For main dashboard area background.
    -   `accent_color_1`: For gold/yellow elements (KPI card left, some chart series, trendline).
    -   `accent_color_2`: For purple elements (KPI icons, other chart series, conditional formatting borders/fills).
    -   `text_light_color`: For titles on dark background.
    -   `text_dark_color`: For KPI values/labels on light background.
    -   `subtitle_color`: For the dashboard subtitle.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference, AreaChart
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.drawing.image import Image # For icons, actual image data would be needed or SVG handling
from openpyxl.utils import get_column_letter

# --- Simulating _helpers.py for theme and basic styling ---
class ThemePalette:
    def __init__(self, name="Aspect"):
        self.name = name
        if name == "Aspect":
            self.header_bg_color = "6F4F7C"
            self.dashboard_bg_color = "F2EFF5"
            self.accent_color_1 = "FFC000"
            self.accent_color_2 = "6F4F7C"
            self.text_light_color = "FFFFFF"
            self.text_dark_color = "6F4F7C"
            self.subtitle_color = "FFFF00"
            self.light_accent_color_2 = "C8B5D3" # Lighter shade for data bars
            self.medium_accent_color_2 = "A98BB9" # Medium shade for data bars
        else: # Default/Fallback
            self.header_bg_color = "4472C4"
            self.dashboard_bg_color = "E6E6E6"
            self.accent_color_1 = "FF0000"
            self.accent_color_2 = "0000FF"
            self.text_light_color = "FFFFFF"
            self.text_dark_color = "000000"
            self.subtitle_color = "808080"
            self.light_accent_color_2 = "ADD8E6"
            self.medium_accent_color_2 = "6495ED"

def get_theme_palette(theme_name: str):
    return ThemePalette(theme_name)

def set_fill(cells, color_hex):
    # Simplified for example. In _helpers.py, it handles cell ranges.
    if isinstance(cells, str): # Assume it's a cell range or single cell
        return PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")
    else: # Assume it's an openpyxl cell object
        cells.fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")

def set_font(cells, color_hex=None, size=None, bold=False):
    # Simplified for example. In _helpers.py, it handles cell ranges.
    font_params = {}
    if color_hex: font_params['color'] = color_hex
    if size: font_params['size'] = size
    if bold: font_params['bold'] = bold
    # This would typically modify an existing font or create a new one
    return Font(**font_params)

# Placeholder for complex shape drawing and textbox linking
def _add_dashboard_shape(ws, top_left_anchor: str, bottom_right_anchor: str, shape_type: str, fill_color: str, outline_color: str, **kwargs):
    # Openpyxl doesn't have direct "shape" drawing like UI tools.
    # This would involve either drawing.shapes.Shape with XML or placing images (PNG/SVG).
    # For a full implementation, detailed shape creation logic would go here.
    # For this exercise, we acknowledge its complexity and provide a conceptual placeholder.
    pass

def _add_kpi_textbox(ws, anchor: str, text: str, font_color: str, font_size: int, is_value: bool, link_cell: str = None):
    # Adding a textbox and linking its text to a cell value is not straightforward in openpyxl.
    # It often requires direct manipulation of the VML or embedding a linked text box as an image.
    # Here, we'll just set static text for demonstration purposes within the code structure.
    cell = ws[anchor]
    cell.value = text
    cell.font = set_font(cell, color_hex=font_color, size=font_size, bold=is_value)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    # If link_cell were functional, it would dynamically fetch the value
    if link_cell:
        # Conceptual: cell.value = "=Analysis!" + link_cell.split('!')[1]
        pass

# --- End of _helpers.py simulation ---


def render_workbook(wb, *, title: str, theme: str = "Aspect") -> None:
    """
    Renders a themed interactive sales dashboard workbook.

    Args:
        wb: The openpyxl workbook object.
        title: The main title for the dashboard.
        theme: The name of the color theme to apply (e.g., "Aspect").
    """
    palette = get_theme_palette(theme)

    # Delete default sheets
    for sheet_name in wb.sheetnames:
        del wb[sheet_name]

    # Create Dashboard Sheet
    ws_dashboard = wb.create_sheet("Dashboard", 0)
    ws_dashboard.sheet_view.showGridLines = False

    # Set background colors for dashboard
    for row_idx in range(1, 9):
        for col_idx in range(1, 20): # Assume columns A to S for header
            ws_dashboard.cell(row=row_idx, column=col_idx).fill = set_fill("", palette.header_bg_color)
    for row_idx in range(9, 41): # Assume rows 9 to 40 for main body
        for col_idx in range(1, 20):
            ws_dashboard.cell(row=row_idx, column=col_idx).fill = set_fill("", palette.dashboard_bg_color)

    # Set column A width for alignment
    ws_dashboard.column_dimensions['A'].width = 5 # Narrow column to shift content

    # Add Dashboard Title and Subtitle
    ws_dashboard['B2'].value = title
    ws_dashboard['B2'].font = set_font(ws_dashboard['B2'], color_hex=palette.text_light_color, size=36, bold=True)

    ws_dashboard['B4'].value = "Evaluating Sales Agent Performance"
    ws_dashboard['B4'].font = set_font(ws_dashboard['B4'], color_hex=palette.subtitle_color, size=16)

    # Create Analysis Sheet
    ws_analysis = wb.create_sheet("Analysis", 1)
    ws_analysis.sheet_view.showGridLines = False

    # Create Data Sheet (Conceptual - assume data is already here or loaded)
    ws_data = wb.create_sheet("Data", 2)
    ws_data.sheet_view.showGridLines = False
    # --- Place Sample Data in Data Sheet ---
    # In a real application, data would be loaded dynamically, e.g., from a file.
    # For this reproduction, we need some sample data for pivot tables.
    headers = ["Name", "Date", "Total Calls", "Calls Reached", "Average Duration (sec)", "Deals Closed", "Call Conversion Rate (%)", "Deal Value ($)", "Call Drop Rate (%)"]
    ws_data.append(headers)
    sample_data = [
        ["Evan", "1/1/2024", 74, 12, 330.42, 4, 0.58, 4276.31, 0.03],
        ["Alice", "1/1/2024", 78, 12, 377.5, 4, 0.33, 3880.96, 0.04],
        ["Diana", "1/1/2024", 47, 14, 418.92, 2, 0.14, 3716.0, 0.04],
        ["Liam", "1/1/2024", 81, 16, 516.23, 3, 0.31, 1030.68, 0.03],
        ["Jake", "1/1/2024", 24, 6, 76.93, 4, 0.67, 1552.35, 0.04],
        ["Bob", "1/1/2024", 59, 19, 520.06, 3, 0.6, 3546.72, 0.01],
        ["Rick", "1/1/2024", 68, 7, 290.39, 3, 0.16, 2472.24, 0.1],
        ["Charlie", "1/1/2024", 60, 7, 251.7, 7, 0.71, 3956.69, 0.04],
        ["Molly", "1/1/2024", 54, 21, 362.62, 5, 0.43, 1140.08, 0.03],
        ["Chris", "1/1/2024", 59, 13, 307.49, 10, 0.77, 979.09, 0.03],
        ["James", "1/1/2024", 18, 8, 206.81, 7, 0.88, 720.56, 0.08],
        ["Richard", "1/1/2024", 36, 6, 547.6, 5, 0.83, 3463.18, 0.04],
        ["Paul", "1/1/2024", 67, 17, 552.55, 2, 0.12, 330.12, 0.04],
        ["Ian", "1/1/2024", 35, 9, 216.03, 2, 0.22, 4072.07, 0.03],
        ["Melissa", "1/1/2024", 54, 10, 208.23, 3, 0.3, 645.83, 0.03],
        ["Alex", "1/1/2024", 82, 4, 180.06, 4, 1.0, 1207.17, 0.08],
        ["Karol", "1/1/2024", 81, 7, 82.43, 7, 1.0, 3945.43, 0.08],
        ["Darren", "1/1/2024", 31, 17, 476.95, 7, 0.41, 3946.93, 0.04],
        ["Will", "1/1/2024", 92, 20, 161.42, 4, 0.2, 425.41, 0.1],
        ["Vicky", "1/1/2024", 73, 12, 507.45, 0, 0.0, 1123.84, 0.05],
        ["Grace", "1/1/2024", 25, 14, 279.95, 2, 0.14, 1432.23, 0.05],
        ["Emma", "1/1/2024", 96, 5, 332.83, 1, 0.17, 3173.53, 0.04],
        ["Josh", "1/1/2024", 63, 17, 170.49, 7, 0.88, 2850.64, 0.02],
        ["Craig", "1/1/2024", 53, 8, 514.23, 4, 0.47, 2432.62, 0.0],
        ["David", "1/1/2024", 42, 13, 363.48, 7, 0.7, 3843.92, 0.03],
        ["Mimi", "1/1/2024", 43, 15, 363.48, 6, 0.43, 2843.62, 0.0],
        ["Evan", "1/2/2024", 78, 14, 404.32, 4, 0.47, 4335.54, 0.0],
        ["Alice", "1/2/2024", 81, 14, 362.39, 3, 0.37, 3626.59, 0.0],
        ["Diana", "1/2/2024", 52, 14, 382.59, 3, 0.21, 3966.89, 0.0],
        ["Liam", "1/2/2024", 22, 7, 79.46, 3, 0.43, 1638.74, 0.04],
        ["Jake", "1/2/2024", 53, 11, 446.3, 4, 0.45, 1957.14, 0.03],
        ["Bob", "1/2/2024", 55, 7, 461.67, 2, 0.36, 2566.23, 0.04],
        ["Rick", "1/2/2024", 68, 7, 247.66, 2, 0.16, 3462.44, 0.1],
        ["Charlie", "1/2/2024", 60, 7, 378.61, 9, 0.77, 3956.69, 0.04],
        ["Molly", "1/2/2024", 59, 21, 372.3, 1, 0.43, 979.09, 0.03],
        ["Chris", "1/2/2024", 65, 13, 307.49, 10, 0.77, 1140.08, 0.03],
        ["James", "1/2/2024", 23, 8, 206.81, 7, 0.88, 867.2, 0.08],
        ["Richard", "1/2/2024", 45, 6, 547.6, 5, 0.83, 3463.18, 0.04],
        ["Paul", "1/2/2024", 78, 17, 552.55, 2, 0.12, 4672.07, 0.04],
        ["Ian", "1/2/2024", 36, 9, 216.03, 2, 0.22, 4072.07, 0.03],
        ["Melissa", "1/2/2024", 58, 10, 208.23, 3, 0.3, 645.83, 0.03],
        ["Alex", "1/2/2024", 84, 4, 180.06, 4, 1.0, 1207.17, 0.08],
        ["Karol", "1/2/2024", 85, 7, 82.43, 7, 1.0, 3945.43, 0.08],
        ["Darren", "1/2/2024", 33, 17, 476.95, 7, 0.41, 3946.93, 0.04],
        ["Will", "1/2/2024", 95, 20, 161.42, 4, 0.2, 425.41, 0.1],
        ["Vicky", "1/2/2024", 75, 12, 507.45, 0, 0.0, 1123.84, 0.05],
        ["Grace", "1/2/2024", 27, 14, 279.95, 2, 0.14, 1432.23, 0.05],
        ["Emma", "1/2/2024", 98, 5, 332.83, 1, 0.17, 3173.53, 0.04],
        ["Josh", "1/2/2024", 65, 17, 170.49, 7, 0.88, 2850.64, 0.02],
        ["Craig", "1/2/2024", 55, 8, 514.23, 4, 0.47, 2432.62, 0.0],
        ["David", "1/2/2024", 45, 13, 363.48, 7, 0.7, 3843.92, 0.03],
        ["Mimi", "1/2/2024", 45, 15, 363.48, 6, 0.43, 2843.62, 0.0],
        # Add more data up to 11 months to match video's demo data extent
        # For brevity, only a few rows per "month" are shown
        ["Evan", "11/1/2024", 70, 10, 320.00, 3, 0.50, 4000.00, 0.03],
        ["Alice", "11/1/2024", 75, 11, 360.00, 3, 0.30, 3500.00, 0.04],
        ["Diana", "11/1/2024", 45, 12, 400.00, 2, 0.12, 3600.00, 0.04],
        ["Liam", "11/1/2024", 80, 15, 500.00, 2, 0.25, 950.00, 0.03],
        # And data for December to simulate refresh
        ["Evan", "12/1/2024", 60, 13, 350.00, 5, 0.60, 4500.00, 0.02],
        ["Alice", "12/1/2024", 70, 11, 380.00, 4, 0.35, 3900.00, 0.03],
    ]
    for row_data in sample_data:
        ws_data.append(row_data)

    # Convert data to Excel Table
    data_range = f"A1:{get_column_letter(len(headers))}{len(sample_data) + 1}"
    tab = Table(displayName="SalesData", ref=data_range)
    style = TableStyleInfo(name="TableStyleLight9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)
    # --- End Sample Data Setup ---

    # --- Setup Analysis Sheet PivotTables (Conceptual - actual PT creation is extensive) ---
    # PT1: KPI Summary
    # For demonstration, we'll manually fill a few cells to simulate PT1 output.
    # In a real scenario, these would be generated by openpyxl's PivotTable class.
    ws_analysis['B4'].value = 16749 # Sum of Total Calls
    ws_analysis['B5'].value = 3328  # Sum of Calls Reached
    ws_analysis['B6'].value = 1203  # Sum of Deals Closed
    ws_analysis['B7'].value = 646979.47 # Sum of Deal Value
    ws_analysis['B7'].number_format = "$#,##0" # Apply currency format

    # PT6: Selected Name for Conditional Formatting
    ws_analysis['A11'].value = "Jake" # Simulate Jake being selected in slicer

    # --- Render Dashboard Elements (Conceptual - actual openpyxl drawing is complex) ---

    # KPI Cards (conceptual placement and linking)
    kpi_definitions = [
        {"icon": "phone", "value_cell": "B4", "label": "CALLS"},
        {"icon": "target", "value_cell": "B5", "label": "REACHED"},
        {"icon": "prize", "value_cell": "B6", "label": "CLOSED"},
        {"icon": "money", "value_cell": "B7", "label": "VALUE"},
    ]
    col_start_idx = 5 # Start from column E
    for i, kpi in enumerate(kpi_definitions):
        # Conceptual: _add_dashboard_shape for gold/white rectangles and vertical line
        # _add_dashboard_icon (e.g., Image class from drawing)
        
        # Textbox for value
        value_anchor = f"{get_column_letter(col_start_idx + i * 4 + 1)}5" # E5, I5, M5, Q5
        _add_kpi_textbox(ws_dashboard, value_anchor, str(ws_analysis[kpi['value_cell']].value), palette.text_dark_color, 32, True, kpi['value_cell'])

        # Textbox for label
        label_anchor = f"{get_column_letter(col_start_idx + i * 4 + 1)}6" # E6, I6, M6, Q6
        _add_kpi_textbox(ws_dashboard, label_anchor, kpi['label'], palette.text_dark_color, 18, False)
        
    # Sales Agent KPIs PivotTable (PT7)
    # This would involve creating a PivotTable object and styling it.
    # Conditional formatting data bars and formula-based highlighting would also be applied here.
    # For demonstration, we'll leave it as a comment.
    # print("Conceptual: Render Sales Agent KPIs PivotTable (PT7) on Dashboard")

    # Slicer for 'Name' (Conceptual)
    # openpyxl doesn't support slicers directly. This would be a VBA or Power BI feature.
    # In a static dashboard simulation, filtering would need to be manual or scripted.
    # print("Conceptual: Add Slicer for Name on Dashboard")

    # Charts (Conceptual - actual PivotChart creation and formatting is extensive)
    # Each chart would be created from its respective PivotTable on the Analysis sheet.
    # print("Conceptual: Render Charts (Stacked Column, Column with Trendline, Area) on Dashboard")

    # Adding shadows to charts/shapes (Conceptual)
    # This feature is also complex to implement directly via openpyxl, often requiring external libraries
    # or direct XML manipulation.
    # print("Conceptual: Add shadows to charts and relevant shapes")

    # Final refresh
    # print("Conceptual: Refresh all pivot tables to update dashboard data after adding new source data.")

    # You would need much more complex Openpyxl code here to replicate the full dashboard features:
    # - Actual PivotTable creation (openpyxl.pivot.pivot_table.PivotTable)
    # - PivotTable field setup (openpyxl.pivot.fields.PivotField)
    # - PivotChart creation and linking (openpyxl.chart.reference.Series, openpyxl.chart.bar_chart.BarChart etc.)
    # - Detailed shape drawing (openpyxl.drawing.shapes.Shape or Image handling)
    # - Advanced conditional formatting rules (FormulaRule for dynamic highlighting)
    # - Precise positioning and sizing of all objects.

```