import os
import urllib.request
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from _shell_helpers import add_infinite_rotation, add_pulse_loop

AMBIENT_CAPABLE = True

def create_slide(
    output_pptx_path: str,
    title_text: str = "LIQUID\nIMAGE\nMASK",
    body_text: str = "Insert some awesome\ntext right here. Just\nremember keep it\nshort and sweet.",
    bg_palette: str = "yosemite,mountain,nature",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Liquid Image Mask effect.
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 0: Background Image ===
    bg_img_path = "temp_bg.jpg"
    try:
        req = urllib.request.Request(
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1920&auto=format&fit=crop", 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            with open(bg_img_path, 'wb') as f:
                f.write(response.read())
    except Exception:
        # Fallback gradient if network fails
        bg = Image.new('RGB', (1920, 1080), (30, 40, 50))
        bg.save(bg_img_path)

    # Insert background to cover full slide
    slide.shapes.add_picture(bg_img_path, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    # === Layer 1: Massive Organic Mask ===
    mask_path = "temp_mask.png"
    mask_w, mask_h = 3000, 3000  # Creates a 30x30 inch massive canvas
    
    # 1. Create a grayscale mask (White = solid, Black = transparent hole)
    hole = Image.new('L', (mask_w, mask_h), 255)
    draw = ImageDraw.Draw(hole)
    
    # Draw overlapping geometric shapes to form a raw blob in the dead center
    cx, cy = mask_w // 2, mask_h // 2
    draw.ellipse([cx - 300, cy - 400, cx + 300, cy + 400], fill=0) # Main body
    draw.ellipse([cx - 150, cy - 150, cx + 450, cy + 250], fill=0) # Bottom right protrusion
    draw.ellipse([cx - 400, cy - 300, cx + 100, cy + 100], fill=0) # Top left protrusion
    draw.ellipse([cx - 200, cy + 100, cx + 200, cy + 500], fill=0) # Bottom left tail
    
    # 2. Metaball effect: Heavy Gaussian Blur + Hard Threshold
    hole = hole.filter(ImageFilter.GaussianBlur(120))
    hole = hole.point(lambda p: 255 if p > 127 else 0)
    
    # 3. Create the final white image and inject the blob as the alpha channel
    final_mask = Image.new('RGBA', (mask_w, mask_h), (255, 255, 255, 255))
    final_mask.putalpha(hole)
    final_mask.save(mask_path)

    # Calculate positioning: We want the hole (center of the massive mask) at specific slide coordinates
    hole_target_x = Inches(4.5)
    hole_target_y = Inches(3.75) # Vertically centered
    
    mask_size = Inches(30)
    left_pos = hole_target_x - (mask_size / 2)
    top_pos = hole_target_y - (mask_size / 2)

    mask_shape = slide.shapes.add_picture(mask_path, left_pos, top_pos, width=mask_size, height=mask_size)

    # Apply Ambient Animation
    # Rotating the massive shape spins the hole perfectly in place without revealing borders
    add_infinite_rotation(slide, mask_shape, duration_ms=25000, direction="cw")
    # Subtle scaling creates the liquid "breathing" effect
    add_pulse_loop(slide, mask_shape, duration_ms=4000, scale_pct=108)

    # === Layer 2: Typography ===
    # Main Headline
    tx_box = slide.shapes.add_textbox(Inches(7.5), Inches(2.2), Inches(4.5), Inches(2.5))
    tf = tx_box.text_frame
    tf.text = title_text
    for idx, p in enumerate(tf.paragraphs):
        p.alignment = PP_ALIGN.RIGHT
        p.font.size = Pt(48)
        p.font.name = "Arial Black" # Use heavy bold font
        p.font.bold = True
        p.font.color.rgb = RGBColor(20, 20, 20)
        # Tight line spacing
        p.line_spacing = Pt(50)

    # Body Description
    body_box = slide.shapes.add_textbox(Inches(9.0), Inches(5.0), Inches(3.0), Inches(1.5))
    bf = body_box.text_frame
    bf.word_wrap = True
    bf.text = body_text
    for p in bf.paragraphs:
        p.alignment = PP_ALIGN.RIGHT
        p.font.size = Pt(12)
        p.font.name = "Arial"
        p.font.color.rgb = RGBColor(120, 120, 120)

    # Cleanup temporary files if needed
    prs.save(output_pptx_path)
    
    try:
        os.remove(bg_img_path)
        os.remove(mask_path)
    except OSError:
        pass
        
    return output_pptx_path
