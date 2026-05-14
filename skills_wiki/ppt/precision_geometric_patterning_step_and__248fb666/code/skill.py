def create_slide(
    output_pptx_path: str,
    title_text: str = "PRECISION GEOMETRY",
    subtitle_text: str = "Simulating Ctrl+D Arrays & Format Painting",
    bg_dot_color: tuple = (226, 232, 240),      # Subtle slate gray-blue
    shape_fill_color: tuple = (255, 192, 0),    # Golden yellow (from video demo)
    shape_line_color: tuple = (0, 0, 0),        # Black
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the geometric arrays, proportional shapes, 
    and format-painting style demonstrated in the shortcut tutorial.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    # Use standard 16:9 widescreen aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ==========================================
    # Layer 1: "Ctrl+D" Step-and-Repeat Texture
    # ==========================================
    # We simulate the user rapidly pressing Ctrl+D to create a dot grid background.
    dot_size = Inches(0.08)
    grid_spacing_x = Inches(0.4)
    grid_spacing_y = Inches(0.4)
    
    rows = int(prs.slide_height / grid_spacing_y) + 1
    cols = int(prs.slide_width / grid_spacing_x) + 1
    
    for row in range(rows):
        for col in range(cols):
            x = col * grid_spacing_x
            y = row * grid_spacing_y
            dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, dot_size, dot_size)
            dot.fill.solid()
            dot.fill.fore_color.rgb = RGBColor(*bg_dot_color)
            dot.line.fill.background() # No outline

    # ==========================================
    # Layer 2: Proportional "Shift" Primitives
    # ==========================================
    # Simulating Shift+Draw (Perfect 1:1 aspect ratio) and orthogonal alignment
    
    shape_size = Inches(2.2)
    y_pos = Inches(3.5)
    
    # Calculate equidistant X positions for 3 shapes
    spacing = (prs.slide_width - (3 * shape_size)) / 4
    x1 = spacing
    x2 = spacing * 2 + shape_size
    x3 = spacing * 3 + shape_size * 2

    s1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x1, y_pos, shape_size, shape_size)
    s2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, x2, y_pos, shape_size, shape_size)
    s3 = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, x3, y_pos, shape_size, shape_size)

    # ==========================================
    # Layer 3: "Ctrl+Shift+C / V" Format Painter
    # ==========================================
    # We define a style once and apply it to all, simulating format pasting.
    def apply_copied_format(shape):
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*shape_fill_color)
        shape.line.color.rgb = RGBColor(*shape_line_color)
        shape.line.width = Pt(4.5) # Thick border as shown in formatting demo
        
        # Add a subtle shadow for depth
        shadow = shape.shadow
        shadow.inherit = False
        shadow.distance = Pt(5)
        shadow.angle = 45
        shadow.blur_radius = Pt(3)
        shadow.color.color_type = RGBColor(0, 0, 0)
        shadow.alpha = 70

    apply_copied_format(s1)
    apply_copied_format(s2)
    apply_copied_format(s3)

    # ==========================================
    # Layer 4: Title Container
    # ==========================================
    # Add a modern overlay title bar to frame the geometry
    title_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0.8), prs.slide_width, Inches(1.8))
    title_bg.fill.solid()
    title_bg.fill.fore_color.rgb = RGBColor(13, 17, 28) # Dark Navy background for text
    title_bg.line.fill.background()

    # Title Text
    tx_box = slide.shapes.add_textbox(Inches(0), Inches(0.9), prs.slide_width, Inches(1))
    tf = tx_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text.upper()
    run.font.bold = True
    run.font.size = Pt(44)
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.name = "Arial"

    # Subtitle Text
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = subtitle_text
    run2.font.size = Pt(20)
    run2.font.color.rgb = RGBColor(0, 191, 255) # Cyan accent
    run2.font.name = "Arial"

    prs.save(output_pptx_path)
    return output_pptx_path
