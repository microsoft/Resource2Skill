def create_slide(
    output_pptx_path: str,
    title_text: str = "Chapter heading here",
    body_text: str = "An economic indicator is simply any economic statistic, such as the unemployment rate, Gross Domestic Product (GDP), or the inflation rate.",
    bg_keyword: str = "landscape,grass", 
    fg_keyword: str = "plant,hands",
    transparency_percent: int = 55,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Faded Image Overlay" visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw
    import urllib.request
    import io

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Helper function to get image from Unsplash or generate fallback
    def get_image(keyword, width, height, fallback_color):
        try:
            url = f"https://source.unsplash.com/random/{width}x{height}/?{keyword}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=5)
            return Image.open(io.BytesIO(response.read()))
        except Exception:
            # Fallback if download fails
            img = Image.new('RGB', (width, height), fallback_color)
            draw = ImageDraw.Draw(img)
            draw.line((0, 0, width, height), fill=(255,255,255), width=5)
            draw.line((0, height, width, 0), fill=(255,255,255), width=5)
            return img

    # === Layer 1: Background Layer ===
    # Download and insert background image
    bg_img = get_image(bg_keyword, 1920, 1080, (200, 220, 200))
    bg_stream = io.BytesIO()
    bg_img.save(bg_stream, format='JPEG')
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Visual Effect (Faded Image Overlay) ===
    # Download foreground image and apply transparency via PIL
    fg_img = get_image(fg_keyword, 800, 600, (100, 150, 100))
    
    # Ensure image has an alpha channel
    if fg_img.mode != 'RGBA':
        fg_img = fg_img.convert('RGBA')
        
    # Calculate opacity from transparency percentage
    opacity_factor = (100 - transparency_percent) / 100.0
    
    # Adjust the alpha channel
    alpha = fg_img.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity_factor))
    fg_img.putalpha(alpha)
    
    # Save modified image to stream
    fg_stream = io.BytesIO()
    fg_img.save(fg_stream, format='PNG') # Must be PNG to preserve alpha
    fg_stream.seek(0)
    
    # Insert the faded image on the right side
    img_width = Inches(6.5)
    img_height = Inches(4.5)
    img_left = prs.slide_width - img_width - Inches(0.5)
    img_top = Inches(1.5)
    slide.shapes.add_picture(fg_stream, img_left, img_top, width=img_width, height=img_height)

    # === Layer 3: Text & Content ===
    # Add title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(5.0), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(51, 51, 51) # Dark gray

    # Add body text
    body_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.0), Inches(1.5))
    tf = body_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = body_text
    p.font.size = Pt(16)
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(80, 80, 80)

    # Add bullet points
    bullet_texts = [
        "Emphasis text: Helvetica Bold #990000",
        "Emphasis text: Helvetica Bold #990000"
    ]
    
    bullet_box = slide.shapes.add_textbox(Inches(1.0), Inches(3.5), Inches(5.0), Inches(1.5))
    tf = bullet_box.text_frame
    
    for i, b_text in enumerate(bullet_texts):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = b_text
        p.font.size = Pt(16)
        p.font.name = "Arial"
        p.font.color.rgb = RGBColor(80, 80, 80)
        p.level = 0
        
        # In python-pptx, enabling true bullets requires XML manipulation, 
        # but we can simulate a stylized list or enable basic bullets:
        p.font.bold = False

    # Save the presentation
    prs.save(output_pptx_path)
    return output_pptx_path
