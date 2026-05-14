def create_slide(
    output_pptx_path: str,
    quote_text: str = "BE THE CHANGE THAT YOU WISH TO SEE IN THE WORLD.",
    author_text: str = "- Mahatma Gandhi",
    image_url: str = "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=800&auto=format&fit=crop",
    accent_color: tuple = (255, 204, 0),  # Vibrant Yellow
    highlight_words: list = ["CHANGE", "WORLD."], # Words to color in the quote
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'High-Impact Geometric Quote Reveal' effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw
    import urllib.request
    from io import BytesIO
    import os

    # 1. Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 2. Set Dark Background
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(24, 26, 30)
    bg.line.fill.background()

    # 3. Add Watermark Oversized Quote Marks
    qm_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(3), Inches(3))
    qm_tf = qm_box.text_frame
    qm_p = qm_tf.add_paragraph()
    qm_p.text = "“"
    qm_p.font.name = "Arial Black"
    qm_p.font.size = Pt(250)
    qm_p.font.color.rgb = RGBColor(45, 48, 55) # Dark gray simulating watermark

    # 4. Prepare B&W Circular Image using PIL
    img_stream = BytesIO()
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read())).convert("RGBA")
            
        # Crop to square
        size = min(img.size)
        left = (img.size[0] - size) / 2
        top = (img.size[1] - size) / 2
        img = img.crop((left, top, left + size, top + size))
        
        # Convert to Grayscale, then back to RGBA for masking
        img = img.convert("L").convert("RGBA")
        
        # Create circular alpha mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        img.save(img_stream, format="PNG")
        img_stream.seek(0)
    except Exception as e:
        print(f"Image download/processing failed: {e}. Using a solid gray circle instead.")
        # Fallback to a gray circle if download fails
        img = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 800, 800), fill=(100, 100, 100, 255))
        img.save(img_stream, format="PNG")
        img_stream.seek(0)

    # 5. Place Accent Geometric Container (Yellow Circle)
    circle_size = Inches(5.2)
    circle_left = Inches(7.2)
    circle_top = Inches(1.15)
    
    accent_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, circle_left, circle_top, circle_size, circle_size
    )
    accent_circle.fill.solid()
    accent_circle.fill.fore_color.rgb = RGBColor(*accent_color)
    accent_circle.line.fill.background() # No line

    # 6. Insert B&W Processed Image over the container (slightly offset)
    img_size = Inches(5.0)
    img_left = Inches(7.3)
    img_top = Inches(1.25)
    slide.shapes.add_picture(img_stream, img_left, img_top, img_size, img_size)

    # 7. Add Typography (The Quote)
    text_box = slide.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(5.0), Inches(2.5))
    text_frame = text_box.text_frame
    text_frame.word_wrap = True
    
    p = text_frame.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    p.line_spacing = 1.1
    
    # Process text for highlighting specific words
    words = quote_text.split()
    for word in words:
        run = p.add_run()
        run.text = word + " "
        run.font.name = "Montserrat"
        run.font.size = Pt(36)
        run.font.bold = True
        
        # Color highlight check
        clean_word = word.strip('.,;!?')
        if any(hw.upper() == clean_word.upper() or hw.upper() == word.upper() for hw in highlight_words):
            run.font.color.rgb = RGBColor(*accent_color)
        else:
            run.font.color.rgb = RGBColor(255, 255, 255)

    # 8. Add Attribution/Author
    p_author = text_frame.add_paragraph()
    p_author.alignment = PP_ALIGN.LEFT
    run_author = p_author.add_run()
    run_author.text = f"\n{author_text}"
    run_author.font.name = "Montserrat"
    run_author.font.size = Pt(20)
    run_author.font.color.rgb = RGBColor(200, 200, 200) # Light gray

    # Save
    prs.save(output_pptx_path)
    return output_pptx_path
