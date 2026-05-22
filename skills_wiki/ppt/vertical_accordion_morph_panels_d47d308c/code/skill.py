def create_slide(
    output_pptx_path: str,
    title_text: str = "WELCOME",
    subtitle_text: str = "FREE POWERPOINT TEMPLATE",
    body_text: str = "Here write a short message about your company objectives and previous year projects that may have influence over your audience and it will bring a good impression.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Vertical Accordion Morph Panels' visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml

    # 1. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 2. Slide Background (Light Gray)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)

    # 3. Tab Data & Palette
    tabs = [
        {'label': 'follow',   'color': RGBColor(38, 166, 154)},
        {'label': 'services', 'color': RGBColor(102, 187, 106)},
        {'label': 'teams',    'color': RGBColor(255, 202, 40)},
        {'label': 'timeline', 'color': RGBColor(120, 144, 156)},
        {'label': 'about',    'color': RGBColor(236, 64, 122)}
    ]

    # Math configuration for tabs
    tab_height = 1.3
    radius = tab_height / 2  # 0.65 inches
    visible_width = radius
    start_y = (7.5 - (len(tabs) * tab_height)) / 2  # Center vertically (0.5")

    # Helper function to inject drop shadow XML
    def apply_panel_shadow(shape):
        shadow_xml = """
        <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:outerShdw blurRad="250000" dist="30000" dir="10800000" algn="ctr" rotWithShape="0">
                <a:srgbClr val="000000">
                    <a:alpha val="15000"/>
                </a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        shape._element.spPr.append(parse_xml(shadow_xml))

    # 4. Construct the Accordion Layers
    # Z-index logic: We loop left-to-right. Each iteration places a circle, THEN a panel.
    # The panel covers the right half of the circle. The NEXT iteration's panel covers the rest.
    for i, tab in enumerate(tabs):
        # Calculate positions
        panel_left = 0.65 + (i * visible_width)
        circle_x_center = panel_left
        circle_y_center = start_y + (i * tab_height) + radius
        
        # A. Create the Tab Circle
        circle_left = circle_x_center - radius
        circle_top = circle_y_center - radius
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(circle_left), Inches(circle_top), Inches(tab_height), Inches(tab_height))
        circle.fill.solid()
        circle.fill.fore_color.rgb = tab['color']
        circle.line.fill.background() # No outline

        # B. Create the Content Panel
        # Extending far to the right to cover the rest of the slide
        panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(panel_left), Inches(0), Inches(13.333 - panel_left + 1), Inches(7.5))
        panel.fill.solid()
        panel.fill.fore_color.rgb = RGBColor(255, 255, 255)
        panel.line.fill.background()
        apply_panel_shadow(panel)

        # C. Add Rotated Text Label
        # Text box must be centered precisely in the VISIBLE left half of the circle
        tb_w = tab_height * 0.9 # Slightly smaller than full height
        tb_h = visible_width * 0.8
        
        # Center of the *visible* semi-circle
        visible_center_x = panel_left - (visible_width / 2)
        tb_left = visible_center_x - (tb_w / 2)
        tb_top = circle_y_center - (tb_h / 2)

        tb = slide.shapes.add_textbox(Inches(tb_left), Inches(tb_top), Inches(tb_w), Inches(tb_h))
        tb.rotation = 270.0 # Read bottom-to-top
        
        tf = tb.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = tab['label']
        run.font.name = 'Century Gothic'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    # 5. Add Main Content Area (on the top-most panel)
    content_start_x = 0.65 + (len(tabs) * visible_width) + 0.5
    active_color = tabs[-1]['color'] # Pink matching the last active tab

    # Title
    title_box = slide.shapes.add_textbox(Inches(content_start_x), Inches(2.0), Inches(7.0), Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text
    run.font.name = 'Century Gothic'
    run.font.size = Pt(64)
    run.font.color.rgb = active_color

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(content_start_x), Inches(3.2), Inches(7.0), Inches(0.5))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = subtitle_text
    run.font.name = 'Century Gothic'
    run.font.size = Pt(22)
    run.font.color.rgb = tabs[0]['color'] # Teal

    # Decorative dots under subtitle
    dot_spacing = 0.4
    start_dot_x = content_start_x + 3.5 - (len(tabs) * dot_spacing / 2) + 0.2
    for j, tab in enumerate(tabs):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(start_dot_x + j*dot_spacing), Inches(3.8), Inches(0.2), Inches(0.2))
        dot.fill.solid()
        dot.fill.fore_color.rgb = tab['color']
        dot.line.fill.background()

    # Body Text
    body_box = slide.shapes.add_textbox(Inches(content_start_x + 1.0), Inches(4.5), Inches(5.0), Inches(1.5))
    tf = body_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = body_text
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(100, 100, 100)

    prs.save(output_pptx_path)
    return output_pptx_path
