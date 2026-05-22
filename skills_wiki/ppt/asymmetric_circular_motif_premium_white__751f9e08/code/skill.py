def create_slide(
    output_pptx_path: str,
    title_text: str = "MORE FUN,\nMORE\nFASHION",
    body_text: str = "yourwebsite.com\nyour@name.com",
    bg_palette: str = "fashion,model", 
    accent_color: tuple = (155, 89, 182),  # Plum/Purple accent
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Asymmetric Circular Motif" editorial layout.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Colors
    color_accent = RGBColor(*accent_color)
    color_dark = RGBColor(30, 30, 30)
    color_gray = RGBColor(120, 120, 120)

    # ==========================================
    # Layer 1: The Giant Circular Image (Right)
    # ==========================================
    # 1. Fetch image
    image_url = f"https://source.unsplash.com/random/1200x1200/?{bg_palette}"
    temp_img_path = "temp_circle_img.png"
    
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        img = Image.open(BytesIO(img_data)).convert("RGBA")
    except Exception as e:
        print(f"Image download failed, using fallback. Error: {e}")
        # Fallback: Create a gray gradient block if download fails
        img = Image.new("RGBA", (1200, 1200), (220, 220, 220, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 1200, 1200], fill=(230, 230, 230, 255))

    # 2. Crop to perfect square
    size = min(img.width, img.height)
    left = (img.width - size) // 2
    top = (img.height - size) // 2
    img = img.crop((left, top, left + size, top + size))
    
    # 3. Create crisp circular mask (using 2x downsampling for anti-aliasing)
    mask = Image.new("L", (size * 2, size * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size * 2, size * 2), fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)
    
    # 4. Apply mask and save
    img.putalpha(mask)
    img.save(temp_img_path, format="PNG")
    
    # 5. Insert into PPTX (Bleeding off the right and bottom edges)
    # Circle diameter = 8 inches
    circle_size = Inches(8.5)
    img_left = Inches(6.5)  # Pushed to the right
    img_top = Inches(0.5)   # Slightly down from top
    
    pic = slide.shapes.add_picture(temp_img_path, img_left, img_top, width=circle_size, height=circle_size)

    # Clean up temp file
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)


    # ==========================================
    # Layer 2: Top Left "Logo" Layout
    # ==========================================
    # Small aesthetic logo marks (three overlapping half-arches/shapes - simplified here to shapes)
    logo_base_x = Inches(1.0)
    logo_base_y = Inches(0.6)
    
    # Abstract logo icon (represented by a simple stylized shape/text combo)
    tx_box_logo = slide.shapes.add_textbox(logo_base_x, logo_base_y, Inches(3), Inches(0.5))
    tf_logo = tx_box_logo.text_frame
    p_logo = tf_logo.add_paragraph()
    p_logo.text = "FASHION SHOP"
    p_logo.font.name = "Arial"
    p_logo.font.size = Pt(14)
    p_logo.font.bold = True
    p_logo.font.color.rgb = color_dark
    p_logo.font.letter_spacing = Pt(1.5)


    # ==========================================
    # Layer 3: Main Typography (Left Center)
    # ==========================================
    tx_box_main = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.5), Inches(3))
    tf_main = tx_box_main.text_frame
    tf_main.word_wrap = True
    
    p_title = tf_main.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Arial Black"  # Heavy bold font
    p_title.font.size = Pt(48)
    p_title.font.bold = True
    p_title.font.color.rgb = color_dark
    # Tight line spacing for editorial feel
    p_title.line_spacing = 0.9 


    # ==========================================
    # Layer 4: Floating Details (Bottom Left)
    # ==========================================
    # Adding tiny accent 'icons' (represented by text symbols for pure pptx code)
    # and contact info
    
    tx_box_contact = slide.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(5), Inches(1))
    tf_contact = tx_box_contact.text_frame
    
    # Line 1
    p_c1 = tf_contact.paragraphs[0]
    # '►' used as a structural bullet in accent color
    run_bullet1 = p_c1.add_run()
    run_bullet1.text = "► "
    run_bullet1.font.color.rgb = color_accent
    run_bullet1.font.size = Pt(12)
    
    run_text1 = p_c1.add_run()
    run_text1.text = body_text.split('\n')[0] if '\n' in body_text else body_text
    run_text1.font.name = "Arial"
    run_text1.font.size = Pt(14)
    run_text1.font.color.rgb = color_gray

    # Line 2 (if exists)
    if '\n' in body_text:
        p_c2 = tf_contact.add_paragraph()
        p_c2.space_before = Pt(6)
        run_bullet2 = p_c2.add_run()
        run_bullet2.text = "► "
        run_bullet2.font.color.rgb = color_accent
        run_bullet2.font.size = Pt(12)
        
        run_text2 = p_c2.add_run()
        run_text2.text = body_text.split('\n')[1]
        run_text2.font.name = "Arial"
        run_text2.font.size = Pt(14)
        run_text2.font.color.rgb = color_gray


    prs.save(output_pptx_path)
    return output_pptx_path
