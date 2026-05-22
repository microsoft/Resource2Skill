def create_slide(
    output_pptx_path: str,
    title_text: str = "Food economics",
    button_text: str = "SELECT",
    bg_theme_keyword: str = "wheat,calculator,money",
    accent_color: tuple = (244, 121, 32),
    **kwargs,
) -> str:
    """
    Creates a PPTX file with 4 slides demonstrating an animated Glassmorphism panel effect.
    The effect is achieved by setting up slides for a Morph transition.

    Returns: path to the saved PPTX file.
    """
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageFilter, ImageDraw, ImageFont

    from lxml import etree
    from pptx.oxml.xmlchemy import OxmlElement

    # Helper function to add a soft drop shadow to a shape
    def add_shadow_to_shape(shape, blur_radius_pt=15, distance_pt=10, angle_deg=45, alpha_pct=40):
        spPr = shape.element.spPr
        # Create <a:effectLst> if it doesn't exist
        effectLst = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
        if effectLst is None:
            effectLst = OxmlElement("a:effectLst")
            spPr.append(effectLst)
        
        # Define the outer shadow effect
        shadow = OxmlElement("a:outerShdw")
        shadow.set("blurRad", str(Emu(Pt(blur_radius_pt))))
        shadow.set("dist", str(Emu(Pt(distance_pt))))
        shadow.set("dir", str(angle_deg * 60000))
        shadow.set("algn", "tl") # Top-left alignment
        shadow.set("rotWithShape", "0")
        
        # Add color with alpha
        srgbClr = OxmlElement("a:srgbClr")
        srgbClr.set("val", "000000")
        alpha_el = OxmlElement("a:alpha")
        alpha_el.set("val", str(alpha_pct * 1000)) # Alpha is in 1/1000ths of a percent
        srgbClr.append(alpha_el)
        shadow.append(srgbClr)
        
        effectLst.append(shadow)

    # Helper function to set Morph transition
    def set_morph_transition(slide):
        slide_xml = slide.element
        transition_xml = etree.fromstring(
            f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            f'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            f'p14:dur="1000" advTm="0">'
            f'<p14:morph option="byObject"/>'
            f'</p:transition>'
        )
        # Find the correct namespace map
        nsmap = {k: v for k, v in slide_xml.nsmap.items() if k}
        nsmap['p14'] = 'http://schemas.microsoft.com/office/powerpoint/2010/main'

        # Create a new transition element with the correct namespace
        new_transition = etree.Element(
            '{' + nsmap['p'] + '}transition',
            nsmap=nsmap
        )
        new_transition.set('{http://schemas.microsoft.com/office/powerpoint/2010/main}dur', "700") # 0.7 seconds
        
        morph_element = etree.Element(
            '{' + nsmap['p14'] + '}morph',
            nsmap=nsmap
        )
        morph_element.set('option', 'byObject')
        new_transition.append(morph_element)
        
        # Remove old transition if it exists and add the new one
        existing_transition = slide_xml.find('.//p:transition')
        if existing_transition is not None:
            slide_xml.remove(existing_transition)
        slide_xml.insert(0, new_transition)

    prs = Presentation()
    SLIDE_WIDTH, SLIDE_HEIGHT = Inches(13.333), Inches(7.5)
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # --- Fetch and prepare background image
    try:
        url = f"https://source.unsplash.com/1920x1080/?{bg_theme_keyword}"
        with urllib.request.urlopen(url) as response:
            bg_image_data = io.BytesIO(response.read())
        bg_pil_image = Image.open(bg_image_data).convert("RGBA")
    except Exception:
        # Fallback to a gradient if image download fails
        bg_pil_image = Image.new("RGBA", (int(SLIDE_WIDTH), int(SLIDE_HEIGHT)), (10, 10, 30))
        draw = ImageDraw.Draw(bg_pil_image)
        for i in range(int(SLIDE_HEIGHT)):
            ratio = i / SLIDE_HEIGHT
            color = (int(10 + ratio * 30), int(10 + ratio * 30), int(30 + ratio * 40), 255)
            draw.line([(0, i), (SLIDE_WIDTH, i)], fill=color)
        bg_image_data = io.BytesIO()
        bg_pil_image.save(bg_image_data, format='PNG')
        bg_image_data.seek(0)
    
    # --- Panel geometry
    panel_width, panel_height = Inches(3.5), Inches(5)
    panel_positions = [
        Inches(0.5),
        (SLIDE_WIDTH - panel_width) / 2,
        SLIDE_WIDTH - panel_width - Inches(0.5),
        (SLIDE_WIDTH - panel_width) / 2
    ]

    for i, panel_left_emu in enumerate(panel_positions):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        if i > 0:
            set_morph_transition(slide)

        # Layer 1: Background Image
        slide.shapes.add_picture(bg_image_data, 0, 0, width=SLIDE_WIDTH, height=SLIDE_HEIGHT)

        # Layer 2: Glassmorphism Panel
        panel_top_emu = (SLIDE_HEIGHT - panel_height) / 2
        
        # Crop, blur, and save the background section
        box = (
            int(panel_left_emu / 914400 * 96), # Emu to px
            int(panel_top_emu / 914400 * 96),
            int((panel_left_emu + panel_width) / 914400 * 96),
            int((panel_top_emu + panel_height) / 914400 * 96),
        )
        cropped_bg = bg_pil_image.crop(box)
        blurred_bg = cropped_bg.filter(ImageFilter.GaussianBlur(radius=20))
        
        blurred_bg_data = io.BytesIO()
        blurred_bg.save(blurred_bg_data, format='PNG')
        
        # Create the panel shape and fill it with the blurred image
        panel_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, panel_left_emu, panel_top_emu, panel_width, panel_height)
        panel_shape.name = f"GlassPanel_Slide{i}" # Naming is crucial for Morph
        panel_shape.fill.solid()
        panel_shape.fill.fore_color.rgb = RGBColor(255, 255, 255) # Placeholder
        panel_shape.element.spPr.blipFill.blip.embed = slide.part.relate_to_image_part(blurred_bg_data).rId

        # Add border
        line = panel_shape.line
        line.color.rgb = RGBColor(255, 255, 255)
        line.color.brightness = 0.2
        line.width = Pt(1.5)
        
        # Add shadow
        add_shadow_to_shape(panel_shape)

        # Layer 3: Content
        # Small image on top
        icon_size = Inches(1.5)
        icon_left = panel_left_emu + (panel_width - icon_size) / 2
        icon_top = panel_top_emu + Inches(0.5)
        # Using a simple shape as a placeholder for the cereal bowl
        icon_shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, icon_left, icon_top, icon_size, icon_size)
        icon_shape.name = f"Icon_Slide{i}"
        icon_shape.fill.solid()
        icon_shape.fill.fore_color.rgb = RGBColor(255, 223, 186)
        icon_shape.line.fill.background()

        # Title Text
        title_box = slide.shapes.add_textbox(
            panel_left_emu, icon_top + icon_size, panel_width, Inches(1)
        )
        title_box.name = f"Title_Slide{i}"
        title_p = title_box.text_frame.paragraphs[0]
        title_p.text = title_text
        title_p.font.name = "Arial Black"
        title_p.font.size = Pt(28)
        title_p.font.color.rgb = RGBColor(255, 255, 255)
        title_p.alignment = 1 # Center

        # Button
        btn_width, btn_height = Inches(2), Inches(0.5)
        btn_left = panel_left_emu + (panel_width - btn_width) / 2
        btn_top = panel_top_emu + panel_height - Inches(1.2)
        button_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, btn_left, btn_top, btn_width, btn_height)
        button_shape.name = f"Button_Slide{i}"
        button_shape.fill.solid()
        button_shape.fill.fore_color.rgb = RGBColor.from_string(f"{accent_color[0]:02x}{accent_color[1]:02x}{accent_color[2]:02x}")
        button_shape.line.fill.background()
        button_shape.text = button_text
        button_p = button_shape.text_frame.paragraphs[0]
        button_p.font.bold = True
        button_p.font.color.rgb = RGBColor(255, 255, 255)
        button_p.alignment = 1 # Center

    prs.save(output_pptx_path)
    return output_pptx_path
