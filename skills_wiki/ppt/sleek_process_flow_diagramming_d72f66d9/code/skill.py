def create_slide(
    output_pptx_path: str,
    title_text: str = "PROCESS FLOW DIAGRAM",
    theme_color: tuple = (38, 166, 154),   # Teal
    accent_color: tuple = (242, 146, 33),  # Orange
    bg_color: tuple = (226, 241, 248),     # Soft Light Cyan
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Sleek Process Flow Diagram visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml.xmlchemy import OxmlElement

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # Optional: Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(6), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Century Gothic"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(50, 50, 50)

    # === Helper Functions ===

    def apply_shadow(shape):
        """Injects XML for a subtle drop shadow."""
        spPr = shape.element.spPr
        effectLst = OxmlElement('a:effectLst')
        outerShdw = OxmlElement('a:outerShdw')
        outerShdw.set('blurRad', '60000')   # 6pt blur
        outerShdw.set('dist', '40000')      # 4pt distance
        outerShdw.set('dir', '2700000')     # 45 degrees
        outerShdw.set('algn', 'tl')
        
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '25000')           # 25% opacity
        srgbClr.append(alpha)
        
        outerShdw.append(srgbClr)
        effectLst.append(outerShdw)
        spPr.append(effectLst)

    def create_node(text, shape_type, left, top, width, height):
        """Creates and formats a flowchart node."""
        shape = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
        
        # Fill & Line
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*theme_color)
        shape.line.color.rgb = RGBColor(255, 255, 255)
        shape.line.width = Pt(2.25)
        
        # Text
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Century Gothic"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        apply_shadow(shape)
        return shape

    def draw_path(points):
        """Draws a precise polyline connector with an arrowhead."""
        # Convert tuples from inches to EMU internally
        builder = slide.shapes.build_freeform(Inches(points[0][0]), Inches(points[0][1]))
        for pt in points[1:]:
            builder.add_line_segments([(Inches(pt[0]), Inches(pt[1]))], close=False)
        
        line_shape = builder.convert_to_shape()
        line_shape.line.color.rgb = RGBColor(*accent_color)
        line_shape.line.width = Pt(3.25)
        
        # Inject Arrowhead XML
        ln = line_shape.line._get_or_add_ln()
        tailEnd = OxmlElement('a:tailEnd')
        tailEnd.set('type', 'triangle')
        tailEnd.set('w', 'lg')
        tailEnd.set('len', 'lg')
        ln.append(tailEnd)
        return line_shape

    # === Layer 2: Shape Instantiation ===
    
    # Grid Logic (Center alignments)
    y_center = 3.75
    y_top = 1.9
    y_bot = 5.6

    create_node("START", MSO_SHAPE.OVAL, 1.0, y_center - 0.5, 1.0, 1.0)
    create_node("DECISION", MSO_SHAPE.DIAMOND, 2.8, y_center - 0.75, 1.5, 1.5)
    
    create_node("PROCESS 1", MSO_SHAPE.RECTANGLE, 5.5, y_top - 0.4, 2.0, 0.8)
    create_node("PROCESS 2", MSO_SHAPE.RECTANGLE, 5.5, y_center - 0.4, 2.0, 0.8)
    create_node("PROCESS 3", MSO_SHAPE.RECTANGLE, 5.5, y_bot - 0.4, 2.0, 0.8)
    
    create_node("ACTION", MSO_SHAPE.PARALLELOGRAM, 8.5, y_center - 0.4, 2.0, 0.8)
    create_node("END", MSO_SHAPE.OVAL, 11.3, y_center - 0.5, 1.0, 1.0)

    # === Layer 3: Connectors ===
    # Defining strict orthogonal paths (X, Y) in inches
    
    # 1. Start to Decision (Straight)
    draw_path([(2.0, y_center), (2.8, y_center)])
    
    # 2. Decision Top to Process 1 (Elbow: Up, then Right)
    draw_path([(3.55, y_center - 0.75), (3.55, y_top), (5.5, y_top)])
    
    # 3. Decision Right to Process 2 (Straight)
    draw_path([(4.3, y_center), (5.5, y_center)])
    
    # 4. Decision Bottom to Process 3 (Elbow: Down, then Right)
    draw_path([(3.55, y_center + 0.75), (3.55, y_bot), (5.5, y_bot)])
    
    # 5. Process 1 to Action Top (Elbow: Right, then Down)
    draw_path([(7.5, y_top), (9.5, y_top), (9.5, y_center - 0.4)])
    
    # 6. Process 2 to Action Left (Straight)
    draw_path([(7.5, y_center), (8.7, y_center)]) # 8.7 accounts for parallelogram slant
    
    # 7. Process 3 to Action Bottom (Elbow: Right, then Up)
    draw_path([(7.5, y_bot), (9.5, y_bot), (9.5, y_center + 0.4)])
    
    # 8. Action to End (Straight)
    draw_path([(10.3, y_center), (11.3, y_center)])

    prs.save(output_pptx_path)
    return output_pptx_path
