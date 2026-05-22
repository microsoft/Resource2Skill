def create_slide(
    output_pptx_path: str,
    title_text: str = "Comparison Of 2 Ideas",
    idea1_title: str = "Idea 1\nTitle\nHere",
    idea2_title: str = "Idea 2\nTitle\nHere",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Split-Screen Radial Comparison layout.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # ==========================================================
    # LAYER 1: Generate Perfect Semicircles via PIL
    # We use 2x supersampling for perfectly smooth antialiased edges
    # ==========================================================
    scale = 2
    W, H = 1280 * scale, 720 * scale
    cx, cy = 640 * scale, 390 * scale  # Y center slightly shifted down
    
    r_inner = int(1.8 * 96 * scale)
    r_outer = int(2.4 * 96 * scale)
    arc_width = int(0.25 * 96 * scale)

    img = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Bounding boxes
    bbox_inner = [cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner]
    bbox_outer = [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer]

    # PIL Angles: 0 is Right, 90 is Down, 180 is Left, 270 is Up.
    # Left Side Semicircles (from 90 bottom to 270 top)
    draw.pieslice(bbox_inner, 90, 270, fill=(138, 180, 218, 255))
    draw.arc(bbox_outer, 90, 270, fill=(200, 220, 240, 255), width=arc_width)

    # Right Side Semicircles (from -90 top to 90 bottom)
    draw.pieslice(bbox_inner, -90, 90, fill=(120, 120, 120, 255))
    draw.arc(bbox_outer, -90, 90, fill=(220, 220, 220, 255), width=arc_width)

    # Downscale for smoothness and save
    img = img.resize((1280, 720), Image.Resampling.LANCZOS)
    temp_bg_path = "temp_radial_bg.png"
    img.save(temp_bg_path)

    # Insert background
    slide.shapes.add_picture(temp_bg_path, 0, 0, width=Inches(13.333), height=Inches(7.5))
    os.remove(temp_bg_path)

    # ==========================================================
    # LAYER 2: PPTX Native Elements (Dashed Line & Main Title)
    # ==========================================================
    
    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(2), Inches(0.4), Inches(9.333), Inches(1))
    tf = title_box.text_frame
    tf.text = title_text
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(36)
    tf.paragraphs[0].font.name = "Calibri Light"

    # Central Dashed Line
    line = slide.shapes.add_connector(
        MSO_SHAPE.LINE, Inches(6.666), Inches(1.5), Inches(6.666), Inches(6.8)
    )
    line.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    line.line.width = Pt(2.5)
    line.line.color.rgb = RGBColor(50, 50, 50)

    # ==========================================================
    # LAYER 3: Interactive Nodes and Text Boxes
    # ==========================================================
    
    center_x = 6.666
    center_y = 3.9
    radius = 2.4 # matches outer arc placement
    node_r = 0.25 # radius of the circular indicator

    # Layout Math Coordinates (dx, dy from center)
    # Cos/Sin for 45 deg = 0.707
    diag = radius * 0.707
    
    nodes_config = [
        # Left Side (Top, Middle, Bottom)
        {"x": center_x - diag, "y": center_y - diag, "num": "1", "color": (237, 125, 49), "side": "left"},
        {"x": center_x - radius, "y": center_y, "num": "2", "color": (112, 173, 71), "side": "left"},
        {"x": center_x - diag, "y": center_y + diag, "num": "3", "color": (255, 192, 0), "side": "left"},
        
        # Right Side (Top, Middle, Bottom)
        {"x": center_x + diag, "y": center_y - diag, "num": "1", "color": (192, 0, 0), "side": "right"},
        {"x": center_x + radius, "y": center_y, "num": "2", "color": (112, 48, 160), "side": "right"},
        {"x": center_x + diag, "y": center_y + diag, "num": "3", "color": (198, 89, 17), "side": "right"},
    ]

    for node in nodes_config:
        # Create Circle Node
        shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(node["x"] - node_r), Inches(node["y"] - node_r), 
            Inches(node_r * 2), Inches(node_r * 2)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*node["color"])
        shape.line.color.rgb = RGBColor(255, 255, 255)
        shape.line.width = Pt(2)
        
        # Node Text
        tf = shape.text_frame
        tf.text = node["num"]
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(16)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Create Corresponding Text Box
        tb_width = 2.5
        tb_height = 1.0
        if node["side"] == "left":
            tb_x = node["x"] - node_r - tb_width - 0.2
            align = PP_ALIGN.RIGHT
        else:
            tb_x = node["x"] + node_r + 0.2
            align = PP_ALIGN.LEFT
            
        tb_y = node["y"] - 0.5
        
        tbox = slide.shapes.add_textbox(Inches(tb_x), Inches(tb_y), Inches(tb_width), Inches(tb_height))
        
        p1 = tbox.text_frame.paragraphs[0]
        p1.text = "TITLE HERE"
        p1.font.bold = True
        p1.font.size = Pt(14)
        p1.alignment = align
        
        p2 = tbox.text_frame.add_paragraph()
        p2.text = "Add details in 2-3 lines to describe the title. Lesser the content better it will look like."
        p2.font.size = Pt(10)
        p2.font.color.rgb = RGBColor(100, 100, 100)
        p2.alignment = align

    # ==========================================================
    # LAYER 4: Inner Semicircle Titles
    # ==========================================================
    
    def add_inner_title(x_offset, text, text_color):
        tb = slide.shapes.add_textbox(Inches(center_x + x_offset - 1.0), Inches(center_y - 0.75), Inches(2.0), Inches(1.5))
        tf = tb.text_frame
        tf.text = text
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(20)
            p.font.color.rgb = text_color
            p.font.name = "Calibri Light"
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_inner_title(-1.0, idea1_title, RGBColor(255, 255, 255))
    add_inner_title(1.0, idea2_title, RGBColor(255, 255, 255))

    prs.save(output_pptx_path)
    return output_pptx_path
