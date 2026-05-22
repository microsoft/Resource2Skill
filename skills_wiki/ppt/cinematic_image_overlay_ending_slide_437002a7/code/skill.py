import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

def create_slide(
    output_pptx_path: str,
    main_text: str = "THANKS",
    sub_text: str = "感 谢 您 的 观 看",  # Spaces added to simulate character tracking
    meta_text: str = "汇报人：Bobbie | 202X年12月",
    bg_keyword: str = "city,night",  # Unsplash keyword for background
    overlay_opacity: float = 0.65,   # 0.0 to 1.0
) -> str:
    """
    Creates a cinematic closing slide with a photographic background, 
    a dark translucent overlay, and high-contrast centered typography.
    """
    prs = Presentation()
    # Use 16:9 widescreen aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # --- Layer 1: Background Image ---
    bg_img_path = "temp_bg.jpg"
    try:
        # Fetch a random high-quality image from Unsplash
        url = f"https://source.unsplash.com/1920x1080/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bg_img_path, 'wb') as out_file:
            out_file.write(response.read())
        # Insert background
        slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except Exception as e:
        print(f"Failed to download image, using solid fallback: {e}")
        # Fallback: Deep Navy Blue background
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = RGBColor(13, 17, 28)
        bg_shape.line.fill.background()

    # --- Layer 2: Semi-Transparent Dark Overlay (Using PIL) ---
    # We generate a 1x1 PNG with an alpha channel and stretch it
    overlay_img_path = "temp_overlay.png"
    alpha_value = int(255 * overlay_opacity)
    # Create a completely black image with calculated transparency
    overlay = Image.new('RGBA', (10, 10), (0, 0, 0, alpha_value))
    overlay.save(overlay_img_path)
    
    # Insert overlay to cover exactly the whole slide
    slide.shapes.add_picture(overlay_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Layer 3: Main Typography (Huge, Serif) ---
    tx_width = Inches(10)
    tx_height = Inches(2)
    tx_left = (prs.slide_width - tx_width) / 2
    tx_top = Inches(2.2)  # Positioned slightly above center
    
    tb_main = slide.shapes.add_textbox(tx_left, tx_top, tx_width, tx_height)
    tf_main = tb_main.text_frame
    tf_main.word_wrap = True
    p_main = tf_main.paragraphs[0]
    p_main.text = main_text
    p_main.alignment = PP_ALIGN.CENTER
    
    font_main = p_main.font
    font_main.name = "Georgia"  # Editorial serif font
    font_main.size = Pt(80)
    font_main.bold = True
    font_main.color.rgb = RGBColor(255, 255, 255)  # Pure White

    # --- Layer 4: Minimalist Divider Line ---
    line_width = Inches(2.5)
    line_left = (prs.slide_width - line_width) / 2
    line_top = tx_top + Inches(1.8)
    
    divider = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, line_left, line_top, line_width, Pt(1)
    )
    divider.fill.solid()
    divider.fill.fore_color.rgb = RGBColor(255, 255, 255)
    divider.line.fill.background() # No border

    # --- Layer 5: Subtitle Typography ---
    sub_top = line_top + Inches(0.2)
    tb_sub = slide.shapes.add_textbox(tx_left, sub_top, tx_width, Inches(1))
    p_sub = tb_sub.text_frame.paragraphs[0]
    p_sub.text = sub_text
    p_sub.alignment = PP_ALIGN.CENTER
    
    font_sub = p_sub.font
    font_sub.name = "Arial"
    font_sub.size = Pt(20)
    font_sub.color.rgb = RGBColor(220, 220, 220)  # Off-white

    # --- Layer 6: Metadata Typography ---
    meta_top = sub_top + Inches(1.2)
    tb_meta = slide.shapes.add_textbox(tx_left, meta_top, tx_width, Inches(1))
    p_meta = tb_meta.text_frame.paragraphs[0]
    p_meta.text = meta_text
    p_meta.alignment = PP_ALIGN.CENTER
    
    font_meta = p_meta.font
    font_meta.name = "Arial"
    font_meta.size = Pt(14)
    font_meta.color.rgb = RGBColor(180, 180, 180)  # Lighter Gray

    # Clean up temporary files
    try:
        if os.path.exists(bg_img_path): os.remove(bg_img_path)
        if os.path.exists(overlay_img_path): os.remove(overlay_img_path)
    except Exception:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("cinematic_ending.pptx", main_text="THANKS", bg_keyword="architecture,modern")
# create_slide("slogan_ending.pptx", main_text="MAKE IT HAPPEN", sub_text="2024 Strategic Vision", bg_keyword="abstract,dark")
