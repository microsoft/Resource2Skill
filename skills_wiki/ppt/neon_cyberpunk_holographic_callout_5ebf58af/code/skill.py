import math
import random
import os
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.shapes.freeform import FreeformBuilder

def create_slide(
    output_pptx_path: str,
    title_text: str = "Cataracts",
    cost_text: str = "£2,300",
    highlight_region: str = "head",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a cyberpunk holographic anatomy background,
    highlighting a specific region and connecting it to a data label.
    
    Supported regions: 'head', 'heart', 'shoulder', 'hip', 'knee', 'hand'
    """
    
    # ---------------------------------------------------------
    # 1. PIL: GENERATE NEON HOLOGRAPHIC BACKGROUND & SUBJECT
    # ---------------------------------------------------------
    WIDTH, HEIGHT = 1280, 720
    
    # Base Canvas (Deep Tech Navy)
    base_img = Image.new('RGBA', (WIDTH, HEIGHT), (10, 14, 25, 255))
    
    # Layers for effects
    glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    sharp_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    reticle_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    
    draw_bg = ImageDraw.Draw(base_img)
    draw_glow = ImageDraw.Draw(glow_layer)
    draw_sharp = ImageDraw.Draw(sharp_layer)
    draw_reticle = ImageDraw.Draw(reticle_layer)
    
    # A. Draw Constellation Network Background
    random.seed(42) # Ensure reproducible background
    nodes = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(80)]
    for p1 in nodes:
        draw_bg.ellipse([p1[0]-1.5, p1[1]-1.5, p1[0]+1.5, p1[1]+1.5], fill=(0, 191, 255, 60))
        for p2 in nodes:
            if p1 != p2 and math.hypot(p2[0]-p1[0], p2[1]-p1[1]) < 100:
                draw_bg.line([p1, p2], fill=(0, 191, 255, 20), width=1)
                
    # B. Define Wireframe Anatomy Coordinates (Center Left)
    cx = 400
    cy = 120
    
    # Core anatomical points
    pts = {
        "head_center": (cx, cy),
        "neck_top": (cx, cy + 35),
        "neck_base": (cx, cy + 70),
        "shoulder_l": (cx - 60, cy + 80),
        "shoulder_r": (cx + 60, cy + 80),
        "elbow_l": (cx - 80, cy + 200),
        "elbow_r": (cx + 80, cy + 200),
        "hand_l": (cx - 70, cy + 320),
        "hand_r": (cx + 70, cy + 320),
        "chest": (cx, cy + 150),
        "pelvis": (cx, cy + 270),
        "hip_l": (cx - 35, cy + 280),
        "hip_r": (cx + 35, cy + 280),
        "knee_l": (cx - 45, cy + 430),
        "knee_r": (cx + 45, cy + 430),
        "foot_l": (cx - 40, cy + 560),
        "foot_r": (cx + 40, cy + 560),
    }

    # Lines to draw the wireframe
    wire_lines = [
        # Spine & Torso
        (pts["neck_top"], pts["neck_base"]),
        (pts["neck_base"], pts["chest"]),
        (pts["chest"], pts["pelvis"]),
        (pts["shoulder_l"], pts["shoulder_r"]),
        (pts["hip_l"], pts["hip_r"]),
        (pts["shoulder_l"], pts["pelvis"]),
        (pts["shoulder_r"], pts["pelvis"]),
        # Arms
        (pts["shoulder_l"], pts["elbow_l"]), (pts["elbow_l"], pts["hand_l"]),
        (pts["shoulder_r"], pts["elbow_r"]), (pts["elbow_r"], pts["hand_r"]),
        # Legs
        (pts["hip_l"], pts["knee_l"]), (pts["knee_l"], pts["foot_l"]),
        (pts["hip_r"], pts["knee_r"]), (pts["knee_r"], pts["foot_r"])
    ]
    
    # Draw function for the humanoid
    def draw_wireframe(draw_obj, width, fill_color):
        # Head (Ellipse)
        hr = 35
        draw_obj.ellipse([cx-hr, cy-hr, cx+hr, cy+hr], outline=fill_color, width=width)
        # Joints (Small circles)
        for name, pt in pts.items():
            if name != "head_center":
                draw_obj.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill=fill_color)
        # Lines
        for line_pts in wire_lines:
            draw_obj.line([line_pts[0], line_pts[1]], fill=fill_color, width=width)
            
        # Add high-tech horizontal scanning arcs (ribs)
        for y_offset in [110, 140, 170, 200, 230]:
            draw_obj.line([(cx-40, cy+y_offset), (cx+40, cy+y_offset)], fill=fill_color, width=max(1, width-1))

    # Apply Glowing Wireframe
    draw_wireframe(draw_glow, width=8, fill_color=(0, 191, 255, 120))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(12))
    draw_wireframe(draw_sharp, width=2, fill_color=(150, 240, 255, 255))
    
    # C. Draw Target Reticle (Neon Red/Magenta)
    regions = {
        "head": pts["head_center"],
        "heart": (cx + 15, cy + 130),
        "shoulder": pts["shoulder_l"],
        "hip": pts["hip_l"],
        "knee": pts["knee_l"],
        "hand": pts["hand_l"],
    }
    
    # Fallback to head if region not found
    target_pt = regions.get(highlight_region.lower(), pts["head_center"])
    rx, ry = target_pt
    
    # Reticle Glow & Sharp
    s = 28 # size of hex
    hex_poly = [
        (rx - s/2, ry - s), (rx + s/2, ry - s),
        (rx + s, ry), (rx + s/2, ry + s),
        (rx - s/2, ry + s), (rx - s, ry)
    ]
    draw_glow.polygon(hex_poly, outline=(255, 40, 100, 180), width=10)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(8))
    draw_sharp.polygon(hex_poly, outline=(255, 100, 150, 255), width=3)
    
    # Composite PIL Image
    final_bg = Image.alpha_composite(base_img, glow_layer)
    final_bg = Image.alpha_composite(final_bg, sharp_layer)
    
    bg_path = "temp_cyber_bg.png"
    final_bg.save(bg_path)
    
    # ---------------------------------------------------------
    # 2. PPTX: LAYOUT & CONNECTIONS
    # ---------------------------------------------------------
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # Add generated background
    slide.shapes.add_picture(bg_path, 0, 0, width=Inches(13.333), height=Inches(7.5))
    
    # Coordinates in Inches for PPTX elements
    rx_inch = rx * 13.333 / WIDTH
    ry_inch = ry * 7.5 / HEIGHT
    
    # Tech Line Anchors
    text_target_x = Inches(8.5)
    text_target_y = Inches(3.5)
    
    # Draw Geometric Connector Line (Reticle -> Text)
    ff_builder = slide.shapes.build_freeform(Inches(rx_inch + 0.3), Inches(ry_inch))
    ff_builder.add_line_segments([
        (Inches(rx_inch + 1.2), Inches(ry_inch)),          # Go right horizontally
        (Inches(8.2), text_target_y + Inches(0.2)),        # Angle down/up to text block
        (text_target_x, text_target_y + Inches(0.2))       # Flat lead-in to text
    ])
    connector = ff_builder.convert_to_shape()
    connector.line.color.rgb = RGBColor(0, 191, 255)       # Cyan match
    connector.line.width = Pt(1.5)
    
    # Add Text Box
    txBox = slide.shapes.add_textbox(text_target_x, text_target_y - Inches(0.5), Inches(4), Inches(2))
    tf = txBox.text_frame
    
    # Main Label (e.g., Cataracts)
    p_title = tf.paragraphs[0]
    p_title.text = title_text.upper()
    p_title.font.name = "Arial"
    p_title.font.bold = True
    p_title.font.size = Pt(36)
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    
    # Value Label (e.g., £2,300)
    p_cost = tf.add_paragraph()
    p_cost.text = cost_text
    p_cost.font.name = "Arial"
    p_cost.font.bold = False
    p_cost.font.size = Pt(28)
    p_cost.font.color.rgb = RGBColor(0, 191, 255)
    
    prs.save(output_pptx_path)
    
    # Cleanup temp file
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
