def create_slide(
    output_pptx_path: str,
    title_text: str = "乘势而上",  # Recommended: 4-character epic title
    subtitle_text: str = "2024 年度工作汇报与战略部署",
    bg_palette: str = "mountain,epic",  # Unsplash keyword
    **kwargs,
) -> str:
    """
    Creates a PPTX reproducing the 'Cinematic Picture-in-Picture' (画中画) title slide.
    Includes the 'Staggered Typography' (高低低高) layout logic.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageEnhance, ImageDraw

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Helper: Download or Generate Base Image ===
    base_img_path = "temp_base_image.jpg"
    try:
        url = f"https://source.unsplash.com/random/1920x1080/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response, open(base_img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback: Generate a dark gradient image if download fails
        img = Image.new('RGB', (1920, 1080))
        draw = ImageDraw.Draw(img)
        for y in range(1080):
            r = int(13 + (40 - 13) * (y / 1080))
            g = int(17 + (50 - 17) * (y / 1080))
            b = int(28 + (70 - 28) * (y / 1080))
            draw.line([(0, y), (1920, y)], fill=(r, g, b))
        img.save(base_img_path)

    # === Layer 1 & 2: PIL Image Processing (Grayscale BG + Color Center) ===
    bg_img_path = "temp_bg_gray.jpg"
    center_img_path = "temp_center_color.jpg"
    
    with Image.open(base_img_path) as img:
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        
        # 1. Create Grayscale Background (Desaturate and slightly darken)
        gray_img = img.convert('L').convert('RGB')
        enhancer = ImageEnhance.Brightness(gray_img)
        dark_gray_img = enhancer.enhance(0.6) # Darken by 40%
        dark_gray_img.save(bg_img_path)
        
        # 2. Create Center Color Crop (40% width, 70% height)
        crop_w, crop_h = int(1920 * 0.4), int(1080 * 0.7)
        left = (1920 - crop_w) // 2
        top = (1080 - crop_h) // 2
        right = left + crop_w
        bottom = top + crop_h
        color_crop = img.crop((left, top, right, bottom))
        color_crop.save(center_img_path)

    # === PPTX Assembly ===
    
    # 1. Insert Grayscale Background
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # 2. Insert Color Center Crop
    center_w_inch = Inches(13.333 * 0.4)
    center_h_inch = Inches(7.5 * 0.7)
    center_left = (prs.slide_width - center_w_inch) / 2
    center_top = (prs.slide_height - center_h_inch) / 2
    slide.shapes.add_picture(center_img_path, center_left, center_top, width=center_w_inch, height=center_h_inch)
    
    # 3. Add Golden/White Frame
    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        center_left - Inches(0.1), center_top - Inches(0.1),
        center_w_inch + Inches(0.2), center_h_inch + Inches(0.2)
    )
    frame.fill.background() # No fill
    frame.line.color.rgb = RGBColor(255, 255, 255) # White frame
    frame.line.width = Pt(1.5)

    # 4. Typography: Staggered Title (旁门左道: 高低错落排版)
    # We break the title into individual text boxes to stagger their Y positions
    char_count = len(title_text)
    if char_count > 0:
        box_width = Inches(1.2)
        box_height = Inches(1.5)
        total_text_width = char_count * box_width
        start_x = (prs.slide_width - total_text_width) / 2
        
        # Y offsets for High-Low-Low-High pattern
        y_offsets = [0, Inches(0.4), Inches(0.4), 0, Inches(0.2), Inches(0.5)] 
        
        for i, char in enumerate(title_text):
            offset = y_offsets[i % len(y_offsets)]
            char_x = start_x + (i * box_width)
            char_y = center_top + Inches(1.0) + offset
            
            tb = slide.shapes.add_textbox(char_x, char_y, box_width, box_height)
            p = tb.text_frame.add_paragraph()
            p.text = char
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(80)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            # Add subtle drop shadow via font styling proxy (native PPT shadow requires lxml, keeping it simple here to ensure stability)

    # 5. Add Subtitle (Bottom of the frame)
    sub_width = center_w_inch
    sub_height = Inches(0.5)
    sub_left = center_left
    sub_top = center_top + center_h_inch - Inches(0.8)
    
    sub_tb = slide.shapes.add_textbox(sub_left, sub_top, sub_width, sub_height)
    sub_tb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    sub_p = sub_tb.text_frame.add_paragraph()
    sub_p.text = subtitle_text
    sub_p.alignment = PP_ALIGN.CENTER
    sub_p.font.size = Pt(16)
    sub_p.font.color.rgb = RGBColor(220, 220, 220)
    sub_p.font.bold = True

    # Save and cleanup
    prs.save(output_pptx_path)
    
    for tmp_file in [base_img_path, bg_img_path, center_img_path]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
            
    return output_pptx_path
