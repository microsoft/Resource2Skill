from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

def render(ws, anchor: str, data_range: str, cats_range: str, title: str = "Conversion Overlap", *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an overlaid 'bullet' column chart.
    
    :param data_range: e.g., "B1:C13" (Should include headers. B is the larger metric, C is the smaller subset).
    :param cats_range: e.g., "A2:A13" (The category labels, e.g., Months).
    """
    chart = BarChart()
    chart.title = title
    chart.type = "col"  # Vertical columns
    
    # 1. Core Trick: Superimpose the columns front-to-back
    chart.overlap = 100
    
    # 2. Thicker columns for better visibility of inside-labels
    chart.gapWidth = 50
    
    # Add data
    data = Reference(ws, range_string=data_range)
    cats = Reference(ws, range_string=cats_range)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    
    # Move legend to top to save horizontal real estate
    if chart.legend:
        chart.legend.position = "t"
    
    # Embed data labels inside the top edge of the columns
    chart.dataLabels = DataLabelList()
    chart.dataLabels.showVal = True
    chart.dataLabels.position = "inEnd"
    
    # Clean up axes: Y-min to 0, no distracting gridlines
    chart.y_axis.scaling.min = 0
    chart.y_axis.majorGridlines = None
    
    # Apply theme colors
    # (Using the video's high-contrast Gold/Purple combination as the 'aspect_purple' fallback)
    palettes = {
        "corporate_blue": ["4F81BD", "C0504D"],
        "aspect_purple": ["FFC000", "7030A0"], 
    }
    colors = palettes.get(theme, palettes["corporate_blue"])
    
    for i, series in enumerate(chart.series):
        # Openpyxl 3.x property assignment for solid fill
        series.graphicalProperties.solidFill = colors[i % len(colors)]
        
    ws.add_chart(chart, anchor)
