def create_slide(
    output_pptx_path: str,
    top_text: str = "THE BEST",
    main_text: str = "MOCKUP",
    bottom_text: str = "TOOLS",
    bg_color: tuple = (11, 7, 24, 255),
    burst_colors: list = [(0, 255, 255, 255), (255, 0, 128, 255), (138, 43, 226, 255), (255, 255, 255, 255)],
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Neon Radial Speedline Burst" visual effect.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import math
    import random
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # 2. Generate PIL Background Image (Neon Burst)
    width, height = 1920, 1080
    cx, cy = width / 2, height / 2
    
    # Base background
    base_img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(base_img)

    # Number of speedlines to generate
    num_lines = 45

    for _ in range(num_lines):
        # Calculate random angle and distance from center
        angle = random.uniform(0, math.pi * 2)
        
        # Keep an empty "safe zone" in the center (radius 200-300)
        r1 = random.uniform(250, 600) 
        # Lines shoot out past the edge of the canvas
        r2 = r1 + random.uniform(200, 1200)
        
        thickness = random.randint(12, 45)
        color = random.choice(burst_colors)

        # Calculate line endpoints using trigonometry
        x1 = cx + r1 * math.cos(angle)
        y1 = cy + r1 * math.sin(angle)
        x2 = cx + r2 * math.cos(angle)
        y2 = cy + r2 * math.sin(angle)

        # Draw the main line
        draw.line((x1, y1, x2, y2), fill=color, width=thickness)
        
        # Draw circles at the endpoints to create perfectly rounded capsules
        r = thickness / 2
        draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=color)
        draw.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill=color)

    # Draw a subtle dark radial gradient in the center to guarantee text legibility
    for i in range(400, 0, -8):
        alpha = int(((400 - i) / 400.0) * 120)  # Max opacity 120
        draw.ellipse((cx - i, cy - i, cx + i, cy + i), fill=(bg_color[0], bg_color[1], bg_color[2], alpha))

    # Save background to temp file
    temp_bg_path = os.path.join(os.path.dirname(output_pptx_path) or '.', "temp_burst_bg.png")
    base_img.save(temp_bg_path)

    # 3. Add Background to Slide
    slide.shapes.add_picture(temp_bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 4. Add Text Elements (Top, Main, Bottom)
    # Top Text
    top_box = slide.shapes.add_textbox(Inches(2), Inches(1.8), Inches(9.333), Inches(1))
    tf_top = top_box.text_frame
    tf_top.text = top_text
    tf_top.paragraphs[0].alignment = PP_ALIGN.CENTER
    font_top = tf_top.paragraphs[0].font
    font_top.name = 'Arial Black'
    font_top.size = Pt(36)
    font_top.bold = True
    font_top.color.rgb = RGBColor(255, 255, 255)

    # Main Text
    main_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.6), Inches(12.333), Inches(2.5))
    tf_main = main_box.text_frame
    tf_main.text = main_text
    tf_main.paragraphs[0].alignment = PP_ALIGN.CENTER
    font_main = tf_main.paragraphs[0].font
    font_main.name = 'Arial Black'
    font_main.size = Pt(110)
    font_main.bold = True
    font_main.color.rgb = RGBColor(255, 255, 255)

    # Bottom Text
    bottom_box = slide.shapes.add_textbox(Inches(2), Inches(5.0), Inches(9.333), Inches(1))
    tf_bot = bottom_box.text_frame
    tf_bot.text = bottom_text
    tf_bot.paragraphs[0].alignment = PP_ALIGN.CENTER
    font_bot = tf_bot.paragraphs[0].font
    font_bot.name = 'Arial Black'
    font_bot.size = Pt(44)
    font_bot.bold = True
    font_bot.color.rgb = RGBColor(255, 255, 255)

    # Clean up temp file and save
    prs.save(output_pptx_path)
    if os.path.exists(temp_bg_path):
        os.remove(temp_bg_path)
        
    return output_pptx_path
