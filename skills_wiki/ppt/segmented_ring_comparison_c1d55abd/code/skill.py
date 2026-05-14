import math
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    title_text: str = "2 Sides of an Issue",
    central_text: str = "You can replace this sample text with your own text",
    side1_color: tuple = (67, 85, 41),  # Green
    side2_color: tuple = (200, 89, 27), # Orange
    num_points: int = 5,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a 'Segmented Ring Comparison' graphic.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Colors & Dimensions ===
    bg_color = RGBColor(255, 255, 255)
    center_circle_color = RGBColor(221, 221, 221)
    line_color = RGBColor(191, 191, 191)
    font_color = RGBColor(0, 0, 0)
    
    # Set slide background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = bg_color

    # Graphic dimensions
    cx = prs.slide_width / 2
    cy = prs.slide_height / 2
    center_radius = Inches(1.2)
    ring_radius = Inches(1.8)
    ring_thickness = Inches(0.5)
    bullet_radius = Inches(0.1)
    bullet_ring_radius = ring_radius - (ring_thickness / 2)

    # === Title ===
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.33), Inches(0.8))
    title_tf = title_shape.text_frame
    title_tf.text = title_text
    p = title_tf.paragraphs[0]
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = font_color
    p.alignment = PP_ALIGN.CENTER
    
    # === Layer 1: Central Circle ===
    inner_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        cx - center_radius,
        cy - center_radius,
        center_radius * 2,
        center_radius * 2,
    )
    fill = inner_circle.fill
    fill.solid()
    fill.fore_color.rgb = center_circle_color
    inner_circle.line.fill.background()

    # === Layer 2: Segmented Outer Ring ===
    # python-pptx doesn't have Merge Shapes. We simulate the split ring with two BLOCK_ARC shapes.
    
    # Right Side (Orange)
    arc_right = slide.shapes.add_shape(
        MSO_SHAPE.BLOCK_ARC,
        cx - ring_radius,
        cy - ring_radius,
        ring_radius * 2,
        ring_radius * 2,
    )
    arc_right.rotation = 90
    # Adjustments: 0 is start angle, 1 is end angle, 2 is thickness
    arc_right.adjustments[0] = 0
    arc_right.adjustments[1] = 18000000 # 180 degrees
    arc_right.adjustments[2] = int(100000 * (ring_thickness / (ring_radius*2)))
    
    fill = arc_right.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*side2_color)
    arc_right.line.fill.background()

    # Left Side (Green)
    arc_left = slide.shapes.add_shape(
        MSO_SHAPE.BLOCK_ARC,
        cx - ring_radius,
        cy - ring_radius,
        ring_radius * 2,
        ring_radius * 2,
    )
    arc_left.rotation = 270
    arc_left.adjustments[0] = 0
    arc_left.adjustments[1] = 18000000
    arc_left.adjustments[2] = int(100000 * (ring_thickness / (ring_radius*2)))
    
    fill = arc_left.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*side1_color)
    arc_left.line.fill.background()

    # === Layer 3: Text & Content ===
    
    # Central Text
    center_text_box = slide.shapes.add_textbox(
        cx - Inches(0.9), cy - Inches(0.5), Inches(1.8), Inches(1.0)
    )
    center_tf = center_text_box.text_frame
    center_tf.word_wrap = True
    p = center_tf.add_paragraph()
    p.text = central_text
    p.font.size = Pt(14)
    p.font.color.rgb = font_color
    p.alignment = PP_ALIGN.CENTER
    center_tf.margin_bottom = 0
    center_tf.margin_top = 0

    # Points on each side
    total_angle_span = 120  # degrees
    start_angle_offset = (180 - total_angle_span) / 2

    # Left side points (Green)
    for i in range(num_points):
        angle_deg = 180 + start_angle_offset + (i * (total_angle_span / (num_points - 1)))
        angle_rad = math.radians(angle_deg)
        bx = cx + bullet_ring_radius * math.cos(angle_rad)
        by = cy + bullet_ring_radius * math.sin(angle_rad)
        
        # Bullet
        bullet = slide.shapes.add_shape(MSO_SHAPE.DONUT, bx - bullet_radius, by - bullet_radius, bullet_radius * 2, bullet_radius * 2)
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = RGBColor(255,255,255)
        bullet.line.fill.background()
        bullet.adjustments[0] = 35000 # thickness of donut
        
        # Line
        line_end_x = cx - ring_radius - Inches(0.5)
        line = slide.shapes.add_connector(MSO_SHAPE_TYPE.LINE, Emu(bx), Emu(by), Emu(line_end_x), Emu(by))
        line.line.color.rgb = line_color
        
        # Text
        txt_box = slide.shapes.add_textbox(line_end_x - Inches(2.1), by - Inches(0.15), Inches(2.0), Inches(0.3))
        p = txt_box.text_frame.paragraphs[0]
        p.text = "Your text here"
        p.font.size = Pt(14)
        p.alignment = PP_ALIGN.RIGHT

    # Right side points (Orange)
    for i in range(num_points):
        angle_deg = -start_angle_offset - (i * (total_angle_span / (num_points - 1)))
        angle_rad = math.radians(angle_deg)
        bx = cx + bullet_ring_radius * math.cos(angle_rad)
        by = cy + bullet_ring_radius * math.sin(angle_rad)

        # Bullet
        bullet = slide.shapes.add_shape(MSO_SHAPE.DONUT, bx - bullet_radius, by - bullet_radius, bullet_radius * 2, bullet_radius * 2)
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = RGBColor(255,255,255)
        bullet.line.fill.background()
        bullet.adjustments[0] = 35000

        # Line
        line_end_x = cx + ring_radius + Inches(0.5)
        line = slide.shapes.add_connector(MSO_SHAPE_TYPE.LINE, Emu(bx), Emu(by), Emu(line_end_x), Emu(by))
        line.line.color.rgb = line_color

        # Text
        txt_box = slide.shapes.add_textbox(line_end_x + Inches(0.1), by - Inches(0.15), Inches(2.0), Inches(0.3))
        p = txt_box.text_frame.paragraphs[0]
        p.text = "Your text here"
        p.font.size = Pt(14)
        p.alignment = PP_ALIGN.LEFT

    prs.save(output_pptx_path)
    return output_pptx_path

