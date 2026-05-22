### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Themed Sales Dashboard Sheet

*   **Tier**: sheet_shell
*   **Core Mechanism**: Builds a single, interactive dashboard sheet with a predefined layout, including navigation icons linked to other sheets, and dynamically updated placeholders for key performance indicators (KPIs), trend charts, and geographical maps. It uses themed shapes and dynamically linked text boxes to display live data, presenting a comprehensive overview of business metrics.
*   **Applicability**: Useful for creating executive summaries, sales reports, or any dashboard requiring a structured layout, dynamic navigation, and visually appealing presentation of KPIs and trends, often for a specific region or business unit. It's best for scenarios where the underlying data is prepared in separate input sheets, allowing for easy updates and consistency.

### 2. Structural Breakdown

-   **Data Layout**: The dashboard sheet itself is primarily visual, receiving data from an 'Inputs' sheet (e.g., `Inputs!C3`, `Inputs!E3`, `Inputs!G3` for KPIs, `Inputs!A10:C22` for sales trend, `Inputs!E10:F17` for sales by country, `Inputs!H10:I15` for customer satisfaction). A narrow left column is dedicated to navigation icons. The main content area is structured with a header, three KPI boxes, two larger chart areas, and one medium map chart area.
-   **Formula Logic**:
    *   **Hyperlinks for navigation**: Icons are hyperlinked to sheets within the workbook (e.g., `#'Inputs'!A1`) or external URLs/email addresses (`mailto:info@support.com`).
    *   **Dynamic text boxes for KPI values**: Text boxes for actual amounts are linked directly to cells on the 'Inputs' sheet (e.g., `=Inputs!C3`).
    *   **Donut chart percentages**: The chart data on the 'Inputs' sheet is calculated as `Actual / Target` and `1 - (Actual / Target)` for the 'completed' and 'remainder' segments, respectively. The percentage text within the donut is also dynamically linked.
-   **Visual Design**:
    *   **Background**: White for the main canvas, dark blue for the navigation sidebar.
    *   **Shapes**: Rounded rectangles (simulated with merged cells and fill due to openpyxl limitations) with white fill and a subtle shadow effect.
    *   **Text**: Dark blue, bolded titles (e.g., "Sales Dashboard South America 2022"). Smaller text for figure units. Dynamically linked KPI values are large, bold, and dark blue.
    *   **Icons**: White text placeholders on a dark blue background in the navigation sidebar.
    *   **Donut Charts**: Blue and orange segments, thick donut hole, white fill, no border. Dynamic text box showing percentage in dark blue, centered.
    *   **Line Chart (Sales Trend)**: Two lines (red for 2021, dark blue for 2022 trends) with circular white-filled markers bordered in their respective line colors. Chart area has no fill or border. Y-axis minimum is set to 180.
    *   **Radar Chart (Customer Satisfaction)**: Dark blue line with circular white-filled markers bordered in dark blue. Chart area has no fill or border. Y-axis is deleted.
    *   **Map Chart (Sales by Country)**: Filled map of South America (simulated with a bar chart), shades of blue for sales by country, no legend displayed, no fill/border for the chart area.
-   **Charts/Tables**:
    *   **Donut Chart**: `openpyxl.chart.PieChart` (specifically, `doughnut`) for KPI completion rates. Data range `Inputs!C5:C6` (and similar for Profit/Customers).
    *   **Line Chart**: `openpyxl.chart.LineChart` for 2021-2022 sales trend. Data range `Inputs!A11:C22`.
    *   **Radar Chart**: `openpyxl.chart.LineChart` configured to represent a radar chart. Data range `Inputs!H11:I15`.
    *   **Map Chart**: `openpyxl.chart.BarChart` (column type) used as a placeholder to represent a map chart. Data range `Inputs!E11:F17`.
-   **Theme Hooks**:
    *   `header_bg`: Dark blue for sidebar, also used for navigation text.
    *   `primary_text`: Dark blue for titles, KPI values, and chart text.
    *   `accent_color_1`: Red for 2021 line chart, orange for donut chart remainder.
    *   `accent_color_2`: Dark blue for 2022 line chart, blue for donut chart completion, radar chart line, map chart gradient (bar chart fill).
    *   `lighter_accent_2`: Lighter blue for remainder in donut chart.
    *   `neutral_bg`: White for main content shapes.
    *   `shadow_color`: Grey for simulated shadow effect.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import PieChart, Reference, LineChart, Series, BarChart
