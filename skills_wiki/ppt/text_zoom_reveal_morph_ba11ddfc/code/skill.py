def create_slide(
    output_pptx_path: str,
    title_text: str = "INDIA",
    bg_image_keyword: str = "india",
    font_name: str = "Montserrat",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Text Zoom-Reveal Morph effect.

    This effect uses a text-shaped mask that expands via the Morph transition
    to reveal a background image, creating a "zoom through text" animation.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The word to use for the text mask (all caps recommended).
        bg_image_keyword: A keyword to search for a background image on Unsplash.
        font_name: The name of the bold font to use (will be downloaded from Google Fonts).

    Returns:
        The path to the saved PPTX file.
    """
    import io
    import os
    import urllib.request
    from lxml import etree
    from PIL import Image, ImageDraw, ImageFont
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu

    # --- Helper function to download resources ---
    def download_resource(url, local_path, is_json=False):
        if os.path.exists(local_path):
            return local_path
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
                if is_json:
                    out_file.write(response.read())
                else:
                    data = response.read()
                    out_file.write(data)
            return local_path
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return None

    # --- Helper function to inject Morph transition XML ---
    def set_morph_transition(slide):
        slide_element = slide._element
        transition_element = etree.SubElement(slide_element, "{http://schemas.openxmlformats.org/presentationml/2006/main}transition")
        morph_element = etree.SubElement(transition_element, "{http://schemas.openxmlformats.org/presentationml/2006/main}morph")

    # --- Helper function to create the text mask ---
    def create_text_mask_image(text, font_path, width_px, height_px):
        img = Image.new('RGB', (width_px, height_px), color='black')
        draw = ImageDraw.Draw(img)
        
        try:
            font_size = int(height_px / 3)
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Font not found at {font_path}, using default.")
            font = ImageFont.load_default()

        # Find the right font size to fit the text
        while font.getbbox(text)[2] < width_px * 0.8:
            font_size += 2
            font = ImageFont.truetype(font_path, font_size)
        
        while font.getbbox(text)[2] > width_px * 0.9:
            font_size -= 2
            font = ImageFont.truetype(font_path, font_size)
            
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((width_px - text_width) / 2, (height_px - text_height) / 2 - bbox[1])
        draw.text(position, text, font=font, fill='white')

        # Convert to RGBA and make white parts transparent
        img = img.convert("RGBA")
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((0, 0, 0, 0))  # Make white transparent
            else:
                new_data.append(item) # Keep black opaque
        img.putdata(new_data)
        
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()

    # --- Main Presentation Logic ---
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_slide_layout = prs.slide_layouts[6]
    
    slide_width_px, slide_height_px = 1920, 1080

    # Download font (Montserrat Black)
    font_url = "https://fonts.gstatic.com/s/montserrat/v25/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtr6Hw5aXo.ttf"
    font_local_path = "Montserrat-Black.ttf"
    font_path = download_resource(font_url, font_local_path)
    if not font_path:
        raise FileNotFoundError("Could not download the required font.")

    # Download background image
    bg_url = f"https://source.unsplash.com/{slide_width_px}x{slide_height_px}/?{bg_image_keyword}"
    bg_image_path = "background.jpg"
    download_resource(bg_url, bg_image_path)
    if not os.path.exists(bg_image_path):
         # Create a fallback gradient if download fails
        img = Image.new('RGB', (slide_width_px, slide_height_px), '#1E3A8A')
        img.save(bg_image_path)

    # Generate the text mask in memory
    mask_bytes = create_text_mask_image(title_text.upper(), font_path, slide_width_px, slide_height_px)

    # === Slide 1: The Initial State ===
    slide1 = prs.slides.add_slide(blank_slide_layout)
    slide1.shapes.add_picture(bg_image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    slide1.shapes.add_picture(io.BytesIO(mask_bytes), 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Slide 2: The Final (Zoomed) State ===
    slide2 = prs.slides.add_slide(blank_slide_layout)
    slide2.shapes.add_picture(bg_image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # Add the same mask, but scaled up dramatically and repositioned to stay centered
    scale_factor = 30
    new_width = prs.slide_width * scale_factor
    new_height = prs.slide_height * scale_factor
    new_left = (prs.slide_width - new_width) // 2
    new_top = (prs.slide_height - new_height) // 2
    slide2.shapes.add_picture(io.BytesIO(mask_bytes), new_left, new_top, width=new_width, height=new_height)

    # Apply the Morph transition to the second slide
    set_morph_transition(slide2)

    prs.save(output_pptx_path)
    
    # Clean up downloaded files
    if os.path.exists(bg_image_path): os.remove(bg_image_path)
    # You might want to keep the font file cached
    # if os.path.exists(font_local_path): os.remove(font_local_path)
    
    return output_pptx_path
