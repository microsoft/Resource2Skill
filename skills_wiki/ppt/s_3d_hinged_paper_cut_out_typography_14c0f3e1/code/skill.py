def create_slide(
    output_pptx_path: str,
    title_text: str = "EFFECT",
    bg_color: tuple = (240, 240, 240),
    void_color: tuple = (75, 0, 130), # Deep purple
    flap_color: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the '3D Hinged Paper Cut-out Typography' effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    import math

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Set Background Color
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # ---------------------------------------------------------
    # Helper: Inject 3D Rotation and Drop Shadow via XML (lxml)
    # ---------------------------------------------------------
    def apply_3d_hinge_effect(shape, rot_y_deg=40):
        # 1. Apply 3D Rotation to Text Body (Perspective Left)
        bodyPr = shape.element.xpath('.//a:bodyPr')[0]
        # PPT uses 60000 units per degree. Left swing means positive Y rotation.
        rot_units = int(rot_y_deg * 60000) 
        sp3d_xml = f"""
        <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:camera prst="perspL" fov="600000"/>
            <a:rot x="0" y="{rot_units}" z="0"/>
        </a:sp3d>
        """
        sp3d = parse_xml(sp3d_xml)
        bodyPr.append(sp3d)

        # 2. Apply Soft Drop Shadow to Shape (Acts as the inner 3D depth)
        spPr = shape.element.xpath('.//a:spPr')[0]
        # blurRad and dist are in EMUs. 150000 = ~12pt. Alpha 40000 = 40% opacity.
        effectLst_xml = f"""
        <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:outerShdw blurRad="150000" dist="200000" dir="0" rotWithShape="0">
                <a:srgbClr val="000000">
                    <a:alpha val="40000"/>
                </a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        effectLst = parse_xml(effectLst_xml)
        spPr.append(effectLst)

    # ---------------------------------------------------------
    # Layout Calculations
    # ---------------------------------------------------------
    title_text = title_text.upper()
    num_chars = len(title_text)
    
    # Box dimensions per letter
    box_w = Inches(1.8)
    box_h = Inches(3.0)
    spacing = Inches(1.6) # Slightly less than width to keep them close
    
    total_width = num_chars * spacing
    start_x = (prs.slide_width - total_width) / 2 + Inches(0.2)
    center_y = (prs.slide_height - box_h) / 2

    # When a shape is rotated in 3D by angle theta, its projected width shrinks.
    # To keep the LEFT edge pinned (acting like a hinge), we must shift the center X to the left.
    theta_deg = 45
    theta_rad = math.radians(theta_deg)
    # The shift needed = (Original Half Width) - (Projected Half Width)
    hinge_shift = (box_w / 2) - ((box_w / 2) * math.cos(theta_rad))

    # ---------------------------------------------------------
    # Generate the Typography
    # ---------------------------------------------------------
    for i, char in enumerate(title_text):
        base_x = start_x + (i * spacing)
        
        # --- Layer 1: The "Void" (Flat Colored Letter) ---
        void_shape = slide.shapes.add_textbox(base_x, center_y, box_w, box_h)
        tf_void = void_shape.text_frame
        tf_void.text = char
        tf_void.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        run_void = tf_void.paragraphs[0].runs[0]
        run_void.font.name = "Arial Black" # Use standard heavy font
        run_void.font.size = Pt(180)
        run_void.font.color.rgb = RGBColor(*void_color)

        # --- Layer 2: The "Flap" (White Rotated Letter with Shadow) ---
        # Shift X to the left to pin the left hinge 
        flap_x = base_x - hinge_shift
        
        flap_shape = slide.shapes.add_textbox(flap_x, center_y, box_w, box_h)
        tf_flap = flap_shape.text_frame
        tf_flap.text = char
        tf_flap.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        run_flap = tf_flap.paragraphs[0].runs[0]
        run_flap.font.name = "Arial Black"
        run_flap.font.size = Pt(180)
        run_flap.font.color.rgb = RGBColor(*flap_color)

        # Inject the magic 3D and shadow XML
        apply_3d_hinge_effect(flap_shape, rot_y_deg=theta_deg)

    prs.save(output_pptx_path)
    return output_pptx_path
