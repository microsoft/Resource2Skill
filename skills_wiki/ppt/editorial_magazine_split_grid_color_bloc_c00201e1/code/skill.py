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
    title_text: str = "INNOVATIVE\nDESIGN",
    subtitle_text: str = "MAGAZINE TEMPLATE",
    body_text: str = "Contrary to popular belief, this layout is not simply random shapes. It has roots in classical editorial print design, making it highly effective for visual storytelling.",
    bg_theme: str = "architecture", 
    accent_color: tuple = (112, 48, 160),  # Default: The Deep Violet from the video
) -> str:
    """
    Creates a PPTX file reproducing the 'Editorial Magazine Split-Grid' effect.
    """
    # 1. Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Colors
    bg_color = RGBColor(245, 245, 245) # Light gray background
    text_dark = RGBColor(20, 20, 20)
    text_light = RGBColor(100, 100, 100)
    accent_rgb = RGBColor(*accent_color)

    # 2. Add Background Base
    bg_rect = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_rect.fill.solid()
    bg_rect.fill.fore_color.rgb = bg_color
    bg_rect.line.fill.background() # No outline

    # 3. Handle Image Fetching & Pre-cropping via PIL
    # We want the image to occupy exactly the right 55% of the screen
    img_width_in = 13.333 * 0.55
    img_height_in = 7.5
    img_left_in = 13.333 - img_width_in
    
    # Target pixel dimensions (assuming 300 DPI for good quality)
    target_px_w = int(img_width_in * 300)
    target_px_h = int(img_height_in * 300)
    
    temp_img_path = "temp_editorial_img.jpg"
    
    try:
        # Fetch image
        url = f"https://source.unsplash.com/random/{target_px_w}x{target_px_h}/?{bg_theme}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read())).convert("RGB")
            
            # Crop to exact aspect ratio to prevent PPTX distortion
            img_ratio = img.width / img.height
            target_ratio = target_px_w / target_px_h
            
            if img_ratio > target_ratio:
                # Image is wider, crop sides
                new_w = int(target_ratio * img.height)
                left = (img.width - new_w) / 2
                img = img.crop((left, 0, left + new_w, img.height))
            elif img_ratio < target_ratio:
                # Image is taller, crop top/bottom
                new_h = int(img.width / target_ratio)
                top = (img.height - new_h) / 2
                img = img.crop((0, top, img.width, top + new_h))
                
            img = img.resize((target_px_w, target_px_h), Image.Resampling.LANCZOS)
            img.save(temp_img_path, format="JPEG", quality=90)
            
    except Exception as e:
        # Fallback: Create a procedural gradient/color block if offline
        img = Image.new("RGB", (target_px_w, target_px_h), color=(50, 50, 50))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, target_px_h*0.8, target_px_w, target_px_h], fill=(30, 30, 30))
        img.save(temp_img_path, format="JPEG")

    # Insert the perfectly cropped image
    slide.shapes.add_picture(
        temp_img_path, 
        Inches(img_left_in), 0, 
        Inches(img_width_in), Inches(img_height_in)
    )

    # 4. Add the Bridging Geometric Accent Block
    # This block spans from the text area into the image area, creating tension
    block_width = Inches(3.5)
    block_height = Inches(0.6)
    block_left = Inches(img_left_in - 1.5) # Overlaps the boundary
    block_top = Inches(4.5)
    
    accent_rect = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, block_left, block_top, block_width, block_height
    )
    accent_rect.fill.solid()
    accent_rect.fill.fore_color.rgb = accent_rgb
    accent_rect.line.fill.background()

    # 5. Add Typography Hierarchy
    
    # Subtitle (Small, Accent Color, Above Title)
    tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.5), Inches(0.5))
    p_sub = tx_sub.text_frame.add_paragraph()
    p_sub.text = subtitle_text.upper()
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = accent_rgb
    p_sub.font.name = "Arial"

    # Main Title (Massive, Bold)
    tx_title = slide.shapes.add_textbox(Inches(0.7), Inches(1.6), Inches(5.0), Inches(2.5))
    tx_title.text_frame.word_wrap = True
    p_title = tx_title.text_frame.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(54)
    p_title.font.bold = True
    p_title.font.color.rgb = text_dark
    p_title.font.name = "Arial Black" # Use a heavy font
    p_title.line_spacing = 0.9 # Tight kerning/leading

    # Body Text
    tx_body = slide.shapes.add_textbox(Inches(0.8), Inches(5.3), Inches(4.0), Inches(1.5))
    tx_body.text_frame.word_wrap = True
    p_body = tx_body.text_frame.add_paragraph()
    p_body.text = body_text
    p_body.font.size = Pt(11)
    p_body.font.color.rgb = text_light
    p_body.font.name = "Arial"
    p_body.line_spacing = 1.2
    
    # Decorative line under body text
    line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, Inches(0.8), Inches(6.8), Inches(1.8), Inches(6.8)
    )
    line.line.color.rgb = text_light
    line.line.width = Pt(1.5)

    # Clean up and save
    prs.save(output_pptx_path)
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)
        
    return output_pptx_path

# Example Usage:
# create_slide("editorial_magazine_layout.pptx", accent_color=(226, 0, 116), bg_theme="fashion")
