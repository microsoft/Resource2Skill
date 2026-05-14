def create_slide(
    output_pptx_path: str,
    title_text: str = "Monthly\nBusiness\nReport",
    banner_text: str = "Presenting",
    bg_theme: str = "mountains,landscape",
    accent_color: tuple = (27, 60, 75),  # Dark Teal
    **kwargs,
) -> str:
    """
    Creates a presentation demonstrating the Corporate Chevron Anchor style.
    Generates two slides: a Hero Title slide and a Dashboard Content slide.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.dml.color import RGBColor
    import urllib.request
    from io import BytesIO
    from PIL import Image, ImageDraw

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # --- Helper Functions ---
    def add_shape_with_text(slide, shape_type, left, top, width, height, fill_rgb, text, font_size, text_rgb, bold=False, align=PP_ALIGN.CENTER):
        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*fill_rgb)
        shape.line.fill.background()
        
        tf = shape.text_frame
        tf.text = text
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = align
        p.font.size = Pt(font_size)
        p.font.color.rgb = RGBColor(*text_rgb)
        p.font.name = 'Arial'
        p.font.bold = bold
        return shape

    def generate_bg_image(width_in, height_in, theme):
        w_px, h_px = int(width_in * 96), int(height_in * 96)
        try:
            url = f"https://images.unsplash.com/featured/{w_px}x{h_px}/?{theme}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img = Image.open(BytesIO(response.read())).convert("RGBA")
                # Resize and crop to fit exactly
                img = img.resize((w_px, h_px), Image.Resampling.LANCZOS)
        except Exception:
            # Fallback gradient
            img = Image.new("RGBA", (w_px, h_px), (40, 50, 60, 255))
        
        # Apply dark overlay for text readability (35% black)
        overlay = Image.new("RGBA", (w_px, h_px), (0, 0, 0, 90))
        final_img = Image.alpha_composite(img, overlay)
        
        img_io = BytesIO()
        final_img.convert("RGB").save(img_io, format="JPEG", quality=90)
        img_io.seek(0)
        return img_io

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide_1 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 1. Background Image
    bg_stream = generate_bg_image(13.333, 7.5, bg_theme)
    slide_1.shapes.add_picture(bg_stream, 0, 0, width=Inches(13.333), height=Inches(7.5))
    
    # 2. Chevron/Pentagon Anchor Banner
    banner = add_shape_with_text(
        slide_1, MSO_SHAPE.PENTAGON, 
        left=Inches(-0.1), top=Inches(0.8), width=Inches(4.5), height=Inches(1.0),
        fill_rgb=accent_color, text=banner_text.upper(), 
        font_size=32, text_rgb=(255, 255, 255), bold=True
    )
    # Adjust the point of the pentagon to not be too sharp
    banner.adjustments[0] = 0.2
    
    # 3. Main Hero Title Text
    tx_box = slide_1.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(8), Inches(4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(72)
    p.font.bold = True
    p.font.color.rgb = RGBColor(230, 235, 238)
    p.line_spacing = 0.9  # Tight leading

    # ==========================================
    # SLIDE 2: DASHBOARD CONTENT SLIDE
    # ==========================================
    slide_2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Light background
    bg_shape = slide_2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(250, 250, 250)
    bg_shape.line.fill.background()
    
    # Section Banner
    section_banner = add_shape_with_text(
        slide_2, MSO_SHAPE.PENTAGON, 
        left=Inches(-0.1), top=Inches(0.5), width=Inches(5.0), height=Inches(0.7),
        fill_rgb=(243, 156, 18), text="Follow up on OKR Goals", 
        font_size=24, text_rgb=(255, 255, 255), bold=True, align=PP_ALIGN.LEFT
    )
    section_banner.adjustments[0] = 0.15
    # Fix left alignment padding hack
    section_banner.text_frame.margin_left = Inches(0.5)

    # --- OKR Metric Cards Generation ---
    cyan_rgb = (23, 162, 184)
    card_top = 1.6
    
    for i, (okr_title, progress) in enumerate([("Objective 1", 30), ("Objective 2", 75), ("Objective 3", 48)]):
        y_pos = Inches(card_top + (i * 1.6))
        
        # Base Card
        card = slide_2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), y_pos, Inches(11.333), Inches(1.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = RGBColor(220, 220, 220)
        card.adjustments[0] = 0.05
        
        # Left Accent Tab (Chevron) inside card
        tab = add_shape_with_text(
            slide_2, MSO_SHAPE.PENTAGON, 
            left=Inches(0.8), top=y_pos + Inches(0.15), width=Inches(1.8), height=Inches(1.0),
            fill_rgb=cyan_rgb, text=okr_title, font_size=16, text_rgb=(255, 255, 255), bold=True
        )
        tab.text_frame.text = okr_title.replace(" ", "\n") # Stack text
        
        # Description text
        desc = slide_2.shapes.add_textbox(Inches(2.8), y_pos + Inches(0.4), Inches(4), Inches(0.5))
        desc.text_frame.text = "Description for this key result and its current status."
        desc.text_frame.paragraphs[0].font.size = Pt(14)
        desc.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)
        
        # Progress Bar Track (Background)
        track = slide_2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), y_pos + Inches(0.6), Inches(3.0), Inches(0.15))
        track.fill.solid()
        track.fill.fore_color.rgb = RGBColor(230, 230, 230)
        track.line.fill.background()
        
        # Progress Bar Fill (Foreground)
        fill_width = Inches(3.0 * (progress / 100.0))
        fill = slide_2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), y_pos + Inches(0.6), fill_width, Inches(0.15))
        fill.fill.solid()
        fill.fill.fore_color.rgb = cyan_rgb
        fill.line.fill.background()
        
        # Progress Indicator (Circle)
        circle = add_shape_with_text(
            slide_2, MSO_SHAPE.OVAL,
            left=Inches(11.0), top=y_pos + Inches(0.25), width=Inches(0.8), height=Inches(0.8),
            fill_rgb=(255, 255, 255), text=f"{progress}%", font_size=16, text_rgb=cyan_rgb, bold=True
        )
        circle.line.color.rgb = cyan_rgb
        circle.line.width = Pt(3)

    prs.save(output_pptx_path)
    return output_pptx_path
