### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Interactive Sales Dashboard

*   **Tier**: sheet_shell
*   **Core Mechanism**: Renders a dynamic, single-sheet Excel dashboard featuring interactive navigation, key performance indicator (KPI) donut charts, a sales trend line chart, a customer satisfaction radar chart, and a geographical sales map. It consumes data from separate 'Inputs' and 'Contacts' sheets and applies consistent visual theming across all elements.
*   **Applicability**: Ideal for executive summaries and detailed operational reports that require a high-level overview with drill-down capabilities. Suitable for business and financial analysts needing to present complex data visually and interactively. Requires well-structured input data on dedicated sheets.

### 2. Structural Breakdown

-   **Data Layout**: The dashboard itself acts as a canvas. Data is sourced from two helper sheets:
    *   **Inputs**: Contains KPI actuals/targets, monthly sales figures for two years, sales by country, and customer satisfaction scores across various metrics.
    *   **Contacts**: Lists country managers and their email addresses.
-   **Formula Logic**:
    *   **KPI Percentage Complete**: Calculated as `Actual / Target` (e.g., `=Inputs!D2/Inputs!D3`).
    *   **KPI Remainder**: Calculated as `1 - % Complete` (e.g., `=1-Inputs!D4`).
    *   **Dynamic Text Boxes for KPIs**: Values are directly linked to the 'Inputs' sheet (e.g., `=Inputs!D2`).
-   **Visual Design**:
    *   **Navigation Bar (Column A)**: Solid fill with `theme.header_bg` (dark blue), font in `theme.header_fg` (white), bold. Icons (represented by text) are hyperlinked to other sheets or email addresses.
    *   **Dashboard Background**: No gridlines, main area is white (`theme.main_bg`).
    *   **Container Shapes**: Rounded rectangles (not directly supported by openpyxl, represented by drawing placeholders) with white fill, no outline, and a subtle shadow effect.
        *   Main title header.
        *   Three KPI overview boxes.
        *   Two larger chart boxes for trends and satisfaction.
        *   One smaller box for the map chart.
    *   **Text Formatting**: Titles within shapes use `theme.text_color` (dark blue), bold, and appropriate font sizes (e.g., 12-16pt for main titles, 10-12pt for chart subtitles).
-   **Charts/Tables**:
    *   **KPI Doughnut Charts (3 instances)**:
        *   Data: `% Complete` and `Remainder` from 'Inputs'.
        *   Style: No title, no legend. `% Complete` slice in `theme.kpi_complete_color` (dark blue), `Remainder` slice in `theme.kpi_remainder_color` (lighter greyish blue). Doughnut hole size set to 65%. Dynamic text box showing `% Complete` is placed in the center, linked to the corresponding cell. No chart area fill or border.
    *   **Sales Trend Line Chart (1 instance)**:
        *   Data: Months vs. 2021 & 2022 Sales from 'Inputs'.
        *   Style: Elegant chart design preset (style 3). 2021 line in `theme.accent_primary` (red), 2022 line in `theme.accent_secondary` (dark blue). Both lines have circular markers (white fill, matching line color border). Y-axis adjusted (e.g., min 180, max 230). No chart title or legend. No chart area fill or border.
    *   **Customer Satisfaction Radar Chart (1 instance)**:
        *   Data: Customer satisfaction metrics and their scores from 'Inputs'.
        *   Style: No chart title or legend. Line in `theme.accent_secondary` (dark blue) with circular markers (white fill, dark blue border). No chart area fill or border.
    *   **Sales by Country Map Chart (1 instance)**:
        *   Data: Countries in South America and their sales figures from 'Inputs'.
        *   Style: (Simulated using a placeholder in code as direct openpyxl map chart support is limited). Visually, a choropleth map with a blue color scale (darker blue for higher sales). No chart title or legend. No chart area fill or border.
