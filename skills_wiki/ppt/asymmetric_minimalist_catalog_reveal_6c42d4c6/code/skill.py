def create_slide(
    output_pptx_path: str,
    title_text: str = "Products\nShowcase",
    body_text: str = "Lorem ipsum dolor sit amet,\nconsectetuer adipiscing elit.",
    bg_keyword: str = "cosmetics flatlay",
    accent_color: tuple = (175, 244, 226),  # Mint Green
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Asymmetric Minimalist Catalog Reveal" effect.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    accent_rgb = RGBColor(*accent_color)
    dark_text_rgb = RGBColor(30, 30, 30)

    # === Layer 1: Background Product Image (Right Side) ===
    # Download placeholder image
    img_path = "temp_product_bg.jpg"
    try:
        url = f"https://source.unsplash.com/1600x900/?{bg_keyword.replace(' ', ',')}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback to a solid gray rectangle if download fails
        fallback = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        fallback.fill.solid()
        fallback.fill.fore_color.rgb = RGBColor(200, 200, 200)
        fallback.line.fill.background()

    if os.path.exists(img_path):
        # Insert image taking up the right side (width = 7.5, left = 5.833)
        # We will actually make it cover the whole slide and mask it with the white polygon for safety
        pic = slide.shapes.add_picture(img_path, 0, 0, width=Inches(13.333), height=Inches(7.5))

    # === Layer 2: The Angled White Polygon Overlay (Left Side) ===
    # Coordinates: Top-Left(0,0), Bottom-Left(0,7.5), Bottom-Right(8.0, 7.5), Top-Right(6.0, 0)
    ff_builder = slide.shapes.build_freeform(0, 0)
    ff_builder.add_line_segments([
        (0, Inches(7.5)), 
        (Inches(8.2), Inches(7.5)),  # Bottom edge reaches further right
        (Inches(5.8), 0),            # Top edge is narrower
        (0, 0)
    ])
    mask_shape = ff_builder.convert_to_shape()
    mask_shape.fill.solid()
    mask_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    mask_shape.line.fill.background()

    # === Layer 3: Dotted Grid Micro-texture ===
    dot_size = Inches(0.06)
    spacing = Inches(0.18)
    start_x = Inches(6.0)
    start_y = Inches(4.5)
    rows, cols = 16, 4
    
    for r in range(rows):
        for c in range(cols):
            x = start_x + (c * spacing)
            y = start_y + (r * spacing)
            dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, dot_size, dot_size)
            dot.fill.solid()
            dot.fill.fore_color.rgb = accent_rgb
            dot.line.fill.background()

    # === Layer 4: Geometric Accent Triangles ===
    # Top left small accent arrows
    for i in range(3):
        tri = slide.shapes.add_shape(
            MSO_SHAPE.ISOSCELES_TRIANGLE, 
            Inches(0.5 + (i * 0.4)), Inches(0.5), Inches(0.3), Inches(0.35)
        )
        tri.rotation = 90  # Pointing right
        tri.fill.solid()
        tri.fill.fore_color.rgb = accent_rgb if i == 0 else RGBColor(220, 240, 235)
        tri.line.fill.background()
        
        # Adding a border to one for stylistic variety as seen in tutorial
        if i > 0:
            tri.fill.background()
            tri.line.color.rgb = accent_rgb
            tri.line.width = Pt(2)

    # Bottom left massive colored corner (Right Triangle)
    corner_tri = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_TRIANGLE, 
        0, Inches(5.5), Inches(2.0), Inches(2.0)
    )
    corner_tri.rotation = 270 # Position to sit flush bottom left
    corner_tri.fill.solid()
    corner_tri.fill.fore_color.rgb = accent_rgb
    corner_tri.line.fill.background()

    # === Layer 5: Typography ===
    # Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.5), Inches(2.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Georgia' # Standard cross-platform serif fallback for Sitka Display
    p.font.size = Pt(65)
    p.font.bold = True
    p.font.color.rgb = dark_text_rgb
    p.alignment = PP_ALIGN.LEFT

    # Subtitle / Body
    body_box = slide.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(3.5), Inches(1.5))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.name = 'Arial' # Standard cross-platform sans-serif
    p_body.font.size = Pt(16)
    p_body.font.color.rgb = RGBColor(80, 80, 80)
    p_body.alignment = PP_ALIGN.LEFT

    # Cleanup temp image
    if os.path.exists(img_path):
        os.remove(img_path)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
