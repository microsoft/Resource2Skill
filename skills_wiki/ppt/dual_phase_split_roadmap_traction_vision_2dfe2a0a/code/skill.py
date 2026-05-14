import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement

def add_drop_shadow(shape):
    """
    Injects OpenXML to add a professional drop shadow to a python-pptx shape.
    """
    spPr = shape.element.spPr
    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    
    # Shadow properties: blur radius, distance, direction, angle
    outerShdw.set('blurRad', str(Emu(Pt(5))))
    outerShdw.set('dist', str(Emu(Pt(3))))
    outerShdw.set('dir', '2700000') # 45 degrees
    outerShdw.set('algn', 'ctr')
    
    # Shadow color (Black with 40% opacity)
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')
    alpha = OxmlElement('a:alpha')
    alpha.set('val', '40000') # 40% opacity
    srgbClr.append(alpha)
    
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    spPr.append(effectLst)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Traction & Roadmap",
    past_title: str = "PAST 9 MONTHS",
    future_title: str = "NEXT 9 MONTHS",
    color_past: tuple = (15, 23, 42),      # Dark Navy
    color_future: tuple = (255, 107, 107), # Vibrant Coral
    **kwargs
) -> str:
    """
    Creates a Dual-Phase Split Timeline slide typical in VC pitch decks.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Split Background ===
    # Left Half (Past)
    left_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(6.6665), Inches(7.5))
    left_bg.fill.solid()
    left_bg.fill.fore_color.rgb = RGBColor(*color_past)
    left_bg.line.fill.background()

    # Right Half (Future)
    right_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6665), 0, Inches(6.6665), Inches(7.5))
    right_bg.fill.solid()
    right_bg.fill.fore_color.rgb = RGBColor(*color_future)
    right_bg.line.fill.background()

    # === Layer 2: Main Axis Line ===
    # Horizontal line crossing both halves
    axis_y = Inches(4.2)
    axis = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(1.0), axis_y - Pt(2), Inches(11.333), Pt(4)
    )
    axis.fill.solid()
    axis.fill.fore_color.rgb = RGBColor(255, 255, 255)
    axis.line.fill.background()

    # Center Marker ("TODAY")
    center_y = axis_y - Inches(0.4)
    today_box = slide.shapes.add_textbox(Inches(6.0), center_y, Inches(1.333), Inches(0.5))
    tf = today_box.text_frame
    tf.text = "TODAY"
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    center_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.65), axis_y - Inches(0.2), Pt(3), Inches(0.4))
    center_line.fill.solid()
    center_line.fill.fore_color.rgb = RGBColor(255, 255, 255)
    center_line.line.fill.background()

    # === Layer 3: Section Headers ===
    def add_header(text, x, y, width, align):
        tb = slide.shapes.add_textbox(x, y, width, Inches(1.0))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = align
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
    
    add_header(past_title, Inches(1.0), Inches(0.5), Inches(5.0), PP_ALIGN.LEFT)
    add_header(future_title, Inches(7.333), Inches(0.5), Inches(5.0), PP_ALIGN.RIGHT)

    # Main Slide Title (Optional, subtle in top left)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.2), Inches(5.0), Inches(0.5))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text.upper()
    title_p.font.size = Pt(12)
    title_p.font.color.rgb = RGBColor(150, 160, 180) # Muted text
    title_p.font.bold = True

    # === Layer 4: Timeline Milestones ===
    milestones = [
        # Past (Left Side)
        {"date": "Sep '18", "metric": "€150K", "desc": "Seed Round", "x": 1.5, "is_top": True},
        {"date": "Jan '19", "metric": "€80K", "desc": "Monthly MRR", "x": 3.2, "is_top": False},
        {"date": "Jun '19", "metric": "1.2M", "desc": "Active Users", "x": 4.9, "is_top": True},
        # Future (Right Side)
        {"date": "Mar '20", "metric": "€1M", "desc": "Series A Target", "x": 8.0, "is_top": False},
        {"date": "Dec '20", "metric": "Microsoft", "desc": "B2B Partnership", "x": 10.0, "is_top": True},
        {"date": "Q4 '21", "metric": "5.0M", "desc": "Global Users", "x": 11.7, "is_top": False},
    ]

    node_radius = Inches(0.15)

    for i, ms in enumerate(milestones):
        # Draw Circular Node
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(ms['x']) - node_radius, 
            axis_y - node_radius, 
            node_radius * 2, 
            node_radius * 2
        )
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor(255, 255, 255)
        node.line.color.rgb = RGBColor(*color_past) if ms['x'] < 6.6 else RGBColor(*color_future)
        node.line.width = Pt(3)
        add_drop_shadow(node) # Add depth

        # Calculate Text Y positions
        box_width = Inches(2.0)
        box_x = Inches(ms['x']) - (box_width / 2)
        
        if ms['is_top']:
            tb_y = axis_y - Inches(1.8)
        else:
            tb_y = axis_y + Inches(0.4)

        # Draw Milestone Text Box
        tb = slide.shapes.add_textbox(box_x, tb_y, box_width, Inches(1.5))
        tf = tb.text_frame
        tf.clear()
        
        # Paragraph 1: Metric (Huge, Bold)
        p1 = tf.paragraphs[0]
        p1.text = ms['metric']
        p1.alignment = PP_ALIGN.CENTER
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(255, 255, 255)
        
        # Paragraph 2: Description
        p2 = tf.add_paragraph()
        p2.text = ms['desc']
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(255, 255, 255)
        
        # Paragraph 3: Date
        p3 = tf.add_paragraph()
        p3.text = ms['date']
        p3.alignment = PP_ALIGN.CENTER
        p3.font.size = Pt(12)
        p3.font.color.rgb = RGBColor(200, 200, 200) if ms['x'] < 6.6 else RGBColor(255, 200, 200)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
