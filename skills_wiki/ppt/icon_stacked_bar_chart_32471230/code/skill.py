import io
import urllib.request
from typing import List, Tuple

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.util import Inches, Pt, Emu

# Helper function to inject XML
def _set_chart_series_picture_fill(chart, series_index, image_url, stack_unit=1000):
    """
    Sets the fill of a chart series to a stacked picture.
    This requires direct manipulation of the chart's XML.
    """
    # Namespace map for XML manipulation
    ns = {
        'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }

    # Get the chart's XML element tree
    chart_part = chart.part
    chart_element = chart_part.element
    tree = etree.fromstring(etree.tostring(chart_element))

    # Find the specific series to modify
    series_elements = tree.xpath('//c:ser', namespaces=ns)
    if series_index >= len(series_elements):
        raise ValueError("Series index out of range")
    target_series = series_elements[series_index]

    try:
        # Download the image and add it to the presentation package
        response = urllib.request.urlopen(image_url)
        image_data = response.read()
        image_stream = io.BytesIO(image_data)
        image_part, rId = chart_part.package.get_or_add_image_part(image_stream)
    except Exception as e:
        print(f"Warning: Could not download image from {image_url}. Error: {e}. Falling back to solid fill.")
        # Fallback to a solid fill if image download fails
        spPr = target_series.find('c:spPr', ns)
        if spPr is None:
            spPr = etree.SubElement(target_series, etree.QName(ns['c'], 'spPr'))
        
        solidFill = spPr.find('a:solidFill', ns)
        if solidFill is None:
            solidFill = etree.SubElement(spPr, etree.QName(ns['a'], 'solidFill'))
        
        srgbClr = solidFill.find('a:srgbClr', ns)
        if srgbClr is None:
            srgbClr = etree.SubElement(solidFill, etree.QName(ns['a'], 'srgbClr'))
        srgbClr.set('val', '8EA9DB') # A default blue color
        chart_part.element.body = tree
        return

    # Create the <c:spPr> (shape properties) element if it doesn't exist
    spPr = target_series.find('c:spPr', ns)
    if spPr is None:
        spPr = etree.SubElement(target_series, etree.QName(ns['c'], 'spPr'))
    
    # Remove any existing fill (like solidFill)
    for fill_type in ['solidFill', 'gradFill', 'pattFill', 'noFill']:
        existing_fill = spPr.find(f"a:{fill_type}", ns)
        if existing_fill is not None:
            spPr.remove(existing_fill)

    # Create the <a:blipFill> element for the picture fill
    blip_fill = etree.SubElement(spPr, etree.QName(ns['a'], 'blipFill'))
    blip = etree.SubElement(blip_fill, etree.QName(ns['a'], 'blip'))
    blip.set(etree.QName(ns['r'], 'embed'), rId)
    
    # Create the <c:pictureOptions> for stacking
    pic_opts = target_series.find('c:pictureOptions', ns)
    if pic_opts is None:
        # Insert after spPr for correct order
        spPr_index = target_series.index(spPr)
        pic_opts = etree.Element(etree.QName(ns['c'], 'pictureOptions'))
        target_series.insert(spPr_index + 1, pic_opts)

    # Set the stacking format and unit
    etree.SubElement(pic_opts, etree.QName(ns['c'], 'pictureFormat')).set('val', 'stack')
    etree.SubElement(pic_opts, etree.QName(ns['c'], 'pictureStackUnit')).set('val', str(stack_unit))

    # Apply the modified XML back to the chart part
    chart_part.element.body = tree


def create_slide(
    output_pptx_path: str,
    title_text: str = "2018北上广篮球场数量 单位(个)",
    chart_data: dict = None,
    icon_url: str = "https://www.flaticon.com/free-icon/basketball_889167?term=basketball&page=1&position=3&origin=search&related_id=889167", # A placeholder, better to use a direct image URL
    **kwargs,
) -> str:
    """
    Creates a PPTX file with an Icon-Stacked Bar Chart.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # === Layer 1: Background (Solid White) ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # === Layer 2: Chart & Content ===
    # --- Title ---
    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.name = 'Arial'
    p.font.color.rgb = RGBColor(89, 89, 89)

    # --- Chart Data ---
    if chart_data is None:
        chart_data_obj = CategoryChartData()
        chart_data_obj.categories = ['北京', '上海', '广州']
        chart_data_obj.add_series('篮球场数量', (9764, 8876, 6789))
    else:
        chart_data_obj = CategoryChartData()
        chart_data_obj.categories = list(chart_data.keys())
        chart_data_obj.add_series('Data', tuple(chart_data.values()))


    # --- Chart Creation ---
    x, y, cx, cy = Inches(1.5), Inches(1.5), Inches(10), Inches(5)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, x, y, cx, cy, chart_data_obj
    )
    chart = graphic_frame.chart

    # --- Chart Formatting ---
    chart.has_legend = False
    
    # Category axis (Y-axis) formatting
    category_axis = chart.category_axis
    category_axis.tick_labels.font.size = Pt(14)
    category_axis.tick_labels.font.color.rgb = RGBColor(89, 89, 89)
    category_axis.has_major_gridlines = False
    
    # Value axis (X-axis) formatting
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = False
    value_axis.tick_labels.font.size = Pt(12) 
    value_axis.visible = False # Hide the value axis

    # Data labels
    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
    data_labels.font.size = Pt(14)
    data_labels.font.color.rgb = RGBColor(89, 89, 89)
    
    # --- XML Injection for Picture Fill ---
    # NOTE: The free flaticon URL might not work directly. A direct link to a PNG is better.
    # Using a known-good direct link for reproducibility.
    basketball_icon_url = "https://i.imgur.com/gYf2z5L.png" 
    
    # The stacking unit determines how many data points one icon represents.
    # Adjust this value to make the chart look good. A smaller value means more icons.
    _set_chart_series_picture_fill(chart, 0, basketball_icon_url, stack_unit=500)

    prs.save(output_pptx_path)
    return output_pptx_path
