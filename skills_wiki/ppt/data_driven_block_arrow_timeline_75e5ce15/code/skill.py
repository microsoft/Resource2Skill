def create_slide(
    output_pptx_path: str,
    title_text: str = "Transition of\nAnnual Advertising\nExpenditures",
    data_points: list = None,
    arrow_color: tuple = (156, 204, 101),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Data-Driven Block Arrow Timeline.
    Generates two slides to demonstrate a "Before and After" sequence ready for Morph transitions.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    # Default data payload demonstrating growth
    if data_points is None:
        data_points = [
            {"period": "1995 - 2000", "value": "$5B", "label": "Internet\nAdvertising\n(Display)", "height_ratio": 0.4},
            {"period": "2000 - 2010", "value": "$30B", "label": "Search\nAnd\nOnline", "height_ratio": 0.7},
            {"period": "2010 +", "value": "$35B+", "label": "Call\nAdvertising\nModels", "height_ratio": 1.0}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # ==========================================================
    # SLIDE 1: The Core Arrow Growth Timeline
    # ==========================================================
    slide1 = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 1. Layered Typographic Title
    title_box = slide1.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(4.5), Inches(3.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    lines = title_text.split('\n')
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        if i == 0:
            # First line: lighter, thinner (simulated by non-bold)
            p.font.size = Pt(36)
            p.font.color.rgb = RGBColor(160, 160, 160)
            p.font.bold = False
        else:
            # Subsequent lines: dark, bold emphasis
            p.font.size = Pt(32)
            p.font.color.rgb = RGBColor(40, 40, 40)
            p.font.bold = True

    # 2. Block Arrow Data Containers
    num_arrows = len(data_points)
    start_x = 4.0
    arrow_w = 2.0
    spacing = 1.0
    baseline_y = 6.5  # Acts as the X-axis anchor
    max_h = 4.5       # Maximum height for the 1.0 ratio arrow

    for i, dp in enumerate(data_points):
        x = Inches(start_x + i * (arrow_w + spacing))
        h = Inches(max_h * dp["height_ratio"])
        y = Inches(baseline_y) - h
        w = Inches(arrow_w)
        
        # Add Upward Arrow
        shape = slide1.shapes.add_shape(MSO_SHAPE.UP_ARROW, x, y, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*arrow_color)
        shape.line.color.rgb = RGBColor(*arrow_color) # Seamless edge
        
        # Format internal text (Data Value + Label)
        text_frame = shape.text_frame
        text_frame.word_wrap = True
        
        p_val = text_frame.paragraphs[0]
        p_val.alignment = PP_ALIGN.CENTER
        p_val.text = dp["value"] + "\n"
        p_val.font.size = Pt(28)
        p_val.font.bold = True
        p_val.font.color.rgb = RGBColor(255, 255, 255)
        
        p_desc = text_frame.add_paragraph()
        p_desc.alignment = PP_ALIGN.CENTER
        p_desc.text = dp["label"]
        p_desc.font.size = Pt(14)
        p_desc.font.color.rgb = RGBColor(255, 255, 255)

        # 3. Timeline Period Label (Below Baseline)
        tb = slide1.shapes.add_textbox(x - Inches(0.5), Inches(baseline_y + 0.1), w + Inches(1.0), Inches(0.6))
        p_per = tb.text_frame.paragraphs[0]
        p_per.alignment = PP_ALIGN.CENTER
        p_per.text = dp["period"]
        p_per.font.size = Pt(14)
        p_per.font.color.rgb = RGBColor(120, 120, 120)

    # ==========================================================
    # SLIDE 2: The Summary Transition (Morph Ready)
    # Replicates the tutorial's horizontal transition shift
    # ==========================================================
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Simplified Title mapped to top-left
    title_box2 = slide2.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(4.0), Inches(3.0))
    p_t = title_box2.text_frame.paragraphs[0]
    p_t.text = title_text.replace('\n', ' ')
    p_t.font.size = Pt(24)
    p_t.font.color.rgb = RGBColor(160, 160, 160)
    p_t.font.bold = True

    # Shrunk, horizontal versions of the timeline data
    for i, dp in enumerate(data_points):
        x = Inches(0.5)
        w = Inches(2.5 * dp["height_ratio"]) # Width now acts as the bar chart
        h = Inches(0.6)
        y = Inches(3.0 + i * 1.0)
        
        shape = slide2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*arrow_color)
        shape.line.color.rgb = RGBColor(*arrow_color)
        
        # Compact internal label
        tf_s = shape.text_frame
        p_s = tf_s.paragraphs[0]
        p_s.text = dp["period"]
        p_s.font.size = Pt(10)
        p_s.font.bold = True
        p_s.font.color.rgb = RGBColor(255, 255, 255)
        p_s.alignment = PP_ALIGN.CENTER

    # Large Horizontal Summary Arrow (The "Takeaway")
    big_arrow = slide2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.0), Inches(3.5), Inches(8.5), Inches(2.0))
    big_arrow.fill.solid()
    big_arrow.fill.fore_color.rgb = RGBColor(*arrow_color)
    big_arrow.line.color.rgb = RGBColor(*arrow_color)
    
    p_big = big_arrow.text_frame.paragraphs[0]
    p_big.text = "We manage an advertising budget of more than\n$250 Million"
    p_big.font.size = Pt(28)
    p_big.font.bold = True
    p_big.font.color.rgb = RGBColor(255, 255, 255)
    p_big.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
