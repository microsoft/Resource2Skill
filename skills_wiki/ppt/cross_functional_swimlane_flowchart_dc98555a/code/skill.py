def create_slide(
    output_pptx_path: str,
    title_text: str = "Process Name: Cross-Functional Swimlane",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Cross-Functional Swimlane Flowchart effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.dml.color import RGBColor
    from pptx.oxml.ns import qn
    from pptx.oxml import OxmlElement

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide

    # Palette
    COLOR_LANE_LINE = RGBColor(180, 200, 220)
    COLOR_TEXT_MAIN = RGBColor(80, 80, 80)
    COLOR_NODE_PROCESS = RGBColor(255, 180, 0)
    COLOR_NODE_DECISION = RGBColor(255, 255, 255)
    COLOR_DECISION_OUTLINE = RGBColor(120, 120, 120)
    COLOR_CONNECTOR = RGBColor(120, 120, 120)

    # --- Add Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.font.bold = True

    # --- Define Grid Dimensions ---
    header_width = Inches(2.0)
    start_y = Inches(1.2)
    lane_height = Inches(1.4)
    canvas_width = prs.slide_width
    
    lanes = ["Customer", "Area 1", "Area 2", "Area 3"]
    
    # --- Draw Grid & Lanes ---
    # Vertical divider
    v_line = slide.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, header_width, start_y, header_width, start_y + (len(lanes)*lane_height))
    v_line.line.color.rgb = COLOR_LANE_LINE
    v_line.line.width = Pt(1.5)

    # Draw Lanes
    for i, lane_name in enumerate(lanes):
        y_pos = start_y + (i * lane_height)
        
        # Horizontal divider (top of the lane)
        h_line = slide.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, Inches(0.5), y_pos, canvas_width - Inches(0.5), y_pos)
        h_line.line.color.rgb = COLOR_LANE_LINE
        h_line.line.width = Pt(1)
        
        # Lane Label
        label_box = slide.shapes.add_textbox(Inches(0.5), y_pos, header_width - Inches(0.6), lane_height)
        label_tf = label_box.text_frame
        label_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        lp = label_tf.paragraphs[0]
        lp.text = lane_name
        lp.font.size = Pt(18)
        lp.font.color.rgb = COLOR_TEXT_MAIN
        lp.alignment = PP_ALIGN.LEFT

    # Bottom border
    y_pos_bottom = start_y + (len(lanes) * lane_height)
    b_line = slide.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, Inches(0.5), y_pos_bottom, canvas_width - Inches(0.5), y_pos_bottom)
    b_line.line.color.rgb = COLOR_LANE_LINE
    b_line.line.width = Pt(1.5)

    # --- Define Process Nodes ---
    # Grid coordinates: lane index (y), abstract col index (x)
    col_w = Inches(1.8)
    offset_x = header_width + Inches(0.5)
    
    nodes_data = [
        {"id": "start", "label": "Start", "type": "term", "lane": 0, "col": 0},
        {"id": "step1", "label": "Step 1", "type": "proc", "lane": 0, "col": 1},
        {"id": "dec1",  "label": "Decision\nPoint", "type": "dec", "lane": 1, "col": 2},
        {"id": "step2", "label": "Step 2", "type": "proc", "lane": 1, "col": 3},
        {"id": "step3", "label": "Step 3", "type": "proc", "lane": 2, "col": 2},
        {"id": "db1",   "label": "Database", "type": "db", "lane": 0, "col": 2.5},
        {"id": "step4", "label": "Step 4", "type": "proc", "lane": 3, "col": 4},
        {"id": "end",   "label": "Finish", "type": "term", "lane": 3, "col": 5},
    ]

    shapes_dict = {}

    # Helper function to style text
    def style_node_text(shape, text, is_dark_bg=True):
        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(255, 255, 255) if is_dark_bg else COLOR_TEXT_MAIN

    # --- Render Nodes ---
    for nd in nodes_data:
        center_x = offset_x + (nd["col"] * col_w)
        center_y = start_y + (nd["lane"] * lane_height) + (lane_height / 2)
        
        node_type = nd["type"]
        w = Inches(1.2)
        h = Inches(0.6)
        
        if node_type == "term":
            s = slide.shapes.add_shape(MSO_SHAPE.FLOWCHART_TERMINATOR, center_x - w/2, center_y - h/2, w, h)
            s.fill.solid()
            s.fill.fore_color.rgb = COLOR_NODE_PROCESS
            s.line.color.rgb = COLOR_NODE_PROCESS
            style_node_text(s, nd["label"], is_dark_bg=True)
            
        elif node_type == "proc":
            s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, center_x - w/2, center_y - h/2, w, h)
            s.fill.solid()
            s.fill.fore_color.rgb = COLOR_NODE_PROCESS
            s.line.color.rgb = COLOR_NODE_PROCESS
            style_node_text(s, nd["label"], is_dark_bg=True)
            
        elif node_type == "dec":
            w_dec = Inches(1.4)
            h_dec = Inches(0.8)
            s = slide.shapes.add_shape(MSO_SHAPE.FLOWCHART_DECISION, center_x - w_dec/2, center_y - h_dec/2, w_dec, h_dec)
            s.fill.solid()
            s.fill.fore_color.rgb = COLOR_NODE_DECISION
            s.line.color.rgb = COLOR_DECISION_OUTLINE
            s.line.width = Pt(1.5)
            style_node_text(s, nd["label"], is_dark_bg=False)
            
        elif node_type == "db":
            h_db = Inches(0.8)
            s = slide.shapes.add_shape(MSO_SHAPE.FLOWCHART_MAGNETIC_DISK, center_x - w/2, center_y - h_db/2, w, h_db)
            s.fill.solid()
            s.fill.fore_color.rgb = RGBColor(245, 245, 245)
            s.line.color.rgb = COLOR_DECISION_OUTLINE
            style_node_text(s, nd["label"], is_dark_bg=False)
            
        shapes_dict[nd["id"]] = s

    # --- Render Connectors ---
    # Tuples: (source_id, dest_id, source_site, dest_site, label)
    # Note: connection sites (0,1,2,3) usually map to Top, Left, Bottom, Right but varies slightly by shape.
    # We will use 3 (Right) to 1 (Left) as standard horizontal flow, and 2 (Bottom) to 0 (Top) for vertical.
    edges = [
        ("start", "step1", 3, 1, ""),
        ("step1", "dec1", 3, 1, ""),
        ("step1", "db1", 0, 1, ""),
        ("dec1", "step2", 3, 1, "Yes"),
        ("dec1", "step3", 2, 0, "No"),
        ("step2", "step4", 3, 0, ""),
        ("step3", "step4", 3, 1, ""),
        ("step4", "end", 3, 1, "")
    ]

    # Helper function to add arrowhead via lxml
    def add_end_arrow(connector_shape):
        ln = connector_shape.line._ln
        if ln is not None:
            tailEnd = OxmlElement('a:tailEnd')
            tailEnd.set('type', 'triangle')
            tailEnd.set('w', 'med')
            tailEnd.set('len', 'med')
            ln.append(tailEnd)

    for edge in edges:
        src_id, dst_id, src_site, dst_site, label = edge
        src_shape = shapes_dict[src_id]
        dst_shape = shapes_dict[dst_id]
        
        # Add Elbow Connector
        connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, Pt(0), Pt(0), Pt(10), Pt(10))
        connector.begin_connect(src_shape, src_site)
        connector.end_connect(dst_shape, dst_site)
        
        # Style Line
        connector.line.color.rgb = COLOR_CONNECTOR
        connector.line.width = Pt(1.5)
        add_end_arrow(connector)
        
        # Add Branch Label if exists
        if label:
            # Estimate mid-point roughly for label placement
            # (PPT routes dynamically, so we approximate bounding box centers)
            sx = src_shape.left + src_shape.width/2
            sy = src_shape.top + src_shape.height/2
            dx = dst_shape.left + dst_shape.width/2
            dy = dst_shape.top + dst_shape.height/2
            
            mid_x = sx + (dx - sx) * 0.4  # Slightly biased towards source
            mid_y = sy + (dy - sy) * 0.2
            if abs(dx - sx) < Inches(0.5): # Vertical line
                mid_x += Inches(0.2)
                mid_y = sy + (dy - sy) * 0.5
                
            lbl_box = slide.shapes.add_textbox(mid_x, mid_y, Inches(0.6), Inches(0.3))
            lbl_box.fill.solid()
            lbl_box.fill.fore_color.rgb = COLOR_NODE_DECISION
            lbl_box.line.color.rgb = COLOR_LANE_LINE
            
            ltf = lbl_box.text_frame
            ltf.margin_top = Pt(1)
            ltf.margin_bottom = Pt(1)
            ltf.margin_left = Pt(1)
            ltf.margin_right = Pt(1)
            lp = ltf.paragraphs[0]
            lp.text = label
            lp.font.size = Pt(10)
            lp.font.color.rgb = COLOR_TEXT_MAIN
            lp.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
