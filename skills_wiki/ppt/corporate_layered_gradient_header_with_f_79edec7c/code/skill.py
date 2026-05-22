def create_slide(
    output_pptx_path: str,
    title_text: str = "Quarterly Sales Review",
    body_text: str = "YOUR COMPANY NAME",
    bg_palette: str = "teal",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Layered Corporate Gradient Header" visual effect.
    
    Args:
        output_pptx_path: Path to save the PPTX file.
        title_text: Main header text.
        body_text: Subtitle text.
        bg_palette: Color theme ('teal', 'navy', 'purple', 'sunset').
    """
    import os
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw, ImageFilter
    
    # 1. Setup Color Palettes
    palettes = {
        "teal": {"c1": (81, 196, 211), "c2": (33, 147, 176)},
        "navy": {"c1": (44, 62, 80), "c2": (26, 37, 47)},
        "purple": {"c1": (157, 80, 187), "c2": (110, 56, 131)},
        "sunset": {"c1": (255, 126, 95), "c2": (254, 180, 123)}
    }
    colors = palettes.get(bg_palette, palettes["teal"])
    
    # 2. Setup PIL Canvas (1080p resolution for high fidelity)
    W, H = 1920, 1080
    header_h = int(H * 0.55)
    
    # Base Canvas (Off-white)
    base = Image.new('RGBA', (W, H), (250, 251, 252, 255))
    
    # --- LAYER 1: Header Drop Shadow ---
    header_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_hs = ImageDraw.Draw(header_shadow)
    draw_hs.rectangle([0, header_h - 10, W, header_h + 30], fill=(0, 0, 0, 60))
    header_shadow = header_shadow.filter(ImageFilter.GaussianBlur(18))
    base = Image.alpha_composite(base, header_shadow)
    
    # --- LAYER 2: Gradient Header & Light Ray ---
    header_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_header = ImageDraw.Draw(header_layer)
    
    # Linear Gradient
    c1, c2 = colors["c1"], colors["c2"]
    for x in range(W):
        r = int(c1[0] + (c2[0] - c1[0]) * (x / W))
        g = int(c1[1] + (c2[1] - c1[1]) * (x / W))
        b = int(c1[2] + (c2[2] - c1[2]) * (x / W))
        draw_header.line([(x, 0), (x, header_h)], fill=(r, g, b, 255))
        
    # Diagonal light ray (paper fold effect)
    poly_points = [(W * 0.4, 0), (W * 0.8, 0), (W * 0.5, header_h), (W * 0.1, header_h)]
    draw_header.polygon(poly_points, fill=(255, 255, 255, 12))
    base = Image.alpha_composite(base, header_layer)
    
    # --- LAYER 3: Floating Hero Element Shadow ---
    float_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_fs = ImageDraw.Draw(float_shadow)
    
    # Geometry metrics for Magnifying Glass
    cx, cy = int(W * 0.78), header_h
    r_outer = 220
    r_inner = 180
    
    # Ring shadow
    draw_fs.ellipse([cx - r_outer + 8, cy - r_outer + 15, cx + r_outer + 8, cy + r_outer + 15], fill=(0, 0, 0, 70))
    
    # Handle shadow
    angle = math.radians(45)
    hx, hy = cx + r_outer * math.cos(angle), cy + r_outer * math.sin(angle)
    ex, ey = hx + 130 * math.cos(angle), hy + 130 * math.sin(angle)
    draw_fs.line([(hx, hy), (ex, ey)], fill=(0, 0, 0, 70), width=45)
    float_shadow = float_shadow.filter(ImageFilter.GaussianBlur(15))
    base = Image.alpha_composite(base, float_shadow)
    
    # --- LAYER 4: Floating Hero Element ---
    float_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_fe = ImageDraw.Draw(float_layer)
    
    # Handle Body
    draw_fe.line([(hx, hy), (ex, ey)], fill=(235, 240, 245, 255), width=45)
    draw_fe.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], fill=(235, 240, 245, 255)) # Rounded Cap
    
    # Outer Ring (requires Pillow >= 8.0.0 for width parameter on ellipse)
    try:
        draw_fe.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=(255, 255, 255, 255), width=(r_outer-r_inner))
    except TypeError:
        # Fallback for very old Pillow versions
        for r in range(r_inner, r_outer):
            draw_fe.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 255))
            
    # Internal Line Chart Graphic
    chart_pts = [
        (cx - 90, cy + 40),
        (cx - 30, cy - 30),
        (cx + 30, cy + 20),
        (cx + 90, cy - 60)
    ]
    # Connecting lines
    for i in range(len(chart_pts)-1):
        draw_fe.line([chart_pts[i], chart_pts[i+1]], fill=(255, 255, 255, 255), width=10)
    # Data nodes
    for pt in chart_pts:
        draw_fe.ellipse([pt[0]-12, pt[1]-12, pt[0]+12, pt[1]+12], fill=(255, 255, 255, 255))

    base = Image.alpha_composite(base, float_layer)
    
    # Save composite background
    bg_path = os.path.join(os.path.dirname(output_pptx_path) or ".", "temp_bg.png")
    base.save(bg_path)
    
    # 3. Build PPTX Document
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Insert constructed background
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # 4. Add Editable Typography
    text_left = Inches(1.0)
    
    # Title Text
    title_box = slide.shapes.add_textbox(text_left, Inches(1.8), Inches(8.0), Inches(1.5))
    tf_title = title_box.text_frame
    p_title = tf_title.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(54)
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    p_title.font.name = "Arial"
    
    # Subtitle Text
    sub_box = slide.shapes.add_textbox(text_left, Inches(2.9), Inches(8.0), Inches(1.0))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.add_paragraph()
    p_sub.text = body_text.upper()
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(255, 255, 255)
    p_sub.font.name = "Arial"
    
    prs.save(output_pptx_path)
    
    # Cleanup temp image
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
