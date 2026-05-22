import os
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

def qn(tag):
    """
    A qualified name utility function to generate Clark-notation tag names for lxml.
    Example: 'c:chart' -> '{http://schemas.openxmlformats.org/drawingml/2006/chart}chart'
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }
    prefix, local_name = tag.split(':')
    return f'{{{nsmap[prefix]}}}{local_name}'

def set_doughnut_hole_size(doughnut_chart, hole_size_percent=75):
    """
    Sets the hole size for a doughnut chart via XML manipulation.
    """
    chart_xml = etree.fromstring(doughnut_chart.chart.blob)
    plot_area = chart_xml.find('.//c:doughnutChart', namespaces=chart_xml.nsmap)
    if plot_area is not None:
        hole_size = plot_area.find('.//c:holeSize', namespaces=chart_xml.nsmap)
        if hole_size is None:
            hole_size = etree.SubElement(plot_area, qn('c:holeSize'))
        hole_size.set('val', str(hole_size_percent))
    doughnut_chart.chart.blob = etree.tostring(chart_xml)

def create_kpi_gauge_slide(
    output_pptx_path: str,
    kpi_value: int = 53,
    gauge_color: tuple = (243, 156, 18),
    gauge_bg_color: tuple = (217, 217, 217),
    title: str = "KPI Gauge Chart",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a data-driven KPI gauge chart.

    This function reproduces the effect of using a modified doughnut chart
    to create a speedometer-style gauge. The pointer's rotation and the chart's
    transparent slice are handled by direct XML manipulation.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        kpi_value (int): The percentage value to display (0-100).
        gauge_color (tuple): RGB tuple for the gauge's "filled" section.
        gauge_bg_color (tuple): RGB tuple for the gauge's "unfilled" background.
        title (str): The title for the slide.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    title_shape = slide.shapes.title
    title_shape.text = title

    # === 1. Create the Doughnut Chart for the Gauge ===
    chart_data = ChartData()
    chart_data.categories = ['Value', 'Remainder', 'Hidden Base']
    
    value = max(0, min(100, kpi_value))
    remainder = 100 - value
    hidden_base = 100 # This large slice forms the invisible bottom half
    chart_data.add_series('KPI', (value, remainder, hidden_base))

    x, y, cx, cy = Inches(4.17), Inches(1.75), Inches(5), Inches(5)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, x, y, cx, cy, chart_data
    )
    chart = graphic_frame.chart

    # === 2. Style the Chart to Look Like a Gauge ===
    chart.has_legend = False
    chart.has_title = False
    chart.plot_area.format.fill.background()
    chart.plot_area.format.line.fill.background()
    chart.plot_area.first_slice_angle = 270 # Start gauge at the bottom

    # Style the "Value" slice
    point_val = chart.series[0].points[0]
    point_val.format.fill.solid()
    point_val.format.fill.fore_color.rgb = RGBColor(*gauge_color)
    point_val.format.line.fill.background()

    # Style the "Remainder" slice
    point_rem = chart.series[0].points[1]
    point_rem.format.fill.solid()
    point_rem.format.fill.fore_color.rgb = RGBColor(*gauge_bg_color)
    point_rem.format.line.fill.background()

    # Make the "Hidden Base" slice transparent via XML injection
    chart_xml = etree.fromstring(chart.blob)
    dpt_base_element = chart_xml.xpath("//c:dPt[c:idx[@val='2']]")[0]
    spPr_element = etree.SubElement(dpt_base_element, qn('c:spPr'))
    etree.SubElement(spPr_element, qn('a:noFill'))
    chart.blob = etree.tostring(chart_xml)

    set_doughnut_hole_size(chart, 80)
    
    # === 3. Create and Rotate the Pointer ===
    grp_cx, grp_cy = Inches(4), Inches(4)
    grp_x, grp_y = x + (cx - grp_cx) / 2, y + (cy - grp_cy) / 2
    
    group_shape = slide.shapes.add_group_shape()
    group_shape.left, group_shape.top = int(grp_x), int(grp_y)
    group_shape.width, group_shape.height = int(grp_cx), int(grp_cy)

    needle_height = grp_cy / 2 * 0.9
    needle = group_shape.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE,
        left=int(grp_cx/2 - Inches(0.05)), top=int(grp_cy/2 - needle_height),
        width=int(Inches(0.1)), height=int(needle_height)
    )
    needle.rotation = 180  # Point upwards
    needle.fill.solid()
    needle.fill.fore_color.rgb = RGBColor(89, 89, 89)
    needle.line.fill.background()

    pivot_size = Inches(0.25)
    pivot = group_shape.shapes.add_shape(
        MSO_SHAPE.OVAL,
        left=int(grp_cx/2 - pivot_size/2), top=int(grp_cy/2 - pivot_size/2),
        width=int(pivot_size), height=int(pivot_size)
    )
    pivot.fill.solid()
    pivot.fill.fore_color.rgb = RGBColor(89, 89, 89)
    pivot.line.fill.background()

    # Calculate rotation: 180-degree range, starting at -90 degrees
    angle_deg = (value / 100.0) * 180 - 90
    angle_emu = int(angle_deg * 60000)

    # Apply rotation to the group shape via lxml
    group_xml = group_shape._element
    xfrm = group_xml.find('.//a:xfrm', namespaces=group_xml.nsmap)
    if xfrm is not None:
        xfrm.set('rot', str(angle_emu))

    # === 4. Add the KPI Value Text Box ===
    text_box = slide.shapes.add_textbox(
        left=x, top=y + Inches(3.25), width=cx, height=Inches(1)
    )
    p = text_box.text_frame.paragraphs[0]
    p.text = f"{kpi_value}%"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*gauge_color)
    p.alignment = 1  # Center alignment

    prs.save(output_pptx_path)
    return output_pptx_path
