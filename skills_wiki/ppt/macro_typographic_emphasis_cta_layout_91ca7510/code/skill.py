def create_slide(
    output_pptx_path: str,
    pre_title: str = "HOW TO",
    main_title: str = "END",
    post_title: str = "A PRESENTATION",
    cta_1: str = "FOLLOW US\nCLICK HERE",
    cta_2: str = "MORE INFO\nCLICK HERE",
    url_text: str = "www.expertacademy.be",
    accent_color: tuple = (30, 90, 150),
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the "Macro Typographic & CTA" visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Radial Gradient Background (via lxml injection) ===
    bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_rect.line.fill.background()
    spPr = bg_rect._element.spPr

    # Remove default solid fill if present
    for child in list(spPr):
        if child.tag.endswith('Fill'):
            spPr.remove(child)

    # Inject native PowerPoint radial gradient (center white, edges light grey)
    grad_xml = """
    <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rotWithShape="1">
        <a:gsLst>
            <a:gs pos="0"><a:srgbClr val="FFFFFF"/></a:gs>
            <a:gs pos="100000"><a:srgbClr val="DCE0E5"/></a:gs>
        </a:gsLst>
        <a:path path="rect">
            <a:fillToRect l="50000" t="50000" r="50000" b="50000"/>
        </a:path>
    </a:gradFill>
    """
    spPr.insert(0, parse_xml(grad_xml))

    # === Layer 2: Massive Typographic Block ===
    # Top 60% of the slide
    tb = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    # Pre-title
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.line_spacing = 0.85
    run1 = p1.add_run()
    run1.text = pre_title + "\n"
    run1.font.size = Pt(54)
    run1.font.bold = True
    run1.font.name = "Arial"
    run1.font.color.rgb = RGBColor(110, 110, 110)

    # Main Hero Title
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.line_spacing = 0.85
    run2 = p2.add_run()
    run2.text = main_title + "\n"
    run2.font.size = Pt(140)
    run2.font.bold = True
    run2.font.name = "Arial"
    run2.font.color.rgb = RGBColor(*accent_color)

    # Post-title
    p3 = tf.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.line_spacing = 0.85
    run3 = p3.add_run()
    run3.text = post_title
    run3.font.size = Pt(44)
    run3.font.bold = True
    run3.font.name = "Arial"
    run3.font.color.rgb = RGBColor(70, 70, 70)

    # === Layer 3: Call-To-Action (CTA) Geometry ===
    arrow_width = Inches(1.8)
    arrow_height = Inches(2.2)
    arrow_y = Inches(4.8)

    # Left CTA Arrow
    x_left = Inches(2.8)
    arrow1 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x_left, arrow_y, arrow_width, arrow_height)
    arrow1.fill.solid()
    arrow1.fill.fore_color.rgb = RGBColor(*accent_color)
    arrow1.line.color.rgb = RGBColor(*accent_color)  # Hide outline
    arrow1.text_frame.text = cta_1
    for paragraph in arrow1.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Right CTA Arrow
    x_right = prs.slide_width - Inches(2.8) - arrow_width
    arrow2 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x_right, arrow_y, arrow_width, arrow_height)
    arrow2.fill.solid()
    arrow2.fill.fore_color.rgb = RGBColor(*accent_color)
    arrow2.line.color.rgb = RGBColor(*accent_color)
    arrow2.text_frame.text = cta_2
    for paragraph in arrow2.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Central CTA Link / URL Text
    url_box = slide.shapes.add_textbox(Inches(4.5), Inches(5.6), Inches(4.333), Inches(0.8))
    url_p = url_box.text_frame.paragraphs[0]
    url_p.alignment = PP_ALIGN.CENTER
    url_run = url_p.add_run()
    url_run.text = url_text
    url_run.font.size = Pt(22)
    url_run.font.bold = True
    url_run.font.color.rgb = RGBColor(*accent_color)
    url_run.font.underline = True

    # Save and return
    prs.save(output_pptx_path)
    return output_pptx_path