-   **Theme Hooks**: `header_bg`, `header_fg`, `main_bg`, `text_color`, `accent_primary`, `accent_secondary`, `kpi_complete_color`, `kpi_remainder_color`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference, series, RadarChart, PieChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout

# Simplified Theme class and helper functions for demonstration
class Theme:
    def __init__(self, name="corporate_blue"):
        if name == "corporate_blue":
            self.header_bg = "1C2F52" # Dark Blue
            self.header_fg = "FFFFFF" # White
            self.main_bg = "FFFFFF" # White
            self.text_color = "1C2F52" # Dark Blue
            self.accent_primary = "EB5E55" # Red
            self.accent_secondary = "1C2F52" # Dark Blue
            self.kpi_complete_color = "1C2F52" # Dark Blue
            self.kpi_remainder_color = "D1D7DD" # Lighter Blue (greyish blue)
        else:
            # Default theme (for other names)
            self.header_bg = "1C2F52"
            self.header_fg = "FFFFFF"
            self.main_bg = "FFFFFF"
            self.text_color = "1C2F52"
            self.accent_primary = "EB5E55"
            self.accent_secondary = "1C2F52"
            self.kpi_complete_color = "1C2F52"
            self.kpi_remainder_color = "D1D7DD"

def create_solid_fill(color_hex):
    return PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")

