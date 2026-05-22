import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def apply_3d_effect(shape, depth_pt=0, z_pt=0, camera_prst="isometricTopUp", material="matPlastic"):
    """
    Injects DrawingML XML into a shape to transform it into a 3D isometric object.
    :param depth_pt: The extrusion depth (thickness) in points.
    :param z_pt: Distance from the ground (Z-axis offset) in points.
    """
    spPr = shape.element.spPr
    
    # Remove existing 3D tags if present to prevent schema errors
    for tag in ['{http://schemas.openxmlformats.org/drawingml/2006/main}scene3d',
                '{http://schemas.openxmlformats.org/drawingml/2006/main}sp3d']:
        el = spPr.find(tag)
        if el is not None:
            spPr.remove(el)

    # 1. Add Camera and Lighting Scene
    scene3d_xml = f"""
    <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:camera prst="{camera_prst}"/>
        <a:lightRig rig="threePt" dir="t"/>
    </a:scene3d>
    """
    spPr.append(parse_xml(scene3d_xml))

    # 2. Add 3D Extrusion and Z-Elevation
    # 1 point = 12,700 EMUs
    extrusion_emu = int(depth_pt * 12700)
    z_emu = int(z_pt * 12700)
    sp3d_xml = f"""
    <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            extrusionH="{extrusion_emu}"
            z="{z_emu}"
            prstMaterial="{material}">
    </a:sp3d>
    """
    spPr.append(parse_xml(sp3d_xml))

def create_slide(
    output_pptx_path: str,
    title_text: str = "Ranking SLIDES",
    body_text: str = "",
    bg_palette: str = "dark",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the '3D Isometric Morphing Bar Charts' visual effect.
    Generates two slides to demonstrate the Morph transition rising effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Data configuration
    bg_color = RGBColor(30, 20, 60)
    
    colors = [
        RGBColor(0, 191, 255),    # Cyan
        RGBColor(58, 117, 255),   # Blue
        RGBColor(255, 0, 150),    # Magenta
        RGBColor(153, 50, 204)    # Purple
    ]
    
    # Target heights for the bars
    target_depths = [80, 140, 200, 100]
    
    # Icons to place on top of the bars
    icons = [
        MSO_SHAPE.STAR_5_POINT,
        MSO_SHAPE.HEART,
        MSO_SHAPE.LIGHTNING_BOLT,
        MSO_SHAPE.SUN
    ]

    # Generate Slide 1 (Flat State) and Slide 2 (Elevated State)
    for slide_idx in range(2):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Slide Background
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = bg_color

        # Add 2D Screen-space Titles
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(5), Inches(1))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "Ranking"
        p.font.size = Pt(44)
        p.font.color.rgb = RGBColor(255, 215, 0)
        p.font.italic = True
        
        subtitle_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(5), Inches(1))
        tf2 = subtitle_box.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = "SLIDES"
        p2.font.size = Pt(64)
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.font.bold = True

        # Render 3D Isometric Chart Elements
        start_x = Inches(3.0)
        start_y = Inches(1.5)
        w_cube = Inches(1.3)
        h_cube = Inches(1.3)
        w_tail = Inches(7.0)

        for i in range(4):
            # Layout cascades downwards in 2D (which projects to down-left in 3D)
            y = start_y + (i * h_cube)

            # Determine depth based on which slide we are generating (animation state)
            current_depth = target_depths[i] if slide_idx == 1 else 1

            # 1. Floor Tail (The long strip)
            tail = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, y, w_tail, h_cube)
            tail.fill.solid()
            tail.fill.fore_color.rgb = colors[i]
            tail.line.color.rgb = colors[i]
            # Sits flat on the floor (Z=0, Depth=1)
            apply_3d_effect(tail, depth_pt=1, z_pt=0)

            # 2. Rising Data Cube
            cube = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, y, w_cube, h_cube)
            cube.fill.solid()
            cube.fill.fore_color.rgb = colors[i]
            cube.line.color.rgb = colors[i]
            # Cube extends upwards. Setting Z=depth pushes the front face towards camera, leaving back face on floor.
            apply_3d_effect(cube, depth_pt=current_depth, z_pt=current_depth)

            # 3. Floor Text (Painted on the strip)
            text_box = slide.shapes.add_textbox(start_x + w_cube + Inches(0.5), y + Inches(0.25), Inches(3), Inches(0.8))
            text_box.margin_left = text_box.margin_top = text_box.margin_right = text_box.margin_bottom = 0
            tf3 = text_box.text_frame
            tf3.word_wrap = False
            p3 = tf3.paragraphs[0]
            p3.text = f"Topic 0{i+1}"
            p3.font.size = Pt(36)
            p3.font.bold = True
            p3.font.color.rgb = RGBColor(255, 255, 255)
            # Text hovers 1 point above the floor to avoid z-fighting with the tail
            apply_3d_effect(text_box, depth_pt=0, z_pt=2)

            # 4. Floating Icon (Rests on top of the data cube)
            icon = slide.shapes.add_shape(icons[i], start_x + Inches(0.3), y + Inches(0.3), Inches(0.7), Inches(0.7))
            icon.fill.solid()
            icon.fill.fore_color.rgb = RGBColor(255, 255, 255)
            icon.line.color.rgb = colors[i]
            # Icon hovers exactly at the front face of the cube (Z = current_depth + 1pt buffer)
            apply_3d_effect(icon, depth_pt=0, z_pt=current_depth + 1)

    prs.save(output_pptx_path)
    return output_pptx_path
