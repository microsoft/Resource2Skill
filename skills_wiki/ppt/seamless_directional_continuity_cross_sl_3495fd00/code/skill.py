def create_slide(
    output_pptx_path: str,
    title_text: str = "THIS IS SLIDE 1",
    body_text: str = "THIS IS SLIDE 2",
    bg_palette: str = "default",  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Seamless Directional Continuity effect.
    Generates a 2-slide presentation with a custom PIL vector skyline and an injected XML Push transition.
    """
    import os
    import random
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    from lxml import etree

    # --- Configuration & Colors ---
    slide_w_in, slide_h_in = 13.333, 7.5
    color_slide1 = (91, 142, 235, 255)  # Sky Blue
    color_slide2 = (221, 143, 148, 255) # Dusty Rose
    color_white = (255, 255, 255, 255)

    # --- Helper 1: Generate Vector Skyline Background via PIL ---
    def generate_skyline_bg(width_in, height_in, bg_color, output_filename, seed=42):
        dpi = 300
        px_w, px_h = int(width_in * dpi), int(height_in * dpi)
        img = Image.new('RGBA', (px_w, px_h), bg_color)
        draw = ImageDraw.Draw(img)
        
        random.seed(seed) # Ensure identical skyline on both slides for continuity
        num_buildings = 25
        b_width = px_w // num_buildings
        
        # Draw flat vector buildings
        for i in range(num_buildings):
            # Vary height but keep it in the bottom 30% of the slide
            bh = random.randint(px_h // 8, px_h // 3)
            # Add some gaps and varied widths for a realistic skyline
            if random.random() > 0.15: 
                x0 = i * b_width + random.randint(0, 10)
                x1 = (i + 1) * b_width - random.randint(0, 10)
                y0 = px_h - bh
                y1 = px_h
                draw.rectangle([x0, y0, x1, y1], fill=color_white)
                
                # Draw a few square "windows" randomly
                if random.random() > 0.5:
                    win_w, win_h = 20, 30
                    win_x = x0 + (x1 - x0)//2 - win_w//2
                    win_y = y0 + 50
                    draw.rectangle([win_x, win_y, win_x+win_w, win_y+win_h], fill=bg_color)

        img.save(output_filename)
        return output_filename

    # Create temporary background images
    bg1_path = generate_skyline_bg(slide_w_in, slide_h_in, color_slide1, "temp_bg1.png")
    bg2_path = generate_skyline_bg(slide_w_in, slide_h_in, color_slide2, "temp_bg2.png")

    # --- Helper 2: Inject Push Transition via lxml ---
    def apply_push_transition(slide, direction="l"):
        """Injects a push transition (p:push) shifting the slide."""
        xml = slide.element
        nsmap = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
        
        # Create Transition elements
        transition = etree.Element("{%s}transition" % nsmap['p'], spd="slow")
        # dir="l" means push from the right to the left
        etree.SubElement(transition, "{%s}push" % nsmap['p'], dir=direction)
        
        # Insert <p:transition> after <p:cSld>
        csld = xml.find('.//p:cSld', namespaces=nsmap)
        if csld is not None:
            csld.addnext(transition)

    # --- PPTX Setup ---
    prs = Presentation()
    prs.slide_width = Inches(slide_w_in)
    prs.slide_height = Inches(slide_h_in)
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: The Origin
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.shapes.add_picture(bg1_path, 0, 0, Inches(slide_w_in), Inches(slide_h_in))

    # Slide 1 Title
    tb1 = slide1.shapes.add_textbox(Inches(2), Inches(1), Inches(9.33), Inches(1.5))
    p1 = tb1.text_frame.add_paragraph()
    p1.text = title_text.upper()
    p1.alignment = PP_ALIGN.CENTER
    p1.font.bold = True
    p1.font.size = Pt(64)
    p1.font.color.rgb = RGBColor(255, 255, 255)

    # Slide 1 Circles (The subjects that will "move")
    circle_size = Inches(1.8)
    # Circle 1 (Left)
    shape1 = slide1.shapes.add_shape(9, Inches(4.5), Inches(3.5), circle_size, circle_size) # 9 is msoShapeOval
    shape1.fill.solid()
    shape1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    shape1.line.fill.background()
    # Circle 2 (Right)
    shape2 = slide1.shapes.add_shape(9, Inches(7), Inches(3.5), circle_size, circle_size)
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = RGBColor(255, 255, 255)
    shape2.line.fill.background()


    # ==========================================
    # SLIDE 2: The Destination
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.shapes.add_picture(bg2_path, 0, 0, Inches(slide_w_in), Inches(slide_h_in))

    # Apply the XML transition to seamlessly flow from Slide 1 -> Slide 2
    apply_push_transition(slide2, direction="l")

    # Slide 2 Title
    tb2 = slide2.shapes.add_textbox(Inches(4), Inches(1), Inches(8), Inches(1.5))
    p2 = tb2.text_frame.add_paragraph()
    p2.text = body_text.upper()
    p2.alignment = PP_ALIGN.LEFT
    p2.font.bold = True
    p2.font.size = Pt(64)
    p2.font.color.rgb = RGBColor(255, 255, 255)

    # Slide 2 Circle (Arriving from the right)
    shape3 = slide2.shapes.add_shape(9, Inches(1.5), Inches(3.5), circle_size, circle_size)
    shape3.fill.solid()
    shape3.fill.fore_color.rgb = RGBColor(255, 255, 255)
    shape3.line.fill.background()

    # Slide 2 Bullet Points
    tb_bullets = slide2.shapes.add_textbox(Inches(4), Inches(3.5), Inches(8), Inches(3))
    tf = tb_bullets.text_frame
    tf.word_wrap = True
    
    bullets = ["This is my first point", "This is my second point", "This is my third point"]
    for i, bullet in enumerate(bullets):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = bullet
        p.font.size = Pt(36)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.level = 0

    # Save and cleanup
    prs.save(output_pptx_path)
    if os.path.exists(bg1_path): os.remove(bg1_path)
    if os.path.exists(bg2_path): os.remove(bg2_path)

    return output_pptx_path
