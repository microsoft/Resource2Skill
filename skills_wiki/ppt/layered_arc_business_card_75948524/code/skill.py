import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw
from lxml import etree

# Helper function for lxml shadow manipulation
def add_shadow_to_picture(picture):
    """Applies a soft outer shadow to a picture shape."""
    pic_element = picture._pic
    props = pic_element.get_or_add_spPr()
    effect_list = props.get_or_add_effectLst()

    # Define the outer shadow effect
    shadow_effect = etree.SubElement(effect_list, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
    shadow_effect.set('blurRad', '127000')  # Blur radius
    shadow_effect.set('dist', '45000')      # Distance
    shadow_effect.set('dir', '2700000')     # Direction (angle in 60,000ths of a degree)
    shadow_effect.set('algn', 'bl')         # Alignment
    shadow_effect.set('rotWithShape', '0')

    # Define shadow color and transparency
    color_elem = etree.SubElement(shadow_effect, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
    color_elem.set('val', '000000')
    alpha_elem = etree.SubElement(color_elem, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
    alpha_elem.set('val', '40000') # 40% opacity

def create_card_front_image(width, height, colors):
    """Generates the front of the business card as a PIL image."""
    img = Image.new('RGBA', (width, height), (245, 245, 245, 255))
    draw = ImageDraw.Draw(img)

    # Main blue shape
    arc_bbox = (width * 0.3, -height * 0.15, width * 1.1, height * 1.15)
    draw.pieslice(arc_bbox, start=88, end=272, fill=colors['dark_blue'])

    # Orange accent arc
    accent1_bbox = (width * 0.2, -height * 0.25, width * 1.2, height * 1.25)
    draw.pieslice(accent1_bbox, start=87, end=273, fill=colors['orange'])

    # Cyan accent arc
    accent2_bbox = (width * 0.25, -height * 0.2, width * 1.15, height * 1.2)
    draw.pieslice(accent2_bbox, start=88, end=272, fill=colors['cyan'])
    
    # Redraw main blue shape to hide inner parts of accents
    draw.pieslice(arc_bbox, start=88, end=272, fill=colors['dark_blue'])
    
    return img

def create_card_back_image(width, height, colors):
    """Generates the back of the business card as a PIL image."""
    img = Image.new('RGBA', (width, height), (245, 245, 245, 255))
    draw = ImageDraw.Draw(img)

    # Main blue shape on the left
    rect_width = int(width * 0.45)
    draw.rectangle([0, 0, rect_width, height], fill=colors['dark_blue'])

    # Arcs on the right side
    arc_bbox = (width * 0.4, -height * 0.15, width * 1.2, height * 1.15)
    # Orange accent arc
    accent1_bbox = (width * 0.3, -height * 0.25, width * 1.3, height * 1.25)
    draw.pieslice(accent1_bbox, start=87, end=273, fill=colors['orange'])
    
    # Cyan accent arc
    accent2_bbox = (width * 0.35, -height * 0.2, width * 1.25, height * 1.2)
    draw.pieslice(accent2_bbox, start=88, end=272, fill=colors['cyan'])
    
    # White overlay to create the clean edge
    draw.pieslice(arc_bbox, start=88, end=272, fill=(245, 245, 245, 255))
    
    return img
    
def create_slide(
    output_pptx_path: str,
    company_name: str = "COMPANY",
    slogan: str = "SLOGAN GOES HERE",
    name_surname: str = "NAME SURNAME",
    job_position: str = "JOB POSITION",
    email: str = "youremail@gmail.com",
    phone: str = "+123456789",
    location: str = "Your company location here",
    website: str = "www.websitename.com",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide showcasing the "Layered Arc Business Card" design.

    Returns: Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Define Colors and Dimensions ---
    colors = {
        'dark_blue': (1, 35, 87),
        'cyan': (0, 165, 222),
        'orange': (201, 114, 48),
        'white_text': RGBColor(255, 255, 255),
        'dark_text': RGBColor(70, 70, 70)
    }
    card_w_in, card_h_in = 3.5, 2
    img_w, img_h = 1050, 600 # High-res image for quality

    # --- Generate and Place Card Front ---
    front_img_pil = create_card_front_image(img_w, img_h, colors)
    front_img_path = "card_front.png"
    front_img_pil.save(front_img_path)
    
    pic_front = slide.shapes.add_picture(front_img_path, Inches(1.5), Inches(1.5), Inches(card_w_in * 1.5), Inches(card_h_in * 1.5))
    add_shadow_to_picture(pic_front)
    
    # Add text to front card
    # Company Name
    tb_company_front = slide.shapes.add_textbox(Inches(1.5 + 2.8), Inches(1.5 + 0.6), Inches(2), Inches(0.5))
    p = tb_company_front.text_frame.paragraphs[0]
    p.text = company_name
    p.font.name = 'Arial Black'
    p.font.size = Pt(16)
    p.font.color.rgb = colors['white_text']
    
    # Slogan
    tb_slogan_front = slide.shapes.add_textbox(Inches(1.5 + 2.8), Inches(1.5 + 0.95), Inches(2), Inches(0.4))
    p = tb_slogan_front.text_frame.paragraphs[0]
    p.text = slogan
    p.font.name = 'Calibri'
    p.font.size = Pt(8)
    p.font.color.rgb = colors['white_text']

    # --- Generate and Place Card Back ---
    back_img_pil = create_card_back_image(img_w, img_h, colors)
    back_img_path = "card_back.png"
    back_img_pil.save(back_img_path)
    
    pic_back = slide.shapes.add_picture(back_img_path, Inches(1.5), Inches(1.5 + card_h_in * 1.5 + 0.5), Inches(card_w_in * 1.5), Inches(card_h_in * 1.5))
    add_shadow_to_picture(pic_back)
    
    # Add text to back card
    # Left side (dark blue)
    left_margin = Inches(1.5 + 0.3)
    top_margin_back = Inches(1.5 + card_h_in * 1.5 + 0.5)
    
    # Name and Position
    tb_name = slide.shapes.add_textbox(left_margin, top_margin_back + Inches(0.4), Inches(2), Inches(0.4))
    p = tb_name.text_frame.paragraphs[0]
    p.text = name_surname.upper()
    p.font.bold = True
    p.font.name = 'Arial'
    p.font.size = Pt(12)
    p.font.color.rgb = colors['white_text']
    
    tb_pos = slide.shapes.add_textbox(left_margin, top_margin_back + Inches(0.7), Inches(2), Inches(0.3))
    p = tb_pos.text_frame.paragraphs[0]
    p.text = job_position
    p.font.name = 'Calibri'
    p.font.size = Pt(8)
    p.font.color.rgb = colors['white_text']

    # Contact Details with Icons
    contact_info = [
        (phone, "📞"), (email, "📧"), (location, "📍"), (website, "🌐")
    ]
    current_y = top_margin_back + Inches(1.2)
    icon_left = left_margin - Inches(0.1)
    text_left = icon_left + Inches(0.3)
    
    for text, icon in contact_info:
        # Icon
        tb_icon = slide.shapes.add_textbox(icon_left, current_y, Inches(0.25), Inches(0.25))
        p = tb_icon.text_frame.paragraphs[0]
        p.text = icon
        p.font.name = 'Segoe UI Symbol'
        p.font.size = Pt(10)
        p.font.color.rgb = colors['white_text']
        
        # Text
        tb_text = slide.shapes.add_textbox(text_left, current_y, Inches(1.8), Inches(0.25))
        p = tb_text.text_frame.paragraphs[0]
        p.text = text
        p.font.name = 'Calibri'
        p.font.size = Pt(8)
        p.font.color.rgb = colors['white_text']
        current_y += Inches(0.35)

    # Right side (white)
    right_margin = Inches(1.5 + 2.8)
    # LOGO Circle
    logo_shape = slide.shapes.add_shape(1, right_margin + Inches(0.8), top_margin_back + Inches(0.6), Inches(0.8), Inches(0.8))
    logo_shape.text = "LOGO"
    logo_shape.text_frame.paragraphs[0].font.color.rgb = colors['dark_text']
    logo_shape.text_frame.paragraphs[0].font.size = Pt(10)
    logo_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    logo_shape.fill.background()
    logo_shape.line.color.rgb = colors['dark_text']
    logo_shape.line.width = Pt(1)

    # Company & Slogan
    tb_company_back = slide.shapes.add_textbox(right_margin, top_margin_back + Inches(1.5), Inches(2), Inches(0.5))
    p = tb_company_back.text_frame.paragraphs[0]
    p.text = company_name
    p.font.name = 'Arial Black'
    p.font.size = Pt(14)
    p.font.color.rgb = colors['dark_text']

    tb_slogan_back = slide.shapes.add_textbox(right_margin, top_margin_back + Inches(1.8), Inches(2), Inches(0.4))
    p = tb_slogan_back.text_frame.paragraphs[0]
    p.text = slogan
    p.font.name = 'Calibri'
    p.font.size = Pt(8)
    p.font.color.rgb = colors['dark_text']

    # Clean up generated image files
    os.remove(front_img_path)
    os.remove(back_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
# create_slide("business_card_output.pptx")

