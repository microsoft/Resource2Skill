import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree

def apply_gradient_fill(shape, stops, angle=90):
    """
    Injects OpenXML to apply a linear gradient fill to a shape.
    stops: list of tuples (position_percentage, (R, G, B), alpha_percentage)
           e.g., [(0, (255,0,0), 100), (100, (0,0,255), 50)]
    angle: rotation angle of the gradient in degrees.
    """
    spPr = shape.element.spPr
    # Remove existing fill properties
    for elem in spPr.xpath('./a:solidFill | ./a:noFill | ./a:blipFill | ./a:gradFill', namespaces=spPr.nsmap):
        spPr.remove(elem)
        
    gradFill = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}gradFill')
    
    # Set angle (convert degrees to PPT's 60000ths of a degree)
    rot_val = str(int(angle * 60000))
    etree.SubElement(gradFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}lin', ang=rot_val, scaled="1")
    
    gsLst = etree.SubElement(gradFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}gsLst')
    
    for pos, rgb, alpha in stops:
        gs = etree.SubElement(gsLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}gs', pos=str(int(pos * 1000)))
        srgbClr = etree.SubElement(gs, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val=f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}")
        if alpha < 100:
            # Alpha is expressed in 1000ths of a percent (e.g., 50% -> 50000)
            etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val=str(int(alpha * 1000)))

def draw_isometric_column(slide, cx, cy, width, depth_y, height, color_scheme, transparency=100):
    """
    Draws an isometric 3D column (cuboid) using three 2D Freeform polygons.
    cx, cy: Top-center vertex X and Y coordinates
    width: Half-width of the cube (horizontal span from center to left/right edge)
    depth_y: Half-height of the top face (vertical span of the top rhombus)
    height: Z-axis height (extrusion downwards)
    color_scheme: dict with RGB tuples for 'top', 'left', 'right' faces.
    """
    # Vertex definitions
    p_top = (cx, cy - depth_y)
    p_left = (cx - width, cy)
    p_right = (cx + width, cy)
    p_center = (cx, cy + depth_y)
    
    p_bottom_left = (cx - width, cy + height)
    p_bottom_center = (cx, cy + depth_y + height)
    p_bottom_right = (cx + width, cy + height)
    
    # 1. Top Face
    fb_top = slide.shapes.build_freeform(p_left[0], p_left[1])
    fb_top.add_line_segments([p_top, p_right, p_center, p_left])
    shape_top = fb_top.convert_to_shape()
    shape_top.line.fill.background() # No line
    
    # Gradient for Top (Simulating light hitting from top left)
    c_top = color_scheme['top']
    apply_gradient_fill(shape_top, [(0, (255,255,255), transparency), (100, c_top, transparency)], angle=45)

    # 2. Left Face
    fb_left = slide.shapes.build_freeform(p_left[0], p_left[1])
    fb_left.add_line_segments([p_center, p_bottom_center, p_bottom_left, p_left])
    shape_left = fb_left.convert_to_shape()
    shape_left.line.fill.background()
    
    # Gradient for Left (Mid-tone)
    c_left = color_scheme['left']
    c_left_dark = (int(c_left[0]*0.8), int(c_left[1]*0.8), int(c_left[2]*0.8))
    apply_gradient_fill(shape_left, [(0, c_left, transparency), (100, c_left_dark, transparency)], angle=90)

    # 3. Right Face
    fb_right = slide.shapes.build_freeform(p_center[0], p_center[1])
    fb_right.add_line_segments([p_right, p_bottom_right, p_bottom_center, p_center])
    shape_right = fb_right.convert_to_shape()
    shape_right.line.fill.background()
    
    # Gradient for Right (Shadow)
    c_right = color_scheme['right']
    c_shadow = (int(c_right[0]*0.5), int(c_right[1]*0.5), int(c_right[2]*0.5))
    apply_gradient_fill(shape_right, [(0, c_right, transparency), (100, c_shadow, transparency)], angle=90)

    return (shape_top, shape_left, shape_right)

def create_slide(
    output_pptx_path: str,
    title_text: str = "3D ISOMETRIC CUBES",
    body_text: str = "Glassmorphism & Gradient Data Representation",
    **kwargs,
) -> str:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    # Dark modern background to make glassmorphism pop
    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height) # Rectangle
    apply_gradient_fill(bg, [(0, (13, 17, 28), 100), (100, (20, 30, 50), 100)], angle=135)
    bg.line.fill.background()

    # === Layer 2: Visual Effect 1 - 3D Bar Chart (Solid Gradients) ===
    chart_color = {'top': (0, 230, 255), 'left': (0, 150, 255), 'right': (0, 80, 180)}
    highlight_color = {'top': (255, 200, 50), 'left': (255, 140, 0), 'right': (180, 80, 0)}
    
    start_x = Inches(2.0)
    base_y = Inches(6.0) # Bottom alignment line
    cube_w = Inches(0.5)
    cube_d = Inches(0.25)
    
    data_points = [1.0, 1.5, 2.2, 3.5, 5.0] # Simulated data heights
    
    for i, h in enumerate(data_points):
        cx = start_x + (i * Inches(1.3))
        # Determine height in Inches
        col_h = Inches(h)
        # cy is the top center. cy + depth_y + col_h = base_y
        cy = base_y - col_h - cube_d
        
        # Make the last one a highlight color
        scheme = highlight_color if i == len(data_points)-1 else chart_color
        
        draw_isometric_column(slide, cx, cy, cube_w, cube_d, col_h, scheme, transparency=100)
        
        # Add Data Label floating above
        tx_box = slide.shapes.add_textbox(cx - Inches(0.5), cy - Inches(0.8), Inches(1), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = f"{int(h * 20)}"
        tf.paragraphs[0].font.size = Pt(20)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # === Layer 3: Visual Effect 2 - Glassmorphism Container ===
    # Large translucent cube acting as a podium on the right side
    glass_color = {'top': (255, 255, 255), 'left': (100, 200, 255), 'right': (50, 100, 200)}
    
    p_cx = Inches(10.5)
    p_cy = Inches(3.5)
    draw_isometric_column(slide, p_cx, p_cy, Inches(1.5), Inches(0.75), Inches(2.0), glass_color, transparency=60)
    
    # Add floating text "inside/above" the glass podium
    tx_box2 = slide.shapes.add_textbox(p_cx - Inches(1.0), p_cy - Inches(0.5), Inches(2), Inches(1))
    tf2 = tx_box2.text_frame
    tf2.text = "01\nTECH"
    p = tf2.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    if len(tf2.paragraphs) > 1:
        tf2.paragraphs[1].font.size = Pt(16)
        tf2.paragraphs[1].font.color.rgb = RGBColor(150, 200, 255)
        tf2.paragraphs[1].alignment = PP_ALIGN.CENTER

    # === Layer 4: Title Content ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(1))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    
    p_sub = tf_title.add_paragraph()
    p_sub.text = body_text
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(0, 191, 255)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("isometric_cubes_glassmorphism.pptx")
