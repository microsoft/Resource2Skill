def create_slide(
    output_pptx_path: str,
    employee_name: str = "MEL STEAD",
    employee_title: str = "Procurement Manager",
    employee_quote: str = "\"I innovate on how we can walk the fine line between keeping our inventory low without stocking out.\"",
    accent_color: tuple = (109, 83, 155),  # Default Purple
    profile_img_url: str = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=800&auto=format&fit=crop",
    qa_pairs: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Split-Panel Employee Profile & Q&A layout.
    """
    import os
    import urllib.request
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    if qa_pairs is None:
        qa_pairs = [
            ("List five hashtags that describe your personality.", "#organized #coffeeholic #problem_solver #teamplayer #sarcastic"),
            ("If you could vacation anywhere in the world, where would you go?", "Norway. I'd love to see the fjords and the Northern Lights."),
            ("What is your favorite part about working here?", "I get to work with super smart and amazing people who are really fun."),
            ("Outside of work, what activity can we find you doing?", "Baking, eating, reading about baking, and hiking with my dog."),
            ("Apple or Android?", "Apple! Unless they stop supporting my favorite apps.")
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # Define colors
    color_accent = RGBColor(*accent_color)
    color_left_top_bg = RGBColor(235, 235, 235)
    color_q_text = RGBColor(60, 100, 120)  # Slate blue
    color_a_text = RGBColor(50, 50, 50)    # Dark grey
    color_white = RGBColor(255, 255, 255)

    # === LEFT PANEL ===
    left_width = Inches(4.5)
    
    # Top Grey Background
    top_bg = slide.shapes.add_shape(
        1, # msoShapeRectangle
        0, 0, left_width, Inches(4.0)
    )
    top_bg.fill.solid()
    top_bg.fill.fore_color.rgb = color_left_top_bg
    top_bg.line.fill.background()

    # Bottom Accent Background
    bottom_bg = slide.shapes.add_shape(
        1, 
        0, Inches(4.0), left_width, Inches(3.5)
    )
    bottom_bg.fill.solid()
    bottom_bg.fill.fore_color.rgb = color_accent
    bottom_bg.line.fill.background()

    # Profile Image Processing (Circular Crop with PIL)
    img_path = "temp_profile.png"
    try:
        req = urllib.request.Request(profile_img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        
        img = Image.open(io.BytesIO(img_data)).convert("RGBA")
        
        # Center crop to square
        min_dim = min(img.size)
        left = (img.width - min_dim)/2
        top = (img.height - min_dim)/2
        img = img.crop((left, top, left+min_dim, top+min_dim))
        
        # Create circular mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, min_dim, min_dim), fill=255)
        
        # Apply mask
        output = Image.new('RGBA', img.size, (0,0,0,0))
        output.paste(img, (0,0), mask)
        output.save(img_path)
        
        # Insert image (centered in top panel)
        img_size = Inches(2.8)
        img_x = (left_width - img_size) / 2
        img_y = Inches(0.6)
        slide.shapes.add_picture(img_path, img_x, img_y, img_size, img_size)
    except Exception as e:
        print(f"Failed to load/process image: {e}")
        # Fallback circle if image fails
        fallback = slide.shapes.add_shape(9, Inches(0.85), Inches(0.6), Inches(2.8), Inches(2.8)) # 9 is msoShapeOval
        fallback.fill.solid()
        fallback.fill.fore_color.rgb = RGBColor(200, 200, 200)
        fallback.line.fill.background()

    # Left Panel Text block
    text_box = slide.shapes.add_textbox(Inches(0.25), Inches(4.2), Inches(4.0), Inches(2.8))
    tf = text_box.text_frame
    tf.word_wrap = True
    
    # Name
    p_name = tf.paragraphs[0]
    p_name.text = employee_name.upper()
    p_name.alignment = PP_ALIGN.CENTER
    p_name.font.size = Pt(28)
    p_name.font.bold = True
    p_name.font.color.rgb = color_white

    # Title
    p_title = tf.add_paragraph()
    p_title.text = employee_title
    p_title.alignment = PP_ALIGN.CENTER
    p_title.font.size = Pt(16)
    p_title.font.color.rgb = color_white
    
    # Add some spacing before line
    p_spacer = tf.add_paragraph()
    p_spacer.font.size = Pt(10)

    # Quote
    p_quote = tf.add_paragraph()
    p_quote.text = employee_quote
    p_quote.alignment = PP_ALIGN.CENTER
    p_quote.font.size = Pt(12)
    p_quote.font.italic = True
    p_quote.font.color.rgb = color_white

    # Decorative Line between Title and Quote
    line = slide.shapes.add_shape(
        9, # msoShapeLine
        Inches(1.25), Inches(5.1), Inches(2.0), 0
    )
    line.line.color.rgb = color_white
    line.line.width = Pt(1.5)

    # === RIGHT PANEL (Q&A) ===
    # Right panel is inherently the slide background (white), we just position elements.
    
    # Logo placeholder in top left of right section
    logo_box = slide.shapes.add_textbox(Inches(4.8), Inches(0.3), Inches(2.0), Inches(0.5))
    logo_tf = logo_box.text_frame
    logo_p = logo_tf.paragraphs[0]
    logo_p.text = "COMPANY SPOTLIGHT"
    logo_p.font.size = Pt(10)
    logo_p.font.bold = True
    logo_p.font.color.rgb = color_accent

    # Q&A List
    start_y = Inches(1.0)
    y_step = Inches(1.25)
    
    for i, (question, answer) in enumerate(qa_pairs[:5]):
        current_y = start_y + (i * y_step)
        
        # Number Node (Circle)
        circle_radius = Inches(0.25)
        circle = slide.shapes.add_shape(
            9, # msoShapeOval
            Inches(5.0), current_y, circle_radius*2, circle_radius*2
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = color_accent
        circle.line.fill.background()
        
        # Text inside circle
        circle_tf = circle.text_frame
        circle_tf.margin_left = circle_tf.margin_right = circle_tf.margin_top = circle_tf.margin_bottom = 0
        circle_p = circle_tf.paragraphs[0]
        circle_p.text = str(i + 1)
        circle_p.alignment = PP_ALIGN.CENTER
        circle_p.font.size = Pt(20)
        circle_p.font.bold = True
        circle_p.font.color.rgb = color_white

        # Text Box for Q&A
        qa_box = slide.shapes.add_textbox(Inches(5.7), current_y - Inches(0.1), Inches(7.0), Inches(1.0))
        qa_tf = qa_box.text_frame
        qa_tf.word_wrap = True
        
        # Question
        q_p = qa_tf.paragraphs[0]
        q_p.text = question
        q_p.font.size = Pt(14)
        q_p.font.bold = True
        q_p.font.color.rgb = color_q_text
        
        # Answer
        a_p = qa_tf.add_paragraph()
        a_p.text = answer
        a_p.font.size = Pt(14)
        a_p.font.color.rgb = color_a_text
        a_p.space_before = Pt(4)

    prs.save(output_pptx_path)
    
    # Cleanup temp image
    if os.path.exists(img_path):
        os.remove(img_path)
        
    return output_pptx_path
