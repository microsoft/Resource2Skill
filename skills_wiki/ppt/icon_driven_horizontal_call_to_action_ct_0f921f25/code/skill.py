def create_slide(
    output_pptx_path: str,
    title_text: str = "Keep In Touch",
    body_text: str = "",
    bg_palette: str = "business",  
    accent_color: tuple = (30, 200, 150),  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Icon-Driven Horizontal CTA Footer effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    import urllib.request
    import os
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # === Layer 1: Background ===
    # Set a soft mint/pastel background color mimicking the video's aesthetic
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(195, 235, 215) 

    # === Layer 2: Top Right Logo ===
    logo_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.5), Inches(2.5), Inches(0.8))
    logo_tf = logo_box.text_frame
    logo_p = logo_tf.paragraphs[0]
    logo_p.text = "Company Logo"
    logo_p.alignment = PP_ALIGN.RIGHT
    logo_p.font.size = Pt(18)
    logo_p.font.bold = True
    logo_p.font.color.rgb = RGBColor(80, 120, 100)

    # === Layer 3: Main Hero Image (The "Gift Voucher" equivalent) ===
    img_path = "temp_hero_image.jpg"
    try:
        # Fetch a visually pleasing placeholder
        req = urllib.request.Request("https://picsum.photos/seed/cta/800/450", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback PIL image if download fails
        img = Image.new("RGB", (800, 450), (245, 245, 245))
        draw = ImageDraw.Draw(img)
        # Draw a simulated card/voucher
        draw.rectangle([20, 20, 780, 430], fill=(220, 220, 220), outline=accent_color, width=8)
        draw.text((300, 200), "Main Presentation Graphic", fill=(100, 100, 100))
        img.save(img_path)
    
    # Place hero image centrally and tilt it slightly (like the video)
    pic = slide.shapes.add_picture(img_path, Inches(2.6), Inches(1.2), Inches(8.0), Inches(4.5))
    pic.rotation = -5  # Slight dynamic tilt

    # Clean up temp image
    if os.path.exists(img_path):
        try:
            os.remove(img_path)
        except:
            pass

    # === Layer 4: Icon-Driven CTA Footer ===
    # Define contact info and universally supported unicode symbols
    contacts = [
        {"icon": "\u260E", "text": "123.456.7890"},         # Telephone
        {"icon": "\u2709", "text": "hello@company.com"},    # Envelope
        {"icon": "\u1F310", "text": "www.company.com"}      # Globe
    ]

    # Layout dimensions
    circle_size = Inches(0.5)
    y_pos = Inches(6.2) # Anchored to the bottom
    
    # X coordinates for evenly spaced 3 columns
    x_positions = [Inches(1.5), Inches(5.5), Inches(9.5)]
    
    dark_gray = RGBColor(60, 60, 60)

    for i, contact in enumerate(contacts):
        x_base = x_positions[i]
        
        # 1. Hollow Circular Outline
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x_base, y_pos, circle_size, circle_size)
        circle.fill.background() # Simulates pure transparency against the solid slide background
        circle.line.color.rgb = dark_gray
        circle.line.width = Pt(1.5)
        
        # 2. Icon (Centered in circle)
        icon_box = slide.shapes.add_textbox(x_base, y_pos, circle_size, circle_size)
        icon_tf = icon_box.text_frame
        icon_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        icon_p = icon_tf.paragraphs[0]
        icon_p.text = contact["icon"]
        icon_p.alignment = PP_ALIGN.CENTER
        icon_p.font.size = Pt(18)
        icon_p.font.color.rgb = dark_gray
        icon_p.font.name = "Segoe UI Symbol" # Safe font for cross-platform symbols
        
        # 3. Contact Details Text (To the right of the circle)
        text_x = x_base + circle_size + Inches(0.15)
        text_y = y_pos + Inches(0.05)
        text_box = slide.shapes.add_textbox(text_x, text_y, Inches(2.5), Inches(0.4))
        text_tf = text_box.text_frame
        text_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        text_p = text_tf.paragraphs[0]
        text_p.text = contact["text"]
        text_p.alignment = PP_ALIGN.LEFT
        text_p.font.size = Pt(14)
        text_p.font.color.rgb = dark_gray

    prs.save(output_pptx_path)
    return output_pptx_path
