import os
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "商务服务",
    subtitle_text: str = "对接方案可行性报告",
    image_url: str = "https://images.unsplash.com/photo-1549048386-8832389141a9?w=1200", # A default city street image
    accent_color_1: tuple = (28, 117, 207),  # Blue
    accent_color_2: tuple = (255, 192, 0), # Yellow
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a wavy image panel divider.

    This reproduces a style where a 'Flowchart: Document' shape is rotated,
    filled with a picture, and the picture is kept upright while the shape container is rotated.
    
    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The main title for the slide.
        subtitle_text: The subtitle for the slide.
        image_url: URL of the background image for the panel.
        accent_color_1: RGB tuple for the rearmost accent shape.
        accent_color_2: RGB tuple for the middle accent shape.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Set a white background for the slide itself
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # === Layer 1: Download Image or Create Fallback ===
    image_path = "temp_wavy_panel_image.jpg"
    try:
        with urllib.request.urlopen(image_url) as response:
            image_data = response.read()
        with open(image_path, "wb") as f:
            f.write(image_data)
    except Exception as e:
        print(f"Failed to download image: {e}. Creating a fallback gradient image.")
        img = Image.new('RGB', (800, 1200), color = accent_color_1)
        draw = ImageDraw.Draw(img)
        # Simple gradient for fallback
        for i in range(1200):
            r = accent_color_1[0] + int((accent_color_2[0] - accent_color_1[0]) * (i / 1200))
            g = accent_color_1[1] + int((accent_color_2[1] - accent_color_1[1]) * (i / 1200))
            b = accent_color_1[2] + int((accent_color_2[2] - accent_color_1[2]) * (i / 1200))
            draw.line([(0, i), (800, i)], fill=(r,g,b))
        img.save(image_path)


    # === Layer 2: Visual Effect Shapes (created back-to-front for layering) ===
    slide_height = prs.slide_height
    shape_width = Inches(4.5)
    
    # Accent Shape 1 (Backmost)
    shape_1_left = prs.slide_width - shape_width + Inches(0.4)
    sp1 = slide.shapes.add_shape(
        MSO_SHAPE.FLOWCHART_DOCUMENT, shape_1_left, 0, shape_width, slide_height
    )
    sp1.rotation = 90.0
    sp1.vertical_flip = True
    fill1 = sp1.fill
    fill1.solid()
    fill1.fore_color.rgb = RGBColor(*accent_color_1)
    sp1.line.fill.background()

    # Accent Shape 2 (Middle)
    shape_2_left = prs.slide_width - shape_width + Inches(0.2)
    sp2 = slide.shapes.add_shape(
        MSO_SHAPE.FLOWCHART_DOCUMENT, shape_2_left, 0, shape_width, slide_height
    )
    sp2.rotation = 90.0
    sp2.vertical_flip = True
    fill2 = sp2.fill
    fill2.solid()
    fill2.fore_color.rgb = RGBColor(*accent_color_2)
    sp2.line.fill.background()

    # Main Image Shape (Topmost)
    shape_3_left = prs.slide_width - shape_width
    sp3 = slide.shapes.add_shape(
        MSO_SHAPE.FLOWCHART_DOCUMENT, shape_3_left, 0, shape_width, slide_height
    )
    sp3.rotation = 90.0
    sp3.vertical_flip = True
    
    # Apply picture fill
    fill3 = sp3.fill
    fill3.solid() # Must add a fill before a picture can be added
    fill3.picture(image_path)
    
    # CRITICAL STEP: Access underlying XML to prevent image from rotating with the shape
    # This is equivalent to unchecking "Rotate with shape" in PowerPoint's UI
    blip_fill = sp3._sp.spPr.blipFill
    blip_fill.set('rotWithShape', '0')
    sp3.line.fill.background() # Remove shape outline


    # === Layer 3: Text & Content ===
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(7), Inches(1.5))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    font_title = p_title.font
    font_title.name = 'Arial Black'
    font_title.size = Pt(54)
    font_title.color.rgb = RGBColor(*accent_color_2)

    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(2.7), Inches(7), Inches(1))
    tf_subtitle = subtitle_box.text_frame
    p_subtitle = tf_subtitle.paragraphs[0]
    p_subtitle.text = subtitle_text
    font_subtitle = p_subtitle.font
    font_subtitle.name = 'Arial'
    font_subtitle.bold = True
    font_subtitle.size = Pt(36)
    font_subtitle.color.rgb = RGBColor(0, 0, 0)
    
    # Body text placeholder
    body_text = ("Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "
                 "Maecenas porttitor congue massa. Fusce posuere, magna sed "
                 "pulvinar ultricies, purus lectus malesuada libero, sit amet "
                 "commodo magna eros quis urna.")
    body_box = slide.shapes.add_textbox(Inches(1), Inches(4.0), Inches(6), Inches(2))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    font_body = p_body.font
    font_body.name = 'Arial'
    font_body.size = Pt(12)
    font_body.color.rgb = RGBColor(128, 128, 128)

    # Cleanup and Save
    if os.path.exists(image_path):
        os.remove(image_path)
    
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("wavy_panel_divider_slide.pptx")

