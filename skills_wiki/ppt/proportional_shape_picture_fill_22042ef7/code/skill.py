import requests
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement
from pptx.parts.image import ImagePart
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw

def _add_picture_fill_to_shape(shape, image_path, prs, slide):
    """
    Adds a non-stretching picture fill to a shape using lxml.
    """
    # 1. Get the shape's XML element tree
    sp = shape._sp
    
    # 2. Get the shape properties element, creating it if it doesn't exist
    spPr = sp.get_or_add_spPr()

    # 3. Remove any existing fill (like the default solid fill)
    # Check for solidFill, gradFill, etc., and remove them.
    for fill_type in ['solidFill', 'gradFill', 'pattFill', 'grpFill', 'noFill']:
        fill_element = spPr.find(qn(f'a:{fill_type}'))
        if fill_element is not None:
            spPr.remove(fill_element)

    # 4. Add the image to the presentation's package and create a relationship
    # This caching mechanism prevents adding the same image multiple times
    if not hasattr(prs, '_image_parts_cache'):
        prs._image_parts_cache = {}
    
    if image_path not in prs._image_parts_cache:
        image_part = ImagePart.from_file(image_path)
        prs._image_parts_cache[image_path] = image_part
    else:
        image_part = prs._image_parts_cache[image_path]
    
    rId = slide.part.relate_to(image_part, RT.IMAGE)

    # 5. Create the blipFill element for picture fill
    blipFill = OxmlElement("a:blipFill")
    
    # 6. Create the blip element with the relationship ID
    blip = OxmlElement("a:blip")
    blip.set(qn("r:embed"), rId)
    
    # 7. Create the tile element - THIS IS THE KEY TO PREVENT STRETCHING
    tile = OxmlElement("a:tile")

    # 8. Create the stretch and fillRect elements (required structure)
    stretch = OxmlElement("a:stretch")
    fillRect = OxmlElement("a:fillRect")
    stretch.append(fillRect)

    # 9. Assemble the blipFill element
    blipFill.append(blip)
    blipFill.append(tile) # Add the tile element
    blipFill.append(stretch)

    # 10. Append the new blipFill to the shape properties
    spPr.append(blipFill)


def create_slide(
    output_pptx_path: str,
    title_text: str = "Proportional Shape Picture Fill",
    image_url: str = "https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=800",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide demonstrating how to fill various shapes with a
    non-distorted picture.

    This technique uses lxml to inject the <a:tile/> property into the shape's
    fill, which preserves the image's aspect ratio.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[5]) # Title only layout

    # Set slide title
    title = slide.shapes.title
    title.text = title_text
    title.text_frame.paragraphs[0].font.size = Pt(36)
    title.text_frame.paragraphs[0].font.bold = True
    
    # --- Image Handling ---
    image_path = "temp_image.jpg"
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(image_path, 'wb') as f:
            f.write(response.content)
    except (requests.exceptions.RequestException, IOError):
        print("Image download failed. Using a fallback placeholder image.")
        img = Image.new('RGB', (800, 1000), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((100,450), "Image Not Found", fill=(255,255,0), font_size=80)
        img.save(image_path)

    # --- Shape Definitions ---
    shapes_to_create = [
        {'type': MSO_SHAPE.OVAL, 'left': 0.5, 'top': 2.0, 'width': 2.5, 'height': 2.5},
        {'type': MSO_SHAPE.HEXAGON, 'left': 3.5, 'top': 2.0, 'width': 2.5, 'height': 2.5},
        {'type': MSO_SHAPE.PENTAGON, 'left': 6.5, 'top': 2.0, 'width': 2.5, 'height': 2.5},
        {'type': MSO_SHAPE.DIAMOND, 'left': 9.5, 'top': 2.0, 'width': 2.5, 'height': 2.5},
        {'type': MSO_SHAPE.RIGHT_ARROW, 'left': 2.0, 'top': 5.0, 'width': 3.5, 'height': 2.0},
        {'type': MSO_SHAPE.ROUNDED_RECTANGLE, 'left': 7.0, 'top': 5.0, 'width': 3.5, 'height': 2.0},
    ]

    # --- Create and Fill Shapes ---
    for s_def in shapes_to_create:
        shape = slide.shapes.add_shape(
            s_def['type'], Inches(s_def['left']), Inches(s_def['top']), 
            Inches(s_def['width']), Inches(s_def['height'])
        )
        
        # Apply the custom picture fill
        _add_picture_fill_to_shape(shape, image_path, prs, slide)
        
        # Optional: Add an outline to the shape
        line = shape.line
        line.color.rgb = (217, 217, 217)
        line.width = Pt(2.0)

    prs.save(output_pptx_path)
    return output_pptx_path
