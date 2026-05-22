import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml.xmlchemy import OxmlElement
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml import parse_xml
from lxml import etree
from PIL import Image, ImageDraw

# Helper function to add a Morph transition using lxml
def add_morph_transition(slide):
    """Adds a Morph transition to the given slide."""
    transition_xml = f"""
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" advTm="1000">
        <p:morph/>
    </p:transition>
    """
    transition_element = parse_xml(transition_xml)
    slide.element.insert(2, transition_element)

def create_person_icon_png(size, color, output_path):
    """Creates a PNG image of a simple person icon."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    head_radius = size[0] * 0.25
    head_center_x = size[0] / 2
    head_center_y = head_radius + 5
    
    body_top = head_center_y + head_radius
    body_width = size[0] * 0.9
    body_height = size[1] - body_top - 5
    
    # Head
    draw.ellipse(
        (head_center_x - head_radius, head_center_y - head_radius, 
         head_center_x + head_radius, head_center_y + head_radius),
        fill=color
    )
    # Body
    draw.rounded_rectangle(
        (head_center_x - body_width/2, body_top, head_center_x + body_width/2, body_top + body_height),
        radius=10, fill=color
    )
    
    img.save(output_path)
    return output_path

def create_slide(
    output_pptx_path: str,
    percentage: int = 70,
    accent_color_main: tuple = (111, 68, 220),
    accent_color_subtle: tuple = (218, 208, 246),
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Icon Array Infographic with a Morph transition.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        percentage: The percentage to visualize (0-100).
        accent_color_main: RGB tuple for the highlighted icons.
        accent_color_subtle: RGB tuple for the de-emphasized icons.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    
    # --- Create Icon Assets ---
    icon_size = (50, 80)
    
    # Opaque Icon
    main_color_rgba = accent_color_main + (255,)
    opaque_icon_path = "person_opaque.png"
    create_person_icon_png(icon_size, main_color_rgba, opaque_icon_path)

    # Transparent Icon (using a different RGB for better visibility as in video)
    subtle_color_rgba = accent_color_subtle + (255,)
    transparent_icon_path = "person_transparent.png"
    create_person_icon_png(icon_size, subtle_color_rgba, transparent_icon_path)

    # --- Slide 1: Combined View ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])

    # Background Gradient
    fill = slide1.background.fill
    fill.gradient()
    fill.gradient_stops[0].color.rgb = RGBColor(245, 245, 245)
    fill.gradient_stops[1].color.rgb = RGBColor(230, 230, 230)

    total_icons = 100
    rows, cols = 5, 20
    icon_w, icon_h = Inches(0.4), Inches(0.6)
    grid_w = cols * icon_w
    start_x = (prs.slide_width - grid_w) / 2
    start_y = Inches(1.5)

    for i in range(total_icons):
        row = i // cols
        col = i % cols
        left = start_x + col * icon_w
        top = start_y + row * icon_h
        
        icon_path = opaque_icon_path if i < percentage else transparent_icon_path
        pic = slide1.shapes.add_picture(icon_path, left, top, width=icon_w, height=icon_h)
        pic.name = f"icon_{i}"

    # Text elements for Slide 1
    tx_box = slide1.shapes.add_textbox(Inches(1), Inches(5.5), Inches(3), Inches(1.5))
    p = tx_box.text_frame.paragraphs[0]
    p.text = f"{percentage}%"
    p.font.name = "Montserrat ExtraBold"
    p.font.size = Pt(96)
    p.font.color.rgb = RGBColor(*accent_color_main)
    
    tx_box_body = slide1.shapes.add_textbox(Inches(4), Inches(5.8), Inches(6), Inches(1.5))
    tx_box_body.text_frame.text = "LOREM IPSUM DOLOR\n"
    p_body = tx_box_body.text_frame.paragraphs[0]
    p_body.font.name = 'Montserrat SemiBold'
    p_body.font.size = Pt(18)
    p_body.font.color.rgb = RGBColor(80, 80, 80)
    
    p_sub = tx_box_body.text_frame.add_paragraph()
    p_sub.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    p_sub.font.name = 'Montserrat'
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = RGBColor(120, 120, 120)

    # --- Slide 2: Split View ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    slide2.background.fill.solid()
    slide2.background.fill.fore_color.rgb = RGBColor(245, 245, 245)

    num_groups = 4
    group_cols, group_rows = 5, 5
    icons_per_group = group_cols * group_rows
    group_spacing = Inches(1)
    total_group_width = num_groups * (group_cols * icon_w) + (num_groups - 1) * group_spacing
    group_start_x = (prs.slide_width - total_group_width) / 2
    
    for i in range(total_icons):
        group_num = i // icons_per_group
        index_in_group = i % icons_per_group
        
        row = index_in_group // group_cols
        col = index_in_group % group_cols
        
        left = group_start_x + group_num * ((group_cols * icon_w) + group_spacing) + col * icon_w
        top = start_y + row * icon_h

        icon_path = opaque_icon_path if i < percentage else transparent_icon_path
        pic = slide2.shapes.add_picture(icon_path, left, top, width=icon_w, height=icon_h)
        pic.name = f"icon_{i}" # Critical: Name must match slide 1

    # Add titles for groups
    for g in range(num_groups):
        title_left = group_start_x + g * ((group_cols * icon_w) + group_spacing)
        title_width = group_cols * icon_w
        tx_box_title = slide2.shapes.add_textbox(title_left, start_y - Inches(0.5), title_width, Inches(0.5))
        p_title = tx_box_title.text_frame.paragraphs[0]
        p_title.text = f"GROUP {g+1}"
        p_title.font.name = 'Montserrat SemiBold'
        p_title.font.size = Pt(14)
        p_title.font.color.rgb = RGBColor(80, 80, 80)

    # Apply Morph Transition to Slide 2
    add_morph_transition(slide2)
    
    # --- Clean up temporary files ---
    os.remove(opaque_icon_path)
    os.remove(transparent_icon_path)
    
    prs.save(output_pptx_path)
    return output_pptx_path
