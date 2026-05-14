import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree

# Helper to get the XML namespace prefix
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace prefixed
    tag name into a Clark-notation qualified tag name for lxml. For example,
    'p:cSld' becomes '{http://schemas.openxmlformats.org/presentationml/2006/main}cSld'.
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }
    prefix, tagroot = tag.split(':')
    return '{{{}}}{}'.format(ns[prefix], tagroot)

def _set_morph_transition(slide):
    """Injects Morph transition XML for a slide."""
    slide_xml = slide.element
    transition = etree.SubElement(slide_xml, qn('p:transition'), dur="1500") # 1.5 seconds
    etree.SubElement(transition, qn('p:morph'))

def _set_fade_transition(slide):
    """Injects Fade transition XML for a slide."""
    slide_xml = slide.element
    transition = etree.SubElement(slide_xml, qn('p:transition'), dur="700") # 0.7 seconds
    etree.SubElement(transition, qn('p:fade'))

def _add_picture_fill(shape, image_rId, focus_point):
    """
    Modifies a shape's XML to use a picture fill, with specific pan/zoom.
    focus_point = {'center_x': 0-1, 'center_y': 0-1, 'zoom': float}
    """
    zoom = focus_point.get('zoom', 2.0)
    cx = focus_point.get('center_x', 0.5)
    cy = focus_point.get('center_y', 0.5)

    sp = shape.element
    spPr = sp.xpath('p:spPr')[0]

    # Remove solid fill
    solid_fill = spPr.find(qn('a:solidFill'))
    if solid_fill is not None:
        spPr.remove(solid_fill)

    # Calculate source rectangle (srcRect) for pan and zoom
    # All values are in 100,000ths
    width_norm = 1.0 / zoom
    height_norm = 1.0 / zoom
    
    left_norm = max(0, cx - width_norm / 2)
    top_norm = max(0, cy - height_norm / 2)
    right_norm = min(1.0, left_norm + width_norm)
    bottom_norm = min(1.0, top_norm + height_norm)
    
    # Adjust for cases where the crop goes out of bounds
    if right_norm > 1.0: left_norm -= (right_norm - 1.0)
    if bottom_norm > 1.0: top_norm -= (bottom_norm - 1.0)

    l = int(left_norm * 100000)
    t = int(top_norm * 100000)
    r = int((1.0 - right_norm) * 100000)
    b = int((1.0 - bottom_norm) * 100000)

    # Add blipFill element
    blip_fill = etree.SubElement(spPr, qn('a:blipFill'))
    blip = etree.SubElement(blip_fill, qn('a:blip'), {'r:embed': image_rId})
    src_rect = etree.SubElement(blip_fill, qn('a:srcRect'), l=str(l), t=str(t), r=str(r), b=str(b))
    stretch = etree.SubElement(blip_fill, qn('a:stretch'))
    etree.SubElement(stretch, qn('a:fillRect'))

def _add_blur_effect(picture):
    """Adds a blur effect to a picture element."""
    pic = picture.element
    picPr = pic.xpath('p:picPr')[0]
    
    effect_lst = etree.SubElement(picPr, qn('a:effectLst'))
    etree.SubElement(effect_lst, qn('a:blur'), rad=str(Emu(Inches(0.1)))) # Adjust radius as needed

def create_slide(
    output_pptx_path: str,
    image_url: str = "https://upload.wikimedia.org/wikipedia/commons/5/5a/Solvay_conference_1927.jpg",
    focus_points: list = None
) -> str:
    """
    Creates a PPTX file demonstrating the Dynamic Spotlight Focus effect.

    Args:
        output_pptx_path: Path to save the final .pptx file.
        image_url: URL of the image to use as the background.
        focus_points: A list of dictionaries defining the spotlight targets.
                      Each dict: {'name': str, 'desc': str, 'center_x': float (0-1), 
                                  'center_y': float (0-1), 'zoom': float, 
                                  'pos_x': Inches, 'pos_y': Inches}

    Returns:
        Path to the saved PPTX file.
    """
    if focus_points is None:
        focus_points = [
            {
                'name': "Marie Curie", 'desc': "Pioneering researcher on radioactivity, two-time Nobel prize winner.",
                'center_x': 0.33, 'center_y': 0.65, 'zoom': 5.0,
                'pos_x': Inches(3), 'pos_y': Inches(1.5)
            },
            {
                'name': "Albert Einstein", 'desc': "Developed the theory of relativity, one of the two pillars of modern physics.",
                'center_x': 0.5, 'center_y': 0.65, 'zoom': 6.0,
                'pos_x': Inches(5.6), 'pos_y': Inches(1.5)
            },
            {
                'name': "Niels Bohr", 'desc': "Made foundational contributions to understanding atomic structure and quantum theory.",
                'center_x': 0.61, 'center_y': 0.35, 'zoom': 6.0,
                'pos_x': Inches(8), 'pos_y': Inches(2.5)
            },
        ]

    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_slide_layout = prs.slide_layouts[6]

    # --- Download and add image ---
    try:
        image_path = "temp_focus_image.jpg"
        urllib.request.urlretrieve(image_url, image_path)
    except Exception as e:
        print(f"Failed to download image: {e}")
        # Fallback: create a dummy image
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (1920, 1080), color = 'darkgray')
        d = ImageDraw.Draw(img)
        d.text((10,10), "Image download failed", fill='white')
        img.save(image_path)

    # === Slide 1: The Initial Clear Image ===
    slide1 = prs.slides.add_slide(blank_slide_layout)
    slide1.shapes.add_picture(image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Create subsequent slides with the effect ---
    for i, point in enumerate(focus_points):
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # Add a unique object name for Morph to track
        # This name must be the same on all slides where the object morphs
        spotlight_name = "SpotlightCircle"

        # --- Layer 1: Blurred Background ---
        bg_pic = slide.shapes.add_picture(image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
        _add_blur_effect(bg_pic)

        # --- Layer 2: Spotlight Circle ---
        spotlight_size = Inches(2.5)
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, point['pos_x'], point['pos_y'], spotlight_size, spotlight_size)
        shape.element.set(qn('p:nvSpPr.cNvPr.name'), spotlight_name) # Set name for Morph

        # Add picture fill via XML
        img_part, rId = shape.part.get_or_add_image(image_path)
        _add_picture_fill(shape, rId, point)

        # Add white border
        line = shape.line
        line.color.rgb = RGBColor(255, 255, 255)
        line.width = Pt(4)

        # --- Layer 3: Text Box ---
        tx_box = slide.shapes.add_textbox(Inches(3), Inches(6.5), Inches(10), Inches(2))
        tf = tx_box.text_frame
        tf.clear()
        
        p_name = tf.paragraphs[0]
        p_name.text = point['name']
        p_name.font.size = Pt(36)
        p_name.font.bold = True
        p_name.font.color.rgb = RGBColor(255, 255, 255)
        
        p_desc = tf.add_paragraph()
        p_desc.text = point['desc']
        p_desc.font.size = Pt(20)
        p_desc.font.color.rgb = RGBColor(220, 220, 220)

        # --- Set Transition ---
        if i == 0:
            _set_fade_transition(slide)
        else:
            _set_morph_transition(slide)

    # Cleanup
    if os.path.exists(image_path):
        os.remove(image_path)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("dynamic_spotlight_focus.pptx")
