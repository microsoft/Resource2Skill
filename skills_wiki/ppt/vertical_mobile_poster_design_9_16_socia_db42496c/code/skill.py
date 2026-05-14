import os
import urllib.request
from io import BytesIO
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    title_text: str = "The Beauty of\nNature",
    subtitle_text: str = "Autumn Harvest • Winter Storage\nWarm Forward Journey",
    cta_text: str = "Scan to learn more PPT skills",
    bg_keyword: str = "dark food ingredients",
    frame_color: tuple = (210, 166, 115),  # Warm Gold
    banner_color: tuple = (120, 30, 30),   # Deep Crimson
    **kwargs,
) -> str:
    """
    Creates a vertical (9:16) mobile poster in PowerPoint reproducing the layered 
    geometric design from the tutorial.
    """
    
    # --- PPTX Setup for 9:16 Portrait ---
    prs = Presentation()
    # Standard 16:9 is 13.333 x 7.5. We swap them for 9:16.
    slide_width_in = 7.5
    slide_height_in = 13.333
    prs.slide_width = Inches(slide_width_in)
    prs.slide_height = Inches(slide_height_in)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # --- Layer 1: Background Image Prep (via PIL) ---
    bg_image_path = "temp_poster_bg.jpg"
    target_dpi = 150
    px_width = int(slide_width_in * target_dpi)
    px_height = int(slide_height_in * target_dpi)
    
    try:
        # Try to download a thematic high-res image
        url = f"https://source.unsplash.com/random/{px_width}x{px_height}/?{bg_keyword.replace(' ', ',')}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img_data = response.read()
        bg_img = Image.open(BytesIO(img_data)).convert("RGB")
        # Resize/Crop to exact 9:16 ratio to prevent PPT distortion
        bg_img = bg_img.resize((px_width, px_height), Image.Resampling.LANCZOS)
    except Exception as e:
        # Fallback: Create a dark moody gradient if download fails
        print(f"Image download failed ({e}), generating fallback background...")
        bg_img = Image.new('RGB', (px_width, px_height))
        draw = ImageDraw.Draw(bg_img)
        for y in range(px_height):
            # Gradient from black to dark charcoal
            r = int(20 * (y / px_height))
            g = int(25 * (y / px_height))
            b = int(30 * (y / px_height))
            draw.line([(0, y), (px_width, y)], fill=(r, g, b))
            
    bg_img.save(bg_image_path)
    slide.shapes.add_picture(bg_image_path, 0, 0, width=Inches(slide_width_in), height=Inches(slide_height_in))

    # --- Layer 2: Hollow Inner Frame ---
    margin = Inches(0.6)
    frame_w = prs.slide_width - (margin * 2)
    frame_h = prs.slide_height - (margin * 2)
    
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, margin, margin, frame_w, frame_h)
    frame.fill.background() # Makes the fill transparent
    frame.line.color.rgb = RGBColor(*frame_color)
    frame.line.width = Pt(4)

    # --- Layer 3: Solid Banner for Subtitle ---
    banner_w = Inches(4.5)
    banner_h = Inches(1.2)
    banner_left = (prs.slide_width - banner_w) / 2
    banner_top = Inches(7.5) # Placed below vertical center
    
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, banner_left, banner_top, banner_w, banner_h)
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(*banner_color)
    banner.line.fill.background() # No border
    
    # --- Layer 4: Typography ---
    
    # Main Display Title
    title_w = Inches(6)
    title_h = Inches(3)
    title_left = (prs.slide_width - title_w) / 2
    title_top = Inches(3.5)
    
    title_box = slide.shapes.add_textbox(title_left, title_top, title_w, title_h)
    tf = title_box.text_frame
    tf.text = title_text
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    # If there's a line break, align second line too
    for p in tf.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(65)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.name = "Georgia" # Fallback elegant font

    # Subtitle inside the Banner
    sub_box = slide.shapes.add_textbox(banner_left, banner_top + Inches(0.15), banner_w, banner_h)
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.size = Pt(22)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(255, 255, 255)
    p_sub.font.name = "Arial"

    # --- Layer 5: Mock QR Code & CTA ---
    # Generate Mock QR Code using PIL
    qr_size = 200
    qr_img = Image.new('RGB', (qr_size, qr_size), 'white')
    q_draw = ImageDraw.Draw(qr_img)
    # Draw simple QR pattern (squares)
    q_draw.rectangle([10, 10, 60, 60], fill="black")
    q_draw.rectangle([20, 20, 50, 50], fill="white")
    q_draw.rectangle([140, 10, 190, 60], fill="black")
    q_draw.rectangle([150, 20, 180, 50], fill="white")
    q_draw.rectangle([10, 140, 60, 190], fill="black")
    q_draw.rectangle([20, 150, 50, 180], fill="white")
    for i in range(20):
        import random
        x = random.randint(70, 130)
        y = random.randint(70, 130)
        q_draw.rectangle([x, y, x+10, y+10], fill="black")
    
    qr_path = "temp_mock_qr.png"
    qr_img.save(qr_path)
    
    # Insert QR
    qr_w = Inches(1.5)
    qr_left = (prs.slide_width - qr_w) / 2
    qr_top = Inches(9.5)
    slide.shapes.add_picture(qr_path, qr_left, qr_top, width=qr_w, height=qr_w)

    # CTA Text below QR
    cta_w = Inches(5)
    cta_h = Inches(0.5)
    cta_left = (prs.slide_width - cta_w) / 2
    cta_top = qr_top + qr_w + Inches(0.2)
    
    cta_box = slide.shapes.add_textbox(cta_left, cta_top, cta_w, cta_h)
    tf_cta = cta_box.text_frame
    p_cta = tf_cta.paragraphs[0]
    p_cta.text = cta_text
    p_cta.alignment = PP_ALIGN.CENTER
    p_cta.font.size = Pt(16)
    p_cta.font.color.rgb = RGBColor(255, 255, 255)
    p_cta.font.name = "Arial"

    # --- Save & Cleanup ---
    prs.save(output_pptx_path)
    
    if os.path.exists(bg_image_path):
        os.remove(bg_image_path)
    if os.path.exists(qr_path):
        os.remove(qr_path)
        
    return output_pptx_path
