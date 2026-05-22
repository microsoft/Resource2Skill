import requests
import io
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

def _add_picture_fill_to_run(run, pic_id, crop_rect=None):
    """
    Injects XML to fill a text run with a picture.
    crop_rect is a dict {'l', 't', 'r', 'b'} with percentage values * 1000.
    e.g., {'l': 40000, 'r': 40000} crops 40% from left and right.
    """
    rPr = run._r.get_or_add_rPr()
    
    blip_fill = etree.Element(qn('a:blipFill'))
    blip = etree.SubElement(blip_fill, qn('a:blip'), {
        qn('r:embed'): pic_id,
        qn('cstate'): 'print'
    })
    
    if crop_rect:
        src_rect = etree.SubElement(blip_fill, qn('a:srcRect'), {
            'l': str(crop_rect.get('l', 0)),
            't': str(crop_rect.get('t', 0)),
            'r': str(crop_rect.get('r', 0)),
            'b': str(crop_rect.get('b', 0))
        })

    stretch = etree.SubElement(blip_fill, qn('a:stretch'))
    fill_rect = etree.SubElement(stretch, qn('a:fillRect'))
    
    rPr.insert(0, blip_fill)

def _set_morph_transition(slide):
    """Injects XML to set the slide transition to 'morph'."""
    slide_element = slide._element
    # Find the p:cSld element to insert after, which is standard
    csld_element = slide_element.find(qn('p:cSld'))
    if csld_element is not None:
        # Check for existing transition and remove it
        existing_transition = slide_element.find(qn('p:transition'))
        if existing_transition is not None:
            slide_element.remove(existing_transition)

        # Create new morph transition element
        transition_element = etree.Element(qn('p:transition'), {
            'spd': 'slow', # slow (2s), med (1s), fast (0.5s)
            'advClick': '1' # Advance on click
        })
        morph_element = etree.SubElement(transition_element, qn('p:morph'))
        
        # Insert the new transition element after the common slide data
        csld_index = list(slide_element).index(csld_element)
        slide_element.insert(csld_index + 1, transition_element)

def create_slide(
    output_pptx_path: str,
    title_text: str = "LONDON",
    image_theme: str = "london",
    bg_color: tuple = (255, 242, 233),
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Morphing Text Photo Reveal effect.

    Args:
        output_pptx_path: Path to save the final .pptx file.
        title_text: The main text to display.
        image_theme: A keyword for fetching a background image from Pexels.
        bg_color: A tuple (R, G, B) for the slide background.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # --- Image Handling ---
    image_url = f"https://source.unsplash.com/1600x900/?{image_theme}"
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()
        image_stream = io.BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}. Cannot create slide.")
        # As a fallback, you could generate a gradient with PIL, but for this
        # specific skill, the image is essential.
        raise

    # --- Slide 1: Start of Morph (Zoomed-in Image) ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide1.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # Add shared image to presentation
    image_part = prs.part.relate_to(image_stream, "image/jpeg")
    pic_id = image_part.rId

    # Text box for slide 1
    txBox1 = slide1.shapes.add_textbox(Inches(0.5), Inches(2), prs.slide_width - Inches(1), Inches(3.5))
    p1 = txBox1.text_frame.paragraphs[0]
    p1.text = title_text
    p1.font.name = 'Arial Black'
    p1.font.size = Pt(220)
    p1.font.bold = True
    p1.alignment = PP_ALIGN.CENTER
    
    # Apply cropped picture fill to text
    run1 = p1.runs[0]
    # Crop 45% from each side, leaving the central 10% visible
    crop = {'l': 45000, 't': 45000, 'r': 45000, 'b': 45000}
    _add_picture_fill_to_run(run1, pic_id, crop_rect=crop)

    # --- Slide 2: End of Morph (Full Image) ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide2.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)
    
    # Text box for slide 2 (must be identical for morph to work)
    txBox2 = slide2.shapes.add_textbox(Inches(0.5), Inches(2), prs.slide_width - Inches(1), Inches(3.5))
    p2 = txBox2.text_frame.paragraphs[0]
    p2.text = title_text
    p2.font.name = 'Arial Black'
    p2.font.size = Pt(220)
    p2.font.bold = True
    p2.alignment = PP_ALIGN.CENTER

    # Apply full picture fill to text
    run2 = p2.runs[0]
    _add_picture_fill_to_run(run2, pic_id)

    # Set the morph transition ON THE SECOND SLIDE
    _set_morph_transition(slide2)
    
    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     create_slide(
#         output_pptx_path="london_morph_reveal.pptx",
#         title_text="LONDON",
#         image_theme="london bridge sunset"
#     )
#     create_slide(
#         output_pptx_path="tokyo_morph_reveal.pptx",
#         title_text="TOKYO",
#         image_theme="tokyo skyline night"
#     )