from openpyxl.utils import get_column_letter

# Simplified theme palette for self-contained code
def get_theme_palette(theme_name: str):
    palettes = {
        "corporate_blue": {
            "header_bg": "FF002060",
            "neutral_bg": "FFFFFFFF",
            "primary_text": "FF002060",
            "accent_color_1": "FFE69F00", # Orange (for donut remainder, 2021 line)
            "accent_color_2": "FF0072B2", # Dark Blue (for donut complete, 2022 line, radar, map)
            "lighter_accent_2": "FF56B4E9", # Lighter Blue (for some chart elements)
            "shadow_color": "FF666666" # Grey for shadows (conceptual, openpyxl limited)
        }
    }
    return palettes.get(theme_name, palettes["corporate_blue"])

# Placeholder for complex shape creation and shadow effects
# Direct complex shape features (like rounded corners and shadows) are limited in openpyxl.
# For full fidelity, pre-rendered images or more advanced XML manipulation would be needed.
def create_dashboard_box(ws, start_cell: str, end_cell: str, fill_color_hex: str, border_color_hex: str = None, title: str = None):
    ws.merge_cells(f"{start_cell}:{end_cell}")
    cell = ws[start_cell]
    cell.fill = PatternFill(start_color=fill_color_hex[2:], end_color=fill_color_hex[2:], fill_type="solid")
    if border_color_hex:
        thin_border = Border(left=Side(style='thin', color=border_color_hex[2:]),
                             right=Side(style='thin', color=border_color_hex[2:]),
                             top=Side(style='thin', color=border_color_hex[2:]),
                             bottom=Side(style='thin', color=border_color_hex[2:]))
        for row in ws[f"{start_cell}:{end_cell}"]:
            for c in row:
                c.border = thin_border
    if title:
        cell.value = title
        cell.font = Font(color=get_theme_palette("corporate_blue")["primary_text"][2:], bold=True, size=12)
        cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    palette = get_theme_palette(theme)
    ws = wb.create_sheet(sheet_name)
    ws.sheet_properties.pageSetup.fitToHeight = 1
    ws.sheet_properties.pageSetup.fitToWidth = 1
    ws.views.sheetView[0].showGridLines = False

    # --- Create dummy data for 'Inputs' sheet if it doesn't exist ---
    if "Inputs" not in wb.sheetnames:
        inputs_ws = wb.create_sheet("Inputs")
        inputs_ws.title = "Inputs"
        inputs_ws["B2"] = "Sales (M)"
        inputs_ws["C2"] = "Amount"
        inputs_ws["D2"] = "Profit"
        inputs_ws["E2"] = "Amount"
        inputs_ws["F2"] = "Customers"
        inputs_ws["G2"] = "Amount"

        inputs_ws["C3"] = 2544 # Actual Sales
        inputs_ws["C4"] = 3000 # Target Sales
        inputs_ws["C5"].value = inputs_ws["C3"].value / inputs_ws["C4"].value # % Complete
        inputs_ws["C6"].value = 1 - inputs_ws["C5"].value # Remainder
        inputs_ws["C5"].number_format = '0%'
        inputs_ws["C6"].number_format = '0%'

        inputs_ws["E3"] = 890 # Actual Profit
        inputs_ws["E4"] = 1000 # Target Profit
        inputs_ws["E5"].value = inputs_ws["E3"].value / inputs_ws["E4"].value # % Complete
        inputs_ws["E6"].value = 1 - inputs_ws["E5"].value # Remainder
        inputs_ws["E5"].number_format = '0%'
        inputs_ws["E6"].number_format = '0%'

        inputs_ws["G3"] = 87.0 # Actual Customers
        inputs_ws["G4"] = 100.0 # Target Customers
        inputs_ws["G5"].value = inputs_ws["G3"].value / inputs_ws["G4"].value # % Complete
        inputs_ws["G6"].value = 1 - inputs_ws["G5"].value # Remainder
        inputs_ws["G5"].number_format = '0%'
        inputs_ws["G6"].number_format = '0%'
        
        inputs_ws["A10"] = "Figures in SM"
        inputs_ws["B10"] = "2021"
        inputs_ws["C10"] = "2022"
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        sales_2021 = [201.9, 204.2, 198.6, 196.4, 205.3, 195.3, 192.4, 199.2, 206.4, 199.8, 204.3, 205.5]
        sales_2022 = [215.3, 217.6, 220.1, 206.4, 204.3, 203.0, 199.6, 200.6, 213.0, 214.6, 222.3, 225.6]
        for i, month in enumerate(months):
            inputs_ws[f"A{11+i}"] = month
            inputs_ws[f"B{11+i}"] = sales_2021[i]
            inputs_ws[f"C{11+i}"] = sales_2022[i]

        inputs_ws["E10"] = "Country"
        inputs_ws["F10"] = "Figures in SM"
        countries = ["Argentina", "Colombia", "Brazil", "Ecuador", "Peru", "Chile", "Bolivia"]
        country_sales = [953.3, 453.2, 553.2, 445.3, 253.6, 253.6, 387.5]
        for i, country in enumerate(countries):
            inputs_ws[f"E{11+i}"] = country
            inputs_ws[f"F{11+i}"] = country_sales[i]

        inputs_ws["H10"] = "Customer Satisfaction"
        inputs_ws["I10"] = "Score"
        satisfaction_factors = ["Speed (54%)", "Quality (86%)", "Hygiene (93%)", "Service (53%)", "Availability (95%)"]
        satisfaction_scores = [0.54, 0.86, 0.93, 0.53, 0.95]
        for i, factor in enumerate(satisfaction_factors):
            inputs_ws[f"H{11+i}"] = factor
            inputs_ws[f"I{11+i}"] = satisfaction_scores[i]

        contacts_ws = wb.create_sheet("Contacts")
        contacts_ws.title = "Contacts"
        contacts_ws["A1"] = "Country"
        contacts_ws["B1"] = "General Manager"
        contacts_ws["C1"] = "Email"
        contacts_data = [
            ("Argentina", "Agustina Facundo Gonzalez", "a.gonzalez@mcdonalds.com"),
            ("Colombia", "Radianel Lopez", "r.lopez@mcdonalds.com"),
            ("Brazil", "Joao Silva", "j.silva@mcdonalds.com"),
            ("Ecuador", "Jaime Lome", "j.lome@mcdonalds.com"),
            ("Peru", "Samuel Armando", "s.armando@mcdonalds.com"),
            ("Chile", "Alvaro Sanchez", "a.sanchez@mcdonalds.com"),
            ("Bolivia", "Angel Garcia", "a.garcia@mcdonalds.com")
        ]
        for r_idx, row_data in enumerate(contacts_data):
            for c_idx, cell_value in enumerate(row_data):
                contacts_ws.cell(row=r_idx + 2, column=c_idx + 1, value=cell_value)
        
        # Set column widths for Inputs and Contacts for better readability
        inputs_ws.column_dimensions['A'].width = 15
        inputs_ws.column_dimensions['B'].width = 15
        inputs_ws.column_dimensions['C'].width = 15
        inputs_ws.column_dimensions['D'].width = 15
        inputs_ws.column_dimensions['E'].width = 25
        inputs_ws.column_dimensions['F'].width = 15
        inputs_ws.column_dimensions['G'].width = 15
        inputs_ws.column_dimensions['H'].width = 20
        inputs_ws.column_dimensions['I'].width = 10
        contacts_ws.column_dimensions['A'].width = 15
        contacts_ws.column_dimensions['B'].width = 25
        contacts_ws.column_dimensions['C'].width = 30

    # --- Sidebar for navigation (Column A) ---
    ws.column_dimensions['A'].width = 5
    for row_num in range(1, ws.max_row + 100):
        ws[f'A{row_num}'].fill = PatternFill(start_color=palette["header_bg"][2:], end_color=palette["header_bg"][2:], fill_type="solid")

    ws['A1'] = "M" # Placeholder for logo
    ws['A1'].font = Font(color="FFFFFFFF", bold=True, size=24)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    icon_cells = ["A6", "A8", "A10", "A12", "A14"]
    icon_labels = ["Dashboard", "Inputs", "Contacts", "Email", "Help"]
    sheet_links = [sheet_name, "Inputs", "Contacts", "mailto:info@support.com", "https://careerprinciples.com"]

    for i, cell_ref in enumerate(icon_cells):
        ws[cell_ref].value = icon_labels[i]
        ws[cell_ref].font = Font(color="FFFFFFFF", size=8)
        ws[cell_ref].alignment = Alignment(horizontal='center', vertical='center')
        if sheet_links[i].startswith("mailto") or sheet_links[i].startswith("http"):
            ws[cell_ref].hyperlink = sheet_links[i]
        else:
            ws[cell_ref].hyperlink = f"#'{sheet_links[i]}'!A1"

    # --- Dashboard Main Header (B1:M3) ---
    create_dashboard_box(ws, "B1", "M3", palette["neutral_bg"])
    header_cell = ws['B1']
    header_cell.value = f"{title} South America 2022"
    header_cell.font = Font(color=palette["primary_text"][2:], bold=True, size=24)
    header_cell.alignment = Alignment(horizontal='left', vertical='center')
    ws['B4'].value = "Figures in millions of USD"
    ws['B4'].font = Font(color=palette["primary_text"][2:], size=10)

    # --- Dashboard Content Boxes (simulated with merged cells) ---
    # KPI Boxes
    kpi_boxes = {
        "Sales": {"range": "B6:D9", "label_cell": "B6", "value_cell": "C3", "donut_ref_complete": "C5", "donut_ref_remainder": "C6"},
        "Profit": {"range": "E6:G9", "label_cell": "E6", "value_cell": "E3", "donut_ref_complete": "E5", "donut_ref_remainder": "E6"},
        "# of Customers": {"range": "H6:J9", "label_cell": "H6", "value_cell": "G3", "donut_ref_complete": "G5", "donut_ref_remainder": "G6"}
    }

    col_offsets = {"Sales": 0, "Profit": 3, "Customers": 6}

    for idx, (kpi_name, props) in enumerate(kpi_boxes.items()):
        create_dashboard_box(ws, props["range"].split(':')[0], props["range"].split(':')[1], palette["neutral_bg"], palette["shadow_color"])
        
        ws[props["label_cell"]].value = kpi_name
        ws[props["label_cell"]].font = Font(color=palette["primary_text"][2:], bold=True, size=12)
        ws[props["label_cell"]].alignment = Alignment(horizontal='left', vertical='top')

        # KPI Value
        kpi_value_cell_dashboard = ws.cell(row=6, column=2 + col_offsets[kpi_name])
        kpi_value_cell_dashboard.value = f"='Inputs'!{props['value_cell']}"
        kpi_value_cell_dashboard.font = Font(color=palette["primary_text"][2:], bold=True, size=18)
        kpi_value_cell_dashboard.alignment = Alignment(horizontal='center', vertical='center')

        # Donut Chart for % Complete
        pie = PieChart()
        pie.title = None
        pie.type = "pie"
        pie.d_series[0].doughnutHoleSize = 65

        # Data for donut chart
        donut_data = Reference(wb["Inputs"], min_col=openpyxl.utils.cell.column_and_row_from_cell_name(props["donut_ref_complete"])[0], min_row=openpyxl.utils.cell.column_and_row_from_cell_name(props["donut_ref_complete"])[1], max_row=openpyxl.utils.cell.column_and_row_from_cell_name(props["donut_ref_remainder"])[1])
        pie.add_data(donut_data, titles_from_data=False)
        
        # Color the segments
        pie.d_series[0].d_points[0].graphicalProperties.solidFill = palette["accent_color_2"][2:] # Completed
        pie.d_series[0].d_points[1].graphicalProperties.solidFill = palette["lighter_accent_2"][2:] # Remainder
        pie.d_series[0].explosion = 0 # No explosion

        # Position donut chart
        chart_anchor_col_start = openpyxl.utils.cell.column_and_row_from_cell_name(props["range"].split(':')[0])[0]
        ws.add_chart(pie, get_column_letter(chart_anchor_col_start + 1) + '6')

        # Dynamic percentage text inside donut
        percent_cell_dashboard = ws.cell(row=7, column=chart_anchor_col_start + 3)
        percent_cell_dashboard.value = f"='Inputs'!{props['donut_ref_complete']}"
        percent_cell_dashboard.number_format = '0%'
        percent_cell_dashboard.font = Font(color=palette["primary_text"][2:], bold=True, size=16)
        percent_cell_dashboard.alignment = Alignment(horizontal='center', vertical='center')


    # 2021-2022 Sales Trend (Line Chart)
    create_dashboard_box(ws, "B11", "J20", palette["neutral_bg"], palette["shadow_color"], "2021-2022 Sales Trend (in millions)")
    line_chart = LineChart()
    line_chart.title = None
    line_chart.style = 10 # Elegant style
    line_chart.height = 10 # pixels, adjust as needed
    line_chart.width = 20 # pixels, adjust as needed
    
    x_data = Reference(wb["Inputs"], min_col=1, min_row=11, max_row=22)
    y_data_2021 = Reference(wb["Inputs"], min_col=2, min_row=10, max_row=22)
    y_data_2022 = Reference(wb["Inputs"], min_col=3, min_row=10, max_row=22)
    
    series_2021 = Series(y_data_2021, title="2021")
    series_2022 = Series(y_data_2022, title="2022")
    
    series_2021.graphicalProperties.line.solidFill = palette["accent_color_1"][2:]
    series_2021.marker.symbol = 'circle'
    series_2021.marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    series_2021.marker.graphicalProperties.line.solidFill = palette["accent_color_1"][2:] # Red border

    series_2022.graphicalProperties.line.solidFill = palette["accent_color_2"][2:]
    series_2022.marker.symbol = 'circle'
    series_2022.marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    series_2022.marker.graphicalProperties.line.solidFill = palette["accent_color_2"][2:] # Blue border

    line_chart.append(series_2021)
    line_chart.append(series_2022)
    line_chart.set_categories(x_data)

    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.majorGridlines = None
    line_chart.x_axis.majorGridlines = None
    line_chart.y_axis.title = "Sales (in millions)"
    line_chart.x_axis.title = "Month"

    ws.add_chart(line_chart, "C12")


    # Customer Satisfaction (Radar Chart - simulated with LineChart)
    create_dashboard_box(ws, "K11", "M20", palette["neutral_bg"], palette["shadow_color"], "Customer Satisfaction")
    radar_chart = LineChart() # Using LineChart as a stand-in for RadarChart
    radar_chart.title = None
    radar_chart.style = 10
    
    radar_categories = Reference(wb["Inputs"], min_col=8, min_row=11, max_row=15)
    radar_values = Reference(wb["Inputs"], min_col=9, min_row=10, max_row=15)
    
    radar_series = Series(radar_values, title="Score")
    radar_series.graphicalProperties.line.solidFill = palette["accent_color_2"][2:]
    radar_series.marker.symbol = 'circle'
    radar_series.marker.graphicalProperties.solidFill = "FFFFFFFF"
    radar_series.marker.graphicalProperties.line.solidFill = palette["accent_color_2"][2:]
    
    radar_chart.append(radar_series)
    radar_chart.set_categories(radar_categories)
    radar_chart.y_axis.delete = True # Remove Y-axis numbers to resemble radar
    radar_chart.x_axis.majorGridlines = None
    radar_chart.y_axis.majorGridlines = None

    ws.add_chart(radar_chart, "K12")


    # Sales by Country Map (Bar Chart - simulated for visual layout)
    create_dashboard_box(ws, "K6", "M10", palette["neutral_bg"], palette["shadow_color"], "Sales by Country 2022")
    map_chart = BarChart() # Using BarChart as a stand-in for MapChart
    map_chart.type = "col"
    map_chart.style = 10
    map_chart.title = None
    map_chart.y_axis.title = "Sales (in millions)"
    map_chart.x_axis.title = "Country"
    map_chart.legend = None # No legend for map chart
    
    countries_ref = Reference(wb["Inputs"], min_col=5, min_row=11, max_row=17)
    sales_ref = Reference(wb["Inputs"], min_col=6, min_row=10, max_row=17)

    series_sales = Series(sales_ref, title="Figures in SM")
    series_sales.graphicalProperties.solidFill = palette["accent_color_2"][2:] # Blue fill
    
    map_chart.append(series_sales)
    map_chart.set_categories(countries_ref)
    
    ws.add_chart(map_chart, "K6")

    # Adjusting column widths for the main dashboard content
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 12
    ws.column_dimensions['I'].width = 12
    ws.column_dimensions['J'].width = 12
    ws.column_dimensions['K'].width = 15
    ws.column_dimensions['L'].width = 15
    ws.column_dimensions['M'].width = 15
```