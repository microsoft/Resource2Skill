import io
import requests
from lxml import etree
from PIL import Image, ImageDraw

from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Helper for lxml to handle XML namespaces
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace prefixed
    tag name into a Clark-notation qualified tag name for lxml. For example,
    qn('p:cSld') returns '{http://schemas.openxmlformats.org/presentationml/2006/main}cSld'.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return f'{{{uri}}}{tagroot}'

def create_magnified_crop(
    magnified_img: Image.Image,
    center_coords_on_base: tuple,
    magnification: float,
    lens_diameter_px: int
) -> Image.Image:
    """
    Creates a circular, magnified crop of an image.

    Args:
        magnified_img: The pre-magnified PIL Image object.
        center_coords_on_base: (x, y) tuple of the lens center on the original, non-magnified image.
        magnification: The factor by which the image was scaled (e.g., 2.0).
        lens_diameter_px: The diameter of the magnifying lens in pixels.

    Returns:
        A new PIL Image object (RGBA) containing the circular magnified view.
    """
    # Calculate the crop box on the *magnified* image
    magnified_center_x = center_coords_on_base[0] * magnification
    magnified_center_y = center_coords_on_base[1] * magnification
    
    half_lens = lens_diameter_px / 2
    
    crop_box = (
        int(magnified_center_x - half_lens),
        int(magnified_center_y - half_lens),
        int(magnified_center_x + half_lens),
        int(magnified_center_y + half_lens)
    )

    # Crop the magnified image
    cropped_content = magnified_img.crop(crop_box)

    # Create a circular alpha mask
    mask = Image.new('L', (lens_diameter_px, lens_diameter_px), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, lens_diameter_px, lens_diameter_px), fill=255)

    # Apply the mask
    result = Image.new('RGBA', (lens_diameter_px, lens_diameter_px))
    result.paste(cropped_content, (0, 0), mask)
    
    return result

def create_slide_magnifying_glass(
    output_pptx_path: str,
    title_text: str = "Product Feature Highlight",
    bg_keyword: str = "technology",
    magnification: float = 2.5,
    **kwargs,
) -> str:
    """
    Creates a two-slide PPTX demonstrating the interactive magnifying glass effect
    using the Morph transition.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_text: The title text to display on the slide.
        bg_keyword: A keyword for fetching a background image from Unsplash.
        magnification: The zoom factor for the magnifying glass.

    Returns:
        Path to the saved PPTX file.
    """
    SLIDE_WIDTH_IN = 13.333
    SLIDE_HEIGHT_IN = 7.5
    
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH_IN)
    prs.slide_height = Inches(SLIDE_HEIGHT_IN)
    blank_layout = prs.slide_layouts[6]

    # --- Image Preparation ---
    img_bytes = None
    try:
        url = f"https://source.unsplash.com/1920x1080/?{bg_keyword}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img_bytes = io.BytesIO(response.content)
        base_img = Image.open(img_bytes).convert("RGBA")
    except requests.exceptions.RequestException:
        # Fallback to a generated gradient if image download fails
        base_img = Image.new("RGB", (1920, 1080))
        draw = ImageDraw.Draw(base_img)
        for i in range(1080):
            r = int(25 + 50 * i / 1080)
            g = int(30 + 60 * i / 1080)
            b = int(40 + 70 * i / 1080)
            draw.line([(0, i), (1920, i)], fill=(r, g, b))

    # Scale image to fit slide width
    img_w, img_h = base_img.size
    slide_w_px = int(prs.slide_width * 96 / 72) # Approximation
    base_h_px = int(slide_w_px * img_h / img_w)
    base_img = base_img.resize((slide_w_px, base_h_px))
    
    magnified_img = base_img.resize((int(slide_w_px * magnification), int(base_h_px * magnification)))
    
    # --- Define positions and lens size ---
    lens_diameter = Inches(2.5)
    lens_diameter_px = int(lens_diameter.emu / Emu(1) * 96 / 914400) # Convert EMU to pixels
    
    start_pos_in = (Inches(2), Inches(2.5))
    end_pos_in = (Inches(8.5), Inches(3.5))

    start_pos_px = (int(start_pos_in[0].emu * 96 / 914400), int(start_pos_in[1].emu * 96 / 914400))
    end_pos_px = (int(end_pos_in[0].emu * 96 / 914400), int(end_pos_in[1].emu * 96 / 914400))
    
    # --- Create magnified crops using PIL ---
    start_crop_img = create_magnified_crop(magnified_img, start_pos_px, magnification, lens_diameter_px)
    end_crop_img = create_magnified_crop(magnified_img, end_pos_px, magnification, lens_diameter_px)
    
    start_crop_stream = io.BytesIO()
    start_crop_img.save(start_crop_stream, format='PNG')
    start_crop_stream.seek(0)
    
    end_crop_stream = io.BytesIO()
    end_crop_img.save(end_crop_stream, format='PNG')
    end_crop_stream.seek(0)

    # --- Helper function to build a slide ---
    def build_slide(slide, pos_in, crop_stream):
        # Add base image
        slide.shapes.add_picture(io.BytesIO(base_img.tobytes()), 0, 0, width=prs.slide_width, height=prs.slide_height)

        # Add magnified lens content
        lens_content = slide.shapes.add_picture(crop_stream, pos_in[0], pos_in[1], width=lens_diameter, height=lens_diameter)
        lens_content.name = "!!MagLens"

        # Add magnifying glass frame
        frame = slide.shapes.add_shape(MSO_SHAPE.DONUT, pos_in[0] - Inches(0.05), pos_in[1] - Inches(0.05), lens_diameter + Inches(0.1), lens_diameter + Inches(0.1))
        frame.name = "!!MagFrame"
        frame.adjustments[0] = 0.1 # Make the donut ring thinner
        fill = frame.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(200, 200, 200)
        line = frame.line
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(150, 150, 150)
        line.width = Pt(1)

    # --- Create Slide 1 (Start Position) ---
    slide1 = prs.slides.add_slide(blank_layout)
    build_slide(slide1, start_pos_in, start_crop_stream)
    
    # --- Create Slide 2 (End Position) ---
    slide2 = prs.slides.add_slide(blank_layout)
    build_slide(slide2, end_pos_in, end_crop_stream)

    # --- Add Morph Transition to Slide 2 using lxml ---
    slide2_element = slide2.element
    transition = etree.SubElement(slide2_element, qn('p:transition'), {qn('p:spd'): 'slow', 'advClick': "0"})
    etree.SubElement(transition, qn('p:morph'), {'option': 'object'})

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == '__main__':
    # Example usage:
    output_file = "magnifying_glass_effect.pptx"
    create_slide_magnifying_glass(
        output_pptx_path=output_file,
        title_text="Highlighting Key Circuitry",
        bg_keyword="circuit board",
        magnification=3.0
    )
    print(f"Presentation saved to {output_file}")
