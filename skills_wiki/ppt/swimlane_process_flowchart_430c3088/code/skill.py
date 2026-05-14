def create_slide(
    output_pptx_path: str,
    title_text: str = "Cross-Functional Swimlane Flowchart",
    body_text: str = "",
    bg_palette: str = "business", 
    accent_color: tuple = (255, 140, 0),  # Deep Orange
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Swimlane Flowchart visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml.ns import qn
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Colors
    c_accent = RGBColor(*accent_color)
    c_white = RGBColor(255, 255, 255)
    c_dark_txt = RGBColor(60, 60, 60)
    c_border = RGBColor(160, 160, 160)
    c_lane_alt = RGBColor(245, 245, 250)

    # === Layer 1: Title ===
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.6))
    title.text = title_text
    p = title.text_frame.paragraphs[0]
    p.font.size = Pt(28)
    p.font.color.rgb = c_dark_txt
    p.font.bold = True

    # === Layer 2: Swimlane Grid ===
    lanes = ["Customer", "Sales Team", "Operations", "System / DB"]
    y_start = 1.0
    lane_h = 1.5

    for i, name in enumerate(lanes):
        y = y_start + i * lane_h
        
        # Alternating background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(y), Inches(12.3), Inches(lane_h))
        bg.line.fill.background()
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_lane_alt if i % 2 == 0 else c_white

        # Thin top divider line
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.5), Inches(y), Inches(12.8), Inches(y))
        line.line.color.rgb = RGBColor(220, 220, 225)
        
        # Lane Header Text
        tb = slide.shapes.add_textbox(Inches(0.5), Inches(y + 0.5), Inches(1.35), Inches(0.5))
        tb.text = name
        tp = tb.text_frame.paragraphs[0]
        tp.font.bold = True
        tp.font.size = Pt(11)
        tp.font.color.rgb = RGBColor(100, 100, 100)
        tp.alignment = PP_ALIGN.RIGHT

    # Bottom border line
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.5), Inches(y_start + 4*lane_h), Inches(12.8), Inches(y_start + 4*lane_h))
    line.line.color.rgb = RGBColor(220, 220, 225)

    # Vertical Header Separator
    vline = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(2.0), Inches(y_start), Inches(2.0), Inches(y_start + 4*lane_h))
    vline.line.color.rgb = RGBColor(220, 220, 225)


    # === Layer 3: Flowchart Nodes ===
    def add_node(shape_type, text, lane_idx, x_inch, w_inch=1.2, h_inch=0.6, fill=None, outline=None, font_clr=c_white):
        # Calculate Y center based on lane index (1-based)
        y_center = y_start + (lane_idx - 0.5) * lane_h
        y_inch = y_center - (h_inch / 2)
        
        shape = slide.shapes.add_shape(shape_type, Inches(x_inch), Inches(y_inch), Inches(w_inch), Inches(h_inch))
        shape.text = text
        
        # Style Shape
        shape.fill.solid()
        if fill: shape.fill.fore_color.rgb = fill
        if outline: 
            shape.line.color.rgb = outline
            shape.line.width = Pt(1.5)
        else: shape.line.fill.background()
            
        # Style Text
        shape.text_frame.word_wrap = True
        shape.text_frame.margin_left = Pt(2)
        shape.text_frame.margin_right = Pt(2)
        for paragraph in shape.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(9) if shape_type == MSO_SHAPE.FLOWCHART_DECISION else Pt(10)
                run.font.bold = True
                run.font.color.rgb = font_clr
        return shape

    # Instantiate the process steps
    n1 = add_node(MSO_SHAPE.FLOWCHART_TERMINAL, "Start", 1, 2.5, fill=c_accent)
    n2 = add_node(MSO_SHAPE.ROUNDED_RECTANGLE, "Receive\nOrder", 2, 4.5, fill=c_accent)
    n3 = add_node(MSO_SHAPE.FLOWCHART_DECISION, "Valid?", 2, 6.5, w_inch=1.1, h_inch=0.9, fill=c_white, outline=c_accent, font_clr=c_dark_txt)
    n4 = add_node(MSO_SHAPE.ROUNDED_RECTANGLE, "Reject\nOrder", 3, 6.5, fill=RGBColor(210, 210, 210), font_clr=c_dark_txt)
    n5 = add_node(MSO_SHAPE.ROUNDED_RECTANGLE, "Process\nFulfillment", 2, 8.5, fill=c_accent)
    n6 = add_node(MSO_SHAPE.CAN, "Database", 4, 8.5, fill=c_white, outline=c_border, font_clr=c_dark_txt)
    n7 = add_node(MSO_SHAPE.FLOWCHART_TERMINAL, "End", 1, 11.0, fill=c_accent)


    # === Layer 4: Connectors & Logic ===
    def inject_arrowhead(connector):
        """XML hack to add an arrowhead to a pptx connector."""
        spPr = connector.element.spPr
        ln = spPr.find(qn('a:ln'))
        if ln is None:
            ln = parse_xml(r'<a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
            spPr.append(ln)
        tailEnd = ln.find(qn('a:tailEnd'))
        if tailEnd is None:
            tailEnd = parse_xml(r'<a:tailEnd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" type="triangle"/>')
            ln.append(tailEnd)
        else:
            tailEnd.set('type', 'triangle')

    def connect(s1, site1, s2, site2, text=None):
        # site mapping (approx): 0=Top, 1=Right, 2=Bottom, 3=Left
        connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, Inches(0), Inches(0), Inches(1), Inches(1))
        connector.begin_connect(s1, site1)
        connector.end_connect(s2, site2)
        connector.line.color.rgb = c_border
        connector.line.width = Pt(1.5)
        inject_arrowhead(connector)
        
        # Add labels for Decision routes
        if text:
            # Estimate label placement
            if site1 == 1: # Moving Right
                mx, my = (s1.left + s1.width + s2.left) / 2, s1.top + (s1.height/2)
            elif site1 == 2: # Moving Down
                mx, my = s1.left + (s1.width/2), (s1.top + s1.height + s2.top) / 2
            else:
                mx, my = (s1.left + s2.left)/2, (s1.top + s2.top)/2
                
            tb = slide.shapes.add_textbox(mx - Inches(0.25), my - Inches(0.2), Inches(0.5), Inches(0.4))
            tb.text = text
            tb.fill.solid()
            tb.fill.fore_color.rgb = c_white # opaque background overlays the line perfectly
            tb.text_frame.margin_left = tb.text_frame.margin_right = Pt(0)
            tb.text_frame.margin_top = tb.text_frame.margin_bottom = Pt(0)
            
            p = tb.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = c_dark_txt
            p.alignment = PP_ALIGN.CENTER

    # Route the Flow
    connect(n1, 2, n2, 3)          # Start (Bottom) to Receive (Left)
    connect(n2, 1, n3, 3)          # Receive (Right) to Decision (Left)
    connect(n3, 2, n4, 0, "No")    # Decision (Bottom) to Reject (Top)
    connect(n3, 1, n5, 3, "Yes")   # Decision (Right) to Process (Left)
    connect(n5, 2, n6, 0)          # Process (Bottom) to DB (Top)
    connect(n5, 1, n7, 3)          # Process (Right) to End (Left)

    prs.save(output_pptx_path)
    return output_pptx_path
