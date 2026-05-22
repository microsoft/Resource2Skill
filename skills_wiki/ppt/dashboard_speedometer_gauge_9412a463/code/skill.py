def create_slide(
    output_pptx_path: str,
    title_text: str = "Project Health Metric",
    percentage: float = 75.0,  # Value from 0.0 to 100.0
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dashboard Speedometer Gauge effect.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    # === Presentation Setup ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    # Optional: Set dark or light background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(248, 249, 250)

    # Add Title
    txBox = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    tf = txBox.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(44, 62, 80)
    p.alignment = PP_ALIGN.CENTER

    # === Helper Function for PIL Gradient ===
    def lerp_color(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    def get_gradient_color(t):
        c_green = (46, 204, 113)
        c_yellow = (241, 196, 15)
        c_red = (231, 76, 60)
        if t < 0.5:
            return lerp_color(c_green, c_yellow, t * 2)
        else:
            return lerp_color(c_yellow, c_red, (t - 0.5) * 2)

    # === Layer 1: Generate Gauge Background using PIL ===
    # We create an 800x400 image (semi-circle). Outer radius 350, inner radius 220.
    gauge_w, gauge_h = 800, 400
    
    # 1. Create linear gradient base
    grad_img = Image.new('RGB', (gauge_w, gauge_h))
    draw_grad = ImageDraw.Draw(grad_img)
    for x in range(gauge_w):
        color = get_gradient_color(x / float(gauge_w - 1))
        draw_grad.line((x, 0, x, gauge_h), fill=color)

    # 2. Create Alpha Mask for the Donut Arc
    # Draw on an 800x800 canvas so we can easily draw full circles, then crop
    mask = Image.new('L', (800, 800), 0)
    draw_mask = ImageDraw.Draw(mask)
    
    # Outer circle (White / visible)
    draw_mask.pieslice([50, 50, 750, 750], 180, 360, fill=255)
    # Inner circle (Black / transparent)
    draw_mask.pieslice([220, 220, 580, 580], 180, 360, fill=0)
    
    # Crop mask to upper half
    mask = mask.crop((0, 0, gauge_w, gauge_h))
    grad_img.putalpha(mask)
    
    gauge_path = "temp_gauge.png"
    grad_img.save(gauge_path)

    # === Layer 2: Generate Pivot-Perfect Needle using PIL ===
    # Image size is 800x800. Pivot is exactly at center (400, 400).
    # Default 0-degree state points LEFT.
    needle_img = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
    draw_needle = ImageDraw.Draw(needle_img)
    
    needle_color = (44, 62, 80, 255)
    
    # Needle triangle: Points Left. Base top/bottom slightly above/below center.
    tip = (100, 400)
    base_top = (400, 385)
    base_bottom = (400, 415)
    draw_needle.polygon([base_top, tip, base_bottom], fill=needle_color)
    
    # Pivot Hub Circle
    r = 30
    draw_needle.ellipse([400-r, 400-r, 400+r, 400+r], fill=needle_color)
    
    # Inner Hub Decorative Circle (White)
    r_inner = 10
    draw_needle.ellipse([400-r_inner, 400-r_inner, 400+r_inner, 400+r_inner], fill=(255, 255, 255, 255))
    
    needle_path = "temp_needle.png"
    needle_img.save(needle_path)

    # === Insert Elements into Slide ===
    # Layout dimensions
    gauge_left = Inches(2.666)
    gauge_top = Inches(2.5)
    gauge_width = Inches(8)
    gauge_height = Inches(4)
    
    # Insert Gauge (Semi-circle)
    slide.shapes.add_picture(gauge_path, gauge_left, gauge_top, gauge_width, gauge_height)
    
    # Insert Needle (Square 8x8 image centered at gauge pivot)
    # The pivot of the gauge is at center-bottom: (gauge_left + 4, gauge_top + 4)
    # If the 8x8 needle image is placed at (gauge_left, gauge_top), its center aligns exactly with the pivot!
    needle_pic = slide.shapes.add_picture(needle_path, gauge_left, gauge_top, gauge_width, Inches(8))
    
    # Apply Mathematical Rotation
    # 0% = 0 degrees (pointing Left). 100% = 180 degrees (pointing Right).
    clamped_percentage = max(0.0, min(100.0, percentage))
    rotation_angle = (clamped_percentage / 100.0) * 180.0
    needle_pic.rotation = rotation_angle

    # === Add Metric Label ===
    # Placed directly underneath the pivot hub
    txt_left = gauge_left + Inches(3)
    txt_top = gauge_top + Inches(4.2)
    txt_width = Inches(2)
    txt_height = Inches(1)
    
    val_box = slide.shapes.add_textbox(txt_left, txt_top, txt_width, txt_height)
    val_tf = val_box.text_frame
    val_tf.text = f"{int(percentage)}%"
    val_p = val_tf.paragraphs[0]
    val_p.font.size = Pt(54)
    val_p.font.bold = True
    val_p.font.color.rgb = RGBColor(44, 62, 80)
    val_p.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    
    # Clean up temp files
    if os.path.exists(gauge_path): os.remove(gauge_path)
    if os.path.exists(needle_path): os.remove(needle_path)
    
    return output_pptx_path
