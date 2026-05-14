def create_slide(
    output_pptx_path: str,
    title_text: str = "PERFORMANCE",
    value_pct: float = 0.65,  # Percentage between 0.0 and 1.0
    metric_label: str = "km/h",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Neon Cyber Dashboard Gauge visual effect.
    """
    import io
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFilter

    # --- 1. Set up Presentation and Slide ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Dark Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(10, 13, 20)

    # --- 2. Generate the PIL Neon Gauge Image ---
    # High resolution for crispness on standard screens
    img_size = 1600
    img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    glow_layer = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    glow_draw = ImageDraw.Draw(glow_layer)

    cx, cy = img_size / 2, img_size / 2
    r_outer = 650
    r_inner = 550
    r_center = 350

    # Gauge spans from 135 degrees to 405 degrees (270 degree span)
    # In PIL/math: 0 is Right, 90 is Down, 180 is Left, 270 is Up.
    start_deg = 135
    end_deg = 405
    span = end_deg - start_deg
    
    # Calculate where the "needle/fill" stops
    # Bound value_pct between 0 and 1
    val_clamped = max(0.0, min(1.0, value_pct))
    val_deg = start_deg + (span * val_clamped)

    # Colors
    color_track = (0, 200, 255, 255)       # Neon Cyan
    color_fill = (255, 20, 60, 255)        # Crimson Red
    color_dark_glow = (0, 80, 200, 180)    # Deep Blue Glow
    color_inner_base = (15, 25, 45, 255)   # Center Dial Base

    # Draw Central Hub
    glow_draw.ellipse([cx-r_center, cy-r_center, cx+r_center, cy+r_center], outline=color_dark_glow, width=30)
    draw.ellipse([cx-r_center, cy-r_center, cx+r_center, cy+r_center], fill=color_inner_base, outline=color_track, width=5)

    # Draw Tick Marks
    # We'll draw 100 ticks (one for each percentage point)
    for i in range(0, 101, 1):
        angle_deg = start_deg + (span * i / 100.0)
        rad = math.radians(angle_deg)
        
        # Determine tick length and thickness
        is_major = (i % 10 == 0)
        is_medium = (i % 5 == 0) and not is_major
        
        if is_major:
            r1 = r_inner - 20
            width = 12
        elif is_medium:
            r1 = r_inner + 20
            width = 8
        else:
            r1 = r_inner + 50
            width = 4
            
        r2 = r_outer

        # Determine color (filled vs track)
        current_color = color_fill if angle_deg <= val_deg else color_track

        x1 = cx + r1 * math.cos(rad)
        y1 = cy + r1 * math.sin(rad)
        x2 = cx + r2 * math.cos(rad)
        y2 = cy + r2 * math.sin(rad)

        # Draw on glow layer (thicker) and main layer (crisp)
        glow_draw.line([(x1, y1), (x2, y2)], fill=current_color, width=width*2)
        draw.line([(x1, y1), (x2, y2)], fill=current_color, width=width)

    # Draw thick inner track ring
    bbox_track = [cx - r_inner + 40, cy - r_inner + 40, cx + r_inner - 40, cy + r_inner - 40]
    # Draw empty track
    glow_draw.arc(bbox_track, start=start_deg, end=end_deg, fill=color_dark_glow, width=40)
    draw.arc(bbox_track, start=start_deg, end=end_deg, fill=(0, 50, 100, 255), width=10)
    # Draw filled track
    if val_deg > start_deg:
        glow_draw.arc(bbox_track, start=start_deg, end=val_deg, fill=color_fill, width=50)
        draw.arc(bbox_track, start=start_deg, end=val_deg, fill=color_fill, width=20)

    # Apply blur to glow layer and composite
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(30))
    final_img = Image.alpha_composite(blurred_glow, img)

    # Save to memory stream
    img_stream = io.BytesIO()
    final_img.save(img_stream, format='PNG')
    img_stream.seek(0)

    # --- 3. Insert Image & Add PPTX Overlays ---
    # Center the gauge on the slide
    img_display_size = Inches(6.5)
    left = (prs.slide_width - img_display_size) / 2
    top = (prs.slide_height - img_display_size) / 2 + Inches(0.2)
    slide.shapes.add_picture(img_stream, left, top, img_display_size, img_display_size)

    # Add Main Metric Text inside the gauge
    txBox_val = slide.shapes.add_textbox(Inches(4.66), Inches(4.0), Inches(4.0), Inches(1.5))
    tf_val = txBox_val.text_frame
    p_val = tf_val.paragraphs[0]
    p_val.text = f"{int(val_clamped * 100)}%"
    p_val.alignment = PP_ALIGN.CENTER
    p_val.font.size = Pt(80)
    p_val.font.bold = True
    p_val.font.name = "Arial"
    p_val.font.color.rgb = RGBColor(0, 230, 255) # Match Cyan

    # Add Subtitle/Metric Label
    txBox_lbl = slide.shapes.add_textbox(Inches(5.16), Inches(5.3), Inches(3.0), Inches(0.8))
    tf_lbl = txBox_lbl.text_frame
    p_lbl = tf_lbl.paragraphs[0]
    p_lbl.text = metric_label.upper()
    p_lbl.alignment = PP_ALIGN.CENTER
    p_lbl.font.size = Pt(24)
    p_lbl.font.bold = True
    p_lbl.font.name = "Arial"
    p_lbl.font.color.rgb = RGBColor(150, 180, 200)

    # Add Top Title
    txBox_title = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    tf_title = txBox_title.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.alignment = PP_ALIGN.CENTER
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.name = "Arial"
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
