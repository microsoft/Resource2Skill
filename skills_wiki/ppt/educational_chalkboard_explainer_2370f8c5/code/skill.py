def create_slide(
    output_pptx_path: str,
    title_text: str = "COMPUTER NETWORKS",
    subtitle_text: str = "A Bottom up approach",
    section_text: str = "Network Topology - Part 1",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a "Chalkboard Tech Diagram" style.
    
    This style uses a dark green background with white and yellow chalk-like text
    to create an educational, hand-drawn feel.

    For the best effect, install a chalk-like font such as 'DK Crayon Crumble' (freely available online).
    If not found, a system-default handwritten font like 'Segoe Print' or 'Comic Sans MS' may be used.
    
    Args:
        output_pptx_path (str): The path to save the generated .pptx file.
        title_text (str): The main title for the slide.
        subtitle_text (str): The subtitle appearing below the main title.
        section_text (str): The section header at the bottom of the slide.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(23, 52, 49)  # Dark Green Chalkboard

    # === Style Definitions ===
    chalk_white = RGBColor(255, 255, 255)
    accent_yellow = RGBColor(255, 191, 0)
    # Recommended Font: "DK Crayon Crumble". If not available, PowerPoint will use a fallback.
    chalk_font = "DK Crayon Crumble"

    # === Layer 2: Text & Content ===

    # --- Main Title ---
    title_shape = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.33), Inches(1.5))
    title_tf = title_shape.text_frame
    title_tf.text = title_text
    p = title_tf.paragraphs[0]
    p.font.name = chalk_font
    p.font.size = Pt(88)
    p.font.bold = True
    p.font.color.rgb = chalk_white
    p.alignment = PP_ALIGN.CENTER

    # --- Decorative Underline for Title ---
    line = slide.shapes.add_shape(MSO_SHAPE.LINE, Inches(9.2), Inches(2.5), Inches(3.3), Inches(0))
    line.line.color.rgb = chalk_white
    line.line.width = Pt(3)

    # --- Subtitle ---
    subtitle_shape = slide.shapes.add_textbox(Inches(1), Inches(3.0), Inches(11.33), Inches(1))
    subtitle_tf = subtitle_shape.text_frame
    subtitle_tf.text = subtitle_text
    p = subtitle_tf.paragraphs[0]
    p.font.name = chalk_font
    p.font.size = Pt(36)
    p.font.color.rgb = chalk_white
    p.alignment = PP_ALIGN.CENTER

    # --- Section Title ---
    section_shape = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(11.33), Inches(1))
    section_tf = section_shape.text_frame
    section_tf.text = section_text
    p = section_tf.paragraphs[0]
    p.font.name = chalk_font
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = accent_yellow
    p.alignment = PP_ALIGN.CENTER

    # --- Decorative Icons (using Unicode for portability) ---
    # Network Icon (top-left)
    icon_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(2), Inches(2))
    icon_tf = icon_shape.text_frame
    icon_tf.text = "✳"  # An asterisk symbol that resembles a simple network node
    p_icon = icon_tf.paragraphs[0]
    p_icon.font.name = 'Arial'  # A standard font for reliable symbol rendering
    p_icon.font.size = Pt(120)
    p_icon.font.color.rgb = chalk_white
    p_icon.alignment = PP_ALIGN.CENTER

    # Globe Icon (mid-right, next to subtitle)
    globe_shape = slide.shapes.add_textbox(Inches(10), Inches(2.9), Inches(1), Inches(1))
    globe_tf = globe_shape.text_frame
    globe_tf.text = "🌍"  # Unicode for Earth Globe
    p_globe = globe_tf.paragraphs[0]
    p_globe.font.name = 'Segoe UI Emoji'  # Font that supports colored emojis
    p_globe.font.size = Pt(36)
    p_globe.font.color.rgb = chalk_white

    prs.save(output_pptx_path)
    return output_pptx_path

