def create_slide(
    output_pptx_path: str,
    title_text: str = "Microservices Architecture",
    body_text: str = "",
    bg_color: tuple = (20, 22, 28),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Neon-Dark Architectural Diagram.
    Generates a classic API Gateway to Microservices to Database flow.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml.xmlchemy import OxmlElement

    # 1. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # 2. Set Dark Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # Helper 1: XML injection for Neon Glow
    def apply_neon_glow(shape, color_rgb, radius_pt=8):
        spPr = shape.element.spPr
        effectLst = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        if effectLst is None:
            effectLst = OxmlElement('a:effectLst')
            spPr.append(effectLst)
        
        glow = OxmlElement('a:glow')
        # rad is in EMUs: 1 pt = 12700 EMUs
        glow.set('rad', str(int(radius_pt * 12700)))
        
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', f"{color_rgb[0]:02X}{color_rgb[1]:02X}{color_rgb[2]:02X}")
        
        glow.append(srgbClr)
        effectLst.append(glow)

    # Helper 2: Create a styled diagram node
    def add_neon_node(slide, text, x, y, w, h, color, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, font_color=(255,255,255), glow=True):
        shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color)
        
        # Transparent/no line
        shape.line.color.rgb = RGBColor(*color)
        shape.line.width = Pt(1.5)
        
        if glow:
            apply_neon_glow(shape, color, radius_pt=10)
            
        # Text styling
        text_frame = shape.text_frame
        text_frame.text = text
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        font = text_frame.paragraphs[0].font
        font.name = "Segoe UI"
        font.size = Pt(16)
        font.bold = True
        font.color.rgb = RGBColor(*font_color)
        
        # Adjust roundness if it's a rounded rect
        if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
            for adj in shape.adjustments:
                adj = 0.2 # Standardize pill roundness
                
        return shape

    # Helper 3: Add connector line
    def connect_shapes(slide, start_shape, end_shape):
        # Determine center points roughly to anchor lines
        sx = start_shape.left + (start_shape.width / 2)
        sy = start_shape.top + start_shape.height
        ex = end_shape.left + (end_shape.width / 2)
        ey = end_shape.top
        
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, sx, sy, ex, ey)
        connector.line.color.rgb = RGBColor(100, 100, 110)
        connector.line.width = Pt(2)
        # Add End Arrow
        line_props = connector.line
        # python-pptx doesn't have a direct enum property for arrows easily exposed without xml, 
        # but we can set it via oxml
        ln = connector.element.spPr.ln
        tailEnd = OxmlElement('a:tailEnd')
        tailEnd.set('type', 'triangle')
        tailEnd.set('w', 'med')
        tailEnd.set('len', 'med')
        ln.append(tailEnd)
        return connector

    # 3. Add Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # 4. Color Palette
    CYAN = (0, 212, 255)
    ORANGE = (255, 153, 0)
    GREEN = (0, 220, 120)
    PURPLE = (180, 0, 255)
    DARK_TEXT = (20, 22, 28)

    # 5. Build Diagram Nodes
    # Level 1: Client
    node_client = add_neon_node(slide, "User Interface\n(Web & Mobile)", 5.16, 1.5, 3.0, 0.8, PURPLE, font_color=tuple(DARK_TEXT))
    
    # Level 2: API Gateway
    node_gateway = add_neon_node(slide, "API Gateway", 3.16, 3.2, 7.0, 0.8, CYAN, font_color=tuple(DARK_TEXT))
    
    # Level 3: Microservices
    services = []
    service_names = ["User Service", "Order Service", "Payment Service"]
    for i, name in enumerate(service_names):
        x_pos = 1.66 + (i * 3.5)
        svc = add_neon_node(slide, name, x_pos, 4.8, 2.5, 0.8, ORANGE, font_color=tuple(DARK_TEXT))
        services.append(svc)
        
    # Level 4: Databases (Cylinders)
    databases = []
    for i in range(3):
        x_pos = 2.16 + (i * 3.5)
        # Using MSO_SHAPE.CAN for database icon
        db = add_neon_node(slide, "DB", x_pos, 6.2, 1.5, 1.0, GREEN, shape_type=MSO_SHAPE.CAN, font_color=tuple(DARK_TEXT))
        databases.append(db)

    # 6. Build Connections
    # Client -> Gateway
    connect_shapes(slide, node_client, node_gateway)
    
    # Gateway -> Services
    for svc in services:
        connect_shapes(slide, node_gateway, svc)
        
    # Services -> DBs
    for svc, db in zip(services, databases):
        connect_shapes(slide, svc, db)

    # 7. Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path
