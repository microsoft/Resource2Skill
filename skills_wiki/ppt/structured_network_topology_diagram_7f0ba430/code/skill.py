def create_network_diagram_slide(
    output_pptx_path: str,
    title_text: str = "Interpreting a Network Diagram",
    devices: list = None,
    connections: list = None,
) -> str:
    """
    Creates a PPTX slide with a structured network topology diagram.

    The function uses pre-defined data from the tutorial if `devices` and 
    `connections` are not provided, allowing it to run as a standalone example.

    Returns: Path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.dml.color import RGBColor
    from pptx.enum.dml import MSO_LINE

    # --- Default Data from the Tutorial ---
    if devices is None:
        devices = [
            # ID, Type, (Left, Top), (Width, Height), Shape Type
            ('PC1', 'PC', (0.5, 1.5), (0.8, 0.6), MSO_SHAPE.RECTANGLE),
            ('R_Access', 'Router', (4.5, 1.5), (0.8, 0.8), MSO_SHAPE.OVAL),
            ('R_Internet', 'Router', (8.5, 2.5), (0.8, 0.8), MSO_SHAPE.OVAL),
            ('R_Branch', 'Router', (10.5, 4.5), (0.8, 0.8), MSO_SHAPE.OVAL),
            ('Firewall', 'Firewall', (10.5, 1.5), (0.25, 1.0), MSO_SHAPE.RECTANGLE),
            ('Switch', 'Switch', (4.5, 4.5), (1.2, 0.6), MSO_SHAPE.RECTANGLE),
            ('AP', 'AP', (0.5, 4.5), (0.8, 0.6), MSO_SHAPE.RECTANGLE),
            ('Laptop', 'Laptop', (0.5, 6.0), (0.8, 0.6), MSO_SHAPE.RECTANGLE),
            ('IP_Phone', 'IP Phone', (2.0, 6.0), (0.8, 0.6), MSO_SHAPE.RECTANGLE),
            ('PC2', 'PC', (3.5, 6.0), (0.8, 0.6), MSO_SHAPE.RECTANGLE),
            ('Server', 'Server', (5.0, 6.0), (0.5, 0.8), MSO_SHAPE.RECTANGLE),
            ('WLAN_Ctrl', 'WLAN Controller', (6.5, 6.0), (1.0, 0.5), MSO_SHAPE.RECTANGLE),
        ]

    if connections is None:
        connections = [
            # From_ID, To_ID, Type, Label
            ('PC1', 'R_Access', 'Ethernet', ''),
            ('R_Access', 'Switch', 'Ethernet', '192.168.1.0/24'),
            ('R_Access', 'R_Internet', 'Ethernet', ''),
            ('R_Internet', 'Firewall', 'Ethernet', 'Gi0/1'),
            ('R_Internet', 'R_Branch', 'Serial', 'S0/0'),
            ('Switch', 'AP', 'Ethernet', 'Fa0/5'),
            ('Switch', 'IP_Phone', 'Ethernet', 'Fa0/6'),
            ('Switch', 'PC2', 'Ethernet', 'Fa0/7'),
            ('Switch', 'Server', 'Ethernet', 'Gi0/11'),
            ('Switch', 'WLAN_Ctrl', 'Ethernet', 'Gi0/12'),
            ('AP', 'Laptop', 'Wireless', ''),
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Color Palette ---
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_RED = RGBColor(255, 0, 0)
    COLOR_BLUE = RGBColor(0, 176, 240)
    COLOR_GREEN_BORDER = RGBColor(146, 208, 80)
    COLOR_SHAPE_FILL = RGBColor(242, 242, 242)
    COLOR_SHAPE_BORDER = RGBColor(89, 89, 89)

    # --- Slide Title ---
    title_shape = slide.shapes.add_textbox(Inches(0), Inches(0.1), prs.slide_width, Inches(0.5))
    title_shape.text_frame.text = title_text
    p = title_shape.text_frame.paragraphs[0]
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.name = 'Calibri'
    p.alignment = 1  # Center alignment

    # --- Main Diagram Container ---
    container = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.2), Inches(0.8), Inches(12.933), Inches(4.5))
    container.fill.background()
    container.line.color.rgb = COLOR_GREEN_BORDER
    container.line.width = Pt(3)

    # --- Draw Devices ---
    device_shapes = {}
    for dev_id, dev_type, pos, size, shape_type in devices:
        shape = slide.shapes.add_shape(shape_type, Inches(pos[0]), Inches(pos[1]), Inches(size[0]), Inches(size[1]))
        shape.text = dev_type
        shape.text_frame.paragraphs[0].font.size = Pt(10)
        shape.text_frame.paragraphs[0].font.name = 'Calibri'
        shape.text_frame.paragraphs[0].alignment = 1 # Center
        
        # Style shape
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_SHAPE_FILL
        shape.line.color.rgb = COLOR_SHAPE_BORDER
        shape.line.width = Pt(1)
        
        device_shapes[dev_id] = shape

    # --- Draw Connections ---
    for conn in connections:
        from_shape = device_shapes[conn['from']]
        to_shape = device_shapes[conn['to']]
        
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, from_shape.left, from_shape.top, to_shape.left, to_shape.top)
        
        # Reposition connector ends to shape centers
        connector.begin_x = from_shape.left + from_shape.width // 2
        connector.begin_y = from_shape.top + from_shape.height // 2
        connector.end_x = to_shape.left + to_shape.width // 2
        connector.end_y = to_shape.top + to_shape.height // 2

        line = connector.line
        line.width = Pt(1.5)
        
        if conn['type'] == 'Ethernet':
            line.color.rgb = COLOR_RED
        elif conn['type'] == 'Serial':
            line.color.rgb = COLOR_RED
            line.dash_style = MSO_LINE.DASH
        elif conn['type'] == 'Wireless':
            line.color.rgb = COLOR_BLUE
            line.dash_style = MSO_LINE.LONG_DASH
        
        if conn['label']:
            label_x = (connector.begin_x + connector.end_x) / 2
            label_y = (connector.begin_y + connector.end_y) / 2
            label_box = slide.shapes.add_textbox(label_x - Inches(0.4), label_y - Inches(0.1), Inches(0.8), Inches(0.2))
            label_box.text_frame.text = conn['label']
            p = label_box.text_frame.paragraphs[0]
            p.font.size = Pt(8)
            p.font.name = 'Calibri'
            p.alignment = 1 # Center
            label_box.fill.background()
            label_box.line.fill.background()

    # --- Draw Legend ---
    legend_items = [
        ('Switch', 'rect', None), ('AP', 'rect', None), ('PC', 'rect', None), ('Ethernet Link', 'line', 'solid_red'),
        ('Router', 'oval', None), ('Server', 'rect_tall', None), ('Laptop', 'rect', None), ('Serial Link', 'line', 'dash_red'),
        ('IP Phone', 'rect', None), ('Wireless LAN Controller', 'rect_wide', None), ('Wireless Link', 'line', 'dash_blue'), ('Firewall', 'rect_thin', None)
    ]
    
    start_x, start_y, x_gap, y_gap = 1.0, 5.5, 3.0, 0.5
    for i, (label, shape_style, line_style) in enumerate(legend_items):
        col = i % 4
        row = i // 4
        x = start_x + col * x_gap
        y = start_y + row * y_gap
        
        # Draw icon/line
        if shape_style == 'rect':
            icon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.4), Inches(0.2))
        elif shape_style == 'rect_tall':
            icon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.2), Inches(0.3))
        elif shape_style == 'rect_wide':
            icon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.5), Inches(0.15))
        elif shape_style == 'rect_thin':
            icon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.1), Inches(0.3))
        elif shape_style == 'oval':
            icon = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.3), Inches(0.3))
        elif shape_style == 'line':
            icon = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y+0.1), Inches(x+0.4), Inches(y+0.1))
            icon.line.width = Pt(1.5)
            if line_style == 'solid_red': icon.line.color.rgb = COLOR_RED
            if line_style == 'dash_red': icon.line.color.rgb = COLOR_RED; icon.line.dash_style = MSO_LINE.DASH
            if line_style == 'dash_blue': icon.line.color.rgb = COLOR_BLUE; icon.line.dash_style = MSO_LINE.LONG_DASH
            
        if shape_style and shape_style != 'line':
            icon.fill.solid(); icon.fill.fore_color.rgb = COLOR_SHAPE_FILL
            icon.line.color.rgb = COLOR_SHAPE_BORDER; icon.line.width = Pt(1)

        # Add text
        text_box = slide.shapes.add_textbox(Inches(x + 0.5), Inches(y - 0.1), Inches(2.0), Inches(0.4))
        text_box.text_frame.text = label
        p = text_box.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.name = 'Calibri'
        p.font.color.rgb = COLOR_BLACK

    prs.save(output_pptx_path)
    return output_pptx_path
