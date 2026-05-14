def create_slide(
    output_pptx_path: str,
    title_text: str = "POWERPOINT",
    subtitle_text: str = "汇报人：清风       部门：清风\n\n清风专业PPT培训定制",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Holographic Glassmorphism" title slide effect.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import random
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from PIL import Image, ImageDraw, ImageFilter

    prs = Presentation()
    # Set to 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # ==========================================
    # Layer 1: Generate Aurora/Mesh Background via PIL
    # ==========================================
    bg_img_path = "temp_aurora_bg.png"
    width, height = 1280, 720
    
    # Base dark color
    base_color = (15, 25, 35)
    img = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(img)
    
    # Draw soft, large colored blobs
    colors = [
        (0, 190, 200),    # Teal
        (200, 220, 100),  # Soft Yellow/Green
        (80, 120, 220),   # Light Blue
        (120, 60, 160)    # Purple
    ]
    
    for _ in range(5):
        color = random.choice(colors)
        radius = random.randint(300, 600)
        x = random.randint(-200, width + 200)
        y = random.randint(-200, height + 200)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
        
    # Apply massive blur to create the mesh gradient effect
    img = img.filter(ImageFilter.GaussianBlur(radius=150))
    img.save(bg_img_path)
    
    # Insert background into slide
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # ==========================================
    # Layer 2: Glassmorphism Center Panel
    # ==========================================
    panel_width = Inches(7.0)
    panel_height = Inches(2.2)
    panel_left = (prs.slide_width - panel_width) / 2
    panel_top = (prs.slide_height - panel_height) / 2 - Inches(0.5)

    glass_panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, panel_left, panel_top, panel_width, panel_height
    )
    # Style as dark frosted glass
    glass_panel.fill.solid()
    glass_panel.fill.fore_color.rgb = RGBColor(0, 0, 0)
    glass_panel.fill.transparency = 0.45
    glass_panel.line.color.rgb = RGBColor(255, 255, 255)
    glass_panel.line.transparency = 0.8  # Very faint white border
    glass_panel.line.width = Pt(1)

    # ==========================================
    # Layer 3: Typography
    # ==========================================
    # Main Title
    title_box = slide.shapes.add_textbox(panel_left, panel_top + Inches(0.2), panel_width, Inches(1.0))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text
    run.font.name = "Arial"
    run.font.size = Pt(60)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle
    sub_box = slide.shapes.add_textbox(panel_left, panel_top + Inches(1.2), panel_width, Inches(1.0))
    sub_frame = sub_box.text_frame
    sub_frame.clear()
    p_sub = sub_frame.paragraphs[0]
    p_sub.alignment = PP_ALIGN.CENTER
    run_sub = p_sub.add_run()
    run_sub.text = subtitle_text
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(230, 230, 230)

    # ==========================================
    # Layer 4: Geometric Accents (Triangles & Lines)
    # ==========================================
    
    # Left floating triangle
    tri_left = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE, 
        panel_left - Inches(1.0), panel_top + Inches(0.5), Inches(0.8), Inches(1.2)
    )
    tri_left.fill.background() # No fill
    tri_left.line.color.rgb = RGBColor(255, 255, 255)
    tri_left.line.transparency = 0.4
    tri_left.line.width = Pt(1.5)
    tri_left.rotation = -90

    # Right floating triangle (smaller)
    tri_right = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE, 
        panel_left + panel_width + Inches(0.3), panel_top + Inches(1.0), Inches(0.6), Inches(0.8)
    )
    tri_right.fill.background() # No fill
    tri_right.line.color.rgb = RGBColor(255, 255, 255)
    tri_right.line.transparency = 0.3
    tri_right.line.width = Pt(1.5)
    tri_right.rotation = 45
    
    # Bottom accent line with dots
    line_top = panel_top + panel_height + Inches(0.5)
    line_left = (prs.slide_width - Inches(3.0)) / 2
    accent_line = slide.shapes.add_shape(
        MSO_SHAPE.LINE_CALLOUT_1,  # Using standard line
        line_left, line_top, Inches(3.0), Inches(0)
    )
    # In pptx, creating a simple line with connector works best
    connector = slide.shapes.add_connector(
        1, line_left, line_top, line_left + Inches(3.0), line_top
    )
    connector.line.color.rgb = RGBColor(255, 255, 255)
    connector.line.width = Pt(1)
    connector.line.transparency = 0.3
    # Small dot accent (simulating line end)
    dot = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        line_left + Inches(3.0) - Inches(0.04), line_top - Inches(0.04), Inches(0.08), Inches(0.08)
    )
    dot.fill.solid()
    dot.fill.fore_color.rgb = RGBColor(255, 255, 255)
    dot.line.fill.background()

    # Save and cleanup
    prs.save(output_pptx_path)
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
