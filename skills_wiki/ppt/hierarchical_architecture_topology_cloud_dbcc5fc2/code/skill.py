def create_slide(
    output_pptx_path: str,
    title_text: str = "Multi-region API Gateway Architecture",
    body_text: str = "",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Hierarchical Architecture Topology" visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.enum.line import MSO_LINE_DASH_STYLE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Color Palette
    COLOR_TEXT = RGBColor(35, 47, 62)
    COLOR_BOUNDARY = RGBColor(135, 149, 150)
    COLOR_CALLOUT = RGBColor(0, 115, 187)
    
    # Domain Colors (AWS-inspired)
    C_NET = RGBColor(140, 79, 255)   # Purple (Route 53, CloudFront, API Gateway)
    C_COMP = RGBColor(237, 113, 0)   # Orange (Lambda)
    C_DB = RGBColor(51, 85, 218)     # Blue (Aurora)
    C_GEN = RGBColor(100, 100, 100)  # Gray (Client)

    # --- Helper Functions ---
    def draw_container(name, left, top, width, height, dash=False):
        """Draws a boundary box with a label."""
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.background() # Transparent
        shape.line.color.rgb = COLOR_BOUNDARY
        shape.line.width = Pt(1.5)
        if dash:
            shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        
        # Add label at top left
        txBox = slide.shapes.add_textbox(left, top, Inches(2), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        return shape

    def draw_node(name, left, top, color):
        """Draws a service node (white box, colored border, colored text)."""
        w, h = Inches(1.4), Inches(1.0)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = color
        shape.line.width = Pt(2.5)
        
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = name
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = color
        return shape, (left + w/2, top + h/2), (left, top, w, h) # return shape, center coords, rect

    def draw_line(pt1, pt2):
        """Draws a connecting arrow between two points."""
        connector = slide.shapes.add_connector(
            1, pt1[0], pt1[1], pt2[0], pt2[1]  # 1 = MSO_CONNECTOR.STRAIGHT
        )
        connector.line.color.rgb = COLOR_BOUNDARY
        connector.line.width = Pt(1.5)
        # To add an arrow head, we use a slight XML hack or rely on default properties. 
        # python-pptx doesn't expose line end arrowheads easily in the top-level API, 
        # but for a pure architecture map, the clean straight line is standard.
        return connector

    def draw_callout(number, cx, cy):
        """Draws a numbered circular badge."""
        r = Inches(0.18)
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - r, cy - r, r*2, r*2)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CALLOUT
        shape.line.fill.background() # No border
        
        tf = shape.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = str(number)
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        return shape

    # --- Step 1: Add Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT

    # --- Step 2: Draw Structural Containers ---
    # Global AWS Cloud Box
    draw_container("AWS Cloud", Inches(2.5), Inches(1.2), Inches(10.0), Inches(5.8), dash=False)
    # Region A Box
    draw_container("Region A", Inches(6.0), Inches(1.5), Inches(6.2), Inches(2.4), dash=True)
    # Region B Box
    draw_container("Region B", Inches(6.0), Inches(4.3), Inches(6.2), Inches(2.4), dash=True)

    # --- Step 3: Draw Nodes (Grid System) ---
    col_1 = Inches(0.6) # Outside AWS
    col_2 = Inches(3.0) # Global AWS
    col_3 = Inches(4.5) # Global AWS (CloudFront)
    col_4 = Inches(6.4) # API Gateway
    col_5 = Inches(8.4) # Lambda
    col_6 = Inches(10.4) # DB
    
    row_A = Inches(2.2)
    row_B = Inches(5.0)

    # Instantiate Nodes
    _, c_client, _ = draw_node("Global Clients", col_1, Inches(3.6), C_GEN)
    
    _, c_r53, _ = draw_node("Route 53", col_2, Inches(3.6), C_NET)
    _, c_cf, _  = draw_node("CloudFront", col_3, Inches(3.6), C_NET)
    
    # Region A Nodes
    _, c_api_a, _ = draw_node("API Gateway", col_4, row_A, C_NET)
    _, c_lam_a, _ = draw_node("Lambda Handlers", col_5, row_A, C_COMP)
    _, c_db_a, _  = draw_node("Aurora DB\n(Primary)", col_6, row_A, C_DB)

    # Region B Nodes
    _, c_api_b, _ = draw_node("API Gateway", col_4, row_B, C_NET)
    _, c_lam_b, _ = draw_node("Lambda Handlers", col_5, row_B, C_COMP)
    _, c_db_b, _  = draw_node("Aurora DB\n(Replica)", col_6, row_B, C_DB)

    # --- Step 4: Draw Connecting Lines ---
    draw_line(c_client, c_r53)
    draw_line(c_r53, c_cf)
    
    # Orthogonal routing simulation (point-to-point for simplicity in PPTX math)
    draw_line(c_cf, c_api_a)
    draw_line(c_cf, c_api_b)
    
    draw_line(c_api_a, c_lam_a)
    draw_line(c_lam_a, c_db_a)
    
    draw_line(c_api_b, c_lam_b)
    draw_line(c_lam_b, c_db_b)
    
    # DB Replication Line (Vertical)
    draw_line(c_db_a, c_db_b)

    # --- Step 5: Add Numbered Callouts ---
    draw_callout(1, col_2 + Inches(0.7), Inches(3.6) - Inches(0.6))  # Over Route 53
    draw_callout(2, col_3 + Inches(0.7), Inches(3.6) - Inches(0.6))  # Over CloudFront
    draw_callout(3, col_4 + Inches(0.7), row_A - Inches(0.6))        # Over API GW A
    draw_callout(4, col_6 + Inches(0.7), Inches(3.6))                # Between DBs for replication

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
