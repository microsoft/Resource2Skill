def create_slide(
    output_pptx_path: str,
    title_text: str = "WHAT WE DO ARE\nGORGEOUS!",
    bg_theme: str = "ocean horizon minimal",
    node_labels: list = ["Good Idea", "Good Timing", "Good Result"],
    node_colors: list = [(255, 180, 0), (0, 160, 220), (220, 50, 50)],
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Circular Node Morph Reveal Layout'.
    Generates perfectly layered numbered circles and circularly cropped images.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Helper 1: Download Image
    def download_image(query, width, height):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(query)}?width={width}&height={height}&nologo=true"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return Image.open(BytesIO(response.read())).convert("RGBA")
        except Exception as e:
            print(f"Image download failed for '{query}': {e}")
            # Fallback: create a solid color image
            return Image.new('RGBA', (width, height), (150, 150, 150, 255))

    # Helper 2: Create Circular Masked Image
    def create_circular_image(img, size=400):
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        # Create a blank transparent image
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        # Create a mask
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        # Paste image using mask
        output.paste(img, (0, 0), mask)
        
        img_stream = BytesIO()
        output.save(img_stream, format='PNG')
        img_stream.seek(0)
        return img_stream

    # === Layer 1: Background ===
    bg_img = download_image(bg_theme, 1920, 1080)
    bg_stream = BytesIO()
    bg_img.convert("RGB").save(bg_stream, format='JPEG')
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Main Title ===
    title_box = slide.shapes.add_textbox(Inches(2), Inches(0.8), Inches(9.33), Inches(2))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # === Layer 3: Nodes & Morph Reveal Layers ===
    num_nodes = len(node_labels)
    circle_diameter = Inches(1.5)
    y_center = Inches(3.5)
    
    # Search queries for the reveal images
    image_queries = ["smiling person laptop yellow background", "clock icon minimal blue", "business team meeting success"]

    for i in range(num_nodes):
        # Calculate equidistant horizontal centers
        x_center = prs.slide_width * (i + 1) / (num_nodes + 1)
        x_pos = x_center - (circle_diameter / 2)
        y_pos = y_center - (circle_diameter / 2)
        
        # State 1: The White Numbered Circle
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, x_pos, y_pos, circle_diameter, circle_diameter
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
        circle.line.fill.background() # No line
        
        # Add number text to circle
        text_frame = circle.text_frame
        text_frame.clear()
        p = text_frame.paragraphs[0]
        p.text = str(i + 1)
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = RGBColor(*node_colors[i % len(node_colors)])

        # Sub-label Text (appears during morph)
        label_width = Inches(2)
        label_box = slide.shapes.add_textbox(
            x_center - (label_width / 2), y_center + circle_diameter/2 + Inches(0.2), 
            label_width, Inches(0.5)
        )
        lp = label_box.text_frame.paragraphs[0]
        lp.text = node_labels[i]
        lp.alignment = PP_ALIGN.CENTER
        lp.font.size = Pt(18)
        lp.font.bold = True
        lp.font.color.rgb = RGBColor(*node_colors[i % len(node_colors)])

        # State 2: The Revealed Image (Layered exactly on top)
        raw_img = download_image(image_queries[i], 400, 400)
        circular_img_stream = create_circular_image(raw_img, size=400)
        
        # Insert the circular image exactly over the shape
        pic = slide.shapes.add_picture(
            circular_img_stream, x_pos, y_pos, circle_diameter, circle_diameter
        )
        
        # Note for end-user: In PowerPoint, apply "Zoom" entrance animation to 'pic', 
        # and "Zoom" exit animation to 'circle' to complete the effect.

    prs.save(output_pptx_path)
    return output_pptx_path
