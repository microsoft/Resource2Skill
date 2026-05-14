import requests
import io
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn

def create_slide(
    output_pptx_path: str,
    title_text: str = "CAR",
    image_url: str = "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=2070",
    font_name: str = "Algerian",
    font_size: int = 200,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with text filled with an image, reproducing the "Photographic Text Mask" effect.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The text to be filled with the image.
        image_url: URL of the image to use as the fill.
        font_name: The name of a thick, bold font. 'Algerian', 'Impact', 'Arial Black' are good choices.
        font_size: The point size of the text.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide layout

    # --- Image Handling ---
    image_rId = None
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_stream = io.BytesIO(response.content)
        
        # Add image to the presentation's media parts and get its relationship ID (rId)
        image_part, image_rId = prs.part.get_or_add_image_part(image_stream)

    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not download image. Using solid fill. Error: {e}")
        # Proceed without image_rId, text will have default fill

    # --- Create Text Shape ---
    # Center the shape on the slide
    left = Inches(0)
    top = Inches(0)
    width = prs.slide_width
    height = prs.slide_height

    shape = slide.shapes.add_textbox(left, top, width, height)
    text_frame = shape.text_frame
    text_frame.word_wrap = False
    text_frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = text_frame.paragraphs[0]
    p.alignment = 1 # Center alignment
    run = p.add_run()
    run.text = title_text

    font = run.font
    font.name = font_name
    font.size = Pt(font_size)
    font.bold = True

    # --- XML Manipulation to Apply Picture Fill ---
    if image_rId:
        # Get the lxml element for the run
        r = run._r
        
        # Find the run properties element (a:rPr)
        rPr = r.get_or_add_rPr()
        
        # Remove any existing fill (like solid fill)
        solid_fill = rPr.find(qn("a:solidFill"))
        if solid_fill is not None:
            rPr.remove(solid_fill)
        
        # Create the picture fill element (a:blipFill)
        blip_fill = etree.SubElement(rPr, qn("a:blipFill"))
        
        # Create the blip element with the image's rId
        blip = etree.SubElement(blip_fill, qn("a:blip"))
        blip.set(qn("r:embed"), image_rId)
        
        # Create stretch properties to ensure the image fills the text
        stretch = etree.SubElement(blip_fill, qn("a:stretch"))
        fill_rect = etree.SubElement(stretch, qn("a:fillRect"))
        
        # Remove text outline for a cleaner look
        ln = rPr.find(qn("a:ln"))
        if ln is not None:
            rPr.remove(ln)
        no_fill_outline = etree.SubElement(rPr, qn("a:ln"))
        no_fill = etree.SubElement(no_fill_outline, qn("a:noFill"))


    prs.save(output_pptx_path)
    return output_pptx_path

