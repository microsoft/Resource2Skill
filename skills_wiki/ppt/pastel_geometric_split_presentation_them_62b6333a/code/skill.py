def create_slide(
    output_pptx_path: str,
    title_line1: str = "SALES",
    title_line2: str = "Review",
    title_line3: str = "Analysis",
    subtitle_text: str = "Your Company Name",
    image_query: str = "business analytics chart",
) -> str:
    """
    Creates a PPTX slide reproducing the 'Pastel Geometric Split' title layout.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw
    import urllib.request
    from io import BytesIO
    import os

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Palette
    color_cyan = RGBColor(226, 240, 249)
    color_pink = RGBColor(248, 227, 228)
    color_text = RGBColor(20, 20, 20)

    # 2. Add Background Accent Arc (Large Cyan Circle on the left)
    # Positioning off-canvas to create a large curved background effect
    arc_left = Inches(-2.5)
    arc_top = Inches(-1.5)
    arc_size = Inches(9.0)
    
    bg_arc = slide.shapes.add_shape(
        9,  # MSO_SHAPE.OVAL
        arc_left, arc_top, arc_size, arc_size
    )
    bg_arc.fill.solid()
    bg_arc.fill.fore_color.rgb = color_cyan
    bg_arc.line.fill.background() # No line

    # 3. Fetch and process circular image using PIL
    image_path = "temp_circle_img.png"
    try:
        # Fetch image
        url = f"https://source.unsplash.com/featured/?{urllib.parse.quote(image_query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        img = Image.open(BytesIO(response.read())).convert("RGBA")
        
        # Crop to square first to avoid squashing
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        img = img.crop((left, top, right, bottom))
        
        # Create circular mask and apply
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        
        # Antialiasing blur on mask edges for clean look
        circle_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
        circle_img.paste(img, (0, 0), mask)
        circle_img.save(image_path, "PNG")
        
    except Exception as e:
        # Fallback if download fails: Draw a solid circle
        img = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 800, 800), fill=(100, 150, 200, 255))
        img.save(image_path, "PNG")

    # Insert circular image into slide
    img_left = Inches(1.0)
    img_top = Inches(1.2)
    img_size = Inches(5.0)
    slide.shapes.add_picture(image_path, img_left, img_top, width=img_size, height=img_size)
    
    # Cleanup temp image
    if os.path.exists(image_path):
        os.remove(image_path)

    # 4. Add Multi-tiered Main Typography
    text_box_left = Inches(7.5)
    text_box_top = Inches(1.5)
    text_box_width = Inches(5.5)
    text_box_height = Inches(3.5)
    
    text_box = slide.shapes.add_textbox(text_box_left, text_box_top, text_box_width, text_box_height)
    tf = text_box.text_frame
    tf.word_wrap = True

    # Line 1 (Huge, Bold)
    p1 = tf.paragraphs[0]
    p1.text = title_line1.upper()
    p1.font.size = Pt(64)
    p1.font.bold = True
    p1.font.name = "Calibri"
    p1.font.color.rgb = color_text

    # Line 2 (Medium, Bold)
    p2 = tf.add_paragraph()
    p2.text = title_line2
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.name = "Calibri"
    p2.font.color.rgb = color_text

    # Line 3 (Huge, Bold)
    p3 = tf.add_paragraph()
    p3.text = title_line3.capitalize()
    p3.font.size = Pt(60)
    p3.font.bold = True
    p3.font.name = "Calibri"
    p3.font.color.rgb = color_text

    # 5. Add Pink Accent Block
    # Positioned at bottom right, bleeding off edge
    banner_left = Inches(7.2)
    banner_top = Inches(5.6)
    banner_width = Inches(6.5) # Extends past edge (13.333 total width)
    banner_height = Inches(1.2)
    
    banner = slide.shapes.add_shape(
        1,  # MSO_SHAPE.RECTANGLE
        banner_left, banner_top, banner_width, banner_height
    )
    banner.fill.solid()
    banner.fill.fore_color.rgb = color_pink
    banner.line.fill.background()

    # 6. Add Subtitle / Company Name inside the banner
    sub_box = slide.shapes.add_textbox(banner_left + Inches(0.3), banner_top + Inches(0.3), Inches(5.0), Inches(0.6))
    sub_tf = sub_box.text_frame
    sub_p = sub_tf.paragraphs[0]
    sub_p.text = subtitle_text
    sub_p.font.size = Pt(20)
    sub_p.font.name = "Calibri"
    sub_p.font.color.rgb = color_text

    # Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path
