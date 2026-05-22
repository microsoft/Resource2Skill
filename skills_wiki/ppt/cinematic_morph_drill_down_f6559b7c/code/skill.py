def create_slide(
    output_pptx_path: str,
    title_text: str = "Quarterly Overview",
    card1_text: str = "Q1 Performance",
    card2_text: str = "Q2 Projections",
    card3_text: str = "Q3 Strategy",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Cinematic Morph Drill-Down effect.
    Slide 1 shows a 3-card overview.
    Slide 2 morphs into a focused view of Card 1.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import qn

    # Helper: Inject soft outer shadow via XML
    def apply_shadow(shape):
        shadow_xml = """
            <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:outerShdw blurRad="150000" dist="60000" dir="5400000" algn="b" rotWithShape="0">
                    <a:srgbClr val="000000">
                        <a:alpha val="20000"/>
                    </a:srgbClr>
                </a:outerShdw>
            </a:effectLst>
        """
        effectLst = parse_xml(shadow_xml)
        spPr = shape.element.spPr
        existing = spPr.find(qn('a:effectLst'))
        if existing is not None:
            spPr.remove(existing)
        spPr.append(effectLst)

    # Helper: Adjust corner radius of rounded rectangles
    def set_rounding(shape, radius=16667):
        prstGeom = shape.element.spPr.find(qn('a:prstGeom'))
        if prstGeom is not None:
            avLst = prstGeom.find(qn('a:avLst'))
            if avLst is None:
                avLst = parse_xml('<a:avLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
                prstGeom.append(avLst)
            for child in list(avLst):
                avLst.remove(child)
            avLst.append(parse_xml(f'<a:gd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="adj" fmla="val {radius}"/>'))

    # Helper: Style the card and populate text
    def style_card(shape, text, bg_color, is_hero=False):
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.fill.background()
        set_rounding(shape, 8333 if is_hero else 16667)
        apply_shadow(shape)
        
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.4)
        tf.margin_right = Inches(0.4)
        tf.margin_top = Inches(0.4)
        tf.margin_bottom = Inches(0.4)
        
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(32) if is_hero else Pt(24)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        if is_hero:
            p2 = tf.add_paragraph()
            p2.text = "\nThis detailed view is dynamically revealed. PowerPoint's Morph transition interpolates the scale, position, and border radius of the object automatically, creating a seamless app-like drill-down experience."
            p2.font.size = Pt(16)
            p2.font.color.rgb = RGBColor(230, 240, 255)

    # Helper: Set slide background color
    def set_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(240, 244, 248) # Light grey-blue

    # Helper: Format Title
    def format_title(slide, text, top, font_size):
        title = slide.shapes.add_textbox(Inches(0.5), Inches(top), Inches(12), Inches(1))
        title.name = "!!MainTitle"  # !! Forces Morph matching
        p = title.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = RGBColor(20, 30, 50)
        return title

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette
    c1_color = RGBColor(45, 106, 255)  # Blue
    c2_color = RGBColor(111, 66, 193)  # Purple
    c3_color = RGBColor(0, 184, 217)   # Cyan
    
    # ==========================================
    # SLIDE 1: Overview State
    # ==========================================
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide1)
    format_title(slide1, title_text, 0.6, 44)
    
    card1_s1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.2), Inches(3.1), Inches(4.2))
    card1_s1.name = "!!Card1"
    style_card(card1_s1, card1_text, c1_color, is_hero=False)
    
    card2_s1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.11), Inches(2.2), Inches(3.1), Inches(4.2))
    card2_s1.name = "!!Card2"
    style_card(card2_s1, card2_text, c2_color, is_hero=False)
    
    card3_s1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.72), Inches(2.2), Inches(3.1), Inches(4.2))
    card3_s1.name = "!!Card3"
    style_card(card3_s1, card3_text, c3_color, is_hero=False)

    # ==========================================
    # SLIDE 2: Drill-Down State
    # ==========================================
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide2)
    format_title(slide2, f"{title_text}: {card1_text} Deep Dive", 0.3, 32)
    
    # Card 1 expands to Hero
    card1_s2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.3), Inches(8.5), Inches(5.7))
    card1_s2.name = "!!Card1"
    style_card(card1_s2, card1_text, c1_color, is_hero=True)
    
    # Card 2 and 3 shrink to sidebar
    card2_s2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.5), Inches(1.3), Inches(3.3), Inches(2.6))
    card2_s2.name = "!!Card2"
    style_card(card2_s2, card2_text, c2_color, is_hero=False)
    
    card3_s2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.5), Inches(4.4), Inches(3.3), Inches(2.6))
    card3_s2.name = "!!Card3"
    style_card(card3_s2, card3_text, c3_color, is_hero=False)

    # Inject Morph Transition into Slide 2
    transition_xml = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2012/main" spd="slow"><p15:morph option="byObject"/></p:transition>'
    transition_el = parse_xml(transition_xml)
    
    sld = slide2.element
    existing_trans = sld.find(qn('p:transition'))
    if existing_trans is not None:
        sld.remove(existing_trans)
        
    timing = sld.find(qn('p:timing'))
    extLst = sld.find(qn('p:extLst'))
    
    if timing is not None:
        timing.addprevious(transition_el)
    elif extLst is not None:
        extLst.addprevious(transition_el)
    else:
        sld.append(transition_el)

    prs.save(output_pptx_path)
    return output_pptx_path
