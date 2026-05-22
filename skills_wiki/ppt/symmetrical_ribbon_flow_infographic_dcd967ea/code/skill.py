def create_slide(
    output_pptx_path: str,
    title_text: str = "10 OPTIONS PERSPECTIVE",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Symmetrical Ribbon-Flow Infographic.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Set Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(235, 235, 235)  # Light gray

    # === Define Colors ===
    row_colors = [
        RGBColor(146, 208, 80),  # Row 1: Light Green
        RGBColor(0, 176, 80),    # Row 2: Green
        RGBColor(0, 176, 240),   # Row 3: Teal
        RGBColor(0, 112, 192),   # Row 4: Blue
        RGBColor(0, 32, 96)      # Row 5: Dark Blue
    ]
    
    white = RGBColor(255, 255, 255)
    text_dark = RGBColor(50, 50, 50)
    text_gray = RGBColor(120, 120, 120)

    # === Layout Mathematics ===
    num_rows = 5
    
    # Outer text boxes (Spaced out)
    box_w = Inches(3.2)
    box_h = Inches(0.85)
    left_box_x = Inches(1.5)
    right_box_x = Inches(13.333 - 1.5) - box_w
    box_start_y = Inches(1.0)
    box_y_spacing = Inches(1.2)

    # Center axis nodes (Packed tight)
    center_w = Inches(0.8)
    center_h = Inches(0.4)
    center_x = Inches(13.333 / 2) - (center_w / 2)
    center_start_y = Inches(2.2)
    center_y_spacing = Inches(0.5)

    # === Helper function to add drop shadow via OpenXML ===
    def add_drop_shadow(shape):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
        outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw",
                                     blurRad="40000", dist="30000", dir="2700000", algn="ctr", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr", val="000000")
        etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha", val="15000") # 15% opacity

    # === Drawing Loop ===
    # Note: We draw connectors FIRST so they sit behind the center blocks and white boxes
    
    # 1. Draw Connectors (Layer 1 - Back)
    for i in range(num_rows):
        color = row_colors[i]
        
        box_y = box_start_y + (i * box_y_spacing)
        center_y = center_start_y + (i * center_y_spacing)
        
        # Left Ribbon Connector
        ff_builder_left = slide.shapes.build_freeform(left_box_x + box_w - Inches(0.1), box_y) # slightly overlap
        ff_builder_left.add_line_segments([
            (center_x, center_y),
            (center_x, center_y + center_h),
            (left_box_x + box_w - Inches(0.1), box_y + box_h)
        ], close=True)
        left_conn = ff_builder_left.convert_to_shape()
        left_conn.fill.solid()
        left_conn.fill.fore_color.rgb = color
        left_conn.line.fill.background() # No line
        
        # Right Ribbon Connector
        ff_builder_right = slide.shapes.build_freeform(right_box_x + Inches(0.1), box_y)
        ff_builder_right.add_line_segments([
            (center_x + center_w, center_y),
            (center_x + center_w, center_y + center_h),
            (right_box_x + Inches(0.1), box_y + box_h)
        ], close=True)
        right_conn = ff_builder_right.convert_to_shape()
        right_conn.fill.solid()
        right_conn.fill.fore_color.rgb = color
        right_conn.line.fill.background() # No line

    # 2. Draw Center Axis & Content Boxes (Layer 2 - Front)
    for i in range(num_rows):
        color = row_colors[i]
        
        box_y = box_start_y + (i * box_y_spacing)
        center_y = center_start_y + (i * center_y_spacing)
        
        # Center Node
        center_node = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, center_x, center_y, center_w, center_h)
        center_node.fill.solid()
        center_node.fill.fore_color.rgb = color
        center_node.line.fill.background()

        # Left Rounded Box
        left_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_box_x, box_y, box_w, box_h)
        left_box.adjustments[0] = 0.2  # Corner radius
        left_box.fill.solid()
        left_box.fill.fore_color.rgb = white
        left_box.line.fill.background()
        add_drop_shadow(left_box)

        # Right Rounded Box
        right_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_box_x, box_y, box_w, box_h)
        right_box.adjustments[0] = 0.2
        right_box.fill.solid()
        right_box.fill.fore_color.rgb = white
        right_box.line.fill.background()
        add_drop_shadow(right_box)

        # === Add Text content ===
        
        # Left Text
        tb_l = slide.shapes.add_textbox(left_box_x + Inches(0.8), box_y + Inches(0.05), box_w - Inches(0.9), box_h)
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        
        p1 = tf_l.paragraphs[0]
        p1.text = f"OPTION {i+1:02d}"
        p1.font.bold = True
        p1.font.size = Pt(14)
        p1.font.color.rgb = color
        
        p2 = tf_l.add_paragraph()
        p2.text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
        p2.font.size = Pt(10)
        p2.font.color.rgb = text_gray

        # Right Text
        tb_r = slide.shapes.add_textbox(right_box_x + Inches(0.1), box_y + Inches(0.05), box_w - Inches(0.9), box_h)
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        
        p1 = tf_r.paragraphs[0]
        p1.text = f"OPTION {i+6:02d}"
        p1.font.bold = True
        p1.font.size = Pt(14)
        p1.font.color.rgb = color
        
        p2 = tf_r.add_paragraph()
        p2.text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
        p2.font.size = Pt(10)
        p2.font.color.rgb = text_gray
        
        # Decorative Icon Placeholders (Circles)
        icon_l = slide.shapes.add_shape(MSO_SHAPE.OVAL, left_box_x + Inches(0.15), box_y + Inches(0.15), Inches(0.55), Inches(0.55))
        icon_l.fill.solid()
        icon_l.fill.fore_color.rgb = RGBColor(240, 240, 240)
        icon_l.line.fill.background()
        
        icon_r = slide.shapes.add_shape(MSO_SHAPE.OVAL, right_box_x + box_w - Inches(0.7), box_y + Inches(0.15), Inches(0.55), Inches(0.55))
        icon_r.fill.solid()
        icon_r.fill.fore_color.rgb = RGBColor(240, 240, 240)
        icon_r.line.fill.background()

    # === Add Slide Title (Optional based on design layout) ===
    # Using a subtle overlay text or a small title block if needed
    
    prs.save(output_pptx_path)
    return output_pptx_path
