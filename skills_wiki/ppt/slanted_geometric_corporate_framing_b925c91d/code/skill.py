import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "Sales Performance\nReview",
    body_text: str = "Q4 Financial Overview & Strategy",
    bg_theme: str = "office,business",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Slanted Geometric Corporate Framing' effect.
    """
    # Color Palette extracted from the video
    NAVY = RGBColor(26, 54, 93)
    RED = RGBColor(155, 44, 44)
    GOLD = RGBColor(214, 158, 46)
    WHITE = RGBColor(255, 255, 255)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    width = prs.slide_width
    height = prs.slide_height

    # === Layer 1: Background Image ===
    # Download an image from Unsplash to match the corporate background seen at 0:00
    bg_img_path = "temp_bg.jpg"
    try:
        url = f"https://source.unsplash.com/random/1920x1080/?{bg_theme}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(bg_img_path, 'wb') as f:
                f.write(response.read())
        # Insert image covering full slide
        slide.shapes.add_picture(bg_img_path, 0, 0, width, height)
    except Exception as e:
        print(f"Image download failed, using fallback background. Error: {e}")
        # Fallback: Create a solid grey background using PIL
        img = Image.new('RGB', (1920, 1080), color=(237, 242, 247))
        img.save(bg_img_path)
        slide.shapes.add_picture(bg_img_path, 0, 0, width, height)

    # === Layer 2: Main Slanted Geometric Polygon (Bottom Left) ===
    # Creates a polygon: starts bottom-left, goes up, slants down to bottom-right
    
    # Points for the main Navy shape
    pt1_x, pt1_y = 0, height                     # Bottom Left
    pt2_x, pt2_y = 0, int(height * 0.4)          # Top Left (starts 40% down)
    pt3_x, pt3_y = int(width * 0.75), height     # Slants to 75% across the bottom
    
    ff_builder = slide.shapes.build_freeform(pt1_x, pt1_y)
    ff_builder.add_line_segments([
        (pt2_x, pt2_y),
        (pt3_x, pt3_y),
        (pt1_x, pt1_y)
    ])
    navy_shape = ff_builder.convert_to_shape()
    navy_shape.fill.solid()
    navy_shape.fill.fore_color.rgb = NAVY
    navy_shape.line.fill.background() # No outline

    # === Layer 3: Parallel Accent Line (Red) ===
    # Creates a thin band perfectly parallel to the slant
    offset = Inches(0.15)
    thickness = Inches(0.1)
    
    r_pt1_x, r_pt1_y = 0, int(height * 0.4) - offset
    r_pt2_x, r_pt2_y = 0, int(height * 0.4) - offset - thickness
    r_pt3_x, r_pt3_y = int(width * 0.75) + offset + thickness, height
    r_pt4_x, r_pt4_y = int(width * 0.75) + offset, height
    
    ff_builder_red = slide.shapes.build_freeform(r_pt1_x, r_pt1_y)
    ff_builder_red.add_line_segments([
        (r_pt2_x, r_pt2_y),
        (r_pt3_x, r_pt3_y),
        (r_pt4_x, r_pt4_y),
        (r_pt1_x, r_pt1_y)
    ])
    red_shape = ff_builder_red.convert_to_shape()
    red_shape.fill.solid()
    red_shape.fill.fore_color.rgb = RED
    red_shape.line.fill.background()

    # === Layer 4: Top Right Minimal Geometric Accent ===
    tr_pt1_x, tr_pt1_y = width, 0
    tr_pt2_x, tr_pt2_y = width, int(height * 0.2)
    tr_pt3_x, tr_pt3_y = int(width * 0.8), 0
    
    ff_builder_tr = slide.shapes.build_freeform(tr_pt1_x, tr_pt1_y)
    ff_builder_tr.add_line_segments([
        (tr_pt2_x, tr_pt2_y),
        (tr_pt3_x, tr_pt3_y),
        (tr_pt1_x, tr_pt1_y)
    ])
    tr_shape = ff_builder_tr.convert_to_shape()
    tr_shape.fill.solid()
    tr_shape.fill.fore_color.rgb = NAVY
    tr_shape.line.fill.background()

    # === Layer 5: Text Formatting ===
    # Main Title on the right side (white space or over image)
    title_box = slide.shapes.add_textbox(Inches(7.5), Inches(4.5), Inches(5.5), Inches(2))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.RIGHT
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.font.name = "Arial"

    # Subtitle positioned over the Navy shape
    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(6), Inches(0.8))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = body_text
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = WHITE
    p_sub.font.name = "Arial"

    # Clean up temp files
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path

