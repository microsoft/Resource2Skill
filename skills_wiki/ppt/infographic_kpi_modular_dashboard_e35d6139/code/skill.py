def create_slide(
    output_pptx_path: str,
    title_text: str = "Main Product Sales Overview",
    bg_palette: str = "city,architecture,night",  
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Infographic KPI Dashboard' visual effect,
    featuring a tinted photographic header, ribbons, and colored data modules.
    """
    import os
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Color Palette ---
    theme_colors = [
        RGBColor(0, 150, 136),   # Teal
        RGBColor(244, 164, 96),  # Orange
        RGBColor(128, 0, 128),   # Purple
        RGBColor(154, 205, 50)   # Green
    ]
    banner_color = RGBColor(0, 174, 239) # Bright Cyan
    dark_text = RGBColor(60, 60, 60)
    grey_text = RGBColor(120, 120, 120)

    # --- Header Section (30% of slide height) ---
    header_height = Inches(2.25)
    
    # 1. Download Background Image
    bg_image_stream = io.BytesIO()
    try:
        url = f"https://source.unsplash.com/random/1920x400/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            bg_image_stream.write(response.read())
        bg_image_stream.seek(0)
        slide.shapes.add_picture(bg_image_stream, Inches(0), Inches(0), width=prs.slide_width, height=header_height)
    except Exception as e:
        # Fallback if download fails: Solid dark shape
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, header_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(34, 45, 50)
        bg.line.fill.background()

    # 2. PIL Tint Overlay (Dark Blue/Grey Translucent)
    tint_path = "temp_tint.png"
    img = Image.new('RGBA', (100, 100), (20, 30, 40, 180)) # Dark slate with alpha
    img.save(tint_path)
    slide.shapes.add_picture(tint_path, Inches(0), Inches(0), width=prs.slide_width, height=header_height)
    if os.path.exists(tint_path): os.remove(tint_path)

    # 3. Cyan Banner / Ribbon
    banner = slide.shapes.add_shape(
        MSO_SHAPE.CHEVRON, 
        Inches(1.5), Inches(0.8), Inches(10.333), Inches(0.8)
    )
    banner.fill.solid()
    banner.fill.fore_color.rgb = banner_color
    banner.line.fill.background()
    
    # Title Text on Banner
    tf = banner.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    # --- KPI Modules Section ---
    data_points = ["55%", "70%", "40%", "60%"]
    labels = ["Product A", "Product B", "Product C", "Product D"]
    icons = ["📦", "📈", "💡", "🎯"] # Unicode for robust icon generation
    
    num_items = len(data_points)
    module_width = prs.slide_width / num_items
    center_offset = module_width / 2
    base_y = Inches(3.2) # Starting Y for content

    for i in range(num_items):
        center_x = (i * module_width) + center_offset
        color = theme_colors[i]

        # 1. Colored Circle Background
        circle_size = Inches(1.2)
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            center_x - (circle_size/2), base_y, 
            circle_size, circle_size
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = color
        circle.line.fill.background()

        # 2. Icon (Using TextFrame inside circle for alignment)
        tf_icon = circle.text_frame
        tf_icon.text = icons[i]
        p_icon = tf_icon.paragraphs[0]
        p_icon.font.size = Pt(40)
        p_icon.font.name = "Segoe UI Emoji" # Good cross-platform emoji font
        p_icon.alignment = PP_ALIGN.CENTER

        # 3. Connecting Line (like in the video)
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            center_x - Inches(0.02), base_y + circle_size + Inches(0.1),
            Inches(0.04), Inches(0.3)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = color
        line.line.fill.background()

        # 4. Large Data Number
        num_box = slide.shapes.add_textbox(
            center_x - Inches(1), base_y + circle_size + Inches(0.4),
            Inches(2), Inches(0.8)
        )
        tf_num = num_box.text_frame
        tf_num.text = data_points[i]
        p_num = tf_num.paragraphs[0]
        p_num.font.size = Pt(54)
        p_num.font.bold = True
        p_num.font.color.rgb = color
        p_num.alignment = PP_ALIGN.CENTER

        # 5. Label / Description Text
        desc_box = slide.shapes.add_textbox(
            center_x - Inches(1.25), base_y + circle_size + Inches(1.3),
            Inches(2.5), Inches(0.6)
        )
        tf_desc = desc_box.text_frame
        tf_desc.word_wrap = True
        
        # Primary Label
        p_lbl = tf_desc.paragraphs[0]
        p_lbl.text = labels[i]
        p_lbl.font.size = Pt(16)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = dark_text
        p_lbl.alignment = PP_ALIGN.CENTER
        
        # Sub-description
        p_sub = tf_desc.add_paragraph()
        p_sub.text = "Your sample text here."
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = grey_text
        p_sub.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
