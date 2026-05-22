import requests
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_FILL
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "Production Plant",
    subtitle_text: str = "Collection of 10+ PowerPoint Templates",
    image_keyword: str = "factory",
    primary_color: tuple = (64, 84, 93),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the "Organic-Geometric Contrast" layout.

    This features a solid color panel on the left for text and a custom,
    organically-shaped picture frame on the right.

    Returns: Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Attempt to download a background image
    try:
        # Use a reliable image source like Pexels or Unsplash
        image_url = f"https://source.unsplash.com/1600x900/?{image_keyword}"
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image_stream = BytesIO(response.content)
    except (requests.exceptions.RequestException, IOError):
        # Fallback to a simple gradient if image download fails
        img = Image.new('RGB', (1600, 900), color=primary_color)
        d = ImageDraw.Draw(img)
        d.rectangle([(0, 0), (1600, 900)], fill=(20, 30, 40))
        image_stream = BytesIO()
        img.save(image_stream, format='PNG')
        image_stream.seek(0)

    # === Layer 1: The Organic Shape with Picture Fill ===
    # Define the path for the blob shape using bezier curves.
    # The FreeformBuilder uses EMUs (English Metric Units).
    slide_width_emu = prs.slide_width
    slide_height_emu = prs.slide_height

    # Coordinates for a nice organic "blob" on the right side of the slide
    # The points are defined as (x, y) tuples in fractions of slide dimensions
    path_points = [
        {"type": "start", "pt": (0.65, 0.15)},
        {"type": "curve", "pt1": (0.95, 0.05), "pt2": (1.05, 0.40), "pt3": (0.90, 0.60)},
        {"type": "curve", "pt1": (0.75, 0.80), "pt2": (0.70, 0.98), "pt3": (0.50, 0.85)},
        {"type": "curve", "pt1": (0.30, 0.72), "pt2": (0.35, 0.40), "pt3": (0.55, 0.35)},
        {"type": "curve", "pt1": (0.60, 0.30), "pt2": (0.55, 0.20), "pt3": (0.65, 0.15)},
    ]

    freeform_builder = slide.shapes.build_freeform(
        Emu(path_points[0]["pt"][0] * slide_width_emu), 
        Emu(path_points[0]["pt"][1] * slide_height_emu)
    )

    for p in path_points[1:]:
        freeform_builder.add_curve(
            Emu(p["pt1"][0] * slide_width_emu), Emu(p["pt1"][1] * slide_height_emu),
            Emu(p["pt2"][0] * slide_width_emu), Emu(p["pt2"][1] * slide_height_emu),
            Emu(p["pt3"][0] * slide_width_emu), Emu(p["pt3"][1] * slide_height_emu)
        )
    freeform_builder.close()
    shape = freeform_builder.convert_to_shape()

    # Fill the shape with the downloaded image
    shape.fill.background() # Clear any default fill
    picture_fill = shape.fill.picture(image_stream)

    # Remove the shape outline
    shape.line.fill.background()

    # === Layer 2: Geometric Text Panel ===
    left = Inches(0)
    top = Inches(0)
    width = Inches(4.75)
    height = prs.slide_height
    panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(*primary_color)
    panel.line.fill.background()

    # Place panel behind the blob shape if needed (adjust Z-order)
    # This isn't strictly necessary with this layout but good practice.
    panel_element = panel._element
    panel_element.getparent().remove(panel_element)
    panel_element.getparent().insert(0, panel_element)

    # === Layer 3: Text & Content ===
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(4), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial Black'
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(4), Inches(0.5))
    tf = subtitle_box.text_frame
    p = tf.paragraphs[0]
    p.text = subtitle_text
    p.font.name = 'Arial'
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Decorative line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(4.0), Inches(4), Inches(0.02))
    line.fill.solid()
    # Using a slightly lighter shade for the line
    line.fill.fore_color.rgb = RGBColor(117, 182, 180) # Light Teal accent
    line.line.fill.background()

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide(
#     "production_plant_slide.pptx",
#     title_text="Advanced Manufacturing",
#     subtitle_text="Optimizing the Factory of the Future",
#     image_keyword="robotics factory"
# )

