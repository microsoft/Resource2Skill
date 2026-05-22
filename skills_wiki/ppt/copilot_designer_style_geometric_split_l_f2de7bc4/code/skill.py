def create_slide(
    output_pptx_path: str,
    title_text: str = "Onboard Experience",
    body_text: str = (
        "Enjoy comfortable seating and plenty of legroom on all flights\n"
        "In-flight entertainment includes movies, TV shows, and music, all available on demand\n"
        "Food and beverage options include snacks, meals, and a selection of beer, wine, and spirits"
    ),
    bg_palette: str = "airplane,interior",
    accent_color: tuple = (54, 53, 153),  # Deep Indigo
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Copilot Designer-Style Geometric Split Layout.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from io import BytesIO
    from PIL import Image, ImageDraw
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # --- helper: download and create circular alpha masked image ---
    def make_circle_image(keyword, size=800):
        img_url = f"https://source.unsplash.com/featured/{size}x{size}/?{keyword}"
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                img = Image.open(BytesIO(response.read())).convert("RGBA")
        except Exception:
            # Fallback to a solid gray image if download fails
            img = Image.new("RGBA", (size, size), (220, 220, 225, 255))
            
        # Crop to square just in case
        min_dim = min(img.width, img.height)
        left = (img.width - min_dim) / 2
        top = (img.height - min_dim) / 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((10, 10, size-10, size-10), fill=255)  # slight padding for anti-aliasing
        
        # Apply mask
        result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        result.paste(img, (0, 0), mask=mask)
        return result

    # 1. Add background accent circle (offset)
    offset_x, offset_y = 1.0, 1.2
    circle_size = 5.0
    bg_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(offset_x), Inches(offset_y), Inches(circle_size), Inches(circle_size)
    )
    bg_circle.fill.solid()
    bg_circle.fill.fore_color.rgb = RGBColor(*accent_color)
    bg_circle.line.fill.background() # No border

    # 2. Generate and insert masked photo
    img_pil = make_circle_image(bg_palette)
    img_path = "temp_circle_hero.png"
    img_pil.save(img_path, format="PNG")
    
    img_x, img_y = 1.6, 1.4 # Shifted slightly right and down to reveal the accent circle
    img_w_h = 4.6
    slide.shapes.add_picture(img_path, Inches(img_x), Inches(img_y), Inches(img_w_h), Inches(img_w_h))
    
    if os.path.exists(img_path):
        os.remove(img_path)

    # 3. Add Geometric Accents (Designer style)
    # 3a. Small hollow circle accent
    ring = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(offset_x - 0.2), Inches(offset_y + 3.0), Inches(0.6), Inches(0.6)
    )
    ring.fill.background()
    ring.line.color.rgb = RGBColor(*accent_color)
    ring.line.width = Pt(3)

    # 3b. Helper function to draw a minimal geometric plus sign
    def add_plus(cx, cy, size, color):
        thickness = 0.04
        # Horizontal line
        h_line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            Inches(cx - size/2), Inches(cy - thickness/2), Inches(size), Inches(thickness)
        )
        # Vertical line
        v_line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            Inches(cx - thickness/2), Inches(cy - size/2), Inches(thickness), Inches(size)
        )
        for shp in (h_line, v_line):
            shp.fill.solid()
            shp.fill.fore_color.rgb = RGBColor(*color)
            shp.line.fill.background() # No line
            
    # Add a couple of plus signs floating around
    add_plus(img_x + img_w_h + 0.2, img_y + 0.5, 0.25, accent_color)
    add_plus(offset_x + 1.0, offset_y - 0.3, 0.15, (100, 150, 200))

    # 4. Add Text Content
    # Title
    title_box = slide.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.name = "Calibri"
    p.font.color.rgb = RGBColor(30, 30, 30)

    # Body (Bulleted List)
    body_box = slide.shapes.add_textbox(Inches(7.0), Inches(3.0), Inches(5.5), Inches(4.0))
    bf = body_box.text_frame
    bf.word_wrap = True
    
    bullets = [line.strip('-* ') for line in body_text.strip().split('\n') if line.strip()]
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = bf.paragraphs[0]
        else:
            p = bf.add_paragraph()
        p.text = bullet
        p.font.size = Pt(20)
        p.font.name = "Calibri"
        p.font.color.rgb = RGBColor(70, 70, 70)
        p.space_after = Pt(20)
        p.level = 0 # Applies standard bullet formatting

    prs.save(output_pptx_path)
    return output_pptx_path
