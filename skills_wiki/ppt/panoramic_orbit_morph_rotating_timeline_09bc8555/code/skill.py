def create_slide(
    output_pptx_path: str,
    title_text: str = "Rotating Timeline",
    body_text: str = "",
    bg_palette: str = "cityscape",
    accent_color: tuple = (214, 175, 140),
    **kwargs,
) -> str:
    """
    Creates a 3-slide presentation reproducing the "Panoramic Orbit Morph" timeline.
    """
    import os
    import math
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 1. Download Background Image
    bg_img_path = "temp_panoramic_bg.jpg"
    try:
        url = f"https://source.unsplash.com/featured/2000x1000/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bg_img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback to a generated solid image if download fails
        img = Image.new('RGB', (2000, 1000), color=(40, 45, 55))
        img.save(bg_img_path)

    # 2. Generate Semi-Transparent Dark Overlay using PIL
    overlay_path = "temp_overlay.png"
    # 60% opacity black (153 out of 255)
    overlay = Image.new('RGBA', (100, 100), (0, 0, 0, 153))
    overlay.save(overlay_path)

    # Transition Injector Helper
    def add_morph_transition(slide):
        xml = '<p:transition spd="slow" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:morph option="byObject"/></p:transition>'
        transition = parse_xml(xml)
        slide.element.append(transition)

    # --- Design Parameters ---
    total_slides = 3
    planet_cx = Inches(0.5)
    planet_cy = Inches(3.75)
    planet_radius = Inches(3.0)
    
    orbit_radius = Inches(4.5)
    
    # Base angles for the 6 nodes (in degrees, 0 is 3 o'clock). 
    # Positive angles go UP in our math logic.
    base_angles = [70, 50, 30, 10, -10, -30]
    
    content_data = [
        {"title": "Research and Analysis", "body": "Fusce tristique massa eget finibus iaculis. Vestibulum convallis tortor ac dictum tincidunt.\n\nEt venenatis tortor justo et sem. Etiam in pellentesque massa."},
        {"title": "Wireframing", "body": "Creating the structural blueprint of the digital experience. Defining hierarchy, navigation, and user flow without the distraction of visual aesthetics."},
        {"title": "Prototyping", "body": "Bringing the wireframes to life. Building interactive models to test functionality, uncover usability flaws, and validate the core concept before development."}
    ]

    # Generate Slides
    for i in range(total_slides):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # A. Background Image (Pan left by 2 inches per slide)
        slide.shapes.add_picture(bg_img_path, Inches(-2.0 * i), Inches(0), width=Inches(20), height=Inches(7.5))
        
        # B. Dark Overlay (covers entire slide)
        slide.shapes.add_picture(overlay_path, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

        # C. The "Planet"
        planet = slide.shapes.add_shape(
            5, # MSO_SHAPE.OVAL
            planet_cx - planet_radius, planet_cy - planet_radius, 
            planet_radius * 2, planet_radius * 2
        )
        planet.fill.solid()
        planet.fill.fore_color.rgb = RGBColor(*accent_color)
        planet.line.fill.background()
        
        # Planet Title Text
        tx_box = slide.shapes.add_textbox(planet_cx - Inches(2), planet_cy - Inches(0.5), Inches(4), Inches(1))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = "Web UX Design"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

        # D. The "Orbit" Line
        orbit = slide.shapes.add_shape(
            5, # MSO_SHAPE.OVAL
            planet_cx - orbit_radius, planet_cy - orbit_radius, 
            orbit_radius * 2, orbit_radius * 2
        )
        orbit.fill.background() # No fill
        orbit.line.color.rgb = RGBColor(200, 200, 200)
        orbit.line.width = Pt(1.5)
        
        # E. Timeline Nodes
        # For slide i, rotate all nodes "up" by i * 20 degrees
        rotation_offset = i * 20
        
        for node_idx, base_angle in enumerate(base_angles):
            current_angle = base_angle + rotation_offset
            rad = math.radians(current_angle)
            
            # Calculate coordinates (PPT Y-axis goes down, so we subtract sin)
            nx = planet_cx + orbit_radius * math.cos(rad)
            ny = planet_cy - orbit_radius * math.sin(rad)
            
            is_active = (node_idx == i)
            node_r = Inches(0.12) if is_active else Inches(0.08)
            
            # Add node circle
            node = slide.shapes.add_shape(5, nx - node_r, ny - node_r, node_r * 2, node_r * 2)
            node.fill.solid()
            node.fill.fore_color.rgb = RGBColor(255, 255, 255)
            node.line.fill.background()
            
            # Add node label (PART 01, etc.)
            lbl_box = slide.shapes.add_textbox(nx - Inches(1.2), ny - Inches(0.2), Inches(1), Inches(0.4))
            lbl_p = lbl_box.text_frame.paragraphs[0]
            lbl_p.text = f"PART 0{node_idx + 1}"
            lbl_p.font.size = Pt(12)
            lbl_p.font.bold = is_active
            lbl_p.alignment = PP_ALIGN.RIGHT
            
            if is_active:
                lbl_p.font.color.rgb = RGBColor(255, 255, 255)
                # F. Add main content text for the active node
                # Placed statically on the right side of the slide
                content_x = Inches(6.5)
                content_y = ny - Inches(0.5) # Align slightly with the active node
                
                title_box = slide.shapes.add_textbox(content_x, content_y, Inches(6), Inches(1))
                t_p = title_box.text_frame.paragraphs[0]
                t_p.text = content_data[node_idx]["title"]
                t_p.font.size = Pt(36)
                t_p.font.bold = True
                t_p.font.color.rgb = RGBColor(255, 255, 255)
                
                body_box = slide.shapes.add_textbox(content_x, content_y + Inches(0.8), Inches(5.5), Inches(2))
                b_p = body_box.text_frame.paragraphs[0]
                b_p.text = content_data[node_idx]["body"]
                b_p.font.size = Pt(16)
                b_p.font.color.rgb = RGBColor(220, 220, 220)
                body_box.text_frame.word_wrap = True
            else:
                lbl_p.font.color.rgb = RGBColor(160, 160, 160)

        # Apply Morph Transition via XML injection
        add_morph_transition(slide)

    # Cleanup temporary files
    if os.path.exists(bg_img_path): os.remove(bg_img_path)
    if os.path.exists(overlay_path): os.remove(overlay_path)

    prs.save(output_pptx_path)
    return output_pptx_path
