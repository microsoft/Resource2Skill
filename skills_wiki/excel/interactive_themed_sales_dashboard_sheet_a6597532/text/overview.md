### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Themed Sales Dashboard Sheet

*   **Tier**: sheet_shell
*   **Core Mechanism**: Creates a visually cohesive and interactive sales dashboard sheet in Excel, pulling aggregated data for KPIs and charts from pivot tables/charts on a separate "Analysis" sheet. It uses themed colors, custom shapes with icons, text boxes linked to aggregated data, conditional formatting for highlighting, and slicers for dynamic data exploration.
*   **Applicability**: For creating dynamic business dashboards to monitor key performance indicators (KPIs) and visualize performance trends by various dimensions (e.g., sales agent, month). Requires pre-aggregated data (e.g., in pivot tables) and ideally an Excel Table for the raw data source to enable easy refresh.

### 2. Structural Breakdown

-   **Data Layout**: The dashboard sheet itself primarily functions as a presentation layer. It assumes the existence of:
    *   A `Data` sheet: Contains the raw sales data in an Excel Table named `SalesData` (columns: `Name`, `Date`, `Total Calls`, `Calls Reached`, `Average Duration (sec)`, `Deals Closed`, `Call Conversion Rate (%)`, `Deal Value ($)`, `Call Drop Rate (%)`).
    *   An `Analysis` sheet: Houses multiple PivotTables and PivotCharts derived from `SalesData`.
        *   **KPI PivotTable**: Aggregates `Total Calls`, `Calls Reached`, `Deals Closed`, `Deal Value ($)` (as sum) into single cells, linked to dashboard text boxes.
        *   **Sales Agent KPIs PivotTable**: Displays `Name` (as rows), `Total Calls`, `Calls Reached`, `Deals Closed`, `Deal Value ($)` (as values).
        *   **Monthly Performance PivotTables**: For `Sum of Calls Reached` vs. `Sum of Deals Closed`, `Sum of Deal Value ($)`, `Average of Average Duration (sec)`, `Average of Call Drop Rate (%)`, all grouped by `Months(Date)`. These feed the various charts.
        *   **Selected Name PivotTable**: A simple PivotTable displaying only the `Name` selected in the main dashboard slicer (used for conditional formatting lookup).
-   **Formula Logic**:
    *   **KPI Text Boxes**: Linked to specific cells in the KPI PivotTable on the `Analysis` sheet (e.g., `='Analysis'!$B$4`).
    *   **Conditional Formatting (Sales Agent KPIs Table)**: A custom formula rule applied to the 'Name' column of the `Sales Agent KPIs` PivotTable: `=D10='Analysis'!$A$11` (where `D10` is the top-left cell of the 'Name' column in the PivotTable, and `Analysis!$A$11` is the cell containing the currently selected name from the slicer).
-   **Visual Design**:
    *   **Header Area (Rows 1-8)**: Filled with `header_bg` color (dark purple). "Sales Dashboard" title (`text_color_light`, 36pt, Aptos Narrow font), "Evaluating Sales Agent Performance" subtitle (`text_color_accent`, 16pt, Aptos Narrow font).
    *   **Main Dashboard Area (Rows 9-40)**: Filled with `main_bg` color (lighter purple).
    *   **KPI Cards**: Custom shapes are used:
        *   A wider rounded rectangle with rounded top-left corners, filled with `accent_color_1` (gold).
        *   A smaller rounded rectangle with rounded top-right corners, filled with `light_bg` (white), overlapped with the gold shape.
        *   A vertical line (gold, 0.5pt weight) separating icon and value area.
        *   Icons (phone, target, ribbon, money) are inserted and colored with `header_bg`.
        *   Text boxes for KPI values (`text_color_dark`, 32pt) and labels (`text_color_dark`, 18pt) are placed within the white shapes, linked to the `Analysis` sheet.
    *   **Slicer**: Themed with a dark color scheme (`header_bg` equivalent) with appropriate button heights to avoid scrollbars.
    *   **Charts**: No chart area fill or border. Gridlines removed, legends positioned strategically or removed if title is sufficient. Custom series colors (`accent_color_1`, `accent_color_2`, `header_bg`). Trendline added to Total Sales chart (yellow dashed line).
    *   **Sales Agent KPIs Table**: PivotTable style using `header_bg` and `main_bg` colors, with conditional formatting data bars (gradient fills using `accent_color_1` and `accent_color_2`).
