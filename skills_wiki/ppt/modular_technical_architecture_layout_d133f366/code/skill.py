def create_slide(
    output_pptx_path: str,
    title_text: str = "ENTERPRISE SYSTEM ARCHITECTURE",
    body_text: str = "High-level logical topology and component interaction flow",
    accent_color: tuple = (52, 152, 219),  # Blue for UI layer
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing a highly structured Modular Architecture Diagram.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import OxmlElement
    from pptx.oxml.ns import qn

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Colors ---
    color_pres = RGBColor(*accent_color)
    color_app = RGBColor(46, 204, 113)  # Emerald Green
    color_data = RGBColor(155, 89, 182) # Amethyst Purple
    bg_layer = RGBColor(245, 246, 250)

    # --- Title & Subtitle ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p1 = tf.paragraphs[0]
    p1.text = title_text.upper()
    p1.font.bold = True
    p1.font.size = Pt(24)
    p1.font.color.rgb = RGBColor(40, 50, 60)
    
    p2 = tf.add_paragraph()
    p2.text = body_text
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(120, 130, 140)

    # --- Data Structure for Architecture ---
    layers = [
        {"name": "Presentation Layer", "y": 1.4, "h": 1.6},
        {"name": "Application Layer",  "y": 3.4, "h": 1.6},
        {"name": "Data Access Layer",  "y": 5.4, "h": 1.6}
    ]

    nodes = {
        # Presentation
        "web": {"label": "Web Client\n(React)", "x": 2.5, "y": 1.65, "w": 2.2, "h": 1.0, "type": MSO_SHAPE.ROUNDED_RECTANGLE, "color": color_pres},
        "mob": {"label": "Mobile App\n(Flutter)", "x": 8.6, "y": 1.65, "w": 2.2, "h": 1.0, "type": MSO_SHAPE.ROUNDED_RECTANGLE, "color": color_pres},
        # App
        "api": {"label": "API Gateway\n(REST)", "x": 5.5, "y": 3.65, "w": 2.2, "h": 1.0, "type": MSO_SHAPE.RECTANGLE, "color": color_app},
        # Data
        "db1": {"label": "User Profiles\n(PostgreSQL)", "x": 2.5, "y": 5.65, "w": 2.2, "h": 1.1, "type": MSO_SHAPE.CAN, "color": color_data},
        "db2": {"label": "Txn Ledger\n(MongoDB)", "x": 8.6, "y": 5.65, "w": 2.2, "h": 1.1, "type": MSO_SHAPE.CAN, "color": color_data}
    }

    edges = [
        ("web", "api"),
        ("mob", "api"),
        ("api", "db1"),
        ("api", "db2")
    ]

    # --- 1. Draw Layers (Backgrounds) ---
    for layer in layers:
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(layer["y"]), Inches(12.33), Inches(layer["h"]))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_layer
        shape.line.color.rgb = RGBColor(220, 225, 230)
        shape.line.width = Pt(1)
        
        # Layer Label
        txBox = slide.shapes.add_textbox(Inches(0.6), Inches(layer["y"] + 0.1), Inches(2.5), Inches(0.5))
        tf = txBox.text_frame
        tf.text = layer["name"].upper()
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.size = Pt(10)
        tf.paragraphs[0].font.color.rgb = RGBColor(140, 150, 160)

    # --- 2. Draw Edges (Connectors underneath nodes) ---
    for start_id, end_id in edges:
        n1 = nodes[start_id]
        n2 = nodes[end_id]
        
        # Calculate centers
        c1_x, c1_y = n1['x'] + n1['w'] / 2, n1['y'] + n1['h'] / 2
        c2_x, c2_y = n2['x'] + n2['w'] / 2, n2['y'] + n2['h'] / 2
        
        # Auto-routing based on relative position
        if abs(c2_x - c1_x) > abs(c2_y - c1_y):  # Horizontal bias
            x1 = n1['x'] + n1['w'] if c2_x > c1_x else n1['x']
            y1 = c1_y
            x2 = n2['x'] if c2_x > c1_x else n2['x'] + n2['w']
            y2 = c2_y
        else:  # Vertical bias
            x1 = c1_x
            y1 = n1['y'] + n1['h'] if c2_y > c1_y else n1['y']
            x2 = c2_x
            y2 = n2['y'] if c2_y > c1_y else n2['y'] + n2['h']

        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        conn.line.width = Pt(2)
        conn.line.color.rgb = RGBColor(160, 170, 180)
        
        # Add arrowhead via lxml
        line_props = conn.line._lineProperties
        tailEnd = OxmlElement('a:tailEnd')
        tailEnd.set('type', 'triangle')
        tailEnd.set('w', 'med')
        tailEnd.set('len', 'med')
        line_props.append(tailEnd)

    # --- 3. Draw Nodes (On top of edges) ---
    for node_id, data in nodes.items():
        shape = slide.shapes.add_shape(data["type"], Inches(data["x"]), Inches(data["y"]), Inches(data["w"]), Inches(data["h"]))
        shape.fill.solid()
        shape.fill.fore_color.rgb = data["color"]
        shape.line.color.rgb = RGBColor(255, 255, 255)
        shape.line.width = Pt(1.5)
        
        # Add subtle outer shadow for 3D layered effect via lxml
        spPr = shape._element.spPr
        effectLst = OxmlElement('a:effectLst')
        outerShdw = OxmlElement('a:outerShdw')
        outerShdw.set('blurRad', '50000')  # ~5pt blur
        outerShdw.set('dist', '30000')     # ~3pt distance
        outerShdw.set('dir', '2700000')    # Downwards (45 deg)
        outerShdw.set('algn', 'tl')
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')       # Black shadow
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '15000')          # 15% opacity
        srgbClr.append(alpha)
        outerShdw.append(srgbClr)
        effectLst.append(outerShdw)
        spPr.append(effectLst)

        # Apply Text
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = data["label"]
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.name = "Arial"
        p.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
