def create_slide(
    output_pptx_path: str,
    title_text: str = "Smooth Handwriting",
    font_name: str = "Patrick Hand",
    bg_color_rgb: tuple = (242, 180, 130),
    text_color_rgb: tuple = (0, 0, 0),
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a masked handwriting reveal effect.

    This function generates a stencil with transparent text using PIL, places a
    text box behind it, and applies a 'Wipe' animation using lxml to reveal the text.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The text to be animated.
        font_name: The name of the handwriting font to use.
        bg_color_rgb: The (R, G, B) tuple for the background color.
        text_color_rgb: The (R, G, B) tuple for the text color.

    Returns:
        The path to the saved PPTX file.
    """
    import os
    import requests
    import tempfile
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    from lxml import etree

    # --- Font Handling: Download a free handwriting font ---
    font_url = "https://fonts.google.com/download?family=Patrick%20Hand"
    font_file_path = os.path.join(tempfile.gettempdir(), "PatrickHand-Regular.ttf")

    if not os.path.exists(font_file_path):
        try:
            import zipfile
            response = requests.get(font_url)
            response.raise_for_status()
            zip_file = zipfile.ZipFile(BytesIO(response.content))
            # The TTF file is usually the first file in the zip from Google Fonts
            font_filename = zip_file.namelist()[0]
            with zip_file.open(font_filename) as zf, open(font_file_path, "wb") as f:
                f.write(zf.read())
        except Exception as e:
            print(f"Warning: Could not download font '{font_name}'. Using a default font. Error: {e}")
            font_file_path = None # Fallback to a system font

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Emu(12192000)  # 16:9 aspect ratio
    prs.slide_height = Emu(6858000)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Dimensions ---
    slide_w_px = 1280
    slide_h_px = 720
    dpi = 96
    font_size = 115

    # --- Layer 1: Solid Background ---
    background = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(*bg_color_rgb)
    background.line.fill.background()

    # --- Layer 2: The Text to be Revealed ---
    # Centered textbox
    tx_width = Inches(12)
    tx_height = Inches(2.5)
    tx_left = (prs.slide_width - tx_width) / 2
    tx_top = (prs.slide_height - tx_height) / 2

    textbox = slide.shapes.add_textbox(tx_left, tx_top, tx_width, tx_height)
    tf = textbox.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = font_name
    p.font.size = Pt(font_size)
    p.font.color.rgb = RGBColor(*text_color_rgb)
    from pptx.enum.text import PP_ALIGN
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_SHAPE.VERTICAL_ANCHOR_MIDDLE

    # --- Layer 3: The Stencil (Generated with PIL) ---
    # Create an RGBA image for the stencil
    stencil_img = Image.new('RGBA', (slide_w_px, slide_h_px), (*bg_color_rgb, 255))
    
    # Create a mask for the text
    mask = Image.new('L', (slide_w_px, slide_h_px), 0) # Black background
    draw_mask = ImageDraw.Draw(mask)

    try:
        font = ImageFont.truetype(font_file_path, int(font_size * 1.25))
    except (IOError, TypeError):
        print(f"Warning: PIL could not load font '{font_name}'. Using default.")
        font = ImageFont.load_default()

    # Calculate text position to center it
    bbox = draw_mask.textbbox((0, 0), title_text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_x = (slide_w_px - text_w) / 2
    text_y = (slide_h_px - text_h) / 2 - (bbox[1] * 1.5) # Adjust for vertical alignment

    # Draw white text on the black mask
    draw_mask.text((text_x, text_y), title_text, font=font, fill=255)

    # Punch a hole in the stencil by making the text area transparent
    stencil_img.putalpha(ImageOps.invert(mask))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
        stencil_img.save(temp_image.name)
        slide.shapes.add_picture(temp_image.name, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    os.unlink(temp_image.name) # Clean up the temp file

    # --- Animation (Applied to Layer 2 Textbox using lxml) ---
    # This requires giving the textbox a unique ID
    shape_id = textbox.shape_id
    
    # Define XML namespaces
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }

    # Find the slide's timing element or create it
    slide_xml = slide.element
    timing = slide_xml.find('.//p:timing', namespaces=ns)
    if timing is None:
        timing = etree.SubElement(slide_xml.find('.//p:cSld', namespaces=ns), '{%s}timing' % ns['p'])
    
    tnLst = timing.find('.//p:tnLst', namespaces=ns)
    if tnLst is None:
        tnLst = etree.SubElement(timing, '{%s}tnLst' % ns['p'])
        
    par = etree.SubElement(tnLst, '{%s}par' % ns['p'])
    cTn = etree.SubElement(par, '{%s}cTn' % ns['p'], id=str(shape_id + 1), dur="3000")
    stCondLst = etree.SubElement(cTn, '{%s}stCondLst' % ns['p'])
    etree.SubElement(stCondLst, '{%s}cond' % ns['p'], delay="0")
    
    childTnLst = etree.SubElement(cTn, '{%s}childTnLst' % ns['p'])
    anim_par = etree.SubElement(childTnLst, '{%s}par' % ns['p'])
    anim_cTn = etree.SubElement(anim_par, '{%s}cTn' % ns['p'], id=str(shape_id + 2), fill="hold")
    anim_stCondLst = etree.SubElement(anim_cTn, '{%s}stCondLst' % ns['p'])
    etree.SubElement(anim_stCondLst, '{%s}cond' % ns['p'], delay="0")
    anim_childTnLst = etree.SubElement(anim_cTn, '{%s}childTnLst' % ns['p'])
    anim = etree.SubElement(anim_childTnLst, '{%s}anim' % ns['p'], calcmode="lin", valueType="num")
    anim_cBhvr = etree.SubElement(anim, '{%s}cBhvr' % ns['p'])
    anim_cTn2 = etree.SubElement(anim_cBhvr, '{%s}cTn' % ns['p'], id=str(shape_id + 3), dur="3000")
    etree.SubElement(anim_cTn2, '{%s}stCondLst' % ns['p']).append(etree.Element('{%s}cond' % ns['p'], delay="0"))
    etree.SubElement(anim_cBhvr, '{%s}tgtEl' % ns['p']).append(etree.Element('{%s}spTgt' % ns['p'], spid=str(shape_id)))
    etree.SubElement(anim_cBhvr, '{%s}attrNameLst' % ns['p']).append(etree.Element('{%s}attrName' % ns['p'], val="wipe.end"))
    
    anim_tavLst = etree.SubElement(anim, '{%s}tavLst' % ns['p'])
    etree.SubElement(tavLst, '{%s}tav' % ns['p'], tm="0").append(etree.Element('{%s}val' % ns['p'], val="0"))
    etree.SubElement(tavLst, '{%s}tav' % ns['p'], tm="100000").append(etree.Element('{%s}val' % ns['p'], val="100000"))
    
    # Add transition properties for the wipe effect
    transition_node = etree.fromstring(
        f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        f'spid="{shape_id}" type="wipe" dir="l" />'
    )
    # This is a bit of a hack as python-pptx doesn't expose this directly.
    # The animation XML above is the correct way. The below would be for slide transitions.
    # The animation part above should correctly create an entrance wipe animation.

    # --- Save and Return ---
    prs.save(output_pptx_path)
    return output_pptx_path

