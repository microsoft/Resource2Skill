def create_slide(
    output_pptx_path: str,
    title_text: str = "PowerPoint Template",
    subtitle_text: str = "Presenter bigchin Project Manager, @Your Inc.",
    base_color_start: tuple = (10, 15, 35),
    base_color_end: tuple = (25, 45, 100),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Corporate Geometric Fluid Rings Aesthetic'.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    import io

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # 2. Generate the Fluid Rings Background using PIL
    width, height = 1920, 1080
    
    # 2a. Draw the Base Gradient
    base_img = Image.new('RGBA', (width, height))
    draw_base = ImageDraw.Draw(base_img)
    for y in range(height):
        r = int(base_color_start[0] + (base_color_end[0] - base_color_start[0]) * (y / height))
        g = int(base_color_start[1] + (base_color_end[1] - base_color_start[1]) * (y / height))
        b = int(base_color_start[2] + (base_color_end[2] - base_color_start[2]) * (y / height))
        draw_base.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # 2b. Draw Overlapping Transparent Rings
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    # Define rings: (x0, y0, x1, y1, stroke_width, color_rgba)
    # Scaled massively to act as macro geometric textures
    rings = [
        (-600, -400, 1000, 1200, 250, (100, 140, 255, 35)),   # Top Left giant ring
        (1200, -300, 2600, 1100, 350, (120, 160, 255, 25)),   # Top Right giant ring
        (600, 500, 1800, 1700, 200, (80, 120, 250, 45)),      # Bottom Right medium ring
        (1400, 800, 2000, 1400, 120, (150, 180, 255, 60)),    # Bottom Right small accent ring
        (-200, 700, 800, 1700, 180, (90, 130, 255, 40)),      # Bottom Left ring
    ]
    
    for bbox in rings:
        # draw.ellipse handles transparency composition perfectly within the overlay layer
        draw_overlay.ellipse(bbox[:4], outline=bbox[5], width=bbox[4])

    # 2c. Composite and Save to BytesIO
    final_bg = Image.alpha_composite(base_img, overlay)
    bg_stream = io.BytesIO()
    # Convert to RGB to save as high-quality JPEG to keep PPTX size reasonable
    final_bg.convert("RGB").save(bg_stream, format="JPEG", quality=95)
    bg_stream.seek(0)

    # 3. Apply Background to Slide
    slide.shapes.add_picture(bg_stream, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    # 4. Add Core Typography (Center Alignment)
    # Title
    title_box = slide.shapes.add_textbox(Inches(2.66), Inches(3.0), Inches(8.0), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(54)
    p.font.name = "Arial"
    p.font.bold = False
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(2.66), Inches(4.2), Inches(8.0), Inches(0.8))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.size = Pt(18)
    p_sub.font.name = "Arial"
    p_sub.font.color.rgb = RGBColor(200, 220, 255)

    # 5. Add Center Icon Decoration (Lightning Bolt / Circle Motif)
    # Create a white circle with a dark icon inside, representing the branding badge seen in the template
    icon_bg = slide.shapes.add_shape(
        5, # msoShapeOval
        Inches(6.33), Inches(1.8), Inches(0.66), Inches(0.66)
    )
    icon_bg.fill.solid()
    icon_bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
    icon_bg.line.fill.background()
    
    # Add simple text icon (Lightning bolt)
    tf_icon = icon_bg.text_frame
    tf_icon.margin_bottom = tf_icon.margin_top = tf_icon.margin_left = tf_icon.margin_right = 0
    p_icon = tf_icon.paragraphs[0]
    p_icon.text = "⚡"
    p_icon.alignment = PP_ALIGN.CENTER
    p_icon.font.size = Pt(24)
    p_icon.font.color.rgb = RGBColor(20, 30, 90)

    # 6. Add "Data Strategy" Footer Cards to emulate the business slide layout
    # Creating 3 clean white transparent overlay cards at the bottom
    card_width = 3.0
    card_height = 1.2
    spacing = 0.5
    start_x = (13.333 - (3 * card_width + 2 * spacing)) / 2  # Center the group of cards
    
    metrics = [("20%", "More than last year"), ("30%", "Growth in Q3"), ("80%", "Customer Retention")]

    for i, (metric, label) in enumerate(metrics):
        x = start_x + (i * (card_width + spacing))
        y = 5.5
        
        # Add Card Shape
        card = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(card_width), Inches(card_height))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        # Emulate transparency by manipulating XML (standard python-pptx doesn't expose shape transparency directly)
        card.fill.fore_color.theme_color = 1
        card.line.fill.background()
        
        # Add Metric Text
        tf_card = card.text_frame
        p_metric = tf_card.paragraphs[0]
        p_metric.text = metric
        p_metric.alignment = PP_ALIGN.CENTER
        p_metric.font.size = Pt(28)
        p_metric.font.bold = True
        p_metric.font.color.rgb = RGBColor(40, 60, 160)
        
        p_label = tf_card.add_paragraph()
        p_label.text = label
        p_label.alignment = PP_ALIGN.CENTER
        p_label.font.size = Pt(12)
        p_label.font.color.rgb = RGBColor(100, 120, 150)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
