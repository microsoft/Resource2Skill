import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "TOWARDS THE FUTURE",
    body_text: str = "Global Market Analysis & Strategic Insights 2024",
    bg_keyword: str = "cityscape,architecture",
    overlay_color_rgba: tuple = (23, 42, 83, 215),  # Corporate Navy with ~85% opacity
    text_color_rgb: tuple = (255, 255, 255)
) -> str:
    """
    Create a PPTX file reproducing the "Professional Geometric Overlay Title" effect.
    Uses PIL to create a perfectly transparent geometric mask (parallelogram).
    """
    
    # 1. Initialize Presentation (16:9 aspect ratio)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Convert inches to pixels for PIL (assuming 96 DPI for standard PPT processing)
    # 13.333 * 96 = ~1280, 7.5 * 96 = ~720
    slide_w_px, slide_h_px = 1280, 720

    # 2. Fetch Background Image (Fallback to solid color if offline)
    bg_image_stream = BytesIO()
    try:
        url = f"https://source.unsplash.com/1280x720/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            bg_image_stream.write(response.read())
    except Exception as e:
        print(f"Image download failed ({e}), generating fallback background.")
        fallback_img = Image.new('RGB', (slide_w_px, slide_h_px), color=(200, 200, 200))
        fallback_img.save(bg_image_stream, format='PNG')
    
    bg_image_stream.seek(0)
    
    # Add Background to Slide
    slide.shapes.add_picture(
        bg_image_stream, 
        0, 0, 
        width=prs.slide_width, 
        height=prs.slide_height
    )

    # 3. Create the Semi-Transparent Geometric Overlay using PIL
    # We draw a parallelogram that covers the left side and angles down to the right.
    mask_stream = BytesIO()
    
    # Create an empty transparent image
    overlay_img = Image.new('RGBA', (slide_w_px, slide_h_px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay_img)
    
    # Define polygon coordinates for the angled mask
    # Top-Left, Top-Right (past middle), Bottom-Right (angled back), Bottom-Left
    polygon_points = [
        (0, 0),
        (slide_w_px * 0.65, 0),          # Top edge extends to 65% width
        (slide_w_px * 0.45, slide_h_px), # Bottom edge pulls back to 45% width
        (0, slide_h_px)
    ]
    
    # Draw the polygon with the specified RGBA color
    draw.polygon(polygon_points, fill=overlay_color_rgba)
    
    # Save the overlay to stream
    overlay_img.save(mask_stream, format='PNG')
    mask_stream.seek(0)
    
    # Add the Overlay to Slide
    slide.shapes.add_picture(
        mask_stream, 
        0, 0, 
        width=prs.slide_width, 
        height=prs.slide_height
    )

    # 4. Add Typography (Title and Subtitle)
    # Position text safely within the bounds of the geometric mask
    
    # Title Box
    title_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(2.5), Inches(6.0), Inches(1.5)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial' # Standard professional sans-serif
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*text_color_rgb)
    p.alignment = PP_ALIGN.LEFT
    
    # Subtitle Box
    sub_box = slide.shapes.add_textbox(
        Inches(0.85), Inches(4.2), Inches(5.5), Inches(1.0)
    )
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = body_text
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(20)
    p_sub.font.bold = False
    
    # Slight opacity effect for subtitle (using a slightly darker/greyer version of text color)
    sub_color = tuple(max(0, c - 40) for c in text_color_rgb) if text_color_rgb == (255,255,255) else tuple(min(255, c + 40) for c in text_color_rgb)
    p_sub.font.color.rgb = RGBColor(*sub_color)
    p_sub.alignment = PP_ALIGN.LEFT

    # Save Presentation
    prs.save(output_pptx_path)
    print(f"Presentation saved successfully to: {output_pptx_path}")
    return output_pptx_path

# Example execution (uncomment to test):
# create_slide("corporate_keynote_title.pptx")
