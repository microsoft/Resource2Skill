def create_slide(
    output_pptx_path: str,
    chart_data: list = None,
    title_text: str = "PERCENTAGE BY YEAR"
) -> str:
    """
    Creates a two-slide PowerPoint presentation ready for an animated rounded bar chart effect.

    To achieve the animation, open the generated PPTX file, select the second slide,
    go to the 'Transitions' tab, and click 'Morph'.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        chart_data: A list of dictionaries, each representing a bar.
                    Example: [{'year': '2017', 'value': 90, 'color': (255, 20, 147)}, ...]
        title_text: The main title for the chart.

    Returns:
        The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    # Default data if none provided
    if chart_data is None:
        chart_data = [
            {'year': '2017', 'value': 90, 'color': (255, 20, 147)},
            {'year': '2018', 'value': 40, 'color': (138, 43, 226)},
            {'year': '2019', 'value': 55, 'color': (30, 144, 255)},
            {'year': '2020', 'value': 30, 'color': (255, 193, 7)},
            {'year': '2021', 'value': 80, 'color': (255, 69, 0)},
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # --- Helper function to add shadow via lxml ---
    def add_shadow_to_shape(shape):
        sp = shape.element
        sp_tree = etree.ElementTree(sp)
        effect_lst = sp_tree.find('.//a:effectLst', namespaces=sp.nsmap)
        if effect_lst is None:
            # If no effectLst exists, create one within prstGeom's parent
            sp_pr = sp.find('.//p:spPr', namespaces=sp.nsmap)
            if sp_pr is not None:
                effect_lst = etree.SubElement(sp_pr, '{' + sp.nsmap['a'] + '}effectLst')

        if effect_lst is not None:
            # Shadow parameters: 5pt blur, 3pt distance, 270 deg (bottom), 80% transparent black
            outer_shdw = etree.SubElement(effect_lst, '{' + sp.nsmap['a'] + '}outerShdw',
                                         blurRad=str(Emu(Pt(5))), 
                                         dist=str(Emu(Pt(3))), 
                                         dir="2700000", 
                                         algn="ctr")
            srgb_clr = etree.SubElement(outer_shdw, '{' + sp.nsmap['a'] + '}srgbClr', val="000000")
            etree.SubElement(srgb_clr, '{' + sp.nsmap['a'] + '}alpha', val="20000") # 20% alpha = 80% transparent


    # Create Slide 1 (Start State) and Slide 2 (End State)
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])

    for slide in [slide1, slide2]:
        # Set background color
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(242, 242, 242)
        
        # Add title
        title_shape = slide.shapes.add_textbox(Inches(0), Inches(0.5), prs.slide_width, Inches(1))
        title_tf = title_shape.text_frame
        title_tf.text = title_text
        p = title_tf.paragraphs[0]
        p.font.name = 'Montserrat Semibold'
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(89, 89, 89)
        p.alignment = 1 # Center

    # --- Chart drawing parameters ---
    num_bars = len(chart_data)
    chart_area_width = Inches(11)
    bar_width = Inches(1.2)
    gap_width = (chart_area_width - (num_bars * bar_width)) / (num_bars - 1)
    start_x = (prs.slide_width - chart_area_width) / 2
    
    max_bar_height = Inches(4.5)
    baseline_y = Inches(6.0) # Bottom of the 100% bar
    start_y_offset = Inches(0.2) # How far below the baseline to start

    # --- Loop through data to create shapes on both slides ---
    for i, data in enumerate(chart_data):
        center_x = start_x + (i * (bar_width + gap_width)) + (bar_width / 2)
        bar_x = center_x - (bar_width / 2)
        
        # === SLIDE 2: FINAL STATE ===
        final_bar_height = max_bar_height * (data['value'] / 100.0)
        final_bar_y = baseline_y - final_bar_height
        final_circle_y = final_bar_y - (bar_width / 2)

        # Bar
        bar_shape2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bar_x, final_bar_y, bar_width, final_bar_height)
        bar_shape2.name = f"Bar_{data['year']}"
        bar_shape2.adjustments[0] = 0.5  # Fully rounded corners
        bar_shape2.line.fill.background()
        
        fill = bar_shape2.fill
        fill.gradient()
        fill.gradient_angle = 90 # Vertical
        
        stop1 = fill.gradient_stops.add()
        stop1.position = 0.0
        stop1.color.rgb = RGBColor(*data['color'])
        stop1.color.alpha = 0.4 # 60% transparent
        
        stop2 = fill.gradient_stops.add()
        stop2.position = 1.0
        stop2.color.rgb = RGBColor(*data['color'])
        stop2.color.alpha = 1.0 # Solid

        # Circle Cap
        circle2 = slide2.shapes.add_shape(MSO_SHAPE.OVAL, bar_x, final_circle_y, bar_width, bar_width)
        circle2.name = f"Circle_{data['year']}"
        circle2.fill.solid()
        circle2.fill.fore_color.rgb = RGBColor(*data['color'])
        circle2.line.fill.background()
        add_shadow_to_shape(circle2)
        
        tf2 = circle2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = f"{data['value']}%"
        p2.font.name = 'Montserrat Semibold'
        p2.font.size = Pt(18)
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.alignment = 1
        tf2.vertical_anchor = 3 # Middle

        # Year Label
        year_label2 = slide2.shapes.add_textbox(bar_x, baseline_y + Inches(0.1), bar_width, Inches(0.5))
        year_label2.name = f"YearLabel_{data['year']}"
        tf_year2 = year_label2.text_frame
        p_year2 = tf_year2.paragraphs[0]
        p_year2.text = str(data['year'])
        p_year2.font.name = 'Montserrat Semibold'
        p_year2.font.size = Pt(14)
        p_year2.font.color.rgb = RGBColor(89, 89, 89)
        p_year2.alignment = 1

        # === SLIDE 1: INITIAL STATE ===
        start_bar_y = baseline_y + start_y_offset
        start_circle_y = start_bar_y - (bar_width / 2)

        # Bar
        bar_shape1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bar_x, start_bar_y, bar_width, final_bar_height)
        bar_shape1.name = f"Bar_{data['year']}" # CRITICAL: Same name
        bar_shape1.adjustments[0] = 0.5
        bar_shape1.line.fill.background()
        
        fill = bar_shape1.fill
        fill.gradient()
        fill.gradient_angle = 90
        
        stop1 = fill.gradient_stops.add()
        stop1.position = 0.0
        stop1.color.rgb = RGBColor(*data['color'])
        stop1.color.alpha = 0.4
        
        stop2 = fill.gradient_stops.add()
        stop2.position = 1.0
        stop2.color.rgb = RGBColor(*data['color'])
        stop2.color.alpha = 1.0

        # Circle Cap
        circle1 = slide1.shapes.add_shape(MSO_SHAPE.OVAL, bar_x, start_circle_y, bar_width, bar_width)
        circle1.name = f"Circle_{data['year']}" # CRITICAL: Same name
        circle1.fill.solid()
        circle1.fill.fore_color.rgb = RGBColor(*data['color'])
        circle1.line.fill.background()
        add_shadow_to_shape(circle1)

        tf1 = circle1.text_frame
        p1 = tf1.paragraphs[0]
        p1.text = f"{data['value']}%"
        p1.font.name = 'Montserrat Semibold'
        p1.font.size = Pt(18)
        p1.font.color.rgb = RGBColor(*data['color']) # Hide text by matching fill
        p1.alignment = 1
        tf1.vertical_anchor = 3

        # Year Label
        year_label1 = slide1.shapes.add_textbox(bar_x, baseline_y + Inches(0.1), bar_width, Inches(0.5))
        year_label1.name = f"YearLabel_{data['year']}"
        tf_year1 = year_label1.text_frame
        p_year1 = tf_year1.paragraphs[0]
        p_year1.text = str(data['year'])
        p_year1.font.name = 'Montserrat Semibold'
        p_year1.font.size = Pt(14)
        p_year1.font.color.rgb = RGBColor(89, 89, 89)
        p_year1.alignment = 1

    prs.save(output_pptx_path)
    return output_pptx_path

