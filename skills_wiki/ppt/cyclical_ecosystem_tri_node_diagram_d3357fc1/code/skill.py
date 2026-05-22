def create_slide(
    output_pptx_path: str,
    title_text: str = "智慧手機生態圈\nSmart Phone APP",
    bg_color_start: tuple = (235, 60, 50),   # Vibrant red
    bg_color_end: tuple = (180, 20, 20),     # Dark red
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Cyclical Ecosystem Tri-Node Diagram" visual effect.
    """
    import os
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml.ns import qn
    from pptx.oxml import OxmlElement
    from PIL import Image, ImageDraw

    # === Helper Functions for XML Injection ===
    
    def set_shape_transparency(shape, alpha_percent: int):
        """Injects alpha transparency into a shape's solid fill."""
        fill = shape.fill
        fill.solid()
        # Navigate to the <a:solidFill> tag and modify the color alpha
        solidFill = shape.element.spPr.find(qn('a:solidFill'))
        if solidFill is not None:
            srgbClr = solidFill.find(qn('a:srgbClr'))
            if srgbClr is not None:
                alpha = OxmlElement('a:alpha')
                # 100% opacity = 100000, 0% opacity = 0
                alpha.set('val', str(int((100 - alpha_percent) * 1000)))
                srgbClr.append(alpha)

    def format_arc_with_arrows(shape, start_deg, end_deg):
        """Sets precise start/end angles for an arc and adds an end arrow."""
        # 1. Set angles
        adjLst = shape.element.spPr.find(qn('a:prstGeom')).find(qn('a:adjLst'))
        if adjLst is not None:
            for child in list(adjLst):
                adjLst.remove(child)
        else:
            adjLst = OxmlElement('a:adjLst')
            shape.element.spPr.find(qn('a:prstGeom')).insert(0, adjLst)

        # PowerPoint angles are in 60,000ths of a degree. 0 is Right/East.
        adj1 = OxmlElement('a:adj')
        adj1.set('name', 'adj1')
        adj1.set('val', str(int(start_deg * 60000)))
        adjLst.append(adj1)

        adj2 = OxmlElement('a:adj')
        adj2.set('name', 'adj2')
        adj2.set('val', str(int(end_deg * 60000)))
        adjLst.append(adj2)

        # 2. Add End Arrow
        ln = shape.element.spPr.find(qn('a:ln'))
        if ln is None:
            ln = OxmlElement('a:ln')
            shape.element.spPr.append(ln)
        
        tailEnd = OxmlElement('a:tailEnd')
        tailEnd.set('type', 'triangle')
        tailEnd.set('w', 'med')
        tailEnd.set('len', 'lrg')
        ln.append(tailEnd)

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background Generation (PIL Gradient) ===
    bg_img_path = "temp_ecosystem_bg.png"
    width_px, height_px = int(13.333 * 100), int(7.5 * 100)
    img = Image.new('RGB', (width_px, height_px))
    draw = ImageDraw.Draw(img)
    
    # Linear gradient mimicking a soft light source from top left
    for y in range(height_px):
        ratio = y / height_px
        r = int(bg_color_start[0] * (1 - ratio) + bg_color_end[0] * ratio)
        g = int(bg_color_start[1] * (1 - ratio) + bg_color_end[1] * ratio)
        b = int(bg_color_start[2] * (1 - ratio) + bg_color_end[2] * ratio)
        draw.line([(0, y), (width_px, y)], fill=(r, g, b))
    
    img.save(bg_img_path)
    slide.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Left Content Area ===
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(5), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text.split('\n')[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = tf.add_paragraph()
    p2.text = title_text.split('\n')[1] if '\n' in title_text else ""
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(255, 200, 200)

    # Metric text
    metric_box = slide.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(5), Inches(1))
    mtf = metric_box.text_frame
    mp1 = mtf.paragraphs[0]
    mp1.text = "2020    2400 億美元"
    mp1.font.size = Pt(28)
    mp1.font.bold = True
    mp1.font.color.rgb = RGBColor(255, 255, 255)
    
    mp2 = mtf.add_paragraph()
    mp2.text = "全球行動廣告支出額"
    mp2.font.size = Pt(14)
    mp2.font.color.rgb = RGBColor(255, 200, 200)

    # === Layer 3: Diagram Geometry Setup ===
    center_x = 9.0  # Inches
    center_y = 3.8  # Inches
    orbit_radius = 2.4 # Inches
    node_radius = 0.9 # Inches

    # Angles for the 3 nodes (Top, Bottom Right, Bottom Left)
    node_angles_deg = [270, 30, 150]
    node_labels = ["APP業者", "手機品牌商", "用戶"]

    # Calculate gap to leave between arc ends and nodes
    # Arc length = r * theta. Let's leave approx 35 degrees gap around nodes.
    gap_deg = 35 

    # === Layer 4: Draw Connecting Arcs ===
    # Arcs connect Node 1->2, Node 2->3, Node 3->1
    arc_spans = [
        (270 + gap_deg, 360 + 30 - gap_deg), # Top to BR
        (30 + gap_deg, 150 - gap_deg),       # BR to BL
        (150 + gap_deg, 270 - gap_deg)       # BL to Top
    ]

    for start_angle, end_angle in arc_spans:
        # Bounding box for arcs must match the whole orbit circle
        arc = slide.shapes.add_shape(
            MSO_SHAPE.ARC, 
            Inches(center_x - orbit_radius), 
            Inches(center_y - orbit_radius), 
            Inches(orbit_radius * 2), 
            Inches(orbit_radius * 2)
        )
        arc.line.color.rgb = RGBColor(255, 255, 255)
        arc.line.width = Pt(1.5)
        
        # Apply XML for specific angles and arrows
        format_arc_with_arrows(arc, start_angle, end_angle)

    # === Layer 5: Draw Nodes ===
    for i, angle in enumerate(node_angles_deg):
        # Calculate node center
        rad = math.radians(angle)
        nx = center_x + (orbit_radius * math.cos(rad))
        ny = center_y + (orbit_radius * math.sin(rad))
        
        # Draw transparent circle
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(nx - node_radius), 
            Inches(ny - node_radius), 
            Inches(node_radius * 2), 
            Inches(node_radius * 2)
        )
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor(*bg_color_end) # Darker red base
        node.line.color.rgb = RGBColor(255, 255, 255)
        node.line.width = Pt(1)
        
        # Inject 62% transparency
        set_shape_transparency(node, 62)

        # Draw Node Label (placed strategically near the node)
        label_offset_x = 0
        label_offset_y = 0
        align = PP_ALIGN.CENTER
        
        if angle == 270: # Top
            label_offset_y = -1.2
        elif angle == 30: # Bottom Right
            label_offset_x = 1.0
            align = PP_ALIGN.LEFT
        elif angle == 150: # Bottom Left
            label_offset_x = -1.2
            align = PP_ALIGN.RIGHT

        label = slide.shapes.add_textbox(
            Inches(nx - 1 + label_offset_x), 
            Inches(ny - 0.2 + label_offset_y), 
            Inches(2), Inches(0.5)
        )
        p = label.text_frame.paragraphs[0]
        p.text = node_labels[i]
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = align

    # Clean up temp files
    try:
        os.remove(bg_img_path)
    except OSError:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path
