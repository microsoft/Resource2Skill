def create_slide(
    output_pptx_path: str,
    title_text: str = "Strategic Management Consultants",
    author_text: str = "Chelsea Seburn\nDepartment of Business: John F. Kennedy University\nSTM 252: Strategic Management\nDr. Keith Wade\nFebruary 5, 2021",
    accent_color: tuple = (31, 73, 125),  # Corporate Navy Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Corporate Geometric Split-Panel & Academic Formatting' visual effect.
    Generates a 3-slide deck demonstrating Title, Content, and Reference formatting.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    # Widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define Theme Colors
    color_accent = RGBColor(*accent_color)
    color_text_dark = RGBColor(60, 60, 60)
    color_text_light = RGBColor(255, 255, 255)
    font_name = "Calibri"

    # ==========================================
    # SLIDE 1: Title Slide (Centered Academic)
    # ==========================================
    slide_layout_blank = prs.slide_layouts[6]
    slide_title = prs.slides.add_slide(slide_layout_blank)

    # Decorative Top Banner
    top_banner = slide_title.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), Inches(13.333), Inches(0.5)
    )
    top_banner.fill.solid()
    top_banner.fill.fore_color.rgb = color_accent
    top_banner.line.fill.background()

    # Title Text
    title_box = slide_title.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.333), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = font_name
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = color_text_dark
    p.alignment = PP_ALIGN.CENTER

    # Author/Meta Text
    meta_box = slide_title.shapes.add_textbox(Inches(2), Inches(3.5), Inches(9.333), Inches(3))
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True
    
    for line in author_text.split('\n'):
        p = tf_meta.add_paragraph()
        p.text = line
        p.font.name = font_name
        p.font.size = Pt(20)
        p.font.color.rgb = color_text_dark
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 2: Body Slide (Geometric Split-Panel)
    # ==========================================
    slide_body = prs.slides.add_slide(slide_layout_blank)

    # Left Anchor Panel (30% width)
    left_panel = slide_body.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), Inches(4), Inches(7.5)
    )
    left_panel.fill.solid()
    left_panel.fill.fore_color.rgb = color_accent
    left_panel.line.fill.background()

    # Heading inside Anchor Panel
    head_box = slide_body.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(3), Inches(3))
    tf_head = head_box.text_frame
    tf_head.word_wrap = True
    p = tf_head.paragraphs[0]
    p.text = "Company History"
    p.font.name = font_name
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = color_text_light
    p.alignment = PP_ALIGN.LEFT

    # Content Area (Right 70%)
    content_box = slide_body.shapes.add_textbox(Inches(4.5), Inches(0.5), Inches(8.333), Inches(6.5))
    tf_content = content_box.text_frame
    tf_content.word_wrap = True
    
    bullets = [
        "Founded by Jeff Bezos in 1995",
        "Started as an online bookstore",
        "Year one reached 1,000,000 in sales",
        "Current market value is extremely high",
        "Largest global e-commerce company",
        "Offers a wide variety of products and services"
    ]
    
    for item in bullets:
        p = tf_content.add_paragraph()
        p.text = item
        p.font.name = font_name
        p.font.size = Pt(24)
        p.font.color.rgb = color_text_dark
        p.level = 0
        p.space_after = Pt(24) # Generous spacing for readability

    # ==========================================
    # SLIDE 3: Reference Slide (Hanging Indent)
    # ==========================================
    slide_ref = prs.slides.add_slide(slide_layout_blank)

    # Simple Top Accent Line for continuity
    ref_line = slide_ref.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), Inches(13.333), Inches(0.2)
    )
    ref_line.fill.solid()
    ref_line.fill.fore_color.rgb = color_accent
    ref_line.line.fill.background()

    # Reference Heading
    ref_head_box = slide_ref.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(1))
    tf_ref_head = ref_head_box.text_frame
    p = tf_ref_head.paragraphs[0]
    p.text = "References"
    p.font.name = font_name
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = color_text_dark
    p.alignment = PP_ALIGN.CENTER

    # Reference List with Hanging Indents
    ref_box = slide_ref.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.333), Inches(5.5))
    tf_ref = ref_box.text_frame
    tf_ref.word_wrap = True
    
    references = [
        "Cuofano et al., (2019, March 20). Amazon Mission Statement and Vision Statement In A Nutshell. FourWeekMBA. https://fourweekmba.com/amazon-vision-statement-mission-statement/",
        "Farfan, B. (2019, November 20). Amazon's Mission Statement. The balance everyday. https://www.thebalanceeveryday.com/amazon-mission-statement-4068548",
        "Feiner, Lauren. (2019, January 7). Amazon is the most valuable public company in the world after passing Microsoft. CNBC. https://www.cnbc.com/2019/01/07/amazon-passes-microsoft-market-value-becomes-largest.html"
    ]
    
    for ref in references:
        p = tf_ref.add_paragraph()
        p.text = ref
        p.font.name = font_name
        p.font.size = Pt(16)
        p.font.color.rgb = color_text_dark
        p.space_after = Pt(14)
        
        # *** CORE MECHANISM: APA Hanging Indent Formula ***
        pf = p.paragraph_format
        pf.left_indent = Inches(0.5)
        pf.first_line_indent = Inches(-0.5)

    prs.save(output_pptx_path)
    return output_pptx_path
