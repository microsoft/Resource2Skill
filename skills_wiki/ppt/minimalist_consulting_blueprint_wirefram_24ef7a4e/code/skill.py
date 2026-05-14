import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_slide(
    output_pptx_path: str,
    title_text: str = "Systemic Failure Analysis",
    subtitle_text: str = "Deconstructing communication bottlenecks in high-performance teams.",
    body_text: str = "• Lack of a unified communication blueprint leads to fragmented efforts.\n\n• The issue is structural, not interpersonal. Without clear protocols, informal channels become overwhelmed.\n\n• Implementing a rigid, yet adaptable framework creates a solid foundation for collaborative success.",
    accent_color: tuple = (160, 40, 40),  # Brick Red
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Minimalist Consulting Blueprint" style.
    Features strict grid layouts, thin divider lines, and a programmatic wireframe graphic.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Colors
    charcoal = RGBColor(30, 30, 30)
    gray = RGBColor(100, 100, 100)
    accent = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    bg_color = RGBColor(250, 250, 250) # Off-white background

    # --- Set Slide Background ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = bg_color

    # --- Left Column: Typography & Content ---
    
    # 1. Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.5), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = 'Arial'
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = charcoal

    # 2. Accent Divider Line
    line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, Inches(1.0), Inches(2.6), Inches(2.5), Inches(2.6)
    )
    line.line.color.rgb = accent
    line.line.width = Pt(2.0)

    # 3. Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(5.5), Inches(0.8))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = 'Georgia' # Serif for elegant contrast
    p_sub.font.size = Pt(18)
    p_sub.font.italic = True
    p_sub.font.color.rgb = gray

    # 4. Body Text
    body_box = slide.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(5.0), Inches(2.5))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.name = 'Arial'
    p_body.font.size = Pt(14)
    p_body.font.color.rgb = charcoal
    # Adjust line spacing for breathability
    p_body.line_spacing = 1.5

    # --- Right Column: Programmatic Wireframe/Blueprint Graphic ---
    # We will generate a "System Node / Orbit" line-art diagram to match the style
    
    center_x = Inches(9.5)
    center_y = Inches(3.75)
    
    # Base configuration for blueprint lines
    def format_blueprint_shape(shape, is_dashed=False, is_accent=False):
        shape.fill.background() # No fill (transparent)
        line = shape.line
        line.color.rgb = accent if is_accent else charcoal
        line.width = Pt(1.0)
        if is_dashed:
            line.dash_style = 7 # msoLineDash
            
    # Outer Orbit
    outer_radius = Inches(2.5)
    outer_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, center_x - outer_radius, center_y - outer_radius, outer_radius*2, outer_radius*2
    )
    format_blueprint_shape(outer_circle)

    # Inner Orbit
    inner_radius = Inches(1.5)
    inner_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, center_x - inner_radius, center_y - inner_radius, inner_radius*2, inner_radius*2
    )
    format_blueprint_shape(inner_circle, is_dashed=True)

    # Core Node (Filled)
    core_radius = Inches(0.4)
    core_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, center_x - core_radius, center_y - core_radius, core_radius*2, core_radius*2
    )
    core_circle.fill.solid()
    core_circle.fill.fore_color.rgb = charcoal
    core_circle.line.fill.background()

    # Intersecting structural lines
    v_line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, center_x, center_y - outer_radius - Inches(0.5), center_x, center_y + outer_radius + Inches(0.5)
    )
    format_blueprint_shape(v_line)
    
    h_line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, center_x - outer_radius - Inches(0.5), center_y, center_x + outer_radius + Inches(0.5), center_y
    )
    format_blueprint_shape(h_line)

    # Add satellite nodes on the inner orbit
    node_coords = [
        (center_x, center_y - inner_radius), # Top
        (center_x, center_y + inner_radius), # Bottom
        (center_x - inner_radius, center_y), # Left
        (center_x + inner_radius, center_y), # Right
    ]
    
    small_node_rad = Inches(0.1)
    for i, (nx, ny) in enumerate(node_coords):
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, nx - small_node_rad, ny - small_node_rad, small_node_rad*2, small_node_rad*2
        )
        node.fill.solid()
        # Make one node the accent color
        node.fill.fore_color.rgb = accent if i == 0 else bg_color
        node.line.color.rgb = charcoal
        node.line.width = Pt(1.5)

    # Add a structural floating box (Consulting aesthetic touch)
    box_w, box_h = Inches(2.0), Inches(0.6)
    float_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, center_x + Inches(1.0), center_y - Inches(2.8), box_w, box_h
    )
    float_box.fill.solid()
    float_box.fill.fore_color.rgb = bg_color
    float_box.line.color.rgb = charcoal
    float_box.line.width = Pt(0.75)
    
    tf_box = float_box.text_frame
    p_box = tf_box.paragraphs[0]
    p_box.text = "FIG 01: SYSTEM ARCH"
    p_box.font.name = 'Arial'
    p_box.font.size = Pt(9)
    p_box.font.bold = True
    p_box.font.color.rgb = charcoal
    p_box.alignment = PP_ALIGN.CENTER

    # --- Footer Structure ---
    footer_line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, Inches(1.0), Inches(6.8), Inches(12.333), Inches(6.8)
    )
    footer_line.line.color.rgb = charcoal
    footer_line.line.width = Pt(0.5)

    footer_box = slide.shapes.add_textbox(Inches(1.0), Inches(6.9), Inches(4.0), Inches(0.4))
    tf_foot = footer_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "STRATEGIC COMMUNICATION BLUEPRINT"
    p_foot.font.name = 'Arial'
    p_foot.font.size = Pt(8)
    p_foot.font.color.rgb = gray

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("blueprint_style_slide.pptx")
