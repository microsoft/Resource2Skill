import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "DATA FLOW DIAGRAM",
    nodes: list = None,
    connections: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dark Mode Arc Diagram effect.
    """
    if nodes is None:
        nodes = ["Data 1", "Data 2", "Data 3", "Data 4", "Data 5", "Data 6", "Data 7"]
        
    if connections is None:
        # Tuple format: (Start_Index, End_Index, Label, Is_Top_Arc)
        connections = [
            (0, 2, "10%", True),
            (1, 5, "20%", True),
            (2, 4, "25%", True),
            (3, 5, "18%", True),
            (0, 3, "75%", False),
            (2, 5, "60%", False),
            (4, 6, "40%", False)
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 0, 0) # Pitch black

    # === Layer 2: Main Title ===
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # === Layout Calculation ===
    num_nodes = len(nodes)
    node_spacing = Inches(1.6)
    total_width = (num_nodes - 1) * node_spacing
    start_x = (Inches(13.333) - total_width) / 2.0
    axis_y = Inches(4.5)  # Positioned slightly below center for top arc room

    # Calculate coordinates for each node
    node_coords = []
    for i in range(num_nodes):
        nx = start_x + i * node_spacing
        node_coords.append((nx, axis_y))

    # === Layer 3: Central Axis Line ===
    axis_line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, 
        int(node_coords[0][0]), int(axis_y), 
        int(node_coords[-1][0]), int(axis_y)
    )
    axis_line.line.color.rgb = RGBColor(150, 150, 150)
    axis_line.line.width = Pt(1.5)

    # === Layer 4: Arcs and Weights ===
    for start_idx, end_idx, weight_text, is_top in connections:
        x1, y1 = node_coords[start_idx]
        x2, y2 = node_coords[end_idx]
        
        distance = abs(x2 - x1)
        # Height scales with distance, but tapers off for very long connections
        height = distance * 0.4 
        # Capping height to avoid running off slide
        max_height = Inches(3.0) if is_top else Inches(1.5)
        height = min(height, max_height)
        
        direction = -1 if is_top else 1 # -1 moves UP (y decreases), 1 moves DOWN

        # Generate points for a smooth sine wave arc
        points = []
        num_steps = 40  # Resolution of the curve
        for i in range(num_steps + 1):
            t = i / num_steps
            px = x1 + t * (x2 - x1)
            py = y1 + direction * height * math.sin(t * math.pi)
            points.append((int(px), int(py)))

        # Draw the Freeform curve
        ff_builder = slide.shapes.build_freeform(points[0][0], points[0][1])
        for p in points[1:]:
            ff_builder.add_line_segments([p])
        
        arc_shape = ff_builder.convert_to_shape()
        arc_shape.line.color.rgb = RGBColor(180, 180, 180)
        arc_shape.line.width = Pt(1.2)

        # Place Percentage Label at the apex of the curve
        peak_x = x1 + 0.5 * (x2 - x1)
        peak_y = y1 + direction * height * math.sin(0.5 * math.pi)
        
        lbl_width = Inches(1.0)
        lbl_height = Inches(0.4)
        
        # Adjust Y offset so text sits neatly above or below the line
        y_offset = Inches(0.2)
        lbl_y = peak_y - lbl_height if is_top else peak_y
        
        weight_box = slide.shapes.add_textbox(
            int(peak_x - lbl_width/2), 
            int(lbl_y), 
            int(lbl_width), int(lbl_height)
        )
        tf_w = weight_box.text_frame
        p_w = tf_w.paragraphs[0]
        p_w.text = weight_text
        p_w.alignment = PP_ALIGN.CENTER
        p_w.font.name = "Arial"
        p_w.font.size = Pt(12)
        p_w.font.color.rgb = RGBColor(220, 220, 220)
        
        # Optional: Add a small decorative "data dot" randomly on the first top arc to mimic the video
        if is_top and start_idx == 0:
            dot_t = 0.35  # 35% along the path
            dot_x = x1 + dot_t * (x2 - x1)
            dot_y = y1 + direction * height * math.sin(dot_t * math.pi)
            dot_radius = Inches(0.06)
            data_dot = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, 
                int(dot_x - dot_radius), int(dot_y - dot_radius), 
                int(dot_radius*2), int(dot_radius*2)
            )
            data_dot.fill.solid()
            data_dot.fill.fore_color.rgb = RGBColor(255, 255, 255)
            data_dot.line.fill.background()

    # === Layer 5: Nodes and Node Labels ===
    node_radius = Inches(0.08)
    
    for i, name in enumerate(nodes):
        nx, ny = node_coords[i]
        
        # Add Node Circle
        node_shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            int(nx - node_radius), int(ny - node_radius), 
            int(node_radius * 2), int(node_radius * 2)
        )
        node_shape.fill.solid()
        node_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        node_shape.line.fill.background() # No border

        # Add Node Label Text
        lbl_width = Inches(1.2)
        lbl_height = Inches(0.5)
        label_box = slide.shapes.add_textbox(
            int(nx - lbl_width / 2), 
            int(ny + Inches(0.1)), 
            int(lbl_width), int(lbl_height)
        )
        tf_l = label_box.text_frame
        p_l = tf_l.paragraphs[0]
        p_l.text = name
        p_l.alignment = PP_ALIGN.CENTER
        p_l.font.name = "Arial"
        p_l.font.size = Pt(14)
        p_l.font.bold = True
        p_l.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
