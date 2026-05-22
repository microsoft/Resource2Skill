import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference, DoughnutChart, BarChart, RadarChart
from openpyxl.chart.series import DataPoint, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.marker import Marker
from openpyxl.drawing.text import RichText, Paragraph, ParagraphProperties, CharacterProperties, TextPoint
from openpyxl.drawing.fill import SolidColor
from openpyxl.drawing.spreadsheet_drawing import Anchor
from openpyxl.drawing.image import Image as OpenpyxlImage # For potential future image support
from openpyxl.drawing.shape import Shape as OpenpyxlShape # For shapes like textboxes
from openpyxl.utils import get_column_letter

# Helper for theme colors (mocked as if loaded from _helpers)
def _get_theme_colors(theme_name):
    themes = {
        "corporate_blue": {
            "header_bg": "FF213F60",  # Dark Blue
            "header_fg": "FFFFFFFF",  # White
            "sidebar_bg": "FF213F60", # Dark Blue
            "text_color_dark": "FF213F60", # Dark Blue
            "accent_red": "FFDA4453", # Red
            "accent_blue_dark": "FF4285F4", # Google Blue
            "accent_blue_light": "FFADD8E6", # Light Blue
            "white": "FFFFFFFF",      # White
            "light_grey": "FFD3D3D3", # Light Grey
            "dark_grey": "FF696969",  # Dark Grey (unused but good to have)
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_dashboard_sheet(wb, sheet_name: str = "Dashboard", *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name, 0)
    colors = _get_theme_colors(theme)

    # --- Setup Sheet Structure ---
    ws.sheet_view.showGridLines = False

    # Column A for navigation (simulated with color and text links)
    ws.column_dimensions['A'].width = 8
    for row_idx in range(1, 30): # Apply color to a reasonable range
        ws[f'A{row_idx}'].fill = PatternFill(start_color=colors['sidebar_bg'], end_color=colors['sidebar_bg'], fill_type="solid")
    
    # Navigation links (as text placeholders for icons)
    link_font = Font(name='Calibri', size=11, color=colors['white'], underline='single')
    ws['A5'].value = "Dashboard"
    ws['A5'].hyperlink = f"#{sheet_name}!A1"
    ws['A5'].font = link_font
    ws['A5'].alignment = Alignment(horizontal='center', vertical='center')

    ws['A7'].value = "Inputs"
    ws['A7'].hyperlink = "#Inputs!A1"
    ws['A7'].font = link_font
    ws['A7'].alignment = Alignment(horizontal='center', vertical='center')
    
    ws['A9'].value = "Contacts"
    ws['A9'].hyperlink = "#Contacts!A1"
    ws['A9'].font = link_font
    ws['A9'].alignment = Alignment(horizontal='center', vertical='center')

    ws['A11'].value = "Email Support"
    ws['A11'].hyperlink = "mailto:info@support.com"
    ws['A11'].font = link_font
    ws['A11'].alignment = Alignment(horizontal='center', vertical='center')


    # Set column widths for content area
    col_widths = {'B': 8, 'C': 10, 'D': 10, 'E': 10, 'F': 10, 'G': 10, 'H': 10, 'I': 10, 'J': 10, 'K': 10, 'L': 10, 'M': 10, 'N': 1}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # Row heights
    ws.row_dimensions[1].height = 20
    ws.row_dimensions[2].height = 25 # Main title row
    ws.row_dimensions[3].height = 15 # Sub-title row

    # --- Create "Inputs" and "Contacts" sheets for mock data and hyperlinks ---
    inputs_ws = wb.create_sheet("Inputs", 1)
    inputs_ws.sheet_view.showGridLines = False
    inputs_ws.sheet_state = 'hidden' # Hide inputs sheet as per video

    contacts_ws = wb.create_sheet("Contacts", 2)
    contacts_ws.sheet_view.showGridLines = False
    contacts_ws['A1'] = "Contact Information"
    contacts_ws['A1'].font = Font(name='Calibri', size=24, bold=True, color=colors['text_color_dark'])
    contacts_ws.sheet_state = 'hidden' # Hide contacts sheet

    # Mock Data on Inputs Sheet
    # KPIs
    inputs_ws['D5'] = 2544
    inputs_ws['D6'] = 3000
    inputs_ws['D7'] = inputs_ws['D5'].value / inputs_ws['D6'].value # 85%
    inputs_ws['G5'] = 890
    inputs_ws['G6'] = 1000
    inputs_ws['G7'] = inputs_ws['G5'].value / inputs_ws['G6'].value # 89%
    inputs_ws['J5'] = 87
    inputs_ws['J6'] = 100
    inputs_ws['J7'] = inputs_ws['J5'].value / inputs_ws['J6'].value # 87%

    # Sales Trend (monthly)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sales_2021 = [201.9, 204.2, 198.6, 199.2, 195.3, 192.4, 190.2, 199.2, 204.4, 209.6, 215.3, 220.3]
    sales_2022 = [215.3, 217.6, 220.1, 206.4, 203.3, 200.6, 201.3, 206.4, 212.8, 219.0, 225.6, 230.8]
    inputs_ws['B20'] = "Month"; inputs_ws['C20'] = 2021; inputs_ws['D20'] = 2022
    for i, month in enumerate(months):
        inputs_ws[f'B{21+i}'] = month
        inputs_ws[f'C{21+i}'] = sales_2021[i]
        inputs_ws[f'D{21+i}'] = sales_2022[i]

    # Sales by Country (for Map chart - simulated with Bar Chart data)
    countries = ["Argentina", "Colombia", "Brazil", "Ecuador", "Peru", "Chile", "Bolivia"]
    country_sales = [953.3, 453.2, 553.2, 445.3, 253.6, 387.5, 300.0]
    inputs_ws['F20'] = "Country"; inputs_ws['G20'] = "Sales"
    for i, country in enumerate(countries):
        inputs_ws[f'F{21+i}'] = country
        inputs_ws[f'G{21+i}'] = country_sales[i]

    # Customer Satisfaction
    satisfaction = {"Speed": 0.54, "Quality": 0.96, "Hygiene": 0.93, "Service": 0.53, "Availability": 0.95}
    inputs_ws['J11'] = "Category"; inputs_ws['K11'] = "Score"
    for i, (cat, score) in enumerate(satisfaction.items()):
        inputs_ws[f'J{12+i}'] = f"{cat} ({int(score*100)}%)"
        inputs_ws[f'K{12+i}'] = score

    # --- Header Section ---
    ws.merge_cells('B2:M2')
    header_cell = ws['B2']
    header_cell.value = f"{title} South America 2022"
    header_cell.font = Font(name='Calibri', size=24, bold=True, color=colors['header_fg'])
    header_cell.fill = PatternFill(start_color=colors['header_bg'], end_color=colors['header_bg'], fill_type="solid")
    header_cell.alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('B3:M3')
    sub_header_cell = ws['B3']
    sub_header_cell.value = "Figures in millions of USD"
    sub_header_cell.font = Font(name='Calibri', size=12, color=colors['header_fg'])
    sub_header_cell.fill = PatternFill(start_color=colors['header_bg'], end_color=colors['header_bg'], fill_type="solid")
    sub_header_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    # General border style for "shapes"
    kpi_border_style = Border(left=Side(style='thin', color=colors['light_grey']),
                              right=Side(style='thin', color=colors['light_grey']),
                              top=Side(style='thin', color=colors['light_grey']),
                              bottom=Side(style='thin', color=colors['light_grey']))

    # --- KPI Section (Simulated with merged cells, numbers, and donut charts) ---
    kpis_info = [
        {'title': "Sales", 'amount_cell': 'Inputs!D5', 'percent_cell': 'Inputs!D7', 'merged_range': 'B5:D9', 'title_pos': 'B5', 'amount_pos': 'B7', 'chart_anchor': 'C6'},
        {'title': "Profit", 'amount_cell': 'Inputs!G5', 'percent_cell': 'Inputs!G7', 'merged_range': 'E5:G9', 'title_pos': 'E5', 'amount_pos': 'E7', 'chart_anchor': 'F6'},
        {'title': "# of Customers", 'amount_cell': 'Inputs!J5', 'percent_cell': 'Inputs!J7', 'merged_range': 'H5:J9', 'title_pos': 'H5', 'amount_pos': 'H7', 'chart_anchor': 'I6'}
    ]

    for kpi in kpis_info:
        # Outer "Shape" (merged cells)
        ws.merge_cells(kpi['merged_range'])
        ws[kpi['title_pos']].font = Font(name='Calibri', size=14, bold=True, color=colors['text_color_dark'])
        ws[kpi['title_pos']].value = kpi['title']
        ws[kpi['title_pos']].alignment = Alignment(horizontal='center', vertical='top')
        ws[kpi['title_pos']].border = kpi_border_style

        # Dynamic Amount Text
        amount_display_cell = ws[kpi['amount_pos']]
        amount_display_cell.value = f"={kpi['amount_cell']}"
        amount_display_cell.font = Font(name='Calibri', size=22, bold=True, color=colors['text_color_dark'])
        amount_display_cell.alignment = Alignment(horizontal='center', vertical='center')
        if kpi['title'] in ['Sales', 'Profit']:
            amount_display_cell.number_format = '$#,##0'
        elif kpi['title'] == '# of Customers':
            amount_display_cell.number_format = '0.0'

        # Donut Chart with internal percentage
        chart = DoughnutChart()
        if kpi['title'] == 'Sales':
            series_ref = Reference(inputs_ws, min_col=4, min_row=6, max_row=7)
        elif kpi['title'] == 'Profit':
            series_ref = Reference(inputs_ws, min_col=7, min_row=6, max_row=7)
        elif kpi['title'] == '# of Customers':
            series_ref = Reference(inputs_ws, min_col=10, min_row=6, max_row=7)

        series = Series(values=series_ref)
        series.dLbls = DataLabelList()
        series.dLbls.showVal = False
        series.dLbls.showPercent = True # Show percentage within the donut
        series.dLbls.txPr = RichText(Paragraph(ParagraphProperties(defRPr=CharacterProperties(sz=1200, b=True, solidFill=SolidColor(srgbClr=colors['text_color_dark'][2:]))), TextPoint()))

        chart.series.append(series)
        
        s1 = chart.series[0]
        s1.dPt = [DataPoint(idx=0), DataPoint(idx=1)]
        s1.dPt[0].graphicalProperties.solidFill = SolidColor(srgbClr=colors['accent_blue_dark'][2:]) # Completed portion
        s1.dPt[1].graphicalProperties.solidFill = SolidColor(srgbClr=colors['accent_blue_light'][2:]) # Remainder portion
        
        chart.title = None
        chart.legend = None
        chart.style = 26 # Style to remove chart area fill and border (approximate)
        chart.doughnutHoleSize = 65 # As per video

        # Position the chart within the merged cell (relative layout)
        chart.layout = Layout(ManualLayout(x=0.58, y=0.15, h=0.7, w=0.4)) # Adjusted position for better visual

        ws.add_chart(chart, kpi['chart_anchor']) # Anchor point of the chart
        chart.width = 2.2
        chart.height = 2.2


    # --- Sales Trend Chart (Line Chart) ---
    ws.merge_cells('B11:H22')
    ws['B11'].font = Font(name='Calibri', size=14, bold=True, color=colors['text_color_dark'])
    ws['B11'].value = "2021-2022 Sales Trend (in millions)"
    ws['B11'].alignment = Alignment(horizontal='center', vertical='top')
    ws['B11'].border = kpi_border_style

    line_chart = LineChart()
    line_chart.style = 2
    line_chart.title = None
    line_chart.y_axis.title = None
    line_chart.x_axis.title = None
    line_chart.legend.position = 'b' # Bottom

    line_data = Reference(inputs_ws, min_col=3, min_row=20, max_col=4, max_row=32) # 2021 & 2022 sales
    line_categories = Reference(inputs_ws, min_col=2, min_row=21, max_row=32) # Months

    line_chart.add_data(line_data, titles_from_data=True)
    line_chart.set_categories(line_categories)

    # Customize lines and markers
    s1 = line_chart.series[0] # 2021 Sales (dark blue)
    s1.graphicalProperties.line.solidFill = SolidColor(srgbClr=colors['accent_blue_dark'][2:])
    s1.marker = Marker('circle')
    s1.marker.graphicalProperties.solidFill = SolidColor(srgbClr=colors['white'][2:])
    s1.marker.graphicalProperties.ln.solidFill = SolidColor(srgbClr=colors['accent_blue_dark'][2:])

    s2 = line_chart.series[1] # 2022 Sales (red)
    s2.graphicalProperties.line.solidFill = SolidColor(srgbClr=colors['accent_red'][2:])
    s2.marker = Marker('circle')
    s2.marker.graphicalProperties.solidFill = SolidColor(srgbClr=colors['white'][2:])
    s2.marker.graphicalProperties.ln.solidFill = SolidColor(srgbClr=colors['accent_red'][2:])

    # Adjust Y-axis scale as per video (180 to 230)
    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.scaling.max = 230

    line_chart.layout = Layout(ManualLayout(x=0.05, y=0.15, h=0.8, w=0.9)) # Position within the merged cell

    ws.add_chart(line_chart, 'B12')
    line_chart.width = 7.5
    line_chart.height = 10


    # --- Customer Satisfaction Chart (Radar Chart) ---
    ws.merge_cells('I18:M22')
    ws['I18'].font = Font(name='Calibri', size=14, bold=True, color=colors['text_color_dark'])
    ws['I18'].value = "Customer Satisfaction"
    ws['I18'].alignment = Alignment(horizontal='center', vertical='top')
    ws['I18'].border = kpi_border_style

    radar_chart = RadarChart()
    radar_chart.type = "marker" # As shown in the video, with markers
    radar_chart.style = 26 # To remove chart area fill/border (approximate)
    radar_chart.title = None
    radar_chart.legend = None

    radar_data = Reference(inputs_ws, min_col=11, min_row=11, max_row=16) # Scores
    radar_categories = Reference(inputs_ws, min_col=10, min_row=12, max_row=16) # Categories

    radar_chart.add_data(radar_data, titles_from_data=True)
    radar_chart.set_categories(radar_categories)
    
    s1_radar = radar_chart.series[0]
    s1_radar.graphicalProperties.line.solidFill = SolidColor(srgbClr=colors['accent_blue_dark'][2:])
    s1_radar.marker = Marker('circle')
    s1_radar.marker.graphicalProperties.solidFill = SolidColor(srgbClr=colors['white'][2:])
    s1_radar.marker.graphicalProperties.ln.solidFill = SolidColor(srgbClr=colors['accent_blue_dark'][2:])
    
    # Hide value axis labels (y-axis) as in video
    radar_chart.y_axis.delete = True 

    ws.add_chart(radar_chart, 'I19')
    radar_chart.width = 5.5
    radar_chart.height = 4.5
    radar_chart.layout = Layout(ManualLayout(x=0.05, y=0.15, h=0.8, w=0.9))


    # --- Sales by Country Chart (Bar Chart as Map Chart placeholder) ---
    ws.merge_cells('K5:M16') # Adjusted range for map chart
    ws['K5'].font = Font(name='Calibri', size=14, bold=True, color=colors['text_color_dark'])
    ws['K5'].value = "Sales by Country 2022"
    ws['K5'].alignment = Alignment(horizontal='center', vertical='top')
    ws['K5'].border = kpi_border_style
    
    # openpyxl does not natively support interactive filled map charts like Excel's built-in one.
    # A BarChart is used as a functional placeholder to represent sales by country.
    bar_chart = BarChart()
    bar_chart.type = "col" # Column chart for better country representation as a fallback
    bar_chart.style = 26 # To remove chart area fill/border (approximate)
    bar_chart.title = None
    bar_chart.legend = None

    bar_data = Reference(inputs_ws, min_col=7, min_row=20, max_row=27) # Country Sales
    bar_categories = Reference(inputs_ws, min_col=6, min_row=21, max_row=27) # Countries

    bar_chart.add_data(bar_data, titles_from_data=True)
    bar_chart.set_categories(bar_categories)
    
    s1_bar = bar_chart.series[0]
    s1_bar.graphicalProperties.solidFill = SolidColor(srgbClr=colors['accent_blue_dark'][2:])
    
    # This placement simulates the visual area for the map
    ws.add_chart(bar_chart, 'K6') 
    bar_chart.width = 3.5
    bar_chart.height = 8.5
    bar_chart.layout = Layout(ManualLayout(x=0.05, y=0.1, h=0.8, w=0.9)) # Adjusted for better fit
