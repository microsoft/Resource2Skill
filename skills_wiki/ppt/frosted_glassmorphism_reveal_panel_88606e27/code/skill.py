def create_slide(
    output_pptx_path: str,
    title_text: str = "T H E   N A T U R E",
    subtitle_text: str = "B e a u t y   i n   E v e r y   B r e a t h",
    bg_keyword: str = "vibrant leaves",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Frosted Glassmorphism Reveal Panel' visual effect.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFilter

    prs = Presentation()
    # Set 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide

    # Constants & Dimensions
    WIDTH_PX, HEIGHT_PX = 1920, 1080
    GLASS_W_IN, GLASS_H_IN = 9.5, 5.5
    
    # Calculate pixel dimensions for the glass panel based on slide ratio
    GLASS_W_PX = int(WIDTH_PX * (GLASS_W_IN / 13.333))
    GLASS_H_PX = int(HEIGHT_PX * (GLASS_H_IN / 7.5))
    
    # Center coordinates for cropping
    left_px = (WIDTH_PX - GLASS_W_PX) // 2
    top_px = (HEIGHT_PX - GLASS_H_PX) // 2
    right_px = left_px + GLASS_W_PX
    bottom_px = top_px + GLASS_H_PX

    # File paths for temp assets
    bg_path = "temp_bg.jpg"
    glass_path = "temp_glass.png"
    bird_path = "temp_bird.png"

    # --- 1. Fetch & Prepare Background Image ---
    try:
        url = f"https://source.unsplash.com/random/1920x1080/?{bg_keyword.replace(' ', ',')}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bg_path, 'wb') as out_file:
            out_file.write(response.read())
        bg_img = Image.open(bg_path).convert("RGB")
        bg_img = bg_img.resize((WIDTH_PX, HEIGHT_PX), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Failed to download background, generating fallback: {e}")
        bg_img = Image.new('RGB', (WIDTH_PX, HEIGHT_PX), color=(20, 10, 40))
        draw = ImageDraw.Draw(bg_img)
        draw.ellipse((-300, -300, 1200, 1200), fill=(200, 50, 100))
        draw.ellipse((800, 200, 2200, 1400), fill=(50, 150, 200))
        bg_img = bg_img.filter(ImageFilter.GaussianBlur(150))
    
    bg_img.save(bg_path)

    # --- 2. Generate Frosted Glass Panel (PIL) ---
    # Crop the exact center area to maintain perfect alignment
    glass_crop = bg_img.crop((left_px, top_px, right_px, bottom_px))
    
    # Apply Gaussian Blur
    glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=35))
    glass_rgba = glass_crop.convert("RGBA")
    
    # Create white overlay to brighten/frost it
    overlay = Image.new("RGBA", glass_rgba.size, (255, 255, 255, 65))
    glass_rgba = Image.alpha_composite(glass_rgba, overlay)
    
    # Create rounded corner mask
    corner_radius = 60
    mask = Image.new("L", glass_rgba.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, GLASS_W_PX, GLASS_H_PX), radius=corner_radius, fill=255)
    
    # Apply mask
    glass_rgba.putalpha(mask)
    
    # Add subtle white border for the realistic glass edge
    border_layer = Image.new("RGBA", glass_rgba.size, (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_layer)
    border_draw.rounded_rectangle(
        (1, 1, GLASS_W_PX - 2, GLASS_H_PX - 2), 
        radius=corner_radius, 
        outline=(255, 255, 255, 140), 
        width=3
    )
    glass_rgba = Image.alpha_composite(glass_rgba, border_layer)
    glass_rgba.save(glass_path)

    # --- 3. Fetch Foreground Subject (Transparent Bird) ---
    try:
        # Wikipedia Commons Kingfisher (reliable transparent PNG)
        bird_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Flying_Kingfisher_transparent_background.png/800px-Flying_Kingfisher_transparent_background.png"
        req = urllib.request.Request(bird_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bird_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"Failed to download bird, using an empty transparent PNG fallback: {e}")
        empty = Image.new("RGBA", (800, 800), (0,0,0,0))
        empty.save(bird_path)

    # --- 4. Assemble PPTX Elements ---
    # Layer 1: Background Image
    slide.shapes.add_picture(bg_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # Layer 2: Glass Panel (positioned perfectly so the blurred image matches the bg beneath it)
    glass_left = Inches((13.333 - GLASS_W_IN) / 2)
    glass_top = Inches((7.5 - GLASS_H_IN) / 2)
    slide.shapes.add_picture(glass_path, glass_left, glass_top, width=Inches(GLASS_W_IN), height=Inches(GLASS_H_IN))

    # Layer 3: Text Boxes
    # Title Text
    title_box = slide.shapes.add_textbox(Inches(3), Inches(3.2), Inches(7.33), Inches(1))
    title_tf = title_box.text_frame
    title_tf.clear()
    p = title_tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text
    run.font.name = "Georgia"  # Readily available serif fallback
    run.font.size = Pt(40)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle Text
    sub_box = slide.shapes.add_textbox(Inches(3), Inches(4.0), Inches(7.33), Inches(0.5))
    sub_tf = sub_box.text_frame
    sub_tf.clear()
    p2 = sub_tf.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = subtitle_text
    run2.font.name = "Calibri"
    run2.font.size = Pt(14)
    run2.font.color.rgb = RGBColor(255, 255, 255)

    # Layer 4: Foreground Subject (overlapping left edge of the glass)
    slide.shapes.add_picture(
        bird_path, 
        left=Inches(0.5),   # Slightly off-center left, breaking the glass boundary
        top=Inches(1.5), 
        height=Inches(5.0)  # Scale to create depth
    )

    prs.save(output_pptx_path)

    # Cleanup temp files
    for temp_file in [bg_path, glass_path, bird_path]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

    return output_pptx_path
