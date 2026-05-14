import os
import requests
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree

# Helper for XML namespace mapping
def qn(tag):
    """
    Get a qualified name for an XML tag.
    e.g. qn('a:prstGeom') -> '{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom'
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }
    prefix, local = tag.split(':')
    return f'{{{ns[prefix]}}}{local}'

def _set_slide_background_fill(shape):
    """Applies 'Slide background fill' to a shape using lxml."""
    spPr = shape.element.spPr
    # Remove any existing fill properties
    for fill_prop in spPr.findall(qn("a:solidFill")):
        spPr.remove(fill_prop)
    for fill_prop in spPr.findall(qn("a:gradFill")):
        spPr.remove(fill_prop)
    for fill_prop in spPr.findall(qn("a:pattFill")):
        spPr.remove(fill_prop)
    # Add the background fill property
    bg_fill = etree.SubElement(spPr, qn('a:bgFill'))

def _add_shadow_to_shape(shape):
    """Adds a soft right-offset shadow to a shape using lxml."""
    spPr = shape.element.spPr
    effect_list = spPr.find(qn('a:effectLst'))
    if effect_list is None:
        effect_list = etree.SubElement(spPr, qn('a:effectLst'))

    # Values from tutorial: Transparency: 60%, Size: 102%, Blur: 4pt, Angle: 0, Distance: 1pt
    shadow = etree.SubElement(effect_list, qn('a:outerShdw'))
    shadow.set('blurRad', str(Emu(Pt(4))))  # Blur 4pt
    shadow.set('dist', str(Emu(Pt(1))))    # Distance 1pt
    shadow.set('dir', '0')                 # Angle 0 degrees
    shadow.set('algn', 'ctr')
    shadow.set('rotWithShape', '0')
    
    srgbClr = etree.SubElement(shadow, qn('a:srgbClr'))
    srgbClr.set('val', '000000')
    alpha = etree.SubElement(srgbClr, qn('a:alpha'))
    alpha.set('val', '40000')  # 100 - 60 = 40% alpha

def _add_reflection_to_text(text_frame):
    """Adds a reflection effect to all text in a text_frame using lxml."""
    p = text_frame._element.xpath('.//a:p')[0]
    for r in p.findall(qn('a:r')):
        rPr = r.find(qn('a:rPr'))
        if rPr is None:
            rPr = etree.SubElement(r, qn('a:rPr'), nsmap=r.nsmap)
        
        effect_list = rPr.find(qn('a:effectLst'))
        if effect_list is None:
            effect_list = etree.SubElement(rPr, qn('a:effectLst'))
            
        # Values from tutorial: Transparency: 45%, Size: 48%, Blur: 0.5pt, Distance: 0pt
        reflection = etree.SubElement(effect_list, qn('a:reflection'))
        reflection.set('blurRad', str(Emu(Pt(0.5)))) # Blur 0.5pt
        reflection.set('stA', '55000')              # Start Alpha (100-45)%
        reflection.set('endA', '1000')              # End Alpha (almost transparent)
        reflection.set('stPos', '0')
        reflection.set('endPos', '48000')           # Size 48%
        reflection.set('dist', '0')                 # Distance 0pt
        reflection.set('dir', '5400000')            # Direction 90 degrees (bottom)
        reflection.set('algn', 'bl')
        reflection.set('rotWithShape', '0')

def create_panoramic_card_reveal(
    output_pptx_path: str,
    title_text: list = ["NEW YEAR", "RESOLUTION"],
    card_data: list = [
        {"number": "1", "label": "HEALTH & WELLNESS"},
        {"number": "2", "label": "PERSONAL GROWTH"},
        {"number": "3", "label": "RELATIONSHIPS"},
        {"number": "4", "label": "CAREER DEVELOPMENT"},
    ],
    bg_keyword: str = "mountains,dawn",
    **kwargs,
) -> str:
    """
    Creates a PPTX with two slides, perfectly set up for a Panoramic Card Reveal
    using the Morph transition.

    The user must open the generated PPTX and apply the 'Morph' transition to the second slide.
    
    Returns: Path to the saved PPTX file.
    """
    prs = Presentation()
    SLIDE_WIDTH = Inches(13.333)
    SLIDE_HEIGHT = Inches(7.5)
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    
    # === Download Background Image ===
    image_stream = None
    try:
        url = f"https://source.unsplash.com/1920x1080/?{bg_keyword}"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        image_stream = BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not download background image ({e}). A fallback will not be used for this effect.")
        # This effect is highly dependent on a background image, so we stop if it fails.
        return None

    # --- Create Slide 1: Start State ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    if image_stream:
        slide1.background.fill.solid() # First set to solid to clear any previous fill
        slide1.background.fill.picture(image_stream)

    # Add Title to Slide 1
    title_y_start = (SLIDE_HEIGHT / 2) - Inches(0.5)
    for i, line in enumerate(title_text):
        tx_box = slide1.shapes.add_textbox(Inches(1), title_y_start + Inches(i * 1.2), SLIDE_WIDTH - Inches(2), Inches(1.2))
        p = tx_box.text_frame.paragraphs[0]
        p.text = line
        p.font.name = "Avenir Next LT Pro"
        p.font.size = Pt(96)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        tx_box.name = f"Title_Line_{i+1}"
        
    # --- Create Slide 2: End State ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    # Reset stream position to reuse image data
    image_stream.seek(0)
    slide2.background.fill.solid()
    slide2.background.fill.picture(image_stream)

    # Move Title Off-Screen on Slide 2
    title_x_end = SLIDE_WIDTH + Inches(1)
    for i, line in enumerate(title_text):
        tx_box = slide2.shapes.add_textbox(title_x_end, title_y_start + Inches(i * 1.2), SLIDE_WIDTH - Inches(2), Inches(1.2))
        p = tx_box.text_frame.paragraphs[0]
        p.text = line
        p.font.name = "Avenir Next LT Pro"
        p.font.size = Pt(96)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        tx_box.name = f"Title_Line_{i+1}"

    # --- Create Card Group on Both Slides ---
    num_cards = len(card_data)
    card_width = SLIDE_WIDTH / num_cards
    
    # Positions
    start_x_offset = -SLIDE_WIDTH
    end_x_offset = 0

    for slide, x_offset in [(slide1, start_x_offset), (slide2, end_x_offset)]:
        card_shapes = []
        for i, data in enumerate(card_data):
            card_left = x_offset + (i * card_width)
            
            # Card Rectangle
            card = slide.shapes.add_shape(1, card_left, 0, card_width, SLIDE_HEIGHT)
            card.line.fill.background() # No line
            _set_slide_background_fill(card)
            _add_shadow_to_shape(card)
            card.name = f"Card_{i+1}"
            
            # Card Number
            num_box = slide.shapes.add_textbox(card_left, Inches(1), card_width, Inches(3))
            p_num = num_box.text_frame.paragraphs[0]
            p_num.text = data["number"]
            p_num.font.name = "Avenir Next LT Pro"
            p_num.font.size = Pt(200)
            p_num.font.color.rgb = RGBColor(255, 255, 255)
            p_num.alignment = PP_ALIGN.CENTER
            _add_reflection_to_text(num_box.text_frame)
            num_box.name = f"CardNumber_{i+1}"

            # Card Label
            lbl_box = slide.shapes.add_textbox(card_left, Inches(4.5), card_width, Inches(1))
            p_lbl = lbl_box.text_frame.paragraphs[0]
            p_lbl.text = data["label"]
            p_lbl.font.name = "Avenir Next LT Pro"
            p_lbl.font.bold = True
            p_lbl.font.size = Pt(18)
            p_lbl.font.color.rgb = RGBColor(255, 255, 255)
            p_lbl.alignment = PP_ALIGN.CENTER
            lbl_box.name = f"CardLabel_{i+1}"

            card_shapes.extend([card, num_box, lbl_box])

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
if __name__ == '__main__':
    output_file = "panoramic_card_reveal.pptx"
    result_path = create_panoramic_card_reveal(output_file)
    if result_path:
        print(f"Presentation saved to {result_path}")
        # To see the effect, open the file and apply the 'Morph' transition to the second slide.
        if os.name == 'nt': # For Windows
            os.startfile(result_path)
        elif os.name == 'posix': # For macOS/Linux
            import subprocess
            subprocess.call(['open', result_path])

