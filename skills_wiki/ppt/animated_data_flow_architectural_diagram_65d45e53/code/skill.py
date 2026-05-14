def create_slide(
    output_pptx_path: str,
    title_text: str = "Animated Architecture Flow",
    body_text: str = "",
    bg_palette: str = "tech",
    accent_color: tuple = (0, 191, 255),  # Cyan data packet
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Animated Data Flow Diagram' effect.
    Uses PPTX Morph transitions across 3 slides to simulate data packets moving
    through a tech architecture (Client -> Server -> Database).
    """
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.dml.color import RGBColor
    from pptx.util import Inches, Pt
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Colors ---
    COLOR_NODE = RGBColor(44, 62, 80)      # Dark Slate
    COLOR_LINE = RGBColor(189, 195, 199)   # Light Gray
    COLOR_PACKET = RGBColor(*accent_color) # Moving Packet Color
    COLOR_BG = RGBColor(248, 249, 250)     # Off-white

    def apply_morph_transition(slide):
        """Injects PPTX Morph transition XML into a slide for fluid animation."""
        # Namespace map for PowerPoint transitions
        nsmap = {
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'
        }
        
        # Get the slide's XML root (p:sld)
        sld = slide._element
        
        # Create transition element: <p:transition spd="slow"><p14:morph option="byObject"/></p:transition>
        transition = etree.Element(f"{{{nsmap['p']}}}transition", spd="slow")
        morph = etree.SubElement(transition, f"{{{nsmap['p14']}}}morph", option="byObject")
        
        # Find if a transition already exists and replace it, or append new
        existing_transition = sld.find(f"{{{nsmap['p']}}}transition")
        if existing_transition is not None:
            sld.replace(existing_transition, transition)
        else:
            # Transition must be inserted before timing/extLst elements if they exist, 
            # but usually appending near the end of standard slide XML works.
            timing = sld.find(f"{{{nsmap['p']}}}timing")
            if timing is not None:
                timing.addprevious(transition)
            else:
                sld.append(transition)

    def build_architecture_slide(slide, packet_position_index):
        """
        Builds the static architecture.
        packet_position_index determines where the 'moving dot' is placed.
        0: At Client, 1: At Server, 2: At Database
        """
        # Set Background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1))
        tf = title_box.text_frame
        p = tf.add_paragraph()
        p.text = title_text
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = COLOR_NODE

        # Subtitle
        p2 = tf.add_paragraph()
        p2.text = "Advance slide to see data flow animation"
        p2.font.size = Pt(16)
        p2.font.color.rgb = RGBColor(127, 140, 141)

        # --- Node Coordinates ---
        node_width = Inches(1.5)
        node_height = Inches(1.5)
        y_center = Inches(3.5)
        
        pos_client = (Inches(2), y_center)
        pos_server = (Inches(6), y_center)
        pos_db = (Inches(10), y_center)

        # --- Create Nodes ---
        # 1. Client (Rectangle)
        client = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pos_client[0], pos_client[1], node_width, node_height)
        client.fill.solid()
        client.fill.fore_color.rgb = COLOR_NODE
        client.line.color.rgb = COLOR_NODE
        client.text = "Client\n(Web/App)"
        
        # 2. Server (Rectangle)
        server = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pos_server[0], pos_server[1], node_width, node_height)
        server.fill.solid()
        server.fill.fore_color.rgb = COLOR_NODE
        server.line.color.rgb = COLOR_NODE
        server.text = "API Gateway\n(Microservice)"

        # 3. Database (Cylinder)
        db = slide.shapes.add_shape(MSO_SHAPE.CAN, pos_db[0], pos_db[1], node_width, node_height)
        db.fill.solid()
        db.fill.fore_color.rgb = COLOR_NODE
        db.line.color.rgb = COLOR_NODE
        db.text = "Database\n(PostgreSQL)"

        # --- Connectors ---
        # Client to Server
        conn1 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, pos_client[0] + node_width, pos_client[1] + node_height/2, pos_server[0], pos_server[1] + node_height/2)
        conn1.line.color.rgb = COLOR_LINE
        conn1.line.width = Pt(3)
        conn1.line.dash_style = 4 # Dashed

        # Server to DB
        conn2 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, pos_server[0] + node_width, pos_server[1] + node_height/2, pos_db[0], pos_db[1] + node_height/2)
        conn2.line.color.rgb = COLOR_LINE
        conn2.line.width = Pt(3)
        conn2.line.dash_style = 4 # Dashed

        # --- Data Packet (The Animated Element) ---
        packet_radius = Inches(0.3)
        
        # Calculate packet coordinates based on state
        if packet_position_index == 0:
            px, py = pos_client[0] + node_width + Inches(0.2), pos_client[1] + node_height/2 - packet_radius/2
        elif packet_position_index == 1:
            px, py = pos_server[0] + node_width + Inches(0.2), pos_server[1] + node_height/2 - packet_radius/2
        else:
            px, py = pos_db[0] - packet_radius - Inches(0.2), pos_db[1] + node_height/2 - packet_radius/2

        packet = slide.shapes.add_shape(MSO_SHAPE.OVAL, px, py, packet_radius, packet_radius)
        packet.fill.solid()
        packet.fill.fore_color.rgb = COLOR_PACKET
        packet.line.fill.background()
        
        # VERY IMPORTANT: To ensure PPTX Morph works perfectly, name the shape exactly the same across slides with '!!' prefix
        packet.name = "!!DataPacket"

    # --- Generate Sequence ---
    # Slide 1: Packet at Client
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    build_architecture_slide(slide1, 0)

    # Slide 2: Packet at Server
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    build_architecture_slide(slide2, 1)
    apply_morph_transition(slide2)

    # Slide 3: Packet at Database
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])
    build_architecture_slide(slide3, 2)
    apply_morph_transition(slide3)

    prs.save(output_pptx_path)
    return output_pptx_path
