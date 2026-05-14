def create_slide(
    output_pptx_path: str,
    title_text: str = "Process Flowchart",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dynamic Native Flowchart Layout.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml.xmlchemy import OxmlElement

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Helper Functions ===

    def format_shape(sp, fill_color=None, text_color=RGBColor(0, 0, 0)):
        """Applies uniform flowchart formatting to a shape."""
        # Solid outline
        sp.line.color.rgb = RGBColor(0, 0, 0)
        sp.line.width = Pt(1.5)
        
        # Fill (default white to obscure background lines cleanly)
        sp.fill.solid()
        if fill_color:
            sp.fill.fore_color.rgb = fill_color
        else:
            sp.fill.fore_color.rgb = RGBColor(255, 255, 255)
            
        # Typography
        for p in sp.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for run in p.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(16)
                run.font.color.rgb = text_color
                
    def format_connector(connector):
        """Styles line and injects arrowhead via lxml."""
        connector.line.color.rgb = RGBColor(0, 0, 0)
        connector.line.width = Pt(1.5)
        
        spPr = connector.element.spPr
        ln = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
        if ln is not None:
            headEnd = ln.find('{http://schemas.openxmlformats.org/drawingml/2006/main}headEnd')
            if headEnd is None:
                headEnd = OxmlElement('a:headEnd')
                ln.append(headEnd)
            # Add medium triangle arrowhead
            headEnd.set('type', 'triangle')
            headEnd.set('w', 'med')
            headEnd.set('len', 'med')

    def add_connected_connector(source_sp, source_idx, target_sp, target_idx, conn_type=MSO_CONNECTOR.STRAIGHT):
        """Creates a connector actively anchored to shape connection sites."""
        # Initial coords are arbitrary; begin_connect/end_connect recalculates them
        connector = slide.shapes.add_connector(conn_type, Pt(0), Pt(0), Pt(100), Pt(100))
        connector.begin_connect(source_sp, source_idx)
        connector.end_connect(target_sp, target_idx)
        format_connector(connector)
        return connector

    # === Build Flowchart Nodes ===
    # Note on standard clockwise indices: 0=Top, 1=Right, 2=Bottom, 3=Left

    # 1. Start Node (Center Top)
    n1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.41), Inches(0.6), Inches(2.5), Inches(0.8))
    n1.text = "Start from home"
    format_shape(n1)

    # 2. Decision Diamond (Center)
    n2 = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, Inches(5.66), Inches(2.25), Inches(2.0), Inches(1.5))
    n2.text = "Before\n7 AM?"
    format_shape(n2)

    # 3. 'No' Node (Left Branch)
    n3l = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(3.26), Inches(2.6), Inches(0.8), Inches(0.8))
    n3l.text = "No"
    format_shape(n3l, fill_color=RGBColor(235, 83, 83)) # Red

    # 4. 'Yes' Node (Right Branch)
    n3r = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.26), Inches(2.6), Inches(0.8), Inches(0.8))
    n3r.text = "Yes"
    format_shape(n3r, fill_color=RGBColor(60, 179, 113)) # Green

    # 5. Expressway Node (Left Path)
    n4l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.41), Inches(4.1), Inches(2.5), Inches(0.8))
    n4l.text = "Expressway"
    format_shape(n4l)

    # 6. Shortcut Node (Right Path)
    n4r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.41), Inches(4.1), Inches(2.5), Inches(0.8))
    n4r.text = "Shortcut"
    format_shape(n4r)

    # 7. End Node (Center Bottom)
    n5 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.41), Inches(5.6), Inches(2.5), Inches(0.8))
    n5.text = "Office on time"
    format_shape(n5)

    # === Connect the Nodes ===
    
    # Start -> Decision (Straight down)
    add_connected_connector(n1, 2, n2, 0)
    
    # Decision -> No (Straight left)
    add_connected_connector(n2, 3, n3l, 1)
    
    # Decision -> Yes (Straight right)
    add_connected_connector(n2, 1, n3r, 3)
    
    # No -> Expressway (Straight down)
    add_connected_connector(n3l, 2, n4l, 0)
    
    # Yes -> Shortcut (Straight down)
    add_connected_connector(n3r, 2, n4r, 0)
    
    # Expressway -> End (Elbow down and right)
    add_connected_connector(n4l, 2, n5, 3, MSO_CONNECTOR.ELBOW)
    
    # Shortcut -> End (Elbow down and left)
    add_connected_connector(n4r, 2, n5, 1, MSO_CONNECTOR.ELBOW)

    # Save to path
    prs.save(output_pptx_path)
    return output_pptx_path
