def create_slide(
    output_pptx_path: str,
    title_text: str = "DEVICE MOCKUP",
    body_text: str = "PHONE",
    bg_palette: str = "city,architecture", 
    accent_color: tuple = (30, 30, 30), 
    **kwargs,
) -> str:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw
    import io
    import urllib.request
    from lxml import etree

    # === Initialize Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Helper Functions ===
    def set_round_rect_adj(shape, adj_val=22000):
        """Uses lxml to set the corner radius of a python-pptx rounded rectangle."""
        try:
            nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            prstGeom = shape._element.xpath('.//a:prstGeom', namespaces=nsmap)[0]
            avLst = prstGeom.find('a:avLst', namespaces=nsmap)
            if avLst is None:
                avLst = etree.SubElement(prstGeom, '{http://schemas.openxmlformats.org/drawingml/2006/main}avLst')
            gd = avLst.find('a:gd[@name="adj"]', namespaces=nsmap)
            if gd is None:
                gd = etree.SubElement(avLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}gd')
                gd.set('name', 'adj')
            gd.set('fmla', f'val {adj_val}')
        except Exception as e:
            print(f"Warning: Could not adjust shape roundness: {e}")

    def create_rounded_screen_image(image_url, width_in, height_in, dpi=300, radius_ratio=0.11):
        """Downloads, crops, and applies a rounded transparency mask via PIL."""
        width_px, height_px = int(width_in * dpi), int(height_in * dpi)
        corner_radius = int(width_px * radius_ratio)

        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                img = Image.open(io.BytesIO(response.read())).convert("RGBA")
        except Exception:
            # Fallback gradient if download fails
            img = Image.new('RGBA', (width_px, height_px))
            draw = ImageDraw.Draw(img)
            for y in range(height_px):
                c = int(240 - (100 * y / height_px))
                draw.line([(0, y), (width_px, y)], fill=(c, c, c+20, 255))

        # Crop to perfectly fit target aspect ratio
        target_ratio = width_px / height_px
        img_ratio = img.width / img.height
        if img_ratio > target_ratio: # Crop sides
            new_w = int(img.height * target_ratio)
            off = (img.width - new_w) // 2
            img = img.crop((off, 0, off + new_w, img.height))
        else: # Crop top/bottom
            new_h = int(img.width / target_ratio)
            off = (img.height - new_h) // 2
            img = img.crop((0, off, img.width, off + new_h))
            
        img = img.resize((width_px, height_px), Image.Resampling.LANCZOS)

        # Apply rounded mask
        mask = Image.new('L', (width_px, height_px), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, width_px, height_px), corner_radius, fill=255)
        
        result = Image.new('RGBA', (width_px, height_px), (0, 0, 0, 0))
        result.paste(img, (0, 0), mask)
        
        output = io.BytesIO()
        result.save(output, format='PNG')
        output.seek(0)
        return output

    def add_info_block(slide, x_center, y, is_left_side=True):
        """Constructs the symmetrical text + icon layout blocks."""
        icon_size = Inches(0.4)
        text_w = Inches(2.3)
        text_h = Inches(1.0)
        
        if is_left_side:
            icon_x = x_center
            text_x = x_center - text_w - Inches(0.15)
            align = PP_ALIGN.RIGHT
        else:
            icon_x = x_center - icon_size
            text_x = x_center + Inches(0.15)
            align = PP_ALIGN.LEFT

        # Add Icon Ring
        icon = slide.shapes.add_shape(MSO_SHAPE.OVAL, icon_x, y, icon_size, icon_size)
        icon.fill.background()
        icon.line.color.rgb = RGBColor(100, 100, 100)
        icon.line.width = Pt(1.5)
        
        p = icon.text_frame.paragraphs[0]
        p.text = "✓"
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(100, 100, 100)
        p.alignment = PP_ALIGN.CENTER
        icon.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Add Typography
        tx_box = slide.shapes.add_textbox(text_x, y - Inches(0.1), text_w, text_h)
        tf = tx_box.text_frame
        
        p1 = tf.paragraphs[0]
        p1.text = "SOME INFO"
        p1.font.bold = True
        p1.font.size = Pt(13)
        p1.alignment = align
        
        p2 = tf.add_paragraph()
        p2.text = "Insert some awesome text right here. Just remember keep it short and sweet."
        p2.font.size = Pt(10)
        p2.font.color.rgb = RGBColor(120, 120, 120)
        p2.alignment = align

    # === Build Layer 1: Slide Layout & Title ===
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.4), prs.slide_width, Inches(0.8))
    tf = title_box.text_frame
    p1 = tf.paragraphs[0]
    p1.text = title_text
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = body_text.upper()
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(150, 150, 150)
    p2.alignment = PP_ALIGN.CENTER

    # === Build Layer 2: Device Mockup ===
    phone_w, phone_h = 2.6, 5.5
    phone_left = (13.333 - phone_w) / 2
    phone_top = 1.6

    # 1. Download & process screen image
    img_url = f"https://source.unsplash.com/random/800x1600/?{bg_palette}"
    screen_stream = create_rounded_screen_image(img_url, phone_w, phone_h)
    
    # 2. Place screen image
    slide.shapes.add_picture(
        screen_stream, 
        Inches(phone_left), Inches(phone_top), 
        Inches(phone_w), Inches(phone_h)
    )

    # 3. Draw Hardware Bezel Overlay
    bezel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        Inches(phone_left), Inches(phone_top), 
        Inches(phone_w), Inches(phone_h)
    )
    bezel.fill.background() # Transparent interior
    bezel.line.color.rgb = RGBColor(*accent_color)
    bezel.line.width = Pt(8)
    set_round_rect_adj(bezel, 22000) # Sync corner radius with PIL image (22% of half-width)

    # 4. Draw Hardware Notch
    notch_w = 1.1
    notch = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches((13.333 - notch_w) / 2), Inches(phone_top - 0.02),
        Inches(notch_w), Inches(0.18)
    )
    notch.fill.solid()
    notch.fill.fore_color.rgb = RGBColor(*accent_color)
    notch.line.fill.background()
    set_round_rect_adj(notch, 50000) # Full pill shape

    # === Build Layer 3: Flanking Symmetrical Content ===
    # Left side (X anchor for icon, text pushes left)
    add_info_block(slide, x_center=Inches(4.5), y=Inches(2.5), is_left_side=True)
    add_info_block(slide, x_center=Inches(4.5), y=Inches(4.5), is_left_side=True)
    
    # Right side (X anchor for icon, text pushes right)
    add_info_block(slide, x_center=Inches(13.333 - 4.5), y=Inches(2.5), is_left_side=False)
    add_info_block(slide, x_center=Inches(13.333 - 4.5), y=Inches(4.5), is_left_side=False)

    prs.save(output_pptx_path)
    return output_pptx_path
