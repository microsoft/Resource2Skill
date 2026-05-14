### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Themed Sales Dashboard

*   **Tier**: sheet_shell
*   **Core Mechanism**: This skill constructs a complete, visually appealing sales dashboard on a single Excel sheet. It integrates multiple chart types (donut for KPIs, line for trends, radar for satisfaction, and a map placeholder for geographical breakdown) alongside dynamic numeric KPI displays and interactive sheet navigation via a hyperlinked sidebar. The design follows a cohesive color theme and layout.
*   **Applicability**: This skill is ideal for creating executive summaries or performance monitoring dashboards. It is suitable for presenting key sales metrics, trends, customer satisfaction, and geographical performance at a glance. It requires structured input data for KPIs and chart series, often sourced from other sheets within the workbook for dynamic updates.

### 2. Structural Breakdown

-   **Data Layout**:
    -   `Dashboard` sheet: Primarily a canvas for charts, shapes, and formatted cells. Column A serves as a navigation sidebar.
    -   `Inputs` sheet: Contains structured tables for KPIs (Actual, Target, % Complete, Remainder), monthly sales figures (2021, 2022), sales by country (Country, Sales), and customer satisfaction scores (Factor, Score).
    -   `Contacts` sheet: Simple table with Country, General Manager, and Email.
-   **Formula Logic**:
    -   `Inputs` sheet: `% Complete` calculated as `Actual / Target`, `Remainder` as `1 - % Complete`.
    -   `Dashboard` sheet: KPI numeric displays directly link to `Actual` cells on the `Inputs` sheet (e.g., `=Inputs!B5`). KPI percentages directly link to `% Complete` cells on the `Inputs` sheet (e.g., `=Inputs!B7`).
-   **Visual Design**:
    -   **Overall Theme**: Predominantly dark blue and white with red and lighter blue accents.
    -   **Sidebar (Column A)**: Dark blue background (`theme.header_bg`), white text (`theme.header_fg`), text-based hyperlinks to other sheets/email.
    -   **Main Title**: Large, bold, dark text (`theme.text_color_dark`) for "Sales Dashboard South America 2022", smaller gray text for "Figures in millions of USD".
    -   **Visual Containers**: Merged cells with white fill (`theme.white`) act as background 'shapes' for charts, providing a clean, bordered appearance.
    -   **KPI Displays**: Large, bold, dark text for actual values; slightly smaller, bold, dark text for percentages, placed next to donut charts.
    -   **Donut Charts**: Dark blue (`theme.accent_2`) for `% Complete`, lighter blue (`theme.accent_3`) for `Remainder`. Doughnut hole size set to 65%. No chart title or legend. Chart area has no fill and no line border.
    -   **Line Chart (Sales Trend)**: Style with markers. 2022 series in red (`theme.accent_1`), 2021 series in dark blue (`theme.accent_2`). Both lines have round markers (size 5) with white fill and matching border color. Y-axis scaling adjusted (180-250) for better detail. No chart title or legend. Chart area has no fill and no line border.
    -   **Radar Chart (Customer Satisfaction)**: Dark blue line (`theme.accent_2`) with round markers (size 5), white fill, and dark blue border. No chart title or legend. Chart area has no fill and no line border.
    -   **Map Chart (Placeholder)**: Represented by a merged cell area with a title due to `openpyxl`'s lack of direct map chart support. If replaced by an actual map, it would typically have no legend, no fill, and no line border for the chart area.
-   **Charts/Tables**:
    -   3 `DoughnutChart` instances for Sales, Profit, and # Customers.
    -   1 `LineChart` for 2021-2022 Sales Trend.
    -   1 `RadarChart` for Customer Satisfaction.
    -   1 Placeholder for Map Chart (as `openpyxl` does not support them).
-   **Theme Hooks**: `header_bg`, `header_fg`, `accent_1`, `accent_2`, `accent_3`, `text_color_dark`, `text_color_light`, `white`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference, DoughnutChart, RadarChart
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.utils import get_column_letter

# Mocking _helpers functions for self-containment and demonstration
class ThemeColors:
    def __init__(self, theme_name):
        self.header_bg = "002060" # Dark Blue
        self.header_fg = "FFFFFF" # White
        self.accent_1 = "FF0000" # Red
        self.accent_2 = "0070C0" # Medium Blue
        self.accent_3 = "8EBAD9" # Lighter Blue
        self.text_color_dark = "000000" # Black for text for better visibility on white shapes
        self.text_color_light = "FFFFFF" # White
        self.white = "FFFFFF"