-   **Charts/Tables**: The dashboard displays:
    *   A PivotTable (`Sales Agent KPIs`) showing individual agent performance.
    *   A stacked column PivotChart showing `Sum of Calls Reached` vs. `Sum of Deals Closed` by month.
    *   A column PivotChart showing `Total Sales` by month with a linear trendline.
    *   A column PivotChart showing `Average Call Duration (seconds)` by month.
    *   An area PivotChart showing `Average Call Drop Rate %` by month.
    *   A Slicer for `Name` (Sales Agent).
-   **Theme Hooks**: `header_bg`, `main_bg`, `light_bg`, `text_color_light`, `text_color_dark`, `text_color_accent`, `accent_color_1`, `accent_color_2`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image
from openpyxl.drawing.shapes import Shape, ConnectionShape, ShapeReference
from openpyxl.chart.label import DataLabel, DataLabelList
from openpyxl.chart import BarChart, LineChart, AreaChart, Reference
from openpyxl.chart.series import DataPoint, DataPoint3D
from openpyxl.chart.trendline import Trendline
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.formatting.rule import FormulaRule, DataBarRule
from openpyxl.utils.units import EMU_per_cm

# Assume _helpers.py is available for theme management
# For local execution, you might need to mock or provide a simple _helpers.py
# Example _helpers.py:
# class Theme:
#     def __init__(self, theme_name):
#         self.header_bg = "FF5B008C"  # Dark Purple
#         self.main_bg = "FFEFE8F5"    # Lighter Purple
#         self.light_bg = "FFFFFFFF"   # White
#         self.text_color_light = "FFFFFFFF"
#         self.text_color_dark = "FF5B008C"
#         self.text_color_accent = "FFE5B800" # Yellow
#         self.accent_color_1 = "FFE5B800" # Gold
#         self.accent_color_2 = "FFC0A0C0" # Pale Purple
#
# def get_theme_colors(theme_name):
#     return Theme(theme_name)
#
# def create_fill(hex_color):
#     return PatternFill(start_color=hex_color[2:], end_color=hex_color[2:], fill_type="solid")
#
# def create_font(size, color, bold=False):
#     return Font(name="Aptos Narrow", size=size, color=color[2:], bold=bold)
#
# def create_border(color_hex, style="thin"):
#     side = Side(border_style=style, color=color_hex[2:])
#     return Border(left=side, right=side, top=side, bottom=side)

# Mock _helpers for demonstration if not available
try:
    from skills_library.excel.components import _helpers
except ImportError:
    class MockTheme:
        def __init__(self, theme_name):
            self.header_bg = "FF5B008C"  # Dark Purple
            self.main_bg = "FFEFE8F5"    # Lighter Purple
            self.light_bg = "FFFFFFFF"   # White
            self.text_color_light = "FFFFFFFF"
            self.text_color_dark = "FF5B008C"
            self.text_color_accent = "FFE5B800" # Yellow
            self.accent_color_1 = "FFE5B800" # Gold
            self.accent_color_2 = "FFC0A0C0" # Pale Purple
    class MockHelpers:
        def get_theme_colors(self, theme_name):
            return MockTheme(theme_name)
        def create_fill(self, hex_color):
            return PatternFill(start_color=hex_color[2:], end_color=hex_color[2:], fill_type="solid")
        def create_font(self, size, color, bold=False):
            return Font(name="Aptos Narrow", size=size, color=color[2:], bold=bold)
        def create_border(self, color_hex, style="thin"):
            side = Side(border_style=style, color=color_hex[2:])
            return Border(left=side, right=side, top=side, bottom=side)
    _helpers = MockHelpers()


