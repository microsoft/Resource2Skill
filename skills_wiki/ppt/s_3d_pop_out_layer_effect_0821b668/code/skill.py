import requests
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

# It is required to install rembg: pip install rembg
try:
    from rembg import remove
except ImportError:
    print("Error: 'rembg' library not found. Please install it using 'pip install rembg'")
    remove = None

# LXML is used for advanced features like gradient fills
from lxml import etree
from pptx.oxml.ns import qn


def _set_gradient_fill(shape, angle, colors):
    """Applies a linear gradient fill to a shape using lxml."""
    sp = shape.element
    spPr = sp.get_or_add_spPr()
    
    gradFill = etree.SubElement(spPr, qn('a:gradFill'))
    lin = etree.SubElement(gradFill, qn('a:lin'), {'ang': str(angle * 60000), 'scaled': '1'})
    gsLst = etree.SubElement(gradFill, qn('a:gsLst'))

    for i, color_rgb in enumerate(colors):
        pos = int(i * 100000 / (len(colors) - 1))
        gs = etree.SubElement(gsLst, qn('a:gs'), {'pos': str(pos)})
        srgbClr = etree.SubElement(gs, qn('a:srgbClr'), {'val': '%02x%02x%02x' % color_rgb})
        etree.SubElement(srgbClr, qn('a:alpha'), {'val': '100000'}) # 100% opaque

def create_slide(
    output_pptx_path: str,
    title_text: str = "城市踏青公益活动",
    body_text: str = "走进自然,感受大自然的美丽和神奇,提高市民的健康意识,增强身体素质,促进社会和谐,让参与者感受到大自然的美好,增进社区居民之间的交流与友谊,激发社区居民积极向上的精神",
    image_url: str = "https://images.unsplash.com/photo-1524502397800-2eea8ff3220c",
    accent_color: tuple = (20, 158, 67),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a 3D Pop-Out Layer Effect.

    This effect layers a cutout of an image's subject over a trapezoid-shaped
    base of the original image to create an illusion of depth.

    Requires: python-pptx, pillow, requests, rembg

    Returns:
        str: The path to the saved PPTX file.
    """
    if remove is None:
        raise ImportError("The 'rembg' library is required for this function. Please install it.")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background & Decorative Elements ===
    # Set a white background (default, but explicit for clarity)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Add the green gradient bar at the bottom
    gradient_bar = slide.shapes.add_shape(1, 0, Inches(13.333), Inches(1.5))
    gradient_bar.top = prs.slide_height - gradient_bar.height
    gradient_bar.line.fill.background()
    
    # Gradient: light green to main accent green
    light_accent_color = tuple(min(255, c + 60) for c in accent_color)
    _set_gradient_fill(gradient_bar, 90, [light_accent_color, accent_color])


    # === Layer 2: Image Processing ===
    try:
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()
        original_image_bytes = response.content
        original_img = Image.open(io.BytesIO(original_image_bytes)).convert("RGBA")
    except (requests.exceptions.RequestException, IOError) as e:
        print(f"Error downloading or processing image: {e}. Using a placeholder.")
        original_img = Image.new('RGBA', (800, 600), (200, 200, 220))
        d = ImageDraw.Draw(original_img)
        d.text((10,10), "Image download failed", fill=(0,0,0))
        original_image_bytes = io.BytesIO()
        original_img.save(original_image_bytes, format='PNG')
        original_image_bytes = original_image_bytes.getvalue()

    # --- Create the Pop-Out Subject Cutout ---
    cutout_bytes = remove(original_image_bytes)
    cutout_img_stream = io.BytesIO(cutout_bytes)

    # --- Create the Trapezoid Base Image ---
    W, H = original_img.size
    
    # Define trapezoid coordinates for the "stage" (bottom ~60% of the image)
    top_y = H * 0.4
    bottom_y = H
    top_inset = W * 0.15 # How much the top corners are inset
    
    trapezoid_coords = [
        (top_inset, top_y), 
        (W - top_inset, top_y), 
        (W, bottom_y), 
        (0, bottom_y)
    ]

    mask = Image.new('L', (W, H), 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(trapezoid_coords, fill=255)

    base_img = Image.new('RGBA', (W, H))
    base_img.paste(original_img, (0, 0), mask)
    base_img_stream = io.BytesIO()
    base_img.save(base_img_stream, format='PNG')
    
    # === Layer 3: Assemble Slide Content ===
    # Add Title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.33), Inches(1.0))
    title_tf = title_shape.text_frame
    title_tf.text = title_text
    title_tf.paragraphs[0].font.size = Pt(40)
    title_tf.paragraphs[0].font.bold = True
    title_tf.paragraphs[0].font.color.rgb = RGBColor(18, 114, 49) # Dark green
    title_tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Add Body Text
    body_shape = slide.shapes.add_textbox(Inches(1), Inches(6.25), Inches(11.33), Inches(1))
    body_tf = body_shape.text_frame
    body_tf.text = body_text
    p = body_tf.paragraphs[0]
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.LEFT
    body_shape.z_order = 10 # Ensure it's on top of the gradient bar

    # Add the images - positioning is key
    img_width = Inches(8)
    img_height = img_width * H / W
    img_left = (prs.slide_width - img_width) / 2
    img_top = (prs.slide_height - img_height) / 2 - Inches(0.2)

    # Add base image first
    slide.shapes.add_picture(base_img_stream, img_left, img_top, img_width, img_height)

    # Add cutout image on top, at the exact same position
    slide.shapes.add_picture(cutout_img_stream, img_left, img_top, img_width, img_height)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function:
# create_slide("pop_out_effect_slide.pptx")
