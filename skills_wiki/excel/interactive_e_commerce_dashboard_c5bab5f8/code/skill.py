import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference, PieChart
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from openpyxl_image_loader import SheetImageLoader # External dependency for logo, not strictly openpyxl
from openpyxl.chart.shapes import Shape, GraphicalProperties
from openpyxl.drawing.line import Line as DrawingLine
from openpyxl.drawing.fill import ColorChoice, GradientFillProperties, Stop, LinearShadeProperties
from openpyxl.chart.axis import ChartLines
from openpyxl.chart.updown_bars import UpDownBars
from openpyxl.chart.data_source import NumData, NumVal
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.title import ChartTitle
from openpyxl.chart.trendline import Trendline
from openpyxl.chart.layout import Layout, ManualLayout

# Mock theme_loader and _helpers for self-containment
class ThemePalette:
    def __init__(self, theme_name):
        self.theme_name = theme_name
        self.colors = {
            "corporate_blue": {
                "header_bg": "FF002060", "page_bg": "FFDDEEFF",
                "accent_1": "FF0070C0", "accent_2": "FFED7D31", "accent_3": "FFA5A5A5",
                "accent_4": "FFFFC000", "accent_5": "FF4472C4", "accent_6": "FF70AD47",
                "text_dark": "FF000000", "text_light": "FFFFFFFF"
            },
            "VivaCalf": { # Custom theme based on video
                "header_bg": "FF356A2D", "page_bg": "FFDDFAE8",
                "accent_1": "FF4E89F0", "accent_2": "FFFF9933", "accent_3": "FFCC0000",
                "accent_4": "FF7C9F68", "accent_5": "FFD4AC0D", "accent_6": "FF2E6A2B",
                "text_dark": "FF000000", "text_light": "FFFFFFFF"
            }
        }
    def get_color(self, name):
        return self.colors.get(self.theme_name, self.colors["corporate_blue"]).get(name, "FF000000")

def get_fill(hex_color):
    return PatternFill(start_color=hex_color[2:], end_color=hex_color[2:], fill_type="solid")

def get_font(color="FF000000", bold=False, size=11):
    return Font(color=color[2:], bold=bold, size=size)

def get_border(color="FF000000", style="thin"):
    return Border(left=Side(style=style, color=color[2:]),
                  right=Side(style=style, color=color[2:]),
                  top=Side(style=style, color=color[2:]),
                  bottom=Side(style=style, color=color[2:]))

class SlicerCache: # Mock SlicerCache for demo
    def __init__(self, name):
        self.name = name
        self.pivotTables = []

def Slicer(name):
    return SlicerCache(name)

# --- End Mock Helpers ---

