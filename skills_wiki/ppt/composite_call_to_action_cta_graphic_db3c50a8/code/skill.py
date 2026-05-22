def create_slide(
    output_pptx_path: str,
    primary_text: str = "DOWNLOAD NOW",
    secondary_text: str = "GET INSTANT ACCESS",
    btn_color: tuple = (31, 78, 121),     # Dark Blue
    accent_color: tuple = (192, 0, 0),    # Dark Red
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Composite CTA Button visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import MSO_COLOR_TYPE, RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import int_to_constants
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls

    # Create Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6] 
    slide = prs.slides.add_slide(slide_layout)

    # --- SETTINGS & DIMENSIONS ---
    center_x = prs.slide_width / 2
    center_y = prs.slide_height / 2
    
    btn_w = Inches(5.5)
    btn_h = Inches(1.2)
    btn_left = center_x - (btn_w / 2)
    btn_top = center_y - (btn_h / 2) + Inches(0.5) # Shifted down slightly to accommodate top text

    # --- 1. SECONDARY TEXT (Hook) ---
    tb_w = Inches(6)
    tb_h = Inches(0.8)
    tb_left = center_x - (tb_w / 2)
    tb_top = btn_top - Inches(0.7)
    
    tb = slide.shapes.add_textbox(tb_left, tb_top, tb_w, tb_h)
    tb.text_frame.word_wrap = True
    p_sub = tb.text_frame.paragraphs[0]
    p_sub.text = secondary_text
    p_sub.font.bold = True
    p_sub.font.size = Pt(22)
    p_sub.font.name = 'Georgia' # Serif font to match the tutorial's style contrast
    p_sub.font.color.rgb = RGBColor(*accent_color)
    p_sub.alignment = PP_ALIGN.CENTER

    # --- 2. MAIN BUTTON (Rounded Rectangle) ---
    btn_shape = slide.shapes.add_shape(
        5, # MSO_SHAPE.ROUNDED_RECTANGLE
        btn_left, btn_top, btn_w, btn_h
    )
    
    # Style the button shape
    btn_shape.fill.solid()
    btn_shape.fill.fore_color.rgb = RGBColor(*btn_color)
    btn_shape.line.color.rgb = RGBColor(int(btn_color[0]*0.8), int(btn_color[1]*0.8), int(btn_color[2]*0.8)) # Darker border
    btn_shape.line.width = Pt(2)
    
    # Adjust corner radius (using generic custom geometry adjustment)
    try:
        adjLst = btn_shape.element.xpath('.//a:avLst')[0]
        gd = parse_xml(f'<a:gd name="adj" fmla="val 16667" {nsdecls("a")}/>') # standard pill-like radius
        adjLst.append(gd)
    except:
        pass

    # Add Drop Shadow via LXML injection
    spPr = btn_shape.element.spPr
    shadow_xml = f"""
        <a:effectLst {nsdecls('a')}>
            <a:outerShdw blurRad="50800" dist="38100" dir="2700000" algn="tl">
                <a:srgbClr val="000000">
                    <a:alpha val="35000"/>
                </a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
    """
    spPr.append(parse_xml(shadow_xml))

    # Button Text
    p_main = btn_shape.text_frame.paragraphs[0]
    p_main.text = primary_text
    p_main.font.bold = True
    p_main.font.size = Pt(36)
    p_main.font.name = 'Arial Black'
    p_main.font.color.rgb = RGBColor(255, 255, 255)
    p_main.alignment = PP_ALIGN.CENTER

    # --- 3. DIRECTIONAL ARROWS ---
    # Using Right/Left curved arrows
    arrow_w = Inches(0.8)
    arrow_h = Inches(0.8)
    arrow_y = tb_top + Inches(0.1) # Aligned with the top text
    
    # Left Arrow (Curved Right Arrow, pointing inwards)
    arr_l = slide.shapes.add_shape(
        60, # MSO_SHAPE.CURVED_RIGHT_ARROW
        tb_left - Inches(0.2), arrow_y, arrow_w, arrow_h
    )
    arr_l.rotation = 45 # Tilt downward toward the button
    arr_l.fill.solid()
    arr_l.fill.fore_color.rgb = RGBColor(*accent_color)
    arr_l.line.color.rgb = RGBColor(255, 255, 255)
    arr_l.line.width = Pt(1.5)
    # Add shadow to arrow
    arr_l.element.spPr.append(parse_xml(shadow_xml))

    # Right Arrow (Curved Left Arrow, pointing inwards)
    arr_r = slide.shapes.add_shape(
        59, # MSO_SHAPE.CURVED_LEFT_ARROW
        tb_left + tb_w - Inches(0.6), arrow_y, arrow_w, arrow_h
    )
    arr_r.rotation = -45 # Tilt downward toward the button
    arr_r.fill.solid()
    arr_r.fill.fore_color.rgb = RGBColor(*accent_color)
    arr_r.line.color.rgb = RGBColor(255, 255, 255)
    arr_r.line.width = Pt(1.5)
    # Add shadow to arrow
    arr_r.element.spPr.append(parse_xml(shadow_xml))

    # Save
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("cta_button_slide.pptx")
