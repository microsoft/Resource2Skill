def create_slide(
    output_pptx_path: str,
    title_text: str = "CONGRATULATIONS",
    body_text: str = "NPFL CHAMPIONS\n2020/21",
    bg_color: tuple = (25, 160, 130),       # Mid-tone Teal
    card_color: tuple = (255, 255, 255),    # White card
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Neumorphic Dual-Shadow Card effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml

    # Helper function to inject precise shadow XML
    def apply_custom_shadow(shape, hex_color, alpha_pct, blur_pt, dist_pt, angle_deg):
        # Convert values to PowerPoint DrawingML units
        alpha_val = int(alpha_pct * 1000)       # 1000ths of a percent
        blur_val = int(blur_pt * 12700)         # EMUs
        dist_val = int(dist_pt * 12700)         # EMUs
        angle_val = int(angle_deg * 60000)      # 60000ths of a degree

        shadow_xml = f"""
        <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:outerShdw blurRad="{blur_val}" dist="{dist_val}" dir="{angle_val}" algn="tl" rotWithShape="0">
                <a:srgbClr val="{hex_color}">
                    <a:alpha val="{alpha_val}"/>
                </a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        effectLst = parse_xml(shadow_xml)
        spPr = shape.element.spPr
        
        # Remove existing effect list if any
        existing = spPr.find(f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}effectLst")
        if existing is not None:
            spPr.remove(existing)
            
        spPr.append(effectLst)

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    # Set solid background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # Card dimensions and position (Centered)
    card_width = Inches(7.0)
    card_height = Inches(3.5)
    card_left = (prs.slide_width - card_width) / 2
    card_top = (prs.slide_height - card_height) / 2

    # === Layer 2: Bottom Shape (Dark Shadow) ===
    shape_bottom = slide.shapes.add_shape(
        1,  # msoShapeRoundedRectangle
        card_left, card_top, card_width, card_height
    )
    shape_bottom.fill.solid()
    shape_bottom.fill.fore_color.rgb = RGBColor(*card_color)
    shape_bottom.line.fill.background() # No outline
    
    # Apply Dark Shadow (Bottom Right)
    # Tutorial settings: Trans=58% (Opacity 42%), Blur=24, Dist=11, Angle=45
    apply_custom_shadow(
        shape=shape_bottom,
        hex_color="000000",
        alpha_pct=42.0,
        blur_pt=24,
        dist_pt=11,
        angle_deg=45
    )

    # === Layer 3: Top Shape (Light Shadow & Content) ===
    shape_top = slide.shapes.add_shape(
        1,  # msoShapeRoundedRectangle
        card_left, card_top, card_width, card_height
    )
    shape_top.fill.solid()
    shape_top.fill.fore_color.rgb = RGBColor(*card_color)
    shape_top.line.fill.background() # No outline

    # Apply Light Shadow (Top Left)
    # Tutorial settings: Trans=70% (Opacity 30%), Blur=24, Dist=11, Angle=Top Left (225)
    apply_custom_shadow(
        shape=shape_top,
        hex_color="FFFFFF",
        alpha_pct=30.0,
        blur_pt=24,
        dist_pt=11,
        angle_deg=225 
    )

    # === Layer 4: Text Content ===
    # Add text to the top shape
    text_frame = shape_top.text_frame
    text_frame.clear()  # Clear default paragraph
    text_frame.vertical_anchor = 3 # Middle

    # Title Paragraph
    p_title = text_frame.paragraphs[0]
    p_title.text = title_text
    p_title.alignment = PP_ALIGN.CENTER
    font_title = p_title.font
    font_title.name = 'Arial'
    font_title.size = Pt(24)
    font_title.bold = True
    font_title.color.rgb = RGBColor(50, 50, 50) # Dark gray

    # Body Paragraph
    p_body = text_frame.add_paragraph()
    p_body.text = body_text
    p_body.alignment = PP_ALIGN.CENTER
    font_body = p_body.font
    font_body.name = 'Arial'
    font_body.size = Pt(28)
    font_body.bold = True
    font_body.color.rgb = RGBColor(30, 30, 30) # Darker gray

    prs.save(output_pptx_path)
    return output_pptx_path
