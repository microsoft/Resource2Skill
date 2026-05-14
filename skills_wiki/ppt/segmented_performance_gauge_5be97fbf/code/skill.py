import os
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

def _add_shadow_effect(shape):
    """
    Adds a centered outer shadow effect to a shape by manipulating its OOXML.
    """
    spPr = shape.element.spPr
    
    # Ensure <a:effectLst> exists, create if not
    try:
        effect_lst = spPr.find(qn('a:effectLst'))
        if effect_lst is None:
            effect_lst = etree.SubElement(spPr, qn('a:effectLst'))
    except:
        effect_lst = etree.SubElement(spPr, qn('a:effectLst'))

    # Attributes for a "Offset: Center" preset shadow in PowerPoint
    outer_shadow = etree.SubElement(
        effect_lst,
        qn('a:outerShdw'),
        blurRad="50800", 
        dist="0", 
        dir="0", 
        algn="ctr", 
        rotWithShape="0"
    )
    
    # Color element for the shadow (black)
    srgb_clr = etree.SubElement(outer_shadow, qn('a:srgbClr'), val="000000")
    
    # Alpha (transparency) element - 60000 corresponds to 40% opaque (60% transparent)
    etree.SubElement(srgb_clr, qn('a:alpha'), val="60000")

def create_gauge_slide(
    output_pptx_path: str,
    title_text: str = "Performance Dashboard",
    values: list = [20, 40, 60, 80, 100],
    colors: list = [(192, 80, 77), (247, 150, 70), (155, 187, 89), (79, 129, 189), (65, 113, 156)],
    needle_value: float = 68.0,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a stylized Segmented Performance Gauge.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The title for the slide.
        values (list): A list of the upper bounds for each segment (e.g., 20, 40, 60, 80, 100).
        colors (list): A list of RGB tuples for the color of each segment.
        needle_value (float): The value the gauge needle should point to.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[5]) # Title Only layout

    # --- Set Title ---
    title = slide.shapes.title
    title.text = title_text
    title.text_frame.paragraphs[0].font.size = Pt(32)
    title.left = Inches(0.5)
    title.top = Inches(0.2)
    
    # --- Gauge Parameters ---
    center_x = Inches(13.333 / 2)
    center_y = Inches(7.5 / 1.8)
    radius = Inches(2.5)
    thickness = Inches(1.0) 

    # --- Create Gauge Segments ---
    full_range = values[-1]
    total_angle_span = 180.0
    start_angle_ppt = 180  # 180 degrees is 9 o'clock in PowerPoint's shape coordinates
    
    gauge_shapes = []

    current_angle_start = 0
    for i, upper_bound in enumerate(values):
        lower_bound = values[i-1] if i > 0 else 0
        segment_range = upper_bound - lower_bound
        sweep_angle = (segment_range / full_range) * total_angle_span
        
        arc = slide.shapes.add_shape(
            MSO_SHAPE.BLOCK_ARC,
            center_x - radius, center_y - radius,
            radius * 2, radius * 2
        )
        
        # Adjustments: 0=start_angle, 1=end_angle, 2=thickness
        arc.adjustments[0] = start_angle_ppt + current_angle_start
        arc.adjustments[1] = start_angle_ppt + current_angle_start + sweep_angle
        arc.adjustments[2] = (thickness / radius) * 50000

        fill = arc.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(f"{colors[i % len(colors)][0]:02x}{colors[i % len(colors)][1]:02x}{colors[i % len(colors)][2]:02x}")
        arc.line.fill.background() # No outline
        
        gauge_shapes.append(arc)
        current_angle_start += sweep_angle

    # --- Create Text Labels ---
    text_radius = radius - (thickness / 2)
    for i, upper_bound in enumerate(values):
        lower_bound = values[i-1] if i > 0 else 0
        mid_point_value = lower_bound + (upper_bound - lower_bound) / 2
        
        angle_rad = math.radians(180 - (mid_point_value / full_range) * 180)
        
        text_x = center_x + text_radius * math.cos(angle_rad)
        text_y = center_y - text_radius * math.sin(angle_rad)

        txBox = slide.shapes.add_textbox(
            text_x - Inches(0.3), text_y - Inches(0.15),
            Inches(0.6), Inches(0.3)
        )
        p = txBox.text_frame.paragraphs[0]
        p.text = f"{upper_bound}%"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        txBox.text_frame.margin_bottom = 0
        txBox.text_frame.margin_top = 0
        
        gauge_shapes.append(txBox)

    # --- Create the Needle ---
    needle_base_radius = Inches(0.25)
    needle_base = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        center_x - needle_base_radius, center_y - needle_base_radius,
        needle_base_radius * 2, needle_base_radius * 2
    )
    needle_base.fill.solid()
    needle_base.fill.fore_color.rgb = RGBColor(89, 89, 89)
    needle_base.line.fill.background()
    
    pointer_height = radius
    pointer_width = Inches(0.1)
    pointer = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE,
        center_x - (pointer_width / 2), center_y - pointer_height,
        pointer_width, pointer_height
    )
    pointer.fill.solid()
    pointer.fill.fore_color.rgb = RGBColor(89, 89, 89)
    pointer.line.fill.background()
    
    needle_parts = [pointer, needle_base]
    
    # --- Position and Rotate Needle ---
    needle_angle = 180 - ((needle_value / full_range) * 180.0)
    for part in needle_parts:
        part.rotation = needle_angle

    gauge_shapes.extend(needle_parts)

    # --- Group everything and apply shadow ---
    if gauge_shapes:
        full_gauge_group = slide.shapes.group_shapes(gauge_shapes)
        _add_shadow_effect(full_gauge_group)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
if __name__ == '__main__':
    file_path = "segmented_performance_gauge.pptx"
    
    create_gauge_slide(
        output_pptx_path=file_path,
        title_text="Customer Satisfaction Index (CSI)",
        values=[20, 40, 60, 80, 100],
        colors=[(192, 0, 0), (255, 192, 0), (146, 208, 80), (0, 176, 80), (0, 112, 192)],
        needle_value=85.0
    )

    print(f"Generated gauge chart at '{file_path}'")
    # To view the file, you might want to open it automatically
    if os.name == 'nt': # For Windows
        os.startfile(file_path)
    elif os.name == 'posix': # For MacOS/Linux
        os.system(f'open {file_path}' if os.uname().sysname == 'Darwin' else f'xdg-open {file_path}')

