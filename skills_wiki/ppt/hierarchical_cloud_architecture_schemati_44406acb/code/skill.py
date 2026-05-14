import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml

def add_drop_shadow(shape):
    """Injects OpenXML to add a subtle drop shadow to a shape for elevation."""
    shadow_xml = '''
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="40000" dist="30000" dir="2700000" algn="tl" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="15000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    '''
    shape.element.spPr.append(parse_xml(shadow_xml))

def create_container(slide, title, x, y, w, h, fill_color=None, border_color=(154, 160, 166), dashed=False):
    """Creates a logical boundary box with a top-left label."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    
    # Styling
    shape.line.color.rgb = RGBColor(*border_color)
    shape.line.width = Pt(1.5)
    if dashed:
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*fill_color)
    else:
        shape.fill.background() # Transparent
        
    # Adjust corner roundness
    shape.adjustments[0] = 0.05
    
    # Container Label
    text_frame = shape.text_frame
    text_frame.clear()
    p = text_frame.paragraphs[0]
    p.text = title
    p.font.name = 'Arial'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(95, 99, 104)
    
    # Align Top-Left
    text_frame.vertical_anchor = MSO_ANCHOR.TOP
    p.alignment = PP_ALIGN.LEFT
    text_frame.margin_left = Pt(10)
    text_frame.margin_top = Pt(10)
    
    return shape

def create_node(slide, text, x, y, accent_color=(66, 133, 244)):
    """Creates a service node with a drop shadow and an accent border."""
    w, h = 1.4, 0.8
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    
    # Styling
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    shape.line.color.rgb = RGBColor(*accent_color)
    shape.line.width = Pt(2)
    shape.adjustments[0] = 0.15 # More rounded corners
    
    # Add XML shadow
    add_drop_shadow(shape)
    
    # Text
    text_frame = shape.text_frame
    text_frame.clear()
    p = text_frame.paragraphs[0]
    p.text = text
    p.font.name = 'Arial'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(60, 64, 67)
    p.alignment = PP_ALIGN.CENTER
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return shape

def connect_shapes(slide, shape_a, shape_b, start_idx=3, end_idx=1):
    """Draws an elbow connector arrow from shape_a to shape_b."""
    # 3 = Right side, 1 = Left side, 0 = Top, 2 = Bottom (varies slightly by shape type)
    connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, Inches(0), Inches(0), Inches(1), Inches(1))
    connector.begin_connect(shape_a, start_idx)
    connector.end_connect(shape_b, end_idx)
    
    # Style the line
    connector.line.color.rgb = RGBColor(95, 99, 104)
    connector.line.width = Pt(1.5)
    
    # Add arrow head using XML because python-pptx doesn't have a direct property for head type on connectors yet
    line_xml = '''
    <a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="19050">
        <a:solidFill>
            <a:srgbClr val="5F6368"/>
        </a:solidFill>
        <a:headEnd type="triangle" w="med" len="med"/>
    </a:ln>
    '''
    # Safely replace the line properties if it exists, or append
    spPr = connector.element.spPr
    ln = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
    if ln is not None:
        spPr.replace(ln, parse_xml(line_xml))
    else:
        spPr.append(parse_xml(line_xml))

def create_slide(output_pptx_path: str, title_text: str = "Cloud Architecture Schematic", **kwargs) -> str:
    """
    Create a PPTX file reproducing the Hierarchical Cloud Architecture Schematic effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Blank slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Slide Background
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(255, 255, 255)

    # 1. Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(10), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial'
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(32, 33, 36)

    # Palette (GCP inspired)
    color_blue = (66, 133, 244)
    color_green = (52, 168, 83)
    color_yellow = (251, 188, 5)
    color_red = (234, 67, 53)
    color_vpc_bg = (240, 244, 248)

    # 2. Setup Containers (Hierarchical)
    # Outer Container: Overall Cloud Provider / Project
    create_container(slide, "Google Cloud Project: prj-web-prod-01", 2.5, 1.5, 10.0, 5.5, dashed=True)
    
    # Inner Container: VPC
    create_container(slide, "VPC Network: default", 3.0, 2.2, 7.0, 4.5, fill_color=color_vpc_bg, border_color=color_blue)

    # 3. Create Nodes
    # External
    node_user = create_node(slide, "End Users", 0.5, 4.0, accent_color=(154, 160, 166))
    
    # Inside VPC
    node_lb = create_node(slide, "Cloud Load\nBalancing", 3.5, 4.0, accent_color=color_blue)
    node_app1 = create_node(slide, "Compute\nEngine (Web)", 5.5, 3.2, accent_color=color_blue)
    node_app2 = create_node(slide, "Compute\nEngine (API)", 5.5, 4.8, accent_color=color_blue)
    node_db = create_node(slide, "Cloud SQL\n(PostgreSQL)", 8.0, 4.0, accent_color=color_yellow)
    
    # Inside Project, Outside VPC
    node_storage = create_node(slide, "Cloud Storage\n(Assets)", 10.5, 3.2, accent_color=color_green)
    node_pubsub = create_node(slide, "Pub/Sub\n(Events)", 10.5, 4.8, accent_color=color_red)

    # 4. Connect the architecture (Topological routing)
    connect_shapes(slide, node_user, node_lb, start_idx=3, end_idx=1)
    
    # LB to Apps
    connect_shapes(slide, node_lb, node_app1, start_idx=3, end_idx=1)
    connect_shapes(slide, node_lb, node_app2, start_idx=3, end_idx=1)
    
    # Apps to DB
    connect_shapes(slide, node_app1, node_db, start_idx=3, end_idx=1)
    connect_shapes(slide, node_app2, node_db, start_idx=3, end_idx=1)
    
    # App1 to Storage
    connect_shapes(slide, node_app1, node_storage, start_idx=3, end_idx=1)
    
    # App2 to Pub/Sub
    connect_shapes(slide, node_app2, node_pubsub, start_idx=3, end_idx=1)

    # Save
    prs.save(output_pptx_path)
    return output_pptx_path

