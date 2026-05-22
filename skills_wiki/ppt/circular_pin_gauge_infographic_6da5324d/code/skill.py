def create_slide(
    output_pptx_path: str,
    title_text: str = "I N F O G R A P H I C S",
    subtitle_text: str = "Here you have to add some subtitle text by your own and replace with this\nsample text this is simple.",
    data_percentages: list = [38, 43, 68],
    **kwargs
) -> str:
    """
    Creates an infographic slide with three circular pin gauges.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Color Palette ---
    BG_COLOR = (35, 46, 62)
    PIN_COLOR = (44, 58, 78)
    ARC_COLOR = (255, 192, 0)
    TEXT_WHITE = (255, 255, 255)
    TEXT_GRAY = (156, 163, 175)
    RED_ACCENT = (239, 68, 68)

    # --- Helper Functions ---
    def add_centered_text(left, top, width, height, text, font_size, font_color, bold=False):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.text = text
        tf.margin_left = Pt(0)
        tf.margin_right = Pt(0)
        tf.margin_top = Pt(0)
        tf.margin_bottom = Pt(0)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        font = p.font
        font.size = Pt(font_size)
        font.color.rgb = RGBColor(*font_color)
        font.bold = bold
        return txBox

    def set_arc_angles(shape, start_deg, sweep_deg):
        # PowerPoint OpenXML uses 1/60000th of a degree
        start_val = int((start_deg % 360) * 60000)
        end_deg = start_deg + sweep_deg
        end_val = int((end_deg % 360) * 60000)

        prstGeom = shape.element.find('.//a:prstGeom', shape.element.nsmap)
        if prstGeom is not None:
            avLst = prstGeom.find('.//a:avLst', shape.element.nsmap)
            if avLst is None:
                avLst = parse_xml('<a:avLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
                prstGeom.append(avLst)
            for child in list(avLst):
                avLst.remove(child)
            # adj1 = start angle, adj2 = end angle
            avLst.append(parse_xml(f'<a:gd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="adj1" fmla="val {start_val}"/>'))
            avLst.append(parse_xml(f'<a:gd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="adj2" fmla="val {end_val}"/>'))

    # --- Step 1: Draw Background ---
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*BG_COLOR)
    bg.line.color.rgb = RGBColor(*BG_COLOR)

    # --- Step 2: Add Headers ---
    add_centered_text(Inches(0), Inches(0.8), prs.slide_width, Inches(0.6), title_text, 32, TEXT_WHITE, bold=True)
    add_centered_text(Inches(2), Inches(1.5), Inches(9.333), Inches(0.6), subtitle_text, 12, TEXT_GRAY)

    # --- Step 3: Draw Nodes ---
    centers_x = [2.66, 6.66, 10.66]
    cy = 3.8  # Central Y axis for the pins

    # Geometric math for a perfect location pin (Circle + Tangent Triangle)
    R = 1.3  # Radius of the main pin head
    y_t = 2.2  # Distance from center to the sharp tip
    y_tangent = (R**2) / y_t  # Y-coordinate where triangle touches circle tangentially (0.768)
    x_tangent = (R**2 - y_tangent**2)**0.5  # X-coordinate for tangent (1.049)
    tri_width = 2 * x_tangent  # Width of triangle base (2.098)
    tri_height = y_t - y_tangent  # Height of triangle (1.432)

    for i in range(3):
        cx = centers_x[i]
        pct = data_percentages[i] if i < len(data_percentages) else 50

        # 3a. Pin Head (Outer Circle)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - R), Inches(cy - R), Inches(2 * R), Inches(2 * R))
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(*PIN_COLOR)
        circle.line.color.rgb = RGBColor(*PIN_COLOR)

        # 3b. Pin Tail (Inverted Triangle)
        # We overlap by 0.02 to prevent anti-aliasing hairline gaps between shapes
        overlap = 0.02
        triangle = slide.shapes.add_shape(
            MSO_SHAPE.ISOSCELES_TRIANGLE,
            Inches(cx - tri_width / 2), Inches(cy + y_tangent - overlap),
            Inches(tri_width), Inches(tri_height + overlap)
        )
        triangle.rotation = 180
        triangle.fill.solid()
        triangle.fill.fore_color.rgb = RGBColor(*PIN_COLOR)
        triangle.line.color.rgb = RGBColor(*PIN_COLOR)

        # 3c. Inner Hole (Mask using background color)
        r_inner = 0.9
        hole = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r_inner), Inches(cy - r_inner), Inches(2 * r_inner), Inches(2 * r_inner))
        hole.fill.solid()
        hole.fill.fore_color.rgb = RGBColor(*BG_COLOR)
        hole.line.color.rgb = RGBColor(*BG_COLOR)

        # 3d. Progress Arc
        r_arc = 1.0  # Centers exactly between the inner hole edge and the outer pin edge
        arc = slide.shapes.add_shape(MSO_SHAPE.ARC, Inches(cx - r_arc), Inches(cy - r_arc), Inches(2 * r_arc), Inches(2 * r_arc))
        arc.line.color.rgb = RGBColor(*ARC_COLOR)
        arc.line.width = Pt(15)  # Creates a thick ring
        
        # Calculate sweep: Top of circle in PPT is 270 degrees
        start_deg = 270
        sweep_deg = pct * 360 / 100
        set_arc_angles(arc, start_deg, sweep_deg)

        # 3e. Text Content
        # Main Number
        add_centered_text(Inches(cx - 1), Inches(cy - 0.3), Inches(2), Inches(0.6), str(pct), 40, TEXT_WHITE, bold=True)
        # PERCENT Label
        add_centered_text(Inches(cx - 1), Inches(cy + 0.35), Inches(2), Inches(0.3), "PERCENT", 10, TEXT_GRAY, bold=True)

        # 3f. Accent Elements
        # Small Red Directional Triangle
        red_tri = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(cx - 0.15), Inches(cy + y_t + 0.1), Inches(0.3), Inches(0.2))
        red_tri.rotation = 180
        red_tri.fill.solid()
        red_tri.fill.fore_color.rgb = RGBColor(*RED_ACCENT)
        red_tri.line.color.rgb = RGBColor(*RED_ACCENT)

        # Bottom Text Label
        add_centered_text(Inches(cx - 1), Inches(cy + y_t + 0.4), Inches(2), Inches(0.3), "TEXT HERE", 11, TEXT_WHITE, bold=True)

    prs.save(output_pptx_path)
    return output_pptx_path
