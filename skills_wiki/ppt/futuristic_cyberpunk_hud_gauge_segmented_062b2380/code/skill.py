def create_slide(
    output_pptx_path: str,
    title_text: str = "元宇宙商機市場分析\n硬體佔有率 Metaverse",
    percentage: int = 65,
    subtitle_text: str = "2021 X牌VR設備佔有率",
    bg_theme: str = "virtual reality",
    accent_color: tuple = (0, 255, 255),  # Neon Cyan
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Futuristic Cyberpunk HUD Gauge visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw, ImageFilter
    import requests
    import io
    import math

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # === Layer 1: Background Setup ===
    # Attempt to download a relevant background image
    try:
        url = f"https://source.unsplash.com/1600x900/?{bg_theme.replace(' ', ',')}"
        response = requests.get(url, timeout=5)
        image_stream = io.BytesIO(response.content)
        slide.shapes.add_picture(image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except:
        # Fallback to solid dark background if network fails
        bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(18, 30, 85)
        bg.line.fill.background()

    # Add deep blue tint overlay (Color Grading)
    overlay = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = RGBColor(13, 20, 60)
    # Set transparency using lxml (approx 40% transparent)
    overlay.fill._xPr.solidFill.srgbClr.set('val', '0D143C')
    overlay.fill._xPr.solidFill.srgbClr.set('alpha', '80000') # 80% opacity
    overlay.line.fill.background()

    # === Layer 2: PIL HUD Gauge Generation ===
    img_size = 1000
    hud_img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(hud_img)
    
    center = (img_size//2, img_size//2)
    outer_radius = 400
    track_width = 80
    segments = 32
    
    # 2a. Draw Segmented Track (Replicating Donut + Star intersection)
    track_color = (accent_color[0], accent_color[1], accent_color[2], 60) # Faded accent
    for i in range(segments):
        start_angle = i * (360 / segments)
        # Leave a small gap between segments
        end_angle = start_angle + (360 / segments) * 0.7 
        bbox = [center[0]-outer_radius, center[1]-outer_radius, 
                center[0]+outer_radius, center[1]+outer_radius]
        draw.arc(bbox, start_angle, end_angle, fill=track_color, width=track_width)
        
    # 2b. Draw Progress Arc
    # Offset by -90 degrees so it starts at the top (12 o'clock)
    progress_end_angle = -90 + (percentage / 100) * 360
    progress_bbox = [center[0]-outer_radius, center[1]-outer_radius, 
                     center[0]+outer_radius, center[1]+outer_radius]
    
    # Create a separate layer for the glow to apply blur
    glow_layer = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.arc(progress_bbox, -90, progress_end_angle, fill=accent_color+(255,), width=track_width)
    
    # Apply blur for neon effect and merge
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(15))
    hud_img = Image.alpha_composite(hud_img, blurred_glow)
    hud_img = Image.alpha_composite(hud_img, glow_layer) # Hard edge on top
    
    # 2c. Inner decorative ring
    inner_radius = 280
    inner_bbox = [center[0]-inner_radius, center[1]-inner_radius, 
                  center[0]+inner_radius, center[1]+inner_radius]
    draw = ImageDraw.Draw(hud_img)
    draw.arc(inner_bbox, 0, 360, fill=(accent_color[0], accent_color[1], accent_color[2], 120), width=3)

    # Save PIL image to buffer and insert to PPTX
    img_buffer = io.BytesIO()
    hud_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Position gauge on the right side
    gauge_size = Inches(5.5)
    gauge_left = Inches(7.0)
    gauge_top = Inches(1.0)
    slide.shapes.add_picture(img_buffer, gauge_left, gauge_top, width=gauge_size, height=gauge_size)

    # === Layer 3: Text & Content ===
    
    # Center Percentage Text (Over the gauge)
    pct_box = slide.shapes.add_textbox(gauge_left, gauge_top, gauge_size, gauge_size)
    pct_tf = pct_box.text_frame
    pct_tf.text = f"{percentage}%"
    pct_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    # Vertical alignment hack using space
    pct_tf.paragraphs[0].space_before = Pt(130) 
    pct_font = pct_tf.paragraphs[0].runs[0].font
    pct_font.size = Pt(72)
    pct_font.bold = True
    pct_font.name = 'Arial'
    pct_font.color.rgb = RGBColor(*accent_color)
    
    # Left Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(4), Inches(5), Inches(2))
    title_tf = title_box.text_frame
    title_tf.word_wrap = True
    p = title_tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Decorative line under title
    line = slide.shapes.add_shape(9, Inches(1.2), Inches(5.2), Inches(3.5), 0)
    line.line.color.rgb = RGBColor(*accent_color)
    line.line.width = Pt(2)
    
    # Subtitle under gauge
    sub_box = slide.shapes.add_textbox(gauge_left, gauge_top + gauge_size, gauge_size, Inches(1))
    sub_tf = sub_box.text_frame
    sub_tf.text = subtitle_text
    sub_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    sub_font = sub_tf.paragraphs[0].runs[0].font
    sub_font.size = Pt(18)
    sub_font.color.rgb = RGBColor(200, 200, 220)

    prs.save(output_pptx_path)
    return output_pptx_path
