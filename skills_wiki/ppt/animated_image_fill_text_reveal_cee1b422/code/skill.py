import os
import requests
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

# Helper function to create namespace-prefixed XML element names
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified name for lxml.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return f'{{{uri}}}{tagroot}'

def create_animated_image_fill_text_slide(
    output_pptx_path: str,
    title_text: str = "WELCOME",
    subtitle_text: str = "TO OUR PRESENTATION",
    image_url_1: str = "https://images.unsplash.com/photo-1444090542259-0af8fa96557e?w=1200",
    image_url_2: str = "https://images.unsplash.com/photo-1519996236531-f8a018a13a24?w=1200",
) -> str:
    """
    Creates a two-slide PowerPoint presentation demonstrating the Animated
    Image-Fill Text Reveal effect.

    A "Wipe" transition is applied to the second slide to create the animation.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_text: The main text to be filled with an image.
        subtitle_text: The subtitle text.
        image_url_1: URL for the initial image fill.
        image_url_2: URL for the revealed image fill.

    Returns:
        The path to the saved .pptx file.
    """
    
    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Image Handling ---
    def get_image_stream(url, fallback_text):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.exceptions.RequestException:
            print(f"Warning: Could not download image from {url}. Using a fallback.")
            img = Image.new('RGB', (1200, 800), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except IOError:
                font = ImageFont.load_default()
            d.text((10,10), fallback_text, fill=(255,255,0), font=font)
            img_stream = BytesIO()
            img.save(img_stream, format='PNG')
            img_stream.seek(0)
            return img_stream

    img_stream_1 = get_image_stream(image_url_1, "Image 1 Failed")
    img_stream_2 = get_image_stream(image_url_2, "Image 2 Failed")

    # Add images to the presentation package to get their relationship IDs (rId)
    # Note: add_image_part is a method of the slide's part, not the slide itself.
    # We create a dummy slide to get access to the part, then delete it.
    temp_slide = prs.slides.add_slide(blank_layout)
    slide_part = temp_slide.part
    rId1 = slide_part.relate_to(slide_part.package.image_parts.get_or_add(img_stream_1), 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image').rId
    rId2 = slide_part.relate_to(slide_part.package.image_parts.get_or_add(img_stream_2), 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image').rId
    
    # Delete the temporary slide
    r_to_delete = prs.slides._sldIdLst[0]
    prs.slides._sldIdLst.remove(r_to_delete)

    # --- Helper function for XML manipulations ---
    def apply_text_effects(textbox, rId, shadow=True, char_spacing_pt=None):
        txBody = textbox._element.get_or_add_txBody()
        p = txBody.find(qn('a:p'))
        r = p.find(qn('a:r'))
        rPr = r.get_or_add_rPr()

        # Remove solid fill
        solid_fill = rPr.find(qn('a:solidFill'))
        if solid_fill is not None:
            rPr.remove(solid_fill)

        # Add picture fill
        blip_fill = etree.SubElement(rPr, qn('a:blipFill'))
        blip = etree.SubElement(blip_fill, qn('a:blip'), {qn('r:embed'): rId})
        stretch = etree.SubElement(blip_fill, qn('a:stretch'))
        etree.SubElement(stretch, qn('a:fillRect'))

        # Add shadow effect
        if shadow:
            effect_list = etree.SubElement(rPr, qn('a:effectLst'))
            # Perspective Upper Right Shadow
            outer_shadow = etree.SubElement(effect_list, qn('a:outerShdw'), {
                'blurRad': '76200', 'dist': '76200', 'dir': '2700000', 'rotWithShape': '0'
            })
            shadow_color = etree.SubElement(outer_shadow, qn('a:srgbClr'), {'val': '000000'})
            etree.SubElement(shadow_color, qn('a:alpha'), {'val': '40000'})

        # Add character spacing
        if char_spacing_pt:
            # 1 point = 100 in XML. Value is in 1/100ths of a point.
            rPr.set('spc', str(int(char_spacing_pt * 100)))

    # --- Function to build a single slide ---
    def build_slide(rId):
        slide = prs.slides.add_slide(blank_layout)

        # Background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(231, 231, 231)

        # Title
        left, top, width, height = Inches(0), Inches(2.25), prs.slide_width, Inches(3)
        title_box = slide.shapes.add_textbox(left, top, width, height)
        tf = title_box.text_frame
        tf.clear()
        tf.word_wrap = False
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = title_text
        font = run.font
        font.name = 'Arial Black'
        font.size = Pt(150)
        font.bold = True
        
        apply_text_effects(title_box, rId, shadow=True)

        # Subtitle
        left, top = Inches(0), Inches(4.75)
        subtitle_box = slide.shapes.add_textbox(left, top, prs.slide_width, Inches(1))
        tf = subtitle_box.text_frame
        tf.clear()
        tf.word_wrap = False
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = subtitle_text
        font = run.font
        font.name = 'Arial'
        font.size = Pt(20)
        font.color.rgb = RGBColor(101, 67, 33)

        apply_text_effects(subtitle_box, rId, shadow=False, char_spacing_pt=15)
        
        return slide

    # --- Create the two slides ---
    slide1 = build_slide(rId1)
    slide2 = build_slide(rId2)
    
    # --- Add Wipe Transition to the Second Slide ---
    slide2_part = slide2.part
    sld = slide2_part.element
    # Find or create the transition element
    transition = sld.find(qn('p:transition'))
    if transition is None:
        transition = etree.SubElement(sld, qn('p:transition'), {
            'spd': 'slow', 'advClick': '0'
        })
    else: # Clear existing transition effects
        for child in list(transition):
            transition.remove(child)

    # Add wipe effect: dir="r" in XML corresponds to "Wipe From Left" in UI
    wipe = etree.SubElement(transition, qn('p:wipe'), {'dir': 'r'})
    
    # --- Save Presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path

# --- Example Usage ---
if __name__ == '__main__':
    output_filename = "animated_image_fill_text.pptx"
    create_animated_image_fill_text_slide(output_filename)
    print(f"Presentation saved to {output_filename}")
    # On Windows, you can open it automatically
    if os.name == 'nt':
        os.startfile(output_filename)

