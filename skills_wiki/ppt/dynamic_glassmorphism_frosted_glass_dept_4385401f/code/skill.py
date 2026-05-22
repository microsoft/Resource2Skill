def create_slide(
    output_pptx_path: str,
    title_text: str = "THE NATURE",
    subtitle_text: str = "B e a u t y   i n   E v e r y   B r e a t h",
    bg_keyword: str = "colorful leaves",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Glassmorphism Reveal Panel effect.
    """
    import os
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Pt, Inches
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
    
    # --- Helper: Fetch Image ---
    def fetch_image(url, fallback_color=(30, 30, 40), size=(1920, 1080)):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                return Image.open(io.BytesIO(response.read())).convert("RGBA")
        except Exception as e:
            print(f"Failed to download image: {e}. Using fallback.")
            img = Image.new("RGBA", size, fallback_color)
            return img

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Calculate dimensions
    w_px, h_px = 1920, 1080
    
    # --- Layer 1: Background Image ---
    bg_url = f"https://source.unsplash.com/random/1920x1080/?{bg_keyword.replace(' ', ',')}"
    bg_img = fetch_image(bg_url, size=(w_px, h_px)).convert("RGB")
    
    # Force 16:9 crop if necessary
    bg_w, bg_h = bg_img.size
    target_ratio = 16 / 9
    current_ratio = bg_w / bg_h
    if current_ratio > target_ratio:
        new_w = int(bg_h * target_ratio)
        offset = (bg_w - new_w) // 2
        bg_img = bg_img.crop((offset, 0, offset + new_w, bg_h))
    elif current_ratio < target_ratio:
        new_h = int(bg_w / target_ratio)
        offset = (bg_h - new_h) // 2
        bg_img = bg_img.crop((0, offset, bg_w, offset + new_h))
        
    bg_img = bg_img.resize((w_px, h_px), Image.Resampling.LANCZOS)
    
    # Save base background to slide
    bg_stream = io.BytesIO()
    bg_img.save(bg_stream, format="PNG")
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Layer 2: Create Frosted Glass Panel via PIL ---
    # Define panel size and position (Center, ~65% width)
    panel_w, panel_h = int(w_px * 0.65), int(h_px * 0.65)
    panel_x, panel_y = (w_px - panel_w) // 2, (h_px - panel_h) // 2
    
    # Crop the area that the glass will cover
    glass_crop = bg_img.crop((panel_x, panel_y, panel_x + panel_w, panel_y + panel_h))
    
    # Apply heavy blur and brighten
    glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=45))
    enhancer = ImageEnhance.Brightness(glass_crop)
    glass_crop = enhancer.enhance(1.4) # Brighten by 40%
    
    # Apply rounded corner mask
    corner_radius = 60
    mask = Image.new("L", (panel_w, panel_h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, panel_w, panel_h), radius=corner_radius, fill=255)
    
    # Combine blur with alpha mask
    glass_crop.putalpha(mask)
    
    # Optional: Add a subtle inner white stroke (simulates glass edge)
    stroke_layer = Image.new("RGBA", (panel_w, panel_h), (0,0,0,0))
    stroke_draw = ImageDraw.Draw(stroke_layer)
    stroke_draw.rounded_rectangle((1, 1, panel_w-2, panel_h-2), radius=corner_radius, outline=(255, 255, 255, 100), width=3)
    glass_crop = Image.alpha_composite(glass_crop, stroke_layer)
    
    # Save glass panel
    glass_stream = io.BytesIO()
    glass_crop.save(glass_stream, format="PNG")
    glass_stream.seek(0)
    
    # Add glass panel to slide at exact center
    pos_x = Inches(13.333) / 2 - Inches(13.333 * 0.65) / 2
    pos_y = Inches(7.5) / 2 - Inches(7.5 * 0.65) / 2
    slide.shapes.add_picture(glass_stream, pos_x, pos_y, width=Inches(13.333 * 0.65), height=Inches(7.5 * 0.65))

    # --- Layer 3: Subject PNG (Bird/Object breaking the frame) ---
    # Using a reliable transparent PNG from Wikimedia as a proxy for the bird
    subject_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Kingfisher_transparent.png/800px-Kingfisher_transparent.png"
    subject_img = fetch_image(subject_url, size=(500, 500))
    
    subject_stream = io.BytesIO()
    subject_img.save(subject_stream, format="PNG")
    subject_stream.seek(0)
    
    # Position subject overlapping the left edge of the glass panel
    subj_w = Inches(5.5)
    subj_h = Inches(5.5)
    subj_x = pos_x - Inches(1.5) # Intersects the glass border
    subj_y = pos_y - Inches(0.5)
    slide.shapes.add_picture(subject_stream, subj_x, subj_y, width=subj_w)

    # --- Layer 4: Typography ---
    # Simulate wide tracking by inserting spaces between characters
    spaced_title = "   ".join(list(title_text))
    
    # Title
    title_box = slide.shapes.add_textbox(pos_x, pos_y + Inches(1.2), Inches(13.333 * 0.65), Inches(1))
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    p = title_frame.paragraphs[0]
    p.text = spaced_title
    p.alignment = PP_ALIGN.CENTER
    font = p.font
    font.name = 'Georgia' # Proxy for Engravers MT / Elegant serif
    font.size = Pt(54)
    font.bold = True
    font.color.rgb = RGBColor(255, 255, 255)
    
    # Subtitle
    sub_box = slide.shapes.add_textbox(pos_x, pos_y + Inches(2.3), Inches(13.333 * 0.65), Inches(0.5))
    sub_frame = sub_box.text_frame
    sub_frame.word_wrap = True
    p_sub = sub_frame.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    sub_font = p_sub.font
    sub_font.name = 'Century Gothic' # Proxy for clean modern sans-serif
    sub_font.size = Pt(18)
    sub_font.color.rgb = RGBColor(230, 230, 230)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
