import io
import requests
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageDraw

def create_circular_avatar(image_url: str, size: int) -> io.BytesIO:
    """
    Downloads an image, crops it to a square, masks it into a circle,
    and returns it as a BytesIO stream.

    Args:
        image_url: URL of the image to download.
        size: The diameter of the circular avatar in pixels.

    Returns:
        A BytesIO stream containing the circular PNG image data.
    """
    try:
        response = requests.get(image_url, stream=True, timeout=5)
        response.raise_for_status()
        img = Image.open(response.raw).convert("RGBA")
    except (requests.exceptions.RequestException, IOError):
        # Fallback: create a gray circle if image download or processing fails
        img = Image.new('RGBA', (300, 300), color=(128, 128, 128, 255))

    # Center-crop to a square
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Create a circular alpha mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply the mask to the image's alpha channel
    img.putalpha(mask)
    
    image_stream = io.BytesIO()
    img.save(image_stream, format='PNG')
    image_stream.seek(0)
    return image_stream

def create_paperclip_icon(slide, left: Emu, top: Emu, color: RGBColor):
    """
    Creates a stylized paperclip icon using a rotated rounded rectangle.

    Args:
        slide: The python-pptx slide object.
        left: The left position in Emu.
        top: The top position in Emu.
        color: The RGBColor for the icon.
    """
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.25), Inches(0.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background() # No outline
    shape.rotation = 315 # Rotated -45 degrees

def create_slide(
    output_pptx_path: str,
    title_text: str = "SWOT Analysis For A YouTuber's Home",
    strengths_text: list = None,
    weaknesses_text: list = None,
    opportunities_text: list = None,
    threats_text: list = None,
    avatar_url: str = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a Modular Color-Block Infographic style,
    reproducing the SWOT analysis template from the tutorial.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    # Use portrait A4-like dimensions for an infographic feel
    prs.slide_width = Inches(8.27)
    prs.slide_height = Inches(11.69)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Default Content ---
    strengths_text = strengths_text or ["Strong community engagement", "Consistent content schedule", "Unique video editing style"]
    weaknesses_text = weaknesses_text or ["High production costs", "Dependent on a single platform", "Burnout risk"]
    opportunities_text = opportunities_text or ["Collaborations with other creators", "Merchandise line", "Expanding to new platforms"]
    threats_text = threats_text or ["Algorithm changes", "New competitors", "Audience fatigue"]

    # === Layer 1: Background ===
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(245, 245, 245)

    # === Header Block ===
    avatar_stream = create_circular_avatar(avatar_url, size=200)
    slide.shapes.add_picture(avatar_stream, Inches(3.635), Inches(0.5), width=Inches(1.0))

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(7.27), Inches(1.0))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = 'Lato Black'
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(51, 51, 51)
    p.alignment = PP_ALIGN.CENTER
    tf.word_wrap = True

    # === Content Grid (2x2) ===
    grid_top, grid_left = Inches(3.0), Inches(0.5)
    grid_width, grid_height = Inches(7.27), Inches(6.0)
    block_width = (grid_width - Inches(0.2)) / 2
    block_height = (grid_height - Inches(0.2)) / 2
    
    colors = {
        "Strengths": RGBColor(133, 184, 230), "Weaknesses": RGBColor(230, 102, 143),
        "Opportunities": RGBColor(244, 201, 88), "Threats": RGBColor(220, 93, 89)
    }
    content = {
        "Strengths": strengths_text, "Weaknesses": weaknesses_text,
        "Opportunities": opportunities_text, "Threats": threats_text
    }
    positions = {
        "Strengths": (grid_left, grid_top),
        "Weaknesses": (grid_left + block_width + Inches(0.2), grid_top),
        "Opportunities": (grid_left, grid_top + block_height + Inches(0.2)),
        "Threats": (grid_left + block_width + Inches(0.2), grid_top + block_height + Inches(0.2))
    }

    for key, (l, t) in positions.items():
        block = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, block_width, block_height)
        block.fill.solid()
        block.fill.fore_color.rgb = colors[key]
        block.line.fill.background()

        text_box = slide.shapes.add_textbox(l + Inches(0.2), t + Inches(0.2), block_width - Inches(0.4), block_height - Inches(0.4))
        tf = text_box.text_frame
        tf.clear(); tf.word_wrap = True

        p_title = tf.paragraphs[0]
        p_title.text = key.upper(); p_title.font.name = 'Lato Bold'; p_title.font.size = Pt(16)
        p_title.font.color.rgb = RGBColor(255, 255, 255); p_title.space_after = Pt(12)

        for item in content[key]:
            p_item = tf.add_paragraph(); p_item.text = f"• {item}"; p_item.font.name = 'Lato'
            p_item.font.size = Pt(11); p_item.font.color.rgb = RGBColor(255, 255, 255)
            p_item.level = 0; p_item.space_after = Pt(6)
        
        # This removes the default first bullet point that python-pptx adds
        tf.paragraphs[1].font.size = Pt(11)

        create_paperclip_icon(slide, l + block_width - Inches(0.3), t - Inches(0.15), RGBColor(180, 180, 180))

    prs.save(output_pptx_path)
    return output_pptx_path

