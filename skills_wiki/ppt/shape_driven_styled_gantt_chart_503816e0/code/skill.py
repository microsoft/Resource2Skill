def create_slide(
    output_pptx_path: str,
    title_text: str = "Project schedule and milestones",
    body_text: str = "This Gantt chart illustrates the project schedule, highlighting key milestones, task dependencies,\nand deadlines to ensure timely completion and efficient resource allocation.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Shape-Driven Styled Gantt Chart visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.oxml import OxmlElement
    import datetime

    # --- XML Injection Helper for Modern Styling ---
    def add_gradient_and_shadow(shape, color1_hex: str, color2_hex: str):
        spPr = shape.element.spPr
        
        # Remove any existing solid fill
        for fill in spPr.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill'):
            spPr.remove(fill)
            
        # Build gradient fill
        gradFill = OxmlElement('a:gradFill')
        gradFill.set('rotWithShape', '1')
        gsLst = OxmlElement('a:gsLst')
        
        gs1 = OxmlElement('a:gs')
        gs1.set('pos', '0')
        clr1 = OxmlElement('a:srgbClr')
        clr1.set('val', color1_hex)
        gs1.append(clr1)
        
        gs2 = OxmlElement('a:gs')
        gs2.set('pos', '100000')
        clr2 = OxmlElement('a:srgbClr')
        clr2.set('val', color2_hex)
        gs2.append(clr2)
        
        gsLst.append(gs1)
        gsLst.append(gs2)
        
        lin = OxmlElement('a:lin')
        lin.set('ang', '0') # horizontal gradient (left to right)
        lin.set('scaled', '1')
        
        gradFill.append(gsLst)
        gradFill.append(lin)
        spPr.append(gradFill)
        
        # Build soft drop shadow
        effectLst = OxmlElement('a:effectLst')
        outerShdw = OxmlElement('a:outerShdw')
        outerShdw.set('blurRad', '120000') # 12pt blur
        outerShdw.set('dist', '40000')     # 4pt distance
        outerShdw.set('dir', '5400000')    # 90 degrees (down)
        outerShdw.set('algn', 'b')
        
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '15000') # 15% opacity
        srgbClr.append(alpha)
        
        outerShdw.append(srgbClr)
        effectLst.append(outerShdw)
        spPr.append(effectLst)

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Render Header ---
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.4), Inches(11.333), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(37, 150, 190) # Brand Teal
    p.alignment = PP_ALIGN.CENTER

    sub_box = slide.shapes.add_textbox(Inches(1), Inches(1.0), Inches(11.333), Inches(0.4))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = body_text
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(120, 120, 120)
    p.alignment = PP_ALIGN.CENTER

    # --- Data Definition ---
    tasks = [
        {"name": "Concept Planning",       "start": datetime.date(2024, 1, 1),  "end": datetime.date(2024, 2, 10)},
        {"name": "Requirements Gathering", "start": datetime.date(2024, 1, 20), "end": datetime.date(2024, 3, 15)},
        {"name": "Design Phase",           "start": datetime.date(2024, 3, 5),  "end": datetime.date(2024, 4, 30)},
        {"name": "Development",            "start": datetime.date(2024, 4, 15), "end": datetime.date(2024, 7, 20)},
        {"name": "Testing",                "start": datetime.date(2024, 7, 5),  "end": datetime.date(2024, 8, 25)},
        {"name": "Quality Assurance",      "start": datetime.date(2024, 8, 10), "end": datetime.date(2024, 9, 20)},
        {"name": "Project Delivery",       "start": datetime.date(2024, 9, 15), "end": datetime.date(2024, 10, 15)},
        {"name": "Project Review",         "start": datetime.date(2024, 10, 5), "end": datetime.date(2024, 11, 15)},
    ]

    palettes = [
        ("4FACFE", "00F2FE"), ("43E97B", "38F9D7"), ("FA709A", "FEE140"), 
        ("E0C3FC", "8EC5FC"), ("F093FB", "F5576C"), ("5EE7DF", "B490CA"), 
        ("FF9A44", "FC6076"), ("00C6FB", "005BEA")
    ]

    # --- Chart Geometry Engine ---
    min_date = min([t['start'] for t in tasks])
    max_date = max([t['end'] for t in tasks])
    total_days = (max_date - min_date).days

    chart_left = Inches(3.0)
    chart_width = Inches(9.8)
    chart_top = Inches(2.2)
    chart_bottom = Inches(7.0)
    chart_height = chart_bottom - chart_top
    
    num_tasks = len(tasks)
    row_height = chart_height / num_tasks
    bar_height = row_height * 0.55

    # --- 1. Draw Timeline Grid & X-Axis ---
    num_markers = 5
    for i in range(num_markers + 1):
        ratio = i / num_markers
        x_pos = chart_left + ratio * chart_width
        marker_date = min_date + datetime.timedelta(days=int(ratio * total_days))
        
        # Vertical thin grid line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, chart_top, Pt(1), chart_height)
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(235, 235, 235)
        line.line.fill.background()
        
        # Date Label
        txBox = slide.shapes.add_textbox(x_pos - Inches(0.6), chart_top - Inches(0.35), Inches(1.2), Inches(0.3))
        tf = txBox.text_frame
        tf.margin_top, tf.margin_bottom, tf.margin_left, tf.margin_right = 0, 0, 0, 0
        p = tf.paragraphs[0]
        p.text = marker_date.strftime("%d/%m/%y")
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(120, 120, 120)
        p.alignment = PP_ALIGN.CENTER

    # --- 2. Draw Task Bars & Y-Axis Categories ---
    for i, task in enumerate(tasks):
        y_pos = chart_top + i * row_height
        
        # Y-Axis Text Label
        txBox = slide.shapes.add_textbox(Inches(0.2), y_pos + (row_height - Inches(0.3)) / 2, Inches(2.6), Inches(0.3))
        tf = txBox.text_frame
        tf.margin_top, tf.margin_bottom, tf.margin_left, tf.margin_right = 0, 0, 0, Inches(0.1)
        p = tf.paragraphs[0]
        p.text = task['name']
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(40, 40, 40)
        p.alignment = PP_ALIGN.RIGHT
        
        # Task Bar Geometry Calculation
        start_days = (task['start'] - min_date).days
        duration_days = (task['end'] - task['start']).days
        
        bar_x = chart_left + (start_days / total_days) * chart_width
        bar_w = max((duration_days / total_days) * chart_width, Inches(0.1)) # Prevent 0-width
        bar_y = y_pos + (row_height - bar_height) / 2
        
        # Draw Rounded Bar
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bar_x, bar_y, bar_w, bar_height)
        shape.adjustments[0] = 0.25 # 25% rounding
        shape.line.fill.background() # Remove border
        
        # Apply programmatic styling
        color1, color2 = palettes[i % len(palettes)]
        add_gradient_and_shadow(shape, color1, color2)

    prs.save(output_pptx_path)
    return output_pptx_path
