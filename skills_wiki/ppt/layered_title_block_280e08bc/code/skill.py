def create_slide(
    output_pptx_path: str,
    main_title: str = "THE BUSINESS NEEDS DRIVE THE",
    overlay_title: str = "ARCHITECTURE, NOT THE TECHNOLOGY ITSELF",
    bg_color: tuple = (13, 27, 56),  # Dark Blue
    overlay_color: tuple = (0, 0, 0),  # Black for the overlay
    font_color: tuple = (255, 255, 255),  # White
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a professional, layered text overlay effect.

    This style is excellent for title slides and section headers, creating a sense of
    depth and modern design by layering a semi-transparent panel over a large title.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        main_title: The large background title text.
        overlay_title: The smaller text that appears on the semi-transparent overlay.
        bg_color: RGB tuple for the slide's background color.
        overlay_color: RGB tuple for the semi-transparent overlay shape.
        font_color: RGB tuple for the text color.

    Returns:
        The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Main Title (underneath the overlay) ===
    left = Inches(1.0)
    top = Inches(3.5)
    width = Inches(14.0)
    height = Inches(1.5)

    txBox_main = slide.shapes.add_textbox(left, top, width, height)
    tf_main = txBox_main.text_frame
    tf_main.word_wrap = True

    p_main = tf_main.paragraphs[0]
    p_main.text = main_title.upper()
    p_main.font.name = 'Arial Black'
    p_main.font.size = Pt(60)
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(*font_color)
    p_main.alignment = PP_ALIGN.CENTER

    # === Layer 3: Semi-Transparent Overlay Shape ===
    # Position the overlay to partially cover the main title
    overlay_left = Inches(0.5)
    overlay_top = top + Inches(0.8)  # Overlap the bottom part of the main title
    overlay_width = Inches(15.0)
    overlay_height = Inches(1.8)

    overlay_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, overlay_left, overlay_top, overlay_width, overlay_height)
    
    # Format the overlay shape
    overlay_shape.line.fill.background()  # No outline
    fill = overlay_shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*overlay_color)
    fill.transparency = 0.5  # 50% transparent

    # === Layer 4: Overlay Title (on top of the shape) ===
    txBox_overlay = slide.shapes.add_textbox(overlay_left, overlay_top, overlay_width, overlay_height)
    tf_overlay = txBox_overlay.text_frame
    tf_overlay.word_wrap = True
    tf_overlay.vertical_anchor = 'middle'

    p_overlay = tf_overlay.paragraphs[0]
    p_overlay.text = overlay_title.upper()
    p_overlay.font.name = 'Arial'
    p_overlay.font.size = Pt(36)
    p_overlay.font.bold = True
    p_overlay.font.color.rgb = RGBColor(*font_color)
    p_overlay.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path

