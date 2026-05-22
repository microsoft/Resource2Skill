import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "POWERPOINT\nTEMPLATE",
    subtitle_text: str = "You Can Write Here Write\nSomething About",
    contact_info: str = "bigchin\nhibigchin@gmail.com\nt. 13612345678"
) -> str:
    """
    Creates a PPTX file reproducing the 'Vibrant Fluid Vector Abstract' aesthetic.
    Generates a custom PIL background of overlapping smooth curves and overlays crisp typography.
    """
    
    # --- 1. Setup Presentation ---
    prs = Presentation()
    # Set 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6] # Blank slide
    slide = prs.slides.add_slide(slide_layout)

    # --- 2. Color Palette ---
    COLOR_PURPLE = (74, 20, 140)     # Dark Royal Purple
    COLOR_YELLOW = (244, 208, 63)    # Vibrant Yellow
    COLOR_ORANGE = (255, 87, 34)     # Neon Orange
    COLOR_MAGENTA = (233, 30, 99)    # Bright Magenta
    COLOR_DEEP = (49, 10, 100)       # Shadow/Depth Purple

    # --- 3. Generate Fluid Vector Background using PIL ---
    img_width, img_height = 1920, 1080
    bg_img = Image.new('RGBA', (img_width, img_height), COLOR_PURPLE)
    draw = ImageDraw.Draw(bg_img, 'RGBA')

    # To simulate smooth sweeping vector waves, we draw massive off-screen ellipses.
    
    # Wave 1: Massive yellow block bottom left
    draw.ellipse([-600, 700, 900, 2200], fill=COLOR_YELLOW)
    
    # Wave 2: Deep purple sweeping shadow/mid-layer
    draw.ellipse([800, 450, 2500, 2150], fill=COLOR_DEEP)
    
    # Wave 3: Magenta sweeping accent
    draw.ellipse([950, 600, 2400, 2050], fill=COLOR_MAGENTA)
    
    # Wave 4: Orange wave cutting through
    draw.ellipse([1100, 550, 2700, 2150], fill=COLOR_ORANGE)
    
    # Wave 5: Front purple wave wrapping around the bottom right
    draw.ellipse([1300, 750, 2600, 2050], fill=COLOR_PURPLE)

    # Save the background
    bg_path = "temp_fluid_bg.png"
    bg_img.save(bg_path)

    # Add image to slide (filling the whole slide)
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- 4. Typography & Content Layout ---
    
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(8), Inches(2))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(60)
    p.font.name = "Arial Black" # Use a heavy sans-serif
    p.font.color.rgb = RGBColor(255, 255, 255) # White text for contrast against purple

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.85), Inches(2.6), Inches(5), Inches(1))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(20)
    p_sub.font.name = "Arial"
    p_sub.font.color.rgb = RGBColor(200, 200, 200) # Slightly dimmed white

    # Contact Info (Bottom Left, sitting over the Yellow curve)
    # Using dark purple text to contrast against the bright yellow
    contact_box = slide.shapes.add_textbox(Inches(0.85), Inches(5.0), Inches(4), Inches(1.5))
    tf_contact = contact_box.text_frame
    
    lines = contact_info.split('\n')
    for i, line in enumerate(lines):
        if i == 0:
            p_contact = tf_contact.paragraphs[0]
        else:
            p_contact = tf_contact.add_paragraph()
            
        p_contact.text = line
        p_contact.font.name = "Arial"
        p_contact.font.color.rgb = RGBColor(*COLOR_PURPLE) # Dark purple text
        
        # Make the first line (Name) bolder and slightly larger
        if i == 0:
            p_contact.font.bold = True
            p_contact.font.size = Pt(24)
        else:
            p_contact.font.bold = True
            p_contact.font.size = Pt(16)

    # --- 5. Cleanup and Save ---
    prs.save(output_pptx_path)
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path

# Example execution:
# create_slide("vibrant_fluid_abstract.pptx")
