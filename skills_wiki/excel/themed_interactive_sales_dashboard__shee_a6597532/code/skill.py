from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, AreaChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.formatting.rule import FormulaRule, DataBarRule
from openpyxl.utils import get_column_letter

# Helper functions (assuming these exist in a _helpers module or similar)
def get_theme_colors(theme_name):
    """Returns a dictionary of colors for a given theme."""
    themes = {
        "sales_dashboard": {
            "header_bg": "49165B",  # Dark purple
            "body_bg": "F2EFF5",    # Light purple
            "title_fg": "FFFFFF",   # White
            "subtitle_fg": "FFD700",# Gold/Yellow
            "accent_1": "FFD700",   # Gold/Yellow
            "accent_2": "6A1A8D",   # Medium Purple (for deals/total sales bars)
            "text_color": "49165B", # Dark purple for general text
            "border_color": "C0C0C0" # Gray for minor borders
        }
        # Add other themes here if needed
    }
    return themes.get(theme_name, themes["sales_dashboard"]) # Default to sales_dashboard

def create_side(color_hex):
    """Creates a Side object for borders."""
    return Side(border_style="thin", color=color_hex)

def create_border(color_hex):
    """Creates a Border object with all sides."""
    side = create_side(color_hex)
    return Border(left=side, right=side, top=side, bottom=side)

def create_font(size, color_hex, bold=False):
    """Creates a Font object."""
    return Font(name="Aptos Narrow", size=size, color=color_hex, bold=bold)

def create_fill(color_hex):
    """Creates a PatternFill object."""
    return PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")

def create_shape(ws, shape_type, anchor, width, height, fill_color, outline_color=None, text="", font_color=None, font_size=11, align="center"):
    """Inserts a basic shape with text and formatting."""
    # openpyxl doesn't directly support inserting complex shapes like PowerPoint,
    # so we'll simulate them with merged cells and text boxes.
    # For this reproduction, we will use merged cells for background shapes
    # and directly link text boxes. The "shapes" parameter in the problem description
    # might refer to image-based shapes or SmartArt, which are complex for direct openpyxl.
    # We will use simple merged cells for background and textboxes for text.
    # Icons would be image insertions. For reproduction, we focus on the structure.
    pass # Placeholder, as complex shapes are not directly supported by openpyxl for drawing.

