def create_slide(
    output_pptx_path: str,
    title_text: str = "FIVE STEPS TO DESIGN",
    steps_data: list = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with an Interlocking S-Curve Process Flow.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title for the slide.
        steps_data (list): A list of dictionaries, each containing 'title' and 'description' for a step.
                           If None, default data will be used.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.dml import MSO_THEME_COLOR
    from lxml import etree

    # Helper function to add animations using lxml
    def add_animation(shape, effect='fade', trigger='afterPrevious', duration=500, delay=0):
        # Access the slide's animation XML tree (p:timing)
        slide = shape.part.parent_part
        if not hasattr(slide, "_timenodelist"):
            slide._timenodelist = slide.element.find('.//p:timing', namespaces=slide.element.nsmap)
            if slide._timenodelist is None:
                timing = etree.SubElement(slide.element, '{' + slide.element.nsmap['p'] + '}timing')
                tn_lst = etree.SubElement(timing, '{' + slide.element.nsmap['p'] + '}tnLst')
                main_sq = etree.SubElement(tn_lst, '{' + slide.element.nsmap['p'] + '}par')
                etree.SubElement(main_sq, '{' + slide.element.nsmap['p'] + '}cTn', id="1", dur="indefinite", restart="never", nodeType="mainSeq")
                slide._timenodelist = main_sq.find('./p:cTn', namespaces=slide.element.nsmap)

        # Get the main sequence node
        main_sequence = slide._timenodelist
        
        # Get a unique ID for the new animation node
        new_id = str(len(main_sequence.getparent().findall('.//p:cTn', namespaces=slide.element.nsmap)) + 1)
        
        # Create the animation node
        anim_node = etree.SubElement(main_sequence, '{' + slide.element.nsmap['p'] + '}par')
        c_tn = etree.SubElement(anim_node, '{' + slide.element.nsmap['p'] + '}cTn', id=new_id, fill="hold")
        
        # Set start trigger (e.g., on click, with previous, after previous)
        st_cond_lst = etree.SubElement(c_tn, '{' + slide.element.nsmap['p'] + '}stCondLst')
        if trigger == 'onClick':
            etree.SubElement(st_cond_lst, '{' + slide.element.nsmap['p'] + '}cond', delay="indefinite")
        else: # withPrevious or afterPrevious
            prev_id = "0" if trigger == 'withPrevious' else str(int(new_id) - 1)
            cond_trigger = "with" if trigger == 'withPrevious' else "after"
            etree.SubElement(st_cond_lst, '{' + slide.element.nsmap['p'] + '}cond', evt="onBegin", delay=str(delay)).append(
                etree.Element('{' + slide.element.nsmap['p'] + '}tgtEl').append(
                    etree.Element('{' + slide.element.nsmap['p'] + '}tn', val=prev_id)
                )
            )

        # Common animation elements
        anim_effect = etree.SubElement(c_tn, '{' + slide.element.nsmap['p'] + '}cTn', id=str(int(new_id)+1), dur=str(duration), fill="hold")
        tgt_el = etree.SubElement(anim_effect, '{' + slide.element.nsmap['p'] + '}tgtEl')
        etree.SubElement(tgt_el, '{' + slide.element.nsmap['p'] + '}spTgt', spid=str(shape.shape_id))
        
        # Define the actual effect (e.g., Fade, Fly In)
        anim_color = etree.SubElement(anim_effect, '{' + slide.element.nsmap['p'] + '}anim')
        if effect == 'fade':
            anim_color.set('calcmode', 'lin')
            c_bhvr = etree.SubElement(anim_color, '{' + slide.element.nsmap['p'] + '}cBhvr')
            etree.SubElement(c_bhvr, '{' + slide.element.nsmap['p'] + '}cTn', id=str(int(new_id)+2), dur=str(duration), fill="hold")
            etree.SubElement(c_bhvr, '{' + slide.element.nsmap['p'] + '}tgtEl').append(tgt_el.find('.//p:spTgt', namespaces=slide.element.nsmap))
            attr_name_lst = etree.SubElement(c_bhvr, '{' + slide.element.nsmap['p'] + '}attrNameLst')
            etree.SubElement(attr_name_lst, '{' + slide.element.nsmap['p'] + '}attrName').text = "style.opacity"
            set_node = etree.SubElement(anim_color, '{' + slide.element.nsmap['p'] + '}set')
            etree.SubElement(set_node, '{' + slide.element.nsmap['p'] + '}cBhvr').append(c_bhvr[0])
            to_node = etree.SubElement(set_node, '{' + slide.element.nsmap['p'] + '}to')
            etree.SubElement(to_node, '{' + slide.element.nsmap['p'] + '}strVal', val="1")
    
    # --- Presentation and Slide Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # --- Background Color ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(232, 234, 246)

    # --- Default Data ---
    if steps_data is None:
        steps_data = [
            {"title": "DO YOUR RESEARCH", "description": "Insert You're Here. Change The Font If Your Want."},
            {"title": "VISUALIZE DATA", "description": "Insert You're Here. Change The Font If Your Want."},
            {"title": "BUILD AN OUTLINE", "description": "Insert You're Here. Change The Font If Your Want."},
            {"title": "LAY OUT THE INFOGRAPHIC", "description": "Insert You're Here. Change The Font If Your Want."},
            {"title": "DESIGN AND STYLIZE", "description": "Insert You're Here. Change The Font If Your Want."},
        ]
    
    colors = [
        RGBColor(103, 58, 183),  # Purple
        RGBColor(0, 150, 198),   # Blue
        RGBColor(0, 178, 148),   # Green
        RGBColor(247, 150, 70),  # Orange
        RGBColor(236, 64, 122),  # Pink
    ]

    # --- Slide Title ---
    title_shape = slide.shapes.add_textbox(Inches(0), Inches(0.5), prs.slide_width, Inches(0.75))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(64, 64, 64)
    p.alignment = 1  # Center align
    add_animation(title_shape, effect='fade', trigger='onClick', duration=500, delay=250)


    # --- S-Curve Elements ---
    num_steps = len(steps_data)
    center_x = prs.slide_width / 2
    
    circle_diameter = Inches(1.2)
    overlap_factor = 0.7  # 1.0 means no overlap, 0.7 means 30% overlap
    total_height = (num_steps - 1) * circle_diameter * overlap_factor + circle_diameter
    start_y = (prs.slide_height - total_height) / 2

    for i, step_info in enumerate(steps_data):
        is_left_aligned = (i % 2 != 0)
        
        # --- Create the Donut Shape Group ---
        y_pos = start_y + i * circle_diameter * overlap_factor
        
        # Add solid half-circle (back)
        solid_pie = slide.shapes.add_shape(MSO_SHAPE.PIE, center_x - circle_diameter/2, y_pos, circle_diameter, circle_diameter)
        solid_pie.rotation = 90 if is_left_aligned else 270
        sp_fill = solid_pie.fill
        sp_fill.solid()
        sp_fill.fore_color.rgb = colors[i % len(colors)]
        solid_pie.line.fill.background()

        # Add transparent half-circle (front)
        trans_pie = slide.shapes.add_shape(MSO_SHAPE.PIE, center_x - circle_diameter/2, y_pos, circle_diameter, circle_diameter)
        trans_pie.rotation = 270 if is_left_aligned else 90
        tp_fill = trans_pie.fill
        tp_fill.solid()
        tp_fill.fore_color.rgb = colors[i % len(colors)]
        tp_fill.transparency = 0.7
        trans_pie.line.fill.background()

        # Add inner white circle
        inner_circle_diameter = Inches(0.9)
        inner_circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, 
                                              center_x - inner_circle_diameter/2, 
                                              y_pos + (circle_diameter - inner_circle_diameter)/2,
                                              inner_circle_diameter, inner_circle_diameter)
        inner_circle.fill.solid()
        inner_circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
        inner_circle.line.fill.background()
        
        # Add step number
        step_num_shape = slide.shapes.add_textbox(center_x - Inches(0.4), y_pos + Inches(0.3), Inches(0.8), Inches(0.5))
        step_num_tf = step_num_shape.text_frame
        step_num_tf.word_wrap = False
        p_num = step_num_tf.paragraphs[0]
        p_num.text = f"{i+1:02}"
        p_num.font.bold = True
        p_num.font.size = Pt(20)
        p_num.font.color.rgb = RGBColor(64, 64, 64)
        p_num.alignment = 1 # Center
        
        add_animation(solid_pie, effect='fade', trigger='afterPrevious', delay=250)
        add_animation(trans_pie, effect='fade', trigger='withPrevious')
        add_animation(inner_circle, effect='fade', trigger='withPrevious')
        add_animation(step_num_shape, effect='fade', trigger='withPrevious')

        # --- Create the Text and Icon Group ---
        line_length = Inches(2)
        text_box_width = Inches(3.5)
        
        if is_left_aligned:
            # Line
            line_start_x = center_x - circle_diameter / 2 - line_length
            line_end_x = center_x - circle_diameter / 2
            # Icon placeholder
            icon_x = line_start_x - Inches(0.4)
            # Text
            text_x = line_start_x - text_box_width
            text_align = 2 # Right
        else: # Right aligned
            # Line
            line_start_x = center_x + circle_diameter / 2
            line_end_x = center_x + circle_diameter / 2 + line_length
            # Icon placeholder
            icon_x = line_end_x + Inches(0.1)
            # Text
            text_x = line_end_x + Inches(0.1)
            text_align = 0 # Left

        line_y = y_pos + circle_diameter / 2
        
        # Line shape
        line = slide.shapes.add_connector(MSO_SHAPE.LINE_INVERSE, line_start_x, line_y, line_end_x, line_y)
        line.line.color.rgb = colors[i % len(colors)]
        line.line.width = Pt(1.5)

        # Text boxes
        title_box = slide.shapes.add_textbox(text_x, line_y - Inches(0.35), text_box_width, Inches(0.3))
        title_box_tf = title_box.text_frame
        p_title = title_box_tf.paragraphs[0]
        p_title.text = step_info['title']
        p_title.font.bold = True
        p_title.font.size = Pt(11)
        p_title.font.color.rgb = colors[i % len(colors)]
        p_title.alignment = text_align

        desc_box = slide.shapes.add_textbox(text_x, line_y - Inches(0.1), text_box_width, Inches(0.4))
        desc_box_tf = desc_box.text_frame
        p_desc = desc_box_tf.paragraphs[0]
        p_desc.text = step_info['description']
        p_desc.font.size = Pt(9)
        p_desc.font.color.rgb = RGBColor(100, 100, 100)
        p_desc.alignment = text_align

        # Icon placeholder shape
        icon_size = Inches(0.3)
        icon_shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, icon_x, line_y - icon_size / 2, icon_size, icon_size)
        icon_shape.fill.solid()
        icon_shape.fill.fore_color.rgb = colors[i % len(colors)]
        icon_shape.line.fill.background()

        # Animate the side elements
        add_animation(line, effect='fade', trigger='withPrevious', delay=100)
        add_animation(title_box, effect='fade', trigger='withPrevious', delay=150)
        add_animation(desc_box, effect='fade', trigger='withPrevious', delay=200)
        add_animation(icon_shape, effect='fade', trigger='withPrevious', delay=100)

    prs.save(output_pptx_path)
    return output_pptx_path

