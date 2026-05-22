def create_slide(
    output_pptx_path: str,
    title_text: str = "Aspect Ratio Test",
    body_text: str = "(Should appear circular)",
    bg_palette: str = "dark",  # Not downloaded, generated via native shape for purity
    accent_color: tuple = (0, 191, 255),  # Cyan
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Technical Blueprint Calibration Pattern' visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.dml import MSO_LINE
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    # Force 16:9 Aspect Ratio
    w, h = Inches(13.333), Inches(7.5)
    prs.slide_width = w
    prs.slide_height = h
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    # Draw a solid black background base for guaranteed reproducibility
    bg_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, w, h)
    bg_box.fill.solid()
    bg_box.fill.fore_color.rgb = RGBColor(0, 0, 0)
    bg_box.line.fill.background()

    # === Layer 2: Visual Effect (Blueprint Geometry) ===
    accent_rgb = RGBColor(*accent_color)
    margin = Inches(0.4)
    
    # 1. Outer 16:9 Safe Area Box
    outer_w = w - (margin * 2)
    outer_h = h - (margin * 2)
    outer_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, margin, margin, outer_w, outer_h)
    outer_box.fill.background()  # Transparent inside
    outer_box.line.color.rgb = accent_rgb
    outer_box.line.width = Pt(1.5)
    
    # Label for Outer Box
    tb_169 = slide.shapes.add_textbox(margin, h - margin - Inches(0.4), Inches(2), Inches(0.4))
    tf_169 = tb_169.text_frame
    p = tf_169.paragraphs[0]
    p.text = "16:9"
    p.font.size = Pt(12)
    p.font.color.rgb = accent_rgb
    p.font.bold = True

    # 2. Inner 4:3 Area Box
    inner_h = outer_h
    inner_w = inner_h * (4.0 / 3.0)  # Calculate exact 4:3 width based on height
    inner_l = (w - inner_w) / 2
    inner_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, inner_l, margin, inner_w, inner_h)
    inner_box.fill.background()
    inner_box.line.color.rgb = accent_rgb
    inner_box.line.width = Pt(1.5)
    inner_box.line.dash_style = MSO_LINE.DASH  # Dashed line
    
    # Label for Inner Box
    tb_43 = slide.shapes.add_textbox(inner_l, h - margin - Inches(0.4), Inches(2), Inches(0.4))
    tf_43 = tb_43.text_frame
    p_43 = tf_43.paragraphs[0]
    p_43.text = "4:3"
    p_43.font.size = Pt(12)
    p_43.font.color.rgb = accent_rgb
    p_43.font.bold = True

    # 3. Center Target Circle
    circle_d = Inches(4.0)
    circle_l = (w - circle_d) / 2
    circle_t = (h - circle_d) / 2
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, circle_l, circle_t, circle_d, circle_d)
    circle.fill.background()
    circle.line.color.rgb = accent_rgb
    circle.line.width = Pt(2.5)

    # === Layer 3: Text & Content ===
    # Center text inside the target circle
    tf = circle.text_frame
    tf.word_wrap = True
    
    # Title
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    p_title.alignment = PP_ALIGN.CENTER
    
    # Subtitle / Body
    if body_text:
        p_body = tf.add_paragraph()
        p_body.text = body_text
        p_body.font.size = Pt(16)
        p_body.font.color.rgb = RGBColor(200, 200, 200)
        p_body.alignment = PP_ALIGN.CENTER

    # Optional Title at the very top (outside the boxes)
    title_box = slide.shapes.add_textbox(margin, Inches(0.1), w, Inches(0.5))
    tf_top = title_box.text_frame
    p_top = tf_top.paragraphs[0]
    p_top.text = "Widescreen Test Pattern (16:9)"
    p_top.font.size = Pt(16)
    p_top.font.bold = True
    p_top.font.color.rgb = RGBColor(255, 255, 255)
    p_top.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
