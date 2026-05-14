def create_slide(
    output_pptx_path: str,
    title_text: str = "Historical Milestone Timeline",
    body_text: str = "",
    bg_palette: str = "white",
    accent_color: tuple = (237, 125, 49),  # Office Orange
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Proportional Data-Driven Timeline visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Default data representing the tutorial's events
    events = [
        {"year": 1974, "desc": "Discovery that CFCs could destroy ozone in the stratosphere (Molina and Rowland)"},
        {"year": 1978, "desc": "United States, Canada, Sweden and Norway ban CFCs in aerosols"},
        {"year": 1984, "desc": "Ozone hole in Antarctica discovered (Chubachi)"},
        {"year": 1985, "desc": "Vienna Convention for the Protection of the Ozone Layer"},
        {"year": 1987, "desc": "Montreal Protocol on Substances that Deplete the Ozone Layer"},
        {"year": 1989, "desc": "Montreal Protocol entered into force"},
        {"year": 1990, "desc": "The London Amendment - Phase out CFCs & Halons"},
        {"year": 1992, "desc": "The Copenhagen Amendment - Tighter controls for HCFCs"},
        {"year": 1997, "desc": "The Montreal Amendment - New licensing system"},
        {"year": 1999, "desc": "The Beijing Amendment - Tighter controls for HCFCs"},
        {"year": 2015, "desc": "The Montreal Protocol became the first universally ratified treaty"},
        {"year": 2016, "desc": "The Kigali Amendment - HFCs added"},
    ]

    # Theme Colors
    COLOR_ACCENT = RGBColor(*accent_color)
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_GRAY = RGBColor(100, 100, 100)

    # Slide Dimensions & Timeline Configuration
    margin_x = Inches(1.0)
    axis_y = Inches(4.0)
    timeline_width = prs.slide_width - (margin_x * 2)
    
    start_year = 1970
    end_year = 2020
    year_range = end_year - start_year

    def get_x_pos(year):
        """Map a year to a physical X coordinate on the slide."""
        percentage = (year - start_year) / year_range
        return margin_x + (percentage * timeline_width)

    # === Layer 1: Connectors (Drawn first so they sit behind nodes and text boxes) ===
    
    # Track configurations to prevent text box overlaps
    # [High Top, Low Bottom, Low Top, High Bottom]
    track_y_positions = [
        axis_y - Inches(2.2),  # Top High
        axis_y + Inches(0.5),  # Bottom Low
        axis_y - Inches(1.1),  # Top Low
        axis_y + Inches(1.6),  # Bottom High
    ]
    
    box_width = Inches(1.8)
    box_height = Inches(0.8)

    # Draw event connectors
    for i, event in enumerate(events):
        x = get_x_pos(event["year"])
        track_idx = i % 4
        ty = track_y_positions[track_idx]
        
        # Determine anchor point for the line depending on if it's above or below axis
        is_above = ty < axis_y
        line_target_y = ty + box_height if is_above else ty
        
        # Draw vertical connector line
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, axis_y, x, line_target_y)
        connector.line.color.rgb = COLOR_ACCENT
        connector.line.width = Pt(1.5)

    # === Layer 2: The Timeline Axis ===
    
    # Main horizontal axis
    axis = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, margin_x, axis_y, margin_x + timeline_width, axis_y)
    axis.line.color.rgb = COLOR_BLACK
    axis.line.width = Pt(2.5)

    # Axis tick marks and labels (every 5 years)
    for yr in range(start_year, end_year + 1, 5):
        x = get_x_pos(yr)
        
        # Tick mark
        tick = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, axis_y - Pt(4), x, axis_y + Pt(4))
        tick.line.color.rgb = COLOR_BLACK
        tick.line.width = Pt(1.5)
        
        # Tick Label
        lbl_box = slide.shapes.add_textbox(x - Inches(0.4), axis_y + Pt(5), Inches(0.8), Inches(0.4))
        lbl_tf = lbl_box.text_frame
        lbl_tf.word_wrap = False
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = str(yr)
        lbl_p.font.bold = True
        lbl_p.font.size = Pt(10)
        lbl_p.font.color.rgb = COLOR_GRAY
        lbl_p.alignment = 2  # Center align

    # === Layer 3: Nodes and Text Boxes ===

    for i, event in enumerate(events):
        x = get_x_pos(event["year"])
        track_idx = i % 4
        ty = track_y_positions[track_idx]
        
        # Draw Circular Marker (Node)
        node_size = Pt(12)
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            x - (node_size / 2), 
            axis_y - (node_size / 2), 
            node_size, 
            node_size
        )
        node.fill.solid()
        node.fill.fore_color.rgb = COLOR_ACCENT
        node.line.fill.background() # No line

        # Draw Text Box
        # We add a solid white fill so it masks the connector line perfectly
        tx_box = slide.shapes.add_textbox(x - (box_width / 2), ty, box_width, box_height)
        tx_box.fill.solid()
        tx_box.fill.fore_color.rgb = COLOR_WHITE
        tx_box.line.color.rgb = COLOR_ACCENT
        tx_box.line.width = Pt(1)
        
        tf = tx_box.text_frame
        tf.word_wrap = True
        
        # Paragraph 1: Year
        p1 = tf.paragraphs[0]
        p1.text = str(event["year"])
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = COLOR_ACCENT
        
        # Paragraph 2: Description
        p2 = tf.add_paragraph()
        p2.text = event["desc"]
        p2.font.bold = False
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_BLACK

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(10), Inches(1))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.bold = True
    title_p.font.size = Pt(28)
    title_p.font.color.rgb = COLOR_BLACK

    prs.save(output_pptx_path)
    return output_pptx_path
