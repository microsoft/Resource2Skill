import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

def add_drop_shadow(shape, blur_rad=100000, dist=50000, alpha=20000):
    """
    Injects OpenXML to add a subtle outer drop shadow to a python-pptx shape.
    """
    shadow_xml = f"""
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="{blur_rad}" dist="{dist}" dir="2700000" algn="tl" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="{alpha}"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    effectLst = parse_xml(shadow_xml)
    shape.element.spPr.append(effectLst)

def create_slide(
    output_pptx_path: str,
    hub_title: str = "Agenda\nTemplate",
    agenda_items: list = None,
    palette: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Connected Circular Node Agenda.
    """
    if agenda_items is None:
        agenda_items = [
            ("Introduction", "Welcome and greetings, overview of meeting purpose and objectives."),
            ("Project Overview", "Summary of the main subject, background info, and progress so far."),
            ("Main Discussion", "Core content is discussed here, focusing on key ideas and challenges."),
            ("Action Plan", "Practical steps that need to be taken moving forward. Define responsibilities."),
            ("Q&A and Closing", "Open floor for questions, clarify doubts, and final remarks.")
        ]
        
    if palette is None:
        # Default professional palette: Blue, Teal, Purple, Orange, Yellow
        palette = [
            (33, 158, 188),   # Blue
            (42, 157, 143),   # Teal
            (114, 9, 183),    # Purple
            (244, 162, 97),   # Orange
            (233, 196, 106)   # Yellow
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Set background color to very light gray
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(250, 250, 250)

    # === Central Hub Variables ===
    center_x = Inches(3.5)
    center_y = Inches(3.75)
    outer_radius = Inches(2.3)
    inner_radius = Inches(1.6)

    # 1. Outer Light Gray Circle
    outer_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        center_x - outer_radius, center_y - outer_radius, 
        outer_radius * 2, outer_radius * 2
    )
    outer_circle.fill.solid()
    outer_circle.fill.fore_color.rgb = RGBColor(235, 235, 235)
    outer_circle.line.fill.background() # No line

    # 2. Inner Colored Circle
    inner_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        center_x - inner_radius, center_y - inner_radius, 
        inner_radius * 2, inner_radius * 2
    )
    inner_circle.fill.solid()
    inner_circle.fill.fore_color.rgb = RGBColor(38, 70, 83) # Dark Slate/Teal
    inner_circle.line.fill.background()
    add_drop_shadow(inner_circle)

    # Add text to inner circle
    text_frame = inner_circle.text_frame
    text_frame.text = hub_title
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    for paragraph in text_frame.paragraphs:
        paragraph.font.size = Pt(32)
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(255, 255, 255)

    # === Radial Layout & Cards Variables ===
    num_items = len(agenda_items)
    
    # Angles for the nodes on the arc (spanning from -50 to +50 degrees on the right side)
    # 0 degrees is strictly right (3 o'clock). Negative is up, Positive is down.
    start_angle = -55
    end_angle = 55
    if num_items > 1:
        angle_step = (end_angle - start_angle) / (num_items - 1)
    else:
        angle_step = 0
        start_angle = 0

    # Card dimensions and positioning
    card_w = Inches(5.5)
    card_h = Inches(0.85)
    card_x = Inches(7.2)
    
    # Calculate vertical spacing for cards
    total_cards_height = num_items * card_h
    available_height = Inches(6.0)
    spacing = (available_height - total_cards_height) / (num_items - 1) if num_items > 1 else 0
    start_y = center_y - (available_height / 2)

    # === Draw Nodes, Connectors, and Cards ===
    for i in range(num_items):
        color_rgb = RGBColor(*palette[i % len(palette)])
        
        # Calculate Card Y Position
        card_y = start_y + i * (card_h + spacing)
        card_mid_y = card_y + (card_h / 2)

        # Calculate Arc Node Position
        angle_deg = start_angle + i * angle_step
        angle_rad = math.radians(angle_deg)
        # Using a radius slightly smaller than outer circle for the connection points
        node_radius = outer_radius * 0.95 
        node_x = center_x + node_radius * math.cos(angle_rad)
        node_y = center_y + node_radius * math.sin(angle_rad)

        # 3. Draw Connector Line
        connector = slide.shapes.add_connector(
            1, # straight line
            node_x, node_y, card_x, card_mid_y
        )
        connector.line.color.rgb = color_rgb
        connector.line.width = Pt(1.5)
        connector.line.dash_style = 4 # Dashed line format

        # 4. Draw Node Dot
        dot_radius = Inches(0.12)
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            node_x - dot_radius, node_y - dot_radius,
            dot_radius * 2, dot_radius * 2
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = color_rgb
        dot.line.color.rgb = RGBColor(255, 255, 255)
        dot.line.width = Pt(2)

        # 5. Draw Content Card (Outer container)
        card_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            card_x, card_y, card_w, card_h
        )
        card_box.fill.solid()
        card_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card_box.line.color.rgb = color_rgb
        card_box.line.width = Pt(1)
        
        # 6. Draw Icon Container (Left side block)
        icon_w = Inches(0.8)
        icon_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            card_x + Inches(0.05), card_y + Inches(0.05), icon_w, card_h - Inches(0.1)
        )
        icon_box.fill.solid()
        icon_box.fill.fore_color.rgb = color_rgb
        icon_box.line.fill.background()

        # 7. Add Text to Card
        txBox = slide.shapes.add_textbox(
            card_x + icon_w + Inches(0.1), card_y, card_w - icon_w - Inches(0.1), card_h
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        
        # Title
        p_title = tf.paragraphs[0]
        p_title.text = agenda_items[i][0]
        p_title.font.bold = True
        p_title.font.size = Pt(14)
        p_title.font.color.rgb = RGBColor(50, 50, 50)
        
        # Description
        p_desc = tf.add_paragraph()
        p_desc.text = agenda_items[i][1]
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = RGBColor(100, 100, 100)

    prs.save(output_pptx_path)
    return output_pptx_path
