def create_slide(
    output_pptx_path: str,
    title_text: str = "翻轉吧! 立方字",
    bg_color: tuple = (253, 208, 23),      # Vibrant Yellow
    cube_face_color: tuple = (255, 225, 53), # Lighter Yellow
    cube_depth_color: tuple = (218, 165, 32), # Gold/Dark Yellow
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "3D Isometric Typography Cubes" visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import qn
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # --- Set Slide Background ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # --- Helper Function for 3D XML Injection ---
    def apply_3d_effect(shape, depth_pt=80, depth_color_hex="DAA520", camera_prst="isometricRightUp"):
        """Injects DrawingML XML to apply 3D Extrusion and Camera Rotation to a shape."""
        spPr = shape._element.spPr
        depth_emu = int(depth_pt * 12700) # Convert points to EMUs
        
        # 1. Construct Scene 3D (Camera Rotation and Lighting)
        # rig="threePt" provides nice highlights and shadows
        scene3d_xml = f'''
        <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:camera prst="{camera_prst}"/>
            <a:lightRig rig="threePt" dir="t"/>
        </a:scene3d>
        '''
        scene3d = parse_xml(scene3d_xml)
        
        # 2. Construct Shape 3D properties (Extrusion Depth and Color)
        sp3d_xml = f'''
        <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" extrusionH="{depth_emu}">
            <a:extrusionClr>
                <a:srgbClr val="{depth_color_hex}"/>
            </a:extrusionClr>
        </a:sp3d>
        '''
        sp3d = parse_xml(sp3d_xml)
        
        # 3. Safely inject into spPr (remove existing tags if present to avoid corruption)
        for tag_name in ['a:scene3d', 'a:sp3d']:
            existing = spPr.find(qn(tag_name))
            if existing is not None:
                spPr.remove(existing)
                
        spPr.append(scene3d)
        spPr.append(sp3d)

    # --- Helper Function to Create a Cube Word ---
    def create_cube_word(text, left, top, size=Inches(1.5), camera_prst="isometricRightUp"):
        # Insert base rounded rectangle
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, size, size
        )
        
        # Format base shape (Face)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*cube_face_color)
        shape.line.fill.background() # No outline
        
        # Adjust corner roundness (make it slightly less rounded)
        # For rounded rectangles, adj1 is the corner radius
        if len(shape.adjustments) > 0:
            shape.adjustments[0] = 0.15 
        
        # Add and format text
        text_frame = shape.text_frame
        text_frame.text = text
        text_frame.word_wrap = False
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        # Align text vertically
        text_frame.vertical_anchor = MSO_SHAPE.ROUNDED_RECTANGLE
        
        font = text_frame.paragraphs[0].runs[0].font
        font.name = "Arial Black" # Bold font works best
        font.size = Pt(48)
        font.color.rgb = RGBColor(0, 0, 0)
        font.bold = True
        
        # Convert depth color RGB tuple to hex string for XML
        depth_hex = f"{cube_depth_color[0]:02X}{cube_depth_color[1]:02X}{cube_depth_color[2]:02X}"
        
        # Apply 3D Effect (80pt depth as per tutorial)
        apply_3d_effect(shape, depth_pt=80, depth_color_hex=depth_hex, camera_prst=camera_prst)

    # --- Layout the Composition ---
    
    # Title Label Text
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(10), Inches(1))
    tf = title_box.text_frame
    tf.text = title_text
    font = tf.paragraphs[0].runs[0].font
    font.size = Pt(44)
    font.bold = True
    font.name = "Arial Black"
    font.color.rgb = RGBColor(0, 0, 0)

    # Row 1: Isometric / Parallel rotation (Clean, uniform look)
    words_isometric = ["翻", "轉", "吧", "!"]
    start_x = 1.5
    start_y = 2.5
    spacing = 2.2
    
    for i, char in enumerate(words_isometric):
        create_cube_word(
            text=char, 
            left=Inches(start_x + (i * spacing)), 
            top=Inches(start_y), 
            camera_prst="isometricRightUp" # Standard parallel isometric
        )

    # Row 2: Perspective / Oblique (Playful, scattered look)
    words_perspective = ["立", "方", "字", "體"]
    start_x = 2.5
    start_y = 4.8
    spacing = 2.2
    
    camera_presets = [
        "perspectiveLeft",      # Tilted left
        "perspectiveRight",     # Tilted right
        "legacyObliqueTopLeft", # Pushed back top-left
        "legacyObliqueFront"    # Straight ahead but deep
    ]
    
    for i, char in enumerate(words_perspective):
        create_cube_word(
            text=char, 
            left=Inches(start_x + (i * spacing)), 
            top=Inches(start_y), 
            camera_prst=camera_presets[i]
        )

    prs.save(output_pptx_path)
    return output_pptx_path
