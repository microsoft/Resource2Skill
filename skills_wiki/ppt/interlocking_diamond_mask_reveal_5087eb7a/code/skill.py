def create_slide(
    output_pptx_path: str,
    title_text: str = "THANK YOU",
    bg_keyword: str = "mountain,landscape",
    mask_color: tuple = (32, 36, 45, 255),  # Dark slate mask
    gradient_colors: tuple = ("8A2387", "E94057"), # Purple to Pink
) -> str:
    """
    Creates a slide featuring an interlocking diamond picture mask and a glowing central focal shape.
    """
    import os
    import tempfile
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw

    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Ensure temp files are cleaned up
    temp_dir = tempfile.mkdtemp()
    bg_img_path = os.path.join(temp_dir, "bg.jpg")
    mask_img_path = os.path.join(temp_dir, "mask.png")

    # === Layer 1: Background Image ===
    try:
        url = f"https://images.unsplash.com/featured/1920x1080/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bg_img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback to a solid dark grey image if download fails
        fallback = Image.new('RGB', (1920, 1080), (50, 50, 50))
        fallback.save(bg_img_path)

    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Generate PIL Interlocking Grid Mask ===
    width, height = 1920, 1080
    CX, CY = width / 2, height / 2

    # Diamond parameters
    S = 260       # Size of unrotated square
    R = 40        # Corner radius
    G = 16        # Gap between diamonds
    W = int(S * 1.4142)  # Diagonal width of rotated square
    
    H_spacing = W + G
    V_spacing = H_spacing / 2.0

    # Create single transparent hole template
    diamond = Image.new('L', (S, S), 0)
    draw = ImageDraw.Draw(diamond)
    draw.rounded_rectangle((0, 0, S, S), radius=R, fill=255)
    # Rotate to make it a diamond; expand to fit new bounds
    diamond = diamond.rotate(45, resample=Image.BICUBIC, expand=True, fillcolor=0)
    W_rot = diamond.width

    # Create the full mask: opaque color, with 255 alpha everywhere initially
    alpha_mask = Image.new('L', (width, height), 255)
    
    # Punch holes in the alpha mask
    # We loop from center outward to ensure perfect symmetry
    for r in range(-4, 5):
        y = CY + r * V_spacing
        # Stagger every other row
        offset = H_spacing / 2.0 if r % 2 != 0 else 0
        for c in range(-4, 5):
            x = CX + c * H_spacing + offset
            paste_x = int(x - W_rot / 2)
            paste_y = int(y - W_rot / 2)
            # Pasting '0' (black) using the diamond as an alpha mask 
            # turns the targeted area transparent.
            alpha_mask.paste(0, (paste_x, paste_y), mask=diamond)

    # Apply alpha mask to solid color overlay
    overlay = Image.new('RGBA', (width, height), mask_color)
    overlay.putalpha(alpha_mask)
    overlay.save(mask_img_path)

    # Add mask to slide
    slide.shapes.add_picture(mask_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)


    # === Layer 3: Central Highlight Shape ===
    # Convert PIL pixels to inches (144 DPI standard mapping for 1920x1080 -> 13.333x7.5)
    # We make it slightly larger than the hole to cover the mask edge perfectly
    shape_size_inches = (S / 144.0) * 1.05 
    
    left = (13.333 - shape_size_inches) / 2
    top = (7.5 - shape_size_inches) / 2

    center_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        Inches(left), Inches(top), 
        Inches(shape_size_inches), Inches(shape_size_inches)
    )
    center_shape.rotation = 45
    center_shape.adjustments[0] = 0.25 # Adjust roundness

    # White thick outline
    center_shape.line.color.rgb = RGBColor(255, 255, 255)
    center_shape.line.width = Pt(3)

    # Inject Gradient and Shadow via lxml
    spPr = center_shape.element.spPr
    # Clear default fills/effects
    for tag in ['solidFill', 'gradFill', 'pattFill', 'noFill', 'blipFill']:
        el = spPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}{tag}')
        if el is not None: spPr.remove(el)
    el = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    if el is not None: spPr.remove(el)

    gradFill_xml = f"""
    <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rotWithShape="1">
      <a:gsLst>
        <a:gs pos="0"><a:srgbClr val="{gradient_colors[0]}"><a:alpha val="90000"/></a:srgbClr></a:gs>
        <a:gs pos="100000"><a:srgbClr val="{gradient_colors[1]}"><a:alpha val="90000"/></a:srgbClr></a:gs>
      </a:gsLst>
      <a:lin ang="3240000" scaled="1"/>
    </a:gradFill>
    """
    effectLst_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:outerShdw blurRad="200000" dist="80000" dir="2700000" algn="ctr" rotWithShape="0">
        <a:srgbClr val="000000"><a:alpha val="50000"/></a:srgbClr>
      </a:outerShdw>
    </a:effectLst>
    """
    
    ln = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
    if ln is not None:
        ln.addprevious(parse_xml(gradFill_xml))
    else:
        spPr.append(parse_xml(gradFill_xml))
    spPr.append(parse_xml(effectLst_xml))

    # === Layer 4: Text ===
    # Using a separate unrotated text box so the text remains horizontal
    tx_width = Inches(4)
    tx_height = Inches(1.5)
    tx_left = (13.333 - 4) / 2
    tx_top = (7.5 - 1.5) / 2
    
    tb = slide.shapes.add_textbox(Inches(tx_left), Inches(tx_top), tx_width, tx_height)
    tf = tb.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    
    font = p.font
    font.name = 'Arial'
    font.size = Pt(54)
    font.bold = True
    font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
