def create_slide(
    output_pptx_path: str,
    title_text: str = "Network Topology & Status",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with an icon-based network topology diagram and a 
    color-coded status monitoring table.

    The network device icons are generated programmatically using PIL to ensure the
    function is self-contained.

    Returns:
        str: The path to the saved PPTX file.
    """
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_CONNECTOR
    from PIL import Image, ImageDraw, ImageFont

    # --- Data for the diagram ---
    # In a real application, this would be an input parameter.
    devices = {
        "Router": {"type": "router", "ip": "10.11.32.1", "pos": (1, 1.5), "status": "Up"},
        "Switch1": {"type": "switch", "ip": "10.11.32.2", "pos": (3.5, 2.5), "status": "Up"},
        "Server01": {"type": "server", "ip": "10.11.32.187", "pos": (1, 4), "status": "Up"},
        "PC01": {"type": "pc", "ip": "10.11.32.87", "pos": (3.5, 5), "status": "Up"},
        "Camera01": {"type": "camera", "ip": "10.11.32.17", "pos": (6, 4), "status": "Down"},
        "AP01": {"type": "ap", "ip": "10.11.32.57", "pos": (6, 1), "status": "Up"},
        "Mary-PC": {"type": "pc", "ip": "10.11.32.14", "pos": (8.5, 2.5), "status": "Down"},
    }
    connections = [
        ("Router", "Switch1"),
        ("Server01", "Switch1"),
        ("PC01", "Switch1"),
        ("Camera01", "Switch1"),
        ("AP01", "Switch1"),
        ("Mary-PC", "AP01"),
    ]
    status_colors = {
        "Up": RGBColor(0, 176, 80),
        "Down": RGBColor(255, 0, 0),
    }
    icon_size = (int(Inches(0.8).emu // 9525), int(Inches(0.6).emu // 9525))
    font_path = "arial.ttf"  # Assumes Arial is available
    try:
        font = ImageFont.truetype(font_path, 18)
        label_font = ImageFont.truetype(font_path, 15)
    except IOError:
        font = ImageFont.load_default()
        label_font = ImageFont.load_default()


    # --- Icon generation functions using PIL ---
    def create_icon_bytes(device_type):
        im = Image.new("RGBA", icon_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)
        w, h = icon_size
        if device_type == "router":
            draw.ellipse([(w*0.1, h*0.2), (w*0.9, h*0.8)], fill=(0, 112, 192), outline="black")
            draw.line([(w*0.3, h*0.3), (w*0.5, h*0.1)], fill="green", width=2)
            draw.line([(w*0.5, h*0.1), (w*0.7, h*0.3)], fill="green", width=2)
            draw.line([(w*0.3, h*0.7), (w*0.5, h*0.9)], fill="green", width=2)
            draw.line([(w*0.5, h*0.9), (w*0.7, h*0.7)], fill="green", width=2)
        elif device_type == "switch":
            draw.rectangle([(w*0.05, h*0.25), (w*0.95, h*0.75)], fill=(0, 112, 192), outline="black")
            draw.line([(w*0.2, h*0.4), (w*0.8, h*0.4)], fill="green", width=2)
            draw.line([(w*0.7, h*0.3), (w*0.8, h*0.4), (w*0.7, h*0.5)], fill="green", width=2)
            draw.line([(w*0.3, h*0.5), (w*0.2, h*0.6), (w*0.3, h*0.7)], fill="green", width=2)
        elif device_type == "server":
            draw.rectangle([(w*0.2, h*0.05), (w*0.8, h*0.95)], fill=(128, 128, 128), outline="black")
            draw.point((w*0.4, h*0.2), fill="green")
        elif device_type == "pc":
            draw.rectangle([(w*0.1, h*0.1), (w*0.9, h*0.7)], fill=(128, 128, 128), outline="black")
            draw.rectangle([(w*0.3, h*0.7), (w*0.7, h*0.9)], fill=(100, 100, 100), outline="black")
        elif device_type == "camera":
            draw.rectangle([(w*0.2, h*0.3), (w*0.8, h*0.7)], fill=(100, 100, 100))
            draw.ellipse([(w*0.4, h*0.1), (w*0.6, h*0.3)], fill=(128, 128, 128))
        elif device_type == "ap":
            draw.rectangle([(w*0.1, h*0.4), (w*0.9, h*0.8)], fill=(0, 112, 192), outline="black")
            draw.line([(w*0.3, h*0.3), (w*0.3, h*0.4)], fill="black")
            draw.line([(w*0.7, h*0.3), (w*0.7, h*0.4)], fill="black")
        
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    # --- Presentation setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # Add title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.8))
    title_shape.text = title_text
    title_shape.text_frame.paragraphs[0].font.size = Pt(36)

    # --- Draw diagram ---
    shape_coords = {}
    for name, data in devices.items():
        icon_bytes = create_icon_bytes(data["type"])
        pic = slide.shapes.add_picture(io.BytesIO(icon_bytes), Inches(data["pos"][0]), Inches(data["pos"][1]), 
                                       width=Inches(0.8), height=Inches(0.6))
        shape_coords[name] = {
            "x": pic.left + pic.width / 2,
            "y": pic.top + pic.height / 2,
            "height": pic.height
        }
        # Add labels
        label_box = slide.shapes.add_textbox(
            pic.left, pic.top + pic.height, pic.width, Inches(0.4)
        )
        label_box.text_frame.text = f"{name}\n{data['ip']}"
        for para in label_box.text_frame.paragraphs:
            para.font.size = Pt(8)
            para.alignment = 1 # Center

    # Draw connections
    for start_dev, end_dev in connections:
        start = shape_coords[start_dev]
        end = shape_coords[end_dev]
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, start["x"], start["y"], end["x"], end["y"]
        )
        connector.line.color.rgb = RGBColor(0, 0, 0)
        # Place connector behind icons
        connector_xml = connector.element
        connector_xml.getparent().remove(connector_xml)
        connector_xml.getparent().insert(0, connector_xml)


    # --- Create Status Table ---
    rows, cols = len(devices) + 1, 2
    table_shape = slide.shapes.add_table(
        rows, cols, Inches(10), Inches(1.5), Inches(3), Inches(rows * 0.3)
    )
    table = table_shape.table
    table.cell(0, 0).text = "Device"
    table.cell(0, 1).text = "Status"
    
    for i, (name, data) in enumerate(devices.items()):
        table.cell(i + 1, 0).text = name
        status_cell = table.cell(i + 1, 1)
        status_cell.text = data["status"]
        fill = status_cell.fill
        fill.solid()
        fill.fore_color.rgb = status_colors[data["status"]]
        status_cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
