def create_slide(
    output_pptx_path: str,
    title_text: str = "Cinematic Spotlight",
    body_text: str = "",
    bg_palette: str = "team",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Cinematic Spotlight Reveal' visual effect.
    """
    import os
    import io
    import requests
    from PIL import Image, ImageEnhance, ImageDraw
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import qn

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    W = prs.slide_width
    H = prs.slide_height

    # === Fetch & Process Assets ===
    img_color_path = "_temp_color.jpg"
    img_gray_path = "_temp_gray.jpg"
    
    # Attempt to fetch a real image from Unsplash (16:9 crop)
    try:
        url = "https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&h=900&q=80"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        img_color = Image.open(io.BytesIO(resp.content)).convert("RGB")
    except Exception:
        # Fallback: Generate a geometric dummy image simulating a group shot
        img_color = Image.new('RGB', (1600, 900), (30, 40, 50))
        draw = ImageDraw.Draw(img_color)
        for x in range(0, 1600, 100):
            draw.line([(x, 0), (x, 900)], fill=(40, 50, 60), width=4)
        for y in range(0, 900, 100):
            draw.line([(0, y), (1600, y)], fill=(40, 50, 60), width=4)
        # Draw "subjects"
        draw.ellipse((int(1600*0.2 - 200), int(900*0.5 - 200), int(1600*0.2 + 200), int(900*0.5 + 200)), fill=(200, 80, 80))
        draw.ellipse((int(1600*0.5 - 200), int(900*0.5 - 200), int(1600*0.5 + 200), int(900*0.5 + 200)), fill=(80, 200, 80))
        draw.ellipse((int(1600*0.8 - 200), int(900*0.5 - 200), int(1600*0.8 + 200), int(900*0.5 + 200)), fill=(80, 80, 200))

    img_color.save(img_color_path)

    # Create desaturated & dimmed background
    enhancer_color = ImageEnhance.Color(img_color)
    img_gray = enhancer_color.enhance(0.0)
    enhancer_brightness = ImageEnhance.Brightness(img_gray)
    img_gray = enhancer_brightness.enhance(0.35) # Darken to make spotlight pop
    img_gray.save(img_gray_path)

    # === Helper to Add Spotlight Slides ===
    def add_spotlight_slide(cx, cy, r, subject_title, subject_desc, align="left"):
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # 1. Background Layer
        bg = slide.shapes.add_picture(img_gray_path, 0, 0, W, H)
        bg.element.nvPicPr.cNvPr.set("name", "!!Background")

        # 2. Spotlight Layer (Calculate exact crop offsets to prevent stretching)
        crop_left = (cx - r) / W
        crop_right = (W - (cx + r)) / W
        crop_top = (cy - r) / H
        crop_bottom = (H - (cy + r)) / H

        pic_left = int(W * crop_left)
        pic_top = int(H * crop_top)
        pic_width = int(W * (1 - crop_left - crop_right))
        pic_height = int(H * (1 - crop_top - crop_bottom))

        pic = slide.shapes.add_picture(img_color_path, pic_left, pic_top, pic_width, pic_height)
        pic.crop_left = float(crop_left)
        pic.crop_right = float(crop_right)
        pic.crop_top = float(crop_top)
        pic.crop_bottom = float(crop_bottom)

        # Force Morph match name and change geometry to Ellipse
        pic.element.nvPicPr.cNvPr.set("name", "!!Spotlight")
        prstGeom = pic.element.spPr.find(qn('a:prstGeom'))
        if prstGeom is not None:
            prstGeom.set('prst', 'ellipse')

        # 3. Floating Typography
        if align == "left":
            tx_left, tx_align = cx - r - Inches(3), PP_ALIGN.RIGHT
        else:
            tx_left, tx_align = cx + r + Inches(0.5), PP_ALIGN.LEFT

        tx_top = cy - Inches(0.5)
        txBox = slide.shapes.add_textbox(tx_left, tx_top, Inches(2.5), Inches(1.5))
        txBox.element.nvSpPr.cNvPr.set("name", "!!TextBox") # Enables text box glide

        tf = txBox.text_frame
        p = tf.add_paragraph()
        p.text = subject_title
        p.font.bold = True
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(*accent_color)
        p.alignment = tx_align

        p2 = tf.add_paragraph()
        p2.text = subject_desc
        p2.font.size = Pt(16)
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.alignment = tx_align

        # 4. Inject Morph Transition (p14 namespace required for Morph)
        morph_xml = '''
        <p:transition spd="slow" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">
            <p14:morph option="byObject"/>
        </p:transition>
        '''
        slide.element.append(parse_xml(morph_xml))
        
        return slide

    # === Construct Sequence ===
    radius = Inches(1.8)
    
    # Slide 1: Focus Left
    add_spotlight_slide(Inches(2.6), Inches(3.75), radius, "Maria Cruise", "Marketing Manager", align="right")
    
    # Slide 2: Focus Center
    add_spotlight_slide(Inches(6.6), Inches(3.75), radius, "Sara Karni", "Marketing Operations", align="left")
    
    # Slide 3: Focus Right
    add_spotlight_slide(Inches(10.6), Inches(3.75), radius, "Rob West", "Marketing Expert", align="left")

    # Cleanup temp files
    if os.path.exists(img_color_path): os.remove(img_color_path)
    if os.path.exists(img_gray_path): os.remove(img_gray_path)

    prs.save(output_pptx_path)
    return output_pptx_path
