def create_slide(
    output_pptx_path: str,
    title_text: str = "Product Capability Comparison",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Comprehensive Capability Comparison Matrix.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # --- Color Palette ---
    dark_teal = RGBColor(45, 75, 70)
    primary_teal = RGBColor(82, 121, 118)
    light_grey = RGBColor(240, 245, 245)  # Subtle cool grey for alternating rows
    white = RGBColor(255, 255, 255)
    text_dark = RGBColor(50, 50, 50)
    check_green = RGBColor(0, 168, 89)
    cross_red = RGBColor(224, 58, 62)

    # --- Slide Title & Subtitle ---
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1.0))
    tf = txBox.text_frame
    
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.color.rgb = dark_teal
    p.font.name = "Calibri"
    p.font.bold = True

    p2 = tf.add_paragraph()
    p2.text = "Feature breakdown across different service tiers and competitors"
    p2.font.size = Pt(16)
    p2.font.color.rgb = primary_teal
    p2.font.name = "Calibri"

    # --- Decorative Top Anchor Bar ---
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.5), Inches(1.6), Inches(12.333), Inches(0.06)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = dark_teal
    bar.line.fill.background()  # Transparent border

    # --- Table Data Structure ---
    headers = ["Core Parameters", "Basic Tier", "Professional", "Business Plus", "Enterprise"]
    features = [
        "Customizable user dashboard",
        "Cloud storage capacity",
        "Responsive mobile app access",
        "Free monthly premium add-ons",
        "Fully hosted & managed infrastructure",
        "White-labeling / Remove branding",
        "24/7 Priority Support SLAs"
    ]
    
    # Use Unicode for visual status: ✔ (\u2714), ✘ (\u2718)
    data = [
        ["\u2714", "\u2714", "\u2714", "\u2714"],
        ["10 GB", "50 GB", "\u2714 (Unlimited)", "\u2714 (Unlimited)"],
        ["\u2718", "\u2714", "\u2714", "\u2714"],
        ["\u2718", "\u2718", "\u2714", "\u2714"],
        ["\u2718", "\u2718", "\u2714", "\u2714"],
        ["\u2718", "\u2718", "\u2718", "\u2714"],
        ["\u2718", "Email only", "Phone + Email", "Dedicated Rep"]
    ]

    rows = len(features) + 1
    cols = len(headers)
    
    # Table geometry positioning
    left = Inches(0.5)
    top = Inches(1.8)
    width = Inches(12.333)
    height = Inches(4.8)
    
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Adjust column widths based on hierarchy (Parameter column gets more space)
    table.columns[0].width = Inches(3.533)
    for c in range(1, cols):
        table.columns[c].width = Inches(2.2)

    # --- Matrix Formatting & Styling ---
    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.15)
            cell.margin_right = Inches(0.15)
            
            # 1. Determine Background Color based on position
            if r == 0:
                bg_color = primary_teal    # Top Header Row
            elif c == 0:
                bg_color = dark_teal       # Left Parameter Column
            else:
                bg_color = light_grey if r % 2 == 1 else white  # Alternating Data Rows
                
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
            
            # 2. Extract Text Content
            if r == 0:
                text = headers[c]
            elif c == 0:
                text = features[r-1]
            else:
                text = data[r-1][c-1]
                
            # 3. Apply Text Formatting & Alignments
            tf = cell.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = text
            p.font.name = "Calibri"
            
            # Styling logic based on cell role
            if r == 0 or c == 0:
                # Header and Parameter styling
                p.font.color.rgb = white
                p.font.bold = True
                p.font.size = Pt(14)
                p.alignment = PP_ALIGN.CENTER if r == 0 else PP_ALIGN.LEFT
            else:
                # Data styling
                p.font.size = Pt(13)
                p.alignment = PP_ALIGN.CENTER
                
                # Checkmarks and Crosses specific styling (Color injection)
                if "\u2714" in text:
                    p.font.color.rgb = check_green
                    p.font.bold = True
                    # If it's just the checkmark, make it bigger
                    if text == "\u2714":
                        p.font.size = Pt(18)
                elif "\u2718" in text:
                    p.font.color.rgb = cross_red
                    p.font.bold = True
                    if text == "\u2718":
                        p.font.size = Pt(18)
                else:
                    p.font.color.rgb = text_dark

    prs.save(output_pptx_path)
    return output_pptx_path
