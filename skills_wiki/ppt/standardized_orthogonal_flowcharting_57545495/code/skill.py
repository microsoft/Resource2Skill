def create_slide(
    output_pptx_path: str,
    title_text: str = "Hiring Process Flowchart",
    shape_color: tuple = (68, 114, 196),  # Standard Corporate Blue
    text_color: tuple = (255, 255, 255),  # White
    **kwargs,
) -> str:
    """
    Creates a standardized, aligned flowchart using native PPTX shapes and elbow connectors.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Helper function to create and style nodes
    def add_node(shape_type, text, left, top, width=Inches(2), height=Inches(0.8)):
        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        
        # Style Fill
        fill = shape.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*shape_color)
        
        # Style Line
        shape.line.color.rgb = RGBColor(47, 85, 151)
        shape.line.width = Pt(1.5)
        
        # Style Text
        text_frame = shape.text_frame
        text_frame.text = text
        text_frame.word_wrap = True
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            paragraph.font.size = Pt(14)
            paragraph.font.name = 'Calibri'
            paragraph.font.bold = True
            paragraph.font.color.rgb = RGBColor(*text_color)
            
        return shape

    # Helper function to add branching text labels (Yes/No)
    def add_label(text, left, top):
        txBox = slide.shapes.add_textbox(left, top, Inches(0.8), Inches(0.4))
        tf = txBox.text_frame
        tf.text = text
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.name = 'Calibri'
        p.font.bold = True
        p.font.color.rgb = RGBColor(89, 89, 89)

    # Layout Parameters
    center_x = Inches(13.333 / 2) - Inches(1) # Offset by half shape width
    start_y = Inches(1.0)
    v_spacing = Inches(1.2)
    
    # === Add Title ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.8))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.size = Pt(28)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(*shape_color)

    # === Create Flowchart Nodes ===
    
    # 1. Begin (Terminator)
    node_begin = add_node(MSO_SHAPE.FLOWCHART_TERMINATOR, "Begin Hiring\nStage 1", center_x, start_y)
    
    # 2. Process
    node_login = add_node(MSO_SHAPE.FLOWCHART_PROCESS, "Login to job\nportal", center_x, start_y + v_spacing)
    
    # 3. Process
    node_screen = add_node(MSO_SHAPE.FLOWCHART_PROCESS, "Screen\nresumes", center_x, start_y + (v_spacing * 2))
    
    # 4. Decision
    node_decision = add_node(MSO_SHAPE.FLOWCHART_DECISION, "Resumes\napproved?", center_x, start_y + (v_spacing * 3), width=Inches(2), height=Inches(1.2))
    
    # 5. Process (Yes Branch - continues down)
    node_interview = add_node(MSO_SHAPE.FLOWCHART_PROCESS, "Call for\nInterview", center_x, start_y + (v_spacing * 4.2))
    
    # 6. Process (No Branch - branches right)
    node_reject = add_node(MSO_SHAPE.FLOWCHART_PROCESS, "Screen more\nresumes", center_x + Inches(3), start_y + (v_spacing * 3.2))
    
    # 7. End (Terminator)
    node_end = add_node(MSO_SHAPE.FLOWCHART_TERMINATOR, "End Hiring\nStage 1", center_x, start_y + (v_spacing * 5.4))

    # === Connect Nodes ===
    # Note on connection sites: Usually 0=Top, 1=Left, 2=Bottom, 3=Right. 
    # This varies slightly by shape, but works reliably for these specific auto-shapes.
    
    def connect_shapes(shapeA, siteA, shapeB, siteB):
        connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, Inches(0), Inches(0), Inches(1), Inches(1))
        connector.begin_connect(shapeA, siteA)
        connector.end_connect(shapeB, siteB)
        connector.line.color.rgb = RGBColor(89, 89, 89)
        connector.line.width = Pt(2)
        # Add arrow head
        connector.line._lineProperties.append(
            '<a:headEnd type="triangle" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'
        )

    # Add XML namespace mapping for the hacky arrow head injection
    import xml.etree.ElementTree as ET
    ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    
    # Function to properly set arrow heads via xml manipulation
    def add_arrow_head(connector):
        line_props = connector.line._lineProperties
        head_end = ET.Element('{http://schemas.openxmlformats.org/drawingml/2006/main}headEnd')
        head_end.set('type', 'triangle')
        head_end.set('w', 'med')
        head_end.set('len', 'med')
        line_props.append(head_end)

    def draw_connector(shapeA, siteA, shapeB, siteB):
        connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, Inches(0), Inches(0), Inches(1), Inches(1))
        connector.begin_connect(shapeA, siteA)
        connector.end_connect(shapeB, siteB)
        connector.line.color.rgb = RGBColor(89, 89, 89)
        connector.line.width = Pt(1.5)
        add_arrow_head(connector)

    # Vertical Connections (Bottom to Top)
    draw_connector(node_begin, 2, node_login, 0)
    draw_connector(node_login, 2, node_screen, 0)
    draw_connector(node_screen, 2, node_decision, 0)
    
    # Decision YES branch
    draw_connector(node_decision, 2, node_interview, 0)
    add_label("Yes", center_x + Inches(0.2), start_y + (v_spacing * 4) - Inches(0.2))
    
    # Decision NO branch
    draw_connector(node_decision, 3, node_reject, 1) # Right of diamond to Left of process
    add_label("No", center_x + Inches(2), start_y + (v_spacing * 3) + Inches(0.1))
    
    # Final step
    draw_connector(node_interview, 2, node_end, 0)

    # Loop back (No branch back up to screen resumes)
    draw_connector(node_reject, 0, node_screen, 3) # Top of reject to Right of screen

    prs.save(output_pptx_path)
    return output_pptx_path
