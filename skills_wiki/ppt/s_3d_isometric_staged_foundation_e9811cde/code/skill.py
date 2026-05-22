import os
import random
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "3D FLOOR FOUNDATION",
    subtitle_text: str = "Procedural Isometric Stage",
    base_color: tuple = (210, 180, 140),  # Light Oak
    extrusion_color: str = "4A2A10",      # Dark Brown Hex
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 3D Isometric Textured Stage effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Dark Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(34, 42, 53)

    # === Layer 2: Procedural Texture Generation (PIL) ===
    # We generate a flat wood-plank floor texture
    tex_size = 1000
    img = Image.new('RGB', (tex_size, tex_size), color=base_color)
    draw = ImageDraw.Draw(img)
    
    plank_height = 50
    for y in range(0, tex_size, plank_height):
        # Staggered offsets for realistic floorboards
        offset = random.randint(0, 300)
        x = -offset
        while x < tex_size:
            plank_width = random.randint(200, 450)
            
            # Slight color variations for individual planks
            r_var = base_color[0] + random.randint(-15, 15)
            g_var = base_color[1] + random.randint(-15, 15)
            b_var = base_color[2] + random.randint(-15, 15)
            plank_col = (max(0, min(255, r_var)), 
                         max(0, min(255, g_var)), 
                         max(0, min(255, b_var)))
            
            # Draw plank with slight dark border for gaps
            draw.rectangle([x, y, x + plank_width, y + plank_height], 
                           fill=plank_col, outline=(160, 130, 90), width=2)
            
            # Add subtle grain lines
            for _ in range(random.randint(2, 6)):
                line_y = y + random.randint(5, plank_height - 5)
                draw.line([(x + 10, line_y), (x + plank_width - 10, line_y)], 
                          fill=(plank_col[0]-20, plank_col[1]-20, plank_col[2]-20), width=1)
            
            x += plank_width

    temp_img_path = "temp_floor_texture.png"
    img.save(temp_img_path)

    # === Layer 3: Insert Image & Apply 3D Extrusion (lxml) ===
    # Insert as a square in the center-bottom
    size = Inches(6.5)
    left = (prs.slide_width - size) / 2
    top = Inches(2.5)
    pic = slide.shapes.add_picture(temp_img_path, left, top, size, size)

    # XML namespaces
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    
    # 1. Construct 3D Scene (Camera and Lighting)
    scene3d = etree.Element(f'{{{a}}}scene3d')
    # Preset "isoTopUp" gives the classic isometric floor look
    camera = etree.SubElement(scene3d, f'{{{a}}}camera', prst="isoTopUp")
    light = etree.SubElement(scene3d, f'{{{a}}}lightRig', rig="threePt", dir="t")
    
    # 2. Construct 3D Shape Properties (Extrusion / Thickness)
    # extrusionH in EMUs (1 inch = 914400 EMUs, 0.4 inches = ~365760)
    sp3d = etree.Element(f'{{{a}}}sp3d', extrusionH="365760")
    
    # Top Bevel for a polished edge
    etree.SubElement(sp3d, f'{{{a}}}bevelT', w="38100", h="38100", prst="relaxedInset")
    
    # Extrusion Color (Foundation Wall)
    ext_clr = etree.SubElement(sp3d, f'{{{a}}}extrusionClr')
    etree.SubElement(ext_clr, f'{{{a}}}srgbClr', val=extrusion_color)
    
    # Surface Material
    etree.SubElement(sp3d, f'{{{a}}}solid', val="warmMatte")

    # 3. Inject into the picture's shape properties
    spPr = pic._element.spPr
    spPr.append(scene3d)
    spPr.append(sp3d)

    # Clean up temp file
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

    # === Layer 4: Typography ===
    # Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(11.333), Inches(1))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial Black"
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1), Inches(1.7), Inches(11.333), Inches(0.6))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(0, 191, 255)  # Cyan accent

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("3d_isometric_stage.pptx")
