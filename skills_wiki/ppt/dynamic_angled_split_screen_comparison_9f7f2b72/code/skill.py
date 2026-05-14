import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

def apply_pattern_fill(shape, prst="lgGrid", fg_hex="FFFFFF", bg_hex="000000"):
    """
    Injects OpenXML to apply a native PowerPoint Pattern Fill to a shape.
    prst options: 'pct5', 'pct10', 'lgGrid', 'smGrid', 'diagCross', etc.
    """
    spPr = shape.element.spPr
    # Remove existing fill types
    for child in list(spPr):
        if child.tag.endswith('Fill'):
            spPr.remove(child)
    
    # Create the pattern fill XML
    patt_fill_xml = f"""
    <a:pattFill prst="{prst}" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:fgClr><a:srgbClr val="{fg_hex}"/></a:fgClr>
        <a:bgClr><a:srgbClr val="{bg_hex}"/></a:bgClr>
    </a:pattFill>
    """
    pattFill = parse_xml(patt_fill_xml)
    spPr.append(pattFill)

def apply_transparent_line(shape, rgb_color, alpha_pct=30):
    """
    Sets a line color and injects an alpha value for transparency via OpenXML.
    """
    shape.line.color.rgb = rgb_color
    shape.line.width = Pt(1)
    
    # Find the newly created srgbClr element and append alpha
    srgbClr = shape.element.spPr.find('.//a:srgbClr', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
    if srgbClr is not None:
        alpha_val = int(alpha_pct * 1000) # OpenXML uses 1/1000th of a percent (30000 = 30%)
        alpha_xml = f'<a:alpha val="{alpha_val}" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'
        srgbClr.append(parse_xml(alpha_xml))

def create_slide(
    output_pptx_path: str,
    title_text: str = "",
    body_text: str = "",
    left_metric: str = "26%",
    left_label: str = "DROPPED THIS YEAR",
    right_metric: str = "74%",
    right_label: str = "GAINED THIS YEAR",
    **kwargs,
) -> str:
    """
    Creates a dynamic diagonal split-screen PPTX slide with native pattern fills.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Colors defined based on the tutorial
    color_left_bg = RGBColor(12, 59, 74)
    color_right_bg = RGBColor(125, 202, 200)
    color_left_circle = RGBColor(7, 31, 39)
    color_cyan_accent = RGBColor(0, 191, 255)
    color_green_accent = MSO_SHAPE.OVAL # Placeholder, we use hex inside
    
    # ----------------------------------------------------
    # LAYER 1: The Diagonal Split Shapes (Trapezoids)
    # ----------------------------------------------------
    
    # 1. Left Trapezoid (Dark Teal)
    ff_builder_left = slide.shapes.build_freeform()
    ff_builder_left.add_line_segments([
        (0, 0),
        (Inches(7.2), 0),          # Top split coordinate
        (Inches(5.8), Inches(7.5)), # Bottom split coordinate
        (0, Inches(7.5)),
        (0, 0)
    ])
    left_shape = ff_builder_left.convert_to_shape()
    left_shape.line.fill.background()
    left_shape.fill.solid()
    left_shape.fill.fore_color.rgb = color_left_bg

    # 2. Right Trapezoid (Light Cyan with Pattern)
    ff_builder_right = slide.shapes.build_freeform()
    ff_builder_right.add_line_segments([
        (Inches(7.2), 0),
        (Inches(13.333), 0),
        (Inches(13.333), Inches(7.5)),
        (Inches(5.8), Inches(7.5)),
        (Inches(7.2), 0)
    ])
    right_shape = ff_builder_right.convert_to_shape()
    right_shape.line.fill.background()
    # Apply native pattern fill (Grid)
    apply_pattern_fill(
        right_shape, 
        prst="lgGrid", 
        fg_hex="90D8D6", # Slightly lighter cyan for the grid lines
        bg_hex="7DCAC8"  # Base light cyan background
    )

    # 3. The Diagonal Separator Line (White Strip)
    ff_builder_sep = slide.shapes.build_freeform()
    ff_builder_sep.add_line_segments([
        (Inches(7.15), 0),
        (Inches(7.35), 0),
        (Inches(5.95), Inches(7.5)),
        (Inches(5.75), Inches(7.5)),
        (Inches(7.15), 0)
    ])
    sep_shape = ff_builder_sep.convert_to_shape()
    sep_shape.line.fill.background()
    sep_shape.fill.solid()
    sep_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    # ----------------------------------------------------
    # LAYER 2: Decorative Abstract Squares
    # ----------------------------------------------------
    # Adding a few translucent overlapping squares to the background
    rect_positions = [
        (Inches(1), Inches(5), Inches(1), Inches(1)),
        (Inches(1.5), Inches(5.5), Inches(1.2), Inches(1.2)),
        (Inches(10), Inches(1), Inches(0.8), Inches(0.8)),
        (Inches(11), Inches(5.5), Inches(1.5), Inches(1.5))
    ]
    for left, top, width, height in rect_positions:
        sq = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        sq.fill.background() # No solid fill
        apply_transparent_line(sq, RGBColor(255, 255, 255), alpha_pct=25)

    # ----------------------------------------------------
    # LAYER 3: Metric Callout Widgets
    # ----------------------------------------------------
    circle_size = Inches(3.5)
    y_pos = Inches(2.0)

    # Left Metric Circle
    left_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(1.5), y_pos, circle_size, circle_size
    )
    left_circle.fill.solid()
    left_circle.fill.fore_color.rgb = color_left_circle
    left_circle.line.color.rgb = color_cyan_accent
    left_circle.line.width = Pt(8)

    # Right Metric Circle
    right_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(8.5), y_pos, circle_size, circle_size
    )
    # Give the right circle a slightly transparent white fill
    right_circle.fill.solid()
    right_circle.fill.fore_color.rgb = RGBColor(240, 250, 250) # Very light
    right_circle.line.color.rgb = RGBColor(60, 179, 113) # Green accent
    right_circle.line.width = Pt(8)

    # Text Helper
    def setup_metric_text(shape, metric_text, label_text, font_color):
        tf = shape.text_frame
        tf.clear() # Clear default
        tf.word_wrap = True
        
        # Metric value (Large)
        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        run1 = p1.add_run()
        run1.text = metric_text + "\n"
        run1.font.size = Pt(64)
        run1.font.bold = True
        run1.font.name = "Arial"
        run1.font.color.rgb = font_color
        
        # Label (Small)
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = label_text
        run2.font.size = Pt(14)
        run2.font.bold = True
        run2.font.name = "Arial"
        run2.font.color.rgb = font_color

    setup_metric_text(left_circle, left_metric, left_label, RGBColor(255, 255, 255))
    setup_metric_text(right_circle, right_metric, right_label, RGBColor(50, 50, 50))

    # Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path

