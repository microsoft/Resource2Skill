def create_slide(
    output_pptx_path: str,
    title_text: str = "Geometric Image Accent",
    body_text: str = "Add depth and visual interest to your presentations by framing your images with customized geometric underlays. This simple yet effective layout emphasizes focus and seamlessly aligns your imagery with your brand's color palette.",
    accent_color: tuple = (0, 150, 136),  # RGB Teal color
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Geometric Offset Underlay Accent visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    import urllib.request
    import os
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Step 1: Download and prepare a square image ===
    img_path = "temp_square_img.jpg"
    try:
        # Download a placeholder image
        req = urllib.request.Request("https://picsum.photos/800/800", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(img_path, 'wb') as f:
                f.write(response.read())
                
        # Ensure the image is perfectly square so it doesn't distort when mapped to the shape
        with Image.open(img_path) as img:
            img = img.convert('RGB')
            min_dim = min(img.size)
            left = (img.size[0] - min_dim) / 2
            top = (img.size[1] - min_dim) / 2
            img_crop = img.crop((left, top, left + min_dim, top + min_dim))
            img_crop.save(img_path)
    except Exception:
        # Fallback if download fails: Create a stylized graphic placeholder
        fallback_img = Image.new('RGB', (800, 800), color=(220, 220, 220))
        draw = ImageDraw.Draw(fallback_img)
        draw.line((0, 0, 800, 800), fill=(180, 180, 180), width=4)
        draw.line((0, 800, 800, 0), fill=(180, 180, 180), width=4)
        fallback_img.save(img_path)

    # === Step 2: Layer 1 - Background Accent Shape (Underlay) ===
    # Adding this first ensures it stays at the back. It is offset slightly down and to the right.
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.HEXAGON,
        left=Inches(1.8), top=Inches(1.5), width=Inches(5.0), height=Inches(5.0)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*accent_color)
    bg_shape.line.color.rgb = RGBColor(*accent_color)  # Match line to fill

    # === Step 3: Layer 2 - Foreground Image Shape ===
    fg_shape = slide.shapes.add_shape(
        MSO_SHAPE.HEXAGON,
        left=Inches(1.5), top=Inches(1.2), width=Inches(5.0), height=Inches(5.0)
    )
    # Filling the shape with an image automatically applies a "crop-to-shape" effect
    fg_shape.fill.user_picture(img_path)
    
    # Add a white outline to the image for crisp separation from the underlay
    fg_shape.line.color.rgb = RGBColor(255, 255, 255)
    fg_shape.line.width = Pt(4)

    # === Step 4: Layer 3 - Typography & Layout ===
    # Small accent line above the title
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left=Inches(7.2), top=Inches(2.0), width=Inches(0.8), height=Inches(0.05)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*accent_color)
    line.line.fill.background()

    # Title text box
    title_box = slide.shapes.add_textbox(Inches(7.2), Inches(2.2), Inches(5.5), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 30, 30)
    p.font.name = "Arial"

    # Body text box
    body_box = slide.shapes.add_textbox(Inches(7.2), Inches(3.5), Inches(5.0), Inches(3.0))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.size = Pt(18)
    p_body.font.color.rgb = RGBColor(100, 100, 100)
    p_body.font.name = "Arial"

    # Save presentation
    prs.save(output_pptx_path)
    
    # Cleanup temporary image file
    if os.path.exists(img_path):
        os.remove(img_path)

    return output_pptx_path
