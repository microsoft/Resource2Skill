import os
import random
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "Opinionated.\nDistinct.",
    subtitle_text: str = "A visual identity built for clarity, trust, and the long arc of consequential work. Every color, every letterform — chosen with intention.",
    eyebrow_text: str = "01 — BRAND GUIDELINES",
    bg_color: tuple = (20, 20, 19),         # Deep Charcoal
    text_color: tuple = (250, 249, 245),    # Off-White
    accent_colors: list = [
        (217, 119, 87),   # Terra Cotta
        (106, 155, 204),  # Muted Teal
        (120, 140, 93),   # Sage Green
        (210, 180, 140)   # Sand/Tan
    ],
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Opinionated Brand Aesthetics" 
    dark-mode design style with subtle noise texture.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # ==========================================
    # Layer 1: Generate & Apply Noise Background
    # ==========================================
    bg_img_path = "temp_bg_noise.png"
    
    # Create a base image with the background color
    width, height = 1920, 1080
    img = Image.new('RGBA', (width, height), bg_color + (255,))
    
    # Add subtle programmatic noise (film grain effect) to avoid "AI slop" flatness
    pixels = img.load()
    for x in range(0, width, 2):  # Step by 2 for performance, creating a coarser grain
        for y in range(0, height, 2):
            if random.random() > 0.7:
                # Add a very faint white speck
                pixels[x, y] = (255, 255, 255, int(random.randint(5, 12)))
            elif random.random() < 0.1:
                # Add a very faint dark speck
                pixels[x, y] = (0, 0, 0, int(random.randint(5, 15)))
                
    img.save(bg_img_path)
    
    # Add background image to slide
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # ==========================================
    # Layer 2: Typographic Hierarchy
    # ==========================================
    
    # Eyebrow (Small, tracked out, accent color)
    tx_box_eye = slide.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(5.0), Inches(0.5))
    tf_eye = tx_box_eye.text_frame
    p_eye = tf_eye.paragraphs[0]
    p_eye.text = eyebrow_text
    p_eye.font.size = Pt(11)
    p_eye.font.name = "Arial" # Fallback geometric sans
    p_eye.font.bold = True
    p_eye.font.color.rgb = RGBColor(*accent_colors[0]) # Use first accent

    # Massive Display Title
    tx_box_title = slide.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(6.0), Inches(2.5))
    tf_title = tx_box_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(64)
    p_title.font.name = "Georgia" # Fallback elegant serif (like Lora)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(*text_color)
    p_title.line_spacing = 1.0

    # Subtitle / Philosophy statement
    tx_box_sub = slide.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.0), Inches(2.0))
    tf_sub = tx_box_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(14)
    p_sub.font.name = "Arial" 
    p_sub.font.color.rgb = RGBColor(*text_color)
    p_sub.line_spacing = 1.4

    # ==========================================
    # Layer 3: Visual Accent / Palette Showcase
    # ==========================================
    # We will create an architectural layout of vertical color bars on the right side
    
    num_colors = len(accent_colors)
    bar_width = Inches(1.2)
    start_x = Inches(7.5)
    start_y = Inches(1.5)
    
    for i, color_rgb in enumerate(accent_colors):
        # Create a vertical bar for each color
        x_pos = start_x + (i * (bar_width + Inches(0.2)))
        
        # Varying heights for an asymmetrical, dynamic look
        bar_height = Inches(4.5) if i % 2 == 0 else Inches(3.5)
        y_offset = start_y if i % 2 == 0 else start_y + Inches(1.0)
        
        shape = slide.shapes.add_shape(
            1, # msoShapeRectangle
            x_pos, y_offset, bar_width, bar_height
        )
        
        # Remove outline and apply precise RGB fill
        shape.line.fill.background()
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color_rgb)
        
        # Add tiny hex code label at the bottom of each bar
        tx_box_hex = slide.shapes.add_textbox(x_pos, start_y + Inches(4.6), bar_width, Inches(0.4))
        tf_hex = tx_box_hex.text_frame
        p_hex = tf_hex.paragraphs[0]
        p_hex.text = f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}".upper()
        p_hex.alignment = PP_ALIGN.CENTER
        p_hex.font.size = Pt(10)
        p_hex.font.name = "Courier New"
        p_hex.font.color.rgb = RGBColor(*text_color)

    # Save and clean up
    prs.save(output_pptx_path)
    
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path

# Example execution:
# create_slide("brand_aesthetics.pptx")
