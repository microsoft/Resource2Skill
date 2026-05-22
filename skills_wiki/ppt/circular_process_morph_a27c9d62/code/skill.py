import math
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import PP_ALIGN
from lxml import etree

# Helper function to inject XML for Morph transition
def _set_morph_transition(slide):
    """Adds a Morph transition to the given slide."""
    slide_xml = slide.element
    transition_xml = etree.fromstring(
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:morph/>'
        '</p:transition>'
    )
    slide_xml.insert(2, transition_xml)

def create_slide(
    output_pptx_path: str,
    list_items: list = None,
    primary_color: tuple = (143, 36, 51),
    accent_color: tuple = (45, 62, 114),
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Circular Process Morph visual effect.

    Args:
        output_pptx_path: Path to save the generated PPTX file.
        list_items: A list of dictionaries, each with 'title' and 'description'.
        primary_color: RGB tuple for the main theme color.
        accent_color: RGB tuple for the highlight color.

    Returns:
        Path to the saved PPTX file.
    """
    if list_items is None:
        list_items = [
            {"title": "Earn Your Money", "description": "Money isn't just necessity; it's freedom. Earning wisely, saving smartly, and investing properly bring stability, respect, and peace of mind."},
            {"title": "Solve Your Problem", "description": "A clear goal gives life direction. Without goals, effort is wasted. Small daily steps help turn big dreams into success."},
            {"title": "Aim Your Target", "description": "Daily targets keep focus strong. Completing tasks on time builds confidence and moves you closer to your bigger achievements."},
            {"title": "Get Your Success", "description": "Success never happens suddenly. Continuous effort, patience, and positive thinking transform dreams into reality and create lasting personal growth."},
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # --- Static Element Data ---
    ring_center_x, ring_center_y = Inches(3), Inches(3.75)
    ring_radius_outer = Inches(2.8)
    ring_radius_inner = Inches(1.8)
    icon_radius = ring_radius_outer * 0.85 # Place icons on the ring
    icon_size = Inches(0.6)
    
    # Calculate angles for 4 icons
    num_items = len(list_items)
    angles = [270 + i * (360 / num_items) for i in range(num_items)] # Start from the top
    icon_positions = []
    for angle in angles:
        rad = math.radians(angle)
        x = ring_center_x + icon_radius * math.cos(rad) - icon_size / 2
        y = ring_center_y + icon_radius * math.sin(rad) - icon_size / 2
        icon_positions.append((x, y))

    # --- Slide Creation Loop ---
    slides_data = []
    # Slide 0: The base slide
    slides_data.append({'highlight_index': -1})
    # Subsequent slides, one for each item
    for i in range(num_items):
        slides_data.append({'highlight_index': i})

    for slide_info in slides_data:
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # --- Draw Static Background Elements ---
        # Main Ring
        ring = slide.shapes.add_shape(MSO_SHAPE.DONUT, 
                                      ring_center_x - ring_radius_outer, 
                                      ring_center_y - ring_radius_outer, 
                                      ring_radius_outer * 2, 
                                      ring_radius_outer * 2)
        ring.name = "MainRing"
        # Adjust donut hole size
        adj = ring.adjustments
        adj[0] = ring_radius_inner / ring_radius_outer
        
        fill = ring.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*primary_color)
        ring.line.fill.background()

        # --- Draw Icons (as placeholders) ---
        for i, pos in enumerate(icon_positions):
            icon_shape = slide.shapes.add_shape(MSO_SHAPE.CAN, pos[0], pos[1], icon_size, icon_size)
            icon_shape.rotation = 90 # Orient can shape to look like puzzle piece
            icon_shape.name = f"Icon_{i}"
            icon_fill = icon_shape.fill
            icon_fill.solid()
            icon_fill.fore_color.rgb = RGBColor(255, 255, 255)
            icon_shape.line.fill.background()

        # --- Draw List Items ---
        start_y = Inches(1.5)
        step_y = Inches(1.5)
        for i, item in enumerate(list_items):
            # Number Circle
            circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.2), start_y + i * step_y, Inches(1), Inches(1))
            circ.name = f"NumberCircle_{i}"
            circ_fill = circ.fill
            circ_fill.solid()
            circ_fill.fore_color.rgb = RGBColor(*primary_color)
            circ_fill.transparency = 0.5
            circ.line.fill.background()
            
            tf = circ.text_frame
            tf.text = f"0{i+1}"
            p = tf.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(32)
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.alignment = PP_ALIGN.CENTER
            
            # Title Rectangle
            rect = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7), start_y + i * step_y + Inches(0.125), Inches(5), Inches(0.75))
            rect.name = f"TitleRect_{i}"
            rect_fill = rect.fill
            rect_fill.solid()
            rect_fill.fore_color.rgb = RGBColor(*primary_color)
            rect.line.fill.background()

            tf_rect = rect.text_frame
            tf_rect.text = item['title']
            p_rect = tf_rect.paragraphs[0]
            p_rect.font.bold = True
            p_rect.font.size = Pt(24)
            p_rect.font.color.rgb = RGBColor(255, 255, 255)
            p_rect.vertical_anchor = PP_ALIGN.CENTER
        
        # --- Draw DYNAMIC Elements for the specific slide ---
        h_index = slide_info['highlight_index']
        if h_index != -1:
            # Add Morph Transition to all slides after the first
            _set_morph_transition(slide)

            # Highlight Wedge
            start_angle = (angles[h_index] - 45) * 64000
            end_angle = (angles[h_index] + 45) * 64000
            
            # Create a pie shape that covers the segment
            pie_wedge = slide.shapes.add_shape(MSO_SHAPE.PIE,
                                              ring_center_x - ring_radius_outer,
                                              ring_center_y - ring_radius_outer,
                                              ring_radius_outer * 2,
                                              ring_radius_outer * 2)
            pie_wedge.name = "HighlightWedge"
            pie_wedge.adjustments[0] = start_angle
            pie_wedge.adjustments[1] = end_angle
            
            pie_fill = pie_wedge.fill
            pie_fill.solid()
            pie_fill.fore_color.rgb = RGBColor(*accent_color)
            pie_wedge.line.fill.background()

            # Ensure wedge is behind the icons but on top of the ring
            pie_wedge_xml = pie_wedge.element
            ring_xml = ring.element
            ring_xml.addnext(pie_wedge_xml)

            # Description Box
            desc_y = start_y + h_index * step_y + Inches(1.0)
            desc_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7), desc_y, Inches(5), Inches(1.5))
            desc_box.name = f"DescriptionBox_{h_index}"
            desc_fill = desc_box.fill
            desc_fill.solid()
            desc_fill.fore_color.rgb = RGBColor(*primary_color)
            desc_fill.transparency = 0.5
            desc_box.line.fill.background()

            tf_desc = desc_box.text_frame
            tf_desc.text = list_items[h_index]['description']
            p_desc = tf_desc.paragraphs[0]
            p_desc.font.size = Pt(14)
            p_desc.font.color.rgb = RGBColor(255, 255, 255)
            p_desc.alignment = PP_ALIGN.LEFT
            tf_desc.margin_left = Inches(0.2)
            tf_desc.margin_right = Inches(0.2)
            tf_desc.word_wrap = True


    prs.save(output_pptx_path)
    return output_pptx_path