def render_workbook(wb, *, title: str = "E-commerce Dashboard", theme: str = "VivaCalf", **kwargs) -> None:
    palette = ThemePalette(theme)

    # 1. Setup Data Sheet
    ws_data = wb.create_sheet("Data", 0)
    ws_data.title = "Data"
    # Mocking data, in a real scenario this would be loaded from a file/DB
    ws_data.append(["TX ID", "Product", "Quantity", "Unit Price", "Amount", "Order Date", "Ship Date", "Customer Gender", "Order Mode", "Rating C", "State", "County"])
    sample_data = [
        ["TX00001", "Shorts", 2, 30.6, 61.2, "1-Jan-25", "1-Jan-25", "F", "App", 5, "California", "Alpine County"],
        ["TX00002", "Tank Tops", 3, 31.2, 93.6, "1-Jan-25", "1-Jan-25", "M", "App", 4, "California", "Contra Costa County"],
        ["TX00003", "Shorts", 1, 38.9, 38.9, "1-Jan-25", "3-Jan-25", "F", "App", 3, "California", "Fresno County"],
        ["TX00004", "Workout Tops", 2, 19.4, 38.8, "1-Jan-25", "4-Jan-25", "F", "App", 5, "California", "Los Angeles County"],
        ["TX00005", "Sneakers", 7, 50.7, 354.9, "1-Jan-25", "4-Jan-25", "M", "Website", 4, "California", "Los Angeles County"],
        ["TX00006", "Graphic Tees", 12, 83, 996, "1-Jan-25", "4-Jan-25", "F", "Target.com", 3, "California", "Los Angeles County"],
        ["TX00007", "Jeans", 3, 56.7, 170.1, "1-Jan-25", "4-Jan-25", "M", "App", 4, "California", "Los Angeles County"],
        ["TX00008", "Tank Tops", 2, 31.2, 62.4, "1-Jan-25", "4-Jan-25", "F", "Website", 3, "California", "Los Angeles County"],
        ["TX00009", "Jeans", 8, 40.3, 322.4, "1-Jan-25", "4-Jan-25", "M", "App", 4, "California", "Los Angeles County"],
        ["TX00010", "Hoodies & Sweatshirts", 11, 55.7, 612.7, "1-Jan-25", "5-Jan-25", "F", "Instagram", 5, "California", "Nevada County"],
        ["TX00011", "Sundresses", 7, 22.4, 156.8, "1-Jan-25", "5-Jan-25", "F", "App", 4, "California", "Placer County"],
        ["TX00012", "Sundresses", 27, 20.4, 550.8, "1-Jan-25", "5-Jan-25", "M", "Website", 3, "California", "Sacramento County"],
        ["TX00013", "Bikinis", 2, 49, 98, "1-Jan-25", "5-Jan-25", "F", "App", 5, "California", "San Benito County"],
        ["TX00014", "Jeans", 8, 40.3, 322.4, "1-Jan-25", "6-Jan-25", "M", "Website", 4, "California", "San Bernardino County"],
        ["TX00015", "Sandals", 18, 33.9, 610.2, "1-Jan-25", "6-Jan-25", "F", "Target.com", 3, "California", "San Bernardino County"],
        # Add more sample data for a robust dashboard, this is just a snippet
    ]
    for row_data in sample_data:
        ws_data.append(row_data)

    # Add calculated columns
    ws_data["M1"] = "Days to Deliver"
    ws_data["N1"] = "Weeknum"
    ws_data["O1"] = "Gender Value"
    for row_idx in range(2, ws_data.max_row + 1):
        ws_data[f"M{row_idx}"] = f"=[@[Ship Date]]-[@[Order Date]]"
        ws_data[f"N{row_idx}"] = f"=WEEKNUM([@[Order Date]])"
        ws_data[f"O{row_idx}"] = f'=IFS([@[Customer Gender]]="M","Male",[@[Customer Gender]]="F","Female",[@[Customer Gender]]="O","Other",TRUE,"Unknown")'

    # Create table for raw data
    tab = Table(displayName="Salesdata", ref=f"A1:{get_column_letter(ws_data.max_column)}{ws_data.max_row}")
    style = TableStyleInfo(name="TableStyleLight10", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)

    # 2. Setup Pivots Sheet
    ws_pivots = wb.create_sheet("Pivots")
    ws_pivots.title = "Pivots"

    # Create PivotTables (simplified for demo, full implementation would involve more code)
    # Pivot for Summary KPIs (placed at A1)
    # pvfSummary = PivotTable(pivotCache=wb.pivotCaches.add(sourceRef="Salesdata", sheet="Data"), name="pvfSummary")
    # pvfSummary.add_row_field("Count of TX ID") # This isn't how openpyxl adds fields, just illustrative
    # ws_pivots.add_pivot(pvfSummary)
    # This section would dynamically generate PivotTables
    # For demonstration, let's just mock the output cells of the pivots for display purposes.

    # Mock PivotTable output in Pivots sheet for dashboard linking
    ws_pivots['A4'] = 2400 # Orders
    ws_pivots['B4'] = 11997 # Quantity
    ws_pivots['C4'] = 649019.8 # Amount
    ws_pivots['D4'] = 3.96 # Avg Rating
    ws_pivots['E4'] = 2.3425 # Avg Days to Deliver

    # Mock data for weekly trends PivotTable
    ws_pivots['A11'] = "Weeknum"
    ws_pivots.append(["Weeknum", "Sum of Quantity", "Sum of Amount"])
    for i in range(1, 14): # 13 weeks of data
        ws_pivots.append([i, i * 100 + i * 5, i * 1000 + i * 50])
    
    # Mock data for gender-mode heatmap PivotTable
    ws_pivots['A20'] = "Order Mode"
    ws_pivots.append(["", "Female", "Male", "Other", "Unknown"])
    ws_pivots.append(["App", 0.19, 0.123, 0.011, 0.031])
    ws_pivots.append(["Instagram", 0.05, 0.043, 0.002, 0.018])
    ws_pivots.append(["Partner App", 0.063, 0.048, 0.002, 0.004])
    ws_pivots.append(["Target.com", 0.096, 0.068, 0.005, 0.013])
    ws_pivots.append(["Website", 0.125, 0.093, 0.006, 0.012])

    # Mock data for map chart source (Quantity)
    ws_pivots['G84'] = "State"
    ws_pivots['H84'] = "County"
    ws_pivots['I84'] = "Qty"
    ws_pivots.append(["California", "Alameda County", 91])
    ws_pivots.append(["California", "Los Angeles County", 553])
    ws_pivots.append(["California", "San Diego County", 300])
    # ... more counties ...
    ws_pivots.append(["California", "Yolo County", 4])
    # Add dummy zero rows for counties not present in filtered data, to avoid map errors
    for i in range(10):
        ws_pivots.append(["", "", 0])

    # Add IF logic to the map chart source data to handle blanks from filters
    for r in range(85, ws_pivots.max_row + 1):
        ws_pivots[f'G{r}'] = f'=IF(A{r}="","",A{r})'
        ws_pivots[f'H{r}'] = f'=IF(B{r}="","",B{r})'
        ws_pivots[f'I{r}'] = f'=IF(C{r}="","",C{r})'

    # 3. Setup Dashboard Sheet
    ws_dashboard = wb.create_sheet("Dashboard")
    ws_dashboard.title = "Dashboard"

    # Set column widths for layout
    ws_dashboard.column_dimensions['A'].width = 3
    ws_dashboard.column_dimensions['B'].width = 18
    ws_dashboard.column_dimensions['C'].width = 3
    for col_idx in range(4, 30): # columns D to AC for charts
        ws_dashboard.column_dimensions[get_column_letter(col_idx)].width = 5

    # Background shapes
    sidebar_shape = ws_dashboard.drawing.add_picture(Shape(), "B2") # Mock adding shape
    sidebar_shape.width = 150 # Adjust as needed
    sidebar_shape.height = 700
    # Simulate filling color
    # ws_dashboard.cell(row=2, column=2).fill = get_fill(palette.get_color("header_bg"))

    main_canvas_shape = ws_dashboard.drawing.add_picture(Shape(), "D2") # Mock adding shape
    main_canvas_shape.width = 1000
    main_canvas_shape.height = 700
    # Simulate filling color
    # ws_dashboard.cell(row=2, column=4).fill = get_fill(palette.get_color("page_bg"))

    # KPI Panel
    ws_dashboard['B2'].value = "VIVA CALIF"
    ws_dashboard['B2'].font = get_font(palette.get_color("text_light"), bold=True, size=24)
    ws_dashboard['B2'].fill = get_fill(palette.get_color("header_bg"))

    # Orders KPI
    ws_dashboard['B4'].value = "2,400" # Linked from Pivots!A4, as in formula logic
    ws_dashboard['B4'].font = get_font(palette.get_color("text_light"), bold=True, size=18)
    ws_dashboard['B5'].value = "Orders"
    ws_dashboard['B5'].font = get_font(palette.get_color("text_light"), size=10)

    # Quantity KPI
    ws_dashboard['B7'].value = "11,997" # Linked from Pivots!B4
    ws_dashboard['B7'].font = get_font(palette.get_color("text_light"), bold=True, size=18)
    ws_dashboard['B8'].value = "Quantity"
    ws_dashboard['B8'].font = get_font(palette.get_color("text_light"), size=10)

    # Amount KPI (Golden color)
    ws_dashboard['B10'].value = "$649.0k" # Linked from Pivots!C4
    ws_dashboard['B10'].font = get_font(palette.get_color("accent_5"), bold=True, size=18) # Golden accent
    ws_dashboard['B11'].value = "Amount"
    ws_dashboard['B11'].font = get_font(palette.get_color("text_light"), size=10)

    # Add other KPIs (Avg. Rating, Avg. Days to Deliver) in a similar fashion.

    # Add Slicers (simplified for demo)
    # slicer_order_mode = Slicer("Order Mode")
    # slicer_gender = Slicer("Gender Value")
    # ws_dashboard.add_slicer(slicer_order_mode)
    # ws_dashboard.add_slicer(slicer_gender)
    # Position slicers in the sidebar

    # Mock slices for visualization
    ws_dashboard['B20'].value = "Order Mode"
    ws_dashboard['B21'].value = "App"
    ws_dashboard['B22'].value = "Instagram"
    ws_dashboard['B23'].value = "Partner App"
    ws_dashboard['B24'].value = "Target.com"
    ws_dashboard['B25'].value = "Website"
    ws_dashboard['B20'].font = get_font(palette.get_color("text_light"), bold=True, size=12)
    ws_dashboard['B20'].fill = get_fill(palette.get_color("accent_1"))
    for r in range(21, 26):
        ws_dashboard[f'B{r}'].fill = get_fill(palette.get_color("accent_1"))
        ws_dashboard[f'B{r}'].font = get_font(palette.get_color("text_light"))
        ws_dashboard.merge_cells(f'B{r}:C{r}')

    ws_dashboard['B28'].value = "Customer Gender"
    ws_dashboard['B29'].value = "Female"
    ws_dashboard['B30'].value = "Male"
    ws_dashboard['B31'].value = "Other"
    ws_dashboard['B32'].value = "Unknown"
    ws_dashboard['B28'].font = get_font(palette.get_color("text_light"), bold=True, size=12)
    ws_dashboard['B28'].fill = get_fill(palette.get_color("accent_6"))
    for r in range(29, 33):
        ws_dashboard[f'B{r}'].fill = get_fill(palette.get_color("accent_6"))
        ws_dashboard[f'B{r}'].font = get_font(palette.get_color("text_light"))
        ws_dashboard.merge_cells(f'B{r}:C{r}')


    # Add Charts (Illustrative, full code for each chart is extensive)

    # Line Chart: Last 13 Week Trends
    c1 = LineChart()
    c1.title = "Last 13 Week Trends - Qty & Amount"
    c1.style = 10
    c1.x_axis.title = "Weeknum"
    c1.y_axis.title = "Quantity"
    c1.y_axis[0].majorGridlines = None
    c1.y_axis[0].number_format = '#,##0'

    data_qty = Reference(ws_pivots, min_col=2, min_row=12, max_col=2, max_row=24)
    data_amount = Reference(ws_pivots, min_col=3, min_row=12, max_col=3, max_row=24)
    cats = Reference(ws_pivots, min_col=1, min_row=12, max_col=1, max_row=24)

    s1 = c1.add_data(data_qty, titles_from_data=True)
    s2 = c1.add_data(data_amount, titles_from_data=True)
    c1.set_categories(cats)
    s2.marker.symbol = "triangle"
    s2.graphical_properties.line.noFill = False
    s2.graphical_properties.line.solidFill = ColorChoice(srgbClr=palette.get_color("accent_2")[2:]) # Orange
    s1.graphical_properties.line.solidFill = ColorChoice(srgbClr=palette.get_color("accent_1")[2:]) # Blue
    c1.height = 8 # inches
    c1.width = 15 # inches
    ws_dashboard.add_chart(c1, "D4")

    # Heatmap (Paste as Linked Picture)
    # The actual heatmap is on the Pivots sheet, formatted with conditional formatting.
    # It's copied and pasted as a linked picture onto the dashboard.
    # Mock visual representation on dashboard
    ws_dashboard['P4'].value = "How they like to buy?"
    ws_dashboard['P4'].font = get_font(palette.get_color("text_dark"), bold=True)
    ws_dashboard['P4'].fill = get_fill(palette.get_color("page_bg")) # Chart background
    ws_dashboard.merge_cells('P4:U4')
    # Actual linked picture would be added here:
    # img = Image(ws_pivots.sheet_ranges['A20:E25']) # Pseudo code for linking a range as image
    # ws_dashboard.add_image(img, "P5")


    # Bar Chart: Which Products are Popular?
    # Similar setup to line chart, using BarChart and adjusting properties.

    # Map Chart: Where our customers live?
    # Requires an external library or specific Excel version features for dynamic map charts.
    # For openpyxl, this is complex. The video's workaround uses helper ranges and then inserts the map.
    # Mock visuals for demo
    ws_dashboard['D25'].value = "Where do our customers live?"
    ws_dashboard['D25'].font = get_font(palette.get_color("text_dark"), bold=True)
    ws_dashboard['D25'].fill = get_fill(palette.get_color("page_bg"))
    ws_dashboard.merge_cells('D25:I25')

    # Adding interactivity (linking slicers to PivotTables)
    # This requires iterating through PivotTables and setting up ReportConnections.
    # For demo purposes, this is a conceptual step in openpyxl as direct slicer manipulation is complex.

    # Final formatting and titles (covered by the archetypal approach)

    # Make the Dashboard sheet active and hide gridlines
    ws_dashboard.sheet_view.showGridLines = False
    wb.active = ws_dashboard

