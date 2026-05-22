import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, PieChart, Reference
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.radar import RadarChart # RadarChart is available
from openpyxl.chart.series import DataPoint
from openpyxl.utils import get_column_letter

# Helper function for themes (as in seed skills)
def get_theme_colors(theme_name="corporate_blue"):
    themes = {
        "corporate_blue": {
            "title_bg": "FF2E6A9C", "title_fg": "FFFFFFFF",
            "sidebar_bg": "FF2E6A9C", "sidebar_fg": "FFFFFFFF",
            "section_bg": "FFFFFFFF", "section_border": "FFD9D9D9", "section_shadow": "FFBFBFBF", # Shadow conceptual
            "accent_red": "FFC00000", "accent_blue": "FF2F5597", "light_blue": "FFD9E1F2",
            "text_dark": "FF333333", "text_light": "FFFFFFFF"
        },
        # Add other themes if needed
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    colors = get_theme_colors(theme)

    # Set up basic column widths
    ws.column_dimensions['A'].width = 8 # Sidebar width
    for col_idx in range(2, 17): # Columns B to P for content
        ws.column_dimensions[get_column_letter(col_idx)].width = 10

    # Sidebar (Column A)
    for row in range(1, 30):
        ws[f'A{row}'].fill = PatternFill(start_color=colors["sidebar_bg"], end_color=colors["sidebar_bg"], fill_type="solid")
        # Icons and hyperlinks for navigation are typically UI elements not directly created by openpyxl shapes.
        # This column serves as a visual placeholder.

    # Main Dashboard Title Area
    ws.merge_cells('B1:P4')
    title_cell = ws['B1']
    title_cell.value = title
    title_cell.font = Font(name='Calibri', size=20, bold=True, color=colors["title_fg"])
    title_cell.fill = PatternFill(start_color=colors["title_bg"], end_color=colors["title_bg"], fill_type="solid")
    title_cell.alignment = Alignment(horizontal='left', vertical='center')

    ws.merge_cells('B5:P5')
    subtitle_cell = ws['B5']
    subtitle_cell.value = "Figures in millions of USD"
    subtitle_cell.font = Font(name='Calibri', size=11, color=colors["title_fg"])
    subtitle_cell.fill = PatternFill(start_color=colors["title_bg"], end_color=colors["title_bg"], fill_type="solid")
    subtitle_cell.alignment = Alignment(horizontal='left', vertical='center')

    # Simulate input data on a hidden part of the sheet for charts
    # KPIs
    ws.cell(row=1, column=20).value = "Sales"
    ws.cell(row=2, column=20).value = 2544 # Actual
    ws.cell(row=3, column=20).value = 3000 # Target
    ws.cell(row=1, column=22).value = "Profit"
    ws.cell(row=2, column=22).value = 890 # Actual
    ws.cell(row=3, column=22).value = 1000 # Target
    ws.cell(row=1, column=24).value = "Customers"
    ws.cell(row=2, column=24).value = 87 # Actual
    ws.cell(row=3, column=24).value = 100 # Target

    # Sales Trend Data
    trend_data_start_row = 1
    trend_data_start_col = 30
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sales_2021 = [201.9, 204.2, 198.6, 199.2, 195.3, 192.4, 195.3, 186.3, 199.2, 202.9, 205.5, 204.3]
    sales_2022 = [215.3, 217.6, 220.1, 206.4, 203.0, 200.6, 200.6, 208.4, 222.6, 225.8, 228.6, 230.8]
    
    ws.cell(row=trend_data_start_row, column=trend_data_start_col).value = "Month"
    ws.cell(row=trend_data_start_row, column=trend_data_start_col+1).value = "2021"
    ws.cell(row=trend_data_start_row, column=trend_data_start_col+2).value = "2022"
    for i, month in enumerate(months):
        ws.cell(row=trend_data_start_row + i + 1, column=trend_data_start_col).value = month
        ws.cell(row=trend_data_start_row + i + 1, column=trend_data_start_col + 1).value = sales_2021[i]
        ws.cell(row=trend_data_start_row + i + 1, column=trend_data_start_col + 2).value = sales_2022[i]

    # Customer Satisfaction Data
    cs_data_start_row = 1
    cs_data_start_col = 40
    metrics = ["Speed", "Quality", "Hygiene", "Service", "Availability"]
    scores = [0.54, 0.89, 0.93, 0.57, 0.95]
    ws.cell(row=cs_data_start_row, column=cs_data_start_col).value = "Metric"
    ws.cell(row=cs_data_start_row, column=cs_data_start_col+1).value = "Score"
    for i, metric in enumerate(metrics):
        ws.cell(row=cs_data_start_row + i + 1, column=cs_data_start_col).value = f"{metric} ({scores[i]:.0%})"
        ws.cell(row=cs_data_start_row + i + 1, column=cs_data_start_col + 1).value = scores[i]

    # Helper for creating KPI sections (simulated shapes)
    def create_kpi_section(ws_target, anchor_cell_str, kpi_name_str, actual_val_cell, target_val_cell, colors, data_col_offset):
        # Background "shape" (merged cells)
        col_start, row_start = openpyxl.utils.cell.coordinate_to_tuple(anchor_cell_str)
        ws_target.merge_cells(start_row=row_start, end_row=row_start+4, start_column=col_start, end_column=col_start+3)
        for r_idx in range(row_start, row_start+5):
            for c_idx in range(col_start, col_start+4):
                cell = ws_target.cell(row=r_idx, column=c_idx)
                cell.fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")
                cell.border = Border(left=Side(style='thin', color=colors["section_border"]),
                                     right=Side(style='thin', color=colors["section_border"]),
                                     top=Side(style='thin', color=colors["section_border"]),
                                     bottom=Side(style='thin', color=colors["section_border"]))
                
        # Section Title
        ws_target.cell(row=row_start, column=col_start).value = kpi_name_str
        ws_target.cell(row=row_start, column=col_start).font = Font(name='Calibri', size=11, bold=True, color=colors["text_dark"])
        ws_target.cell(row=row_start, column=col_start).alignment = Alignment(horizontal='left', vertical='top')

        # KPI Actual Value (simulated dynamic text box)
        kpi_value_cell = ws_target.cell(row=row_start+1, column=col_start)
        kpi_value_cell.value = f"${actual_val_cell.value:,}" if kpi_name_str != "# of Customers" else f"{actual_val_cell.value:,}.0"
        kpi_value_cell.font = Font(name='Calibri', size=16, bold=True, color=colors["accent_blue"])
        kpi_value_cell.alignment = Alignment(horizontal='center', vertical='center')

        # Donut Chart Data (linking to actual values on the simulated inputs part)
        complete_val = actual_val_cell.value / target_val_cell.value
        remainder_val = 1 - complete_val

        ws_target.cell(row=row_start + 1, column=trend_data_start_col + data_col_offset).value = "Complete"
        ws_target.cell(row=row_start + 2, column=trend_data_start_col + data_col_offset).value = complete_val
        ws_target.cell(row=row_start + 3, column=trend_data_start_col + data_col_offset).value = "Remainder"
        ws_target.cell(row=row_start + 4, column=trend_data_start_col + data_col_offset).value = remainder_val

        pie = PieChart()
        pie_data_ref = Reference(ws_target, min_col=trend_data_start_col + data_col_offset, min_row=row_start + 2, max_row=row_start + 4)
        
        pie.add_data(pie_data_ref, from_rows=True) # Data from rows (one series per row)
        pie.title = ""
        pie.doughnutHoleSize = 65

        # Custom colors for slices
        s1 = pie.series[0]
        s1.dPt[0].graphicalProperties.solidFill = colors["accent_blue"] # Complete
        s1.dPt[1].graphicalProperties.solidFill = colors["light_blue"] # Remainder

        pie.width = 1.2 # inches
        pie.height = 1.2 # inches
        
        # Position the chart relative to the section's anchor
        pie_anchor_col = get_column_letter(col_start + 2)
        pie_anchor_row = row_start + 1
        ws_target.add_chart(pie, pie_anchor_col + str(pie_anchor_row))
        
        # Set chart area to no fill, no border
        pie.graphical_properties.noFill = True
        pie.graphical_properties.noBorder = True

        # Percentage text over donut (simulated with a cell)
        percent_cell = ws_target.cell(row=row_start + 2, column=col_start + 2)
        percent_cell.value = f"{complete_val:.0%}"
        percent_cell.font = Font(name='Calibri', size=12, bold=True, color=colors["accent_blue"])
        percent_cell.alignment = Alignment(horizontal='center', vertical='center')


    # Create KPI sections
    create_kpi_section(ws, 'B7', "Sales", ws.cell(row=2, column=20), ws.cell(row=3, column=20), colors, 5)
    create_kpi_section(ws, 'F7', "Profit", ws.cell(row=2, column=22), ws.cell(row=3, column=22), colors, 6)
    create_kpi_section(ws, 'J7', "# of Customers", ws.cell(row=2, column=24), ws.cell(row=3, column=24), colors, 7)

    # Sales Trend Line Chart Section
    trend_section_start_col = 2
    trend_section_start_row = 13
    ws.merge_cells(start_row=trend_section_start_row, end_row=trend_section_start_row+14, start_column=trend_section_start_col, end_column=trend_section_start_col+7)
    for r_idx in range(trend_section_start_row, trend_section_start_row+15):
        for c_idx in range(trend_section_start_col, trend_section_start_col+8):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")
            cell.border = Border(left=Side(style='thin', color=colors["section_border"]),
                                 right=Side(style='thin', color=colors["section_border"]),
                                 top=Side(style='thin', color=colors["section_border"]),
                                 bottom=Side(style='thin', color=colors["section_border"]))

    trend_title_cell = ws.cell(row=trend_section_start_row, column=trend_section_start_col)
    trend_title_cell.value = "2021-2022 Sales Trend (in millions)"
    trend_title_cell.font = Font(name='Calibri', size=11, bold=True, color=colors["text_dark"])
    trend_title_cell.alignment = Alignment(horizontal='left', vertical='top')

    line_chart = LineChart()
    line_chart.title = ""
    line_chart.style = 10
    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.scaling.max = 230
    line_chart.y_axis.title = ""
    line_chart.x_axis.title = ""

    data = Reference(ws, min_col=trend_data_start_col + 1, min_row=trend_data_start_row, max_col=trend_data_start_col + 2, max_row=trend_data_start_row + len(months))
    categories = Reference(ws, min_col=trend_data_start_col, min_row=trend_data_start_row + 1, max_row=trend_data_start_row + len(months))
    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(categories)

    # Customize line colors and markers
    s1_line_props = LineProperties()
    s1_line_props.solidFill = colors["accent_blue"]
    line_chart.series[0].graphicalProperties.line = s1_line_props
    line_chart.series[0].marker = chart_types.Marker(symbol='circle')
    line_chart.series[0].marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    line_chart.series[0].marker.graphicalProperties.ln = chart_types.LineProperties(solidFill=colors["accent_blue"]) # Blue border

    s2_line_props = LineProperties()
    s2_line_props.solidFill = colors["accent_red"]
    line_chart.series[1].graphicalProperties.line = s2_line_props
    line_chart.series[1].marker = chart_types.Marker(symbol='circle')
    line_chart.series[1].marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    line_chart.series[1].marker.graphicalProperties.ln = chart_types.LineProperties(solidFill=colors["accent_red"]) # Red border
    
    line_chart.width = 7.0 # inches
    line_chart.height = 5.0 # inches
    
    ws.add_chart(line_chart, get_column_letter(trend_section_start_col) + str(trend_section_start_row + 2))
    line_chart.graphical_properties.noFill = True
    line_chart.graphical_properties.noBorder = True

    # Customer Satisfaction Radar Chart Section
    radar_section_start_col = 10
    radar_section_start_row = 13
    ws.merge_cells(start_row=radar_section_start_row, end_row=radar_section_start_row+14, start_column=radar_section_start_col, end_column=radar_section_start_col+5)
    for r_idx in range(radar_section_start_row, radar_section_start_row+15):
        for c_idx in range(radar_section_start_col, radar_section_start_col+6):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")
            cell.border = Border(left=Side(style='thin', color=colors["section_border"]),
                                 right=Side(style='thin', color=colors["section_border"]),
                                 top=Side(style='thin', color=colors["section_border"]),
                                 bottom=Side(style='thin', color=colors["section_border"]))

    satisfaction_title_cell = ws.cell(row=radar_section_start_row, column=radar_section_start_col)
    satisfaction_title_cell.value = "Customer Satisfaction"
    satisfaction_title_cell.font = Font(name='Calibri', size=11, bold=True, color=colors["text_dark"])
    satisfaction_title_cell.alignment = Alignment(horizontal='left', vertical='top')

    radar_chart = RadarChart()
    radar_chart.title = ""
    radar_chart.y_axis.delete = True # Remove y-axis
    radar_chart.x_axis.delete = True # Remove x-axis labels (metrics are in data labels)

    data = Reference(ws, min_col=cs_data_start_col + 1, min_row=cs_data_start_row + 1, max_row=cs_data_start_row + len(metrics))
    categories = Reference(ws, min_col=cs_data_start_col, min_row=cs_data_start_row + 1, max_row=cs_data_start_row + len(metrics))
    radar_chart.add_data(data, titles_from_data=False) # Titles from data not used for radar series names here
    radar_chart.set_categories(categories)
    
    # Customize radar line and markers
    s1_radar_props = LineProperties()
    s1_radar_props.solidFill = colors["accent_blue"]
    radar_chart.series[0].graphicalProperties.line = s1_radar_props
    radar_chart.series[0].marker = chart_types.Marker(symbol='circle')
    radar_chart.series[0].marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    radar_chart.series[0].marker.graphicalProperties.ln = chart_types.LineProperties(solidFill=colors["accent_blue"]) # Blue border

    radar_chart.width = 5.0 # inches
    radar_chart.height = 5.0 # inches
    
    ws.add_chart(radar_chart, get_column_letter(radar_section_start_col) + str(radar_section_start_row + 2))
    radar_chart.graphical_properties.noFill = True
    radar_chart.graphical_properties.noBorder = True

    # Sales by Country (Map Chart - Openpyxl doesn't support this directly. Placeholder cells)
    map_section_start_col = 16
    map_section_start_row = 7
    ws.merge_cells(start_row=map_section_start_row, end_row=map_section_start_row+20, start_column=map_section_start_col, end_column=map_section_start_col+3)
    for r_idx in range(map_section_start_row, map_section_start_row+21):
        for c_idx in range(map_section_start_col, map_section_start_col+4):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.fill = PatternFill(start_color=colors["section_bg"], end_color=colors["section_bg"], fill_type="solid")
            cell.border = Border(left=Side(style='thin', color=colors["section_border"]),
                                 right=Side(style='thin', color=colors["section_border"]),
                                 top=Side(style='thin', color=colors["section_border"]),
                                 bottom=Side(style='thin', color=colors["section_border"]))
    
    map_title_cell = ws.cell(row=map_section_start_row, column=map_section_start_col)
    map_title_cell.value = "Sales by Country 2022"
    map_title_cell.font = Font(name='Calibri', size=11, bold=True, color=colors["text_dark"])
    map_title_cell.alignment = Alignment(horizontal='left', vertical='top')

    ws.cell(row=map_section_start_row+3, column=map_section_start_col).value = "Map Chart Placeholder"
    ws.cell(row=map_section_start_row+4, column=map_section_start_col).value = "(Requires Excel's native feature)"
    ws.merge_cells(start_row=map_section_start_row+3, end_row=map_section_start_row+4, start_column=map_section_start_col, end_column=map_section_start_col+3)
    ws.cell(row=map_section_start_row+3, column=map_section_start_col).alignment = Alignment(horizontal='center', vertical='center', wrapText=True)
    ws.cell(row=map_section_start_row+3, column=map_section_start_col).font = Font(color=colors["text_dark"], size=9)

if __name__ == '__main__':
    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet) # Remove default blank sheet
    
    render_sheet(wb, "Dashboard", title="Sales Dashboard South America 2022")
    
    # Save the workbook
    output_path = "themed_sales_dashboard.xlsx"
    wb.save(output_path)
    print(f"Dashboard saved to {output_path}")
