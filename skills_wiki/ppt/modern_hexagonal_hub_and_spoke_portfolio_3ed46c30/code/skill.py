import math
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree
from PIL import Image, ImageDraw

def _apply_subtle_shadow(shape):
    """Injects openXML to add a subtle drop shadow to a shape."""
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    p = "http://schemas.openxmlformats.org/presentationml/2006/main"
    spPr = shape.element.find('.//p:spPr', namespaces={'p': p})
    if spPr is not None:
        effectLst = etree.SubElement(spPr, f'{{{a}}}effectLst')
        outerShdw = etree.SubElement(effectLst, f'{{{a}}}outerShdw', 
                                     blurRad="50800", dist="38100", dir="5400000", algn="ctr", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, f'{{{a}}}srgbClr', val="000000")
        etree.SubElement(srgbClr, f'{{{a}}}alpha', val="15000") # 15% opacity

def _create_honeycomb_bg(filepath, width=1920, height=1080):
    """Generates a subtle tech/corporate honeycomb pattern background."""
    img = Image.new("RGBA", (width, height), (252, 252, 254, 255))
    draw = ImageDraw.Draw(img)
    
    r = 60 # Hexagon radius
    w = 2 * r
    h = math.sqrt(3) * r
    
    x_spacing = 0.75 * w
    y_spacing = h
    
    cols = int(width / x_spacing) + 2
    rows = int(height / y_spacing) + 2
    
    for row in range(rows):
        for col in range(cols):
            cx = col * x_spacing
            cy = row * y_spacing
            if col % 2 == 1:
                cy += y_spacing / 2
                
            pts = []
            for i in range(6):
                # Flat-top hexagon corners: 30, 90, 150, 210, 270, 330 degrees
                angle_rad = math.radians(60 * i - 30)
                px = cx + r * math.cos(angle_rad)
                py = cy + r * math.sin(angle_rad)
                pts.append((px, py))
            draw.polygon(pts, outline=(235, 235, 240, 255), width=2)
            
    img.save(filepath)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Corporate Ecosystem & Portfolio",
    body_text: str = "",
    bg_palette: str = "corporate",
    accent_color: tuple = (219, 20, 60), # Default Crimson Red
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modern Hexagonal Hub-and-Spoke visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Geometric Background ===
    bg_path = "temp_honeycomb_bg.png"
    _create_honeycomb_bg(bg_path, width=1920, height=1080)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    os.remove(bg_path) # Cleanup

    # === Slide Title ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(10), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(40, 40, 45)

    # === Data Setup ===
    default_nodes = [
        {"title": "Knorr", "desc": "Sector: Food\nRegion: Germany\nEst: 1838", "angle": 270},
        {"title": "Lux", "desc": "Sector: Soap\nRegion: UK\nEst: 1925", "angle": 330},
        {"title": "Lipton", "desc": "Sector: Tea\nRegion: UK\nEst: 1890", "angle": 30},
        {"title": "Sunsilk", "desc": "Sector: Hair Care\nRegion: UK\nEst: 1954", "angle": 90},
        {"title": "Dove", "desc": "Sector: Personal Care\nRegion: UK\nEst: 1955", "angle": 150},
        {"title": "Magnum", "desc": "Sector: Ice Cream\nRegion: Belgium\nEst: 1989", "angle": 210}
    ]
    nodes = kwargs.get("nodes", default_nodes)
    center_title = kwargs.get("center_title", "CORE\nHUB")

    # === Layout Mathematics ===
    cx = Inches(13.333 / 2)
    cy = Inches(7.5 / 2) + Inches(0.2) # Slightly lower to account for title
    
    # Hexagon sizing (maintaining mathematically accurate sqrt(3) aspect ratio for flat-top)
    center_hex_w = Inches(2.4)
    center_hex_h = Inches(2.08)
    node_hex_w = Inches(1.6)
    node_hex_h = Inches(1.38)
    R = Inches(2.7) # Distance from center to nodes

    # === Layer 2: Connectors (Drawn first to remain behind shapes) ===
    for node in nodes:
        angle_rad = math.radians(node['angle'])
        nx = cx + R * math.cos(angle_rad)
        ny = cy + R * math.sin(angle_rad)
        
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, cx, cy, nx, ny)
        conn.line.width = Pt(2)
        conn.line.color.rgb = RGBColor(210, 210, 215)

    # === Layer 3: Central Hub ===
    center_shape = slide.shapes.add_shape(
        MSO_SHAPE.HEXAGON, cx - center_hex_w/2, cy - center_hex_h/2, center_hex_w, center_hex_h
    )
    center_shape.fill.solid()
    center_shape.fill.fore_color.rgb = RGBColor(*accent_color)
    center_shape.line.fill.background() # No border
    _apply_subtle_shadow(center_shape)

    tf_center = center_shape.text_frame
    tf_center.clear()
    for i, line in enumerate(center_title.split('\n')):
        p = tf_center.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(20) if i == 0 else Pt(16)
        p.font.color.rgb = RGBColor(255, 255, 255)
    tf_center.vertical_anchor = MSO_ANCHOR.MIDDLE

    # === Layer 4: Satellite Nodes & Details ===
    for node in nodes:
        angle_rad = math.radians(node['angle'])
        nx = cx + R * math.cos(angle_rad)
        ny = cy + R * math.sin(angle_rad)
        
        # Node Shape
        node_shape = slide.shapes.add_shape(
            MSO_SHAPE.HEXAGON, nx - node_hex_w/2, ny - node_hex_h/2, node_hex_w, node_hex_h
        )
        node_shape.fill.solid()
        node_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        node_shape.line.solid()
        node_shape.line.fore_color.rgb = RGBColor(*accent_color)
        node_shape.line.width = Pt(2.5)
        _apply_subtle_shadow(node_shape)
        
        # Node Title
        tf_node = node_shape.text_frame
        tf_node.text = node['title']
        tf_node.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf_node.paragraphs[0].font.bold = True
        tf_node.paragraphs[0].font.size = Pt(14)
        tf_node.paragraphs[0].font.color.rgb = RGBColor(50, 50, 55)
        tf_node.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        # Detail Text Box setup and placement logic
        text_w = Inches(2.0)
        text_h = Inches(1.0)
        
        # Alignment logic based on spatial position relative to center
        if nx < cx - Inches(0.1): 
            tx = nx - node_hex_w/2 - text_w - Inches(0.2)
            align = PP_ALIGN.RIGHT
        else: 
            tx = nx + node_hex_w/2 + Inches(0.2)
            align = PP_ALIGN.LEFT
            
        ty = ny - text_h/2
        
        tb = slide.shapes.add_textbox(tx, ty, text_w, text_h)
        tf_detail = tb.text_frame
        tf_detail.clear()
        tf_detail.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        # Parse and stylize detail lines (Bold keys, normal values)
        details = node['desc'].split('\n')
        for i, detail in enumerate(details):
            p = tf_detail.add_paragraph() if i > 0 else tf_detail.paragraphs[0]
            p.alignment = align
            
            if ":" in detail:
                parts = detail.split(":", 1)
                p.text = parts[0] + ":"
                p.font.size = Pt(11)
                p.font.bold = True
                p.font.color.rgb = RGBColor(80, 80, 85)
                
                run = p.add_run()
                run.text = parts[1]
                run.font.bold = False
                run.font.size = Pt(11)
                run.font.color.rgb = RGBColor(140, 140, 145)
            else:
                p.text = detail
                p.font.size = Pt(11)
                p.font.color.rgb = RGBColor(100, 100, 105)

    prs.save(output_pptx_path)
    return output_pptx_path
