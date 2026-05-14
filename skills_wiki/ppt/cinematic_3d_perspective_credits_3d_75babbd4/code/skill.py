import os
import requests
from io import BytesIO
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw

def create_dark_gradient_bg(width_px=1920, height_px=1080):
    """Generates a cinematic deep radial gradient background using PIL."""
    base = Image.new('RGB', (width_px, height_px), color=(0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    # Center of the glow
    cx, cy = int(width_px * 0.5), int(height_px * 0.5)
    max_radius = int((cx**2 + cy**2)**0.5)
    
    # Deep navy to black gradient
    center_color = (25, 35, 55)
    edge_color = (5, 5, 10)
    
    for r in range(max_radius, 0, -5):
        ratio = r / max_radius
        # ease-out interpolation
        ratio = ratio ** 1.5 
        
        red = int(center_color[0] * (1 - ratio) + edge_color[0] * ratio)
        green = int(center_color[1] * (1 - ratio) + edge_color[1] * ratio)
        blue = int(center_color[2] * (1 - ratio) + edge_color[2] * ratio)
        
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(red, green, blue))
        
    img_stream = BytesIO()
    base.save(img_stream, format='PNG')
    img_stream.seek(0)
    return img_stream

def apply_3d_perspective(shape):
    """Injects OpenXML to apply a 3D perspective rotation to a picture shape."""
    spPr = shape._element.spPr
    
    # Define 3D Scene (Camera and Light)
    scene3d_xml = """
    <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:camera prst="perspectiveRight" fov="50000">
            <!-- lat: vertical tilt, lon: horizontal pan -->
            <a:rot lat="1200000" lon="1800000" rev="0"/>
        </a:camera>
        <a:lightRig rig="twoPt" dir="t">
            <a:rot lat="0" lon="0" rev="1200000"/>
        </a:lightRig>
    </a:scene3d>
    """
    
    # Define 3D Shape properties (Bevel/Depth)
    sp3d_xml = """
    <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:bevelT w="25400" h="25400"/>
        <a:extrusionClr>
            <a:srgbClr val="222222"/>
        </a:extrusionClr>
    </a:sp3d>
    """
    
    scene3d_elem = etree.fromstring(scene3d_xml)
    sp3d_elem = etree.fromstring(sp3d_xml)
    
    # Append to shape properties
    spPr.append(scene3d_elem)
    spPr.append(sp3d_elem)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Unleash Imagination",
    credits_data: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Cinematic 3D Credits visual effect.
    """
    if credits_data is None:
        credits_data = [
            ("Topic Curation", "Sarah Jenkins"),
            ("Data Gathering", "Markus Doe"),
            ("Material Sorting", "Liu Yan"),
            ("Visual Design", "Alex Rivera"),
            ("3D Animation", "Chris Wong"),
            ("Post Production", "Emma Stone"),
            ("Final Review", "Dr. Alan Grant")
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    bg_stream = create_dark_gradient_bg()
    slide.shapes.add_picture(bg_stream, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Main Vision (3D Screen) ===
    # Download a placeholder image representing the presentation's video/cover
    try:
        res = requests.get("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800", timeout=5)
        res.raise_for_status()
        img_bytes = BytesIO(res.content)
    except:
        # Fallback to a solid dark grey block if network fails
        img_bytes = BytesIO()
        Image.new('RGB', (800, 450), color=(50, 50, 60)).save(img_bytes, format='PNG')
        img_bytes.seek(0)
    
    pic_left = Inches(0.8)
    pic_top = Inches(2.0)
    pic_width = Inches(7.0)
    
    pic = slide.shapes.add_picture(img_bytes, pic_left, pic_top, width=pic_width)
    
    # Apply the 3D projection
    apply_3d_perspective(pic)

    # === Layer 3: Title ===
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(7.0), Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # === Layer 4: The Credits (Movie Style Table Layout) ===
    table_left = Inches(8.5)
    table_top = Inches(1.5)
    table_width = Inches(4.0)
    table_height = Inches(len(credits_data) * 0.6)
    
    table_shape = slide.shapes.add_table(len(credits_data), 2, table_left, table_top, table_width, table_height)
    table = table_shape.table
    
    # Adjust column widths (Role column slightly narrower)
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(2.2)
    
    for row_idx, (role, name) in enumerate(credits_data):
        cell_role = table.cell(row_idx, 0)
        cell_name = table.cell(row_idx, 1)
        
        # Format Role (Gray, Right Aligned)
        cell_role.text = role
        p_role = cell_role.text_frame.paragraphs[0]
        p_role.alignment = PP_ALIGN.RIGHT
        p_role.font.size = Pt(16)
        p_role.font.color.rgb = RGBColor(160, 170, 180)
        
        # Format Name (White, Bold, Left Aligned)
        cell_name.text = name
        p_name = cell_name.text_frame.paragraphs[0]
        p_name.alignment = PP_ALIGN.LEFT
        p_name.font.size = Pt(18)
        p_name.font.bold = True
        p_name.font.color.rgb = RGBColor(255, 255, 255)
        
        # Remove cell borders and fills (mimicking text boxes but perfectly aligned)
        for cell in [cell_role, cell_name]:
            cell.fill.background()
            # To strictly remove borders in python-pptx, we leave the native style empty.

    prs.save(output_pptx_path)
    return output_pptx_path
