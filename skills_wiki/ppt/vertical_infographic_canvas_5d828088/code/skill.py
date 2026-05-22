def create_slide(
    output_pptx_path: str,
    title_text: str = "TIPS FOR WORKING\nFROM HOME",
    body_text: str = "As many people adapt to a work-from-home lifestyle, it is important to integrate key routines. Here are tips and techniques to ensure you are productive.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Vertical Infographic Canvas' visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    
    # 1. SET CUSTOM VERTICAL SLIDE DIMENSIONS (Core mechanism from tutorial)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(26.666)  # 1:2 ratio (Double standard height)
    
    # Use a blank slide layout
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # --- Color Palette (Extracted from video style) ---
    c_header_bg = RGBColor(84, 106, 123)     # Slate Navy
    c_text_light = RGBColor(255, 255, 255)
    c_text_dark = RGBColor(40, 40, 40)
    
    # Alternating band colors
    band_colors = [
        RGBColor(115, 153, 172),  # Steel Blue
        RGBColor(226, 192, 143),  # Sand/Orange
        RGBColor(204, 214, 217),  # Light Gray
        RGBColor(115, 153, 172),  # Steel Blue (repeat)
        RGBColor(226, 192, 143),  # Sand/Orange (repeat)
    ]

    # Content for the infographic sections
    sections = [
        {"num": "1", "title": "ESTABLISH A ROUTINE", "icon": MSO_SHAPE.MATH_PLUS},
        {"num": "2", "title": "SCHEDULE BREAKS", "icon": MSO_SHAPE.MATH_MINUS},
        {"num": "3", "title": "EYE EXERCISES", "icon": MSO_SHAPE.OVAL},
        {"num": "4", "title": "CREATE A WORKSPACE", "icon": MSO_SHAPE.RECTANGLE},
        {"num": "5", "title": "AVOID DISTRACTIONS", "icon": MSO_SHAPE.MATH_MULTIPLY},
    ]

    # --- LAYOUT CALCULATIONS ---
    header_height = Inches(5.5)
    footer_height = Inches(3.0)
    available_section_height = prs.slide_height - header_height - footer_height
    section_height = available_section_height / len(sections)

    # === LAYER 1: Header Background ===
    header_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, header_height
    )
    header_bg.fill.solid()
    header_bg.fill.fore_color.rgb = c_header_bg
    header_bg.line.fill.background() # No border

    # === LAYER 2: Header Content (Thick framed title box) ===
    # Frame Box
    frame_width = Inches(10)
    frame_height = Inches(3)
    frame_left = (prs.slide_width - frame_width) / 2
    frame_top = Inches(0.8)
    
    title_frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, frame_left, frame_top, frame_width, frame_height
    )
    title_frame.fill.solid()
    title_frame.fill.fore_color.rgb = RGBColor(245, 245, 245)
    title_frame.line.color.rgb = c_header_bg
    title_frame.line.width = Pt(8)

    tf = title_frame.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Arial Black'
    p.font.size = Pt(64)
    p.font.color.rgb = c_header_bg

    # Header Subtext / Intro paragraph
    intro_box = slide.shapes.add_textbox(
        Inches(1.5), frame_top + frame_height + Inches(0.2), 
        Inches(10.333), Inches(1.5)
    )
    intro_tf = intro_box.text_frame
    intro_tf.word_wrap = True
    intro_p = intro_tf.paragraphs[0]
    intro_p.text = body_text
    intro_p.alignment = PP_ALIGN.CENTER
    intro_p.font.name = 'Arial'
    intro_p.font.size = Pt(22)
    intro_p.font.color.rgb = c_text_light

    # === LAYER 3: Dynamic Infographic Sections ===
    current_top = header_height

    for i, section in enumerate(sections):
        bg_color = band_colors[i % len(band_colors)]
        
        # 1. Band Background
        band = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, current_top, prs.slide_width, section_height
        )
        band.fill.solid()
        band.fill.fore_color.rgb = bg_color
        band.line.fill.background()

        # 2. Section Number (Large watermark style or bold text)
        num_box = slide.shapes.add_textbox(
            Inches(1.5), current_top + Inches(0.5), Inches(2), Inches(1)
        )
        num_p = num_box.text_frame.paragraphs[0]
        num_p.text = section["num"]
        num_p.font.name = 'Arial Black'
        num_p.font.size = Pt(60)
        num_p.font.color.rgb = c_text_dark

        # 3. Section Title
        title_box = slide.shapes.add_textbox(
            Inches(2.5), current_top + Inches(0.6), Inches(8), Inches(1)
        )
        title_p = title_box.text_frame.paragraphs[0]
        title_p.text = section["title"]
        title_p.font.name = 'Arial Black'
        title_p.font.size = Pt(44)
        title_p.font.color.rgb = c_text_dark
        
        # 4. Icon Placeholder (Using basic shape as placeholder for visual weight)
        icon_size = Inches(1.2)
        icon = slide.shapes.add_shape(
            section["icon"], 
            (prs.slide_width - icon_size) / 2, # Centered horizontally
            current_top + Inches(1.8),         # Placed below text
            icon_size, icon_size
        )
        icon.fill.solid()
        icon.fill.fore_color.rgb = c_header_bg
        icon.line.fill.background()

        current_top += section_height

    # === LAYER 4: Footer ===
    footer_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, current_top, prs.slide_width, footer_height
    )
    footer_bg.fill.solid()
    footer_bg.fill.fore_color.rgb = c_header_bg
    footer_bg.line.fill.background()
    
    footer_box = slide.shapes.add_textbox(
        Inches(1.5), current_top + Inches(1), Inches(10.333), Inches(1)
    )
    footer_p = footer_box.text_frame.paragraphs[0]
    footer_p.text = "Save this presentation as a PDF to distribute as a scrolling infographic."
    footer_p.alignment = PP_ALIGN.CENTER
    footer_p.font.name = 'Arial'
    footer_p.font.size = Pt(24)
    footer_p.font.color.rgb = c_text_light

    prs.save(output_pptx_path)
    return output_pptx_path