def render_sheet(wb, sheet_name: str, *, title: str, theme_name: str = "corporate_blue", **kwargs) -> None:
    theme = Theme(theme_name)

    # --- Prepare mock data sheets if they don't exist ---
    if 'Inputs' not in wb.sheetnames:
        inputs_ws = wb.create_sheet("Inputs")
        _prepare_input_data(inputs_ws)
    else:
        inputs_ws = wb["Inputs"]

    if 'Contacts' not in wb.sheetnames:
        contacts_ws = wb.create_sheet("Contacts")
        _prepare_contact_data(contacts_ws)
    else:
        contacts_ws = wb["Contacts"]

    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    ws.title = sheet_name

    # --- 1. Basic Sheet Setup ---
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 8 # Navigation bar width
    for col_letter in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']:
        ws.column_dimensions[col_letter].width = 12

    # --- 2. Navigation Bar (Column A) ---
    for row_idx in range(1, 20): # Extend navigation bar height
        ws[f'A{row_idx}'].fill = create_solid_fill(theme.header_bg)

    nav_items = {
        "A1": ("McDonald's", "Dashboard"), # Logo placeholder
        "A5": ("📊 Dashboard", "Dashboard"),
        "A7": ("🗂 Inputs", "Inputs"),
        "A9": ("📧 Contacts", "Contacts"),
        "A11": ("❓ Help", "mailto:info@support.com")
    }

    for cell_ref, (text, link_target) in nav_items.items():
        cell = ws[cell_ref]
        cell.value = text
        cell.font = Font(color=theme.header_fg, bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        if link_target.startswith("mailto:"):
            cell.hyperlink = link_target
        else:
            cell.hyperlink = f"#'{link_target}'!A1"
        cell.style = "Hyperlink" # Apply default hyperlink style for underline/color

    # --- 3. Dashboard Structure (Simulated Shapes) ---
    # Using merged cells and applying fill/border to simulate shapes
    
    # Main Title Shape
    ws.merge_cells('B1:P3')
    title_cell = ws['B1']
    title_cell.fill = create_solid_fill(theme.main_bg)
    title_cell.border = Border(left=Side(), right=Side(), top=Side(), bottom=Side()) # Simulate shadow with borders
    
    ws['B1'].value = title
    ws['B1'].font = Font(color=theme.text_color, bold=True, size=16)
    ws['B2'].value = "Figures in millions of USD"
    ws['B2'].font = Font(color=theme.text_color, size=10)
    ws['B1'].alignment = Alignment(horizontal='left', vertical='center') # Title top left
    ws['B2'].alignment = Alignment(horizontal='left', vertical='center') # Subtitle below title


    # KPI Boxes
    kpi_box_ranges = ['B5:E9', 'F5:I9', 'J5:M9']
    kpi_titles = ['Sales', 'Profit', '# of Customers']
    for i, box_range in enumerate(kpi_box_ranges):
        ws.merge_cells(box_range)
        box_cell = ws[box_range.split(':')[0]]
        box_cell.fill = create_solid_fill(theme.main_bg)
        box_cell.border = Border(left=Side(), right=Side(), top=Side(), bottom=Side())
        box_cell.value = kpi_titles[i]
        box_cell.font = Font(color=theme.text_color, bold=True, size=12)
        box_cell.alignment = Alignment(horizontal='left', vertical='top') # Title at top left of box

    # Charts boxes
    ws.merge_cells('B11:I19') # 2021-2022 Sales Trend
    chart_box_cell = ws['B11']
    chart_box_cell.fill = create_solid_fill(theme.main_bg)
    chart_box_cell.border = Border(left=Side(), right=Side(), top=Side(), bottom=Side())
    ws['B11'].value = "2021-2022 Sales Trend (in millions)"
    ws['B11'].font = Font(color=theme.text_color, bold=True, size=12)
    chart_box_cell.alignment = Alignment(horizontal='left', vertical='top')

    ws.merge_cells('J11:M19') # Customer Satisfaction
    chart_box_cell = ws['J11']
    chart_box_cell.fill = create_solid_fill(theme.main_bg)
    chart_box_cell.border = Border(left=Side(), right=Side(), top=Side(), bottom=Side())
    ws['J11'].value = "Customer Satisfaction"
    ws['J11'].font = Font(color=theme.text_color, bold=True, size=12)
    chart_box_cell.alignment = Alignment(horizontal='left', vertical='top')

    ws.merge_cells('N5:P19') # Sales by Country (Map Chart)
    chart_box_cell = ws['N5']
    chart_box_cell.fill = create_solid_fill(theme.main_bg)
    chart_box_cell.border = Border(left=Side(), right=Side(), top=Side(), bottom=Side())
    ws['N5'].value = "Sales by Country 2022"
    ws['N5'].font = Font(color=theme.text_color, bold=True, size=12)
    chart_box_cell.alignment = Alignment(horizontal='left', vertical='top')

    # --- 4. Create and Customize Visuals ---

    # KPI Donut Charts
    kpi_donut_data_ranges = [
        inputs_ws['D4:D5'], # Sales % Complete, Remainder
        inputs_ws['G4:G5'], # Profit % Complete, Remainder
        inputs_ws['J4:J5'], # Customers % Complete, Remainder
    ]
    kpi_donut_chart_anchors = ['D6', 'H6', 'L6'] # Actual chart anchor
    kpi_value_display_anchors = ['C7', 'G7', 'K7'] # Text box anchor
    kpi_actual_value_cells = ['D2', 'G2', 'J2'] # Cell reference for text box

    for i, data_range in enumerate(kpi_donut_data_ranges):
        chart = PieChart()
        chart.type = "doughnut"
        chart.holeSize = 65
        chart.dLbls = DataLabelList()
        chart.dLbls.showCatName = False
        chart.dLbls.showVal = False
        chart.dLbls.showPercent = False
        chart.delete_legend()
        chart.title = None

        series_data = Reference(inputs_ws, min_col=data_range.min_col, min_row=data_range.min_row, max_row=data_range.max_row)
        chart.add_data(series_data, from_rows=False, titles_from_data=False)
        
        # Customize colors (first slice = complete, second = remainder)
        chart.series[0].dPts[0].graphicalProperties.solidFill = theme.kpi_complete_color
        chart.series[0].dPts[1].graphicalProperties.solidFill = theme.kpi_remainder_color
        
        chart.width = 3.5 # Width in Excel units (approx columns)
        chart.height = 3.5 # Height in Excel units (approx rows)
        
        ws.add_chart(chart, kpi_donut_chart_anchors[i])
        
        # Add dynamic text box for KPI percentage (e.g. 85%)
        pct_cell = ws[kpi_value_display_anchors[i]]
        pct_cell.value = f"={data_range.sheet.title}!{data_range.min_col_letter}{data_range.min_row}" # Link to % Complete
        pct_cell.font = Font(color=theme.text_color, bold=True, size=18)
        pct_cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Add dynamic text box for actual KPI value (e.g. $2,544)
        value_cell_anchor_row = int(kpi_value_display_anchors[i][1:]) - 2 # 2 rows above percentage
        value_cell = ws[f"{kpi_value_display_anchors[i][0]}{value_cell_anchor_row}"]
        value_cell.value = f"={inputs_ws.title}!{kpi_actual_value_cells[i]}"
        value_cell.font = Font(color=theme.text_color, bold=True, size=16)
        value_cell.alignment = Alignment(horizontal='center', vertical='center')
        value_cell.number_format = '"$"#,##0' # Example format

    # Sales Trend Line Chart
    line_chart = LineChart()
    line_chart.title = None
    line_chart.style = 3 # Chart style preset
    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.scaling.max = 230
    line_chart.y_axis.delete = False
    line_chart.x_axis.delete = False
    line_chart.delete_legend()

    dates = Reference(inputs_ws, min_col=1, min_row=22, max_row=33) # Jan-Dec
    data = Reference(inputs_ws, min_col=3, min_row=21, max_col=4, max_row=33) # 2021, 2022 figures

    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(dates)

    # Customize lines and markers for 2021 (Red)
    s1 = line_chart.series[0]
    s1.marker = series.Marker("circle")
    s1.marker.graphicalProperties.solidFill = "FFFFFF" # White fill
    s1.marker.graphicalProperties.ln.solidFill = theme.accent_primary # Red border
    s1.graphicalProperties.ln.solidFill = theme.accent_primary # Red line
    s1.graphicalProperties.ln.w = 25000 # ~1pt thickness

    # Customize lines and markers for 2022 (Dark Blue)
    s2 = line_chart.series[1]
    s2.marker = series.Marker("circle")
    s2.marker.graphicalProperties.solidFill = "FFFFFF" # White fill
    s2.marker.graphicalProperties.ln.solidFill = theme.accent_secondary # Dark blue border
    s2.graphicalProperties.ln.solidFill = theme.accent_secondary # Dark blue line
    s2.graphicalProperties.ln.w = 25000 # ~1pt thickness

    line_chart.width = 10.5
    line_chart.height = 7
    ws.add_chart(line_chart, "B12") # Place below the "2021-2022 Sales Trend" title


    # Customer Satisfaction Radar Chart
    radar_chart = RadarChart()
    radar_chart.title = None
    radar_chart.delete_legend()

    radar_labels = Reference(inputs_ws, min_col=1, min_row=37, max_row=41) # Speed to Availability
    radar_data = Reference(inputs_ws, min_col=3, min_row=36, max_row=41) # Scores

    radar_chart.add_data(radar_data, titles_from_data=True)
    radar_chart.set_categories(radar_labels)

    r_s1 = radar_chart.series[0]
    r_s1.marker = series.Marker("circle")
    r_s1.marker.graphicalProperties.solidFill = "FFFFFF" # White fill
    r_s1.marker.graphicalProperties.ln.solidFill = theme.accent_secondary # Dark blue border
    r_s1.graphicalProperties.ln.solidFill = theme.accent_secondary # Dark blue line
    r_s1.graphicalProperties.ln.w = 25000 # ~1pt thickness

    radar_chart.width = 6.5
    radar_chart.height = 7
    ws.add_chart(radar_chart, "J12") # Place below "Customer Satisfaction" title


    # Sales by Country Map Chart (simulated placeholder for visual structure)
    # Openpyxl doesn't directly support Map Charts. We'll add a simple drawing object
    # or a text placeholder to indicate its presence and position.
    map_placeholder = ws.drawing.add_drawing(None) # Generic drawing
    map_placeholder.anchor = 'N6'
    map_placeholder.width = 300
    map_placeholder.height = 200
    # You would typically place an image of a map here if possible
    # For now, let's add a text in a cell below the title to simulate content
    ws['N7'].value = "Map Chart (South America)"
    ws['N7'].font = Font(color=theme.text_color, italic=True)
    ws['N7'].alignment = Alignment(horizontal='center', vertical='center')


def _prepare_input_data(ws):
    # Mock data for Inputs sheet
    data = [
        ["KPIs", "", "Sales (M)", "Amount", "", "Profit", "Amount", "", "Customers", "Amount", "", "", "", "", "", ""],
        ["", "Actual", "", 2544, "", "Actual", "", 890, "", "Actual", "", 87.0, "", "", "", ""],
        ["", "Target", "", 3000, "", "Target", "", 1000, "", "Target", "", 100.0, "", "", "", ""],
        ["", "% Complete", "", "=D2/D3", "", "% Complete", "", "=G2/G3", "", "% Complete", "", "=J2/J3", "", "", "", ""],
        ["", "Remainder", "", "=1-D4", "", "Remainder", "", "=1-G4", "", "Remainder", "", "=1-J4", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Sales", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Figures in SA", "", "2021", "2022", "", "Sales by count Figures in SA", "", "", "", "Customer Satisfaction", "", "Score", "", "", "", ""],
        ["Jan", "", 201.9, 215.3, "", "Argentina", "", 953.3, "", "Speed (54%)", "", 54, "", "", "", ""],
        ["Feb", "", 204.2, 217.6, "", "Colombia", "", 453.2, "", "Quality (86%)", "", 86, "", "", "", ""],
        ["Mar", "", 198.6, 220.1, "", "Brazil", "", 553.2, "", "Hygiene (93%)", "", 93, "", "", "", ""],
        ["Apr", "", 206.4, 204.3, "", "Ecuador", "", 445.3, "", "Service (53%)", "", 53, "", "", "", ""],
        ["May", "", 199.2, 206.4, "", "Peru", "", 253.6, "", "Availability (95%)", "", 95, "", "", "", ""],
        ["Jun", "", 195.3, 203.0, "", "Chile", "", 253.6, "", "", "", "", "", "", "", ""],
        ["Jul", "", 186.3, 200.6, "", "Bolivia", "", 387.5, "", "", "", "", "", "", "", ""],
        ["Aug", "", 194.2, 210.0, "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Sep", "", 199.2, 206.4, "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Oct", "", 205.2, 222.3, "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Nov", "", 210.6, 222.5, "", "", "", "", "", "", "", "", "", "", "", ""],
        ["Dec", "", 225.8, 230.1, "", "", "", "", "", "", "", "", "", "", "", ""]
    ]
    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, cell_value in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=cell_value)

    # Apply number formats
    for cell_ref in ['D2', 'G2', 'J2']:
        ws[cell_ref].number_format = '"$"#,##0'
    for cell_ref in ['D4', 'D5', 'G4', 'G5', 'J4', 'J5']:
        ws[cell_ref].number_format = '0%'

def _prepare_contact_data(ws):
    # Mock data for Contacts sheet
    data = [
        ["Country", "General Manager", "Email"],
        ["Argentina", "Facundo Gonzalez", "f.gonzalez@mcdonalds.com"],
        ["Colombia", "Radael Lopez", "r.lopez@mcdonalds.com"],
        ["Brazil", "Joao Silva", "j.silva@mcdonalds.com"],
        ["Ecuador", "Jaime Loor", "j.loor@mcdonalds.com"],
        ["Peru", "Samuel Armando", "s.armando@mcdonalds.com"],
        ["Chile", "Alvaro Sanchez", "a.sanchez@mcdonalds.com"],
        ["Bolivia", "Angel Garcia", "a.garcia@mcdonalds.com"]
    ]
    for row in data:
        ws.append(row)
```