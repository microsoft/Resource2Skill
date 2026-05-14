import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from lxml import etree

# Helper to get XML namespace prefixes for lxml
_nsmap = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

def _ns(tag):
    """
    Given a namespace-prefixed tag, return the lxml-friendly qualified name.
    e.g., _ns('p:spPr') returns '{http://...}spPr'
    """
    prefix, tag_name = tag.split(':')
    return f'{{{_nsmap[prefix]}}}{tag_name}'

def create_slide(
    output_pptx_path: str,
    cta_text: str = "Get Instant Access",
    testimonial_text: str = (
        "That's it. Master these 3 skills and nothing can stop you from being a success. "
        "Well, in theory that's all well and good. In reality though, it's never that easy, is it?\n\n"
        "If we add a 4th skill to that list then nothing can stop you. The 4th skill is actually "
        "far more important than the previous 3 I mentioned above. What is it?"
    ),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with styled Call-to-Action buttons and testimonial boxes,
    reproducing the effect from the tutorial.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background (Solid White as per tutorial) ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # === Effect 1: Call-to-Action (CTA) Button ===
    cta_left, cta_top, cta_width, cta_height = Inches(3.67), Inches(1), Inches(6), Inches(1.2)
    shape_cta = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cta_left, cta_top, cta_width, cta_height)

    # Basic Fill and Line
    shape_cta.fill.solid()
    shape_cta.fill.fore_color.rgb = RGBColor(255, 255, 0)
    line_cta = shape_cta.line
    line_cta.color.rgb = RGBColor(89, 89, 89)
    line_cta.width = Pt(2.25)

    # XML Injection for Bevel Effect
    spPr = shape_cta.element.get_or_add_p_spPr()
    effect_list = etree.SubElement(spPr, _ns('a:effectLst'))
    etree.SubElement(effect_list, _ns('a:bevel'), w="57150", h="57150", prst="circle")

    # Add and Style Text
    text_frame_cta = shape_cta.text_frame
    text_frame_cta.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_cta = text_frame_cta.paragraphs[0]
    p_cta.alignment = PP_ALIGN.CENTER
    run_cta = p_cta.add_run()
    run_cta.text = cta_text
    
    font_cta = run_cta.font
    font_cta.name = 'Calibri'
    font_cta.size = Pt(36)
    font_cta.bold = True

    # XML Injection for Text WordArt Style (Gradient Fill + Outline)
    rPr = run_cta._r.get_or_add_rPr()
    rPr.set('b', '1') # Ensure bold is set in XML
    
    grad_fill = etree.SubElement(rPr, _ns('a:gradFill'))
    etree.SubElement(grad_fill, _ns('a:lin'), ang="5400000", scaled="0")
    gs_list = etree.SubElement(grad_fill, _ns('a:gsLst'))
    gs1 = etree.SubElement(gs_list, _ns('a:gs'), pos="0")
    etree.SubElement(gs1, _ns('a:srgbClr'), val="9B2B22") # Dark Red
    gs2 = etree.SubElement(gs_list, _ns('a:gs'), pos="100000")
    etree.SubElement(gs2, _ns('a:srgbClr'), val="4C0099") # Dark Purple

    line_props = etree.SubElement(rPr, _ns('a:ln'), w="12700", cap="flat", cmpd="sng", algn="ctr")
    solid_fill_line = etree.SubElement(line_props, _ns('a:solidFill'))
    etree.SubElement(solid_fill_line, _ns('a:srgbClr'), val="000000")

    # === Effect 2: Testimonial Box ===
    test_left, test_top, test_width, test_height = Inches(2.67), Inches(3.0), Inches(8), Inches(3.5)
    shape_test = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, test_left, test_top, test_width, test_height)

    # XML Injection for Red Gradient Fill and Bevel
    spPr_test = shape_test.element.get_or_add_p_spPr()
    
    grad_fill_test = etree.SubElement(spPr_test, _ns('a:gradFill'), rotWithShape="1")
    etree.SubElement(grad_fill_test, _ns('a:lin'), ang="5400000", scaled="0")
    gs_list_test = etree.SubElement(grad_fill_test, _ns('a:gsLst'))
    gs1_test = etree.SubElement(gs_list_test, _ns('a:gs'), pos="0")
    etree.SubElement(gs1_test, _ns('a:srgbClr'), val="FF0000") # Bright Red
    gs2_test = etree.SubElement(gs_list_test, _ns('a:gs'), pos="100000")
    etree.SubElement(gs2_test, _ns('a:srgbClr'), val="990000") # Dark Red

    effect_list_test = etree.SubElement(spPr_test, _ns('a:effectLst'))
    etree.SubElement(effect_list_test, _ns('a:bevel'), w="76200", h="76200")
    
    # Add and Style Text
    text_frame_test = shape_test.text_frame
    text_frame_test.margin_left = Inches(0.2)
    text_frame_test.margin_right = Inches(0.2)
    text_frame_test.word_wrap = True
    p_test = text_frame_test.paragraphs[0]
    p_test.alignment = PP_ALIGN.LEFT
    run_test = p_test.add_run()
    run_test.text = testimonial_text
    
    font_test = run_test.font
    font_test.name = 'Calibri'
    font_test.size = Pt(18)
    font_test.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
