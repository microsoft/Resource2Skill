def create_slide(
    output_pptx_path: str,
    pro_title: str = "PROS",
    con_title: str = "CONS",
    pro_points: list = ["Clarity and focus", "Saves significant time", "Aids quick decision-making"],
    con_points: list = ["Can look generic", "Risk of oversimplification", "May hide weak thinking"],
    pro_color_rgb: tuple = (46, 179, 74),
    con_color_rgb: tuple = (217, 30, 24),
    font_color_rgb: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a classic Pros and Cons dichotomy decision panel.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        pro_title (str): The title for the positive (left) panel.
        con_title (str): The title for the negative (right) panel.
        pro_points (list): A list of strings for the positive panel's bullet points.
        con_points (list): A list of strings for the negative panel's bullet points.
        pro_color_rgb (tuple): The RGB background color for the positive panel.
        con_color_rgb (tuple): The RGB background color for the negative panel.
        font_color_rgb (tuple): The RGB color for all text and icons.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 aspect ratio
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Define common dimensions
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    panel_width = slide_width / 2

    # === Layer 1: Background Panels ===

    # Pro Panel (Left, Green)
    pro_panel = slide.shapes.add_shape(1, 0, 0, panel_width, slide_height)  # 1 is autoshape for rectangle
    pro_panel.fill.solid()
    pro_panel.fill.fore_color.rgb = RGBColor(*pro_color_rgb)
    pro_panel.line.fill.background()

    # Con Panel (Right, Red)
    con_panel = slide.shapes.add_shape(1, panel_width, 0, panel_width, slide_height)
    con_panel.fill.solid()
    con_panel.fill.fore_color.rgb = RGBColor(*con_color_rgb)
    con_panel.line.fill.background()

    # === Layer 2: Text and Icons ===

    # --- Pro Side Elements ---
    # Pro Title
    pro_title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), panel_width - Inches(1), Inches(1.0))
    tf_pro_title = pro_title_box.text_frame
    tf_pro_title.text = pro_title
    p_pro_title = tf_pro_title.paragraphs[0]
    p_pro_title.font.name = 'Arial Black'
    p_pro_title.font.size = Pt(44)
    p_pro_title.font.bold = True
    p_pro_title.font.color.rgb = RGBColor(*font_color_rgb)
    p_pro_title.alignment = PP_ALIGN.CENTER
    
    # Pro Icon (Checkmark)
    pro_icon_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), panel_width - Inches(1), Inches(1.5))
    tf_pro_icon = pro_icon_box.text_frame
    tf_pro_icon.text = "\u2714" # Unicode for Heavy Check Mark
    p_pro_icon = tf_pro_icon.paragraphs[0]
    p_pro_icon.font.name = 'Segoe UI Symbol'
    p_pro_icon.font.size = Pt(80)
    p_pro_icon.font.color.rgb = RGBColor(*font_color_rgb)
    p_pro_icon.alignment = PP_ALIGN.CENTER
    
    # Pro Bullet Points
    pro_points_box = slide.shapes.add_textbox(Inches(0.75), Inches(3.0), panel_width - Inches(1.5), Inches(4.0))
    tf_pro_points = pro_points_box.text_frame
    tf_pro_points.clear() # clear the default paragraph
    for point in pro_points:
        p = tf_pro_points.add_paragraph()
        p.text = point
        p.font.name = 'Arial'
        p.font.size = Pt(22)
        p.font.color.rgb = RGBColor(*font_color_rgb)
        p.level = 0
    tf_pro_points.margin_left = Inches(0.25)
    
    # --- Con Side Elements ---
    # Con Title
    con_title_box = slide.shapes.add_textbox(panel_width + Inches(0.5), Inches(0.5), panel_width - Inches(1), Inches(1.0))
    tf_con_title = con_title_box.text_frame
    tf_con_title.text = con_title
    p_con_title = tf_con_title.paragraphs[0]
    p_con_title.font.name = 'Arial Black'
    p_con_title.font.size = Pt(44)
    p_con_title.font.bold = True
    p_con_title.font.color.rgb = RGBColor(*font_color_rgb)
    p_con_title.alignment = PP_ALIGN.CENTER

    # Con Icon (X Mark)
    con_icon_box = slide.shapes.add_textbox(panel_width + Inches(0.5), Inches(1.5), panel_width - Inches(1), Inches(1.5))
    tf_con_icon = con_icon_box.text_frame
    tf_con_icon.text = "\u2718" # Unicode for Heavy Ballot X
    p_con_icon = tf_con_icon.paragraphs[0]
    p_con_icon.font.name = 'Segoe UI Symbol'
    p_con_icon.font.size = Pt(80)
    p_con_icon.font.color.rgb = RGBColor(*font_color_rgb)
    p_con_icon.alignment = PP_ALIGN.CENTER

    # Con Bullet Points
    con_points_box = slide.shapes.add_textbox(panel_width + Inches(0.75), Inches(3.0), panel_width - Inches(1.5), Inches(4.0))
    tf_con_points = con_points_box.text_frame
    tf_con_points.clear()
    for point in con_points:
        p = tf_con_points.add_paragraph()
        p.text = point
        p.font.name = 'Arial'
        p.font.size = Pt(22)
        p.font.color.rgb = RGBColor(*font_color_rgb)
        p.level = 0
    tf_con_points.margin_left = Inches(0.25)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("dichotomy_decision_panel.pptx")
