from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.colors import ColorChoice
from openpyxl.utils import coordinate_to_tuple, get_column_letter

def render(ws, anchor: str, *, title: str, actual_val: float, target_val: float, format_str: str = "#,##0", theme: str = "corporate_blue", **kwargs) -> None:
    row, col = coordinate_to_tuple(anchor)
    
    # Calculate progress metrics
    pct = actual_val / target_val if target_val != 0 else 0
    rem = 1 - pct if pct < 1 else 0
    
    # Theme color fallbacks
    bg_color = "FFFFFF"
    accent_color = "4F81BD" # Primary blue
    text_color = "595959"
    gray_color = "D9D9D9"
    
    # 1. Write chart data off-screen
    data_r1, data_c1 = row, col + 10
    ws.cell(row=data_r1, column=data_c1, value="Actual")
    ws.cell(row=data_r1+1, column=data_c1, value="Remainder")
    ws.cell(row=data_r1, column=data_c1+1, value=pct)
    ws.cell(row=data_r1+1, column=data_c1+1, value=rem)
    
    # 2. Style Card Area (4 rows x 5 cols)
    card_fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    border_thin = Side(style="thin", color=gray_color)
    border_shadow = Side(style="medium", color="BFBFBF")
    
    for r in range(row, row + 4):
        for c in range(col, col + 5):
            cell = ws.cell(row=r, column=c)
            cell.fill = card_fill
            # Add basic borders with a faux drop-shadow on bottom and right
            top = border_thin if r == row else None
            bottom = border_shadow if r == row + 3 else None
            left = border_thin if c == col else None
            right = border_shadow if c == col + 4 else None
            cell.border = Border(top=top, bottom=bottom, left=left, right=right)
            
    # 3. Add Title
    title_cell = ws.cell(row=row, column=col)
    title_cell.value = title
    title_cell.font = Font(name="Calibri", size=12, bold=True, color=text_color)
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+4)
    
    # 4. Add Primary Value
    val_cell = ws.cell(row=row+1, column=col)
    val_cell.value = actual_val
    val_cell.number_format = format_str
    val_cell.font = Font(name="Calibri", size=22, bold=True, color=accent_color)
    val_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.merge_cells(start_row=row+1, start_column=col, end_row=row+3, end_column=col+1)
    
    # 5. Create Progress Doughnut Chart
    chart = DoughnutChart()
    chart.width = 4.5
    chart.height = 2.5
    chart.holeSize = 65
    chart.legend = None
    chart.title = None
    
    # Strip borders and background from chart frame
    chart.graphical_properties = GraphicalProperties(line=LineProperties(noFill=True))
    
    # Bind Data
    data = Reference(ws, min_col=data_c1+1, min_row=data_r1, max_row=data_r1+1)
    chart.add_data(data, titles_from_data=False)
    series = chart.series[0]
    
    # 6. Color Data Points (Progress Ring)
    dp_actual = DataPoint(idx=0)
    dp_actual.graphicalProperties = GraphicalProperties(
        solidFill=ColorChoice(srgbClr=accent_color),
        line=LineProperties(noFill=True)
    )
    series.dPt.append(dp_actual)
    
    dp_rem = DataPoint(idx=1)
    dp_rem.graphicalProperties = GraphicalProperties(
        solidFill=ColorChoice(srgbClr=gray_color),
        line=LineProperties(noFill=True)
    )
    series.dPt.append(dp_rem)
    
    # Anchor the chart in the right half of the card
    chart_anchor = f"{get_column_letter(col+2)}{row+1}"
    ws.add_chart(chart, chart_anchor)
