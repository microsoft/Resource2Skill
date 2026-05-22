def create_slide(
    output_pptx_path: str,
    title_text: str = "Process Flow Diagram",
    body_text: str = "",
    bg_palette: str = "cyan",
    accent_color: tuple = (243, 156, 18),  # Orange for arrows
    node_color: tuple = (30, 142, 142),    # Dark Teal for shapes
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'High-Contrast Branching Process Diagram' visual effect.
    Returns: path to the saved PPTX file.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    from lxml import etree

    # === 1. Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # === 2. Generate Background (PIL Radial Gradient) ===
    bg_img_path = "temp_bg_radial.png"
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    center_x, center_y = width / 2, height / 2
    max_radius = 1200
    
    for r in range(max_radius, 0, -4):
        # Soft transition from light cyan at edges to off-white at center
        ratio = r / max_radius
        red = int(250 - (250 - 210) * ratio)
        green = int(252 - (252 - 235) * ratio)
        blue = int(252 - (252 - 240) * ratio)
        draw.ellipse(
            (center_x - r, center_y - r, center_x + r, center_y + r),
            fill=(red, green, blue)
        )
    img.save(bg_img_path)
    
    # Insert background
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # Add Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(5), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = 'Century Gothic'
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(50, 50, 50)

    # === 3. Define Shape Creation Helper ===
    def add_node(shape_type, x, y, w, h, text):
        shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
        # Fill
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*node_color)
        # Outline
        shape.line.color.rgb = RGBColor(255, 255, 255)
        shape.line.width = Pt(2.5)
        # Text
        tf = shape.text_frame
        tf.text = text
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = 'Century Gothic'
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(255, 255, 255)
        return shape

    # === 4. Place Nodes ===
    # Standard connection sites: 0=Top, 1=Left, 2=Bottom, 3=Right
    start_node = add_node(MSO_SHAPE.OVAL, 0.8, 3.25, 1.0, 1.0, "START")
    decision_node = add_node(MSO_SHAPE.DIAMOND, 2.5, 3.0, 1.5, 1.5, "DECISION")
    
    proc1_node = add_node(MSO_SHAPE.RECTANGLE, 5.0, 1.5, 2.0, 1.0, "PROCESS 1")
    proc2_node = add_node(MSO_SHAPE.RECTANGLE, 5.0, 3.25, 2.0, 1.0, "PROCESS 2")
    proc3_node = add_node(MSO_SHAPE.RECTANGLE, 5.0, 5.0, 2.0, 1.0, "PROCESS 3")
    
    action_node = add_node(MSO_SHAPE.PARALLELOGRAM, 8.0, 3.25, 2.0, 1.0, "ACTION")
    end_node = add_node(MSO_SHAPE.OVAL, 11.0, 3.25, 1.0, 1.0, "END")

    # === 5. Define Connector Helper (with lxml arrowhead injection) ===
    def add_flow_connector(node_a, site_a, node_b, site_b, c_type=MSO_CONNECTOR.STRAIGHT):
        # Create a connector
        connector = slide.shapes.add_connector(c_type, 0, 0, 0, 0)
        # Connect it to the shapes
        connector.begin_connect(node_a, site_a)
        connector.end_connect(node_b, site_b)
        
        # Style line
        connector.line.color.rgb = RGBColor(*accent_color)
        connector.line.width = Pt(2.5)
        
        # Inject XML for large triangle arrowhead
        line_props = connector.line._lineProperties
        nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        
        # Check if tailEnd exists, if not create it
        tail_end = line_props.find('a:tailEnd', namespaces=nsmap)
        if tail_end is None:
            tail_end = etree.SubElement(line_props, '{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd')
        
        tail_end.set('type', 'triangle')
        tail_end.set('w', 'lrg')
        tail_end.set('len', 'lrg')
        
        return connector

    # === 6. Route Connectors ===
    # Start -> Decision
    add_flow_connector(start_node, 3, decision_node, 1, MSO_CONNECTOR.STRAIGHT)
    
    # Decision -> Processes
    add_flow_connector(decision_node, 0, proc1_node, 1, MSO_CONNECTOR.ELBOW)
    add_flow_connector(decision_node, 3, proc2_node, 1, MSO_CONNECTOR.STRAIGHT)
    add_flow_connector(decision_node, 2, proc3_node, 1, MSO_CONNECTOR.ELBOW)
    
    # Processes -> Action
    add_flow_connector(proc1_node, 3, action_node, 0, MSO_CONNECTOR.ELBOW)
    add_flow_connector(proc2_node, 3, action_node, 1, MSO_CONNECTOR.STRAIGHT)
    add_flow_connector(proc3_node, 3, action_node, 2, MSO_CONNECTOR.ELBOW)
    
    # Action -> End
    add_flow_connector(action_node, 3, end_node, 1, MSO_CONNECTOR.STRAIGHT)

    # === 7. Save and Cleanup ===
    prs.save(output_pptx_path)
    
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
