def create_slide(
    output_pptx_path: str,
    agenda_items: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX file containing TWO professional agenda variations:
    Slide 1: Dark Mode Vertical Cards
    Slide 2: Light Mode Circular Hub & Horizontal Ribbons

    Returns: path to the saved PPTX file.
    """
    import copy
    from pptx import Presentation
    from pptx.util import Pt, Inches, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.dml import MSO_LINE
    from lxml.etree import ElementBase
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls

    if not agenda_items:
        agenda_items = [
            {"title": "Introduction", "body": "Welcome and greetings to all participants.\nOverview of meeting purpose."},
            {"title": "Key Presentation", "body": "Detailed presentation on the main topic.\nReview of performance metrics."},
            {"title": "Action Plan", "body": "Define actionable tasks and responsibilities.\nSet clear timeline and deliverables."},
            {"title": "Q&A & Closing", "body": "Open floor for questions and feedback.\nConfirmation of agreed next steps."}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Helper: Add Drop Shadow via lxml ---
    def add_shadow(shape):
        spPr = shape.element.spPr
        shadow_xml = f"""
        <a:effectLst {nsdecls('a')}>
            <a:outerShdw blurRad="254000" dist="38100" dir="2700000" algn="ctr" rotWithShape="0">
                <a:srgbClr val="000000">
                    <a:alpha val="15000"/>
                </a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        effectLst = parse_xml(shadow_xml)
        spPr.append(effectLst)

    # ==========================================
    # SLIDE 1: DARK MODE VERTICAL CARDS
    # ==========================================
    slide_dark = prs.slides.add_slide(blank_layout)
    
    # Set Dark Background
    background = slide_dark.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(17, 24, 39) # #111827

    # Title
    title_box = slide_dark.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(1))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = "Agenda Template"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    # Bottom Anchor Block
    anchor = slide_dark.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(5.5), Inches(13.333), Inches(2))
    anchor.fill.solid()
    anchor.fill.fore_color.rgb = RGBColor(0, 0, 0)
    anchor.line.fill.background()

    # Cards
    card_width = Inches(2.7)
    card_height = Inches(4.5)
    spacing = Inches(0.4)
    total_width = (card_width * 4) + (spacing * 3)
    start_x = (Inches(13.333) - total_width) / 2
    start_y = Inches(1.5)

    for i, item in enumerate(agenda_items[:4]):
        x = start_x + (i * (card_width + spacing))
        
        # Base Card
        card = slide_dark.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, start_y, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(31, 41, 55) # #1F2937
        card.line.fill.background()
        # Adjust roundness (approximate via lxml adjustment)
        for adj in card.element.xpath('.//a:adjLst/a:gd'):
            adj.set('fmla', 'val 10000') # Less rounded

        # Text inside card
        txBox = slide_dark.shapes.add_textbox(x + Inches(0.2), start_y + Inches(0.3), card_width - Inches(0.4), card_height - Inches(0.6))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        # Header
        p_title = tf.add_paragraph()
        p_title.text = item["title"]
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        if i == 0:
            p_title.font.color.rgb = RGBColor(74, 222, 128) # Accent Green
        else:
            p_title.font.color.rgb = RGBColor(255, 255, 255)

        # Body
        p_body = tf.add_paragraph()
        p_body.text = "\n" + item["body"]
        p_body.font.size = Pt(12)
        p_body.font.color.rgb = RGBColor(156, 163, 175) # Light Grey

        # Bottom Accent Bar
        bar_height = Inches(0.5)
        bar_y = start_y + card_height - bar_height
        bar = slide_dark.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, bar_y, card_width, bar_height)
        bar.fill.solid()
        if i == 0:
            bar.fill.fore_color.rgb = RGBColor(74, 222, 128) # Active Neon Green
        else:
            bar.fill.fore_color.rgb = RGBColor(17, 24, 39) # Inactive blending into bg
        bar.line.fill.background()

    # ==========================================
    # SLIDE 2: LIGHT MODE CIRCULAR HUB
    # ==========================================
    slide_light = prs.slides.add_slide(blank_layout)
    
    # Hub Circles
    cx, cy = Inches(2.5), Inches(3.75)
    r_outer = Inches(2.2)
    r_inner = Inches(1.8)

    # Outer light grey circle
    outer_circ = slide_light.shapes.add_shape(MSO_SHAPE.OVAL, cx - r_outer, cy - r_outer, r_outer*2, r_outer*2)
    outer_circ.fill.solid()
    outer_circ.fill.fore_color.rgb = RGBColor(243, 244, 246) # #F3F4F6
    outer_circ.line.fill.background()

    # Inner white circle with shadow
    inner_circ = slide_light.shapes.add_shape(MSO_SHAPE.OVAL, cx - r_inner, cy - r_inner, r_inner*2, r_inner*2)
    inner_circ.fill.solid()
    inner_circ.fill.fore_color.rgb = RGBColor(255, 255, 255)
    inner_circ.line.fill.background()
    add_shadow(inner_circ)

    # Hub Text
    hub_tx = slide_light.shapes.add_textbox(cx - r_inner, cy - Inches(0.6), r_inner*2, Inches(1.2))
    h_tf = hub_tx.text_frame
    h_tf.word_wrap = True
    h_p = h_tf.add_paragraph()
    h_p.text = "Agenda\nTemplate"
    h_p.font.size = Pt(32)
    h_p.font.bold = True
    h_p.font.color.rgb = RGBColor(31, 41, 55)
    h_p.alignment = PP_ALIGN.CENTER

    # Row Cards & Colors
    colors = [
        RGBColor(59, 130, 246),  # Blue
        RGBColor(20, 184, 166),  # Teal
        RGBColor(139, 92, 246),  # Purple
        RGBColor(249, 115, 22),  # Orange
        RGBColor(234, 179, 8)    # Yellow
    ]
    
    card_w = Inches(7.5)
    card_h = Inches(1.0)
    spacing_y = Inches(0.2)
    total_h = (card_h * 5) + (spacing_y * 4)
    start_rx = Inches(5.2)
    start_ry = (Inches(7.5) - total_h) / 2

    # Draw right side cards
    items_to_draw = (agenda_items + [{"title":"Action Item", "body":"Follow up steps."}])[:5] # Pad to 5 if needed
    
    for i, item in enumerate(items_to_draw):
        y = start_ry + (i * (card_h + spacing_y))
        c_color = colors[i % len(colors)]
        
        # Connection Line (Draw first so it goes behind nodes)
        conn = slide_light.shapes.add_connector(MSO_SHAPE.LINE, cx + r_outer - Inches(0.2), cy, start_rx, y + card_h/2)
        conn.line.color.rgb = RGBColor(156, 163, 175)
        conn.line.width = Pt(1.5)
        conn.line.dash_style = MSO_LINE.DASH
        
        # Node Dot on Circle
        dot_r = Inches(0.12)
        dot_x = (cx + r_outer - Inches(0.2)) - dot_r
        # Approximate projection on circle edge for Y
        dot_y = cy - dot_r + ((i - 2) * Inches(0.4)) 
        
        # Update connection start point to dot
        conn.begin_x = dot_x + dot_r
        conn.begin_y = dot_y + dot_r

        dot = slide_light.shapes.add_shape(MSO_SHAPE.OVAL, dot_x, dot_y, dot_r*2, dot_r*2)
        dot.fill.solid()
        dot.fill.fore_color.rgb = c_color
        dot.line.color.rgb = RGBColor(255,255,255)
        dot.line.width = Pt(2)
        add_shadow(dot)

        # Card Ribbon
        ribbon = slide_light.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_rx, y, card_w, card_h)
        ribbon.fill.solid()
        ribbon.fill.fore_color.rgb = c_color
        ribbon.line.fill.background()
        
        # Inner White Ribon
        i_ribbon = slide_light.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_rx + Inches(0.1), y + Inches(0.1), card_w - Inches(0.2), card_h - Inches(0.2))
        i_ribbon.fill.solid()
        i_ribbon.fill.fore_color.rgb = RGBColor(255, 255, 255)
        i_ribbon.line.fill.background()

        # Icon box (Simulated)
        icon_box = slide_light.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_rx + Inches(0.2), y + Inches(0.2), Inches(0.6), Inches(0.6))
        icon_box.fill.solid()
        icon_box.fill.fore_color.rgb = c_color
        icon_box.line.fill.background()

        # Text inside ribbon
        tx = slide_light.shapes.add_textbox(start_rx + Inches(1.0), y + Inches(0.05), card_w - Inches(1.2), card_h)
        tf = tx.text_frame
        p_t = tf.add_paragraph()
        p_t.text = item["title"]
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = c_color
        
        p_b = tf.add_paragraph()
        p_b.text = item["body"].replace("\n", " - ")
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = RGBColor(107, 114, 128)

    prs.save(output_pptx_path)
    return output_pptx_path
