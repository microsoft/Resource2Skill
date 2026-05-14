import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw, ImageFont

def create_slide(
    output_pptx_path: str,
    title_text: str = "Contoso Cloud Architecture (3-Tier)",
    **kwargs,
) -> str:
    """
    Creates a native PowerPoint architecture diagram featuring nested clusters (Subnets),
    generated service nodes, and directional flow arrows.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Add Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = "Segoe UI"
    p.font.color.rgb = RGBColor(50, 50, 50)

    # --- Helper 1: Generate Mock Icons using PIL ---
    def generate_icon(name, bg_color, text_color, filename):
        """Generates a rounded rectangle icon to represent a cloud service."""
        size = (150, 150)
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw rounded rectangle
        draw.rounded_rectangle([(10, 10), (140, 140)], radius=20, fill=bg_color, outline=text_color, width=4)
        
        # Draw text (Fallback to default font if custom isn't available)
        try:
            font = ImageFont.truetype("arialbd.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
            
        # Center text roughly
        text_w = draw.textlength(name, font=font)
        draw.text(((size[0]-text_w)/2, 60), name, fill=text_color, font=font)
        
        img.save(filename)
        return filename

    # Prepare icons (we will clean these up later)
    icons = {
        "User": generate_icon("User", (240, 240, 240), (80, 80, 80), "icon_user.png"),
        "FrontDoor": generate_icon("FD", (0, 120, 212), (255, 255, 255), "icon_fd.png"),
        "WebApp": generate_icon("Web", (0, 150, 250), (255, 255, 255), "icon_web.png"),
        "API": generate_icon("API", (128, 0, 128), (255, 255, 255), "icon_api.png"),
        "SQL": generate_icon("SQL", (0, 180, 100), (255, 255, 255), "icon_sql.png"),
    }

    # --- Helper 2: Draw Cluster Boundary (Subnet) ---
    def add_cluster(slide, x, y, w, h, name, bg_rgb, border_rgb):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
        
        # Make the background slightly transparent using XML injection
        fill_elem = shape.fill._xPr.solidFill
        alpha_xml = f'<a:alpha xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" val="30000"/>' # 30% opacity
        fill_elem.append(parse_xml(alpha_xml))

        shape.line.color.rgb = RGBColor(*border_rgb)
        shape.line.width = Pt(1.5)
        shape.line.dash_style = 7 # Dashed line
        
        # Label
        lbl = slide.shapes.add_textbox(x, y - Inches(0.1), w, Inches(0.4))
        p = lbl.text_frame.paragraphs[0]
        p.text = name
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(*border_rgb)
        return shape

    # --- Helper 3: Add Directed Connector Arrow (lxml) ---
    def add_flow_arrow(slide, start_x, start_y, end_x, end_y):
        connector = slide.shapes.add_connector(MSO_SHAPE.LINE_INVERSE, start_x, start_y, end_x, end_y)
        connector.line.color.rgb = RGBColor(100, 100, 100)
        connector.line.width = Pt(2)
        
        # Inject XML for arrowhead
        ln = connector.line._lineFormat.ln
        headEnd = parse_xml('<a:headEnd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" type="triangle" w="med" len="med"/>')
        
        # Clean up existing tailEnd/headEnd to avoid schema errors, then append
        for elem in ln.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}headEnd"):
            ln.remove(elem)
        ln.append(headEnd)
        return connector

    # --- Layout Construction ---
    
    # 1. Clusters (VNet/Subnets)
    vnet = add_cluster(slide, Inches(3.5), Inches(1.5), Inches(9), Inches(5.5), "VNet: contoso-prod-vnet", (230, 240, 255), (0, 120, 212))
    snet_web = add_cluster(slide, Inches(4.0), Inches(2.2), Inches(2.2), Inches(4.5), "snet-frontend", (255, 255, 255), (100, 150, 200))
    snet_app = add_cluster(slide, Inches(6.8), Inches(2.2), Inches(2.2), Inches(4.5), "snet-backend", (255, 255, 255), (100, 150, 200))
    snet_db = add_cluster(slide, Inches(9.6), Inches(2.2), Inches(2.2), Inches(4.5), "snet-data", (255, 255, 255), (100, 150, 200))

    # 2. Placement Coordinates (Nodes)
    nodes = {
        "Users": {"x": Inches(1.0), "y": Inches(4.0), "icon": icons["User"], "lbl": "Public Users"},
        "FrontDoor": {"x": Inches(2.5), "y": Inches(4.0), "icon": icons["FrontDoor"], "lbl": "Azure Front Door"},
        "Web1": {"x": Inches(4.6), "y": Inches(3.0), "icon": icons["WebApp"], "lbl": "Web App (UI)"},
        "Web2": {"x": Inches(4.6), "y": Inches(5.0), "icon": icons["WebApp"], "lbl": "Web App (UI)"},
        "API1": {"x": Inches(7.4), "y": Inches(3.0), "icon": icons["API"], "lbl": "Order API"},
        "API2": {"x": Inches(7.4), "y": Inches(5.0), "icon": icons["API"], "lbl": "Order API"},
        "SQL": {"x": Inches(10.2), "y": Inches(4.0), "icon": icons["SQL"], "lbl": "Azure SQL DB"},
    }

    # Draw Nodes and Labels
    icon_size = Inches(1.0)
    for key, data in nodes.items():
        slide.shapes.add_picture(data["icon"], data["x"], data["y"], width=icon_size, height=icon_size)
        lbl = slide.shapes.add_textbox(data["x"] - Inches(0.25), data["y"] + icon_size, Inches(1.5), Inches(0.4))
        p = lbl.text_frame.paragraphs[0]
        p.text = data["lbl"]
        p.font.size = Pt(10)
        p.font.name = "Segoe UI"
        p.alignment = 2 # Center alignment

    # 3. Draw Edges (Traffic Flow)
    def connect(n1, n2):
        # Calculate center-to-center connecting lines
        offset = icon_size / 2
        add_flow_arrow(slide, nodes[n2]["x"] + offset, nodes[n2]["y"] + offset, nodes[n1]["x"] + offset, nodes[n1]["y"] + offset)

    connect("FrontDoor", "Users")
    connect("Web1", "FrontDoor")
    connect("Web2", "FrontDoor")
    connect("API1", "Web1")
    connect("API2", "Web2")
    connect("API1", "Web2") # Load balancing cross-talk
    connect("API2", "Web1")
    connect("SQL", "API1")
    connect("SQL", "API2")

    # Cleanup temp images
    for img_path in icons.values():
        if os.path.exists(img_path):
            os.remove(img_path)

    prs.save(output_pptx_path)
    return output_pptx_path
