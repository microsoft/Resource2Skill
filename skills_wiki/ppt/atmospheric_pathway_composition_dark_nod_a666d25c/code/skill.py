def create_slide(
    output_pptx_path: str,
    title_text: str = "SLIDE ZOOM",
    subtitle_text: str = "POWERPOINT TEMPLATE",
    bg_keyword: str = "dark forest foggy",
    nodes: list = ["OPPORTUNITY", "MARKET", "SOLUTION", "BUSINESS MODEL"],
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Atmospheric Pathway" design style.
    Downloads a moody background, applies an overlay, and draws a connected node map.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageEnhance

    # 1. Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 2. Generate/Process Background Image via PIL
    bg_img_path = "temp_bg_atmospheric.jpg"
    
    try:
        # Fetch an HD image from Unsplash
        url = f"https://source.unsplash.com/1920x1080/?{bg_keyword.replace(' ', ',')}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(bg_img_path, 'wb') as f:
                f.write(response.read())
        
        # Process image: ensure size and add dark overlay for contrast
        with Image.open(bg_img_path) as img:
            img = img.convert("RGBA")
            # Resize and crop to 16:9 (1920x1080)
            target_ratio = 16 / 9
            img_ratio = img.width / img.height
            if img_ratio > target_ratio:
                new_width = int(target_ratio * img.height)
                offset = (img.width - new_width) / 2
                img = img.crop((offset, 0, img.width - offset, img.height))
            else:
                new_height = int(img.width / target_ratio)
                offset = (img.height - new_height) / 2
                img = img.crop((0, offset, img.width, img.height - offset))
            
            img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            
            # Apply darkening overlay (opacity 100 out of 255)
            overlay = Image.new('RGBA', img.size, (15, 20, 25, 100))
            img = Image.alpha_composite(img, overlay)
            
            # Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            img.convert("RGB").save(bg_img_path, quality=90)
            
    except Exception as e:
        # Fallback: Create a dark atmospheric gradient/solid image
        print(f"Image download failed, using fallback. Error: {e}")
        img = Image.new('RGB', (1920, 1080), (13, 22, 28))
        draw = ImageDraw.Draw(img)
        # Simple radial-ish gradient simulation
        for i in range(1080):
            color = (int(13 + i/100), int(22 + i/80), int(28 + i/70))
            draw.line([(0, i), (1920, i)], fill=color)
        img.save(bg_img_path)

    # Add background to slide
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 3. Add Main Title
    title_box = slide.shapes.add_textbox(Inches(2), Inches(0.5), Inches(9.333), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial" # Fallback for Impact/Montserrat
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = False
    p2.font.color.rgb = RGBColor(200, 200, 200)

    # 4. Calculate Node Layout (Zig-Zag Pathway)
    # We want them spread evenly across the width
    num_nodes = len(nodes)
    start_x, end_x = Inches(2.5), Inches(10.8)
    gap_x = (end_x - start_x) / (num_nodes - 1) if num_nodes > 1 else 0
    
    # Alternating Y positions for the dynamic look
    y_positions = [Inches(5.0), Inches(3.5), Inches(5.0), Inches(3.0), Inches(5.5)]
    
    node_coords = []
    for i in range(num_nodes):
        x = start_x + (i * gap_x)
        y = y_positions[i % len(y_positions)]
        node_coords.append((x, y))

    # 5. Draw Connectors (Lines) BEFORE nodes so they sit behind
    for i in range(num_nodes - 1):
        x1, y1 = node_coords[i]
        x2, y2 = node_coords[i+1]
        
        connector = slide.shapes.add_connector(MSO_SHAPE.LINE_CALLOUT_1, x1, y1, x2, y2)
        line = connector.line
        line.color.rgb = RGBColor(255, 255, 255)
        line.width = Pt(3)
        line.dash_style = 4 # MSO_LINE.DASH (usually maps to 4)

    # 6. Draw Nodes (Circles + Text)
    circle_size = Inches(1.8)
    
    for i, (cx, cy) in enumerate(node_coords):
        # Top-left corner of the bounding box for the circle
        left = cx - (circle_size / 2)
        top = cy - (circle_size / 2)
        
        # Circle shape
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, circle_size, circle_size)
        
        # Style: Dark fill (to mask lines behind it) and thick white line
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(25, 30, 35) # Dark hue to match nature background
        circle.line.color.rgb = RGBColor(255, 255, 255)
        circle.line.width = Pt(4)
        
        # Inner text (Number/Icon placeholder)
        tf = circle.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"0{i+1}"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # External Label below the circle
        label_width = Inches(2.5)
        label_box = slide.shapes.add_textbox(cx - (label_width/2), cy + (circle_size/2) + Inches(0.1), label_width, Inches(0.5))
        tf_label = label_box.text_frame
        p_label = tf_label.paragraphs[0]
        p_label.text = nodes[i]
        p_label.alignment = PP_ALIGN.CENTER
        p_label.font.name = "Arial"
        p_label.font.size = Pt(16)
        p_label.font.bold = True
        p_label.font.color.rgb = RGBColor(255, 255, 255)

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
