import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw

# Helper function to generate a gradient image
def generate_gradient_image(width, height, color1, color2, vertical=True):
    """Generates a gradient image using PIL."""
    base = Image.new('RGBA', (width, height), color1)
    draw = ImageDraw.Draw(base)
    if vertical:
        for i in range(height):
            blend = i / height
            r = int(color1[0] * (1 - blend) + color2[0] * blend)
            g = int(color1[1] * (1 - blend) + color2[1] * blend)
            b = int(color1[2] * (1 - blend) + color2[2] * blend)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
    else: # Horizontal
        for i in range(width):
            blend = i / width
            r = int(color1[0] * (1 - blend) + color2[0] * blend)
            g = int(color1[1] * (1 - blend) + color2[1] * blend)
            b = int(color1[2] * (1 - blend) + color2[2] * blend)
            draw.line([(i, 0), (i, height)], fill=(r, g, b))
    return base

def create_curtain_reveal_slide(
    output_pptx_path: str,
    title_text: str = "Business Strengths",
    image_keyword: str = "business meeting",
    **kwargs,
) -> str:
    """
    Creates a slide pre-configured for a 'Curtain Reveal' animation.
    The animation itself (Fly In) must be applied in PowerPoint.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background Content ===
    # Dark blue background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(13, 27, 42)

    # Left side: Image with Letter 'S'
    img_path = "temp_bg_image.jpg"
    try:
        url = f"https://source.unsplash.com/1600x900/?{image_keyword}"
        urllib.request.urlretrieve(url, img_path)
        # Crop the image to the left half
        with Image.open(img_path) as img:
            left_half = img.crop((0, 0, img.width // 2, img.height))
            left_half.save("temp_left_image.png")
        slide.shapes.add_picture("temp_left_image.png", Inches(0), Inches(0), width=Inches(8))
    except Exception as e:
        print(f"Could not download image, using placeholder: {e}")
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(8), Inches(9))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(30, 30, 50)
        shape.line.fill.background()

    # Right side: Text
    title_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.5), Inches(1), Inches(7), Inches(1))
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(103, 58, 183)
    title_shape.line.fill.background()
    title_shape.text_frame.text = title_text
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.size = Pt(28)
    
    # Body Text
    txBox = slide.shapes.add_textbox(Inches(8.5), Inches(2.5), Inches(7), Inches(4))
    tf = txBox.text_frame
    for i in range(4):
        p = tf.add_paragraph()
        p.text = f"Lorem ipsum dolor sit amet, consectetuer."
        p.font.color.rgb = RGBColor(220, 220, 220)
        p.font.size = Pt(16)


    # === Layer 2: The 'Curtains' ===
    # These are added last so they are on top. In PPT, you'd move them off-slide.
    # Here we generate them as images and place them to cover the content.
    # To animate, open the PPT, move the top panel above the slide, the bottom panel
    # below, and apply 'Fly In' animations (from top/from bottom).
    
    width_px, height_px = 1536, 432  # 16:9 aspect ratio for a half-slide panel
    color1 = (103, 58, 183) # Purple
    color2 = (0, 188, 212) # Cyan
    
    # Top curtain
    grad_top = generate_gradient_image(width_px, height_px, color1, color2, vertical=True)
    top_path = "temp_grad_top.png"
    grad_top.save(top_path)
    slide.shapes.add_picture(top_path, Inches(0), Inches(0), width=Inches(16), height=Inches(4.5))

    # Bottom curtain (reversed gradient)
    grad_bottom = generate_gradient_image(width_px, height_px, color2, color1, vertical=True)
    bottom_path = "temp_grad_bottom.png"
    grad_bottom.save(bottom_path)
    slide.shapes.add_picture(bottom_path, Inches(0), Inches(4.5), width=Inches(16), height=Inches(4.5))

    prs.save(output_pptx_path)
    
    # Clean up temp files
    for f in ["temp_bg_image.jpg", "temp_left_image.png", top_path, bottom_path]:
        if os.path.exists(f):
            os.remove(f)
            
    return output_pptx_path


def create_depth_illusion_slide(
    output_pptx_path: str,
    bg_image_path: str,
    fg_cutout_path: str,
    title_text: str = "Business Opportunities",
    graphic_text: str = "O",
    **kwargs,
) -> str:
    """
    Creates a slide with a text/object depth illusion.
    Requires a background image and a foreground cutout PNG.

    Returns: path to the saved PPTX file.
    """
    if not os.path.exists(bg_image_path) or not os.path.exists(fg_cutout_path):
        raise FileNotFoundError("Background image or foreground cutout image not found.")

    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Dark blue background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(13, 27, 42)

    # === Layering is CRITICAL here. Order of addition is the Z-order. ===

    # Layer 1: The full background image (left side)
    slide.shapes.add_picture(bg_image_path, Inches(0), Inches(0), width=Inches(8))

    # Layer 2: The large graphic text ('O')
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(7), Inches(7))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = graphic_text
    p.font.name = 'Arial Black'
    p.font.size = Pt(500)
    p.font.bold = True
    # Semi-transparent light blue fill
    p.font.color.rgb = RGBColor(173, 216, 230)
    # The transparency must be set on the fill of the font, which is more complex (lxml)
    # For simplicity here, we use a solid color. A true reproduction would use lxml.

    # Layer 3: The foreground cutout, placed directly on top of the background
    slide.shapes.add_picture(fg_cutout_path, Inches(0), Inches(0), width=Inches(8))

    # Layer 4: Text content on the right
    title_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.5), Inches(1), Inches(7), Inches(1))
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(103, 58, 183)
    title_shape.line.fill.background()
    title_shape.text_frame.text = title_text
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    body_txBox = slide.shapes.add_textbox(Inches(8.5), Inches(2.5), Inches(7), Inches(4))
    body_tf = body_txBox.text_frame
    body_tf.text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa."

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
if __name__ == '__main__':
    # Create the curtain reveal slide
    curtain_pptx = "curtain_reveal_example.pptx"
    create_curtain_reveal_slide(curtain_pptx, image_keyword="city-skyline")
    print(f"Curtain reveal setup slide saved to {curtain_pptx}")
    print("Open it, move the top/bottom panels off-slide, and apply 'Fly In' animations.")

    # Create the depth illusion slide
    # NOTE: You must provide your own images for this to work.
    # 1. Download an image, e.g., a person standing. Save as 'my_background.jpg'
    # 2. Use a tool (e.g., remove.bg) to remove the background. Save as 'my_foreground.png'
    bg_img = 'background_man_on_stairs.jpg'
    fg_img = 'foreground_man_on_stairs.png'

    # Download example images if they don't exist
    if not os.path.exists(bg_img):
        print("Downloading example background image...")
        urllib.request.urlretrieve("https://images.unsplash.com/photo-1543269664-7e6795b55898", bg_img) # Man on stairs
    if not os.path.exists(fg_img):
         print("Downloading example foreground image (pre-cut)...")
         # This is a placeholder cutout. A real one would be higher quality.
         # For a real use case, you'd create this yourself.
         urllib.request.urlretrieve("https://i.imgur.com/kSjVq7N.png", fg_img)

    depth_pptx = "depth_illusion_example.pptx"
    create_depth_illusion_slide(depth_pptx, bg_image_path=bg_img, fg_cutout_path=fg_img)
    print(f"Depth illusion slide saved to {depth_pptx}")
