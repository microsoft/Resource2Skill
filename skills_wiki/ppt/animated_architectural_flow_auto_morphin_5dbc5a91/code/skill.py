import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image, ImageDraw

def _create_dark_gradient_bg(filename, width=1920, height=1080):
    """Generates a deep cosmic dark gradient for the background."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Deep navy to dark purple gradient
    color_top = (10, 15, 30)
    color_bottom = (25, 10, 40)
    
    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / height))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / height))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    img.save(filename)
    return filename

def _add_glow_effect(shape, color_hex="FFD700", radius_pt=15):
    """Injects an <a:glow> element into the shape's XML properties."""
    spPr = shape.element.spPr
    
    # Find or create effectLst
    effectLst = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    if effectLst is None:
        effectLst = OxmlElement('a:effectLst')
        spPr.append(effectLst)
        
    # Create glow element
    glow = OxmlElement('a:glow')
    glow.set('rad', str(int(radius_pt * 12700))) # Convert points to EMUs
    
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', color_hex)
    glow.append(srgbClr)
    
    effectLst.append(glow)

def _add_morph_and_auto_advance(slide, duration_ms=500, advance_ms=0):
    """Injects the Morph transition and Auto-advance timer into the slide XML."""
    sld = slide.element
    
    # Create transition element
    transition = OxmlElement('p:transition')
    transition.set('spd', 'fast')
    transition.set('advClick', '0')
    transition.set('advTm', str(advance_ms))
    
    # Create morph specific elements (PowerPoint 2016+ extension)
    extLst = OxmlElement('p:extLst')
    ext = OxmlElement('p:ext')
    ext.set('uri', '{C57A40D1-1C30-4663-8FDC-6A0ABBE0BAE1}')
    
    morph = OxmlElement('p15:morph')
    morph.set('xmlns:p15', 'http://schemas.microsoft.com/office/mac/powerpoint/2012/main')
    morph.set('option', 'byObject')
    
    ext.append(morph)
    extLst.append(ext)
    transition.append(extLst)
    
    # Insert right after <p:cSld>
    cSld = sld.find('{http://schemas.openxmlformats.org/presentationml/2006/main}cSld')
    index = sld.index(cSld) + 1
    sld.insert(index, transition)

def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Creates an animated PowerPoint presentation demonstrating architectural flow 
    using duplicated slides, glowing particles, and automated Morph transitions.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    bg_img_path = "temp_bg.png"
    _create_dark_gradient_bg(bg_img_path)

    # Define the static architecture nodes
    nodes = {
        "Client":     {"x": 1.0, "y": 3.25, "w": 2.0, "h": 1.0, "color": (50, 70, 150)},
        "API Gateway":{"x": 4.5, "y": 3.25, "w": 2.0, "h": 1.0, "color": (150, 50, 150)},
        "Lambda 1":   {"x": 8.0, "y": 1.50, "w": 2.0, "h": 1.0, "color": (200, 100, 50)},
        "Lambda 2":   {"x": 8.0, "y": 5.00, "w": 2.0, "h": 1.0, "color": (200, 100, 50)},
        "Database":   {"x": 11.0,"y": 3.25, "w": 1.5, "h": 1.5, "color": (50, 150, 100)},
    }
    
    # Define the exact animation path (coordinates for the glowing orb to travel)
    # The orb will pause at these precise locations across successive slides
    packet_path = [
        (1.9, 3.75),   # Start at Client
        (3.0, 3.75),   # Midpoint 1
        (4.4, 3.75),   # Hit API Gateway
        (5.5, 3.75),   # Inside API Gateway
        (6.75, 2.0),   # Route to Lambda 1
        (7.9, 2.0),    # Hit Lambda 1
        (10.2, 3.75),  # Route to DB
        (11.0, 4.0),   # Hit DB
    ]
    
    blank_layout = prs.slide_layouts[6]
    
    # Generate one slide for each step in the path
    for i, packet_pos in enumerate(packet_path):
        slide = prs.slides.add_slide(blank_layout)
        
        # 1. Add Background
        slide.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)
        
        # 2. Add Architecture Title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(5), Inches(1))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "System Data Flow Animation"
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.bold = True
        
        # 3. Draw Static Architecture Connections (Lines)
        shapes = slide.shapes
        def draw_line(x1, y1, x2, y2):
            line = shapes.add_connector(MSO_SHAPE.LINE_INVERSE, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
            line.line.color.rgb = RGBColor(100, 100, 150)
            line.line.width = Pt(2)
            
        draw_line(3.0, 3.75, 4.5, 3.75) # Client to API
        draw_line(6.5, 3.75, 8.0, 2.0)  # API to L1
        draw_line(6.5, 3.75, 8.0, 5.5)  # API to L2
        draw_line(10.0, 2.0, 11.0, 4.0) # L1 to DB
        draw_line(10.0, 5.5, 11.0, 4.0) # L2 to DB
        
        # 4. Draw Static Nodes (Servers/Services)
        for name, props in nodes.items():
            shape = shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(props["x"]), Inches(props["y"]), 
                Inches(props["w"]), Inches(props["h"])
            )
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(*props["color"])
            shape.line.color.rgb = RGBColor(255, 255, 255)
            shape.line.width = Pt(1.5)
            
            tf = shape.text_frame
            tf.text = name
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.paragraphs[0].font.size = Pt(16)
            tf.paragraphs[0].font.bold = True
            
        # 5. Draw the Dynamic "Data Packet" (Glowing Orb)
        # Using a small circle
        orb_size = 0.3
        packet = shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(packet_pos[0] - (orb_size/2)), 
            Inches(packet_pos[1] - (orb_size/2)), 
            Inches(orb_size), Inches(orb_size)
        )
        packet.fill.solid()
        packet.fill.fore_color.rgb = RGBColor(255, 255, 0) # Bright Yellow
        packet.line.fill.background() # No border
        
        # Name shape with '!!' prefix to force strict Morph matching across slides
        packet.name = "!!DataPacketOrb"
        
        # Inject custom XML for the neon glow
        _add_glow_effect(packet, color_hex="FFC000", radius_pt=18)
        
        # 6. Apply Auto-Advancing Morph Transition
        # We apply this to all slides except the very first one, 
        # so that entering slide 2, 3, etc., triggers the Morph.
        if i > 0:
            # advance_ms=100 means the slide waits 0.1s before moving to the next
            # creating a continuous flow effect
            _add_morph_and_auto_advance(slide, duration_ms=400, advance_ms=100)

    prs.save(output_pptx_path)
    
    # Cleanup temporary files
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
