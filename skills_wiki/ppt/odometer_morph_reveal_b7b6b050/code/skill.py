def create_slide(
    output_pptx_path: str,
    title_text: str = "MOUNT EVEREST",
    start_number: str = "0000",
    end_number: str = "8848",
    unit_text: str = "m",
    bg_theme: str = "mountain,peak",
    **kwargs,
) -> str:
    """
    Creates a 2-slide presentation demonstrating the Odometer Morph Reveal.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    from lxml import etree

    # --- Helper 1: Generate the vertical number strip (0-9) ---
    def create_digit_strip(filename="digit_strip.png"):
        width, block_height = 200, 250
        height = block_height * 10
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to load a bold font
        font = None
        for font_name in ['arialbd.ttf', 'Arial Bold.ttf', 'DejaVuSans-Bold.ttf', 'arial.ttf']:
            try:
                font = ImageFont.truetype(font_name, 200)
                break
            except IOError:
                continue
        if not font:
            font = ImageFont.load_default()

        for d in range(10):
            text = str(d)
            # Center the text in its block
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            x = (width - text_w) / 2
            y = (d * block_height) + ((block_height - text_h) / 2) - bbox[1]

            # Draw Shadow
            draw.text((x+5, y+8), text, font=font, fill=(0, 0, 0, 150))
            # Draw White Text
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
            
        # Apply a slight blur to the whole image to soften the shadow, then redraw text sharp
        # To do this properly, we could separate layers, but a simple drop shadow text works well enough
        img.save(filename)
        return filename, width, block_height * 10

    # --- Helper 2: Download Background Image ---
    def get_background(filename="bg.jpg", theme="mountain"):
        url = f"https://source.unsplash.com/1600x900/?{theme}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
                out_file.write(response.read())
            return filename
        except Exception:
            # Fallback gradient
            img = Image.new('RGB', (1600, 900))
            draw = ImageDraw.Draw(img)
            for y in range(900):
                r = int(13 + (0 - 13) * (y / 900))
                g = int(17 + (191 - 17) * (y / 900))
                b = int(28 + (255 - 28) * (y / 900))
                draw.line([(0, y), (1600, y)], fill=(r, g, b))
            img.save(filename)
            return filename

    # --- Helper 3: Inject Morph Transition XML ---
    def apply_morph(slide):
        # We need to insert <p:transition spd="slow"><p14:morph/></p:transition>
        p_sld = slide.element
        
        # Remove existing transition if any
        trans = p_sld.find("{http://schemas.openxmlformats.org/presentationml/2006/main}transition")
        if trans is not None:
            p_sld.remove(trans)
            
        # Add morph transition
        nsmap = {
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'
        }
        trans_el = etree.Element("{http://schemas.openxmlformats.org/presentationml/2006/main}transition", spd="slow", nsmap=nsmap)
        morph_el = etree.SubElement(trans_el, "{http://schemas.microsoft.com/office/powerpoint/2010/main}morph")
        
        # Insert transition near the beginning of the slide element properties
        p_sld.insert(1, trans_el)

    # --- Helper 4: Rename Shape for Morph Linking ---
    def set_shape_name(shape, name):
        shape.element.nvPicPr.cNvPr.set('name', name)

    # Prepare assets
    strip_path, strip_w, strip_h = create_digit_strip()
    bg_path = get_background(theme=bg_theme)

    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Pad strings to be equal length
    max_len = max(len(start_number), len(end_number))
    start_number = start_number.rjust(max_len, '0')
    end_number = end_number.rjust(max_len, '0')

    # Layout calculations
    num_chars = len(start_number)
    char_width = 1.2  # width per digit in inches
    total_width = num_chars * char_width
    start_x = (13.333 - total_width) / 2
    y_pos = 2.0  # vertical center roughly
    digit_height = 1.8 # height of displayed digit

    # Generate the two slides
    slides_data = [
        (start_number, prs.slides.add_slide(prs.slide_layouts[6])),
        (end_number, prs.slides.add_slide(prs.slide_layouts[6]))
    ]

    for slide_idx, (number_str, slide) in enumerate(slides_data):
        # 1. Background
        slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

        # 2. Add digits
        for i, char in enumerate(number_str):
            x = start_x + (i * char_width)
            
            if char.isdigit():
                d = int(char)
                # To make the cropped shape exactly char_width x digit_height:
                # The inserted image must have the height of 10 * digit_height
                pic = slide.shapes.add_picture(strip_path, Inches(x), Inches(y_pos), Inches(char_width), Inches(digit_height * 10))
                
                # Crop percentages (0.0 to 1.0)
                crop_top = d / 10.0
                crop_bottom = 1.0 - ((d + 1) / 10.0)
                
                pic.crop_top = crop_top
                pic.crop_bottom = crop_bottom
                
                # Force rename so Morph knows they are the same object across slides
                set_shape_name(pic, f"!!Digit_{i}")
            else:
                # Handle commas or dots
                txBox = slide.shapes.add_textbox(Inches(x), Inches(y_pos), Inches(char_width), Inches(digit_height))
                tf = txBox.text_frame
                p = tf.add_paragraph()
                p.text = char
                p.font.size = Pt(120)
                p.font.color.rgb = RGBColor(255, 255, 255)
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER
                txBox.element.nvSpPr.cNvPr.set('name', f"!!Static_{i}")

        # 3. Add Labels
        # Title Label (bottom left)
        tx_title = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(5), Inches(1))
        tf_title = tx_title.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text.upper()
        p_title.font.size = Pt(20)
        p_title.font.color.rgb = RGBColor(200, 200, 200)
        p_title.font.letter_spacing = Pt(5)

        # Unit Label (next to numbers)
        tx_unit = slide.shapes.add_textbox(Inches(start_x + total_width), Inches(y_pos + 0.5), Inches(2), Inches(1))
        p_unit = tx_unit.text_frame.paragraphs[0]
        p_unit.text = unit_text
        p_unit.font.size = Pt(60)
        p_unit.font.color.rgb = RGBColor(255, 255, 255)

        # 4. Apply Morph to the second slide
        if slide_idx == 1:
            apply_morph(slide)

    prs.save(output_pptx_path)
    
    # Cleanup temp files
    if os.path.exists(strip_path): os.remove(strip_path)
    if os.path.exists(bg_path): os.remove(bg_path)
    
    return output_pptx_path
