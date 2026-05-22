def create_slide(
    output_pptx_path: str,
    title_text: str = "HOW TO MASK\nTEXT IN\nPOWERPOINT",
    bg_palette: str = "bird,nature",  # Keyword for stock image
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Photographic Text Masking' visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches
    from PIL import Image, ImageDraw, ImageFont
    import urllib.request
    import io
    import os

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Setup dimensions (1920x1080 for 16:9)
    img_w, img_h = 1920, 1080

    # 2. Fetch Background Image (with fallback)
    try:
        # Using a reliable stock image service via keyword
        url = f"https://image.pollinations.ai/prompt/{bg_palette.replace(',', '%20')}?width=1920&height=1080&nologo=true"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            base_img = Image.open(io.BytesIO(response.read())).convert("RGBA")
    except Exception as e:
        print(f"Image download failed, using gradient fallback. Error: {e}")
        # Fallback: Create a vibrant gradient if network fails
        base_img = Image.new('RGBA', (img_w, img_h))
        draw_base = ImageDraw.Draw(base_img)
        for y in range(img_h):
            r = int(20 + (230 * (y / img_h)))
            g = int(50 + (100 * (y / img_h)))
            b = int(180 + (50 * (y / img_h)))
            draw_base.line([(0, y), (img_w, y)], fill=(r, g, b, 255))

    # Resize background to strictly match canvas
    base_img = base_img.resize((img_w, img_h), Image.Resampling.LANCZOS)

    # 3. Create the Text Alpha Mask
    # L mode (8-bit pixels, black and white)
    mask = Image.new("L", (img_w, img_h), 0)  # Start completely black (transparent)
    draw_mask = ImageDraw.Draw(mask)

    # Robust Font Loading: Try to find a heavy, bold font
    font_options = [
        "impact.ttf", "Impact.ttf", 
        "arialbd.ttf", "Arial Bold.ttf", 
        "trebucbd.ttf", "tahoma.ttf", 
        "DejaVuSans-Bold.ttf"
    ]
    
    font = None
    # Dynamically find the best font size (Start huge and shrink)
    font_size = 350
    
    # Try loading fonts
    for font_name in font_options:
        try:
            font = ImageFont.truetype(font_name, font_size)
            break
        except IOError:
            continue
            
    if not font:
        font = ImageFont.load_default()
        print("Warning: Heavy fonts not found. Using default font.")

    # Format text (add newlines if single long string)
    if "\n" not in title_text and len(title_text) > 15:
        words = title_text.split()
        title_text = "\n".join([" ".join(words[i:i+2]) for i in range(0, len(words), 2)])

    # Scale down font size to fit within 90% of width / 80% of height
    if hasattr(font, "getbbox"):
        while font_size > 50:
            bbox = draw_mask.multiline_textbbox((0, 0), title_text, font=font, align="center")
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            if text_w < img_w * 0.9 and text_h < img_h * 0.8:
                break
            font_size -= 10
            try:
                font = ImageFont.truetype(font.path, font_size)
            except:
                break

    # Calculate centered position
    bbox = draw_mask.multiline_textbbox((0, 0), title_text, font=font, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (img_w - text_w) // 2
    y = (img_h - text_h) // 2

    # Draw white text on black mask (White = keep image, Black = transparent)
    draw_mask.multiline_text((x, y), title_text, font=font, fill=255, align="center")

    # 4. Composite Image and Mask
    # Create a completely transparent canvas
    transparent_bg = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    # Apply the base image onto the transparent canvas using the text as the alpha mask
    final_composite = Image.composite(base_img, transparent_bg, mask)

    # 5. Save and Insert to Slide
    temp_img_path = "temp_text_mask.png"
    final_composite.save(temp_img_path, format="PNG")

    # Insert image taking up the full slide
    slide.shapes.add_picture(temp_img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))

    # Clean up temp file
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
