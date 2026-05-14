import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "THANKS",
    subtitle_text: str = "欢迎指正 / Q & A",
    bg_theme: str = "skyscraper,business",
    overlay_color: tuple = (24, 86, 171, 160), # RGBA: Deep blue with 60% opacity
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Cinematic Color-Overlay Closure" effect.
    """
    # 1. Initialize Presentation (16:9 aspect ratio)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Canvas dimensions in pixels (assuming 144 dpi for high quality generation)
    # 13.333 * 144 = 1920, 7.5 * 144 = 1080
    WIDTH, HEIGHT = 1920, 1080

    # 2. Generate Background with PIL
    bg_img_path = "temp_bg_overlay.png"
    try:
        # Fetch thematic image
        # Using pollinations.ai for reliable AI-generated thematic images based on keywords
        url = f"https://image.pollinations.ai/prompt/{bg_theme}?width={WIDTH}&height={HEIGHT}&nologo=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        base_image = Image.open(BytesIO(response.content)).convert("RGBA")
        base_image = base_image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Image download failed: {e}. Falling back to solid gradient.")
        # Fallback: Create a subtle radial gradient base if network fails
        base_image = Image.new("RGBA", (WIDTH, HEIGHT), (200, 200, 200, 255))
        draw = ImageDraw.Draw(base_image)
        for i in range(HEIGHT):
            shade = int(255 - (i / HEIGHT) * 100)
            draw.line([(0, i), (WIDTH, i)], fill=(shade, shade, shade, 255))

    # Apply Color Overlay via Alpha Compositing
    overlay = Image.new("RGBA", base_image.size, overlay_color)
    final_bg = Image.alpha_composite(base_image, overlay)
    
    # Save temp background
    final_bg.save(bg_img_path, format="PNG")

    # 3. Add Background to Slide
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 4. Add Geometric Accent (Thin Circle)
    # Calculate circle size and position (Centered)
    circle_diameter = Inches(4.5)
    circle_left = (prs.slide_width - circle_diameter) / 2
    circle_top = (prs.slide_height - circle_diameter) / 2 - Inches(0.5) # Shifted slightly up

    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, circle_left, circle_top, circle_diameter, circle_diameter
    )
    circle.fill.background() # No fill (transparent)
    circle.line.color.rgb = RGBColor(255, 255, 255)
    circle.line.width = Pt(1.5)
    
    # Make the circle line slightly transparent using an xml workaround (optional, but nice)
    # However, keeping it solid white matches the minimalist aesthetic well.

    # 5. Add Main Title Typography
    title_box = slide.shapes.add_textbox(
        Inches(0), circle_top + Inches(1.5), prs.slide_width, Inches(1.5)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(88)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Add spacing between characters if it's english text (simulated with spaces for simplicity in standard PPTX)
    if title_text.isascii():
        p.text = " ".join(title_text)

    # 6. Add Subtitle Typography
    sub_box = slide.shapes.add_textbox(
        Inches(0), circle_top + circle_diameter + Inches(0.2), prs.slide_width, Inches(1)
    )
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Microsoft YaHei" # Good for Chinese and English
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(220, 220, 220) # Slightly dimmed white

    # 7. Save and Cleanup
    prs.save(output_pptx_path)
    
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path

# Example Usage:
# create_slide("cinematic_end_slide.pptx", title_text="THANKS", subtitle_text="感谢您的观看与指导", bg_theme="ocean,waves", overlay_color=(30, 144, 255, 170))
