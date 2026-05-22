def create_split_screen_cta_slide(
    output_pptx_path: str,
    title_text: str = "Design Faster than ever!",
    body_text: str = "We pursue relationships based on transparency, persistence, mutual trust, and integrity with our employees, customers and other business partners.",
    primary_cta_text: str = "Buy Now - $64",
    secondary_cta_text: str = "or try Free Version",
    image_keyword: str = "technology",
    accent_color: tuple = (91, 95, 224),
) -> str:
    """
    Creates a PPTX file with a single "Split-Screen Visual CTA" slide.

    This style features a high-impact image on the right and clear, actionable
    text with CTA buttons on the left against a clean background.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The main headline for the slide.
        body_text: The descriptive paragraph.
        primary_cta_text: The text for the main call-to-action button.
        secondary_cta_text: The text for the secondary, less-emphasized action.
        image_keyword: A keyword to search for a background image on Unsplash.
        accent_color: An (R, G, B) tuple for the primary CTA button color.

    Returns:
        The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml.xmlchemy import OxmlElement
    from pptx.oxml.ns import qn
    import requests
    from io import BytesIO

    # --- Presentation and Slide Setup ---
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Layer 1: Background & Image Pane ---
    # Set a white background for the content pane
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Define Image Pane dimensions (right 45% of the slide)
    img_pane_width = prs.slide_width * 0.45
    img_pane_left = prs.slide_width - img_pane_width

    # Fetch and add image
    try:
        unsplash_url = f"https://source.unsplash.com/1600x900/?{image_keyword}"
        response = requests.get(unsplash_url, timeout=10)
        response.raise_for_status()
        image_stream = BytesIO(response.content)
        slide.shapes.add_picture(image_stream, img_pane_left, Inches(0), width=img_pane_width, height=prs.slide_height)
    except (requests.exceptions.RequestException, IOError):
        print("Image download failed. Using a gray placeholder.")
        shape = slide.shapes.add_shape(1, img_pane_left, Inches(0), img_pane_width, prs.slide_height) # 1 is MSO_SHAPE.RECTANGLE
        fill = shape.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(200, 200, 200)
        shape.line.fill.background()

    # --- Layer 2: Text & Content Pane ---
    # Define Content Pane dimensions (left 55%)
    content_pane_width = prs.slide_width - img_pane_width
    left_margin = Inches(0.8)
    text_box_width = content_pane_width - (left_margin * 1.5)

    # Title
    title_shape = slide.shapes.add_textbox(left_margin, Inches(2.5), text_box_width, Inches(1.5))
    p_title = title_shape.text_frame.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Calibri"
    p_title.font.bold = True
    p_title.font.size = Pt(44)
    p_title.font.color.rgb = RGBColor(34, 34, 34)

    # Body
    body_shape = slide.shapes.add_textbox(left_margin, Inches(4.0), text_box_width, Inches(1.0))
    p_body = body_shape.text_frame.paragraphs[0]
    p_body.text = body_text
    p_body.font.name = "Calibri"
    p_body.font.size = Pt(16)
    p_body.font.color.rgb = RGBColor(89, 89, 89)

    # --- Layer 3: CTA Buttons ---
    # Helper function to create a rounded rectangle using lxml
    def create_rounded_rect(shapes, left, top, width, height):
        # Create a generic shape element
        sp = OxmlElement('p:sp')
        spTree = shapes._spTree
        spTree.append(sp)

        # Define shape properties
        nvSpPr = OxmlElement('p:nvSpPr')
        cnvPr = OxmlElement('c:nvPr')
        cnvPr.set('id', str(len(spTree)))
        cnvPr.set('name', f'Rounded Rectangle {len(spTree)}')
        nvSpPr.append(cnvPr)
        # Add other non-visual properties...
        sp.append(nvSpPr)

        # Define the geometry: roundRect
        spPr = OxmlElement('p:spPr')
        prstGeom = OxmlElement('a:prstGeom')
        prstGeom.set('prst', 'roundRect')
        avLst = OxmlElement('a:avLst')
        prstGeom.append(avLst)
        spPr.append(prstGeom)

        # Define position and size
        xfrm = OxmlElement('a:xfrm')
        off = OxmlElement('a:off')
        off.set('x', str(left))
        off.set('y', str(top))
        ext = OxmlElement('a:ext')
        ext.set('cx', str(width))
        ext.set('cy', str(height))
        xfrm.append(off)
        xfrm.append(ext)
        spPr.append(xfrm)
        sp.append(spPr)
        
        # This returns the low-level object; we need to wrap it
        from pptx.shapes.autoshape import Shape
        return Shape(sp, None)

    # Primary CTA Button
    btn_width = Inches(2.5)
    btn_height = Inches(0.6)
    btn_left = left_margin
    btn_top = Inches(5.5)
    
    primary_btn = create_rounded_rect(slide.shapes, btn_left.emu, btn_top.emu, btn_width.emu, btn_height.emu)
    fill = primary_btn.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    primary_btn.line.fill.background()

    text_frame = primary_btn.text_frame
    text_frame.clear()
    p_btn = text_frame.paragraphs[0]
    p_btn.text = primary_cta_text
    p_btn.font.name = 'Calibri'
    p_btn.font.bold = True
    p_btn.font.size = Pt(16)
    p_btn.font.color.rgb = RGBColor(255, 255, 255)
    p_btn.alignment = PP_ALIGN.CENTER
    text_frame.margin_bottom = 0
    text_frame.margin_top = 0

    # Secondary CTA Text
    secondary_cta_left = btn_left + btn_width + Inches(0.2)
    secondary_shape = slide.shapes.add_textbox(secondary_cta_left, btn_top, Inches(3), btn_height)
    secondary_shape.text_frame.vertical_anchor = 'middle'
    p_secondary = secondary_shape.text_frame.paragraphs[0]
    p_secondary.text = secondary_cta_text
    p_secondary.font.name = 'Calibri'
    p_secondary.font.size = Pt(14)
    p_secondary.font.color.rgb = RGBColor(128, 128, 128)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_split_screen_cta_slide(
#     "split_screen_cta.pptx",
#     title_text="Launch Your Next Idea.",
#     body_text="Leverage our powerful platform to build, deploy, and scale your applications faster than ever before.",
#     primary_cta_text="Get Started Now",
#     secondary_cta_text="or request a demo",
#     image_keyword="rocket launch",
#     accent_color=(255, 107, 107) # A coral red accent
# )
