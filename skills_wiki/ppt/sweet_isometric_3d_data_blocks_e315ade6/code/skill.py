def create_slide(
    output_pptx_path: str,
    title_text: str = "3D Information Slide",
    subtitle_text: str = "Title Information Content Overview",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a 'Sweet Isometric 3D' pie chart infographic.

    This function reproduces the effect by creating pie slice shapes and then
    injecting Open XML to apply 3D extrusion and isometric rotation. A custom
    polygon with a gradient fill is used to create the long shadow effect.

    Returns:
        str: The path to the saved .pptx file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.enum.shapes import MSO_SHAPE, MSO_GEOMETRY
    from pptx.dml.color import RGBColor
    from pptx.oxml.ns import qn
    from pptx.oxml import OxmlElement

    # --- Presentation and Slide Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # --- Define Color Palette ---
    colors = {
        "purple": RGBColor(111, 68, 255),
        "orange": RGBColor(253, 117, 53),
        "yellow": RGBColor(255, 193, 7),
        "white": RGBColor(245, 245, 245),
        "text_dark": RGBColor(64, 64, 64),
        "shadow": RGBColor(111, 68, 255)
    }

    # --- Layer 1: Background (White) ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    # --- Layer 2: Custom Long Shadow ---
    shadow_path = [
        ("M", (Inches(5.0), Inches(4.5))),
        ("L", (Inches(8.5), Inches(4.5))),
        ("L", (Inches(9.5), Inches(6.5))),
        ("L", (Inches(6.0), Inches(6.5))),
        ("Z",)
    ]
    shadow_shape = slide.shapes.add_freeform_shape(Emu(0), Emu(0), Emu(0), Emu(0), shadow_path, with_fill=True)
    shadow_shape.line.fill.background()

    # Apply gradient fill to the shadow
    fill = shadow_shape.fill
    fill.gradient()
    fill.gradient_angle = 90
    
    # Gradient stop 1: Semi-transparent shadow color
    stop1 = fill.gradient_stops.add()
    stop1.position = 0.0
    stop1.color.rgb = colors["shadow"]
    stop1.color.alpha = 0.2  # 80% transparent
    
    # Gradient stop 2: Faded shadow color
    stop2 = fill.gradient_stops.add()
    stop2.position = 1.0
    stop2.color.rgb = colors["shadow"]
    stop2.color.alpha = 0.0 # 100% transparent

    # --- Layer 3: 3D Pie Chart ---
    def set_3d_format(shape, extrusion_height_pt=70):
        """Injects lxml to apply 3D effects to a shape."""
        sp = shape.element
        spPr = sp.spPr

        # Scene3D for camera and lighting
        scene3d = OxmlElement('a:scene3d')
        camera = OxmlElement('a:camera')
        camera.set('prst', 'isometricTopUp')
        scene3d.append(camera)
        
        lightRig = OxmlElement('a:lightRig')
        lightRig.set('rig', 'threePt')
        lightRig.set('dir', 't')
        scene3d.append(lightRig)
        
        spPr.append(scene3d)

        # Shape3D for extrusion
        shape3d = OxmlElement('a:sp3d')
        extrusion = OxmlElement('a:extrusion')
        extrusion.set('h', str(int(extrusion_height_pt * 12700))) # Convert points to EMUs
        shape3d.append(extrusion)
        
        spPr.append(shape3d)

    # Pie chart properties
    pie_data = [
        {"angle_start": 0, "angle_end": 90, "color": colors["orange"]},
        {"angle_start": 90, "angle_end": 180, "color": colors["yellow"]},
        {"angle_start": 180, "angle_end": 270, "color": colors["white"]},
        {"angle_start": 270, "angle_end": 360, "color": colors["purple"]},
    ]
    
    center_x, center_y = Inches(6.66), Inches(3.75)
    width, height = Inches(3.5), Inches(3.5)
    
    # Sort to draw the back piece first
    sorted_pie_data = sorted(pie_data, key=lambda x: (x["angle_start"] + x["angle_end"]) / 2, reverse=True)

    for piece in sorted_pie_data:
        # Create a pie slice shape
        shape = slide.shapes.add_shape(
            MSO_SHAPE.PIE, center_x - width / 2, center_y - height / 2, width, height
        )
        
        # Set angles for the pie slice
        shape.adjustments[0] = piece["angle_start"] * -60000
        shape.adjustments[1] = piece["angle_end"] * -60000

        # Apply fill color and remove outline
        shape.fill.solid()
        shape.fill.fore_color.rgb = piece["color"]
        shape.line.fill.background()

        # Apply 3D formatting
        set_3d_format(shape, extrusion_height_pt=60)
    
    # --- Layer 4: Text & Content ---
    # Main Title and Subtitle
    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    title_shape.text_frame.text = title_text
    p = title_shape.text_frame.paragraphs[0]
    p.font.name = 'Arial Black'
    p.font.size = Pt(36)
    p.font.color.rgb = colors["text_dark"]

    subtitle_shape = slide.shapes.add_textbox(Inches(1), Inches(1.2), Inches(11.33), Inches(0.5))
    subtitle_shape.text_frame.text = subtitle_text
    p = subtitle_shape.text_frame.paragraphs[0]
    p.font.name = 'Arial'
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(128, 128, 128)

    # Text Labels for pie chart
    labels_data = [
        {"x": Inches(1.5), "y": Inches(3.0), "text": "Your Text Here", "desc": "This is simply dummy text of\nthe printing", "color": colors["purple"]},
        {"x": Inches(1.5), "y": Inches(4.5), "text": "Your Text Here", "desc": "This is simply dummy text of\nthe printing", "color": colors["orange"]},
        {"x": Inches(9.5), "y": Inches(3.0), "text": "Your Text Here", "desc": "This is simply dummy text of\nthe printing", "color": colors["yellow"]},
        {"x": Inches(9.5), "y": Inches(4.5), "text": "Your Text Here", "desc": "This is simply dummy text of\nthe printing", "color": colors["text_dark"]},
    ]

    for label in labels_data:
        # Add color indicator line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, label["x"], label["y"], Inches(0.3), Inches(0.05))
        line.fill.solid()
        line.fill.fore_color.rgb = label["color"]
        line.line.fill.background()

        # Add label title
        title_box = slide.shapes.add_textbox(label["x"], label["y"] + Inches(0.1), Inches(2.5), Inches(0.4))
        title_box.text_frame.text = label["text"]
        p = title_box.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = colors["text_dark"]

        # Add label description
        desc_box = slide.shapes.add_textbox(label["x"], label["y"] + Inches(0.4), Inches(2.5), Inches(0.6))
        desc_box.text_frame.text = label["desc"]
        p = desc_box.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(128, 128, 128)

    # --- Save Presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path

