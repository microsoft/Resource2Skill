from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

def render(ws, anchor: str, *, min_col: int, min_row: int, max_row: int, title: str = "Total vs. Subset", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an overlapped column chart.
    Expects data to be exactly 3 columns starting at (min_row, min_col):
      Col 1: Categories (e.g., Months)
      Col 2: Total Values (larger bars, e.g., 'Calls Reached')
      Col 3: Subset Values (smaller bars, e.g., 'Deals Closed')
    """
    # Load theme colors, fallback to standard hex if helper is missing
    try:
        from _helpers import get_theme
        theme_colors = get_theme(theme)
        c_total = theme_colors.get("primary", "FFC000").replace("#", "")
        c_subset = theme_colors.get("accent", "7030A0").replace("#", "")
    except ImportError:
        c_total = "FFC000"  # Gold
        c_subset = "7030A0" # Purple
        
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "clustered"
    
    # Core Mechanism: 100% overlap overlays the bars, 50% gap width makes them thicker
    chart.overlap = 100
    chart.gapWidth = 50
    chart.title = title
    
    # Clean dashboard formatting
    chart.legend.position = "t"
    chart.y_axis.majorGridlines = None
    
    # Setup data references (2 data columns)
    data = Reference(ws, min_col=min_col+1, min_row=min_row, max_col=min_col+2, max_row=max_row)
    cats = Reference(ws, min_col=min_col, min_row=min_row+1, max_row=max_row)
    
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    
    # Apply series styling
    if len(chart.series) >= 2:
        s1 = chart.series[0]
        s2 = chart.series[1]
        
        # Apply theme colors
        s1.graphicalProperties.solidFill = c_total
        s2.graphicalProperties.solidFill = c_subset
        
        # Add Data Labels to the smaller subset series and position at the inner top
        s2.dLbls = DataLabelList()
        s2.dLbls.showVal = True
        s2.dLbls.dLblPos = "inEnd"
        
    ws.add_chart(chart, anchor)