# Note: For actual shapes and icons, you would use `openpyxl.drawing.image.Image`
# for pictures or manually create text boxes, and then position them.
# The `create_shape` helper here is conceptual for the intent of the video.

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "sales_dashboard", **kwargs) -> None:
    """
    Renders an interactive sales dashboard sheet.

    Assumes the 'Analysis' sheet exists with PivotTables and aggregated values
    in specific cells for KPI linking and chart data.
    """
    ws = wb.create_sheet(title=sheet_name)
    colors = get_theme_colors(theme)

    # 1. Set up row/column dimensions and overall background
    ws.column_dimensions['A'].width = 4
    for i in range(2, 27): # Columns B to Z
        ws.column_dimensions[get_column_letter(i)].width = 7.5
    for i in range(1, 41): # Rows 1 to 40
        ws.row_dimensions[i].height = 18

    # Apply overall sheet background
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=26):
        for cell in row:
            cell.fill = create_fill(colors["body_bg"])

    # Header section (rows 1-8)
    for row in ws.iter_rows(min_row=1, max_row=8, min_col=1, max_col=26):
        for cell in row:
            cell.fill = create_fill(colors["header_bg"])

    ws.merge_cells('B2:F2')
    ws['B2'] = title
    ws['B2'].font = create_font(36, colors["title_fg"], bold=True)
    ws['B2'].alignment = Alignment(horizontal='left', vertical='center')

    ws.merge_cells('B4:F4')
    ws['B4'] = "Evaluating Sales Agent Performance"
    ws['B4'].font = create_font(16, colors["subtitle_fg"])
    ws['B4'].alignment = Alignment(horizontal='left', vertical='center')

    # 2. Add KPI sections (simulated using merged cells and text boxes for demonstration)
    # The actual shapes/icons are more complex than direct openpyxl support.
    # We'll create merged cell areas for visual placeholders and link text boxes.

    # KPI 1: Calls
    ws.merge_cells('G2:K7') # Gold top part
    ws.cell(row=2, column=7).fill = create_fill(colors["accent_1"])
    ws.merge_cells('H2:K7') # White inner part
    ws.cell(row=2, column=8).fill = create_fill("FFFFFF")
    # Link text for KPI value (example, actual requires textbox or careful cell placement)
    ws['H4'] = f"='Analysis'!B4"
    ws['H4'].font = create_font(32, colors["text_color"], bold=True)
    ws['H4'].alignment = Alignment(horizontal='center', vertical='center')
    ws['H5'] = "CALLS"
    ws['H5'].font = create_font(18, colors["text_color"])
    ws['H5'].alignment = Alignment(horizontal='center', vertical='center')

    # KPI 2: Reached
    ws.merge_cells('L2:P7')
    ws.cell(row=2, column=12).fill = create_fill(colors["accent_1"])
    ws.merge_cells('M2:P7')
    ws.cell(row=2, column=13).fill = create_fill("FFFFFF")
    ws['M4'] = f"='Analysis'!B5"
    ws['M4'].font = create_font(32, colors["text_color"], bold=True)
    ws['M4'].alignment = Alignment(horizontal='center', vertical='center')
    ws['M5'] = "REACHED"
    ws['M5'].font = create_font(18, colors["text_color"])
    ws['M5'].alignment = Alignment(horizontal='center', vertical='center')

    # KPI 3: Closed
    ws.merge_cells('Q2:U7')
    ws.cell(row=2, column=17).fill = create_fill(colors["accent_1"])
    ws.merge_cells('R2:U7')
    ws.cell(row=2, column=18).fill = create_fill("FFFFFF")
    ws['R4'] = f"='Analysis'!B6"
    ws['R4'].font = create_font(32, colors["text_color"], bold=True)
    ws['R4'].alignment = Alignment(horizontal='center', vertical='center')
    ws['R5'] = "CLOSED"
    ws['R5'].font = create_font(18, colors["text_color"])
    ws['R5'].alignment = Alignment(horizontal='center', vertical='center')

    # KPI 4: Value
    ws.merge_cells('V2:Z7')
    ws.cell(row=2, column=22).fill = create_fill(colors["accent_1"])
    ws.merge_cells('W2:Z7')
    ws.cell(row=2, column=23).fill = create_fill("FFFFFF")
    ws['W4'] = f"='Analysis'!B7" # Assuming formatted as currency on Analysis sheet
    ws['W4'].font = create_font(32, colors["text_color"], bold=True)
    ws['W4'].alignment = Alignment(horizontal='center', vertical='center')
    ws['W5'] = "VALUE"
    ws['W5'].font = create_font(18, colors["text_color"])
    ws['W5'].alignment = Alignment(horizontal='center', vertical='center')

    # 3. Sales Agent KPIs Table (Assuming a PivotTable will be moved here)
    # This section simulates the appearance of the PivotTable. The actual PivotTable
    # would be created on 'Analysis' and then moved or linked.
    ws.merge_cells('B9:H9')
    ws['B9'] = "Sales Agent KPIs"
    ws['B9'].font = create_font(14, colors["text_color"], bold=True)
    ws['B9'].alignment = Alignment(horizontal='left', vertical='center')
    # Placeholder for PivotTable, assuming it's been moved from 'Analysis'
    # We will apply conditional formatting to a assumed range.
    sales_agent_kpis_range = 'B10:H36'
    ws.cell(row=10, column=2).value = "Name"
    ws.cell(row=10, column=3).value = "Total Calls"
    ws.cell(row=10, column=4).value = "Calls Reached"
    ws.cell(row=10, column=5).value = "Deals Closed"
    ws.cell(row=10, column=6).value = "Deal Value ($)"
    # Apply initial formatting to headers
    for col_idx in range(2, 7):
        cell = ws.cell(row=10, column=col_idx)
        cell.font = create_font(11, colors["title_fg"], bold=True)
        cell.fill = create_fill(colors["header_bg"])
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Conditional formatting for highlighting selected salesperson
    # This assumes Analysis!$A$11 contains the currently selected name from the slicer.
    # The rule applies to the full data range of the Sales Agent KPIs table (e.g., B10:F36)
    cf_range = 'B11:F36' # Assuming data starts from B11
    highlight_color = "FFD700" # Gold
    font_color = "FFFFFF" # White

    rule = FormulaRule(
        formula=[f'=INDIRECT("B"&ROW())="Analysis!$A$11"'], # Compare name in col B to slicer selection
        fill=create_fill(highlight_color),
        font=create_font(11, font_color, bold=True)
    )
    ws.conditional_formatting.add(cf_range, rule)

    # Data bars for 'Total Calls'
    data_bar_range_calls = 'C11:C36' # Assuming Total Calls is in column C
    ws.conditional_formatting.add(data_bar_range_calls, DataBarRule(
        start_type='Min', start_value=None, start_condition='gte',
        end_type='Max', end_value=None, end_condition='lte',
        color=colors["accent_1"], showValue=True, minLength=0, maxLength=100
    ))
    # Data bars for 'Calls Reached'
    data_bar_range_reached = 'D11:D36' # Assuming Calls Reached is in column D
    ws.conditional_formatting.add(data_bar_range_reached, DataBarRule(
        start_type='Min', start_value=None, start_condition='gte',
        end_type='Max', end_value=None, end_condition='lte',
        color=colors["subtitle_fg"], showValue=True, minLength=0, maxLength=100 # Using subtitle_fg as yellow
    ))
    # Data bars for 'Deals Closed'
    data_bar_range_closed = 'E11:E36' # Assuming Deals Closed is in column E
    ws.conditional_formatting.add(data_bar_range_closed, DataBarRule(
        start_type='Min', start_value=None, start_condition='gte',
        end_type='Max', end_value=None, end_condition='lte',
        color=colors["accent_2"], showValue=True, minLength=0, maxLength=100
    ))
    # Data bars for 'Deal Value'
    data_bar_range_value = 'F11:F36' # Assuming Deal Value is in column F
    ws.conditional_formatting.add(data_bar_range_value, DataBarRule(
        start_type='Min', start_value=None, start_condition='gte',
        end_type='Max', end_value=None, end_condition='lte',
        color=colors["body_bg"], showValue=True, minLength=0, maxLength=100 # Using light purple
    ))


    # 4. Charts (placeholders and styling for chart areas)
    # Openpyxl chart creation is detailed, so we'll set up the ranges and basic styling
    # Chart 1: Sum of Calls Reached vs Deals Closed
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10 # Example style
    chart1.title = "Sum of Calls Reached + Sum of Deals Closed"
    chart1.y_axis.title = None # Removed from video
    chart1.x_axis.title = None # Removed from video
    chart1.x_axis.number_format = 'mmm' # Jan, Feb, etc.
    chart1.y_axis.scaling.min = 0 # Fix vertical axis to start at 0

    data_ref1_reached = Reference(kwargs.get('analysis_ws'), min_col=4, min_row=4, max_col=4, max_row=14) # Calls Reached by Month
    data_ref1_closed = Reference(kwargs.get('analysis_ws'), min_col=5, min_row=4, max_col=5, max_row=14) # Deals Closed by Month
    categories_ref1 = Reference(kwargs.get('analysis_ws'), min_col=3, min_row=4, max_col=3, max_row=14) # Months

    series1_reached = chart1.add_data(data_ref1_reached, titles_from_data=True)
    series1_closed = chart1.add_data(data_ref1_closed, titles_from_data=True)
    chart1.set_categories(categories_ref1)

    chart1.series[0].graphicalProperties.solidFill = colors["accent_1"] # Calls Reached - Yellow
    chart1.series[1].graphicalProperties.solidFill = colors["accent_2"] # Deals Closed - Purple

    chart1.shape_properties = {'spPr': {'noFill': False, 'solidFill': {'srgbClr': {'val': 'FFFFFF'}}, 'ln': {'noFill': True}}} # White background, no border
    chart1.border = None
    chart1.show_gridlines = False
    chart1.legend.position = 't' # Top

    ws.add_chart(chart1, "J10") # Anchor chart on dashboard


    # Chart 2: Total Sales
    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 10
    chart2.title = "Total Sales $"
    chart2.y_axis.title = None
    chart2.x_axis.title = None
    chart2.x_axis.number_format = 'mmm'
    chart2.y_axis.scaling.min = 0

    data_ref2 = Reference(kwargs.get('analysis_ws'), min_col=7, min_row=4, max_col=7, max_row=14) # Deal Value by Month
    categories_ref2 = Reference(kwargs.get('analysis_ws'), min_col=3, min_row=4, max_col=3, max_row=14) # Months

    series2 = chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(categories_ref2)

    chart2.series[0].graphicalProperties.solidFill = colors["accent_2"] # Purple

    # Add trendline
    trendline_series = LineChart() # Trendline is usually a separate series or an element of the series
    trendline_series.title = "Linear (Total)"
    trendline_series.style = 10
    trendline_series.y_axis.crosses = "max"
    trendline_series.x_axis.visible = False
    trendline_series.y_axis.visible = False

    trendline_data = Reference(kwargs.get('analysis_ws'), min_col=7, min_row=4, max_col=7, max_row=14) # Same data for trendline
    series_trend = trendline_series.add_data(trendline_data, titles_from_data=True)
    series_trend.graphicalProperties.line.solidFill = colors["accent_1"] # Yellow
    series_trend.graphicalProperties.line.width = 25400 # 2pt
    series_trend.graphicalProperties.line.dashDotBdr = {'val': 'dash'} # Dashed line
    series_trend.chart_type = "line"
    series_trend.tx.v = "Linear (Total)" # Name for legend

    chart2.plot_area.overlay = True
    chart2.plot_area.clear_styles() # Clear default styles to allow custom fills
    
    chart2.shape_properties = {'spPr': {'noFill': False, 'solidFill': {'srgbClr': {'val': 'FFFFFF'}}, 'ln': {'noFill': True}}} # White background, no border
    chart2.border = None
    chart2.show_gridlines = False
    chart2.legend.position = 't' # Top
    chart2.legend.layout = {'x': 0.8, 'y': 0.05, 'w': 0.15, 'h': 0.15} # Adjust legend position to not overlap title
    
    ws.add_chart(chart2, "S10") # Anchor chart on dashboard

    # Chart 3: Average Call Duration
    chart3 = BarChart()
    chart3.type = "col"
    chart3.style = 10
    chart3.title = "Average Call Duration (Seconds)"
    chart3.y_axis.title = None
    chart3.x_axis.title = None
    chart3.x_axis.number_format = 'mmm'
    chart3.y_axis.scaling.min = 0

    data_ref3 = Reference(kwargs.get('analysis_ws'), min_col=10, min_row=4, max_col=10, max_row=14) # Avg Duration by Month
    categories_ref3 = Reference(kwargs.get('analysis_ws'), min_col=3, min_row=4, max_col=3, max_row=14) # Months

    series3 = chart3.add_data(data_ref3, titles_from_data=True)
    chart3.set_categories(categories_ref3)

    chart3.series[0].graphicalProperties.solidFill = colors["accent_1"] # Yellow

    chart3.shape_properties = {'spPr': {'noFill': False, 'solidFill': {'srgbClr': {'val': 'FFFFFF'}}, 'ln': {'noFill': True}}} # White background, no border
    chart3.border = None
    chart3.show_gridlines = False
    chart3.legend.visible = False # Removed from video
    
    ws.add_chart(chart3, "J27") # Anchor chart on dashboard

    # Chart 4: Average Call Drop Rate
    chart4 = AreaChart()
    chart4.style = 10
    chart4.title = "Average Call Drop Rate %"
    chart4.y_axis.title = None
    chart4.x_axis.title = None
    chart4.x_axis.number_format = 'mmm'
    chart4.y_axis.scaling.min = 0
    chart4.y_axis.number_format = '0.00%'

    data_ref4 = Reference(kwargs.get('analysis_ws'), min_col=13, min_row=4, max_col=13, max_row=14) # Call Drop Rate by Month
    categories_ref4 = Reference(kwargs.get('analysis_ws'), min_col=3, min_row=4, max_col=3, max_row=14) # Months

    series4 = chart4.add_data(data_ref4, titles_from_data=True)
    chart4.set_categories(categories_ref4)

    # Gradient fill for area chart
    series4.graphicalProperties.noFill = False
    series4.graphicalProperties.gradFill = {
        'rotWithEllipses': True,
        'path': {'val': 'linear'},
        'tileRect': None,
        'lin': {'ang': 2700000, 'scaled': True}, # Angle 270 degrees
        'gsLst': {
            'gs': [
                {'pos': 0, 'rgb': 'FFFFFF'},   # White at the top
                {'pos': 50000, 'rgb': colors["accent_1"]}, # Yellow in the middle
                {'pos': 100000, 'rgb': 'FFFFFF'}  # White at the bottom
            ]
        }
    }
    series4.graphicalProperties.line.noFill = True # No line border for area

    chart4.shape_properties = {'spPr': {'noFill': False, 'solidFill': {'srgbClr': {'val': 'FFFFFF'}}, 'ln': {'noFill': True}}} # White background, no border
    chart4.border = None
    chart4.show_gridlines = False
    chart4.legend.visible = False
    
    ws.add_chart(chart4, "S27") # Anchor chart on dashboard

    # Note: Adding shadows to charts directly via openpyxl is complex as it requires
    # low-level XML manipulation for shape effects. This is usually done by
    # saving the workbook, opening in Excel, applying shadows, and saving again.
    # The current openpyxl API has limited high-level support for shape effects like shadows.

    # Final adjustments (e.g., hiding gridlines for the entire sheet if desired)
    ws.views.sheetView[0].showGridLines = False

