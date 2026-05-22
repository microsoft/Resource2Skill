def create_slide(
    output_pptx_path: str,
    title_text: str = "MASTER\nLAYOUTS",
    body_text: str = "Discover the core principles of overlapping elements, asymmetrical balance, and color flow to create professional and engaging visual hierarchies.",
    bg_color_start: tuple = (255, 65, 108),  # Vibrant Pink
    bg_color_end: tuple = (255, 135, 90),    # Warm Peach
    cta_color: tuple = (0, 229, 255),        # Bright Turquoise
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Dynamic Asymmetric Overlap Layout' visual effect.
    
    Returns: path to the saved PPTX file.
    """
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from lxml import etree
    from PIL import Image, ImageDraw, ImageFilter

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Color Flow Background (lxml gradient) ===
    # We use a fullscreen rectangle for a robust background gradient
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.line.fill.background()  # Remove outline
    spPr = bg_shape._element.spPr

    # Remove default solid fill
    for elem in spPr.findall('.//a:solidFill', namespaces=spPr.nsmap):
        spPr.remove(elem)

    # Inject linear gradient
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    gradFill = etree.SubElement(spPr, f"{{{a}}}gradFill", rotWithShape="1")
    gsLst = etree.SubElement(gradFill, f"{{{a}}}gsLst")
    
    # Start color
    gs1 = etree.SubElement(gsLst, f"{{{a}}}gs", pos="0")
    srgbClr1 = etree.SubElement(gs1, f"{{{a}}}srgbClr", val=f"{bg_color_start[0]:02X}{bg_color_start[1]:02X}{bg_color_start[2]:02X}")
    
    # End color
    gs2 = etree.SubElement(gsLst, f"{{{a}}}gs", pos="100000")
    srgbClr2 = etree.SubElement(gs2, f"{{{a}}}srgbClr", val=f"{bg_color_end[0]:02X}{bg_color_end[1]:02X}{bg_color_end[2]:02X}")
    
    lin = etree.SubElement(gradFill, f"{{{a}}}lin", ang="5400000", scaled="1")  # Top to bottom

    # === Layer 2: Main Typography (Visual Hierarchy) ===
    # Positioned asymmetrically on the left
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(8.0), Inches(3.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(110)
    p.font.bold = True
    p.font.name = "Arial Black"
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.line_spacing = 0.9

    # === Layer 3: Dynamic Overlapping Graphic (PIL generated) ===
    # We generate a soft, blurred frosted glass/glowing orb to overlap the text
    orb_size = 1000
    img = Image.new('RGBA', (orb_size, orb_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a semi-transparent white/blue polygon/circle
    margin = 150
    draw.ellipse(
        [margin, margin, orb_size - margin, orb_size - margin], 
        fill=(255, 255, 255, 120)  # 50% transparent white
    )
    # Apply a heavy blur to make it soft and abstract
    img = img.filter(ImageFilter.GaussianBlur(radius=60))
    
    # Save to BytesIO and insert
    image_stream = io.BytesIO()
    img.save(image_stream, format='PNG')
    image_stream.seek(0)
    
    # Position the graphic so it intentionally overlaps the title text and breaks the grid
    slide.shapes.add_picture(
        image_stream, 
        Inches(6.0), Inches(0.5), 
        width=Inches(7.0), height=Inches(7.0)
    )

    # === Layer 4: Body Text and Visual Pathways ===
    # Ample white space below the title
    body_box = slide.shapes.add_textbox(Inches(0.9), Inches(4.5), Inches(4.5), Inches(1.5))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.size = Pt(18)
    p_body.font.name = "Arial"
    p_body.font.color.rgb = RGBColor(255, 255, 255)
    p_body.line_spacing = 1.3

    # === Layer 5: High Contrast Call to Action (CTA) ===
    # Placed at the bottom left to finalize the visual pathway
    cta_width, cta_height = Inches(2.2), Inches(0.6)
    cta = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        Inches(0.9), Inches(6.0), 
        cta_width, cta_height
    )
    cta.fill.solid()
    cta.fill.fore_color.rgb = RGBColor(*cta_color)
    cta.line.fill.background()  # No outline
    
    # CTA Text
    cta_tf = cta.text_frame
    cta_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    cta_p = cta_tf.paragraphs[0]
    cta_p.text = "LEARN MORE"
    cta_p.alignment = PP_ALIGN.CENTER
    cta_p.font.size = Pt(14)
    cta_p.font.bold = True
    cta_p.font.name = "Arial"
    cta_p.font.color.rgb = RGBColor(20, 20, 30)  # Dark text for high contrast

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
