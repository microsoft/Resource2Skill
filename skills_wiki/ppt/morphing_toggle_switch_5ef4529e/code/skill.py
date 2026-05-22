def create_slide(
    output_pptx_path: str,
    pros_title: str = "PROS",
    pros_body: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed tristique justo ut nunc blandit, ac congue tortor aliquet.",
    cons_title: str = "CONS",
    cons_body: str = "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae.",
    **kwargs
) -> str:
    """
    Creates a two-slide PowerPoint presentation demonstrating the Morphing Toggle Switch
    for a Pros and Cons comparison.

    The generated presentation uses the Morph transition to animate between the two states.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        pros_title: The title for the 'Pros' panel.
        pros_body: The body text for the 'Pros' panel.
        cons_title: The title for the 'Cons' panel.
        cons_body: The body text for the 'Cons' panel.

    Returns:
        The path to the saved .pptx file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from lxml import etree

    # --- Configuration ---
    # Colors
    BG_COLOR = RGBColor(45, 45, 45)
    INACTIVE_COLOR = RGBColor(68, 68, 68)
    PROS_COLOR = RGBColor(0, 255, 85)
    CONS_COLOR = RGBColor(255, 69, 86)
    ACTIVE_TEXT_COLOR = RGBColor(255, 255, 255)
    INACTIVE_TEXT_COLOR = RGBColor(20, 20, 20)

    # Fonts
    TITLE_FONT = 'Arial Black'
    BODY_FONT = 'Calibri'

    # Dimensions
    SLIDE_WIDTH = Inches(13.333)
    SLIDE_HEIGHT = Inches(7.5)
    PANEL_WIDTH = Inches(5)
    PANEL_HEIGHT = Inches(4)
    PANEL_Y = Inches(1.25)
    PROS_PANEL_X = Inches(1.5)
    CONS_PANEL_X = Inches(6.83)

    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    def set_slide_background(slide, rgb_color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = rgb_color

    def create_panel(slide, x, y, width, height, fill_color, title, body, title_font_color, body_font_color):
        # Panel shape
        panel = slide.shapes.add_shape(5, x, y, width, height) # 5 corresponds to rounded rectangle
        panel.fill.solid()
        panel.fill.fore_color.rgb = fill_color
        panel.line.fill.background()

        # Title text box
        title_box = slide.shapes.add_textbox(x, y + Inches(0.2), width, Inches(1))
        p_title = title_box.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.name = TITLE_FONT
        p_title.font.size = Pt(44)
        p_title.font.bold = True
        p_title.font.color.rgb = title_font_color
        p_title.alignment = PP_ALIGN.CENTER
        
        # Body text box
        body_box = slide.shapes.add_textbox(x + Inches(0.25), y + Inches(1.2), width - Inches(0.5), height - Inches(1.4))
        p_body = body_box.text_frame.paragraphs[0]
        p_body.text = body
        p_body.font.name = BODY_FONT
        p_body.font.size = Pt(16)
        p_body.font.color.rgb = body_font_color
        body_box.text_frame.word_wrap = True

    # --- Create the two slides representing the two states ---
    states = ['PROS', 'CONS']
    for state in states:
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
        set_slide_background(slide, BG_COLOR)

        # Slider Track
        track_width = Inches(8)
        track_height = Inches(0.75)
        track_x = (SLIDE_WIDTH - track_width) / 2
        track_y = Inches(5.75)
        track = slide.shapes.add_shape(5, track_x, track_y, track_width, track_height)
        track.fill.solid()
        track.fill.fore_color.rgb = INACTIVE_COLOR
        track.line.fill.background()
        # Make it a pill shape
        track.adjustments[0] = 0.5

        if state == 'PROS':
            # Active Pros Panel
            create_panel(slide, PROS_PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT, PROS_COLOR, pros_title, pros_body, ACTIVE_TEXT_COLOR, ACTIVE_TEXT_COLOR)
            # Inactive Cons Panel
            create_panel(slide, CONS_PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT, INACTIVE_COLOR, cons_title, cons_body, INACTIVE_TEXT_COLOR, INACTIVE_TEXT_COLOR)
            # Slider Handle for Pros
            handle_size = Inches(0.9)
            handle = slide.shapes.add_shape(1, track_x - Inches(0.1), track_y - Inches(0.07), handle_size, handle_size) # 1 is rectangle, we make it a circle
            handle.fill.solid()
            handle.fill.fore_color.rgb = PROS_COLOR
            handle.line.fill.background()
            handle.adjustments[0] = 0.5 # Make it a circle
            
        elif state == 'CONS':
            # Inactive Pros Panel
            create_panel(slide, PROS_PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT, INACTIVE_COLOR, pros_title, pros_body, INACTIVE_TEXT_COLOR, INACTIVE_TEXT_COLOR)
            # Active Cons Panel
            create_panel(slide, CONS_PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT, CONS_COLOR, cons_title, cons_body, ACTIVE_TEXT_COLOR, ACTIVE_TEXT_COLOR)
            # Slider Handle for Cons
            handle_size = Inches(0.9)
            handle_x_cons = track_x + track_width - handle_size + Inches(0.1)
            handle = slide.shapes.add_shape(1, handle_x_cons, track_y - Inches(0.07), handle_size, handle_size)
            handle.fill.solid()
            handle.fill.fore_color.rgb = CONS_COLOR
            handle.line.fill.background()
            handle.adjustments[0] = 0.5

    # --- Apply Morph Transition using LXML ---
    for slide in prs.slides:
        slide_xml = slide.element
        # The transition element should be a child of the <p:sld> tag
        # Define the namespace map
        ns_map = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
        
        # Create the <p:transition> element
        transition_tag = etree.SubElement(slide_xml, '{%s}transition' % ns_map['p'])
        
        # Create the <p:morph> element inside <p:transition>
        etree.SubElement(transition_tag, '{%s}morph' % ns_map['p'])

    prs.save(output_pptx_path)
    return output_pptx_path
