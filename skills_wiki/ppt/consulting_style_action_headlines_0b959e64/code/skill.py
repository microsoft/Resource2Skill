def create_slide(
    output_pptx_path: str,
    action_title: str = "Hospitals is the largest turnover and fastest growing segment in healthcare",
    descriptive_subtitle: str = "Industry segments by annual turnover and growth rate",
    source_text: str = "Source: Slide Science analysis",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide demonstrating the Consulting-Style Action Headline pattern.

    This pattern prioritizes the key insight ("so what") in the main title,
    followed by a descriptive subtitle. The body of the slide, represented here
    by a placeholder, contains the data that proves the headline.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        action_title (str): The main headline, a full sentence stating the key insight.
        descriptive_subtitle (str): A smaller, secondary title describing the slide's content.
        source_text (str): The source attribution for the data, placed in the footer.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE

    # --- Setup Presentation and Slide ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 aspect ratio
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(blank_slide_layout)

    # --- Colors and Fonts ---
    TEXT_COLOR_DARK = RGBColor(38, 38, 38)
    TEXT_COLOR_MEDIUM = RGBColor(128, 128, 128)
    LINE_COLOR = RGBColor(200, 200, 200)
    PLACEHOLDER_BG_COLOR = RGBColor(242, 242, 242)

    # --- Layer 1: Action Headline (The "So What") ---
    # This is the most important part of the slide.
    left_margin = Inches(0.5)
    top_margin = Inches(0.4)
    title_width = prs.slide_width - (2 * left_margin)

    tx_box_title = slide.shapes.add_textbox(left_margin, top_margin, title_width, Inches(0.6))
    p_title = tx_box_title.text_frame.paragraphs[0]
    p_title.text = action_title
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_COLOR_DARK

    # --- Layer 2: Descriptive Sub-headline (The "What") ---
    # Optional, but good practice. Describes the content factually.
    subtitle_top = top_margin + Inches(0.6)
    tx_box_subtitle = slide.shapes.add_textbox(left_margin, subtitle_top, title_width, Inches(0.4))
    p_subtitle = tx_box_subtitle.text_frame.paragraphs[0]
    p_subtitle.text = descriptive_subtitle
    p_subtitle.font.name = 'Arial'
    p_subtitle.font.size = Pt(16)
    p_subtitle.font.bold = False
    p_subtitle.font.color.rgb = TEXT_COLOR_MEDIUM

    # --- Layer 3: Separator Line ---
    line_top = subtitle_top + Inches(0.5)
    slide.shapes.add_shape(
        MSO_SHAPE.LINE_INVERSE,
        left_margin,
        line_top,
        width=title_width,
        height=0
    ).line.fill.solid.fore_color.rgb = LINE_COLOR

    # --- Layer 4: Content Body Placeholder ---
    # This represents the chart, table, or diagram that provides the evidence.
    body_top = line_top + Inches(0.2)
    body_height = prs.slide_height - body_top - Inches(0.7)
    body_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left_margin,
        body_top,
 иммунитетwidth,
        body_height
    )
    body_shape.fill.solid.fore_color.rgb = PLACEHOLDER_BG_COLOR
    body_shape.line.fill.solid.fore_color.rgb = LINE_COLOR

    # Add a label to the placeholder
    tf_body = body_shape.text_frame
    tf_body.text = "Slide Body\n(Chart, Table, or Framework to support the Action Headline)"
    tf_body.paragraphs[0].font.color.rgb = TEXT_COLOR_MEDIUM
    tf_body.paragraphs[0].font.size = Pt(18)
    tf_body.vertical_anchor = 2 # Middle

    # --- Layer 5: Source Note ---
    source_top = body_top + body_height + Inches(0.1)
    tx_box_source = slide.shapes.add_textbox(left_margin, source_top, title_width, Inches(0.3))
    p_source = tx_box_source.text_frame.paragraphs[0]
    p_source.text = source_text
    p_source.font.name = 'Arial'
    p_source.font.size = Pt(10)
    p_source.font.italic = True
    p_source.font.color.rgb = TEXT_COLOR_MEDIUM

    # --- Save and return ---
    prs.save(output_pptx_path)
    return output_pptx_path

