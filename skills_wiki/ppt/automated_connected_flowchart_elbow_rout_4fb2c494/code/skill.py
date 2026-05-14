def create_slide(
    output_pptx_path: str,
    title_text: str = "Customer Support Process Flow",
    body_text: str = "",
    bg_palette: str = "corporate",  
    accent_color: tuple = (68, 114, 196),  # Standard corporate blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing an Automated Connected Flowchart.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Title Section ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(50, 50, 50)

    # === Helper Function 1: Add Node ===
    def add_node(text, left_in, top_in, width_in=2.5, height_in=0.8, fill_color=accent_color):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            Inches(left_in), Inches(top_in), 
            Inches(width_in), Inches(height_in)
        )
        
        # Format text
        shape.text = text
        tf = shape.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(14)
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        
        # Format styling
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*fill_color)
        shape.line.color.rgb = RGBColor(int(fill_color[0]*0.8), int(fill_color[1]*0.8), int(fill_color[2]*0.8))
        shape.line.width = Pt(1)
        
        return shape

    # === Helper Function 2: Add Snapped Connector with Arrow ===
    def add_connector(shape1, shape2, site1_idx, site2_idx):
        # Create elbow connector
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.ELBOW, Inches(0), Inches(0), Inches(1), Inches(1)
        )
        
        # Bind connection points
        connector.begin_connect(shape1, site1_idx)
        connector.end_connect(shape2, site2_idx)
        
        # Format line color & weight
        connector.line.color.rgb = RGBColor(120, 120, 120)
        connector.line.width = Pt(1.5)
        
        # LXML XML Injection: Add Arrowhead
        # PowerPoint standard schema namespace for drawingml
        a_ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
        spPr = connector.element.find('.//p:spPr', namespaces=connector.element.nsmap)
        
        if spPr is not None:
            ln = spPr.find('.//a:ln', namespaces=connector.element.nsmap)
            if ln is not None:
                # Add or update tailEnd for arrow
                tail = ln.find(f'.//{{{a_ns}}}tailEnd')
                if tail is None:
                    tail = etree.SubElement(ln, f'{{{a_ns}}}tailEnd')
                tail.set('type', 'triangle')
                tail.set('w', 'med')
                tail.set('len', 'med')

    # === Layer 1: Build the Nodes ===
    # Standard PPT connection sites for Rectangles: 0=Top, 1=Right, 2=Bottom, 3=Left
    
    # Main vertical flow
    node1 = add_node("Customer Submits Issue", 5.4, 1.5)
    node2 = add_node("System Creates Ticket", 5.4, 3.0)
    node3 = add_node("Agent Reviews Issue", 5.4, 4.5)
    node4 = add_node("Issue Resolved", 5.4, 6.0, fill_color=(46, 172, 109))  # Green ending
    
    # Branching flow
    node5 = add_node("Escalate to Tier 2", 9.0, 3.0, fill_color=(235, 120, 40)) # Orange branch
    node6 = add_node("Developer Fix Required", 9.0, 4.5, fill_color=(235, 120, 40))

    # === Layer 2: Wire the Connections ===
    # Connect downward (Bottom of 1 -> Top of 2)
    add_connector(node1, node2, 2, 0)
    add_connector(node2, node3, 2, 0)
    add_connector(node3, node4, 2, 0)
    
    # Connect branch (Right of 2 -> Left of 5)
    add_connector(node2, node5, 1, 3)
    
    # Connect down branch (Bottom of 5 -> Top of 6)
    add_connector(node5, node6, 2, 0)
    
    # Route branch back (Bottom of 6 -> Right of 4)
    add_connector(node6, node4, 2, 1)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
