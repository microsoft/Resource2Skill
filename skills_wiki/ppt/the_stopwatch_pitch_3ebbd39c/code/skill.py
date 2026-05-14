import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

def add_shadow_to_shape(shape):
    """
    Adds a soft outer shadow effect to a shape using lxml to manipulate the OOXML.
    """
    sp = shape.element
    spPr = sp.get_or_add_spPr()
    
    # Create <a:effectLst>
    effect_lst = etree.SubElement(spPr, qn('a:effectLst'))
    
    # Create <a:outerShdw> with attributes
    shadow_attrs = {
        'blurRad': '101600',  # 10 pt blur
        'dist': '45720',      # 5 pt distance
        'dir': '2700000',     # 45 degrees (2700000 / 60000)
        'algn': 'ctr',
        'rotWithShape': '0'
    }
    outer_shadow = etree.SubElement(effect_lst, qn('a:outerShdw'), **shadow_attrs)
    
    # Create <a:srgbClr> for shadow color
    srgb_clr = etree.SubElement(outer_shadow, qn('a:srgbClr'), val="000000")
    
    # Create <a:alpha> for transparency (40%)
    etree.SubElement(srgb_clr, qn('a:alpha'), val="40000")


def create_slide(
    output_pptx_path: str,
    title_text: str = "In a world of opportunity, success is temporary. So is failure.",
    subtitle_text: str = "THE 20-SECOND PITCH",
    bg_color: tuple = (40, 40, 40),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing 'The Stopwatch Pitch' visual effect.

    This design uses a minimalist, high-contrast style with a stopwatch graphic
    to frame a powerful, concise message, conveying urgency and precision.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Stopwatch Graphic ===
    # Main body
    body_left = Inches(1.5)
    body_top = Inches(2.25)
    body_width = Inches(4.5)
    body_height = Inches(4.5)
    body = slide.shapes.add_shape(MSO_SHAPE.OVAL, body_left, body_top, body_width, body_height)
    body.fill.solid()
    body.fill.fore_color.rgb = RGBColor(128, 128, 128)
    body.line.fill.background() # No outline

    # Add shadow to the main body using lxml
    add_shadow_to_shape(body)
    
    # Face
    face_left = body_left + Inches(0.25)
    face_top = body_top + Inches(0.25)
    face_width = body_width - Inches(0.5)
    face_height = body_height - Inches(0.5)
    face = slide.shapes.add_shape(MSO_SHAPE.OVAL, face_left, face_top, face_width, face_height)
    face.fill.solid()
    face.fill.fore_color.rgb = RGBColor(245, 245, 245)
    face.line.fill.background()

    # Top Buttons
    btn_width = Inches(0.8)
    btn_height = Inches(0.4)
    main_btn_left = body_left + (body_width / 2) - (btn_width / 2)
    main_btn_top = body_top - Inches(0.2)
    main_btn = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, main_btn_left, main_btn_top, btn_width, btn_height)
    main_btn.fill.solid()
    main_btn.fill.fore_color.rgb = RGBColor(128, 128, 128)
    main_btn.line.fill.background()

    # Timer display
    timer_box = slide.shapes.add_textbox(face_left, face_top + Inches(1.5), face_width, Inches(1))
    timer_p = timer_box.text_frame.paragraphs[0]
    timer_p.text = "00:20"
    timer_p.font.name = "Arial Black"
    timer_p.font.size = Pt(48)
    timer_p.font.color.rgb = RGBColor(40, 40, 40)
    timer_p.alignment = PP_ALIGN.CENTER
    
    # === Layer 3: Text & Content ===
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(7.5), Inches(2.5), Inches(7), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.clear()
    subtitle_p = subtitle_frame.paragraphs[0]
    subtitle_p.text = subtitle_text
    subtitle_p.font.name = "Arial"
    subtitle_p.font.bold = True
    subtitle_p.font.size = Pt(24)
    subtitle_p.font.color.rgb = RGBColor(180, 180, 180)

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(7.5), Inches(3.2), Inches(7.5), Inches(3))
    title_frame = title_box.text_frame
    title_frame.clear()
    title_frame.word_wrap = True
    title_p = title_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.name = "Arial Black"
    title_p.font.size = Pt(40)
    title_p.font.color.rgb = RGBColor(255, 255, 255)
    title_p.line_spacing = 1.2
    
    if not os.path.exists(os.path.dirname(output_pptx_path)) and os.path.dirname(output_pptx_path):
        os.makedirs(os.path.dirname(output_pptx_path))

    prs.save(output_pptx_path)
    return output_pptx_path

