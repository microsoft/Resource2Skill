import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "Animated Architecture Data Flow",
    body_text: str = "",
    bg_palette: str = "dark", 
    accent_color: tuple = (255, 215, 0),  # Bright Yellow data packet
    **kwargs,
) -> str:
    """
    Creates a multi-slide presentation simulating data flow through an architecture 
    using the Morph transition and auto-advance timings.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define colors
    bg_color = RGBColor(20, 15, 35) # Dark Purple/Navy
    node_color = RGBColor(45, 50, 75)
    line_color = RGBColor(100, 105, 130)
    text_color = RGBColor(200, 200, 220)
    packet_color = RGBColor(*accent_color)
    
    # Define our architecture nodes (Name, X, Y, Width, Height)
    nodes = {
        "Client": (Inches(1), Inches(3)),
        "API Gateway": (Inches(5), Inches(1.5)),
        "Auth Server": (Inches(5), Inches(5)),
        "Backend System": (Inches(9), Inches(3)),
        "Database": (Inches(11.5), Inches(3))
    }
    
    # Define the "Path" the data packet will take (sequence of coordinates)
    # Start -> Client -> API -> Auth -> API -> Backend -> DB
    flow_path = [
        (Inches(0), Inches(3.5)), # Off screen start
        (Inches(1.5), Inches(3.5)), # At Client
        (Inches(5.5), Inches(2.0)), # At API Gateway
        (Inches(5.5), Inches(5.5)), # At Auth Server
        (Inches(5.5), Inches(2.0)), # Back to API Gateway
        (Inches(9.5), Inches(3.5)), # At Backend
        (Inches(12.0), Inches(3.5)) # At Database
    ]
    
    # We will create one slide per step in the flow path
    for step_idx, packet_pos in enumerate(flow_path):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
        
        # --- 1. Set Background Color ---
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color
        
        # --- 2. Draw the Static Architecture Diagram ---
        # Draw connection lines first (so they are under the nodes)
        lines = [
            (nodes["Client"], nodes["API Gateway"]),
            (nodes["API Gateway"], nodes["Auth Server"]),
            (nodes["API Gateway"], nodes["Backend System"]),
            (nodes["Backend System"], nodes["Database"])
        ]
        
        for start_node, end_node in lines:
            # Connect centers
            sx, sy = start_node[0] + Inches(0.5), start_node[1] + Inches(0.5)
            ex, ey = end_node[0] + Inches(0.5), end_node[1] + Inches(0.5)
            connector = slide.shapes.add_connector(MSO_SHAPE.LINE_INVERSE, sx, sy, ex, ey)
            connector.line.color.rgb = line_color
            connector.line.width = Pt(2)
        
        # Draw Nodes
        for name, (x, y) in nodes.items():
            box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(1.5), Inches(1))
            box.fill.solid()
            box.fill.fore_color.rgb = node_color
            box.line.color.rgb = line_color
            box.line.width = Pt(1.5)
            
            # Node Text
            tf = box.text_frame
            tf.text = name
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.paragraphs[0].font.size = Pt(12)
            tf.paragraphs[0].font.color.rgb = text_color
            tf.paragraphs[0].font.bold = True
            
        # Add a title to the diagram
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(1))
        title_box.text_frame.text = title_text
        title_box.text_frame.paragraphs[0].font.size = Pt(24)
        title_box.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

        # --- 3. Draw the moving "Actor" (Data Packet) ---
        # The key to morphing is keeping the object properties consistent.
        packet_x, packet_y = packet_pos
        # We draw a small circle representing the packet
        packet = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            packet_x - Inches(0.15), 
            packet_y - Inches(0.15), 
            Inches(0.3), 
            Inches(0.3)
        )
        packet.fill.solid()
        packet.fill.fore_color.rgb = packet_color
        packet.line.fill.background() # No line
        # Naming the shape identically across slides ensures PowerPoint morphs it perfectly
        packet.name = "!!DataPacket" 

        # --- 4. Inject LXML to force Morph Transition and Auto-Advance ---
        # We want the transition to be "Morph", advance on click = False, advance after 0.5s (500ms)
        # Note: We do this for all slides except the first one (which just appears).
        if step_idx > 0:
            slide_elem = slide.element
            
            # Define namespace
            p_ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'
            
            # Create <p:transition advClick="0" advTm="500">
            transition = etree.Element(f'{{{p_ns}}}transition', advClick="0", advTm="500")
            
            # Create <p:morph option="byObject"/>
            morph = etree.SubElement(transition, f'{{{p_ns}}}morph', option="byObject")
            
            # Append transition to the slide XML element
            slide_elem.append(transition)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
