def create_slide(
    output_pptx_path: str,
    title_text: str = "Split-Screen Presentation Setup",
    body_text: str = "How to present with Zoom on a single monitor",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Windowed Slide Show' setup effect.
    The script generates a split-screen infographic and modifies the internal 
    XML so the presentation natively launches in a resizable window.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: OS Desktop Background Mockup ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(0, 120, 215)  # Windows 10 Blue
    bg.line.fill.background()

    # === Layer 2: Left Split (Zoom/Meeting App Mockup) ===
    left_x, left_y, left_w, left_h = Inches(0.5), Inches(1), Inches(5.8), Inches(5.5)
    
    # Main Window Body
    left_win = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, left_y, left_w, left_h)
    left_win.fill.solid()
    left_win.fill.fore_color.rgb = RGBColor(255, 255, 255)
    left_win.line.color.rgb = RGBColor(200, 200, 200)
    
    # Title Bar
    zoom_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, left_y, left_w, Inches(0.4))
    zoom_bar.fill.solid()
    zoom_bar.fill.fore_color.rgb = RGBColor(240, 240, 240)
    zoom_bar.line.fill.background()
    
    # Application Title
    tx_box1 = slide.shapes.add_textbox(left_x + Inches(0.1), left_y + Inches(0.05), Inches(3), Inches(0.3))
    tx1 = tx_box1.text_frame
    tx1.text = "📹 Zoom / Meeting App"
    tx1.paragraphs[0].font.size = Pt(14)
    tx1.paragraphs[0].font.bold = True
    tx1.paragraphs[0].font.color.rgb = RGBColor(50, 50, 50)

    # Empty content area visualization
    mock_video = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x + Inches(0.4), left_y + Inches(0.8), left_w - Inches(0.8), left_h - Inches(1.2))
    mock_video.fill.solid()
    mock_video.fill.fore_color.rgb = RGBColor(230, 230, 230)
    mock_video.line.fill.background()

    # === Layer 3: Right Split (PowerPoint Mockup) ===
    right_x, right_y, right_w, right_h = Inches(6.5), Inches(1), Inches(6.3), Inches(5.5)
    
    # Main Window Body
    right_win = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, right_y, right_w, right_h)
    right_win.fill.solid()
    right_win.fill.fore_color.rgb = RGBColor(255, 255, 255)
    right_win.line.color.rgb = RGBColor(200, 200, 200)
    
    # Title Bar
    pptx_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, right_y, right_w, Inches(0.4))
    pptx_bar.fill.solid()
    pptx_bar.fill.fore_color.rgb = RGBColor(196, 62, 28)  # PowerPoint Brand Orange
    pptx_bar.line.fill.background()
    
    # Application Title
    tx_box2 = slide.shapes.add_textbox(right_x + Inches(0.1), right_y + Inches(0.05), Inches(3), Inches(0.3))
    tx2 = tx_box2.text_frame
    tx2.text = "📊 PowerPoint Slide Show"
    tx2.paragraphs[0].font.size = Pt(14)
    tx2.paragraphs[0].font.bold = True
    tx2.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Contextual Instructions inside the right window
    inst_box = slide.shapes.add_textbox(right_x + Inches(0.4), right_y + Inches(0.8), right_w - Inches(0.8), right_h - Inches(1.2))
    inst_tf = inst_box.text_frame
    inst_tf.word_wrap = True
    
    p = inst_tf.add_paragraph()
    p.text = "How to use this pre-configured file:"
    p.font.bold = True
    p.font.size = Pt(22)
    p.font.color.rgb = RGBColor(40, 40, 40)
    
    instructions = [
        "1. This PPTX has been coded to open in 'Browsed by an individual (window)' mode.",
        "2. Press F5. Notice it opens in a resizable window, NOT full screen.",
        "3. Drag this window to the right edge of your screen to snap it.",
        "4. Open your meeting app (Zoom) and snap it to the left edge.",
        "5. Share Screen -> Select ONLY the PowerPoint window."
    ]
    
    for text in instructions:
        p_step = inst_tf.add_paragraph()
        p_step.text = text
        p_step.font.size = Pt(16)
        p_step.font.color.rgb = RGBColor(80, 80, 80)
        p_step.space_before = Pt(14)

    # === XML INJECTION: Force Windowed Slide Show Mode ===
    # Iterate through package parts to find the presentation properties XML
    for part in prs.part.package.parts:
        if '/ppt/presProps.xml' in str(part.partname):
            root = part.element
            nsmap = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            
            # Find the Slide Show Properties element
            show_pr = root.find('.//p:showPr', namespaces=nsmap)
            
            if show_pr is None:
                # Create it if it doesn't exist
                show_pr = etree.SubElement(root, '{http://schemas.openxmlformats.org/presentationml/2006/main}showPr')
            
            # Remove any existing presentation types to avoid schema conflicts
            for tag in ['present', 'kiosk', 'browse']:
                existing = show_pr.find(f'p:{tag}', namespaces=nsmap)
                if existing is not None:
                    show_pr.remove(existing)
            
            # Append the 'browse' element which forces Windowed mode
            browse = etree.SubElement(show_pr, '{http://schemas.openxmlformats.org/presentationml/2006/main}browse')
            browse.set('showScrollbar', '1')

    prs.save(output_pptx_path)
    return output_pptx_path
