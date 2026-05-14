def create_slide(
    output_pptx_path: str,
    title_text: str = "Layered Architecture Framework",
    body_text: str = "",
    bg_palette: str = "light",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 3D Isometric Stacked Layers visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    import math

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Background Setup ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(248, 249, 250)
    bg.line.color.rgb = RGBColor(248, 249, 250)

    # === Header Title ===
    title_tb = slide.shapes.add_textbox(Pt(40), Pt(30), Pt(600), Pt(50))
    title_p = title_tb.text_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.size = Pt(28)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(40, 40, 40)

    # === Data & Colors ===
    layers_data = kwargs.get("layers", [
        {"title": "PHASE 01", "desc": "Initial planning and requirements gathering.", "color": (230, 57, 70)},   # Red
        {"title": "PHASE 02", "desc": "System architecture and design modeling.", "color": (244, 162, 97)},      # Orange
        {"title": "PHASE 03", "desc": "Core development and module integration.", "color": (233, 196, 106)},     # Yellow
        {"title": "PHASE 04", "desc": "Quality assurance and comprehensive testing.", "color": (42, 157, 143)},  # Green
        {"title": "PHASE 05", "desc": "Final deployment and continuous monitoring.", "color": (0, 150, 199)},    # Blue
    ])

    # === Isometric Grid Math ===
    cx = 480          # Center X coordinate
    y_start = 120     # Starting Y coordinate for the top-most block
    dx = 130          # Isometric half-width
    dy = 65           # Isometric half-height
    t = 35            # Block thickness
    gap = 15          # Vertical gap between floating blocks

    # Helper function to draw a custom polygon
    def draw_polygon(vertices, rgb_color):
        builder = slide.shapes.build_freeform(Pt(vertices[0][0]), Pt(vertices[0][1]))
        for v in vertices[1:]:
            builder.add_line_segments([(Pt(v[0]), Pt(v[1]))])
        builder.add_line_segments([(Pt(vertices[0][0]), Pt(vertices[0][1]))])
        shape = builder.convert_to_shape()
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*rgb_color)
        shape.line.color.rgb = RGBColor(*rgb_color) # Hide border seam
        return shape

    # === Shadow Generation ===
    # Render shadow below the bottom-most block footprint
    bottom_i = len(layers_data) - 1
    cy_bot = y_start + bottom_i * (t + gap)
    P_back_s = (cx, cy_bot + t)
    P7_s = (cx + dx, cy_bot + dy + t)
    P5_s = (cx, cy_bot + 2 * dy + t)
    P6_s = (cx - dx, cy_bot + dy + t)
    
    # Offset shadow slightly down and right
    sx, sy = 0, 25 
    shadow_vertices = [
        (P_back_s[0] + sx, P_back_s[1] + sy),
        (P7_s[0] + sx, P7_s[1] + sy),
        (P5_s[0] + sx, P5_s[1] + sy),
        (P6_s[0] + sx, P6_s[1] + sy)
    ]
    draw_polygon(shadow_vertices, (225, 225, 230))

    # === Render 3D Blocks ===
    # Must draw from bottom (N-1) to top (0) so higher blocks overlap lower ones visually
    for i in range(len(layers_data)-1, -1, -1):
        layer = layers_data[i]
        base_color = layer["color"]
        
        # Calculate lighting shades
        top_c = base_color
        left_c = (int(base_color[0]*0.85), int(base_color[1]*0.85), int(base_color[2]*0.85))
        right_c = (int(base_color[0]*0.7), int(base_color[1]*0.7), int(base_color[2]*0.7))
        
        cy = y_start + i * (t + gap)
        
        # Define 7 key vertices for the block
        P1 = (cx, cy)                           # Top Corner
        P2 = (cx + dx, cy + dy)                 # Right Corner
        P3 = (cx, cy + 2 * dy)                  # Front Center Corner
        P4 = (cx - dx, cy + dy)                 # Left Corner
        P5 = (cx, cy + 2 * dy + t)              # Bottom Center Corner
        P6 = (cx - dx, cy + dy + t)             # Bottom Left Corner
        P7 = (cx + dx, cy + dy + t)             # Bottom Right Corner
        
        # Draw Faces
        draw_polygon([P4, P3, P5, P6], left_c)  # Left Face
        draw_polygon([P3, P2, P7, P5], right_c) # Right Face
        draw_polygon([P1, P2, P3, P4], top_c)   # Top Face
        
        # --- Add Isometric Label to Left Face ---
        tb_width, tb_height = 60, 30
        x_center = cx - dx / 2
        y_center = cy + dy + t / 2
        
        tb_label = slide.shapes.add_textbox(Pt(x_center - tb_width / 2), Pt(y_center - tb_height / 2), Pt(tb_width), Pt(tb_height))
        # Rotate textbox to match the angle of the left edge (atan2(dy, dx))
        tb_label.rotation = math.degrees(math.atan2(dy, dx)) 
        
        # Remove margins so text centers perfectly
        tb_label.text_frame.margin_left = 0
        tb_label.text_frame.margin_right = 0
        tb_label.text_frame.margin_top = 0
        tb_label.text_frame.margin_bottom = 0
        tb_label.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        p = tb_label.text_frame.paragraphs[0]
        p.text = f"{i+1:02d}"
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        
        # --- Add Side Descriptions & Connectors ---
        if i % 2 == 0: # Right side placement
            start_x, start_y = cx + dx, cy + dy + t/2
            end_x, end_y = start_x + 50, start_y
            
            conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(start_x), Pt(start_y), Pt(end_x), Pt(end_y))
            conn.line.color.rgb = RGBColor(*right_c)
            conn.line.width = Pt(1.5)
            
            desc_tb = slide.shapes.add_textbox(Pt(end_x + 10), Pt(end_y - 20), Pt(200), Pt(60))
            p1 = desc_tb.text_frame.paragraphs[0]
            p1.text = layer["title"]
            p1.font.bold = True
            p1.font.size = Pt(14)
            p1.font.color.rgb = RGBColor(*top_c)
            
            p2 = desc_tb.text_frame.add_paragraph()
            p2.text = layer["desc"]
            p2.font.size = Pt(10)
            p2.font.color.rgb = RGBColor(100, 100, 100)
            
        else: # Left side placement
            start_x, start_y = cx - dx, cy + dy + t/2
            end_x, end_y = start_x - 50, start_y
            
            conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(start_x), Pt(start_y), Pt(end_x), Pt(end_y))
            conn.line.color.rgb = RGBColor(*left_c)
            conn.line.width = Pt(1.5)
            
            desc_tb = slide.shapes.add_textbox(Pt(end_x - 210), Pt(end_y - 20), Pt(200), Pt(60))
            p1 = desc_tb.text_frame.paragraphs[0]
            p1.text = layer["title"]
            p1.font.bold = True
            p1.font.size = Pt(14)
            p1.font.color.rgb = RGBColor(*top_c)
            p1.alignment = PP_ALIGN.RIGHT
            
            p2 = desc_tb.text_frame.add_paragraph()
            p2.text = layer["desc"]
            p2.font.size = Pt(10)
            p2.font.color.rgb = RGBColor(100, 100, 100)
            p2.alignment = PP_ALIGN.RIGHT

    prs.save(output_pptx_path)
    return output_pptx_path
