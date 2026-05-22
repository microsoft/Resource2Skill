def create_slide(
    output_pptx_path: str,
    title_text: str = "GLASS MORPHIC",
    image_url: str = "https://images.unsplash.com/photo-1517852119568-a06715b806b5",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a Glassmorphism effect.

    This effect places a shape on the slide that appears to be a frosted glass panel,
    blurring the background image behind it.

    Args:
        output_pptx_path (str): The path to save the generated .pptx file.
        title_text (str): The text to display on the glass panel.
        image_url (str): The URL of the background image to use.

    Returns:
        str: The path to the saved .pptx file.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.dml import MSO_THEME_COLOR
    from PIL import Image, ImageFilter
    from lxml import etree

    # Create presentation and slide
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- 1. Prepare Background Images ---
    # Download image and create temp paths
    temp_dir = "temp_assets"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    original_image_path = os.path.join(temp_dir, "background.jpg")
    blurred_image_path = os.path.join(temp_dir, "background_blurred.png")

    try:
        urllib.request.urlretrieve(image_url, original_image_path)
        # Create blurred version with PIL
        with Image.open(original_image_path) as img:
            blurred_img = img.filter(ImageFilter.GaussianBlur(radius=50))
            blurred_img.save(blurred_image_path, "PNG")
    except Exception as e:
        print(f"Failed to download or process image: {e}. Using a fallback.")
        # Fallback: create a dummy image if download fails
        img = Image.new('RGB', (1920, 1080), color = 'rgb(73, 109, 137)')
        img.save(original_image_path)
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=50))
        blurred_img.save(blurred_image_path, "PNG")

    # --- 2. Build Slide Layers ---
    # Layer 1: Set slide background to the BLURRED image
    slide.background.fill.picture(blurred_image_path)

    # Layer 2: Add the ORIGINAL, sharp image as a full-slide picture
    slide.shapes.add_picture(
        original_image_path, 0, 0, 
        width=prs.slide_width, height=prs.slide_height
    )

    # --- 3. Create the Glassmorphism Shape ---
    # Layer 3: Add the rounded rectangle that will become the glass panel
    left = Inches(4.5)
    top = Inches(3.5)
    width = Inches(7)
    height = Inches(2)
    
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)

    # Set shape fill to "Slide background fill"
    shape.fill.background()

    # Set shape outline
    line = shape.line
    line.color.rgb = RGBColor(255, 255, 255)
    line.width = Pt(1.5)
    
    # --- 4. Add Frosted Edge using lxml for Inner Shadow ---
    def set_inner_shadow(shape, blur_radius_pt, color_rgb):
        shape_element = shape.element
        spPr = shape_element.get_or_add_spPr()
        
        effect_list = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
        if effect_list is None:
            effect_list = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
        
        inner_shadow = etree.SubElement(effect_list, "{http://schemas.openxmlformats.org/drawingml/2006/main}innerShdw")
        inner_shadow.set("blurRad", str(Emu(Pt(blur_radius_pt))))
        inner_shadow.set("dist", "0")
        
        srgb_clr = etree.SubElement(inner_shadow, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
        srgb_clr.set("val", f"{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
        
        alpha = etree.SubElement(srgb_clr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
        alpha.set("val", "85000") # 85% opacity

    set_inner_shadow(shape, 30, (255, 255, 255))

    # --- 5. Add Text to the Panel ---
    text_frame = shape.text_frame
    text_frame.clear() 
    p = text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = 'Poppins ExtraBold'
    p.font.size = Pt(48)
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Add a drop shadow to the text for better contrast
    shadow = p.font.shadow
    shadow.color.rgb = RGBColor(0, 0, 0)
    shadow.blur_radius = Emu(Pt(2))
    shadow.distance = Emu(Pt(2))
    shadow.alpha_int = 150 * 1000 # 50% opacity in 100,000ths

    # --- 6. Save and Clean up ---
    prs.save(output_pptx_path)
    os.remove(original_image_path)
    os.remove(blurred_image_path)
    os.rmdir(temp_dir)
    
    return output_pptx_path

