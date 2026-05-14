import openpyxl
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.styles import Font, Alignment
from openpyxl.utils import coordinate_from_string, column_index_from_string

def render(ws, anchor: str, *, title: str = "Sales Target", actual: float = 850, target: float = 1000, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a transparent Donut Chart KPI over a formatted cell containing the percentage.
    This creates the "linked textbox" effect purely using cells and charts.
    """
    # 1. Resolve Anchor and Geometry
    col_str, row_str = coordinate_from_string(anchor)
    col_idx = column_index_from_string(col_str)
    row_idx = int(row_str)
    
    # Create a square-ish cell to hold the transparent chart (approx 80x80 pixels)
    ws.row_dimensions[row_idx].height = 65
    ws.column_dimensions[col_str].width = 14
    
    pct_complete = min(actual / target, 1.0)
    pct_remain = 1.0 - pct_complete
    
    # Theme palette fallback
    primary_color = kwargs.get("primary_color", "003366")  # Dark Blue
    track_color = kwargs.get("track_color", "D9E1E8")      # Light Gray-Blue
    
    # 2. Setup the text in the center
    anchor_cell = ws[anchor]
    anchor_cell.value = pct_complete
    anchor_cell.number_format = '0%'
    anchor_cell.font = Font(size=18, bold=True, color=primary_color)
    anchor_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Add title above the chart
    title_cell = ws.cell(row=row_idx - 1, column=col_idx)
    title_cell.value = title
    title_cell.font = Font(size=11, bold=True, color="555555")
    title_cell.alignment = Alignment(horizontal="center", vertical="bottom")
    
    # 3. Write Chart Data (offset to a hidden area far right)
    data_col = col_idx + 20
    ws.cell(row=row_idx, column=data_col, value="Complete")
    ws.cell(row=row_idx + 1, column=data_col, value="Remaining")
    ws.cell(row=row_idx, column=data_col + 1, value=pct_complete)
    ws.cell(row=row_idx + 1, column=data_col + 1, value=pct_remain)
    
    # 4. Create the Transparent Doughnut Chart
    chart = DoughnutChart()
    chart.holeSize = 65
    chart.width = 2.4   # ~85 pixels to perfectly overlay the cell
    chart.height = 2.4
    chart.title = None
    chart.legend = None
    
    # Make chart area and borders completely transparent
    transparent_props = GraphicalProperties(noFill=True)
    transparent_props.line = LineProperties(noFill=True)
    chart.graphical_properties = transparent_props
    
    # Provide Data
    data = Reference(ws, min_col=data_col+1, min_row=row_idx, max_row=row_idx+1)
    cats = Reference(ws, min_col=data_col, min_row=row_idx, max_row=row_idx+1)
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(cats)
    
    # Color the slices
    series = chart.series[0]
    
    pt1 = DataPoint(idx=0)
    pt1.graphicalProperties.solidFill = primary_color
    series.dPt.append(pt1)
    
    pt2 = DataPoint(idx=1)
    pt2.graphicalProperties.solidFill = track_color
    series.dPt.append(pt2)
    
    # 5. Anchor the chart over the cell
    chart.anchor = anchor
    ws.add_chart(chart)
