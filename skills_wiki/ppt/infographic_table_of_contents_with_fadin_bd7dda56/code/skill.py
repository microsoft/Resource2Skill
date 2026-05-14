import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "Table of content",
    list_items: list = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with an infographic-style table of contents.

    Args:
        output_pptx_path: Path to save the generated PPTX file.
        title_text: The main title for the slide.
        list_items: A list of strings for the content items. Defaults to a sample list if None.

    Returns:
        The path to the saved PPTX file.
    """

    # --- Namespace setup for lxml ---
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    def set_transparent_gradient(shape, rgb_color_hex, angle=0):
        """
        Applies a linear gradient fading to transparent using lxml.
        Angle 0 is left-to-right, 90 is top-to-bottom.
        """
        sp = shape._element
        spPr = sp.get_or_add_p_spPr()
        
        gradFill = etree.SubElement(spPr, etree.QName(ns['a'], 'gradFill'))
        lin = etree.SubElement(gradFill, etree.QName(ns['a'], 'lin'), {'ang': str(angle * 60000), 'scaled': '1'})
        
        gsLst = etree.SubElement(gradFill, etree.QName(ns['a'], 'gsLst'))
        
        # Gradient Stop 1: Solid color (left side)
        gs1 = etree.SubElement(gsLst, etree.QName(ns['a'], 'gs'), {'pos': '0'})
        srgbClr1 = etree.SubElement(gs1, etree.QName(ns['a'], 'srgbClr'), {'val': rgb_color_hex})
        alpha1 = etree.SubElement(srgbClr1, etree.QName(ns['a'], 'alpha'), {'val': '100000'}) # 100% opaque

        # Gradient Stop 2: Transparent color (right side)
        gs2 = etree.SubElement(gsLst, etree.QName(ns['a'], 'gs'), {'pos': '100000'})
        srgbClr2 = etree.SubElement(gs2, etree.QName(ns['a'], 'srgbClr'), {'val': rgb_color_hex})
        alpha2 = etree.SubElement(srgbClr2, etree.QName(ns['a'], 'alpha'), {'val': '0'}) # 0% opaque (fully transparent)

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Set Slide Background ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)

    # --- Define Colors & Content ---
    if list_items is None:
        list_items = [
            "Your text here", "Your text here", "Your text here",
            "Your text here", "Your text here", "Your text here"
        ]
        
    color_palette = [
        RGBColor(231, 76, 60),    # 1. Red
        RGBColor(155, 89, 182),   # 2. Purple
        RGBColor(52, 152, 219),   # 3. Blue
        RGBColor(46, 204, 113),   # 4. Green
        RGBColor(241, 196, 15),   # 5. Yellow-Orange
        RGBColor(230, 126, 34),   # 6. Orange
    ]
    
    # --- Layer 1: Thematic Graphic (Left Side) ---
    graphic_cx, graphic_cy = Inches(2.5), prs.slide_height / 2
    outer_radius = Inches(1.8)
    
    # Outer gray circle
    outer_ring = slide.shapes.add_shape(
        MSO_SHAPE.DONUT, 
        graphic_cx - outer_radius, graphic_cy - outer_radius,
        outer_radius * 2, outer_radius * 2
    )
    outer_ring.adjustments[0] = 0.85 # Make it a thin ring
    fill = outer_ring.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(235, 235, 235)
    outer_ring.line.fill.background()

    # Inner gray circle
    inner_radius = outer_radius * 0.82
    inner_ring = slide.shapes.add_shape(
        MSO_SHAPE.DONUT, 
        graphic_cx - inner_radius, graphic_cy - inner_radius,
        inner_radius * 2, inner_radius * 2
    )
    inner_ring.adjustments[0] = 0.95
    fill = inner_ring.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(221, 221, 221)
    inner_ring.line.fill.background()

    # Placeholder "Brain" Icon (simplified)
    brain_radius = inner_radius * 0.90
    brain_shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        graphic_cx - brain_radius, graphic_cy - brain_radius,
        brain_radius * 2, brain_radius * 2
    )
    fill = brain_shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(204, 236, 255) # Light Cyan
    brain_shape.line.fill.fore_color.rgb = RGBColor(0, 176, 240)
    brain_shape.line.width = Pt(1.5)

    # --- Layer 2: Content (Right Side) ---
    start_x = Inches(5.0)
    start_y = Inches(1.5)
    bar_height = Inches(0.7)
    bar_width = Inches(7.5)
    circle_diameter = bar_height
    vertical_gap = Inches(0.2)
    
    # Title
    title_box = slide.shapes.add_textbox(start_x, Inches(0.5), bar_width, Inches(0.5))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = 'Calibri'
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(89, 89, 89)

    # Underline and dots
    line = slide.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, start_x, Inches(1.05), Inches(2.5), Inches(0))
    line.line.color.rgb = RGBColor(150, 150, 150)
    line.line.width = Pt(1)
    
    dot_start_x = start_x
    for i in range(6):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, dot_start_x + Inches(i*0.25), Inches(0.9), Inches(0.1), Inches(0.1))
        dot.fill.solid()
        dot.fill.fore_color.rgb = color_palette[i]
        dot.line.fill.background()

    # List Items
    for i, item_text in enumerate(list_items):
        current_y = start_y + i * (bar_height + vertical_gap)
        
        # Gradient Bar
        bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, start_x, current_y, bar_width, bar_height
        )
        bar.line.fill.background()
        set_transparent_gradient(bar, 'D9D9D9') # Hex for RGB(217,217,217)
        
        # Number Circle
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, start_x - circle_diameter / 2, current_y, circle_diameter, circle_diameter
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = color_palette[i % len(color_palette)]
        circle.line.fill.background()
        
        # Number Text
        tf_num = circle.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = str(i + 1)
        p_num.font.name = 'Arial'
        p_num.font.bold = True
        p_num.font.size = Pt(22)
        p_num.font.color.rgb = RGBColor(255, 255, 255)
        p_num.alignment = PP_ALIGN.CENTER
        tf_num.vertical_anchor = 'middle'
        
        # Item Text
        tf_item = slide.shapes.add_textbox(start_x + Inches(0.5), current_y, bar_width - Inches(0.7), bar_height).text_frame
        p_item = tf_item.paragraphs[0]
        p_item.text = item_text
        p_item.font.name = 'Calibri'
        p_item.font.size = Pt(20)
        p_item.font.color.rgb = RGBColor(89, 89, 89)
        tf_item.vertical_anchor = 'middle'

    # --- Save Presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path
