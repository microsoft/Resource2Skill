import openpyxl
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter

def render(ws, anchor: str, *, kpi_name: str = "Sales Revenue", actual: float = 2544.0, target: float = 3000.0, format_str: str = "$#,##0", theme: dict = None, **kwargs) -> None:
    """
    Renders a KPI widget panel with a Doughnut chart showing progress against target.
    The percentage text is rendered in the cells behind the chart's transparent background.
    """
    if theme is None:
        theme = {
            "panel_bg": "FFFFFF",
            "panel_border": "E0E0E0",
            "text_main": "333333",
            "text_light": "888888",
            "primary": "0052CC",    # Dark Blue
            "secondary": "EAECEF"   # Light Grey
        }
        
    # Parse anchor
    col_str, row_str = coordinate_from_string(anchor)
    c = column_index_from_string(col_str)
    r = int(row_str)
    
    # 1. Format the Panel Area (5 columns wide x 6 rows high)
    panel_fill = PatternFill(start_color=theme["panel_bg"], end_color=theme["panel_bg"], fill_type="solid")
    thin_border = Side(border_style="thin", color=theme["panel_border"])
    
    for row in range(r, r + 6):
        for col in range(c, c + 5):
            cell = ws.cell(row=row, column=col)
            cell.fill = panel_fill
            
            # Draw outer border around the 5x6 block
            top = thin_border if row == r else None
            bottom = thin_border if row == r + 5 else None
            left = thin_border if col == c else None
            right = thin_border if col == c + 4 else None
            cell.border = Border(top=top, bottom=bottom, left=left, right=right)

    # 2. Add KPI Text Elements (Left Side)
    # KPI Name
    ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+1)
    name_cell = ws.cell(row=r, column=c, value=kpi_name)
    name_cell.font = Font(size=11, bold=True, color=theme["text_main"])
    name_cell.alignment = Alignment(vertical="top", wrap_text=True)
    
    # KPI Actual Value
    ws.merge_cells(start_row=r+2, start_column=c, end_row=r+3, end_column=c+1)
    actual_cell = ws.cell(row=r+2, column=c, value=actual)
    actual_cell.font = Font(size=18, bold=True, color=theme["text_main"])
    actual_cell.number_format = format_str
    actual_cell.alignment = Alignment(vertical="center")
    
    # KPI Target Subtext
    t_label = ws.cell(row=r+5, column=c, value="Target:")
    t_label.font = Font(size=9, color=theme["text_light"])
    t_val = ws.cell(row=r+5, column=c+1, value=target)
    t_val.font = Font(size=9, color=theme["text_light"])
    t_val.number_format = format_str
    t_val.alignment = Alignment(horizontal="left")
    
    # 3. Add Chart Data (Hidden in rightmost column)
    pct_complete = min(actual / target, 1.0)
    pct_remaining = max(1.0 - pct_complete, 0.0)
    
    data_r, data_c = r, c + 4
    val1 = ws.cell(row=data_r, column=data_c, value=pct_complete)
    val1.font = Font(color=theme["panel_bg"])  # Hide text
    
    val2 = ws.cell(row=data_r+1, column=data_c, value=pct_remaining)
    val2.font = Font(color=theme["panel_bg"])  # Hide text
    
    # 4. Add the % text that will appear INSIDE the doughnut hole
    ws.merge_cells(start_row=r+2, start_column=c+2, end_row=r+3, end_column=c+3)
    pct_cell = ws.cell(row=r+2, column=c+2, value=actual / target)
    pct_cell.font = Font(size=14, bold=True, color=theme["primary"])
    pct_cell.number_format = "0%"
    pct_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 5. Create and Position Doughnut Chart
    chart = DoughnutChart()
    data = Reference(ws, min_col=data_c, min_row=data_r, max_row=data_r+1)
    chart.add_data(data, titles_from_data=False)
    
    chart.width = 4.0   # ~2 columns wide
    chart.height = 3.0  # ~6 rows high
    chart.legend = None
    chart.title = None
    chart.holeSize = 75 # Maximize hole for the text behind it
    
    # Make chart area and plot area completely transparent
    chart.graphical_properties = GraphicalProperties(noFill=True)
    chart.graphical_properties.line = LineProperties(noFill=True)
    
    # Stretch plot area to fill the shape bounding box
    chart.layout = Layout(
        manualLayout=ManualLayout(x=0.0, y=0.0, w=1.0, h=1.0)
    )
    
    # Style the slices
    series = chart.series[0]
    
    # Completed Slice
    pt1 = DataPoint(idx=0)
    pt1.graphicalProperties.solidFill = theme["primary"]
    pt1.graphicalProperties.line = LineProperties(noFill=True)
    
    # Remaining Slice
    pt2 = DataPoint(idx=1)
    pt2.graphicalProperties.solidFill = theme["secondary"]
    pt2.graphicalProperties.line = LineProperties(noFill=True)
    
    series.dPt.append(pt1)
    series.dPt.append(pt2)
    
    # Place the chart so it hovers exactly over columns c+2 and c+3
    chart_anchor = f"{get_column_letter(c+2)}{r}"
    ws.add_chart(chart, chart_anchor)
