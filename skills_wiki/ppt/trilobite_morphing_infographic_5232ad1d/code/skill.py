import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree
import urllib.request
from io import BytesIO

# Helper functions for XML manipulation
def _get_shape_element(shape):
    return shape.element

def _get_or_create_spPr(shape_element):
    spPr = shape_element.find('.//p:spPr', namespaces=shape_element.nsmap)
    if spPr is None:
        spPr = etree.SubElement(shape_element, '{' + shape_element.nsmap['p'] + '}spPr')
    return spPr

def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return '{%s}%s' % (uri, tagroot)

def add_inner_shadow(shape, color_rgb, blur_radius, distance, direction):
    spPr = _get_or_create_spPr(shape.element)
    effect_list = spPr.find(qn('a:effectLst'))
    if effect_list is None:
        effect_list = etree.SubElement(spPr, qn('a:effectLst'))

    shadow_el = etree.SubElement(effect_list, qn('a:innerShdw'), {
        'blurRad': str(blur_radius),
        'dist': str(distance),
        'dir': str(direction),
    })
    color_el = etree.SubElement(shadow_el, qn('a:srgbClr'), {'val': '%02x%02x%02x' % color_rgb})
    etree.SubElement(color_el, qn('a:alpha'), {'val': '100000'}) # 100%

def add_drop_shadow(shape, color_rgb=(0, 0, 0), transparency=60, blur_radius=25, distance=12, direction=5400000):
    spPr = _get_or_create_spPr(shape.element)
    effect_list = spPr.find(qn('a:effectLst'))
    if effect_list is None:
        effect_list = etree.SubElement(spPr, qn('a:effectLst'))

    shadow_el = etree.SubElement(effect_list, qn('a:outerShdw'), {
        'blurRad': str(blur_radius), 'dist': str(distance), 'dir': str(direction), 'algn': 'bl', 'rotWithShape': '0'
    })
    color_el = etree.SubElement(shadow_el, qn('a:srgbClr'), {'val': '%02x%02x%02x' % color_rgb})
    alpha_val = str(int((100 - transparency) * 1000))
    etree.SubElement(color_el, qn('a:alpha'), {'val': alpha_val})

def set_morph_transition(slide):
    slide_xml = slide.element
    transition = etree.SubElement(slide_xml, qn('p:transition'), {'advClick': "0"})
    etree.SubElement(transition, qn('p:morph'))

