import os
import math
import random
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

def _create_blueprint_bg(output_path: str):
    """Generates a dark, subtle architectural grid background."""
    w, h = 1920, 1080
    img = Image.new('RGB', (w, h), (10, 10, 12))
    draw = ImageDraw.Draw(img)
    # Subtle architectural grid
    for i in range(0, w, 80):
        draw.line([(i, 0), (i, h)], fill=(20, 20, 25), width=1)
    for i in range(0, h, 80):
        draw.line([(0, i), (w, i)], fill=(20, 20, 25), width=1)
    img.save(output_path)

def _create_abstract_diagram(path: str, seed: int, is_accent: bool = False):
    """Generates randomized 'architectural concept sketches' so the script runs self-contained."""
    random.seed(seed)
    img = Image.new('RGB', (400, 300), (10, 10, 12))
    draw = ImageDraw.Draw(img)
    
    line_col = (220, 60, 60) if is_accent else (200, 200, 200)
    bg_line = (40, 40, 45)
    
    # Draw perspective/isometric grid lines
    for _ in range(15):
        x1, y1 = random.randint(0, 400), random.randint(0, 300)
        x2, y2 = random.randint(0, 400), random.randint(0, 300)
        draw.line([(x1, y1), (x2, y2)], fill=bg_line, width=1)
        
    # Draw main structure
    cx, cy = 200, 150
    w, h = random.randint(60, 140), random.randint(60, 100)
    draw.rectangle([cx-w, cy-h, cx+w, cy+h], outline=line_col, width=2)
    
    # Inner architectural details
    if random.choice([True, False]):
        draw.ellipse([cx-w/2, cy-h/2, cx+w/2, cy+h/2], outline=(255,255,255), width=1)
    else:
        draw.line([(cx-w, cy-h), (cx+w, cy+h)], fill=(255,255,255), width=1)
        draw.line([(cx+w, cy-h), (cx-w, cy+h)], fill=(255,255,255), width=1)
        
    img.save(path)

def _remove_shape_fill(shape):
    """Uses lxml to inject <a:noFill/> ensuring the shape is entirely transparent."""
    spPr = shape._element.spPr
    for elem in spPr.xpath('.//a:solidFill | .//a:bgFill | .//a:gradFill | .//a:pattFill | .//a:blipFill'):
        spPr.remove(elem)
    noFill = parse_xml('<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
    spPr.insert(0, noFill)

def _add_node_text(slide, left, top, width, title, desc, is_accent):
    tb = slide.shapes.add_textbox(left, top, width, Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.clear() 
    
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title
    run.font.name = 'Georgia' 
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = RGBColor(220, 60, 60) if is_accent else RGBColor(240, 240, 240)
    
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(3)
    run2 = p2.add_run()
    run2.text = desc
    run2.font.name = 'Century Gothic' 
    run2.font.size = Pt(8)
    run2.font.color.rgb = RGBColor(150, 150, 150)

def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Creates an Editorial Architectural Orbital Concept Map.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 1. Background
    bg_path = "temp_blueprint_bg.png"
    _create_blueprint_bg(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    
    cx_pt, cy_pt = Inches(13.333 / 2), Inches(7.5 / 2)
    outer_radius = Inches(2.7)
    inner_radius = Inches(0.8)
    
    # 2. Concentric Orbit Rings (Using lxml to ensure true transparency over the background)
    c_outer = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx_pt - outer_radius, cy_pt - outer_radius, outer_radius*2, outer_radius*2)
    _remove_shape_fill(c_outer)
    c_outer.line.color.rgb = RGBColor(100, 100, 100)
    c_outer.line.width = Pt(0.75)
    
    c_inner = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx_pt - inner_radius, cy_pt - inner_radius, inner_radius*2, inner_radius*2)
    _remove_shape_fill(c_inner)
    c_inner.line.color.rgb = RGBColor(80, 80, 80)
    c_inner.line.width = Pt(0.5)

    # 3. Center Anchor Image
    center_img_path = "temp_center.png"
    _create_abstract_diagram(center_img_path, seed=99)
    cw, ch = Inches(2.0), Inches(1.5)
    pic_c = slide.shapes.add_picture(center_img_path, cx_pt - cw/2, cy_pt - ch/2, cw, ch)
    pic_c.line.color.rgb = RGBColor(255, 255, 255)
    pic_c.line.width = Pt(0.75)

    # 4. Node Data (Angles: 0=Right, 90=Bottom, 180=Left, 270=Top)
    nodes = [
        {"title": "SPEED & DISTRACTION", "desc": "Urban space and kinetic energy", "angle": 270, "align": "above", "accent": False},
        {"title": "CATEGORIZATION", "desc": "Systematic flow of information", "angle": 90, "align": "below", "accent": False},
        {"title": "ANTI-LIBRARY", "desc": "The collection of unread books", "angle": 180, "align": "below", "accent": False},
        {"title": "LUXURY OF TIME", "desc": "Slowing down in a fast world", "angle": 0, "align": "below", "accent": False},
        {"title": "DERIVE", "desc": "Unplanned journeys through a landscape", "angle": 320, "align": "above", "accent": True},
    ]

    # 5. Render Nodes
    for i, node in enumerate(nodes):
        angle_rad = math.radians(node["angle"])
        
        # Image center coordinates
        nx = cx_pt + outer_radius * math.cos(angle_rad)
        ny = cy_pt + outer_radius * math.sin(angle_rad)
        
        # Connectors (starting from inner radius)
        sx = cx_pt + inner_radius * math.cos(angle_rad)
        sy = cy_pt + inner_radius * math.sin(angle_rad)
        
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, sx, sy, nx, ny)
        line.line.width = Pt(1.5) if node["accent"] else Pt(0.75)
        line.line.color.rgb = RGBColor(220, 60, 60) if node["accent"] else RGBColor(120, 120, 120)
        if not node["accent"]:
            line.line.dash_style = 3  # Dashed

        # Orbital Images
        img_path = f"temp_node_{i}.png"
        _create_abstract_diagram(img_path, seed=i*10, is_accent=node["accent"])
        img_w, img_h = Inches(1.6), Inches(1.2)
        pic = slide.shapes.add_picture(img_path, nx - img_w/2, ny - img_h/2, img_w, img_h)
        pic.line.color.rgb = RGBColor(255, 255, 255)
        pic.line.width = Pt(0.5)
        
        # Text positioning
        tx = nx - Inches(1.25)
        tw = Inches(2.5)
        ty = (ny - img_h/2 - Inches(0.6)) if node["align"] == "above" else (ny + img_h/2 + Inches(0.1))
        
        _add_node_text(slide, tx, ty, tw, node["title"], node["desc"], node["accent"])

    # 6. Folio / Metadata Top Left
    folio = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(4), Inches(0.5))
    run = folio.text_frame.paragraphs[0].add_run()
    run.text = "CONCEPTUAL FRAMEWORK // 04"
    run.font.name = 'Century Gothic'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(120, 120, 120)
    run.font.bold = True

    # Cleanup temp files
    try:
        os.remove(bg_path)
        os.remove(center_img_path)
        for i in range(len(nodes)):
            os.remove(f"temp_node_{i}.png")
    except OSError:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path
