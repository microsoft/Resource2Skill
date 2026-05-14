def create_slide(
    output_pptx_path: str,
    target_data: list = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with three 3D isometric targets.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        target_data (list): A list of dictionaries, each containing 'title', 'text', 'color', and 'icon_path'.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import OxmlElement
    from pptx.oxml.ns import qn
    from PIL import Image, ImageDraw, ImageFilter
    import io

    # Default data if none provided
    if target_data is None:
        target_data = [
            {'title': 'TARGET 01', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'color': RGBColor(47, 85, 151)},
            {'title': 'TARGET 02', 'text': 'Maecenas porttitor congue massa. Fusce posuere, magna.', 'color': RGBColor(255, 0, 0)},
            {'title': 'TARGET 03', 'text': 'In sit amet felis malesuada, feugiat purus eget, varius.', 'color': RGBColor(0, 176, 80)}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Helper function to apply 3D effect via lxml ---
    def apply_3d_target_effect(group_shape):
        grpSp = group_shape.element
        grpSpPr = grpSp.grpSpPr

        # 1. 3D Scene (Camera)
        scene3d = OxmlElement('a:scene3d')
        camera = OxmlElement('a:camera')
        camera.set('prst', 'perspRelaxedModerately')
        camera.set('fov', str(int(80 * 60000)))  # Field of View (Perspective)
        scene3d.append(camera)

        lightRig = OxmlElement('a:lightRig')
        lightRig.set('rig', 'threePt')
        lightRig.set('dir', 't')
        scene3d.append(lightRig)
        grpSpPr.append(scene3d)

        # 2. 3D Format (Depth/Extrusion)
        sp3d = OxmlElement('a:sp3d')
        extrusion = OxmlElement('a:extrusion')
        extrusion.set('h', str(Emu(Inches(0.3)))) # Depth of the target
        sp3d.append(extrusion)
        grpSpPr.append(sp3d)
        
        # 3. 3D Rotation (Transform)
        xfrm = grpSpPr.first_child_found_in("a:xfrm")
        if xfrm is None:
            xfrm = OxmlElement('a:xfrm')
            grpSpPr.insert(0, xfrm)
        
        # This rotation flattens the perspective view
        rot = OxmlElement('a:rot')
        rot.set('lat', str(int(320 * 60000))) # Tilts the object
        rot.set('lon', '0')
        rot.set('rev', '0')
        xfrm.append(rot)

    # --- Helper function to create a soft shadow ---
    def create_shadow_image(width, height):
        shadow_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(shadow_img)
        
        # Draw a semi-transparent black ellipse
        draw.ellipse([(0, 0), (width, height)], fill=(0, 0, 0, 100))
        
        # Apply a Gaussian blur
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=15))
        
        img_byte_arr = io.BytesIO()
        shadow_img.save(img_byte_arr, format='PNG')
        return img_byte_arr

    # --- Create the three targets ---
    num_targets = len(target_data)
    total_width = prs.slide_width
    target_diameter = Inches(2.5)
    
    # Calculate spacing
    spacing = (total_width - (num_targets * target_diameter)) / (num_targets + 1)

    for i, data in enumerate(target_data):
        left_pos = spacing + i * (target_diameter + spacing)
        top_pos = Inches(4.5)

        # Create soft shadow first and place it
        shadow_width = int(target_diameter * 1.1)
        shadow_height = int(Inches(0.5))
        shadow_io = create_shadow_image(shadow_width, shadow_height)
        slide.shapes.add_picture(shadow_io, left_pos - Emu(Inches(0.1)), top_pos + Emu(Inches(1.0)), width=shadow_width, height=shadow_height)

        # Create concentric circles for the target
        shapes_to_group = []
        num_rings = 5
        for j in range(num_rings):
            dia = target_diameter - (j * target_diameter / num_rings)
            offset = (target_diameter - dia) / 2
            shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left_pos + offset, top_pos + offset, dia, dia)
            shape.line.fill.background()
            
            fill = shape.fill
            if j % 2 == 0:
                fill.solid()
                fill.fore_color.rgb = data['color']
            else:
                fill.solid()
                fill.fore_color.rgb = RGBColor(255, 255, 255)
            shapes_to_group.append(shape)
        
        # Group the circles and apply 3D effect
        group_shape = slide.shapes.group_shapes(shapes_to_group)
        apply_3d_target_effect(group_shape)
        
        # --- Create Arrow ---
        arrow_shaft = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos + target_diameter/2 - Inches(0.03), top_pos - Inches(1.5), Inches(0.06), Inches(2.6))
        arrow_shaft.line.fill.background()
        fill = arrow_shaft.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = RGBColor(217, 217, 217)
        fill.gradient_stops[1].color.rgb = RGBColor(166, 166, 166)
        
        fletching1 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, left_pos + target_diameter/2 - Inches(0.2), top_pos - Inches(1.8), Inches(0.2), Inches(0.4))
        fletching1.line.fill.background()
        fletching1.fill.solid()
        fletching1.fill.fore_color.rgb = data['color']
        
        fletching2 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, left_pos + target_diameter/2, top_pos - Inches(1.8), Inches(0.2), Inches(0.4))
        fletching2.line.fill.background()
        fletching2.rotation = 180.0
        fletching2.fill.solid()
        fletching2.fill.fore_color.rgb = data['color']
        
        arrow_group = slide.shapes.group_shapes([arrow_shaft, fletching1, fletching2])
        arrow_group.top = top_pos - Inches(2.2) # Adjust final position

        # --- Add Text ---
        title_box = slide.shapes.add_textbox(left_pos, Inches(2.5), target_diameter, Inches(0.5))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = data['title']
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = data['color']
        tf.word_wrap = False

        text_box = slide.shapes.add_textbox(left_pos, Inches(2.9), target_diameter, Inches(1.0))
        tf = text_box.text_frame
        p = tf.paragraphs[0]
        p.text = data['text']
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(128, 128, 128)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("3d_targets.pptx")
