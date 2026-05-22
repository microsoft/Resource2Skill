from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.styles import Font

def render(ws, anchor: str, *, metric_name: str = "Sales", actual: float = 2544, target: float = 3000, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a minimalist KPI Progress Doughnut chart at the specified anchor.
    Default values match the McDonald's Dashboard tutorial ($2,544 actual vs $3,000 target = ~85%).
    """
    # 1. Define colors (In production, these would be extracted from a theme palette helper)
    primary_hex = "1F4E78"   # Dark Blue accent for completion
    remainder_hex = "D9D9D9" # Light neutral gray for the remainder
    
    # 2. Calculate percentages
    pct_complete = max(0.0, min(actual / target if target else 0, 1.0))
    pct_remain = 1.0 - pct_complete
    
    # 3. Write background data directly at the anchor
    row = ws[anchor].row
    col = ws[anchor].column
    
    ws.cell(row=row, column=col, value="Complete")
    ws.cell(row=row, column=col+1, value=pct_complete).number_format = "0%"
    ws.cell(row=row+1, column=col, value="Remaining")
    ws.cell(row=row+1, column=col+1, value=pct_remain).number_format = "0%"
    
    # Hide the raw data by matching the font color to the assumed white background
    hidden_font = Font(color="FFFFFF")
    ws.cell(row=row, column=col).font = hidden_font
    ws.cell(row=row, column=col+1).font = hidden_font
    ws.cell(row=row+1, column=col).font = hidden_font
    ws.cell(row=row+1, column=col+1).font = hidden_font

    # 4. Construct the Chart
    chart = DoughnutChart()
    chart.width = 5.0
    chart.height = 4.0
    chart.holeSize = 65  # Key mechanism: Thicker ring characteristic of modern KPI dashboards
    chart.title = None
    chart.legend = None

    # 5. Bind Data
    data_ref = Reference(ws, min_col=col+1, min_row=row, max_row=row+1)
    cats_ref = Reference(ws, min_col=col, min_row=row, max_row=row+1)
    chart.add_data(data_ref, titles_from_data=False)
    chart.set_categories(cats_ref)

    # 6. Style the slices via indexed DataPoints
    series = chart.series[0]

    # First slice (Complete)
    dp_complete = DataPoint(idx=0)
    dp_complete.graphicalProperties = GraphicalProperties(solidFill=primary_hex)
    series.dPt.append(dp_complete)

    # Second slice (Remaining)
    dp_remain = DataPoint(idx=1)
    dp_remain.graphicalProperties = GraphicalProperties(solidFill=remainder_hex)
    series.dPt.append(dp_remain)

    # 7. Add to worksheet
    ws.add_chart(chart, anchor)
