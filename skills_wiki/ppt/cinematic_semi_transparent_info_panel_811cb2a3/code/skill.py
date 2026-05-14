def create_slide(
    output_pptx_path: str,
    title_text: str = "1. SITE INFORMATION",
    body_text: str = "local climate\nprevailing winds\nsolar aspect\nvegetation\nbuilding context",
    bg_palette: str = "architecture",
    accent_color: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Cinematic Semi-Transparent Info Panel' 
    architectural presentation style.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.xmlchemy import OxmlElement
    from PIL import Image

    # Initialize 16:9 Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Background Image ===
    img_path = "temp_architectural_bg.jpg"
    try:
        # Fetch a high-quality contextual image
        req = urllib.request.Request(
            f"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1920&h=1080&fit=crop", 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback to a solid dark slate if network fails
        img = Image.new('RGB', (1920, 1080), color=(40, 45, 50))
        img.save(img_path)

    # Insert full bleed
    slide.shapes.add_picture(img_path, 0, 0, width=Inches(13.333), height=Inches(7.5))

    # === Layer 2: Semi-Transparent Matte Panel ===
    # Positioned flush left
    matte = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        0, Inches(1.2), Inches(5.5), Inches(5.8)
    )
    matte.line.fill.background()  # Remove border
    
    # XML Injection to achieve 65% transparency on a black fill
    matte.fill.solid()
    matte.fill.fore_color.rgb = RGBColor(10, 10, 10) 
    
    spPr = matte.element.spPr
    solidFill = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
    if solidFill is not None:
        srgbClr = solidFill.find('{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        if srgbClr is not None:
            alpha = OxmlElement('a:alpha')
            alpha.set('val', '65000')  # 65000 / 100000 = 65% Opacity
            srgbClr.append(alpha)

    # === Layer 3: Typography & Content ===
    
    # 3a. Bordered Title Box
    header_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.6), Inches(1.8), Inches(4.3), Inches(0.8)
    )
    header_box.fill.background()  # Transparent inside
    header_box.line.color.rgb = RGBColor(255, 255, 255)
    header_box.line.width = Pt(1.5)
    
    tf_header = header_box.text_frame
    tf_header.text = title_text
    # Internal padding to let the text breathe away from the border
    tf_header.margin_left = Inches(0.2)
    tf_header.margin_top = Inches(0.15)
    
    p_header = tf_header.paragraphs[0]
    p_header.font.name = "Arial"
    p_header.font.size = Pt(22)
    p_header.font.color.rgb = RGBColor(255, 255, 255)
    p_header.font.bold = True
    p_header.alignment = PP_ALIGN.LEFT

    # 3b. Subheading Text
    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.75), Inches(4.3), Inches(0.4))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "PROJECT INVENTORY"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = RGBColor(180, 180, 180)
    p_sub.font.bold = True

    # 3c. Architectural "+" Bullet List
    list_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.2), Inches(4.5), Inches(3.5))
    tf_list = list_box.text_frame
    tf_list.word_wrap = True

    items = body_text.split('\n')
    for i, item in enumerate(items):
        if not item.strip():
            continue
        p_list = tf_list.paragraphs[0] if i == 0 else tf_list.add_paragraph()
        # Using the stylistic "+" instead of standard bullet dots
        p_list.text = f"+  {item.strip()}"
        p_list.font.name = "Arial"
        p_list.font.size = Pt(18)
        p_list.font.color.rgb = RGBColor(255, 255, 255)
        p_list.space_after = Pt(10)  # Add breathing room between list items

    # Cleanup and Save
    prs.save(output_pptx_path)
    
    if os.path.exists(img_path):
        os.remove(img_path)
        
    return output_pptx_path
