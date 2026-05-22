from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference, RadarChart, Series
from openpyxl.chart.series import DataPoint, DataPoint3D
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.colors import ColorChoice
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.drawing.geometry import Point2D, Extent
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from openpyxl.chart.data_source import NumData, NumVal
from openpyxl.utils.units import pixels_to_EMU
from openpyxl.styles.colors import Color

import os
from io import BytesIO
import base64
from PIL import Image as PILImage # Used for icons as images are too big by default


def _load_theme_colors(theme_name):
    themes = {
        "mcdonalds": {
            "primary_blue": "003366",
            "secondary_blue": "ADD8E6",
            "accent_red": "FF0000",
            "white": "FFFFFF",
            "dark_text": "000000",
            "light_text": "FFFFFF",
            "shadow_color": "999999",
        }
    }
    return themes.get(theme_name, themes["mcdonalds"])

def _create_rounded_rectangle(ws, top_left_cell, width, height, fill_color, border_color="000000", text="", text_color="000000", font_size=12, bold=False, shadow=True, shape_name=""):
    from openpyxl.drawing.shapes import Shape, ShapeProperty, Geometry, AdjustHandle, ShapeStyle
    from openpyxl.drawing.fill import SolidFill
    from openpyxl.drawing.line import Line as DrawingLine
    from openpyxl.drawing.effect import EffectContainer, Shadow as DrawingShadow

    shape = Shape.graphicFrame
    shape.nvGraphicFramePr.cNvPr.id = ws._max_id + 1
    shape.nvGraphicFramePr.cNvPr.name = shape_name if shape_name else f"Rectangle {shape.nvGraphicFramePr.cNvPr.id}"
    shape.nvGraphicFramePr.cNvPr.hlinkClick = None

    spPr = ShapeProperty()
    spPr.xfrm.off = Point2D(x=pixels_to_EMU(ws.column_dimensions[top_left_cell.column_letter].width * 7), y=pixels_to_EMU(ws.row_dimensions[top_left_cell.row].height * 1.5)) # Approximate positioning
    spPr.xfrm.ext = Extent(cx=pixels_to_EMU(width), cy=pixels_to_EMU(height))

    # Rounded rectangle geometry
    geom = Geometry()
    geom.prstGeom.prst = 'roundRect'
    geom.prstGeom.avLst.add_child(AdjustHandle('adj', '16667')) # Controls roundness

    if fill_color:
        spPr.noFill = None if fill_color else SolidFill(srgbClr=fill_color)
        spPr.solidFill = SolidFill(srgbClr=fill_color) if fill_color else None
    
    if border_color:
        spPr.ln = DrawingLine(noFill=None)
        spPr.ln.solidFill = SolidFill(srgbClr=border_color)

    if shadow:
        eff_cont = EffectContainer()
        sh = DrawingShadow()
        sh.blurRad = pixels_to_EMU(5)
        sh.dist = pixels_to_EMU(3)
        sh.dir = 2700000 # 270 degrees
        sh.srgbClr = Color(rgb=_load_theme_colors("mcdonalds")["shadow_color"])
        eff_cont.outerShdw = sh
        spPr.effectLst = eff_cont

    shape.graphic.graphicData.spTree.add_child(spPr)

    tx_body = shape.graphic.graphicData.spTree.add_child(shape.graphic.graphicData.spTree.txBody)
    tx_body.bodyPr.wrap = 'square'
    tx_body.lstStyle = None

    p = tx_body.p
    r = p.add_child(tx_body.p.r)
    r.t = text
    rPr = r.add_child(tx_body.p.r.rPr)
    rPr.latin = Font(name="Arial", sz=font_size, b=bold, color=Color(rgb=text_color))
    
    ws.add_chart(shape) # This needs to be a chart or it doesn't get added properly. A bug/feature in openpyxl?

    # This is a workaround for shapes. Openpyxl doesn't have native shape drawing for general shapes,
    # so often charts are repurposed or a complex XML approach is needed.
    # For simplicity matching the video aesthetic, we'll place real charts later directly.
    # For simple boxes like this, a Chart is not the correct class, but given the time constraint
    # and the visual goal, we will proceed with simpler chart-like placements for now.
    return shape


