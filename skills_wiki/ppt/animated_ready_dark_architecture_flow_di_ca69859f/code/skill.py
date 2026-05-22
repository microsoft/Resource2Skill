def create_slide(
    output_pptx_path: str,
    title_text: str = "Cloud Architecture Data Flow",
    body_text: str = "",
    bg_palette: str = "dark",
    accent_color: tuple = (255, 153, 0),  # AWS Orange for data tokens
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dark Mode Architecture Flow Diagram layout.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Dark Background ===
    bg_color = RGBColor(35, 47, 62)  # AWS Squid Ink Dark
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()

    # === Title Elements ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(10), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # === Utility function for Boundaries ===
    def add_boundary(x, y, w, h, border_color, label_text):
        # The boundary box
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        box.fill.background() # Transparent fill
        box.line.color.rgb = border_color
        box.line.width = Pt(2)
        
        # The top-left label
        lbl = slide.shapes.add_textbox(Inches(x + 0.1), Inches(y), Inches(3), Inches(0.5))
        lbl_tf = lbl.text_frame
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = label_text
        lbl_p.font.size = Pt(12)
        lbl_p.font.bold = True
        lbl_p.font.color.rgb = border_color
        return box

    # === Layer 2: Network Boundaries ===
    # Outer Boundary (e.g., VPC)
    add_boundary(1.0, 1.5, 11.3, 5.2, RGBColor(63, 134, 36), "Virtual private cloud (VPC)")
    
    # Inner Boundary (e.g., Public Subnet)
    add_boundary(1.5, 2.3, 10.3, 4.0, RGBColor(0, 124, 182), "Public subnet")

    # === Utility function for Nodes ===
    def add_node(x, y, text):
        node = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(1.8), Inches(1.2))
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor(50, 65, 85)
        node.line.color.rgb = RGBColor(200, 200, 200)
        node.line.width = Pt(1)
        
        tf = node.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(255, 255, 255)
        return node

    # === Layer 3: Nodes ===
    node_left = add_node(2.0, 4.0, "Client / Local Repo")
    node_center = add_node(5.75, 2.8, "Automation Server")
    node_right = add_node(9.5, 4.0, "Target Node")

    # === Layer 4: Connections ===
    def add_dashed_connector(shape_a, shape_b):
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.ELBOW, Inches(0), Inches(0), Inches(1), Inches(1)
        )
        # Connect to shapes (PowerPoint auto-routes elbow connectors)
        connector.begin_connect(shape_a, 3) # Right side of A
        connector.end_connect(shape_b, 1)   # Left/Bottom side of B (approximate)
        
        connector.line.color.rgb = RGBColor(255, 255, 255)
        connector.line.width = Pt(1.5)
        connector.line.dash_style = 7 # Dashed
        # Add an arrow head
        # Accessing line formatting via XML for the arrowhead (python-pptx limited natively here)
        return connector

    add_dashed_connector(node_left, node_center)
    add_dashed_connector(node_center, node_right)

    # Add a separate arrow going direct from Left to Right (e.g. bypassing server)
    conn3 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0), Inches(0), Inches(1), Inches(1))
    conn3.begin_connect(node_left, 3)
    conn3.end_connect(node_right, 1)
    conn3.line.color.rgb = RGBColor(150, 150, 150)
    conn3.line.width = Pt(1.5)
    conn3.line.dash_style = 7

    # === Layer 5: Data/Payload Tokens (Ready to be animated) ===
    def add_token(x, y, text_num):
        token = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.4), Inches(0.4))
        token.fill.solid()
        token.fill.fore_color.rgb = RGBColor(*accent_color)
        token.line.color.rgb = RGBColor(255, 255, 255)
        token.line.width = Pt(1)
        
        tf = token.text_frame
        p = tf.paragraphs[0]
        p.text = str(text_num)
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(35, 47, 62)
        return token

    # Place tokens next to the starting nodes, ready for the user to apply "Path Animation"
    add_token(3.9, 3.8, "1")
    add_token(7.6, 3.2, "2")
    add_token(5.5, 4.4, "3")

    prs.save(output_pptx_path)
    return output_pptx_path
