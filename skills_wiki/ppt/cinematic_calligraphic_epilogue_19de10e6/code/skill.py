import os
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

def create_slide(
    output_pptx_path: str,
    line1_text: str = "道阻且长",
    line2_text: str = "行则将至",
    stamp_text: str = "共勉",
    bg_theme: str = "landscape,road",
    **kwargs,
) -> str:
    """
    Creates a Cinematic Calligraphic Epilogue slide.
    Features staggered typography, a red accent stamp, and a cinematic background with a contrast overlay.
    """
    prs = Presentation()
    # Set 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # === Layer 1: Cinematic Background ===
    bg_image_path = "temp_bg.jpg"
    try:
        # Fetch a beautiful landscape image from reliable source
        url = f"https://picsum.photos/seed/{bg_theme}/1920/1080"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(bg_image_path, 'wb') as f:
                f.write(response.read())
    except Exception as e:
        # Fallback: Create a gradient dark blue background using PIL if network fails
        print(f"Network error, using fallback background. Error: {e}")
        img = Image.new('RGB', (1920, 1080), color=(13, 27, 42))
        img.save(bg_image_path)

    # Add background image to slide
    slide.shapes.add_picture(bg_image_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))

    # === Layer 2: Contrast Overlay (PIL) ===
    # Create a semi-transparent black overlay to ensure the white calligraphy pops
    overlay_path = "temp_overlay.png"
    # Create an RGBA image
    overlay = Image.new('RGBA', (1920, 1080), (0, 0, 0, 100)) # Black with ~40% opacity
    overlay.save(overlay_path)
    
    # Add overlay to slide
    slide.shapes.add_picture(overlay_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))

    # === Layer 3: Staggered Typography ===
    
    # Try to use a Calligraphy font, fallback to standard serif
    font_name = "STXingkai"  # Standard Chinese calligraphy font, replace with Brush Script MT for English
    
    # Line 1: Top Left offset
    left_1 = Inches(3.0)
    top_1 = Inches(2.2)
    width_1 = Inches(5.0)
    height_1 = Inches(1.5)
    
    txBox1 = slide.shapes.add_textbox(left_1, top_1, width_1, height_1)
    tf1 = txBox1.text_frame
    tf1.word_wrap = False
    p1 = tf1.paragraphs[0]
    p1.text = line1_text
    p1.font.name = font_name
    p1.font.size = Pt(88)
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.font.bold = True
    
    # Line 2: Bottom Right offset (Staggered Effect)
    left_2 = Inches(5.0) # Pushed to the right
    top_2 = Inches(3.8)  # Pushed down
    width_2 = Inches(5.0)
    height_2 = Inches(1.5)
    
    txBox2 = slide.shapes.add_textbox(left_2, top_2, width_2, height_2)
    tf2 = txBox2.text_frame
    tf2.word_wrap = False
    p2 = tf2.paragraphs[0]
    p2.text = line2_text
    p2.font.name = font_name
    p2.font.size = Pt(88)
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.font.bold = True

    # === Layer 4: Red Accent Stamp ===
    # Positioned relative to Line 1
    stamp_left = left_1 + Inches(3.8) # Adjust based on text length
    stamp_top = top_1 + Inches(0.2)
    stamp_size = Inches(0.4)
    
    # Add rounded rectangle
    stamp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        stamp_left, stamp_top, stamp_size, stamp_size
    )
    # Style the stamp (Red fill, no border)
    stamp.fill.solid()
    stamp.fill.fore_color.rgb = RGBColor(192, 0, 0)
    stamp.line.fill.background() # No line
    
    # Add text to stamp
    stamp_tf = stamp.text_frame
    stamp_tf.word_wrap = True
    stamp_p = stamp_tf.paragraphs[0]
    stamp_p.alignment = PP_ALIGN.CENTER
    stamp_p.text = stamp_text
    stamp_p.font.name = "SimHei" # Clean sans-serif for the stamp
    stamp_p.font.size = Pt(12)
    stamp_p.font.color.rgb = RGBColor(255, 255, 255)
    stamp_p.font.bold = True

    # Save presentation
    prs.save(output_pptx_path)
    
    # Cleanup temporary files
    if os.path.exists(bg_image_path):
        os.remove(bg_image_path)
    if os.path.exists(overlay_path):
        os.remove(overlay_path)
        
    return output_pptx_path

# Example usage:
# create_slide("staggered_epilogue.pptx", line1_text="道阻且长", line2_text="行则将至")
