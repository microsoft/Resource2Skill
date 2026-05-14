import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from lxml import etree
from PIL import Image

def set_shape_transparency(shape, alpha_percent: int):
    """
    Injects transparency into a shape's solid fill using lxml.
    alpha_percent: 0 (fully transparent) to 100 (fully opaque)
    """
    # Convert percentage to OOXML alpha value (0 to 100000)
    # Note: OOXML uses 'alpha' as opacity. 70% opacity = 70000.
    alpha_val = str(int(alpha_percent * 1000))
    
    # Locate the srgbClr element in the shape's XML tree
    srgbClr_elements = shape.element.xpath('.//a:srgbClr')
    if srgbClr_elements:
        srgbClr = srgbClr_elements[0]
        # Remove any existing alpha tags to prevent duplicates
        for existing_alpha in srgbClr.xpath('.//a:alpha'):
            srgbClr.remove(existing_alpha)
            
        # Create and append the new alpha element
        alpha_element = etree.Element("{http://schemas.openxmlformats.org/drawingml/2006/main}alpha", val=alpha_val)
        srgbClr.append(alpha_element)

def create_slide(
    output_pptx_path: str = "Consulting_Style_Deck.pptx",
    deck_title: str = "Market Analysis & Strategy",
    deck_subtitle: str = "Q4 Performance Review",
    accent_color: tuple = (237, 125, 49),  # Vibrant Orange
    dark_text: tuple = (64, 64, 64),
    bg_keyword: str = "cityscape"
) -> str:
    """
    Generates a PPTX featuring a modern Hero cover with transparent mask,
    and a strictly formatted consulting-style content slide.
    """
    prs = Presentation()
    # Set to 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    
    # Define Theme Colors
    COLOR_ACCENT = RGBColor(*accent_color)
    COLOR_TEXT = RGBColor(*dark_text)
    COLOR_HEADER_BG = RGBColor(242, 242, 242)
    COLOR_WHITE = RGBColor(255, 255, 255)

    # ==========================================
    # SLIDE 1: "Apple/Modern" Hero Cover Slide
    # ==========================================
    slide_cover = prs.slides.add_slide(blank_layout)
    
    # 1. Fetch and process background image
    bg_img_path = "temp_bg.jpg"
    try:
        # Using a reliable placeholder service
        url = f"https://picsum.photos/seed/{bg_keyword}/1920/1080"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read()))
            img = img.convert("RGB")
            img.save(bg_img_path)
    except Exception as e:
        print(f"Image download failed, generating fallback. Error: {e}")
        img = Image.new('RGB', (1920, 1080), color=(40, 50, 60))
        img.save(bg_img_path)

    # Insert Full-bleed background
    slide_cover.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 2. Add Semi-Transparent Overlay Mask (The "Skill" element)
    # Covering the left 50% of the slide
    mask_width = prs.slide_width / 2.2
    overlay = slide_cover.shapes.add_shape(
        1,  # 1 = msoShapeRectangle
        0, 0, width=mask_width, height=prs.slide_height
    )
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = COLOR_WHITE
    overlay.line.fill.background()  # No outline
    
    # Apply 85% Opacity (15% transparency) via lxml XML injection
    set_shape_transparency(overlay, 85)

    # 3. Add Cover Typography
    title_box = slide_cover.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(5), Inches(2))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p = tf.add_paragraph()
    p.text = deck_title
    p.font.name = 'Arial'
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    
    p2 = tf.add_paragraph()
    p2.text = deck_subtitle
    p2.font.name = 'Arial'
    p2.font.size = Pt(20)
    p2.font.color.rgb = COLOR_ACCENT

    # ==========================================
    # SLIDE 2: "Bain/Consulting" Content Slide
    # ==========================================
    slide_content = prs.slides.add_slide(blank_layout)

    # 1. Consistent Header Bar
    header_h = Inches(1.2)
    header_bg = slide_content.shapes.add_shape(1, 0, 0, width=prs.slide_width, height=header_h)
    header_bg.fill.solid()
    header_bg.fill.fore_color.rgb = COLOR_HEADER_BG
    header_bg.line.fill.background()
    
    # 2. Accent Line (The Anchor)
    accent_line = slide_content.shapes.add_shape(
        1, 0, header_h, width=prs.slide_width, height=Pt(3)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = COLOR_ACCENT
    accent_line.line.fill.background()

    # 3. Header Text
    header_txt = slide_content.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.8))
    htf = header_txt.text_frame
    htf.vertical_anchor = MSO_ANCHOR.MIDDLE
    hp = htf.paragraphs[0]
    hp.text = "Executive Summary: Key Performance Indicators"
    hp.font.name = 'Arial'
    hp.font.size = Pt(28)
    hp.font.bold = True
    hp.font.color.rgb = COLOR_TEXT

    # 4. Content Area Layout (Mocking structured consulting data)
    col_width = Inches(3.8)
    for i in range(3):
        left_pos = Inches(0.8) + (i * (col_width + Inches(0.3)))
        
        # Section Title
        box = slide_content.shapes.add_textbox(left_pos, Inches(1.8), col_width, Inches(0.5))
        p = box.text_frame.paragraphs[0]
        p.text = f"Strategic Pillar {i+1}"
        p.font.name = 'Arial'
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        
        # Flat element / mock chart container
        chart_box = slide_content.shapes.add_shape(1, left_pos, Inches(2.4), col_width, Inches(2))
        chart_box.fill.solid()
        chart_box.fill.fore_color.rgb = RGBColor(230, 230, 230)
        chart_box.line.fill.background()
        
        # Body bullet points
        body = slide_content.shapes.add_textbox(left_pos, Inches(4.6), col_width, Inches(2))
        btf = body.text_frame
        btf.word_wrap = True
        bp = btf.paragraphs[0]
        bp.text = "• Consistent formatting eliminates noise."
        bp.font.size = Pt(14)
        bp.font.name = 'Arial'
        bp.font.color.rgb = COLOR_TEXT
        
        bp2 = btf.add_paragraph()
        bp2.text = "• 2D elements prevent visual fatigue."
        bp2.font.size = Pt(14)
        bp2.font.name = 'Arial'
        bp2.font.color.rgb = COLOR_TEXT

    # Save and cleanup
    prs.save(output_pptx_path)
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path

if __name__ == "__main__":
    create_slide()
