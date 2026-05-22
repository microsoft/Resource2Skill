def create_slide(
    output_pptx_path: str,
    title_text: str = "Save Nature",
    body_text: str = "Protect our planet",
    bg_keyword: str = "waterfall,forest",  
    accent_color: tuple = (255, 215, 0),  # Yellow text
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Glassmorphism Focus Panel effect.
    Returns: path to the saved PPTX file.
    """
    import io
    import urllib.request
    from PIL import Image, ImageFilter, ImageDraw, ImageOps
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    # Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Constants for 16:9 rendering at 150 DPI
    CANVAS_W, CANVAS_H = 2000, 1125
    
    # Define Glass Panel Geometry (in Inches and Pixels)
    # Positioned on the right side of the screen
    panel_left_in = 7.5
    panel_top_in = 1.25
    panel_width_in = 4.5
    panel_height_in = 5.0
    corner_radius_px = 60

    # Convert inches to canvas pixels for cropping
    left_px = int((panel_left_in / 13.333) * CANVAS_W)
    top_px = int((panel_top_in / 7.5) * CANVAS_H)
    width_px = int((panel_width_in / 13.333) * CANVAS_W)
    height_px = int((panel_height_in / 7.5) * CANVAS_H)
    right_px = left_px + width_px
    bottom_px = top_px + height_px

    # === Layer 1: Fetch and Prepare Background Image ===
    try:
        url = f"https://source.unsplash.com/featured/2000x1125/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            bg_img = Image.open(io.BytesIO(response.read())).convert("RGBA")
    except Exception:
        # Fallback: Dark Green/Blue gradient-like solid if network fails
        bg_img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (20, 50, 40, 255))

    # Ensure background exactly matches our calculated 16:9 canvas
    bg_img = ImageOps.fit(bg_img, (CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    
    # Save background to BytesIO and insert
    bg_stream = io.BytesIO()
    bg_img.convert("RGB").save(bg_stream, format="JPEG", quality=85)
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, 0, 0, width=Inches(13.333), height=Inches(7.5))

    # === Layer 2: Generate Glassmorphism Panel via PIL ===
    # 1. Crop the exact region from the background
    crop_box = (left_px, top_px, right_px, bottom_px)
    glass_base = bg_img.crop(crop_box)

    # 2. Apply strong Gaussian Blur
    glass_blurred = glass_base.filter(ImageFilter.GaussianBlur(radius=25))

    # 3. Apply White Frosting Tint (Semi-transparent overlay)
    frost_overlay = Image.new("RGBA", glass_blurred.size, (255, 255, 255, 45)) # 45/255 alpha
    glass_frosted = Image.alpha_composite(glass_blurred, frost_overlay)

    # 4. Create Rounded Rectangle Mask
    mask = Image.new("L", glass_frosted.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, width_px, height_px), radius=corner_radius_px, fill=255)

    # 5. Apply Mask to Frosted Glass
    glass_final = Image.new("RGBA", glass_frosted.size, (0, 0, 0, 0))
    glass_final.paste(glass_frosted, (0, 0), mask)

    # 6. Add a subtle 2px white edge to simulate glass thickness
    draw_edge = ImageDraw.Draw(glass_final)
    draw_edge.rounded_rectangle((1, 1, width_px-1, height_px-1), radius=corner_radius_px, outline=(255, 255, 255, 120), width=3)

    # Save glass panel to BytesIO and insert
    glass_stream = io.BytesIO()
    glass_final.save(glass_stream, format="PNG")
    glass_stream.seek(0)
    slide.shapes.add_picture(
        glass_stream, 
        Inches(panel_left_in), Inches(panel_top_in), 
        width=Inches(panel_width_in), height=Inches(panel_height_in)
    )

    # === Layer 3: Overlay Text (python-pptx native) ===
    # Add title text inside the glass panel
    tx_box = slide.shapes.add_textbox(
        Inches(panel_left_in), Inches(panel_top_in + 2.0), 
        Inches(panel_width_in), Inches(1.0)
    )
    tf = tx_box.text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text
    run.font.name = "Segoe UI"
    run.font.size = Pt(44)
    run.font.bold = True
    run.font.color.rgb = RGBColor(*accent_color)

    # Add body text
    if body_text:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = body_text
        run2.font.name = "Segoe UI"
        run2.font.size = Pt(20)
        run2.font.color.rgb = RGBColor(255, 255, 255)

    # Save output
    prs.save(output_pptx_path)
    return output_pptx_path