def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an interactive sales dashboard sheet.

    This function sets up the visual layout, header, KPI cards, and placeholders
    for charts and slicers, assuming that the underlying PivotTables and PivotCharts
    are already present on an 'Analysis' sheet and raw data on a 'Data' sheet.

    Args:
        wb: The openpyxl workbook object.
        sheet_name: The name of the sheet to render the dashboard on.
        title: The main title for the dashboard.
        theme: The name of the theme to use for colors (e.g., "corporate_blue").
               Assumes _helpers.py provides theme definitions.
        **kwargs: Additional arguments (not used in this skill).
    """
    ws = wb.create_sheet(sheet_name)
    theme_colors = _helpers.get_theme_colors(theme)

    # --- Set up basic sheet properties ---
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 4.86  # For alignment of main title
    for col_letter in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        ws.column_dimensions[col_letter].width = 10  # Standardize width

    # Set row heights
    for r in range(1, 41):
        ws.row_dimensions[r].height = 20

    # --- Apply background colors ---
    header_fill = _helpers.create_fill(theme_colors.header_bg)
    main_fill = _helpers.create_fill(theme_colors.main_bg)

    for row_num in range(1, 9):
        for col_idx in range(1, ws.max_column + 1):
            ws.cell(row=row_num, column=col_idx).fill = header_fill

    for row_num in range(9, 41):
        for col_idx in range(1, ws.max_column + 1):
            ws.cell(row=row_num, column=col_idx).fill = main_fill

    # --- Header and Subheader ---
    ws['B2'].value = title
    ws['B2'].font = _helpers.create_font(36, theme_colors.text_color_light, bold=True)
    ws['B2'].alignment = Alignment(horizontal='left', vertical='center')

    ws['B4'].value = "Evaluating Sales Agent Performance"
    ws['B4'].font = _helpers.create_font(16, theme_colors.text_color_accent)
    ws['B4'].alignment = Alignment(horizontal='left', vertical='center')

    # --- KPI Cards and Icons ---
    kpi_count = 4
    kpi_start_col = 8
    kpi_width_cm = 6.5
    kpi_height_cm = 3.5
    kpi_spacing_cm = 0.5

    kpi_labels = ["CALLS", "REACHED", "CLOSED", "VALUE"]
    kpi_analysis_cells = ["B4", "B5", "B6", "B7"] # Cells on 'Analysis' sheet for KPI values

    for i in range(kpi_count):
        start_col = kpi_start_col + i * (int(kpi_width_cm / (ws.column_dimensions['A'].width * 0.25)) + 2) # Approximate pixel to column calculation
        start_row = 2

        # Gold rounded rectangle (left part)
        shape_gold = Shape.from_geometry_string(
            'm 0,0 l {}sv 0 {}sv 0 {}sv {}sv {}sv {}sv 0 {}sv xe'.format(
                int(kpi_width_cm * EMU_per_cm * 0.3), # width of gold strip
                int(kpi_height_cm * EMU_per_cm),
                int(kpi_width_cm * EMU_per_cm * 0.7),
                int(kpi_width_cm * EMU_per_cm * 0.3),
                int(kpi_height_cm * EMU_per_cm),
                int(kpi_width_cm * EMU_per_cm * 0.7)
            ),
            'GoldFillShape{}'.format(i)
        )
        shape_gold.fill = _helpers.create_fill(theme_colors.accent_color_1)
        shape_gold.noFill = False
        shape_gold.border.noFill = True
        shape_gold.width = int(kpi_width_cm * EMU_per_cm)
        shape_gold.height = int(kpi_height_cm * EMU_per_cm)
        # Position needs to be precise relative to top-left of the first cell
        ws.add_chart(shape_gold, anchor=ws.cell(row=start_row, column=start_col).coordinate)
        # openpyxl shape positioning is tricky, direct xy pos might be needed for precise control
        # For simplicity in this `sheet_shell`, we place it by cell and assume manual adjustment or
        # more complex positioning logic if precise pixel alignment is critical.

        # White rounded rectangle (right part)
        shape_white = Shape.from_geometry_string(
            'm 0,0 l {}sv 0 {}sv 0 {}sv {}sv {}sv {}sv 0 {}sv xe'.format(
                int(kpi_width_cm * EMU_per_cm * 0.7), # width of white strip
                int(kpi_height_cm * EMU_per_cm),
                int(kpi_width_cm * EMU_per_cm * 0.3),
                int(kpi_width_cm * EMU_per_cm * 0.7),
                int(kpi_height_cm * EMU_per_cm),
                int(kpi_width_cm * EMU_per_cm * 0.3)
            ),
            'WhiteFillShape{}'.format(i)
        )
        shape_white.fill = _helpers.create_fill(theme_colors.light_bg)
        shape_white.noFill = False
        shape_white.border.noFill = True
        shape_white.width = int(kpi_width_cm * EMU_per_cm)
        shape_white.height = int(kpi_height_cm * EMU_per_cm)
        ws.add_chart(shape_white, anchor=ws.cell(row=start_row, column=start_col + 1).coordinate) # Offset for white part

        # Vertical separator line
        # Line drawing in openpyxl for exact overlay is complex.
        # This part is simplified, assuming it's part of the overall visual.

        # Text boxes for KPI values and labels
        kpi_value_textbox = openpyxl.drawing.text.RichText()
        kpi_value_textbox.add(openpyxl.drawing.text.Paragraph())
        kpi_value_textbox.paragraphs[0].add(openpyxl.drawing.text.TextRun(text=f"={kpi_analysis_cells[i]}"))
        kpi_value_textbox.paragraphs[0].font = _helpers.create_font(32, theme_colors.text_color_dark, bold=False)

        # openpyxl does not directly support linking textbox to cell formula in a way that refreshes in Excel UI
        # A common workaround is to put the value in a cell behind the textbox and make the textbox transparent.
        # For this example, we'll write the formula directly for clarity, but be aware of limitations.
        ws.cell(row=start_row + 2, column=start_col + 3).value = f"='Analysis'!{kpi_analysis_cells[i]}"
        ws.cell(row=start_row + 2, column=start_col + 3).font = _helpers.create_font(32, theme_colors.text_color_dark, bold=False)
        ws.cell(row=start_row + 2, column=start_col + 3).alignment = Alignment(horizontal='center', vertical='center')

        ws.cell(row=start_row + 3, column=start_col + 3).value = kpi_labels[i]
        ws.cell(row=start_row + 3, column=start_col + 3).font = _helpers.create_font(18, theme_colors.text_color_dark, bold=False)
        ws.cell(row=start_row + 3, column=start_col + 3).alignment = Alignment(horizontal='center', vertical='center')

        # Placeholder for Icons (actual image insertion is complex and depends on image source)
        # img = Image(f'path/to/icon_{i}.png')
        # img.width, img.height = 1.8 * EMU_per_cm, 1.8 * EMU_per_cm
        # ws.add_image(img, ws.cell(row=start_row + 2, column=start_col + 1).coordinate) # Approximate placement

    # --- Sales Agent KPIs Table ---
    # Assume the pivot table "Sales Agent KPIs" is already on the 'Analysis' sheet
    # and has been copied here. We'll just set its top-left position and apply CF.
    # For actual openpyxl code, you would need to define and insert Table objects.
    ws['B9'].value = "Sales Agent KPIs"
    ws['B9'].font = _helpers.create_font(14, theme_colors.text_color_dark, bold=True)
    ws['B9'].alignment = Alignment(horizontal='left', vertical='center')

    # Simulate pivot table data for conditional formatting to apply to
    # In a real scenario, this range would be dynamically determined from the copied pivot table.
    cf_range = f"D10:G39" # Example range for data bars

    # Conditional formatting for Data Bars
    # Calls Reached (Yellow)
    ws.conditional_formatting.add(f'E10:E39', DataBarRule(
        start_type='Num', start_value=0, start_color=_helpers.get_theme_colors(theme).accent_color_1,
        end_type='Max', end_value=None, end_color=_helpers.get_theme_colors(theme).accent_color_1
    ))
    # Deals Closed (Light Purple)
    ws.conditional_formatting.add(f'F10:F39', DataBarRule(
        start_type='Num', start_value=0, start_color=_helpers.get_theme_colors(theme).accent_color_2,
        end_type='Max', end_value=None, end_color=_helpers.get_theme_colors(theme).accent_color_2
    ))
    # Deal Value (Dark Purple)
    ws.conditional_formatting.add(f'G10:G39', DataBarRule(
        start_type='Num', start_value=0, start_color=_helpers.get_theme_colors(theme).header_bg,
        end_type='Max', end_value=None, end_color=_helpers.get_theme_colors(theme).header_bg
    ))

    # Conditional formatting to highlight selected name (example for D10)
    ws.conditional_formatting.add('D10:D39', FormulaRule(
        formula=['$D10=Analysis!$A$11'],
        fill=_helpers.create_fill(theme_colors.accent_color_1),
        font=_helpers.create_font(11, theme_colors.text_color_dark, bold=True),
        border=_helpers.create_border(theme_colors.header_bg)
    ))

    # --- Chart Placeholders ---
    # The actual charts would be copied from the 'Analysis' sheet.
    # We place dummy cells or shapes to mark their positions.

    # Chart 1: Sum of Calls Reached + Sum of Deals Closed (Stacked Column)
    ws['H9'].value = "Sum of Calls Reached + Sum of Deals Closed"
    ws['H9'].font = _helpers.create_font(14, theme_colors.text_color_dark, bold=True)
    ws['H9'].alignment = Alignment(horizontal='center', vertical='center')
    # Placeholder for chart object
    # ws.add_chart(chart_object_from_analysis, "H10")

    # Chart 2: Total Sales (Column with Trendline)
    ws['P9'].value = "Total Sales $"
    ws['P9'].font = _helpers.create_font(14, theme_colors.text_color_dark, bold=True)
    ws['P9'].alignment = Alignment(horizontal='center', vertical='center')
    # Placeholder for chart object
    # ws.add_chart(chart_object_from_analysis, "P10")

    # Chart 3: Average Call Duration (Seconds) (Column)
    ws['H26'].value = "Average Call Duration (Seconds)"
    ws['H26'].font = _helpers.create_font(14, theme_colors.text_color_dark, bold=True)
    ws['H26'].alignment = Alignment(horizontal='center', vertical='center')
    # Placeholder for chart object
    # ws.add_chart(chart_object_from_analysis, "H27")

    # Chart 4: Average Call Drop Rate % (Area)
    ws['P26'].value = "Average Call Drop Rate %"
    ws['P26'].font = _helpers.create_font(14, theme_colors.text_color_dark, bold=True)
    ws['P26'].alignment = Alignment(horizontal='center', vertical='center')
    # Placeholder for chart object
    # ws.add_chart(chart_object_from_analysis, "P27")

    # --- Slicer Placeholder ---
    # Slicers are not directly created via openpyxl, they are an Excel UI element.
    # The video shows it being copied and positioned.
    # Its functionality is driven by its connection to PivotTables.
    # For a full reproduction, you'd insert a slicer via the Excel UI and connect it.
```