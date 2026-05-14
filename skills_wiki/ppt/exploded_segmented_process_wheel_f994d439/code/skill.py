def create_slide(
    output_pptx_path: str,
    title_text: str = "Segmented Process Cycle",
    body_text: str = "",
    bg_palette: str = "light",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Exploded Segmented Wheel visual effect.
    """
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 248, 250)  # Very light blue-gray

    # Add Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(1))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 41, 59)
    p.alignment = PP_ALIGN.CENTER

    # === Layer 2: Core Visual Effect (Exploded Wheel) ===
    # Configuration
    cx = Inches(13.333) / 2
    cy = Inches(7.5) / 2 + Inches(0.4) # Shifted down slightly
    radius = Inches(2.6)
    explosion = Inches(0.08) # Distance to separate the pieces
    num_slices = 8
    angle_step = 360 / num_slices
    
    # 8 vibrant colors mapping to the tutorial
    colors = [
        RGBColor(239, 68, 68),   # Red
        RGBColor(249, 115, 22),  # Orange
        RGBColor(234, 179, 8),   # Yellow
        RGBColor(34, 197, 94),   # Green
        RGBColor(6, 182, 212),   # Cyan
        RGBColor(59, 130, 246),  # Blue
        RGBColor(139, 92, 246),  # Purple
        RGBColor(236, 72, 153),  # Magenta
    ]

    labels = [
        "Initiation", "Planning", "Execution", "Monitoring",
        "Control", "Evaluation", "Optimization", "Closure"
    ]

    for i in range(num_slices):
        # Calculate angles (-90 starts at 12 o'clock)
        start_deg = i * angle_step - 90
        end_deg = (i + 1) * angle_step - 90
        mid_deg = (start_deg + end_deg) / 2
        
        mid_rad = math.radians(mid_deg)
        
        # Explosion offset (moves the entire wedge outwards along its bisector)
        dx = explosion * math.cos(mid_rad)
        dy = explosion * math.sin(mid_rad)
        
        # 1. Build the freeform wedge
        # start at the offset center
        builder = slide.shapes.build_freeform(cx + dx, cy + dy)
        
        # approximate the outer arc
        pts = []
        arc_steps = 15 # Provides a smooth curve for a 45-degree arc
        for j in range(arc_steps + 1):
            angle = start_deg + (end_deg - start_deg) * j / arc_steps
            rad = math.radians(angle)
            x = cx + dx + radius * math.cos(rad)
            y = cy + dy + radius * math.sin(rad)
            pts.append((x, y))
            
        # Draw arc and close path back to center
        builder.add_line_segments(pts, close=True)
        shape = builder.convert_to_shape()
        
        # 2. Styling the wedge
        color = colors[i]
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        # Set line to same color to prevent default blue borders
        shape.line.color.rgb = color 
        shape.line.width = Pt(1)
        
        # 3. Add Drop Shadow (lxml)
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                     blurRad="50000", dist="35000", dir="2700000", algn="ctr", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
        etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="18000") # 18% opacity
        
        # === Layer 3: Text Placement ===
        # Position text halfway along the radius
        d_text = radius * 0.65
        tx = cx + dx + d_text * math.cos(mid_rad)
        ty = cy + dy + d_text * math.sin(mid_rad)
        
        # Add textbox centered on (tx, ty)
        tw, th = Inches(1.5), Inches(0.8)
        tbox = slide.shapes.add_textbox(tx - tw/2, ty - th/2, tw, th)
        t_frame = tbox.text_frame
        t_frame.word_wrap = True
        
        # Wedge Numbering
        p1 = t_frame.paragraphs[0]
        p1.text = f"0{i+1}"
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(255, 255, 255)
        p1.alignment = PP_ALIGN.CENTER
        
        # Wedge Label
        p2 = t_frame.add_paragraph()
        p2.text = labels[i]
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
