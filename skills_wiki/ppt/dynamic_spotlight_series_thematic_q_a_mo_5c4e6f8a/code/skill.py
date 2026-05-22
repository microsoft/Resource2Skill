def create_slide(
    output_pptx_path: str,
    series_title: str = "Employee Spotlight",
    person_name: str = "Jimmy Pineda",
    person_role: str = "Financial Analyst",
    topic_1: str = "L.A. Native",
    topic_2: str = "Skateboarding Dreams",
    **kwargs,
) -> str:
    """
    Creates a dynamic, multi-slide "Spotlight Series" presentation using 
    custom Freeform polygons, PIL generated assets, and Morph transitions.
    """
    import os
    import urllib.request
    from io import BytesIO
    from PIL import Image, ImageDraw
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    import lxml.etree
    
    # -------------------------------------------------------------------------
    # Helper: Morph Naming Contract
    # -------------------------------------------------------------------------
    try:
        from _shell_helpers import set_morph_anchor
    except ImportError:
        def set_morph_anchor(shape, role):
            # Fallback: PPTX uses !! prefix to force match shapes for Morph
            shape.name = f"!!{role}_{shape.name}"

    # -------------------------------------------------------------------------
    # Helper: Set Shape Transparency (lxml injection)
    # -------------------------------------------------------------------------
    def apply_transparency(shape, opacity_percent: float):
        """Injects alpha transparency into a python-pptx shape's solid fill."""
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255) # Force SRGB element creation
        
        # Find the srgbClr element
        srgbClr_list = shape.element.xpath('.//a:srgbClr')
        if srgbClr_list:
            srgbClr = srgbClr_list[0]
            # Convert 0.0-1.0 float to 0-100000 format expected by OpenXML
            alpha_val = int(opacity_percent * 100000)
            alpha_el = lxml.etree.SubElement(
                srgbClr, 
                '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha'
            )
            alpha_el.set('val', str(alpha_val))

    # -------------------------------------------------------------------------
    # Helper: Apply Morph Transition to Slide
    # -------------------------------------------------------------------------
    def apply_morph_to_slide(slide):
        """Injects Morph transition into the slide's XML."""
        transition = lxml.etree.Element('{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
        transition.set('spd', 'slow')
        lxml.etree.SubElement(transition, '{http://schemas.openxmlformats.org/presentationml/2006/main}morph')
        # Insert transition as the second element (after sldPr)
        slide.element.insert(1, transition)

    # -------------------------------------------------------------------------
    # Asset Generation
    # -------------------------------------------------------------------------
    # 1. Background Gradient
    bg_path = "temp_bg.png"
    bg_img = Image.new('RGB', (1280, 720))
    draw_bg = ImageDraw.Draw(bg_img)
    color_top = (210, 225, 240)
    color_bottom = (245, 250, 255)
    for y in range(720):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / 720))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / 720))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / 720))
        draw_bg.line([(0, y), (1280, y)], fill=(r, g, b))
    bg_img.save(bg_path)

    # 2. Spotlight Vector-style Icon (Drawn programmatically)
    icon_path = "temp_spotlight.png"
    icon_img = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
    draw_icon = ImageDraw.Draw(icon_img)
    base_color = (13, 71, 120, 255)
    white_line = (255, 255, 255, 255)
    
    # Mount bracket
    draw_icon.rectangle([130, 20, 170, 100], fill=base_color, outline=white_line, width=4)
    # Swivel joint
    draw_icon.ellipse([120, 80, 180, 140], fill=base_color, outline=white_line, width=4)
    # Conical Housing
    draw_icon.polygon([(150, 110), (250, 250), (50, 250)], fill=base_color, outline=white_line, width=4)
    # Lens
    draw_icon.ellipse([40, 220, 260, 280], fill=(200, 230, 255, 255), outline=white_line, width=4)
    icon_img.save(icon_path)

    # 3. Profile Photo (Fetch a generic headshot if available)
    photo_path = "temp_photo.jpg"
    try:
        req = urllib.request.Request(
            'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=600&h=600&fit=crop',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read()))
            img.save(photo_path)
    except Exception:
        # Fallback to a solid block if download fails
        fallback = Image.new('RGB', (600, 600), (100, 140, 180))
        fallback.save(photo_path)


    # -------------------------------------------------------------------------
    # Presentation Setup
    # -------------------------------------------------------------------------
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    DARK_BLUE = RGBColor(13, 71, 120)
    LIGHT_BLUE = RGBColor(110, 150, 190)

    # =========================================================================
    # SLIDE 1: Hero Intro Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # 1. Top Banner
    banner = slide1.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(1.5)) # 1 = MSO_SHAPE.RECTANGLE
    banner.fill.solid()
    banner.fill.fore_color.rgb = DARK_BLUE
    banner.line.fill.background()
    
    # 2. Top Banner Text
    tb = slide1.shapes.add_textbox(Inches(2.5), Inches(0.25), Inches(8), Inches(1))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = series_title
    p.font.name = "Arial"
    p.font.size = Pt(48)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # 3. Beam (Using FreeformBuilder for morphing capability)
    ff1 = slide1.shapes.build_freeform()
    # Beam angles from top-left outwards
    ff1.add_line_segments([
        (Inches(1.0), Inches(1.0)), 
        (Inches(13.333), Inches(0.0)), 
        (Inches(13.333), Inches(3.0)), 
        (Inches(1.0), Inches(1.5))
    ], close=True)
    beam1 = ff1.convert_to_shape()
    beam1.line.fill.background()
    apply_transparency(beam1, opacity_percent=0.25)
    set_morph_anchor(beam1, "brand_mark")  # Match tag across slides

    # 4. Spotlight Icon
    spot1 = slide1.shapes.add_picture(icon_path, Inches(0.2), Inches(0.2), Inches(1.8), Inches(1.8))
    spot1.rotation = -40  # Pointing down-right
    set_morph_anchor(spot1, "accent_orb")

    # 5. Profile Picture
    pic = slide1.shapes.add_picture(photo_path, Inches(8.5), Inches(2.2), Inches(4), Inches(4))
    
    # 6. Role & Name
    role_box = slide1.shapes.add_textbox(Inches(1.5), Inches(3.0), Inches(6), Inches(0.8))
    role_box.text_frame.text = person_role
    role_box.text_frame.paragraphs[0].font.size = Pt(28)
    role_box.text_frame.paragraphs[0].font.color.rgb = LIGHT_BLUE
    
    name_box = slide1.shapes.add_textbox(Inches(1.4), Inches(3.8), Inches(6), Inches(2.5))
    p = name_box.text_frame.paragraphs[0]
    p.text = person_name.replace(" ", "\n") # Stack the name
    p.font.size = Pt(85)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.line_spacing = 0.9

    apply_morph_to_slide(slide1)


    # =========================================================================
    # SLIDE 2: Topic 1
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # Beam 2 - Angled lower, sweeping towards center
    ff2 = slide2.shapes.build_freeform()
    ff2.add_line_segments([
        (Inches(1.0), Inches(1.0)), 
        (Inches(13.333), Inches(2.0)), 
        (Inches(13.333), Inches(5.5)), 
        (Inches(1.0), Inches(1.5))
    ], close=True)
    beam2 = ff2.convert_to_shape()
    beam2.line.fill.background()
    apply_transparency(beam2, opacity_percent=0.25)
    set_morph_anchor(beam2, "brand_mark")

    # Spotlight Icon 2 - Rotated further down
    spot2 = slide2.shapes.add_picture(icon_path, Inches(0.2), Inches(0.2), Inches(1.8), Inches(1.8))
    spot2.rotation = -20 
    set_morph_anchor(spot2, "accent_orb")

    # Topic Text
    topic_box = slide2.shapes.add_textbox(Inches(2.0), Inches(3.0), Inches(9.333), Inches(2.0))
    p = topic_box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = topic_1
    p.font.size = Pt(72)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    apply_morph_to_slide(slide2)


    # =========================================================================
    # SLIDE 3: Topic 2
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    slide3.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # Beam 3 - Sweeping even lower
    ff3 = slide3.shapes.build_freeform()
    ff3.add_line_segments([
        (Inches(1.0), Inches(1.0)), 
        (Inches(13.333), Inches(4.0)), 
        (Inches(13.333), Inches(7.5)), 
        (Inches(1.0), Inches(1.5))
    ], close=True)
    beam3 = ff3.convert_to_shape()
    beam3.line.fill.background()
    apply_transparency(beam3, opacity_percent=0.25)
    set_morph_anchor(beam3, "brand_mark")

    # Spotlight Icon 3 - Pointing steep
    spot3 = slide3.shapes.add_picture(icon_path, Inches(0.2), Inches(0.2), Inches(1.8), Inches(1.8))
    spot3.rotation = 0 
    set_morph_anchor(spot3, "accent_orb")

    # Topic Text
    topic_box3 = slide3.shapes.add_textbox(Inches(2.0), Inches(3.0), Inches(9.333), Inches(2.0))
    p = topic_box3.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = topic_2
    p.font.size = Pt(72)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    apply_morph_to_slide(slide3)


    # Cleanup temporary assets
    prs.save(output_pptx_path)
    for tmp_file in [bg_path, icon_path, photo_path]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

    return output_pptx_path
