def create_slide(
    output_pptx_path: str,
    title_text: str = "workflow",
    body_text: str = "the way that a particular type of work is organized, or the order of the stages in a particular work process",
    bg_palette: str = "architecture",  
    accent_color: tuple = (255, 204, 0),  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Architectural Blueprint & Typographic Grid effect.
    """
    import os
    import random
    import urllib.request
    import io
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.oxml.xmlchemy import OxmlElement

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # === Layer 1: Procedural Paper & Grid via PIL ===
    width, height = 1920, 1080
    bg = Image.new('RGB', (width, height), (242, 242, 238))
    
    # 1a. Simulate Paper Texture with Noise
    pixels = bg.load()
    for _ in range(250000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        r, g, b = pixels[x, y]
        noise = random.randint(-15, 5)
        pixels[x, y] = (max(0, r+noise), max(0, g+noise), max(0, b+noise))
        
    bg = bg.filter(ImageFilter.GaussianBlur(radius=0.5))
    draw = ImageDraw.Draw(bg)

    # 1b. Draw Faint Drafting Grid (12x8 layout)
    grid_color = (225, 225, 220)
    col_width = width / 12
    row_height = height / 8
    
    for i in range(13):
        x = int(i * col_width)
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for i in range(9):
        y = int(i * row_height)
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # 1c. Draw Geometric Accent
    cx = int(1.5 * col_width)
    cy = int(2.5 * row_height)
    r = int(1.2 * col_width)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent_color)

    bg_path = "arch_bg_temp.png"
    bg.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # Grid metrics mapping for PPTX insertion
    col_inch = 13.333 / 12
    row_inch = 7.5 / 8

    # === Layer 2: Image Processing ===
    url = f"https://images.unsplash.com/featured/1000x800/?{bg_palette},building,structure"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    img_path = "arch_img_temp.jpg"
    has_img = False
    
    try:
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        arch_img = Image.open(io.BytesIO(img_data)).convert("L")  # Grayscale
        arch_img = arch_img.convert("RGB") # Re-convert to RGB for standard PPTX handling
        
        # Boost contrast for dramatic render aesthetic
        enhancer = ImageEnhance.Contrast(arch_img)
        arch_img = enhancer.enhance(1.3)
        
        # Crop to strict grid proportions (4.5 columns wide, 5 rows high)
        target_w, target_h = int(4.5 * col_width), int(5 * row_height)
        img_ratio = arch_img.width / arch_img.height
        target_ratio = target_w / target_h
        
        # Safe resampling fallback
        resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
        
        if img_ratio > target_ratio:
            new_h = target_h
            new_w = int(new_h * img_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / img_ratio)
            
        arch_img = arch_img.resize((new_w, new_h), resample_filter)
        left = (new_w - target_w) / 2
        top = (new_h - target_h) / 2
        arch_img = arch_img.crop((left, top, left + target_w, top + target_h))
        
        arch_img.save(img_path, quality=90)
        
        # Position mapping: Column 6.5, Row 2
        img_left = Inches(6.5 * col_inch)
        img_top = Inches(2 * row_inch)
        img_w_inch = Inches(4.5 * col_inch)
        img_h_inch = Inches(5 * row_inch)
        
        slide.shapes.add_picture(img_path, img_left, img_top, img_w_inch, img_h_inch)
        has_img = True
    except Exception as e:
        print(f"Image fetch failed: {e}")

    # === Layer 3: Typography Engine (lxml Injection) ===
    def add_tracked_text(text, left, top, width, height, font_size, tracking=200, color=RGBColor(50, 50, 50), is_title=False):
        """Helper to inject XML letter spacing (tracking) for Swiss aesthetic."""
        txBox = slide.shapes.add_textbox(left, top, width, height)
        txBox.margin_left, txBox.margin_top = 0, 0
        txBox.margin_right, txBox.margin_bottom = 0, 0
        
        p = txBox.text_frame.add_paragraph()
        run = p.add_run()
        run.text = text
        run.font.size = Pt(font_size)
        run.font.name = "Arial Black" if is_title else "Arial"
        run.font.bold = True
        run.font.color.rgb = color
        
        # Inject <a:spc> into run properties
        rPr = run._r.get_or_add_rPr()
        spc = OxmlElement('a:spc')
        spc.set('val', str(tracking)) # spacing in 1/100ths of a point
        rPr.append(spc)
        return txBox

    # Grid Anchors (Wide-tracked small caps)
    add_tracked_text("ARCHITECTURE REPRESENTATION", Inches(0.5), Inches(0.4), Inches(4), Inches(0.5), 8, tracking=300)
    add_tracked_text("DESIGN PROCESS", Inches(11), Inches(0.4), Inches(2), Inches(0.5), 8, tracking=300)
    add_tracked_text("showitbetter.", Inches(0.5), Inches(6.8), Inches(2), Inches(0.5), 10, tracking=50)

    if has_img:
        # Technical image caption
        add_tracked_text("FIG 1.0 - SPATIAL ORGANIZATION", img_left, img_top + img_h_inch + Inches(0.1), img_w_inch, Inches(0.3), 7, tracking=200, color=RGBColor(120, 120, 120))

    # Main Hierarchy
    title_left = Inches(1 * col_inch)
    
    # Hero Title (Negative tracking for tightly squashed letters)
    add_tracked_text(title_text.lower(), title_left, Inches(1.8 * row_inch), Inches(6), Inches(1.5), 68, tracking=-150, color=RGBColor(20, 20, 20), is_title=True)
    
    # Secondary / Phonetic accent
    txBox = slide.shapes.add_textbox(title_left, Inches(3.3 * row_inch), Inches(4), Inches(0.5))
    txBox.margin_left, txBox.margin_top = 0, 0
    run = txBox.text_frame.add_paragraph().add_run()
    run.text = "/ wɜːk.fləʊ /"
    run.font.size = Pt(16)
    run.font.italic = True
    run.font.name = "Georgia"
    run.font.color.rgb = RGBColor(100, 100, 100)

    # Body Paragraph
    txBox = slide.shapes.add_textbox(title_left, Inches(4.0 * row_inch), Inches(4.5 * col_inch), Inches(3 * row_inch))
    txBox.margin_left, txBox.margin_top = 0, 0
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.line_spacing = 1.3  # Clean editorial leading
    run = p.add_run()
    run.text = body_text
    run.font.size = Pt(13)
    run.font.name = "Arial"
    run.font.color.rgb = RGBColor(40, 40, 40)

    # Cleanup temporary assets
    try:
        os.remove(bg_path)
        if has_img: os.remove(img_path)
    except: pass

    prs.save(output_pptx_path)
    return output_pptx_path
