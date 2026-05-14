def create_slide(
    output_pptx_path: str,
    title_text: str = "Think like a designer",
    subtitle_text: str = "MASTERING THE 5 PRINCIPLES",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the flat, grid-based "5 Principles" layout 
    demonstrated in the tutorial, featuring strict alignment, contrast, and white space.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    # Core Video Palette
    COLOR_BG = RGBColor(247, 244, 235)       # Off-White
    COLOR_TEXT = RGBColor(63, 61, 68)        # Charcoal
    COLOR_ACCENT_YELLOW = RGBColor(242, 195, 71)  # Mustard
    COLOR_ACCENT_TEAL = RGBColor(98, 204, 182)    # Teal

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 1. Background Fill
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

    # 2. Add Subtitle Highlight Block (Must be added BEFORE text to be 'behind' it)
    # This demonstrates the 'Contrast' and 'Repetition' flat style of the video
    highlight_top = Inches(1.85)
    highlight_left = Inches(1.0)
    highlight_width = Inches(5.0)
    highlight_height = Inches(0.4)
    
    highlight = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, highlight_left, highlight_top, highlight_width, highlight_height
    )
    highlight.fill.solid()
    highlight.fill.fore_color.rgb = COLOR_ACCENT_YELLOW
    highlight.line.fill.background() # No border

    # 3. Main Title (Alignment & Contrast)
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.33), Inches(1.0))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = "Arial Black"
    p.font.size = Pt(54)
    p.font.color.rgb = COLOR_TEXT
    p.font.bold = True

    # 4. Subtitle Text (Overlapping the highlight block)
    sub_box = slide.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(5.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    tf_sub.clear()
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = COLOR_TEXT
    p_sub.font.bold = True

    # 5. Grid Layout for Cards (Proximity, White Space, Alignment, Repetition)
    # 3 Columns with strict mathematical alignment
    margin_left = 1.0
    gap = 0.5
    total_width = 11.333
    col_width = (total_width - (gap * 2)) / 3
    
    cards_data = [
        {"title": "Proximity", "desc": "Group related items together to visually establish their relationship and declutter the layout."},
        {"title": "White Space", "desc": "Leave generous empty space around elements to let the content breathe and guide the eye."},
        {"title": "Alignment", "desc": "Align elements to an invisible grid to create a crisp, organized, and unified aesthetic."}
    ]

    card_y = 3.5

    for i, data in enumerate(cards_data):
        col_x = margin_left + (i * (col_width + gap))

        # A. Accent Icon / Circle (Repetition)
        circle_size = 0.6
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(col_x), Inches(card_y), 
            Inches(circle_size), Inches(circle_size)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = COLOR_ACCENT_TEAL
        circle.line.fill.background()

        # B. Card Title (Contrast & Proximity)
        card_title_box = slide.shapes.add_textbox(
            Inches(col_x - 0.1), Inches(card_y + 0.8), Inches(col_width), Inches(0.5)
        )
        ctf = card_title_box.text_frame
        ctf.word_wrap = True
        cp = ctf.paragraphs[0]
        cp.text = data["title"]
        cp.font.name = "Arial"
        cp.font.size = Pt(24)
        cp.font.color.rgb = COLOR_TEXT
        cp.font.bold = True

        # C. Card Body (White Space & Proximity)
        card_body_box = slide.shapes.add_textbox(
            Inches(col_x - 0.1), Inches(card_y + 1.4), Inches(col_width), Inches(2.0)
        )
        btf = card_body_box.text_frame
        btf.word_wrap = True
        bp = btf.paragraphs[0]
        bp.text = data["desc"]
        bp.font.name = "Arial"
        bp.font.size = Pt(14)
        bp.font.color.rgb = COLOR_TEXT
        bp.line_spacing = 1.2  # Generous line spacing for readability

    # 6. Bottom Structural Line (Alignment anchor)
    line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, 
        begin_x=Inches(margin_left), begin_y=Inches(6.8),
        end_x=Inches(13.333 - margin_left), end_y=Inches(6.8)
    )
    line.line.color.rgb = COLOR_TEXT
    line.line.width = Pt(2)

    prs.save(output_pptx_path)
    return output_pptx_path
