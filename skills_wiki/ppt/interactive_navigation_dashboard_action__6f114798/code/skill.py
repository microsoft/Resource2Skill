import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def _add_interactive_button(slide, text, left, top, width, height, target_slide, bg_color):
    """Helper function to create a styled button with an action link and drop shadow."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.text = text
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*bg_color)
    shape.line.color.rgb = RGBColor(255, 255, 255)
    shape.line.width = Pt(1.5)
    
    # Style the text inside the button
    for paragraph in shape.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.font.name = "Segoe UI"
        paragraph.font.size = Pt(20)
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(255, 255, 255)
        
    # The Core Skill: Map the shape to hyperlink to another slide
    if target_slide:
        shape.click_action.target_slide = target_slide
        
    # LXML Injection: Add a drop shadow to make it feel "clickable"
    try:
        from pptx.oxml.ns import qn
        from lxml import etree
        spPr = shape.element.spPr
        effectLst = spPr.find(qn('a:effectLst'))
        if effectLst is None:
            effectLst = etree.SubElement(spPr, qn('a:effectLst'))
        
        outerShdw = etree.SubElement(effectLst, qn('a:outerShdw'))
        outerShdw.set('blurRad', '150000') # 15 pt blur
        outerShdw.set('dist', '40000')     # 4 pt distance
        outerShdw.set('dir', '5400000')    # 90 degrees straight down
        outerShdw.set('algn', 'tl')
        outerShdw.set('rotWithShape', '0')
        
        srgbClr = etree.SubElement(outerShdw, qn('a:srgbClr'))
        srgbClr.set('val', '000000')
        alpha = etree.SubElement(srgbClr, qn('a:alpha'))
        alpha.set('val', '35000') # 35% opacity shadow
    except Exception:
        pass # Graceful fallback if lxml manipulation fails
        
    return shape

def create_slide(
    output_pptx_path: str,
    title_text: str = "Interactive Dashboard",
    body_text: str = "Select a module to navigate directly to its content.",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Interactive Navigation Dashboard effect.
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Create 4 slides total (1 Dashboard Hub, 3 Content Spokes)
    slide_dash = prs.slides.add_slide(prs.slide_layouts[6])
    slide_1 = prs.slides.add_slide(prs.slide_layouts[6])
    slide_2 = prs.slides.add_slide(prs.slide_layouts[6])
    slide_3 = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Generate & Apply Background to all slides ===
    bg_path = "temp_dashboard_bg.png"
    img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(img)
    color_top = (15, 20, 30)
    color_bottom = (30, 40, 50)
    for y in range(1080):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * y / 1080)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * y / 1080)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * y / 1080)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    img.save(bg_path)
    
    for slide in prs.slides:
        slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Dashboard Title & Subtitle ===
    tb = slide_dash.shapes.add_textbox(Inches(1), Inches(1.2), Inches(11.333), Inches(1))
    tf = tb.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Segoe UI"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    tb_sub = slide_dash.shapes.add_textbox(Inches(1), Inches(2.2), Inches(11.333), Inches(0.5))
    tf_sub = tb_sub.text_frame
    tf_sub.text = body_text
    p_sub = tf_sub.paragraphs[0]
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(180, 190, 200)

    # === Layer 3: Interactive Forward Navigation Buttons ===
    btn_width = Inches(2.8)
    btn_height = Inches(1.4)
    gap = Inches(1.23)
    top_pos = Inches(4)
    
    # Add buttons and link them to their respective slides
    _add_interactive_button(slide_dash, "Data Analytics", gap, top_pos, btn_width, btn_height, slide_1, accent_color)
    _add_interactive_button(slide_dash, "Market Strategy", gap + btn_width + gap, top_pos, btn_width, btn_height, slide_2, (255, 105, 180)) # Hot Pink
    _add_interactive_button(slide_dash, "Financial Projections", gap + 2*btn_width + 2*gap, top_pos, btn_width, btn_height, slide_3, (50, 205, 50)) # Lime Green

    # === Layer 4: Setup Content Slides with Return Navigation ===
    content_titles = ["Data Analytics Module", "Market Strategy Module", "Financial Projections Module"]
    
    for i, (slide_content, title) in enumerate(zip([slide_1, slide_2, slide_3], content_titles)):
        # Title
        tb = slide_content.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(1))
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(40)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Simulated content area (glassmorphic placeholder)
        shape = slide_content.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(2.5), Inches(11.333), Inches(4))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.fill.transparency = 0.93 # 93% transparent
        shape.line.color.rgb = RGBColor(255, 255, 255)
        shape.line.transparency = 0.5
        
        # The Utility Return Button (Top Right Corner)
        _add_interactive_button(slide_content, "⟵ Back to Dashboard", Inches(10), Inches(1), Inches(2.333), Inches(0.6), slide_dash, (60, 70, 80))

    # Clean up temp files
    if os.path.exists(bg_path):
        os.remove(bg_path)

    prs.save(output_pptx_path)
    return output_pptx_path
