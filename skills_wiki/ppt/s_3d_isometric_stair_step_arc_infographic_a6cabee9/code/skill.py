import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

def create_slide(
    output_pptx_path: str,
    title_text: str = "6 Step 3D Pie Chart Infographic",
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the 3D Isometric Stair-Step Arc Infographic.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(60, 60, 60)

    # --- Core Parameters ---
    # Gradient color palette from teal to navy
    colors = [
        (29, 179, 166),   # 1: Light Teal
        (24, 150, 140),   # 2: Teal
        (26, 126, 146),   # 3: Medium Blue
        (22, 95, 125),    # 4: Blue
        (33, 67, 101),    # 5: Dark Blue
        (28, 48, 74)      # 6: Navy
    ]

    # Increasing 3D depths for the stair-step effect
    depths_pt = [30, 50, 70, 90, 110, 130]

    # Slice angles: 6 slices of 45 degrees, starting at 90 (Bottom), going clockwise.
    # Gap is 0 to 90 degrees (Right to Bottom).
    angles = [(90 + i * 45, 90 + (i + 1) * 45) for i in range(6)]

    # Chart 2D bounding box (centered)
    cx_inch, cy_inch = 6.66, 3.8
    radius = 2.4
    left = Inches(cx_inch - radius)
    top = Inches(cy_inch - radius)
    width = height = Inches(radius * 2)

    # Peripheral label fixed coordinates to avoid 3D math projection collisions
    label_coords = [
        (Inches(1.5), Inches(5.5)),  # 1: Bottom Left
        (Inches(1.0), Inches(3.5)),  # 2: Mid Left
        (Inches(2.0), Inches(1.5)),  # 3: Top Left
        (Inches(8.5), Inches(1.0)),  # 4: Top Right
        (Inches(10.0), Inches(3.0)), # 5: Mid Right
        (Inches(9.0), Inches(5.0)),  # 6: Bottom Right
    ]

    # --- XML Injection Helper ---
    def apply_native_3d(shape, depth_pt: int, z_pt: int = 0):
        """Injects Office Open XML to apply Isometric 3D Rotation and Extrusion"""
        spPr = shape.element.spPr
        
        # 1. 3D Scene (Camera and Lighting)
        scene_xml = f'''
        <a:scene3d {nsdecls("a")}>
            <a:camera prst="isoTopUp"/>
            <a:lightRig rig="threePt" dir="t"/>
        </a:scene3d>
        '''
        
        # 2. 3D Shape Properties (Extrusion depth and Z-axis levitation)
        depth_emu = int(depth_pt * 12700)
        z_emu = int(z_pt * 12700)
        sp3d_xml = f'''
        <a:sp3d extrusionH="{depth_emu}" z="{z_emu}" {nsdecls("a")}>
            <a:bevelT w="0" h="0"/>
        </a:sp3d>
        '''
        
        # Append to shape properties
        spPr.append(parse_xml(scene_xml))
        spPr.append(parse_xml(sp3d_xml))

    # --- Build the 3D Chart ---
    for i in range(6):
        start_ang, end_ang = angles[i]
        color = colors[i]
        depth = depths_pt[i]

        # 1. Add Arc Segment
        arc = slide.shapes.add_shape(MSO_SHAPE.BLOCK_ARC, left, top, width, height)
        arc.fill.solid()
        arc.fill.fore_color.rgb = RGBColor(*color)
        arc.line.fill.background() # Hides border

        # Override Geometry Adjustments for precise arcs (Angle = degrees * 60000)
        geom = arc.element.spPr.prstGeom
        avLst = geom.find('.//a:avLst', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
        if avLst is not None:
            geom.remove(avLst)
            
        avLst_xml = f'''
        <a:avLst {nsdecls("a")}>
            <a:gd name="adj1" fmla="val {start_ang * 60000}"/>
            <a:gd name="adj2" fmla="val {end_ang * 60000}"/>
            <a:gd name="adj3" fmla="val 50000"/> <!-- 50% Inner Radius -->
        </a:avLst>
        '''
        geom.append(parse_xml(avLst_xml))

        # Apply 3D Extrusion to the Arc
        apply_native_3d(arc, depth_pt=depth)

        # Apply Drop Shadow natively
        arc.shadow.inherit = False
        arc.shadow.distance = Pt(12)
        arc.shadow.blur_radius = Pt(15)
        arc.shadow.angle = 90
        arc.shadow.alpha = 0.3

        # 2. Add Floating Number Label
        # Calculate 2D position at the radial center of the arc segment
        mid_ang_rad = math.radians((start_ang + end_ang) / 2)
        r_mid = radius * 0.75  # exactly halfway between outer (1.0) and inner (0.5)
        txt_x = cx_inch + r_mid * math.cos(mid_ang_rad)
        txt_y = cy_inch + r_mid * math.sin(mid_ang_rad)

        txt_size = 0.5
        txBox = slide.shapes.add_textbox(
            Inches(txt_x - txt_size/2), 
            Inches(txt_y - txt_size/2), 
            Inches(txt_size), 
            Inches(txt_size)
        )
        tf_num = txBox.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = str(i + 1)
        p_num.font.size = Pt(24)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(255, 255, 255)
        p_num.alignment = PP_ALIGN.CENTER

        # Apply 3D Rotation to the text box, and float it using Z-translation
        # z_pt = depth + 5 floats it exactly 5 points above the top surface of the arc!
        apply_native_3d(txBox, depth_pt=0, z_pt=depth + 5)

        # 3. Add Peripheral Flat Text Label
        lx, ly = label_coords[i]
        label_box = slide.shapes.add_textbox(lx, ly, Inches(2.2), Inches(1))
        tf_lbl = label_box.text_frame
        
        # Step Title
        p_title = tf_lbl.paragraphs[0]
        p_title.text = f"TITLE HERE {i+1}"
        p_title.font.bold = True
        p_title.font.size = Pt(14)
        p_title.font.color.rgb = RGBColor(*color)
        
        # Body
        p_body = tf_lbl.add_paragraph()
        p_body.text = "Some text goes here. Some text goes here. Some text goes here."
        p_body.font.size = Pt(10)
        p_body.font.color.rgb = RGBColor(120, 120, 120)

        # Right-align labels on the left side, Left-align on the right side
        if i < 3:
            p_title.alignment = PP_ALIGN.RIGHT
            p_body.alignment = PP_ALIGN.RIGHT
        else:
            p_title.alignment = PP_ALIGN.LEFT
            p_body.alignment = PP_ALIGN.LEFT

    prs.save(output_pptx_path)
    return output_pptx_path
