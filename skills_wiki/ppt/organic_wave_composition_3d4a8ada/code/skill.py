import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.shapes.freeform import FreeformBuilder
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "Call to Action",
    subtitle_text: str = "Digital Action Project",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a dynamic, modern design using layered organic wave shapes.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Define colors from the tutorial's palette
    COLOR_BG_WHITE = RGBColor(255, 255, 255)
    COLOR_PURPLE = RGBColor(76, 38, 134)
    COLOR_ORANGE = RGBColor(244, 122, 33)
    COLOR_LILAC = RGBColor(216, 203, 235)
    COLOR_TEXT = RGBColor(68, 68, 68)

    # Set a solid white background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG_WHITE

    # --- Layer 1: Wavy Shapes using FreeformBuilder ---
    width, height = prs.slide_width, prs.slide_height

    # Shape 1: Bottom Lilac Wave
    with FreeformBuilder(slide, Inches(0), Inches(0), width, height) as builder:
        builder.move_to(0, height * 0.6)
        builder.curve_to(width * 0.3, height * 0.5, width * 0.7, height, width, height * 0.8)
        builder.line_to(width, height)
        builder.line_to(0, height)
        builder.close()
    shape1 = builder.shape
    shape1.fill.solid()
    shape1.fill.fore_color.rgb = COLOR_LILAC
    shape1.line.fill.background()

    # Shape 2: Top/Main Purple Wave
    with FreeformBuilder(slide, Inches(0), Inches(0), width, height) as builder:
        builder.move_to(0, 0)
        builder.line_to(width * 0.95, 0)
        builder.curve_to(width * 0.8, height * 0.4, width * 0.4, height * 0.9, 0, height * 0.7)
        builder.close()
    shape2 = builder.shape
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = COLOR_PURPLE
    shape2.line.fill.background()

    # Shape 3: Top-Right Orange Wave
    with FreeformBuilder(slide, Inches(0), Inches(0), width, height) as builder:
        builder.move_to(width * 0.3, 0)
        builder.curve_to(width * 0.6, height * 0.1, width * 0.9, height * 0.5, width, height * 0.4)
        builder.line_to(width, 0)
        builder.close()
    shape3 = builder.shape
    shape3.fill.solid()
    shape3.fill.fore_color.rgb = COLOR_ORANGE
    shape3.line.fill.background()

    # Send shapes to the back to act as a background
    slide.shapes._spTree.remove(shape1._sp)
    slide.shapes._spTree.insert(2, shape1._sp)
    slide.shapes._spTree.remove(shape2._sp)
    slide.shapes._spTree.insert(2, shape2._sp)
    slide.shapes._spTree.remove(shape3._sp)
    slide.shapes._spTree.insert(2, shape3._sp)

    # --- Layer 2: Central Graphic Placeholder (using PIL) ---
    img_size = (int(Inches(4).to_emu() / 9525), int(Inches(3).to_emu() / 9525))
    im = Image.new("RGBA", img_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Monitor
    draw.rectangle([img_size[0]*0.1, img_size[1]*0.1, img_size[0]*0.9, img_size[1]*0.7], fill=(220, 220, 220, 255))
    draw.rectangle([img_size[0]*0.15, img_size[1]*0.15, img_size[0]*0.85, img_size[1]*0.65], fill=(245, 245, 245, 255))
    draw.rectangle([img_size[0]*0.4, img_size[1]*0.7, img_size[0]*0.6, img_size[1]*0.9], fill=(200, 200, 200, 255))
    draw.rectangle([img_size[0]*0.3, img_size[1]*0.9, img_size[0]*0.7, img_size[1]*0.95], fill=(200, 200, 200, 255))

    # Megaphone
    megaphone_color = tuple(COLOR_LILAC)
    draw.polygon([
        (img_size[0]*0.4, img_size[1]*0.3), 
        (img_size[0]*0.7, img_size[1]*0.2), 
        (img_size[0]*0.75, img_size[1]*0.5), 
        (img_size[0]*0.4, img_size[1]*0.4)
    ], fill=megaphone_color)
    draw.rectangle([img_size[0]*0.3, img_size[1]*0.32, img_size[0]*0.4, img_size[1]*0.38], fill=megaphone_color)
    
    placeholder_path = "placeholder_graphic.png"
    im.save(placeholder_path)
    slide.shapes.add_picture(placeholder_path, Inches(4.66), Inches(2.25), width=Inches(4))
    os.remove(placeholder_path)

    # --- Layer 3: Text ---
    # Title
    txBox = slide.shapes.add_textbox(Inches(0), Inches(2.8), width, Inches(1.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial Black'
    p.font.size = Pt(72)
    p.font.color.rgb = COLOR_TEXT
    p.alignment = 1  # Center

    # Subtitle
    txBox_sub = slide.shapes.add_textbox(Inches(0), Inches(3.9), width, Inches(1))
    tf_sub = txBox_sub.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(24)
    p_sub.font.color.rgb = COLOR_TEXT
    p_sub.alignment = 1  # Center

    prs.save(output_pptx_path)
    return output_pptx_path

