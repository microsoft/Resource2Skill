import os
import math
import tempfile
from lxml import etree
from typing import List, Tuple

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.part import XmlPart

from PIL import Image, ImageDraw


def _get_element_by_class_name(element, class_name):
    """Helper to find an element by its p:cNvPr name attribute."""
    for child in element.iter():
        if child.tag.endswith('cNvPr') and child.get('name') == class_name:
            return child.getparent().getparent().getparent() # Return the <p:sp> element
    return None

def _add_shadow_effect(shape, shadow_type='inner', blur_rad=63500, dist=25400, direction=2700000, color='000000', alpha=40000):
    """Adds an inner or outer shadow effect to a shape using lxml."""
    sp = shape.element
    spPr = sp.xpath('./p:spPr')[0]

    # Ensure <a:effectLst> exists
    effectLst = spPr.find(f'.//{'{http://schemas.openxmlformats.org/drawingml/2006/main}'}effectLst')
    if effectLst is None:
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')

    # Add the shadow element
    shadow_tag = '{http://schemas.openxmlformats.org/drawingml/2006/main}' + ('innerShdw' if shadow_type == 'inner' else 'outerShdw')
    shadow = etree.SubElement(effectLst, shadow_tag,
                              blurRad=str(blur_rad), dist=str(dist), dir=str(direction))
    
    srgbClr = etree.SubElement(shadow, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val=color)
    etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val=str(alpha))


def _set_morph_transition(slide):
    """Sets the morph transition for a slide using lxml."""
    slide_part = slide.part
    # Define the transition XML content
    transition_xml = f'''
        <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" advTm="1000">
            <p:morph transition="byObject"/>
        </p:transition>
    '''.strip()
    # Create a new XML part for the transition
    part = XmlPart.new(
        'application/vnd.openxmlformats-officedocument.presentationml.transition+xml',
        transition_xml.encode('utf-8')
    )
    # Relate the slide part to the new transition part
    slide_part.relate_to(part, RT.TRANSITION)


def create_link_image(width_px: int, height_px: int, color: Tuple[int, int, int]) -> str:
    """
    Creates the custom link shape using PIL and saves it as a temporary PNG file.
    """
    img = Image.new('RGBA', (width_px, height_px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    node_radius = height_px // 2
    
    # 1. Draw the main body (rectangle + two end circles)
    # Rectangle
    draw.rectangle([node_radius, 0, width_px - node_radius, height_px], fill=(255, 255, 255, 255))
    # Left circle
    draw.ellipse([0, 0, height_px, height_px], fill=(255, 255, 255, 255))
    # Right circle
    draw.ellipse([width_px - height_px, 0, width_px, height_px], fill=(255, 255, 255, 255))

    # 2. Draw the concave curves using two large chord shapes
    # These chords "add" to the shape to create the curved sides
    chord_height = int(height_px * 4)
    chord_bbox_top = [node_radius, -chord_height + height_px/2, width_px - node_radius, height_px/2]
    chord_bbox_bottom = [node_radius, height_px/2, width_px - node_radius, chord_height + height_px/2]

    draw.chord(chord_bbox_top, 180, 360, fill=(255, 255, 255, 255))
    draw.chord(chord_bbox_bottom, 0, 180, fill=(255, 255, 255, 255))

    # 3. Colorize the final shape
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i, j][3] > 0: # If pixel is not transparent
                pixels[i, j] = color + (255,)

    # Save to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp_file.name)
    return temp_file.name

def create_slide(
    output_pptx_path: str,
    title_text: str = "6 Steps Material Design Hexagonal Infographics",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Material Design Linked Hexagon Infographic.

    This function generates a two-slide presentation:
    - Slide 1: The "before" state with infographic elements scattered.
    - Slide 2: The final assembled infographic with a Morph transition applied.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Initial state for Morph
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Slide 2: Final Layout
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Set background color for both slides
    for slide in [slide1, slide2]:
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(230, 230, 230)

    # --- Define Geometry and Colors ---
    slide_center_x = prs.slide_width / 2
    slide_center_y = prs.slide_height / 2
    hexagon_radius = Inches(2.0)
    node_diameter = Inches(0.8)

    # Calculate distance between hexagon vertices for link length
    p1 = (hexagon_radius * math.cos(math.radians(0)), hexagon_radius * math.sin(math.radians(0)))
    p2 = (hexagon_radius * math.cos(math.radians(60)), hexagon_radius * math.sin(math.radians(60)))
    link_length = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    link_height = node_diameter * 0.8  # Make links slightly thinner than nodes
    
    colors = [
        (237, 28, 36),   # Red
        (112, 48, 160),  # Purple
        (0, 32, 96),     # Dark Blue
        (0, 176, 240),   # Cyan
        (255, 192, 0),   # Yellow
        (255, 124, 0),   # Orange
    ]

    # --- Build Final Layout on Slide 2 ---
    final_shapes = []
    link_image_files = []
    
    for i in range(6):
        # 1. Create and add the colored link image
        angle_start_deg = i * 60
        angle_end_deg = (i + 1) * 60
        angle_mid_deg = (angle_start_deg + angle_end_deg) / 2
        
        # Calculate center position for the link
        pos_x = slide_center_x + (hexagon_radius * math.cos(math.radians(angle_mid_deg))) - (link_length / 2)
        pos_y = slide_center_y + (hexagon_radius * math.sin(math.radians(angle_mid_deg))) - (link_height / 2)
        
        link_image_path = create_link_image(int(link_length * 96 / 914400), int(link_height * 96/ 914400), colors[i])
        link_image_files.append(link_image_path)
        
        link_pic = slide2.shapes.add_picture(
            link_image_path, pos_x, pos_y, width=link_length, height=link_height
        )
        link_pic.rotation = angle_mid_deg
        link_pic.name = f"link_{i}"
        final_shapes.append(link_pic)

        # 2. Add the two white nodes (circles) for this link
        for j in range(2):
            angle_deg = (i + j) * 60
            node_x = slide_center_x + (hexagon_radius * math.cos(math.radians(angle_deg))) - (node_diameter / 2)
            node_y = slide_center_y + (hexagon_radius * math.sin(math.radians(angle_deg))) - (node_diameter / 2)
            
            # Check if this node already exists to avoid duplicates
            node_name = f"node_{(i+j)%6}"
            if not any(s.name == node_name for s in final_shapes):
                node = slide2.shapes.add_shape(
                    MSO_SHAPE.OVAL, node_x, node_y, node_diameter, node_diameter
                )
                node.name = node_name
                node.fill.solid()
                node.fill.fore_color.rgb = RGBColor(255, 255, 255)
                node.line.fill.background()
                
                # Add inner shadow using lxml helper
                _add_shadow_effect(node, shadow_type='inner', direction=31500000) # Top-left shadow
                final_shapes.append(node)

    # --- Add Title and Step Text to Slide 2 ---
    title_shape = slide2.shapes.add_textbox(Inches(0), Inches(0.2), prs.slide_width, Inches(0.8))
    title_shape.text = title_text
    p = title_shape.text_frame.paragraphs[0]
    p.font.name = 'Calibri (Body)'
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(89, 89, 89)
    p.alignment = 1 # Center align

    # --- Duplicate shapes to Slide 1 in scattered positions for Morph ---
    from copy import deepcopy
    for shape in slide2.shapes:
        new_el = deepcopy(shape.element)
        slide1.shapes._spTree.insert_element_before(new_el, 'p:extLst')

    # Reposition and rotate shapes on slide 1
    _get_element_by_class_name(slide1.shapes.element, 'link_0').rotation = 90
    _get_element_by_class_name(slide1.shapes.element, 'link_0').left = Inches(1)
    
    _get_element_by_class_name(slide1.shapes.element, 'link_1').rotation = -45
    _get_element_by_class_name(slide1.shapes.element, 'link_1').left = Inches(10)
    _get_element_by_class_name(slide1.shapes.element, 'link_1').top = Inches(5)
    # (...add more random positions for other shapes for a more dramatic effect)
    
    # --- Apply Morph Transition to Slide 2 ---
    _set_morph_transition(slide2)

    # --- Cleanup and Save ---
    for file_path in link_image_files:
        os.remove(file_path)

    prs.save(output_pptx_path)
    return output_pptx_path

