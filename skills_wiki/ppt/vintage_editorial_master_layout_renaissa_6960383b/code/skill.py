def create_slide(
    output_pptx_path: str,
    title_text: str = "Classic Heritage",
    body_items: list = ["Artisanal Quality", "Timeless Design", "Curated Experiences", "Authentic Materials"],
    image_keyword: str = "vintage,architecture",
    theme_color: tuple = (84, 66, 52),  # Dark warm brown
    bg_base_color: tuple = (242, 235, 217),  # Parchment base
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Vintage Editorial Master Layout.
    Uses PIL to generate a procedural parchment vignette and photo-realistic image frames.
    
    Returns: path to the saved PPTX file.
    """
    import math
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_CONNECTOR
    from PIL import Image, ImageDraw, ImageFilter
    import os

    # === Helper: Generate Background Vignette ===
    def make_vignette_bg(width_px, height_px, base_rgb):
        img = Image.new('RGBA', (width_px, height_px), base_rgb)
        pixels = img.load()
        cx, cy = width_px / 2, height_px / 2
        max_d = math.sqrt(cx**2 + cy**2)
        
        # Apply radial darkening towards edges
        for y in range(height_px):
            for x in range(width_px):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                factor = (dist / max_d) ** 1.8  # Exponential falloff for softer center
                r = max(0, int(base_rgb[0] - 40 * factor))
                g = max(0, int(base_rgb[1] - 40 * factor))
                b = max(0, int(base_rgb[2] - 40 * factor))
                pixels[x, y] = (r, g, b, 255)
        return img

    # === Helper: Frame Image with Drop Shadow ===
    def make_framed_image(img_path, target_width_px=800):
        img = Image.open(img_path).convert("RGBA")
        aspect = img.height / img.width
        img = img.resize((target_width_px, int(target_width_px * aspect)), Image.Resampling.LANCZOS)
        
        border = int(target_width_px * 0.04) # 4% border
        shadow_blur = 20
        shadow_offset_x, shadow_offset_y = 10, 15
        
        # 1. Create the framed photo
        framed_w = img.width + 2 * border
        framed_h = img.height + 2 * border
        framed = Image.new("RGBA", (framed_w, framed_h), (250, 248, 245, 255))
        framed.paste(img, (border, border))
        
        # Draw inner thin border line (vintage print style)
        draw = ImageDraw.Draw(framed)
        draw.rectangle([border-3, border-3, framed_w-border+2, framed_h-border+2], 
                       outline=(220, 215, 205, 255), width=1)
        
        # 2. Create larger canvas for shadow compositing
        padding = shadow_blur * 3
        canvas_w = framed_w + padding * 2
        canvas_h = framed_h + padding * 2
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        
        # 3. Generate shadow
        shadow = Image.new("RGBA", (framed_w, framed_h), (0, 0, 0, 90))
        shadow_x = padding + shadow_offset_x
        shadow_y = padding + shadow_offset_y
        canvas.paste(shadow, (shadow_x, shadow_y))
        
        # Blur the shadow
        canvas = canvas.filter(ImageFilter.GaussianBlur(shadow_blur))
        
        # 4. Paste the sharp framed photo over the blurred shadow
        canvas.paste(framed, (padding, padding), framed)
        
        out_path = "temp_framed_asset.png"
        canvas.save(out_path)
        return out_path

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    bg_path = "temp_vignette_bg.png"
    bg_img = make_vignette_bg(1280, 720, bg_base_color)
    bg_img.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Outer Frame ===
    margin = Inches(0.4)
    w, h = prs.slide_width, prs.slide_height
    frame_color = RGBColor(180, 165, 145)
    
    # Draw four individual lines to create a clean transparent border
    lines = [
        (margin, margin, w-margin, margin),             # Top
        (margin, h-margin, w-margin, h-margin),         # Bottom
        (margin, margin, margin, h-margin),             # Left
        (w-margin, margin, w-margin, h-margin)          # Right
    ]
    for x1, y1, x2, y2 in lines:
        l = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
        l.line.color.rgb = frame_color
        l.line.width = Pt(1)

    # === Layer 3: Image Acquisition and Placement ===
    raw_img_path = "temp_raw_image.jpg"
    try:
        url = "https://picsum.photos/seed/vintageeditorial/1024/768"
        urllib.request.urlretrieve(url, raw_img_path)
    except Exception:
        # Fallback image generation
        fallback = Image.new("RGB", (1024, 768), (170, 160, 150))
        draw = ImageDraw.Draw(fallback)
        draw.line((0,0,1024,768), fill=(200,190,180), width=3)
        draw.line((1024,0,0,768), fill=(200,190,180), width=3)
        fallback.save(raw_img_path)

    framed_img_path = make_framed_image(raw_img_path)
    
    # Place on the right side of the layout. Bounding box width is 6 inches.
    # Due to shadow padding, the visual picture will be slightly smaller and perfectly framed.
    slide.shapes.add_picture(framed_img_path, Inches(6.5), Inches(1.0), width=Inches(6.0))

    # === Layer 4: Typography and Content ===
    # Main Title
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(5.0), Inches(1.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(54)
    p.font.name = "Georgia"
    p.font.color.rgb = RGBColor(*theme_color)
    
    # Separator Line
    sep_line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(1.0), Inches(2.8), Inches(4.0), Inches(2.8))
    sep_line.line.color.rgb = RGBColor(*theme_color)
    sep_line.line.width = Pt(1.5)
    
    # Body List Items
    top_y = 3.3
    for item in body_items:
        tb = slide.shapes.add_textbox(Inches(1.0), Inches(top_y), Inches(5.0), Inches(0.6))
        p = tb.text_frame.paragraphs[0]
        p.text = item
        p.font.size = Pt(24)
        p.font.name = "Georgia"
        p.font.italic = True
        p.font.color.rgb = RGBColor(*theme_color)
        top_y += 0.7

    # Save and clean up
    prs.save(output_pptx_path)
    
    for tmp_file in [bg_path, raw_img_path, framed_img_path]:
        if os.path.exists(tmp_file):
            try:
                os.remove(tmp_file)
            except OSError:
                pass

    return output_pptx_path
