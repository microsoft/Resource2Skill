import os
import random
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw
from lxml import etree

# Declare ambient capability per system requirements
AMBIENT_CAPABLE = True

def create_slide(
    output_pptx_path: str,
    title_text: str = "Winter Wonderland",
    body_text: str = "Adding ambient life to static slides.",
    bg_palette: str = "twilight",
    accent_color: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Creates a presentation slide with a procedural vector-style winter landscape
    and an ambient, animated snowfall particle system.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Procedural Landscape Background via PIL ===
    bg_image_path = "temp_winter_landscape.png"
    width, height = 1920, 1080
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    
    # Gradient Sky (Dark purple to soft pink)
    color_top = (85, 43, 105, 255)
    color_bottom = (240, 163, 196, 255)
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Snowy Foreground Hills (Overlapping ellipses)
    draw.ellipse([(-300, 750), (1200, 1500)], fill=(235, 235, 245, 255))
    draw.ellipse([(600, 650), (2300, 1400)], fill=(255, 255, 255, 255))
    
    img.save(bg_image_path)
    
    # Insert background
    slide.shapes.add_picture(bg_image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Ambient Particle Field (Snowflakes) ===
    # Generate ~120 snowflakes with randomized properties for organic depth
    for _ in range(120):
        # Randomize size (depth cue)
        size_in = random.uniform(0.04, 0.18)
        
        # Randomize starting position
        x_pos = random.uniform(-0.5, 13.8)
        y_pos = random.uniform(-1.0, 7.5)
        
        # Create the particle
        shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(x_pos), Inches(y_pos),
            Inches(size_in), Inches(size_in)
        )
        
        # Style: White, no border
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.fill.background() # Transparent border
        
        # lxml Injection: Add Transparency for parallax depth
        # Smaller particles should generally be more transparent (further away)
        opacity_pct = random.uniform(30.0, 95.0)
        alpha_val = int(opacity_pct * 1000) # OpenXML expects 0 - 100000
        
        srgbClr = shape.fill.fore_color._xFill.srgbClr
        if srgbClr is not None:
            alpha_elem = etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
            alpha_elem.set("val", str(alpha_val))

        # Add Ambient Motion
        try:
            from _shell_helpers import add_drift_motion
            # Snow gently falls (positive Y drift) and flutters horizontally
            drift_y = random.uniform(1.5, 4.5) 
            drift_x = random.uniform(-0.8, 0.8)
            duration = int(random.uniform(4000, 9000)) # 4 to 9 seconds
            
            add_drift_motion(slide, shape, dx_in=drift_x, dy_in=drift_y, duration_ms=duration, pingpong=True)
        except ImportError:
            pass # Graceful degradation if helper is unavailable

    # === Layer 3: Text Content ===
    # Title Box
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1.5))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Lxml Injection: Add a subtle text shadow to ensure readability against snow
    shadow = etree.SubElement(p.font._element, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
    outerShdw = etree.SubElement(shadow, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw")
    outerShdw.set("blurRad", "50800")     # ~4pt blur
    outerShdw.set("dist", "38100")        # ~3pt distance
    outerShdw.set("dir", "2700000")       # 45 degrees
    outerShdw.set("algn", "tl")
    shdw_clr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
    shdw_clr.set("val", "000000")
    alpha_shdw = etree.SubElement(shdw_clr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
    alpha_shdw.set("val", "50000")        # 50% opacity
    
    # Subtitle Box
    sub_box = slide.shapes.add_textbox(Inches(0.55), Inches(1.5), Inches(10), Inches(1))
    p_sub = sub_box.text_frame.paragraphs[0]
    p_sub.text = body_text
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(24)
    p_sub.font.color.rgb = RGBColor(240, 240, 255)

    # Clean up and save
    prs.save(output_pptx_path)
    if os.path.exists(bg_image_path):
        os.remove(bg_image_path)
        
    return output_pptx_path
