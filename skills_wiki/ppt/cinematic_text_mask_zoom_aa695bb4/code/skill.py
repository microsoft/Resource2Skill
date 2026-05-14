def create_slide(
    output_pptx_path: str,
    title_text: str = "THANKS",
    bg_keyword: str = "nature,landscape",
    accent_color_rgb: tuple = (200, 220, 240),
    font_family: str = "Arial Black",
    font_size_pt: int = 120,
    **kwargs,
) -> str:
    """
    Creates a two-slide PPTX presentation reproducing the Cinematic Text Mask Zoom effect.

    The first slide features the title text filled with a background image.
    The second slide reveals the full background image.
    A Morph transition is applied for a cinematic zoom effect.

    Returns: Path to the saved PPTX file.
    """
    import os
    import urllib.request
    import io
    from lxml import etree
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)

    # === Helper for lxml ===
    def _get_shape_xml(shape):
        return shape.element

    def qn(tag):
        """
        Stands for 'qualified name', a utility function to turn a namespace-prefixed
        tag name into a Clark-notation qualified tag name for lxml.
        """
        nsmap = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        }
        prefix, tagroot = tag.split(':')
        uri = nsmap[prefix]
        return f'{{{uri}}}{tagroot}'

    # === Download or Create Background Image ===
    image_stream = io.BytesIO()
    try:
        url = f"https://source.unsplash.com/1920x1080/?{bg_keyword}"
        with urllib.request.urlopen(url) as response:
            image_stream.write(response.read())
        image_stream.seek(0)
        print(f"Successfully downloaded image for '{bg_keyword}'.")
    except Exception as e:
        print(f"Failed to download image, creating fallback gradient: {e}")
        img = Image.new('RGB', (1920, 1080), color = '#1c2e4a')
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 1920, 540], fill='#2d4a78')
        img.save(image_stream, format='PNG')
        image_stream.seek(0)
        
    # === Slide 1: The Text Mask ===
    slide1 = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Set a solid black background
    background = slide1.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 0, 0)
    
    # Add text box for the title
    txBox = slide1.shapes.add_textbox(Inches(0.5), Inches(3), prs.slide_width - Inches(1), Inches(3))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title_text
    
    font = run.font
    font.name = font_family
    font.size = Pt(font_size_pt)
    font.bold = True
    font.color.rgb = RGBColor(255, 255, 255) # Fallback color
    
    # --- lxml Magic: Picture Fill and Outline for Text ---
    # Add image to presentation parts to get a relationship ID (rId)
    image_part, rId = slide1.part.get_or_add_image_part(image_stream)

    # Get the lxml element for the run
    el = run._r
    rPr = el.get_or_add_rPr()

    # Create the picture fill element
    blip_fill = etree.SubElement(rPr, qn('a:blipFill'))
    blip = etree.SubElement(blip_fill, qn('a:blip'), {qn('r:embed'): rId})
    stretch = etree.SubElement(blip_fill, qn('a:stretch'))
    etree.SubElement(stretch, qn('a:fillRect'))
    
    # Create the outline element
    line = etree.SubElement(rPr, qn('a:ln'), {'w': str(Pt(1.5).emu)})
    solid_fill = etree.SubElement(line, qn('a:solidFill'))
    srgb_clr = etree.SubElement(solid_fill, qn('a:srgbClr'), {'val': f'{accent_color_rgb[0]:02x}{accent_color_rgb[1]:02x}{accent_color_rgb[2]:02x}'})

    # === Slide 2: The Full Reveal ===
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    image_stream.seek(0) # Reset stream pointer
    slide2.background.fill.picture(image_stream)

    # --- lxml Magic: Apply Morph Transition to Slide 2 ---
    slide2_xml = slide2.element
    transition_xml = etree.SubElement(slide2_xml, qn('p:transition'), {
        'type': 'morph',
        'advTm': '3000' # 3000ms = 3 seconds
    })

    # === Save Presentation ===
    prs.save(output_pptx_path)
    return output_pptx_path

