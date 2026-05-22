import requests
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

def _set_transition(slide, transition_type="morph", duration="1500"):
    """
    Sets a slide transition using lxml to manipulate the underlying XML.
    `python-pptx` does not support this natively.
    """
    slide_xml = slide._element
    transition_ns = '{' + slide_xml.nsmap['p'] + '}'
    
    # Find or create the <p:transition> element
    transition_tag = slide_xml.find('.//p:transition', namespaces=slide_xml.nsmap)
    if transition_tag is None:
        transition_tag = etree.SubElement(slide_xml, f"{transition_ns}transition")

    # Clear existing transition details to be safe
    for child in list(transition_tag):
        transition_tag.remove(child)

    # Set duration
    transition_tag.set('dur', duration) # in milliseconds

    # Add the specific transition effect
    if transition_type == "morph":
        morph_effect = etree.SubElement(transition_tag, f"{transition_ns}morph")
        morph_effect.set('thruBlk', '1')
    elif transition_type == "push":
        push_effect = etree.SubElement(transition_tag, f"{transition_ns}push")
        push_effect.set('dir', 'u') # 'u' for up

def _add_hyperlink_to_slide(shape, slide_rid):
    """
    Adds a hyperlink to a specific slide for a given shape using lxml.
    """
    shape_xml = shape._element
    # Namespace map
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }

    nvSpPr = shape_xml.find('.//p:nvSpPr', namespaces=ns)
    cNvPr = nvSpPr.find('.//p:cNvPr', namespaces=ns)
    
    hlinkClick = cNvPr.find('.//a:hlinkClick', namespaces=ns)
    if hlinkClick is None:
        hlinkClick = etree.SubElement(cNvPr, '{%s}hlinkClick' % ns['a'])
    
    hlinkClick.set('action', 'ppaction://hlinksldjump')
    hlinkClick.set('{%s}id' % ns['r'], slide_rid)


def create_slide(
    output_pptx_path: str,
    theme1_keyword: str = "snow mountain",
    theme2_keyword: str = "desert dunes",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Interactive Split-Screen Morph Reveal effect.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        theme1_keyword: Keyword for Unsplash image search for the left theme.
        theme2_keyword: Keyword for Unsplash image search for the right theme.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    UNSPLASH_URL = "https://source.unsplash.com/1600x900/?"
    
    # --- Download Images ---
    try:
        response1 = requests.get(f"{UNSPLASH_URL}{theme1_keyword.replace(' ', '+')}")
        img1_io = BytesIO(response1.content)
    except requests.exceptions.RequestException:
        print(f"Warning: Could not download image for '{theme1_keyword}'.")
        img1_io = None

    try:
        response2 = requests.get(f"{UNSPLASH_URL}{theme2_keyword.replace(' ', '+')}")
        img2_io = BytesIO(response2.content)
    except requests.exceptions.RequestException:
        print(f"Warning: Could not download image for '{theme2_keyword}'.")
        img2_io = None

    # --- Create all slides and get their relationship IDs ---
    slides_info = []
    for _ in range(5):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slides_info.append({
            'slide': slide,
            'rId': prs.slides.part.rel_id_for(slide.part)
        })

    slide1, slide2, slide3, slide4, slide5 = [s['slide'] for s in slides_info]

    # --- Configure Transitions ---
    _set_transition(slide2, "morph")
    _set_transition(slide3, "push")
    _set_transition(slide4, "morph")
    _set_transition(slide5, "push")

    # --- Populate Slide 1: Main Menu ---
    if img1_io:
        pic1 = slide1.shapes.add_picture(img1_io, 0, 0, width=prs.slide_width, height=prs.slide_height)
        pic1.crop_right = 0.5
    if img2_io:
        pic2 = slide1.shapes.add_picture(img2_io, 0, 0, width=prs.slide_width, height=prs.slide_height)
        pic2.crop_left = 0.5

    tx_box1 = slide1.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(2))
    p1 = tx_box1.text_frame.add_paragraph()
    p1.text = theme1_keyword.upper()
    p1.font.name = 'Garamond'; p1.font.size = Pt(36); p1.font.color.rgb = RGBColor(0, 0, 0)
    
    tx_box2 = slide1.shapes.add_textbox(Inches(7.33), Inches(1), Inches(5), Inches(2))
    p2 = tx_box2.text_frame.add_paragraph()
    p2.text = theme2_keyword.upper()
    p2.font.name = 'Garamond'; p2.font.size = Pt(36); p2.font.color.rgb = RGBColor(0, 0, 0)

    btn1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.33), Inches(3.5), Inches(2), Inches(0.5))
    btn1.text_frame.text = "Explore"; btn1.fill.solid(); btn1.fill.fore_color.rgb = RGBColor(255, 255, 255); btn1.fill.transparency = 0.8
    btn1.line.color.rgb = RGBColor(0, 0, 0); btn1.line.width = Pt(1)
    _add_hyperlink_to_slide(btn1, slides_info[1]['rId'])

    btn2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9), Inches(3.5), Inches(2), Inches(0.5))
    btn2.text_frame.text = "Explore"; btn2.fill.solid(); btn2.fill.fore_color.rgb = RGBColor(255, 255, 255); btn2.fill.transparency = 0.8
    btn2.line.color.rgb = RGBColor(0, 0, 0); btn2.line.width = Pt(1)
    _add_hyperlink_to_slide(btn2, slides_info[3]['rId'])

    # --- Populate Slide 2: Theme 1 Full Screen (Morph Target) ---
    if img1_io:
        img1_io.seek(0)
        slide2.shapes.add_picture(img1_io, 0, 0, width=prs.slide_width, height=prs.slide_height)
    if img2_io:
        img2_io.seek(0)
        pic2_hidden = slide2.shapes.add_picture(img2_io, 0, 0, width=prs.slide_width, height=prs.slide_height)
        pic2_hidden.crop_left = 1.0

    # --- Populate Slide 4: Theme 2 Full Screen (Morph Target) ---
    if img1_io:
        img1_io.seek(0)
        pic1_hidden = slide4.shapes.add_picture(img1_io, 0, 0, width=prs.slide_width, height=prs.slide_height)
        pic1_hidden.crop_right = 1.0
    if img2_io:
        img2_io.seek(0)
        slide4.shapes.add_picture(img2_io, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Populate Detail Slides 3 & 5 ---
    slide3.background.fill.solid(); slide3.background.fill.fore_color.rgb = RGBColor(230, 230, 230)
    back_btn1 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.8), Inches(0.5), Inches(1), Inches(0.5))
    back_btn1.text_frame.text = "Back"; back_btn1.fill.solid(); back_btn1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    _add_hyperlink_to_slide(back_btn1, slides_info[0]['rId'])
    
    slide5.background.fill.solid(); slide5.background.fill.fore_color.rgb = RGBColor(210, 180, 140)
    back_btn2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.8), Inches(0.5), Inches(1), Inches(0.5))
    back_btn2.text_frame.text = "Back"; back_btn2.fill.solid(); back_btn2.fill.fore_color.rgb = RGBColor(255, 255, 255)
    _add_hyperlink_to_slide(back_btn2, slides_info[0]['rId'])
    
    prs.save(output_pptx_path)
    return output_pptx_path

