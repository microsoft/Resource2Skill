def create_slide(
    output_pptx_path: str,
    title_text: str = "Process Workflow Diagram",
    steps: list = ["Step 1\nInitiation", "Step 2\nPlanning", "Step 3\nExecution", "Step 4\nClosure"],
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Automated SmartArt-Style Process Flowchart.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree
    from PIL import Image, ImageDraw
    import os

    # --- Helper Functions for OOXML Injection ---
    def remove_outline(shape):
        """Removes the border/outline from a shape via XML."""
        spPr = shape.element.spPr
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        ln = spPr.find('.//a:ln', namespaces=ns)
        if ln is not None:
            spPr.remove(ln)

    def add_drop_shadow(shape):
        """Injects a modern drop shadow to the shape."""
        spPr = shape.element.spPr
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        effectLst = spPr.find('.//a:effectLst', namespaces=ns)
        if effectLst is None:
            effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        
        # 45 degree shadow (2700000), 35% opacity (35000), distance and blur
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                     blurRad="50000", dist="40000", dir="2700000", algn="tl", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
        etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="35000")

    def apply_transparency(shape, alpha_percent=30):
        """Applies transparency to an existing solid fill."""
        spPr = shape.element.spPr
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        srgbClr = spPr.find('.//a:solidFill/a:srgbClr', namespaces=ns)
        if srgbClr is not None:
            alpha_val = str(int(alpha_percent * 1000))
            etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val=alpha_val)

    # --- 1. Background Generation (PIL) ---
    bg_path = "process_bg_temp.png"
    img = Image.new("RGB", (1920, 1080))
    draw = ImageDraw.Draw(img)
    color_top = (26, 42, 58)    # Dark slate
    color_bottom = (13, 23, 33) # Deep navy
    for y in range(1080):
        ratio = y / 1080.0
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    img.save(bg_path)

    # --- 2. Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Insert Background
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # --- 3. Title Element ---
    title_box = slide.shapes.add_textbox(Inches(1.16), Inches(1), Inches(11), Inches(1))
    tf = title_box.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Segoe UI"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # --- 4. Layout Mathematics ---
    N = len(steps)
    flowchart_w = Inches(11.0)
    start_x = (prs.slide_width - flowchart_w) / 2
    y_pos = Inches(3.2)
    
    # Calculate widths based on aspect ratios
    # Box gets standard width, Arrow gets 40% of Box width
    arrow_ratio = 0.4
    box_w = flowchart_w / (N + arrow_ratio * (N - 1))
    spacing = box_w * arrow_ratio
    
    box_h = Inches(1.6)
    arrow_h = Inches(0.6)
    overlap = Inches(0.2) # Tuck the arrows behind the boxes

    box_colors = [
        RGBColor(238, 82, 83),  # Deep Red
        RGBColor(255, 159, 67), # Orange
        RGBColor(10, 189, 227), # Cyan
        RGBColor(16, 172, 132)  # Dark Green
    ]

    # --- 5. Render Arrows FIRST (Sent to back implicitly) ---
    for i in range(N - 1):
        x = start_x + i * (box_w + spacing)
        arrow_x = x + box_w - overlap
        arrow_y = y_pos + (box_h - arrow_h) / 2
        actual_arrow_w = spacing + (2 * overlap)
        
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arrow_x, arrow_y, actual_arrow_w, arrow_h)
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = RGBColor(255, 255, 255)
        remove_outline(arrow)
        apply_transparency(arrow, 30) # 30% Opacity White

    # --- 6. Render Step Boxes ---
    for i in range(N):
        x = start_x + i * (box_w + spacing)
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y_pos, box_w, box_h)
        
        # Color & Styling
        box.fill.solid()
        box.fill.fore_color.rgb = box_colors[i % len(box_colors)]
        remove_outline(box)
        add_drop_shadow(box)
        
        # Typography
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.text = steps[i]
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Segoe UI"
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    # --- 7. Cleanup & Save ---
    prs.save(output_pptx_path)
    
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
