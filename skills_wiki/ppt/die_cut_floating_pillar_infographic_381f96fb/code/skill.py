def create_slide(
    output_pptx_path: str,
    title_text: str = "POWERPOINT INFOGRAPHIC",
    option_titles: list = ["OPTION A", "OPTION B", "OPTION C", "OPTION D"],
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Die-Cut Floating Pillar Infographic" visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    # Create presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Helper function: Inject outer drop shadow via lxml
    def apply_drop_shadow(shape, blur_pt=10, dist_pt=3, angle_deg=45, alpha_pct=30):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
        outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw")
        
        outerShdw.set("blurRad", str(int(blur_pt * 12700)))
        outerShdw.set("dist", str(int(dist_pt * 12700)))
        outerShdw.set("dir", str(int(angle_deg * 60000)))
        outerShdw.set("algn", "tl")
        outerShdw.set("rotWithShape", "0")
        
        srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
        srgbClr.set("val", "000000") # Black shadow
        alpha = etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
        alpha.set("val", str(int((100 - alpha_pct) * 1000)))

    # --- 1. Background Generation (Diagonal Split) ---
    # Draw a black triangle filling the bottom right
    ff_builder = slide.shapes.build_freeform()
    ff_builder.add_line_segments([
        (Inches(0), Inches(7.5)),         # Bottom Left
        (Inches(13.333), Inches(0)),      # Top Right
        (Inches(13.333), Inches(7.5)),    # Bottom Right
        (Inches(0), Inches(7.5))          # Close path
    ])
    bg_triangle = ff_builder.convert_to_shape()
    bg_triangle.fill.solid()
    bg_triangle.fill.fore_color.rgb = RGBColor(0, 0, 0)
    bg_triangle.line.fill.background() # No line

    # Overall Slide Title
    title_box = slide.shapes.add_textbox(Inches(2), Inches(0.5), Inches(9.333), Inches(0.8))
    tf = title_box.text_frame
    tf.text = title_text
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(28)
    tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)

    # --- 2. Color Palette ---
    colors = [
        RGBColor(0, 112, 192),   # Option A: Blue
        RGBColor(0, 176, 80),    # Option B: Green
        RGBColor(255, 0, 0),     # Option C: Red
        RGBColor(112, 48, 160)   # Option D: Purple
    ]

    # --- 3. Geometric Parameters for Pillars ---
    num_pillars = 4
    pillar_w = 1.8
    pillar_h = 4.5
    start_x = 1.8
    spacing_x = (13.333 - (start_x * 2) - (pillar_w * num_pillars)) / (num_pillars - 1)
    y_offset = 2.0
    notch_h = 0.3
    
    body_text = "More information\nwill go here about\nthis option"

    # --- 4. Draw Pillars ---
    for i in range(num_pillars):
        x = start_x + i * (pillar_w + spacing_x)
        y = y_offset
        color = colors[i]

        # Draw the custom die-cut white pillar body
        builder = slide.shapes.build_freeform()
        builder.add_line_segments([
            (Inches(x), Inches(y)),                                        # Top Left
            (Inches(x + pillar_w*0.25), Inches(y)),                        # Top notch start
            (Inches(x + pillar_w*0.35), Inches(y + notch_h)),              # Top notch angle down
            (Inches(x + pillar_w*0.65), Inches(y + notch_h)),              # Top notch flat bottom
            (Inches(x + pillar_w*0.75), Inches(y)),                        # Top notch angle up
            (Inches(x + pillar_w), Inches(y)),                             # Top Right
            (Inches(x + pillar_w), Inches(y + pillar_h)),                  # Bottom Right
            (Inches(x + pillar_w/2), Inches(y + pillar_h - notch_h)),      # Bottom Center Inward Chevron
            (Inches(x), Inches(y + pillar_h)),                             # Bottom Left
            (Inches(x), Inches(y))                                         # Close to Top Left
        ])
        pillar = builder.convert_to_shape()
        pillar.fill.solid()
        pillar.fill.fore_color.rgb = RGBColor(255, 255, 255)
        pillar.line.fill.background()
        
        # Apply drop shadow to lift off background
        apply_drop_shadow(pillar, blur_pt=15, dist_pt=5, alpha_pct=25)

        # Draw Accent Hexagon (snaps into the top notch)
        # Using a snipped rectangle or custom hexagon. Since standard hexagon is pointed, 
        # we'll build a simple custom top cap that matches perfectly.
        top_builder = slide.shapes.build_freeform()
        top_builder.add_line_segments([
            (Inches(x + pillar_w*0.2), Inches(y - notch_h*0.8)),           # Top Left
            (Inches(x + pillar_w*0.8), Inches(y - notch_h*0.8)),           # Top Right
            (Inches(x + pillar_w*0.75), Inches(y + notch_h*0.5)),          # Bottom Right angled in
            (Inches(x + pillar_w*0.25), Inches(y + notch_h*0.5)),          # Bottom Left angled in
            (Inches(x + pillar_w*0.2), Inches(y - notch_h*0.8))            # Close
        ])
        top_cap = top_builder.convert_to_shape()
        top_cap.fill.solid()
        top_cap.fill.fore_color.rgb = color
        top_cap.line.fill.background()

        # Add Option Letter (inside the top cap)
        cap_txt = slide.shapes.add_textbox(Inches(x), Inches(y - notch_h*0.7), Inches(pillar_w), Inches(notch_h*1.2))
        tf = cap_txt.text_frame
        tf.text = option_titles[i].replace(" ", "\n")
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(12)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        if len(tf.paragraphs) > 1:
             tf.paragraphs[1].alignment = PP_ALIGN.CENTER
             tf.paragraphs[1].font.size = Pt(16)
             tf.paragraphs[1].font.bold = True
             tf.paragraphs[1].font.color.rgb = RGBColor(255, 255, 255)

        # Add Main Title (Colored)
        m_txt = slide.shapes.add_textbox(Inches(x), Inches(y + 0.8), Inches(pillar_w), Inches(0.5))
        tf_m = m_txt.text_frame
        tf_m.text = "MAIN TITLE"
        tf_m.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf_m.paragraphs[0].font.size = Pt(14)
        tf_m.paragraphs[0].font.bold = True
        tf_m.paragraphs[0].font.color.rgb = color

        # Add Body Text (Grey)
        b_txt = slide.shapes.add_textbox(Inches(x + 0.1), Inches(y + 1.4), Inches(pillar_w - 0.2), Inches(1.5))
        tf_b = b_txt.text_frame
        tf_b.word_wrap = True
        p = tf_b.paragraphs[0]
        p.text = body_text
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(89, 89, 89)

        # Add decorative circular icon placeholder at bottom
        icon_size = 0.5
        icon_y = y + pillar_h - notch_h - 0.8
        icon = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(x + (pillar_w - icon_size)/2), 
            Inches(icon_y), 
            Inches(icon_size), 
            Inches(icon_size)
        )
        icon.fill.solid()
        icon.fill.fore_color.rgb = RGBColor(255, 255, 255)
        icon.line.color.rgb = color
        icon.line.width = Pt(2)
        
        # Add a tiny accent line/circle inside the icon to simulate detail
        inner_icon = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(x + (pillar_w - icon_size)/2 + 0.15), 
            Inches(icon_y + 0.15), 
            Inches(icon_size - 0.3), 
            Inches(icon_size - 0.3)
        )
        inner_icon.fill.solid()
        inner_icon.fill.fore_color.rgb = color
        inner_icon.line.fill.background()

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
