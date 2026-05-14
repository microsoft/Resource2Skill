def create_slide(
    output_pptx_path: str,
    title_text: str = "YOUR TITLE",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Radial Pocket-Fold Infographic visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.dml import MSO_LINE_DASH_STYLE, MSO_ARROWHEAD_STYLE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    import math

    # Helper function for advanced XML formatting (Gradients and Shadows)
    def apply_custom_formatting(shape, fill_type=None, color1="FFFFFF", color2="FFFFFF", angle=135,
                                shadow=False, blur=25, dist=12, shadow_angle=45, alpha=20):
        from pptx.oxml import parse_xml
        spPr = shape.element.spPr
        
        # 1. Clean existing fills, lines, and effects to prevent schema conflicts
        for child in list(spPr):
            if child.tag.endswith('Fill') or child.tag.endswith('ln') or child.tag.endswith('effectLst'):
                spPr.remove(child)

        # 2. Find safe insertion point (immediately after geometry definition)
        insert_idx = 0
        for i, child in enumerate(spPr):
            if child.tag.endswith('Geom'):
                insert_idx = i + 1

        # 3. Add Custom Fill
        if fill_type == 'gradient':
            grad_xml = f"""
            <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rotWithShape="1">
                <a:gsLst>
                    <a:gs pos="0"><a:srgbClr val="{color1}"/></a:gs>
                    <a:gs pos="100000"><a:srgbClr val="{color2}"/></a:gs>
                </a:gsLst>
                <a:lin ang="{int(angle * 60000)}" scaled="1"/>
            </a:gradFill>
            """
            spPr.insert(insert_idx, parse_xml(grad_xml))
            insert_idx += 1
        elif fill_type == 'solid':
            solid_xml = f"""
            <a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:srgbClr val="{color1}"/>
            </a:solidFill>
            """
            spPr.insert(insert_idx, parse_xml(solid_xml))
            insert_idx += 1

        # 4. Add Drop Shadow
        if shadow:
            shadow_xml = f"""
            <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:outerShdw blurRad="{int(blur * 12700)}" dist="{int(dist * 12700)}" dir="{int(shadow_angle * 60000)}" algn="tl" rotWithShape="0">
                    <a:srgbClr val="000000">
                        <a:alpha val="{int(alpha * 1000)}"/>
                    </a:srgbClr>
                </a:outerShdw>
            </a:effectLst>
            """
            spPr.insert(insert_idx, parse_xml(shadow_xml))

    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Enforce pure white background for seamless masking
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Coordinates for the central hub
    center_x, center_y = 9.5, 3.75
    radius = 1.25

    # === Layer 1: Central Hub Circle ===
    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        Inches(center_x - radius), Inches(center_y - radius), 
        Inches(radius * 2), Inches(radius * 2)
    )
    apply_custom_formatting(
        circle, fill_type='gradient', color1="47C99D", color2="FFFFFF", angle=135,
        shadow=True, blur=25, dist=8, shadow_angle=45, alpha=10
    )

    # === Layer 2: The "Pocket Fold" Mask ===
    # A polygon specifically drawn to cover the top-left arc of the circle
    builder = slide.shapes.build_freeform()
    builder.add_line_segments([
        (Inches(6.5), Inches(1.0)),
        (Inches(9.7), Inches(1.0)),
        (Inches(9.7), Inches(2.3)),  # Top intersection point with circle
        (Inches(8.0), Inches(4.0)),  # Left intersection point with circle
        (Inches(6.5), Inches(4.0)),
        (Inches(6.5), Inches(1.0)),
    ])
    flap = builder.convert_to_shape()
    apply_custom_formatting(
        flap, fill_type='solid', color1="FFFFFF", 
        shadow=True, blur=20, dist=8, shadow_angle=45, alpha=15
    )

    # === Layer 3: Central Number ===
    tx_center = slide.shapes.add_textbox(
        Inches(center_x - radius), Inches(center_y - radius), 
        Inches(radius * 2), Inches(radius * 2)
    )
    tx_center.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tx_center.text_frame.paragraphs[0]
    p.text = "5"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(80)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x47, 0xC9, 0x9D) # Sea Green

    # === Layer 4: Radiating Lines and Text Blocks ===
    angles_deg = [145, 90, 15, -35, -90]
    line_start_radius = 1.45
    line_length = 1.2
    
    for i, angle in enumerate(angles_deg):
        rad = math.radians(angle)
        sx = center_x + line_start_radius * math.cos(rad)
        sy = center_y - line_start_radius * math.sin(rad)
        ex = center_x + (line_start_radius + line_length) * math.cos(rad)
        ey = center_y - (line_start_radius + line_length) * math.sin(rad)

        # Draw connecting line
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(sx), Inches(sy), Inches(ex), Inches(ey))
        conn.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        conn.line.end_arrowhead = MSO_ARROWHEAD_STYLE.STEALTH
        conn.line.color.rgb = RGBColor(160, 160, 160)
        conn.line.width = Pt(1.5)

        # Draw starting dot
        dot_rad = 0.05
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(sx - dot_rad), Inches(sy - dot_rad), Inches(dot_rad*2), Inches(dot_rad*2))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(160, 160, 160)
        dot.line.fill.background()

        # Position textual option blocks based on angle
        tx_width, tx_height = 2.2, 1.0
        if 90 < angle < 270: # Left hemisphere
            tx = ex - tx_width - 0.1
            ty = ey - tx_height / 2
            align = PP_ALIGN.RIGHT
        elif angle == 90: # Top center
            tx = ex - tx_width / 2
            ty = ey - tx_height - 0.1
            align = PP_ALIGN.CENTER
        elif angle == -90 or angle == 270: # Bottom center
            tx = ex - tx_width / 2
            ty = ey + 0.1
            align = PP_ALIGN.CENTER
        else: # Right hemisphere
            tx = ex + 0.1
            ty = ey - tx_height / 2
            align = PP_ALIGN.LEFT

        tb_opt = slide.shapes.add_textbox(Inches(tx), Inches(ty), Inches(tx_width), Inches(tx_height))
        tb_opt.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        # Option Identifier (Placeholder for icon)
        p0 = tb_opt.text_frame.paragraphs[0]
        p0.text = f"0{i+1}"
        p0.font.bold = True
        p0.font.size = Pt(18)
        p0.font.color.rgb = RGBColor(200, 200, 200)
        p0.alignment = align

        # Option Title
        p1 = tb_opt.text_frame.add_paragraph()
        p1.text = f"OPTION {i+1}"
        p1.font.bold = True
        p1.font.size = Pt(14)
        p1.font.color.rgb = RGBColor(40, 40, 40)
        p1.alignment = align

        # Option Body
        p2 = tb_opt.text_frame.add_paragraph()
        p2.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        p2.font.size = Pt(10)
        p2.font.color.rgb = RGBColor(136, 136, 136)
        p2.alignment = align

    # === Layer 5: Left Panel Main Title ===
    tb_main = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(4.0), Inches(4.0))
    tf_main = tb_main.text_frame
    
    p_title = tf_main.paragraphs[0]
    p_title.text = title_text
    p_title.font.bold = True
    p_title.font.size = Pt(36)
    p_title.font.color.rgb = RGBColor(230, 95, 92) # Coral Red accent

    p_body = tf_main.add_paragraph()
    p_body.text = body_text
    p_body.font.size = Pt(14)
    p_body.font.color.rgb = RGBColor(119, 119, 119)
    p_body.space_before = Pt(14)

    prs.save(output_pptx_path)
    return output_pptx_path
