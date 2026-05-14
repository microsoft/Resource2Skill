import collections.abc
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from lxml import etree

# Define XML namespaces for chart manipulation
_ns = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}

def _set_bar_color(chart, series_idx, point_idx, rgb_hex):
    """
    Helper function to set the color of a single bar in a chart series using lxml.
    """
    chart_part = chart.part
    chart_xml = chart_part.chart_xml
    chart_base = etree.fromstring(chart_xml)

    series_elements = chart_base.xpath('c:chart/c:plotArea/c:barChart/c:ser', namespaces=_ns)
    if series_idx >= len(series_elements):
        return
    series_element = series_elements[series_idx]

    # Find or create the data point element (dPt) for the specific bar
    dpt_xpath = f'c:dPt[c:idx[@val="{point_idx}"]]'
    dpt_element = series_element.find(dpt_xpath, namespaces=_ns)
    if dpt_element is None:
        dpt_element = etree.SubElement(series_element, etree.QName(_ns['c'], 'dPt'))
        idx_element = etree.SubElement(dpt_element, etree.QName(_ns['c'], 'idx'))
        idx_element.set('val', str(point_idx))

    # Add shape properties (spPr) and solid fill with the specified color
    spPr_element = etree.SubElement(dpt_element, etree.QName(_ns['c'], 'spPr'))
    solidFill_element = etree.SubElement(spPr_element, etree.QName(_ns['a'], 'solidFill'))
    srgbClr_element = etree.SubElement(solidFill_element, etree.QName(_ns['a'], 'srgbClr'))
    srgbClr_element.set('val', rgb_hex)

    # Update the chart's XML with the new color information
    chart_part._chart_xml = etree.tostring(chart_base, pretty_print=False)

def create_slide(
    output_pptx_path: str,
    chart_title: str = "App Downloads 2020 (Millions)",
    chart_data: dict = None,
    highlight_points: list = None,
    **kwargs
) -> str:
    """
    Creates a PPTX with a sequence of slides to animate focus on specific
    data points in a bar chart, reproducing the 'Sequential Data Point Focus' effect.

    Args:
        output_pptx_path (str): Path to save the generated .pptx file.
        chart_title (str): The title for the chart.
        chart_data (dict): Data for the chart, e.g., {"categories": [...], "values": [...]}.
        highlight_points (list): A list of tuples, each defining a focus slide:
                                 (index_to_highlight, (R, G, B) color).

    Returns:
        str: The path to the saved PPTX file.
    """
    # --- Default Data & Colors ---
    if chart_data is None:
        chart_data = {
            "categories": ["TikTok", "WhatsApp", "Facebook", "Instagram", "Zoom"],
            "values": [850, 600, 540, 503, 477]
        }
    if highlight_points is None:
        highlight_points = [
            (0, (25, 63, 114)),   # Highlight TikTok in Dark Blue
            (4, (78, 172, 160))   # Highlight Zoom in Teal
        ]
    
    inactive_color_hex = "D3D3D3"  # Light Gray
    default_bar_color = RGBColor(47, 82, 143)
    
    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # --- Chart Data and Base Styling Function ---
    categories = chart_data['categories']
    values = chart_data['values']
    chart_data_obj = ChartData()
    chart_data_obj.categories = categories
    chart_data_obj.add_series('Data', values)

    def style_chart(chart):
        chart.has_title = True
        chart.chart_title.text_frame.text = chart_title
        chart.chart_title.text_frame.paragraphs[0].font.size = Pt(24)
        
        chart.category_axis.tick_labels.font.size = Pt(12)
        
        value_axis = chart.value_axis
        value_axis.has_major_gridlines = False
        value_axis.visible = False # Hide axis for a cleaner look
        
        chart.has_legend = False
        
        plot = chart.plots[0]
        plot.has_data_labels = True
        data_labels = plot.data_labels
        data_labels.font.size = Pt(14)
        data_labels.font.bold = True

    # --- Slide 1: Full Color Chart (Optional introduction slide) ---
    slide1 = prs.slides.add_slide(blank_slide_layout)
    x, y, cx, cy = Inches(1.5), Inches(1.5), Inches(10), Inches(5.5)
    chart1 = slide1.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data_obj
    ).chart
    style_chart(chart1)
    chart1.series[0].format.fill.solid()
    chart1.series[0].format.fill.fore_color.rgb = default_bar_color
    chart1.plots[0].data_labels.font.color.rgb = RGBColor(255, 255, 255)


    # --- Generate Highlight Slides ---
    for point_idx, highlight_rgb in highlight_points:
        slide = prs.slides.add_slide(blank_slide_layout)
        
        chart_graphic_frame = slide.shapes.add_chart(
            XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data_obj
        )
        chart = chart_graphic_frame.chart
        style_chart(chart)
        
        highlight_color_hex = f'{highlight_rgb[0]:02x}{highlight_rgb[1]:02x}{highlight_rgb[2]:02x}'
        
        # Color all bars: inactive gray, except the highlighted one
        for i in range(len(categories)):
            if i == point_idx:
                _set_bar_color(chart, 0, i, highlight_color_hex)
                chart.plots[0].data_labels.font.color.rgb = RGBColor(255, 255, 255)
            else:
                _set_bar_color(chart, 0, i, inactive_color_hex)
                chart.plots[0].data_labels.font.color.rgb = RGBColor(89, 89, 89)

    prs.save(output_pptx_path)
    return output_pptx_path
