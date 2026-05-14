import os
import urllib.request
from io import BytesIO
import random
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageColor
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def generate_fallback_background(width, height):
    """Generates an abstract, saturated 'tropical foliage' style background natively in PIL."""
    base = Image.new("RGB", (width, height), (6, 28, 15))
    draw = ImageDraw.Draw(base)
    
    # Draw overlapping circles to simulate deep leaves/bokeh
    for _ in range(30):
        r = random.randint(100, 500)
        x = random.randint(-r, width)
        y = random.randint(-r, height)
        # Vibrant green palette
        color = random.choice([
            (11, 74, 39), (28, 117, 61), (50, 180, 80), (15, 45, 25), (60, 200, 110)
        ])
        draw.ellipse((x, y, x+r*2, y+r*2), fill=color)
        
    # Apply blur to smooth it into a nice abstract texture
    return base.filter(ImageFilter.GaussianBlur(radius=60))

def create_slide(
    output_pptx_path: str,
    title_text: str = "THE ARCHITECTURE\nOF RENEWAL",
    body_text: str = "Redesigning our world to thrive within planetary boundaries.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Glassmorphism Reveal Panel effect.
    """
    
    # 1. Setup Presentation Dimensions (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.33333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Canvas dimensions in pixels (for PIL processing)
    canvas_w, canvas_h = 1920, 1080
    
    # 2. Acquire or Generate Background Image
    bg_img = None
    try:
        # Try to fetch a high-res tropical leaf image
        url = "https://images.unsplash.com/photo-1599598425947-33002629b52a?q=80&w=1920&auto=format&fit=crop"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            bg_img = Image.open(BytesIO(response.read())).convert("RGB")
            # Resize and crop to perfectly fit 1920x1080
            bg_aspect = bg_img.width / bg_img.height
            target_aspect = canvas_w / canvas_h
            if bg_aspect > target_aspect:
                new_w = int(bg_img.height * target_aspect)
                offset = (bg_img.width - new_w) // 2
                bg_img = bg_img.crop((offset, 0, offset + new_w, bg_img.height))
            else:
                new_h = int(bg_img.width / target_aspect)
                offset = (bg_img.height - new_h) // 2
                bg_img = bg_img.crop((0, offset, bg_img.width, offset + new_h))
            bg_img = bg_img.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Failed to download image ({e}), using generative fallback.")
        bg_img = generate_fallback_background(canvas_w, canvas_h)

    # Enhance background saturation (as in tutorial)
    enhancer = ImageEnhance.Color(bg_img)
    bg_img = enhancer.enhance(1.8)
    
    # Save the background for PPTX
    bg_path = "temp_bg.png"
    bg_img.save(bg_path)
    
    # 3. Create the Glassmorphism Panel
    # Panel occupies center 55% of width, 60% of height
    panel_w = int(canvas_w * 0.55)
    panel_h = int(canvas_h * 0.60)
    panel_x = (canvas_w - panel_w) // 2
    panel_y = (canvas_h - panel_h) // 2
    
    # Crop the exact region from the background
    glass = bg_img.crop((panel_x, panel_y, panel_x + panel_w, panel_y + panel_h))
    
    # Apply intense Gaussian blur and tweak brightness/saturation
    glass = glass.filter(ImageFilter.GaussianBlur(radius=45))
    glass = ImageEnhance.Color(glass).enhance(1.5)
    glass = ImageEnhance.Brightness(glass).enhance(0.9) # Slightly darker for text contrast
    
    # Create an alpha mask for rounded corners
    corner_radius = 60
    mask = Image.new("L", (panel_w, panel_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, panel_w, panel_h), radius=corner_radius, fill=255)
    glass.putalpha(mask)
    
    # 4. Composite Glass Panel with Drop Shadow
    shadow_padding = 150 # Large padding for soft shadow
    composite_w = panel_w + (shadow_padding * 2)
    composite_h = panel_h + (shadow_padding * 2)
    
    composite_img = Image.new("RGBA", (composite_w, composite_h), (0, 0, 0, 0))
    shadow_img = Image.new("RGBA", (composite_w, composite_h), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    
    # Draw shadow geometry (slightly offset down)
    y_offset = 20
    shadow_draw.rounded_rectangle(
        (shadow_padding, shadow_padding + y_offset, shadow_padding + panel_w, shadow_padding + panel_h + y_offset),
        radius=corner_radius, 
        fill=(0, 0, 0, 160) # Dark shadow
    )
    # Blur the shadow
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(30))
    
    # Merge shadow and glass
    composite_img.alpha_composite(shadow_img)
    composite_img.paste(glass, (shadow_padding, shadow_padding), glass)
    
    # Save composite panel
    panel_path = "temp_glass_panel.png"
    composite_img.save(panel_path)
    
    # 5. Insert Elements into PPTX
    # A. Add Background
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    
    # B. Add Glass Panel
    # Calculate exact position to align perfectly with the background crop
    # Conversion: Slide Width (Inches) / Canvas Width (Pixels)
    scale = prs.slide_width / canvas_w
    pic_left = (panel_x - shadow_padding) * scale
    pic_top = (panel_y - shadow_padding) * scale
    pic_width = composite_w * scale
    pic_height = composite_h * scale
    
    slide.shapes.add_picture(panel_path, pic_left, pic_top, pic_width, pic_height)
    
    # 6. Add Typography
    # Text box matching the panel bounds
    text_left = panel_x * scale
    text_top = (panel_y * scale) + Inches(0.8)
    text_width = panel_w * scale
    text_height = panel_h * scale
    
    txBox = slide.shapes.add_textbox(text_left, text_top, text_width, text_height)
    tf = txBox.text_frame
    tf.word_wrap = True
    
    # Main Title
    p_title = tf.paragraphs[0]
    p_title.text = title_text.upper()
    p_title.alignment = PP_ALIGN.CENTER
    p_title.font.name = "Arial Black" # Sturdy, modern font
    p_title.font.size = Pt(48)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    
    # Spacing
    p_space = tf.add_paragraph()
    p_space.font.size = Pt(20)
    
    # Body Text
    p_body = tf.add_paragraph()
    p_body.text = body_text
    p_body.alignment = PP_ALIGN.CENTER
    p_body.font.name = "Arial"
    p_body.font.size = Pt(20)
    p_body.font.color.rgb = RGBColor(230, 240, 235) # Slightly off-white for depth
    
    # Clean up temporary files
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(panel_path): os.remove(panel_path)

    prs.save(output_pptx_path)
    return output_pptx_path

# To test the function, uncomment the line below:
# create_slide("glassmorphism_reveal.pptx")
