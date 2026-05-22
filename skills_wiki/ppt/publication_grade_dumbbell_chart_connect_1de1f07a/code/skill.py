def create_slide(
    output_pptx_path: str,
    title_text: str = "Employee Engagement Scores",
    body_text: str = "Comparing internal departmental survey results: 2023 vs 2024",
    accent_color: tuple = (217, 58, 70),  # The Economist Red
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Publication-Grade Dumbbell Chart.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Default Data Structure ===
    data = kwargs.get("chart_data", [
        {"cat": "Operations", "past": 85, "present": 78},
        {"cat": "HR", "past": 75, "present": 80},
        {"cat": "Customer Service", "past": 80, "present": 70},
        {"cat": "Finance", "past": 60, "present": 70},
        {"cat": "Sales", "past": 60, "present": 65},
        {"cat": "IT", "past": 45, "present": 55},
        {"cat": "Procurement", "past": 32, "present": 55},
        {"cat": "Production", "past": 20, "present": 35}
    ])

    # === Color Palette ===
    c_accent = RGBColor(*accent_color)
    c_past = RGBColor(166, 166, 166)      # Muted Gray
    c_line = RGBColor(217, 217, 217)      # Light Gray
    c_text_dark = RGBColor(38, 38, 38)    # Near Black
    c_text_light = RGBColor(115, 115, 115)# Gray text
    c_grid = RGBColor(235, 235, 235)      # Very faint gridlines

    # === Layout Parameters ===
    margin_left = Inches(2.5)
    margin_top = Inches(2.2)
    chart_width = Inches(9.5)
    chart_height = Inches(4.5)
    
    # === Layer 1: Publication Header ===
    # Editorial signature red block
    red_block = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.5), Inches(0.4), Inches(0.08))
    red_block.fill.solid()
    red_block.fill.fore_color.rgb = c_accent
    red_block.line.fill.background()

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.7), Inches(10), Inches(0.6))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = c_text_dark

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.4), Inches(1.2), Inches(10), Inches(0.4))
    p2 = sub_box.text_frame.paragraphs[0]
    p2.text = body_text
    p2.font.size = Pt(14)
    p2.font.color.rgb = c_text_light

    # === Layer 2: Grid & X-Axis ===
    min_val, max_val = 0, 100
    steps = [0, 20, 40, 60, 80, 100]
    
    for step in steps:
        x_pos = margin_left + (step / 100.0) * chart_width
        
        # Vertical gridline
        gridline = slide.shapes.add_connector(1, x_pos, margin_top, x_pos, margin_top + chart_height)
        gridline.line.color.rgb = c_grid
        gridline.line.width = Pt(1)
        
        # Axis label
        lbl_box = slide.shapes.add_textbox(x_pos - Inches(0.5), margin_top - Inches(0.4), Inches(1), Inches(0.3))
        p = lbl_box.text_frame.paragraphs[0]
        p.text = f"{step}%"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.color.rgb = c_text_light

    # === Layer 3: Data Plotting (Dumbbells) ===
    num_items = len(data)
    row_height = chart_height / num_items
    circle_radius = Inches(0.08)

    for i, item in enumerate(data):
        # Y position is centered in its row slot
        y_pos = margin_top + (i * row_height) + (row_height / 2)

        # 1. Category Label (Y-Axis)
        cat_box = slide.shapes.add_textbox(Inches(0.2), y_pos - Inches(0.18), margin_left - Inches(0.4), Inches(0.3))
        p = cat_box.text_frame.paragraphs[0]
        p.text = item["cat"]
        p.alignment = PP_ALIGN.RIGHT
        p.font.size = Pt(12)
        p.font.color.rgb = c_text_dark

        # Calculate X positions
        x_past = margin_left + (item["past"] / 100.0) * chart_width
        x_present = margin_left + (item["present"] / 100.0) * chart_width

        # 2. Connecting Line (Draw first so it goes behind circles)
        conn = slide.shapes.add_connector(1, x_past, y_pos, x_present, y_pos)
        conn.line.color.rgb = c_line
        conn.line.width = Pt(2.5)

        # 3. Past Circle (Gray)
        c_past_shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, x_past - circle_radius, y_pos - circle_radius, circle_radius*2, circle_radius*2
        )
        c_past_shape.fill.solid()
        c_past_shape.fill.fore_color.rgb = c_past
        c_past_shape.line.fill.background()

        # 4. Present Circle (Accent)
        c_pres_shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, x_present - circle_radius, y_pos - circle_radius, circle_radius*2, circle_radius*2
        )
        c_pres_shape.fill.solid()
        c_pres_shape.fill.fore_color.rgb = c_accent
        c_pres_shape.line.fill.background()

        # 5. Integrated Legend / Data Labels (Only on the first row)
        if i == 0:
            # Determine which is left and which is right to avoid text collision
            left_val = min(item["past"], item["present"])
            right_val = max(item["past"], item["present"])
            
            # Past Label
            lbl_past = slide.shapes.add_textbox(x_past - Inches(0.5), y_pos - Inches(0.45), Inches(1), Inches(0.3))
            p_past = lbl_past.text_frame.paragraphs[0]
            p_past.text = str(item["past"])
            p_past.alignment = PP_ALIGN.CENTER
            p_past.font.size = Pt(12)
            p_past.font.bold = True
            p_past.font.color.rgb = c_past
            
            # Present Label
            lbl_pres = slide.shapes.add_textbox(x_present - Inches(0.5), y_pos - Inches(0.45), Inches(1), Inches(0.3))
            p_pres = lbl_pres.text_frame.paragraphs[0]
            p_pres.text = str(item["present"])
            p_pres.alignment = PP_ALIGN.CENTER
            p_pres.font.size = Pt(12)
            p_pres.font.bold = True
            p_pres.font.color.rgb = c_accent

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
