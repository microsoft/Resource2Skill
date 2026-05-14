from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter

def render(ws, anchor: str, *, title: str, actual_value: float, target_value: float, value_format: str = "$#,##0", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a KPI card containing a main value and a progress doughnut chart.
    
    Example:
        render(ws, "B2", title="Sales Revenue", actual_value=2544, target_value=3000)
    """
    row, col = coordinate_to_tuple(anchor)
    
    # Percentage calculations
    percent_complete = min(actual_value / target_value, 1.0) if target_value else 0
    percent_remaining = 1.0 - percent_complete
    
    # Color configuration (Theme mapping)
    bg_color = "FFFFFF"
    title_color = "595959"
    val_color = "203864" if theme == "corporate_blue" else "000000" # Target theme color
    remainder_color = "D9D9D9" 
    border_color = "BFBFBF"
    
    # 1. Store chart data behind the chart (in right-side columns)
    # Using font color matching background to hide the numbers from view
    ws.cell(row=row+1, column=col+2, value=percent_complete).font = Font(color=bg_color)
    ws.cell(row=row+2, column=col+2, value=percent_remaining).font = Font(color=bg_color)
    
    # 2. Build the Card Grid (4x4 cells)
    card_fill = PatternFill("solid", fgColor=bg_color)
    thin_border = Side(style="thin", color=border_color)
    
    for r in range(row, row+4):
        for c in range(col, col+4):
            cell = ws.cell(row=r, column=c)
            cell.fill = card_fill
            # Draw perimeter border to simulate a "card" container
            borders = {}
            if r == row: borders['top'] = thin_border
            if r == row+3: borders['bottom'] = thin_border
            if c == col: borders['left'] = thin_border
            if c == col+3: borders['right'] = thin_border
            cell.border = Border(**borders)
            
    # 3. Add Title (Top row spanning all 4 cols)
    ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+3)
    title_cell = ws.cell(row=row, column=col)
    title_cell.value = title
    title_cell.font = Font(name="Arial", size=11, bold=True, color=title_color)
    title_cell.alignment = Alignment(vertical="center", horizontal="left")
    
    # 4. Add Main Value (Left 2 cols, middle 2 rows)
    ws.merge_cells(start_row=row+1, start_column=col, end_row=row+2, end_column=col+1)
    val_cell = ws.cell(row=row+1, column=col)
    val_cell.value = actual_value
    val_cell.number_format = value_format
    val_cell.font = Font(name="Arial", size=20, bold=True, color=val_color)
    val_cell.alignment = Alignment(vertical="center", horizontal="center")
    
    # 5. Add Subtext / Percentage (Left 2 cols, bottom row)
    ws.merge_cells(start_row=row+3, start_column=col, end_row=row+3, end_column=col+1)
    pct_cell = ws.cell(row=row+3, column=col)
    pct_cell.value = f"{percent_complete:.0%} of Target"
    pct_cell.font = Font(name="Arial", size=9, italic=True, color=title_color)
    pct_cell.alignment = Alignment(vertical="top", horizontal="center")
    
    # 6. Add Progress Doughnut Chart
    chart = DoughnutChart()
    chart.holeSize = 65
    chart.width = 3.5  # cm - fits roughly in 2 columns
    chart.height = 2.5 # cm - fits roughly in 3 rows
    chart.legend = None
    
    # Reference the hidden data
    data = Reference(ws, min_col=col+2, min_row=row+1, max_row=row+2)
    chart.add_data(data, titles_from_data=False)
    
    # Apply colors to slices to simulate a progress bar
    series = chart.series[0]
    
    pt_complete = DataPoint(idx=0)
    pt_complete.graphicalProperties.solidFill = val_color
    pt_remain = DataPoint(idx=1)
    pt_remain.graphicalProperties.solidFill = remainder_color
    
    series.dPt.append(pt_complete)
    series.dPt.append(pt_remain)
    
    # Position chart over the right two columns of the card
    ws.add_chart(chart, f"{get_column_letter(col+2)}{row+1}")