def get_theme_colors(theme_name="corporate_blue"):
    return ThemeColors(theme_name)

def apply_font(cell, font_name="Calibri", size=11, bold=False, color="000000"):
    cell.font = Font(name=font_name, sz=size, bold=bold, color=color)

def apply_fill(cell, color="FFFFFF"):
    cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

def apply_border(cell, style="thin", color="000000"):
    side = Side(border_style=style, color=color)
    cell.border = Border(left=side, right=side, top=side, bottom=side)

# End mock helpers

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    theme_colors = get_theme_colors(theme)
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Create Inputs and Contacts sheets with dummy data for linking and charts
    inputs_ws = wb.create_sheet("Inputs")
    contacts_ws = wb.create_sheet("Contacts")
    
    # --- Dummy Data for Inputs Sheet ---
    inputs_ws.cell(row=1, column=2, value="KPIs").font = Font(bold=True)
    inputs_ws.cell(row=3, column=2, value="Sales (M)")
    inputs_ws.cell(row=3, column=5, value="Profit (M)")
    inputs_ws.cell(row=3, column=8, value="Customers (M)")

    inputs_ws.cell(row=4, column=2, value="Actual")
    inputs_ws.cell(row=5, column=2, value=2544) # Sales Actual
    inputs_ws.cell(row=4, column=3, value="Target")
    inputs_ws.cell(row=6, column=3, value=3000) # Sales Target
    inputs_ws.cell(row=7, column=2, value="=B5/C6") # % Complete Sales (Placeholder text, openpyxl won't calculate)
    inputs_ws.cell(row=7, column=2).value = 0.85 # Actual value
    inputs_ws.cell(row=8, column=2, value="=1-B7")  # Remainder Sales
    inputs_ws.cell(row=8, column=2).value = 0.15 # Actual value
    inputs_ws.cell(row=7, column=2).number_format = '0%'
    inputs_ws.cell(row=8, column=2).number_format = '0%'

    inputs_ws.cell(row=4, column=5, value="Actual")
    inputs_ws.cell(row=5, column=5, value=890) # Profit Actual
    inputs_ws.cell(row=4, column=6, value="Target")
    inputs_ws.cell(row=6, column=6, value=1000) # Profit Target
    inputs_ws.cell(row=7, column=5, value="=E5/F6") # % Complete Profit
    inputs_ws.cell(row=7, column=5).value = 0.89 # Actual value
    inputs_ws.cell(row=8, column=5, value="=1-E7")  # Remainder Profit
    inputs_ws.cell(row=8, column=5).value = 0.11 # Actual value
    inputs_ws.cell(row=7, column=5).number_format = '0%'
    inputs_ws.cell(row=8, column=5).number_format = '0%'

    inputs_ws.cell(row=4, column=8, value="Actual")
    inputs_ws.cell(row=5, column=8, value=87.0) # Customers Actual
    inputs_ws.cell(row=4, column=9, value="Target")
    inputs_ws.cell(row=6, column=9, value=100) # Customers Target
    inputs_ws.cell(row=7, column=8, value="=H5/I6") # % Complete Customers
    inputs_ws.cell(row=7, column=8).value = 0.87 # Actual value
    inputs_ws.cell(row=8, column=8, value="=1-H7")  # Remainder Customers
    inputs_ws.cell(row=8, column=8).value = 0.13 # Actual value
    inputs_ws.cell(row=7, column=8).number_format = '0%'
    inputs_ws.cell(row=8, column=8).number_format = '0%'
    
    # Sales Trend Data
    inputs_ws.cell(row=15, column=2, value="Sales Trend").font = Font(bold=True)
    inputs_ws.cell(row=16, column=2, value="Month")
    inputs_ws.cell(row=16, column=3, value="2021")
    inputs_ws.cell(row=16, column=4, value="2022")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sales_2021 = [201.9, 204.2, 198.6, 199.2, 195.3, 192.4, 198.6, 199.2, 202.4, 205.5, 210.0, 215.3]
    sales_2022 = [215.3, 217.6, 220.1, 206.4, 204.3, 203.0, 208.4, 212.6, 218.6, 222.6, 225.8, 228.6]
    for i, month in enumerate(months):
        inputs_ws.cell(row=17+i, column=2, value=month)
        inputs_ws.cell(row=17+i, column=3, value=sales_2021[i])
        inputs_ws.cell(row=17+i, column=4, value=sales_2022[i])

    # Sales by Country Data
    inputs_ws.cell(row=15, column=6, value="Sales by Country").font = Font(bold=True)
    inputs_ws.cell(row=16, column=6, value="Country")
    inputs_ws.cell(row=16, column=7, value="Sales (M)")
    countries = ["Argentina", "Colombia", "Brazil", "Ecuador", "Peru", "Chile", "Bolivia"]
    country_sales = [953.3, 453.2, 553.2, 445.3, 253.6, 253.6, 387.5]
    for i, country in enumerate(countries):
        inputs_ws.cell(row=17+i, column=6, value=country)
        inputs_ws.cell(row=17+i, column=7, value=country_sales[i])

    # Customer Satisfaction Data (Radar Chart)
    inputs_ws.cell(row=12, column=10, value="Customer Satisfaction").font = Font(bold=True)
    inputs_ws.cell(row=13, column=10, value="Factor")
    inputs_ws.cell(row=13, column=11, value="Score")
    satisfaction_factors = ["Speed", "Quality", "Hygiene", "Service", "Availability"]
    satisfaction_scores = [0.54, 0.89, 0.93, 0.57, 0.95]
    for i, factor in enumerate(satisfaction_factors):
        inputs_ws.cell(row=14+i, column=10, value=factor)
        inputs_ws.cell(row=14+i, column=11, value=satisfaction_scores[i])
        inputs_ws.cell(row=14+i, column=11).number_format = '0%'

    # --- Dummy Data for Contacts Sheet ---
    contacts_ws.cell(row=1, column=1, value="Country").font = Font(bold=True)
    contacts_ws.cell(row=1, column=2, value="General Manager").font = Font(bold=True)
    contacts_ws.cell(row=1, column=3, value="Email").font = Font(bold=True)
    contacts_data = [
        ("Argentina", "Argentina Facundo Gonzalez", "f.gonzalez@mcdonalds.com"),
        ("Colombia", "Radamel Lopez", "r.lopez@mcdonalds.com"),
        ("Brazil", "Joao Silva", "j.silva@mcdonalds.com"),
        ("Ecuador", "Jaime Loimo", "j.loimo@mcdonalds.com"),
        ("Peru", "Samuel Armando", "s.armando@mcdonalds.com"),
        ("Chile", "Alvaro Sanchez", "a.sanchez@mcdonalds.com"),
        ("Bolivia", "Angel Garcia", "a.garcia@mcdonalds.com")
    ]
    for r, row_data in enumerate(contacts_data):
        for c, value in enumerate(row_data):
            cell = contacts_ws.cell(row=r+2, column=c+1, value=value)
            if c == 2: # Apply hyperlink to email
                cell.hyperlink = Hyperlink(ref=f"mailto:{value}")
                cell.font = Font(underline="single", color="0563C1")


    # --- Dashboard Structure (on 'ws' sheet) ---
    ws.column_dimensions['A'].width = 5 # Sidebar width
    for col_idx in range(2, 18): # Adjusting column widths for content
        ws.column_dimensions[get_column_letter(col_idx)].width = 10
    for row_idx in range(1, 20): # Adjusting row heights
        ws.row_dimensions[row_idx].height = 20 if row_idx > 4 else 25
    ws.row_dimensions[1].height = 30


    # Sidebar (Column A)
    for row_idx in range(1, 20):
        apply_fill(ws.cell(row=row_idx, column=1), theme_colors.header_bg)

    # Hyperlinked Icons (using text labels as placeholders for actual images/icons)
    icon_rows = {
        "Dashboard": 5,
        "Inputs": 7,
        "Contacts": 9,
        "Email": 11,
        "Support": 13
    }
    for text, row_idx in icon_rows.items():
        cell = ws.cell(row=row_idx, column=1, value=text)
        if text == "Dashboard":
            cell.hyperlink = Hyperlink(ref=f"'{sheet_name}'!A1")
        elif text == "Inputs":
            cell.hyperlink = Hyperlink(ref=f"'Inputs'!A1")
        elif text == "Contacts":
            cell.hyperlink = Hyperlink(ref=f"'Contacts'!A1")
        elif text == "Email":
            cell.hyperlink = Hyperlink(ref=f"mailto:info@mcdonalds.com")
        elif text == "Support":
            cell.hyperlink = Hyperlink(ref=f"mailto:support@mcdonalds.com")
        
        # Apply font and align to mimic icon look
        apply_font(cell, size=10, bold=True, color=theme_colors.header_fg)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Main Dashboard Title Area
    ws.merge_cells(start_column=2, end_column=17, start_row=1, end_row=3)
    title_cell = ws.cell(row=1, column=2, value=f"{title} South America 2022")
    apply_font(title_cell, size=18, bold=True, color=theme_colors.text_color_dark)
    title_cell.alignment = Alignment(horizontal='left', vertical='center')
    ws.cell(row=2, column=2, value="Figures in millions of USD").font = Font(size=10, color="666666")


    # KPI Sections (3 sections with merged cells for background, then chart and values)
    kpi_section_col_starts = [2, 7, 12]
    kpi_section_titles = ["Sales", "Profit", "# of Customers"]
    kpi_data_col_starts = [2, 5, 8] # On Inputs sheet
    
    for i, col_start in enumerate(kpi_section_col_starts):
        # Background 'shape' for KPI
        ws.merge_cells(start_column=col_start, end_column=col_start+4, start_row=5, end_row=9)
        kpi_bg_cell = ws.cell(row=5, column=col_start)
        apply_fill(kpi_bg_cell, theme_colors.white)

        # KPI Title
        kpi_title_cell = ws.cell(row=5, column=col_start, value=kpi_section_titles[i])
        apply_font(kpi_title_cell, size=12, bold=True, color=theme_colors.text_color_dark)
        
        # KPI Value (e.g. $2,544)
        kpi_value_cell = ws.cell(row=7, column=col_start)
        kpi_value_cell.value = f"={inputs_ws.title}!{get_column_letter(kpi_data_col_starts[i])}5"
        kpi_value_cell.number_format = "$#,##0" if i != 2 else "0.0" # $ for sales/profit, decimal for customers
        apply_font(kpi_value_cell, size=24, bold=True, color=theme_colors.text_color_dark)
        kpi_value_cell.alignment = Alignment(horizontal='center', vertical='center')

        # Donut Chart
        donut_chart = DoughnutChart()
        donut_chart.title = None
        donut_chart.legend = None
        donut_chart.doughnutHoleSize = 65
        
        data = Reference(inputs_ws, min_col=kpi_data_col_starts[i]+1, min_row=7, max_row=8)
        labels = Reference(inputs_ws, min_col=kpi_data_col_starts[i], min_row=7, max_row=8) # Not used for labels, but needed

        donut_chart.add_data(data, titles_from_data=False)
        donut_chart.set_categories(labels)
        
        series = donut_chart.series[0]
        series.dLbls = openpyxl.chart.label.DataLabelList() # Ensure no labels are shown
        series.dLbls.showVal = False
        series.dLbls.showPercent = False
        
        series.dPt = [DataPoint(idx=0, spPr=GraphicalProperties(solidFill=theme_colors.accent_2)), # % Complete
                      DataPoint(idx=1, spPr=GraphicalProperties(solidFill=theme_colors.accent_3))] # Remainder
        
        donut_chart.width = 1.5
        donut_chart.height = 1.5
        
        ws.add_chart(donut_chart, get_column_letter(col_start+3) + str(6)) # Position next to value

        # KPI Percentage (e.g. 85%) - placed in a cell over the donut hole visually
        kpi_percent_cell = ws.cell(row=7, column=col_start+4)
        kpi_percent_cell.value = f"={inputs_ws.title}!{get_column_letter(kpi_data_col_starts[i])}7"
        kpi_percent_cell.number_format = '0%'
        apply_font(kpi_percent_cell, size=16, bold=True, color=theme_colors.text_color_dark)
        kpi_percent_cell.alignment = Alignment(horizontal='center', vertical='center')

    # 2021-2022 Sales Trend (Line Chart)
    ws.merge_cells(start_column=2, end_column=10, start_row=11, end_row=18)
    trend_bg_cell = ws.cell(row=11, column=2)
    apply_fill(trend_bg_cell, theme_colors.white)
    ws.cell(row=11, column=2, value="2021-2022 Sales Trend (in millions)").font = Font(bold=True, size=12, color=theme_colors.text_color_dark)

    line_chart = LineChart()
    line_chart.title = None
    line_chart.style = 10 # A style with markers
    
    labels = Reference(inputs_ws, min_col=2, min_row=17, max_row=28) # Months
    data = Reference(inputs_ws, min_col=3, min_row=16, max_col=4, max_row=28) # 2021 and 2022 sales
    
    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(labels)
    line_chart.x_axis.crosses = "min"
    line_chart.x_axis.tickLblPos = "low"
    line_chart.y_axis.scaling.min = 180 # As per video
    line_chart.y_axis.scaling.max = 250 # As per video

    # Customizing series colors and markers
    s1 = line_chart.series[0] # 2021 series
    s1.graphicalProperties.line.solidFill = theme_colors.accent_2 # Dark blue
    s1.marker = openpyxl.chart.marker.Marker(symbol='circle', size=5)
    s1.marker.graphicalProperties.solidFill = theme_colors.white
    s1.marker.graphicalProperties.line.solidFill = theme_colors.accent_2

    s2 = line_chart.series[1] # 2022 series
    s2.graphicalProperties.line.solidFill = theme_colors.accent_1 # Red
    s2.marker = openpyxl.chart.marker.Marker(symbol='circle', size=5)
    s2.marker.graphicalProperties.solidFill = theme_colors.white
    s2.marker.graphicalProperties.line.solidFill = theme_colors.accent_1

    line_chart.legend.position = 'b' # Bottom
    line_chart.width = 8.5
    line_chart.height = 5.5

    line_chart.layout = Layout(ManualLayout(
        x=0.04, y=0.15,
        h=0.8, w=0.9
    ))
    ws.add_chart(line_chart, "B12")


    # Customer Satisfaction (Radar Chart)
    ws.merge_cells(start_column=11, end_column=17, start_row=11, end_row=18)
    satisfaction_bg_cell = ws.cell(row=11, column=11)
    apply_fill(satisfaction_bg_cell, theme_colors.white)
    ws.cell(row=11, column=11, value="Customer Satisfaction").font = Font(bold=True, size=12, color=theme_colors.text_color_dark)

    radar_chart = RadarChart()
    radar_chart.title = None
    radar_chart.legend = None

    radar_data = Reference(inputs_ws, min_col=11, min_row=14, max_row=18)
    radar_categories = Reference(inputs_ws, min_col=10, min_row=14, max_row=18)
    
    radar_chart.add_data(radar_data, titles_from_data=False)
    radar_chart.set_categories(radar_categories)
    
    r_series = radar_chart.series[0]
    r_series.graphicalProperties.line.solidFill = theme_colors.accent_2 # Dark blue
    r_series.marker = openpyxl.chart.marker.Marker(symbol='circle', size=5)
    r_series.marker.graphicalProperties.solidFill = theme_colors.white
    r_series.marker.graphicalProperties.line.solidFill = theme_colors.accent_2

    radar_chart.width = 5.5
    radar_chart.height = 5.5

    radar_chart.layout = Layout(ManualLayout(
        x=0.04, y=0.15,
        h=0.8, w=0.9
    ))
    ws.add_chart(radar_chart, "L12")


    # Sales by Country (Map Chart) - Openpyxl does not support Map Charts directly
    ws.merge_cells(start_column=14, end_column=17, start_row=5, end_row=9)
    map_bg_cell = ws.cell(row=5, column=14)
    apply_fill(map_bg_cell, theme_colors.white)
    ws.cell(row=5, column=14, value="Sales by Country 2022").font = Font(bold=True, size=12, color=theme_colors.text_color_dark)
    ws.cell(row=7, column=14, value="[Map Chart Placeholder]").font = Font(size=10, color="666666", italic=True)
    ws.cell(row=8, column=14, value="Source: Inputs!F17:G23").font = Font(size=8, color="999999", italic=True)


    # Final aesthetic touches for all charts (no fill, no border for chart area)
    for chart in ws._charts:
        chart.graphicalProperties.noFill = True
        chart.graphicalProperties.noLine = True

    # Move Input and Contacts to end of sheets
    wb.active = ws
    wb.move_sheet(inputs_ws, offset=1)
    wb.move_sheet(contacts_ws, offset=1)
```