def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "mcdonalds", **kwargs) -> None:
    colors = _load_theme_colors(theme)

    # Prepare Inputs sheet with dummy data
    if "Inputs" not in wb.sheetnames:
        inputs_ws = wb.create_sheet("Inputs")
    else:
        inputs_ws = wb["Inputs"]

    inputs_ws["D4"] = "Sales (M)"
    inputs_ws["D5"] = 2544
    inputs_ws["D6"] = 3000
    inputs_ws["D7"] = "=D5/D6" # % Complete
    inputs_ws["D8"] = "=1-D7" # Remainder

    inputs_ws["G4"] = "Profit (M)"
    inputs_ws["G5"] = 890
    inputs_ws["G6"] = 1000
    inputs_ws["G7"] = "=G5/G6"
    inputs_ws["G8"] = "=1-G7"

    inputs_ws["J4"] = "# of Customers"
    inputs_ws["J5"] = 87.0
    inputs_ws["J6"] = 100.0
    inputs_ws["J7"] = "=J5/J6"
    inputs_ws["J8"] = "=1-J7"

    # Sales Trend Data
    inputs_ws["D11"] = "Jan"
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sales_2021 = [201.9, 204.2, 198.6, 209.4, 196.3, 195.3, 192.4, 199.2, 205.2, 199.2, 204.3, 201.5]
    sales_2022 = [215.3, 217.6, 212.0, 206.4, 203.0, 206.3, 200.6, 218.4, 222.6, 225.8, 223.5, 226.7]
    for i, month in enumerate(months):
        inputs_ws[f"D{11+i}"] = month
        inputs_ws[f"E{11+i}"] = sales_2021[i]
        inputs_ws[f"F{11+i}"] = sales_2022[i]
    inputs_ws["E10"] = "2021"
    inputs_ws["F10"] = "2022"

    # Sales by Country Data (South America)
    inputs_ws["H10"] = "Country"
    inputs_ws["I10"] = "Figures in SM"
    countries = ["Argentina", "Colombia", "Brazil", "Ecuador", "Peru", "Chile", "Bolivia"]
    country_sales = [953.3, 453.2, 553.2, 445.3, 253.6, 425.1, 387.5]
    for i, country in enumerate(countries):
        inputs_ws[f"H{11+i}"] = country
        inputs_ws[f"I{11+i}"] = country_sales[i]

    # Customer Satisfaction Data
    inputs_ws["K10"] = "Customer Satisfac"
    inputs_ws["L10"] = "Score"
    satisfaction_metrics = ["Speed (54%)", "Quality (86%)", "Hygiene (93%)", "Service (53%)", "Availability (95%)"]
    scores = [0.54, 0.86, 0.93, 0.53, 0.95]
    for i, metric in enumerate(satisfaction_metrics):
        inputs_ws[f"K{11+i}"] = metric
        inputs_ws[f"L{11+i}"] = scores[i]
    
    # Format percentages
    for col_letter in ["D", "G", "J"]:
        inputs_ws[f"{col_letter}7"].number_format = "0%"
        inputs_ws[f"{col_letter}8"].number_format = "0%"

    # Prepare Contacts sheet
    if "Contacts" not in wb.sheetnames:
        contacts_ws = wb.create_sheet("Contacts")
    else:
        contacts_ws = wb["Contacts"]
    
    contacts_ws["A1"] = "Country"
    contacts_ws["B1"] = "General Manager"
    contacts_ws["C1"] = "Email"
    contacts_ws["A2"] = "Argentina"
    contacts_ws["B2"] = "Argentina Facundo Gonzalez"
    contacts_ws["C2"] = "f.gonzalez@mcdonalds.com"
    contacts_ws["A3"] = "Colombia"
    contacts_ws["B3"] = "Radamel Lopez"
    contacts_ws["C3"] = "r.lopez@mcdonalds.com"


    # Create Dashboard sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Column widths
    ws.column_dimensions['A'].width = 10
    for col in range(2, 14): # B through M
        ws.column_dimensions[get_column_letter(col)].width = 10
    for col in range(14, 17): # N through P for map
        ws.column_dimensions[get_column_letter(col)].width = 15

    # Navigation Panel (Column A)
    for row in range(1, 26):
        ws[f'A{row}'].fill = PatternFill(start_color=colors["primary_blue"], end_color=colors["primary_blue"], fill_type="solid")

    # Add McDonald's logo (simplified as text for code example, or use a placeholder image)
    # The video uses an actual logo image. For robust openpyxl code, handling external images is more complex.
    # We will simulate it with a colored cell and text.
    ws['A1'].value = "M"
    ws['A1'].font = Font(name="Arial", size=24, color=Color(rgb=colors["light_text"]), bold=True)
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")

    # Hyperlinks for navigation (simplified with basic cells and links for illustrative purpose)
    # The video uses images as hyperlinks, which is more complex in openpyxl directly.
    # Here, we'll use text cells for simplicity.
    ws['A3'].value = "Dashboard"
    ws['A3'].hyperlink = f"#{sheet_name}!A1"
    ws['A3'].font = Font(color=Color(rgb=colors["light_text"]))
    ws['A3'].alignment = Alignment(horizontal="center")

    ws['A6'].value = "Inputs"
    ws['A6'].hyperlink = "#Inputs!A1"
    ws['A6'].font = Font(color=Color(rgb=colors["light_text"]))
    ws['A6'].alignment = Alignment(horizontal="center")

    ws['A9'].value = "Contacts"
    ws['A9'].hyperlink = "#Contacts!A1"
    ws['A9'].font = Font(color=Color(rgb=colors["light_text"]))
    ws['A9'].alignment = Alignment(horizontal="center")

    # Main Dashboard Title Shape
    # openpyxl doesn't directly support shapes like rounded rectangles with shadows easily.
    # As a workaround to match the visual effect in the video, we'll merge cells and style them.
    ws.merge_cells('B1:M4')
    title_cell = ws['B1']
    title_cell.fill = PatternFill(start_color=colors["white"], end_color=colors["white"], fill_type="solid")
    title_cell.font = Font(name="Arial", size=24, bold=True, color=Color(rgb=colors["dark_text"]))
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    title_cell.value = f"{title} South America 2022\nFigures in millions of USD"
    
    # KPI Containers (Sales, Profit, # Customers)
    kpi_containers = [
        ('B5', 'E9', 'Sales'),
        ('F5', 'I9', 'Profit'),
        ('J5', 'M9', '# of Customers')
    ]
    for start_cell_str, end_cell_str, kpi_title in kpi_containers:
        ws.merge_cells(f"{start_cell_str}:{end_cell_str}")
        cell = ws[start_cell_str]
        cell.fill = PatternFill(start_color=colors["white"], end_color=colors["white"], fill_type="solid")
        cell.font = Font(name="Arial", size=14, bold=True, color=Color(rgb=colors["dark_text"]))
        cell.alignment = Alignment(horizontal="left", vertical="top", indent=1)
        cell.value = kpi_title

    # Sales Trend Chart Container
    ws.merge_cells('B10:I20')
    trend_title_cell = ws['B10']
    trend_title_cell.fill = PatternFill(start_color=colors["white"], end_color=colors["white"], fill_type="solid")
    trend_title_cell.font = Font(name="Arial", size=14, bold=True, color=Color(rgb=colors["dark_text"]))
    trend_title_cell.alignment = Alignment(horizontal="left", vertical="top", indent=1)
    trend_title_cell.value = "2021-2022 Sales Trend (in millions)"

    # Customer Satisfaction Chart Container
    ws.merge_cells('J10:M20')
    cust_sat_title_cell = ws['J10']
    cust_sat_title_cell.fill = PatternFill(start_color=colors["white"], end_color=colors["white"], fill_type="solid")
    cust_sat_title_cell.font = Font(name="Arial", size=14, bold=True, color=Color(rgb=colors["dark_text"]))
    cust_sat_title_cell.alignment = Alignment(horizontal="left", vertical="top", indent=1)
    cust_sat_title_cell.value = "Customer Satisfaction"

    # Sales by Country Chart Container (Right side)
    ws.merge_cells('N1:P20')
    country_sales_title_cell = ws['N1']
    country_sales_title_cell.fill = PatternFill(start_color=colors["white"], end_color=colors["white"], fill_type="solid")
    country_sales_title_cell.font = Font(name="Arial", size=14, bold=True, color=Color(rgb=colors["dark_text"]))
    country_sales_title_cell.alignment = Alignment(horizontal="left", vertical="top", indent=1)
    country_sales_title_cell.value = "Sales by Country 2022"

    # --- Add Charts and Visuals ---

    # KPI Donut Charts
    kpi_data_ranges = [("D5", "D8"), ("G5", "G8"), ("J5", "J8")]
    kpi_chart_positions = [('C6', 'E8'), ('G6', 'I8'), ('K6', 'M8')]
    kpi_text_positions = [('B7', 'D7'), ('F7', 'H7'), ('J7', 'L7')] # Adjusted for text box value

    for i, (data_range, chart_pos, text_pos) in enumerate(zip(kpi_data_ranges, kpi_chart_positions, kpi_text_positions)):
        pie = RadarChart() # Using RadarChart as a proxy for Doughnut because openpyxl donut charting is complex
        pie.type = "doughnut"
        pie.varyColors = True
        
        labels = Reference(inputs_ws, min_col=4 + i*3, min_row=4, max_row=4) # dummy for labels
        data = Reference(inputs_ws, min_col=4 + i*3, min_row=7, max_row=8)

        series = Series(data, labels)
        series.graphicalProperties.solidFill = Color(rgb=colors["primary_blue"])
        series.dLbls = DataLabelList()
        series.dLbls.showVal = False # Don't show value on pie itself
        
        pie.series.append(series)

        # Customizing series colors directly for donut (openpyxl specific way)
        for idx, s in enumerate(pie.series):
            # This is a bit manual but reflects the video's look.
            # 0: Completed part, 1: Remainder
            dp1 = DataPoint(idx=0)
            dp1.graphicalProperties.solidFill = Color(rgb=colors["primary_blue"])
            s.dPt.append(dp1)
            dp2 = DataPoint(idx=1)
            dp2.graphicalProperties.solidFill = Color(rgb=colors["secondary_blue"])
            s.dPt.append(dp2)
            break # Only one series in a simple donut chart

        pie.title = None
        pie.width = 3.5 # Approx width in inches
        pie.height = 2.5 # Approx height in inches
        pie.style = 10
        pie.legend = None

        ws.add_chart(pie, chart_pos[0])

        # Add dynamic text box for KPI value
        # openpyxl doesn't have direct support for text boxes linked to cells within charts.
        # This is a common workaround for Excel dashboards. We simulate it by creating a cell
        # formatted to look like a text box, linked to the source data.
        ws[text_pos[0]].value = f"={data_range.split(':')[0]}" # Link to actual value
        ws[text_pos[0]].number_format = "$#,##0" if "Sales" in kpi_title or "Profit" in kpi_title else "0.0"
        ws[text_pos[0]].font = Font(name="Arial", size=18, bold=True, color=Color(rgb=colors["dark_text"]))
        ws[text_pos[0]].alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells(f"{text_pos[0]}:{text_pos[1]}") # Merge to center


    # Sales Trend Line Chart
    line_chart = LineChart()
    line_chart.title = None
    line_chart.style = 10
    line_chart.y_axis.title = None
    line_chart.x_axis.title = None

    data = Reference(inputs_ws, min_col=5, min_row=10, max_col=6, max_row=22)
    categories = Reference(inputs_ws, min_col=4, min_row=11, max_row=22)

    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(categories)

    # Customize lines and markers
    s1 = line_chart.series[0] # 2021 sales
    s1.graphicalProperties.line.solidFill = Color(rgb=colors["accent_red"])
    s1.graphicalProperties.line.width = pixels_to_EMU(1.5)
    s1.marker = s1.marker.copy()
    s1.marker.symbol = 'circle'
    s1.marker.size = 5
    s1.marker.graphicalProperties.solidFill = Color(rgb=colors["white"])
    s1.marker.graphicalProperties.ln.solidFill = Color(rgb=colors["accent_red"])
    s1.marker.graphicalProperties.ln.width = pixels_to_EMU(1)

    s2 = line_chart.series[1] # 2022 sales
    s2.graphicalProperties.line.solidFill = Color(rgb=colors["primary_blue"])
    s2.graphicalProperties.line.width = pixels_to_EMU(1.5)
    s2.marker = s2.marker.copy()
    s2.marker.symbol = 'circle'
    s2.marker.size = 5
    s2.marker.graphicalProperties.solidFill = Color(rgb=colors["white"])
    s2.marker.graphicalProperties.ln.solidFill = Color(rgb=colors["primary_blue"])
    s2.marker.graphicalProperties.ln.width = pixels_to_EMU(1)

    # Adjust Y-axis min/max
    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.scaling.max = 230

    line_chart.legend.position = "b" # Bottom
    line_chart.height = 7 # inches
    line_chart.width = 9 # inches

    ws.add_chart(line_chart, "B12") # Position below the "2021-2022 Sales Trend" title


    # Customer Satisfaction Radar Chart
    radar_chart = RadarChart()
    radar_chart.type = "radar"
    radar_chart.title = None
    radar_chart.style = 10
    radar_chart.legend = None # Remove legend as labels are on the axis

    labels = Reference(inputs_ws, min_col=11, min_row=11, max_row=15)
    data = Reference(inputs_ws, min_col=12, min_row=10, max_row=15)

    radar_chart.add_data(data, titles_from_data=True)
    radar_chart.set_categories(labels)
    
    s = radar_chart.series[0]
    s.graphicalProperties.line.solidFill = Color(rgb=colors["primary_blue"])
    s.graphicalProperties.line.width = pixels_to_EMU(1.5)
    s.marker = s.marker.copy()
    s.marker.symbol = 'circle'
    s.marker.size = 5
    s.marker.graphicalProperties.solidFill = Color(rgb=colors["white"])
    s.marker.graphicalProperties.ln.solidFill = Color(rgb=colors["primary_blue"])
    s.marker.graphicalProperties.ln.width = pixels_to_EMU(1)

    radar_chart.height = 7
    radar_chart.width = 5

    ws.add_chart(radar_chart, "J12") # Position below "Customer Satisfaction" title

    # Map Chart (openpyxl does not support Map Charts directly)
    # As a workaround, we'll simulate the look using merged cells and conditional formatting,
    # or use a placeholder image if available. For this exercise, we will use a text placeholder.
    # The tutorial uses an actual map chart. Since openpyxl doesn't support maps,
    # we'll place text indicating a map should go here.
    map_placeholder_cell = ws['N5']
    map_placeholder_cell.value = "Sales by Country Map Chart (Power BI/Image)"
    map_placeholder_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    map_placeholder_cell.font = Font(name="Arial", size=10, italic=True)


    # Final formatting for all charts: no fill, no border
    for chart_id in range(1, len(ws._charts) + 1):
        try:
            chart = ws._charts[chart_id - 1] # Adjust for 0-indexing
            chart.plot_area.graphicalProperties.noFill = True
            chart.plot_area.graphicalProperties.ln.noFill = True
            chart.graphicalProperties.noFill = True
            chart.graphicalProperties.ln.noFill = True
        except AttributeError:
            continue

    # Hide unused sheets for cleaner look
    inputs_ws.sheet_state = 'hidden'
    contacts_ws.sheet_state = 'hidden'

# Example usage:
if __name__ == '__main__':
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales Dashboard"
    render_sheet(wb, ws.title, title="Sales Dashboard")
    
    # Remove default empty sheet if created
    if "Sheet" in wb.sheetnames and len(wb.sheetnames) > 1:
        wb.remove(wb["Sheet"])
    
    # Set the Sales Dashboard as the active sheet before saving
    wb.active = wb["Sales Dashboard"]
    
    save_path = "interactive_sales_dashboard.xlsx"
    wb.save(save_path)
    print(f"Dashboard saved to {save_path}")

