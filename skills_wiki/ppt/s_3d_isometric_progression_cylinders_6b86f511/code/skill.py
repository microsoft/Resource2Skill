def create_slide(
    output_pptx_path: str,
    title_text: str = "Growth Progression",
    body_text: str = "Detailed description of this milestone.",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 3D Isometric Progression Cylinders visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    # Soft sky blue background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(225, 235, 245)

    # === XML Injection Helper Function ===
    def apply_3d_isometric(shape, depth_pt: int, is_hollow_ring: bool = False):
        """
        Injects OpenXML to apply Isometric Top Up rotation and 3D extrusion (depth).
        """
        spPr = shape.element.spPr
        a_ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

        # Remove existing 3D properties if any to prevent schema conflicts
        for tag in ['a:scene3d', 'a:sp3d']:
            existing = spPr.find(tag, namespaces=a_ns)
            if existing is not None:
                spPr.remove(existing)

        # 1. Scene 3D: Isometric Top Up Camera + Lighting
        scene3d_xml = f"""
        <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:camera prst="isometricTopUp"/>
            <a:lightRig rig="threePt" dir="t"/>
        </a:scene3d>
        """
        scene3d = parse_xml(scene3d_xml)
        spPr.append(scene3d)

        # 2. Shape 3D: Extrusion Depth
        # 1 Point = 12,700 EMUs
        extrusion_h = depth_pt * 12700 if not is_hollow_ring else 0
        
        sp3d_xml = f"""
        <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" 
                extrusionH="{extrusion_h}" 
                prstMaterial="powder">
        </a:sp3d>
        """
        sp3d = parse_xml(sp3d_xml)
        spPr.append(sp3d)

    # === Layer 2 & 3: Visual Effect & Content ===
    
    # Palette for the steps
    step_colors = [
        RGBColor(255, 80, 80),   # Red
        RGBColor(255, 170, 0),   # Orange
        RGBColor(30, 200, 150),  # Teal
        RGBColor(50, 150, 255),  # Blue
        RGBColor(150, 80, 255)   # Purple
    ]

    # Layout starting coordinates
    start_x = Inches(1.5)
    start_y = Inches(5.5)
    
    num_steps = 5

    for i in range(num_steps):
        # Calculate dynamic positions and depth
        depth = 30 + (i * 20)  # Starts at 30pt, increases by 20pt each step
        x_pos = start_x + Inches(i * 2.0)
        y_pos = start_y - Inches(i * 0.8) # Move up and to the right
        
        current_color = step_colors[i]

        # 1. Base Cylinder (Solid White)
        base_size = Inches(1.2)
        base = slide.shapes.add_shape(MSO_SHAPE.OVAL, x_pos, y_pos, base_size, base_size)
        base.fill.solid()
        base.fill.fore_color.rgb = RGBColor(255, 255, 255)
        base.line.fill.background() # Remove outline
        apply_3d_isometric(base, depth_pt=depth, is_hollow_ring=False)

        # 2. Floating Outer Ring
        ring_size = Inches(1.6)
        ring_offset = Inches(0.2) # (1.6 - 1.2) / 2
        ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, x_pos - ring_offset, y_pos - ring_offset, ring_size, ring_size)
        ring.fill.background() # Transparent fill
        ring.line.color.rgb = current_color
        ring.line.width = Pt(2.5)
        apply_3d_isometric(ring, depth_pt=0, is_hollow_ring=True)

        # 3. Flat Icon Plate (Simulating an icon laid flat on top of the cylinder)
        icon_size = Inches(0.4)
        icon_offset = Inches(0.4) # (1.2 - 0.4) / 2
        icon = slide.shapes.add_shape(MSO_SHAPE.OVAL, x_pos + icon_offset, y_pos + icon_offset, icon_size, icon_size)
        icon.fill.solid()
        icon.fill.fore_color.rgb = current_color
        icon.line.fill.background()
        apply_3d_isometric(icon, depth_pt=0, is_hollow_ring=True) # Applies isometric rotation so it sits flat

        # 4. Text Content (placed to the right of the cylinder base)
        # We estimate the bottom of the cylinder by adding depth to the Y position
        text_y_offset = y_pos + Inches(1.0) + Inches(depth / 72.0) 
        
        tx_box = slide.shapes.add_textbox(x_pos - Inches(0.2), text_y_offset, Inches(2.2), Inches(1))
        tf = tx_box.text_frame
        
        # Title
        p_title = tf.paragraphs[0]
        p_title.text = f"STEP 0{i+1}"
        p_title.font.bold = True
        p_title.font.name = "Century Gothic"
        p_title.font.size = Pt(14)
        p_title.font.color.rgb = RGBColor(30, 30, 30)
        
        # Body
        p_body = tf.add_paragraph()
        p_body.text = body_text
        p_body.font.name = "Century Gothic"
        p_body.font.size = Pt(10)
        p_body.font.color.rgb = RGBColor(100, 100, 100)

    # Add Main Slide Title
    main_title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(6), Inches(1))
    tf_main = main_title.text_frame
    p_main = tf_main.paragraphs[0]
    p_main.text = title_text.upper()
    p_main.font.bold = True
    p_main.font.name = "Century Gothic"
    p_main.font.size = Pt(24)
    p_main.font.color.rgb = RGBColor(30, 30, 30)

    prs.save(output_pptx_path)
    return output_pptx_path