def create_trilobite_infographic(
    output_pptx_path: str,
    title_text: str = "COVID",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Trilobite Morphing Infographic effect.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_text: The main title for the presentation.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Emu(12192000)  # 16:9 aspect ratio
    prs.slide_height = Emu(6858000)
    blank_slide_layout = prs.slide_layouts[6]

    # --- Slide Data ---
    slide_data = [
        {
            "text": "YOUR TEXT HERE1:",
            "image_url": "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?w=800",
            "image_keyword": "virus"
        },
        {
            "text": "YOUR TEXT HERE2:",
            "image_url": "https://images.unsplash.com/photo-1584470352504-b94f4a3403a2?w=800",
            "image_keyword": "face mask"
        },
        {
            "text": "YOUR TEXT HERE3:",
            "image_url": "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=800",
            "image_keyword": "medical research"
        }
    ]
    
    # --- Title Slide ---
    slide = prs.slides.add_slide(blank_slide_layout)
    # Background
    bg_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height / 2)
    bg_top.fill.solid()
    bg_top.fill.fore_color.rgb = RGBColor(1, 22, 56)
    bg_top.line.fill.background()
    
    bg_bottom = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, prs.slide_height / 2, prs.slide_width, prs.slide_height / 2)
    bg_bottom.fill.solid()
    bg_bottom.fill.fore_color.rgb = RGBColor(27, 117, 187)
    bg_bottom.line.fill.background()
    
    # Title Text
    textbox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.33), Inches(2.5))
    text_frame = textbox.text_frame
    p = text_frame.paragraphs[0]
    p.text = "INFOGRAPHIC\nPOWERPOINT"
    p.font.name = 'Arial Black'
    p.font.size = Pt(80)
    p.font.color.rgb = RGBColor(122, 212, 240)
    

    # --- Create Morphing Slides ---
    
    # Create the image strip group once
    image_group_height = Inches(4.0)
    image_group_width = Inches(3.2)
    
    # This group shape will act as a container for our images
    image_group_shape = prs.slides.add_slide(blank_slide_layout).shapes.add_group_shape()
    prs.slides.remove(prs.slides[-1]) # remove temporary slide

    for i, data in enumerate(slide_data):
        try:
            with urllib.request.urlopen(data["image_url"]) as response:
                image_stream = BytesIO(response.read())
                image_group_shape.shapes.add_picture(
                    image_stream, Inches(0), Inches(i * 4.2), 
                    width=image_group_width, height=image_group_height
                )
        except Exception:
            # Fallback if image download fails
            rect = image_group_shape.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(i*4.2), width=image_group_width, height=image_group_height)
            rect.fill.solid(); rect.fill.fore_color.rgb = RGBColor(200, 200, 200)
            rect.line.fill.background()

    for i in range(len(slide_data)):
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # Add background rectangles
        bg_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height / 2)
        bg_top.fill.solid(); bg_top.fill.fore_color.rgb = RGBColor(1, 22, 56)
        bg_top.line.fill.background()
        bg_bottom = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, prs.slide_height / 2, prs.slide_width, prs.slide_height / 2)
        bg_bottom.fill.solid(); bg_bottom.fill.fore_color.rgb = RGBColor(27, 117, 187)
        bg_bottom.line.fill.background()

        # Main content container
        container = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.25), Inches(11), Inches(5))
        container.fill.gradient()
        container.fill.gradient_stops[0].color.rgb = RGBColor(27, 117, 187)
        container.fill.gradient_stops[1].color.rgb = RGBColor(122, 212, 240)
        container.line.fill.background()
        add_drop_shadow(container)

        # Infographic Shape (as a group)
        infographic_group = slide.shapes.add_group_shape()
        infographic_group.left = Inches(1.2)
        infographic_group.top = Inches(1.6)
        infographic_group.width = Inches(4.25)
        infographic_group.height = Inches(4.25)
        infographic_group.rotation = 120 * i

        # Add trilobite lobes to the group
        # This is complex geometry derived from fragmenting circles
        lobe_paths = [
            # Path 1 (Top Lobe)
            "M 2125,0 C 3298,0 4250,952 4250,2125 C 4250,3298 3298,4250 2125,4250 C 1545,4250 1024,3947 640,3443 C 1205,2633 1205,1617 640,807 C 1024,303 1545,0 2125,0 Z",
        ]
        
        for j in range(3):
            freeform = infographic_group.shapes.add_freeform_builder(
                x=0, y=0, width=Emu(4250), height=Emu(4250)
            )
            freeform.path(lobe_paths[0])
            shape = freeform.convert_to_shape()
            shape.rotation = 120 * j
            shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
            shape.line.fill.background()
            add_inner_shadow(shape, (122, 212, 240), blur_radius=Pt(60), distance=0, direction=0)
        
        # Text and icons (add to the same group)
        icons = ["LUNGS", "SEARCH", "MICROSCOPE"]
        texts = ["RESULT", "RESEARCH", "DATA ANALYSIS"]
        positions = [(1.3, 0.7), (2.7, 2.1), (0, 2.1)] # in Inches relative to group
        
        for j in range(3):
            icon_shape = infographic_group.shapes.add_textbox(Inches(positions[j][0]), Inches(positions[j][1]), Inches(1), Inches(1))
            icon_shape.text = texts[j] # Use text as placeholder for icons
            icon_shape.text_frame.paragraphs[0].font.bold = True
            icon_shape.text_frame.paragraphs[0].font.size = Pt(12)
            icon_shape.rotation = - (120 * i) # Counter-rotate text to keep it upright
        
        # Add side panel and images
        slide.shapes._spTree.insert(2, image_group_shape.element)
        image_group_shape.left = Inches(9.2)
        image_group_shape.top = Inches(1.75) - Inches(i * 4.2)
        
        # Add descriptive text
        text_container = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(2.2), Inches(3.2), Inches(3))
        text_container.fill.background()
        text_container.line.solid(); text_container.line.color.rgb = RGBColor(255,255,255)
        text_container.text_frame.text = f"{slide_data[i]['text']}\n\nNature is an integral part of our lives. It is the source of all life on earth and it is the most beautiful thing that we can ever witness."
        
        set_morph_transition(slide)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to call the function
if __name__ == '__main__':
    create_trilobite_infographic("trilobite_infographic.pptx")
