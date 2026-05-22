def create_slide(
    output_pptx_path: str,
    title_text: str = "Though the King County point-in-time count dropped in 2019, homelessness continues to increase",
    kicker_text: str = "Situation",
    content_lines: list = None,
    accent_color: tuple = (0, 81, 155),
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the Consulting-Grade "Dot-Dash" Action Slide.
    
    :param output_pptx_path: Path to save the presentation.
    :param title_text: The main persuasive action title.
    :param kicker_text: The SCR category (e.g., SITUATION, COMPLICATION, RESOLUTION).
    :param content_lines: List of strings. Strings starting with "-" become dashed sub-bullets.
    :param accent_color: RGB tuple for the corporate accent color.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.xmlchemy import OxmlElement
    
    # Default content mirroring the video's McKinsey example
    if content_lines is None:
        content_lines = [
            "More than 22,000 households experience homelessness in Seattle each year",
            "- 22,500 households were homeless for at least some of 2018",
            "- 30% of households experiencing homelessness were chronically homeless",
            "Despite robust growth, the housing supply and average household incomes have not kept pace",
            "- Rents have grown faster than incomes, exacerbating pressure on the poorest households",
            "- Since 2010, Seattle has lost 112,000 housing units affordable to low-income earners"
        ]

    def apply_custom_bullet(paragraph, char):
        """Safely inject OpenXML to force a specific bullet character."""
        pPr = paragraph._p.get_or_add_pPr()
        # Clean out existing bullet configurations
        for prefix in ['a:buNone', 'a:buChar', 'a:buAutoNum', 'a:buBlip']:
            tag = pPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}{prefix.split(":")[1]}')
            if tag is not None:
                pPr.remove(tag)
        # Inject custom bullet character
        buChar = OxmlElement('a:buChar')
        buChar.set('char', char)
        pPr.insert(0, buChar)

    # Initialize Widescreen Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Layer 1: Kicker (Context Label) ---
    kicker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_kicker = kicker_box.text_frame
    tf_kicker.word_wrap = False
    p_kicker = tf_kicker.paragraphs[0]
    p_kicker.text = kicker_text.upper()
    p_kicker.font.size = Pt(12)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = RGBColor(*accent_color)
    p_kicker.font.name = "Arial"

    # --- Layer 2: Action Title ---
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(1.0))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(38, 38, 38)
    p_title.font.name = "Arial"

    # --- Layer 3: Accent Divider Line ---
    # Using a thin rectangle as a line for absolute color and thickness control
    divider = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(1.85), Inches(11.733), Pt(2)
    )
    divider.fill.solid()
    divider.fill.fore_color.rgb = RGBColor(*accent_color)
    divider.line.fill.background() # Remove border

    # --- Layer 4: "Dot-Dash" Body Content ---
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(4.5))
    tf_content = content_box.text_frame
    tf_content.word_wrap = True
    tf_content.clear() # Remove default empty paragraph

    for item in content_lines:
        p = tf_content.add_paragraph()
        if item.startswith("-"):
            # DASH Logic (Supporting evidence)
            p.text = item[1:].strip()
            p.level = 1
            apply_custom_bullet(p, '–') # En-dash
            p.font.size = Pt(16)
            p.font.bold = False
            p.font.color.rgb = RGBColor(89, 89, 89)
            p.font.name = "Arial"
            p.space_before = Pt(6)
        else:
            # DOT Logic (Key Statement)
            p.text = item.lstrip("•").strip()
            p.level = 0
            apply_custom_bullet(p, '•') # Solid Dot
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = RGBColor(38, 38, 38)
            p.font.name = "Arial"
            p.space_before = Pt(14)

    # --- Layer 5: Institutional Footer ---
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(4), Inches(0.3))
    p_footer = footer_box.text_frame.paragraphs[0]
    p_footer.text = "CONFIDENTIAL AND PROPRIETARY"
    p_footer.font.size = Pt(9)
    p_footer.font.color.rgb = RGBColor(140, 140, 140)
    p_footer.font.name = "Arial"

    page_box = slide.shapes.add_textbox(Inches(12.2), Inches(7.0), Inches(0.5), Inches(0.3))
    p_page = page_box.text_frame.paragraphs[0]
    p_page.text = "1"
    p_page.font.size = Pt(10)
    p_page.font.color.rgb = RGBColor(140, 140, 140)
    p_page.font.name = "Arial"

    prs.save(output_pptx_path)
    return output_pptx_path
