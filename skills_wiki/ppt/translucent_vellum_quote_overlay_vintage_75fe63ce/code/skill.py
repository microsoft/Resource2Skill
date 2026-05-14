def create_slide(
    output_pptx_path: str,
    title_text: str = "THERE IS NO TIME",
    body_text: str = "like the present",
    bg_palette: str = "vintage floral pattern", 
    accent_color: tuple = (220, 120, 140),  # Vintage Pink
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Translucent Vellum Quote Overlay" aesthetic.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw, ImageFilter

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Helper: Download Background Image ===
    def get_background_image(keyword):
        url = f"https://source.unsplash.com/featured/1920x1080/?{urllib.parse.quote(keyword)}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                return BytesIO(response.read())
        except Exception:
            # Fallback: Create a solid pastel sage background if network fails
            img = Image.new('RGB', (1920, 1080), (230, 240, 230))
            bio = BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)
            return bio

    # 1. Add Background
    bg_image_stream = get_background_image(bg_palette)
    slide.shapes.add_picture(bg_image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Create the Vellum Sticker via PIL ===
    # We create a semi-transparent white rounded rect with a drop shadow and vintage borders
    sticker_w, sticker_h = 1200, 800
    img = Image.new('RGBA', (sticker_w + 100, sticker_h + 100), (0, 0, 0, 0)) # Padding for shadow
    
    # Draw Shadow
    shadow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_box = [55, 55, sticker_w + 45, sticker_h + 45]
    shadow_draw.rounded_rectangle(shadow_box, radius=40, fill=(0, 0, 0, 60))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(15))
    img.alpha_composite(shadow_layer)

    # Draw Vellum Base
    draw = ImageDraw.Draw(img)
    vellum_box = [50, 50, sticker_w + 50, sticker_h + 50]
    draw.rounded_rectangle(vellum_box, radius=40, fill=(255, 255, 255, 215)) # 85% opaque white

    # Draw Vintage Nested Borders
    gold_color = (190, 160, 100, 255)
    outer_border_box = [75, 75, sticker_w + 25, sticker_h + 25]
    draw.rounded_rectangle(outer_border_box, radius=30, outline=gold_color, width=4)
    
    inner_border_box = [85, 85, sticker_w + 15, sticker_h + 15]
    draw.rounded_rectangle(inner_border_box, radius=24, outline=(190, 160, 100, 150), width=1)

    # Save Vellum Sticker
    sticker_stream = BytesIO()
    img.save(sticker_stream, format='PNG')
    sticker_stream.seek(0)

    # Insert Vellum Sticker into PPTX (Centered)
    stick_w = Inches(7)
    stick_h = Inches(4.66)
    stick_l = (prs.slide_width - stick_w) / 2
    stick_t = (prs.slide_height - stick_h) / 2
    slide.shapes.add_picture(sticker_stream, stick_l, stick_t, width=stick_w, height=stick_h)

    # === Layer 3: Craft Paper Accents (Rosettes) ===
    # Adding layered shapes at the corners to mimic the dimensional crafting elements
    def add_rosette(cx, cy, color, size_inches):
        # Base scalloped/star shape
        star = slide.shapes.add_shape(MSO_SHAPE.SEAL_24_POINT, cx - size_inches/2, cy - size_inches/2, size_inches, size_inches)
        star.fill.solid()
        star.fill.fore_color.rgb = RGBColor(*color)
        star.line.color.rgb = RGBColor(255, 255, 255)
        star.line.width = Pt(2)
        
        # Inner circle
        inner_size = size_inches * 0.6
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - inner_size/2, cy - inner_size/2, inner_size, inner_size)
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(*gold_color[:3])
        circle.line.color.rgb = RGBColor(255, 255, 255)

    # Top Left Rosette
    add_rosette(stick_l + Inches(0.5), stick_t + Inches(0.5), accent_color, Inches(1.2))
    # Bottom Right Rosette
    add_rosette(stick_l + stick_w - Inches(0.5), stick_t + stick_h - Inches(0.5), (160, 185, 155), Inches(1.5)) # Sage green

    # === Layer 4: Mixed Typography ===
    # Text box matching the inner frame
    tx_box = slide.shapes.add_textbox(stick_l + Inches(0.5), stick_t + Inches(0.5), stick_w - Inches(1), stick_h - Inches(1))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_SHAPE.RECTANGLE # Center vertically conceptually by spacing

    # Run 1: Top Small Caps / Serif
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    run1 = p1.add_run()
    run1.text = title_text.upper() + "\n"
    run1.font.name = "Georgia"
    run1.font.size = Pt(28)
    run1.font.color.rgb = RGBColor(50, 50, 50)
    run1.font.bold = True

    # Run 2: Middle Script / Italic
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    # Emulate the script feel with an elegant italic
    run2.text = body_text.lower() + "\n"
    run2.font.name = "Georgia"
    run2.font.italic = True
    run2.font.size = Pt(36)
    run2.font.color.rgb = RGBColor(100, 100, 100)

    # Run 3: Accent Word (Pop of color)
    p3 = tf.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    run3 = p3.add_run()
    run3.text = "TODAY" # Additional decorative word to finish the sticker
    run3.font.name = "Trebuchet MS"
    run3.font.size = Pt(44)
    run3.font.color.rgb = RGBColor(*accent_color)
    run3.font.bold = True

    # Vertically center the text within the box by adding space before the first paragraph
    p1.space_before = Pt(40)

    prs.save(output_pptx_path)
    return output_pptx_path
