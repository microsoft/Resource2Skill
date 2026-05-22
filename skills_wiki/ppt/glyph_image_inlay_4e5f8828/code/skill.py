def create_slide(
    output_pptx_path: str,
    title_text: str = "BRICS",
    image_keywords: list = None,
    subtitle_text: str = "2023年金砖国家峰会",
    font_family: str = "Alibaba PuHuiTi 2.0 115 Black", # A very heavy font is required
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with the "Glyph Image Inlay" effect.

    Each character of the title_text is used as a mask to show a unique image
    fetched based on the corresponding keyword in image_keywords.

    Args:
        output_pptx_path: Path to save the generated PPTX file.
        title_text: The main word to display (e.g., "BRICS").
        image_keywords: A list of search terms for Unsplash, one for each letter.
                        Must have the same length as title_text.
        subtitle_text: Supporting text below the main title.
        font_family: The name of a very bold/heavy font installed on the system.

    Returns:
        Path to the saved PPTX file.
    """
    import io
    import requests
    from lxml import etree
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw

    # Default keywords for "BRICS" example
    if image_keywords is None:
        image_keywords = ["Brazil", "Russia landmark", "India Taj Mahal", "China Forbidden City", "South Africa coast"]
    
    if len(title_text) != len(image_keywords):
        raise ValueError("The length of title_text and image_keywords must be the same.")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    # Generate a subtle diagonal line background with PIL
    bg_color = (245, 245, 245)
    line_color = (220, 220, 220)
    bg_image = Image.new('RGB', (1280, 720), bg_color)
    draw = ImageDraw.Draw(bg_image)
    for i in range(-bg_image.width, bg_image.width, 20):
        draw.line([(i, 0), (i + bg_image.height, bg_image.height)], fill=line_color, width=2)

    bg_image_stream = io.BytesIO()
    bg_image.save(bg_image_stream, format='PNG')
    bg_image_stream.seek(0)
    slide.shapes.add_picture(bg_image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Glyph Image Inlay ===
    # XML namespace mapping
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    # Helper function for lxml
    def qn(tag):
        prefix, tagroot = tag.split(':')
        return f'{{{ns[prefix]}}}{tagroot}'

    total_width_in_emu = Emu(10.5 * 914400) # Approx 10.5 inches
    char_width_in_emu = total_width_in_emu / len(title_text)
    start_left_in_emu = (prs.slide_width - total_width_in_emu) / 2
    char_height = Inches(4.5)
    top_pos = (prs.slide_height - char_height) / 2 - Inches(0.2)
    font_size = Pt(550)

    for i, char in enumerate(title_text):
        # Fetch image from Unsplash
        image_url = f"https://source.unsplash.com/1600x900/?{image_keywords[i].replace(' ', '+')}"
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image_stream = io.BytesIO(response.content)
            pic = slide.shapes.add_picture(image_stream, Inches(-5), Inches(-5), width=Inches(1)) # Hidden
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not download image for '{char}'. Skipping fill. Error: {e}")
            pic = None

        # Create text box for the character
        left = Emu(start_left_in_emu + i * char_width_in_emu)
        tx_box = slide.shapes.add_textbox(left, top_pos, Emu(char_width_in_emu), char_height)
        tf = tx_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = char
        font = run.font
        font.name = font_family
        font.size = font_size
        font.bold = True
        font.color.rgb = RGBColor(89, 89, 89) # Fallback color

        # Inject picture fill using lxml
        if pic:
            tx_box_element = tx_box.element
            rpr = tx_box_element.xpath('.//a:rPr', namespaces=ns)[0]
            
            # Remove existing solid fill if it exists
            solid_fill = rpr.find(qn('a:solidFill'))
            if solid_fill is not None:
                rpr.remove(solid_fill)

            pic_fill = etree.SubElement(rpr, qn('a:picFill'))
            blip_fill = etree.SubElement(pic_fill, qn('a:blipFill'))
            
            # Get the relationship ID (rId) of the hidden picture
            pic_r_id = pic.element.xpath('.//a:blip/@r:embed', namespaces=ns)[0]
            
            blip = etree.SubElement(blip_fill, qn('a:blip'), attrib={qn('r:embed'): pic_r_id})
            stretch = etree.SubElement(blip_fill, qn('a:stretch'))
            fill_rect = etree.SubElement(stretch, qn('a:fillRect'))
            
            # Remove the hidden picture shape
            spTree = slide.shapes.element
            spTree.remove(pic.element)

    # === Layer 3: Subtitle Text ===
    subtitle_box = slide.shapes.add_textbox(Inches(1.66), Inches(5.5), Inches(10), Inches(1))
    subtitle_tf = subtitle_box.text_frame
    subtitle_tf.text = f"{subtitle_text}\n{title_text.upper()} summit"
    subtitle_p = subtitle_tf.paragraphs[0]
    subtitle_p.font.name = "Alibaba PuHuiTi 2.0 55 Regular"
    subtitle_p.font.size = Pt(24)
    subtitle_p.font.color.rgb = RGBColor(89, 89, 89)
    from pptx.enum.text import PP_ALIGN
    subtitle_p.alignment = PP_ALIGN.CENTER
    subtitle_p2 = subtitle_tf.paragraphs[1]
    subtitle_p2.font.name = "Alibaba PuHuiTi 2.0 55 Regular"
    subtitle_p2.font.size = Pt(18)
    subtitle_p2.font.color.rgb = RGBColor(150, 150, 150)
    subtitle_p2.alignment = PP_ALIGN.CENTER


    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("glyph_image_inlay_brics.pptx")
# create_slide(
#     "glyph_image_inlay_grow.pptx",
#     title_text="GROW",
#     image_keywords=["finance chart", "teamwork", "green energy", "technology abstract"],
#     subtitle_text="Q4 Business Growth Summit"
# )
