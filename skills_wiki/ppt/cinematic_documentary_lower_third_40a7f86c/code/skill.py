import os
import urllib.request
from io import BytesIO
from PIL import Image, ImageEnhance
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    title_text: str = "“THE SUPREME ART OF WAR IS TO SUBDUE THE ENEMY WITHOUT FIGHTING.”",
    subtitle_text: str = "Applying historical strategy to modern business negotiations",
    bg_keyword: str = "historical,war",
    accent_color: tuple = (0, 194, 168),  # Video's signature Cyan/Teal
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Cinematic Documentary Lower-Third' visual style.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # ==========================================
    # Layer 1: Background Image Generation (PIL)
    # ==========================================
    bg_path = "temp_bg_grayscale.jpg"
    
    try:
        # Fetch an image
        url = f"https://source.unsplash.com/featured/1920x1080/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img = Image.open(BytesIO(response.read()))
    except Exception:
        # Fallback if download fails
        img = Image.new('RGB', (1920, 1080), color=(40, 40, 40))

    # Convert to Grayscale
    img = img.convert('L')
    
    # Increase contrast slightly for dramatic historical effect
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)

    # Add a dark overlay to ensure text legibility
    img = img.convert('RGBA')
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 140)) # 55% opacity black
    final_bg = Image.alpha_composite(img, overlay)
    
    # Save temp background
    final_bg.convert('RGB').save(bg_path, quality=95)

    # Insert background
    slide.shapes.add_picture(bg_path, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    # ==========================================
    # Layer 2: The Cinematic Text (Top/Center)
    # ==========================================
    tb_title = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(3.0))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    p_title.font.name = "Arial"
    p_title.alignment = PP_ALIGN.LEFT

    # ==========================================
    # Layer 3: Vibrant Lower-Third UI Ribbon
    # ==========================================
    ribbon_height = 1.0
    ribbon_top = 5.8
    ribbon_width = 11.5 # 86% of the screen width for the asymmetrical tab look
    
    # Main Ribbon Rectangle
    ribbon = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(ribbon_top), 
        Inches(ribbon_width), Inches(ribbon_height)
    )
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = RGBColor(*accent_color)
    ribbon.line.fill.background() # No outline

    # Decorative Top Line (Thin white line just above the ribbon to give it a UI feel)
    top_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(ribbon_top - 0.1),
        Inches(ribbon_width + 0.2), Inches(0.05)
    )
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = RGBColor(255, 255, 255)
    top_line.line.fill.background()

    # Logo/Icon Anchor (Circular element on the left)
    icon_size = 0.6
    icon = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(0.5), Inches(ribbon_top + (ribbon_height - icon_size)/2),
        Inches(icon_size), Inches(icon_size)
    )
    icon.fill.solid()
    icon.fill.fore_color.rgb = RGBColor(255, 255, 255)
    icon.line.fill.background()
    
    # Inner dark triangle (Play button motif common in these videos)
    triangle = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE,
        Inches(0.72), Inches(ribbon_top + 0.35),
        Inches(0.2), Inches(0.3)
    )
    triangle.rotation = 90
    triangle.fill.solid()
    triangle.fill.fore_color.rgb = RGBColor(*accent_color)
    triangle.line.fill.background()

    # ==========================================
    # Layer 4: Ribbon Subtitle Text
    # ==========================================
    tb_sub = slide.shapes.add_textbox(
        Inches(1.5), Inches(ribbon_top + 0.1), 
        Inches(ribbon_width - 1.5), Inches(0.8)
    )
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(24)
    p_sub.font.bold = True
    # Dark text looks better on bright Cyan/Teal
    p_sub.font.color.rgb = RGBColor(20, 20, 20) 
    p_sub.font.name = "Arial"
    p_sub.alignment = PP_ALIGN.LEFT
    
    # Cleanup and Save
    prs.save(output_pptx_path)
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
