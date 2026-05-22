def create_slide(
    output_pptx_path: str,
    title_text: str = "IT Infrastructure diagram for XYZ LLC.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Hub-and-Spoke Infrastructure Architecture Visualization.
    """
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # ==========================================
    # Helper Functions: Synthesize Topology Icons
    # ==========================================
    def generate_building_icon(color=(135, 206, 250, 255)):
        img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Main building block
        draw.rectangle([40, 20, 160, 180], fill=color)
        draw.rectangle([40, 20, 160, 180], outline=(100, 150, 200, 255), width=3)
        # Windows
        for x in [60, 100, 140]:
            for y in [40, 75, 110, 145]:
                draw.rectangle([x, y, x+20, y+20], fill=(255, 255, 255, 200))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes

    def generate_router_icon(color=(0, 150, 214, 255)):
        img = Image.new('RGBA', (200, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # 3D Cylinder base
        draw.ellipse([20, 80, 180, 130], fill=(0, 100, 160, 255))
        draw.rectangle([20, 45, 180, 105], fill=color)
        # Top face
        draw.ellipse([20, 20, 180, 70], fill=(50, 180, 240, 255))
        # Abstract arrows (cross pattern on top)
        draw.line([100, 30, 100, 60], fill=(255,255,255,255), width=4)
        draw.polygon([90,35, 110,35, 100,25], fill=(255,255,255,255))
        draw.polygon([90,55, 110,55, 100,65], fill=(255,255,255,255))
        
        draw.line([65, 45, 135, 45], fill=(255,255,255,255), width=4)
        draw.polygon([70,35, 70,55, 60,45], fill=(255,255,255,255))
        draw.polygon([130,35, 130,55, 140,45], fill=(255,255,255,255))
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes

    def generate_server_icon(bg_color=(60, 60, 60, 255), led_color=(0, 255, 0, 255)):
        img = Image.new('RGBA', (150, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw 4 stacked server units
        for i, y in enumerate([10, 60, 110, 160]):
            draw.rectangle([10, y, 140, y+35], fill=bg_color)
            draw.rectangle([10, y, 140, y+35], outline=(100, 100, 100, 255), width=2)
            # Vents
            for vx in range(25, 100, 10):
                draw.line([vx, y+10, vx, y+25], fill=(30, 30, 30, 255), width=3)
            # Status LEDs
            draw.ellipse([115, y+15, 125, y+25], fill=led_color)
            if i % 2 == 0:
                draw.ellipse([100, y+15, 110, y+25], fill=(0, 150, 255, 255)) # Activity LED
                
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes

    def generate_cloud_icon(color=(255, 204, 0, 255)):
        img = Image.new('RGBA', (200, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Overlapping circles to form cloud
        draw.ellipse([30, 50, 100, 120], fill=color)
        draw.ellipse([70, 20, 150, 100], fill=color)
        draw.ellipse([110, 50, 180, 120], fill=color)
        draw.rectangle([65, 70, 145, 120], fill=color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes

    # ==========================================
    # Text Setup: Slide Title
    # ==========================================
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(8), Inches(1))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(0, 51, 102)

    # ==========================================
    # Layout Definitions & Placement
    # ==========================================
    nodes = {
        "central": {"x": 6.0, "y": 1.5, "label": "Central Office"},
        "branch1": {"x": 2.5, "y": 4.5, "label": "Branch Office 1"},
        "branch2": {"x": 9.5, "y": 4.5, "label": "Branch Office 2"},
    }

    # Store center points of routers for drawing connections later
    router_centers = {}

    for key, pos in nodes.items():
        # 1. Place Building
        b_pic = slide.shapes.add_picture(generate_building_icon(), Inches(pos["x"]), Inches(pos["y"]), width=Inches(1.0))
        
        # 2. Add Label
        label_box = slide.shapes.add_textbox(Inches(pos["x"] - 0.5), Inches(pos["y"] + 1.05), Inches(2), Inches(0.5))
        tf = label_box.text_frame
        tf.text = pos["label"]
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(14)
        tf.paragraphs[0].font.name = "Arial"
        
        # 3. Place Router (slightly overlapping the bottom right of the building)
        rx = pos["x"] + 0.3
        ry = pos["y"] + 1.4
        r_pic = slide.shapes.add_picture(generate_router_icon(), Inches(rx), Inches(ry), width=Inches(0.8))
        
        # Calculate precise center point of the router for connectors
        rcx = Inches(rx) + r_pic.width / 2
        rcy = Inches(ry) + r_pic.height / 2
        router_centers[key] = (rcx, rcy)

    # 4. Place Server Farm at Central Office
    slide.shapes.add_picture(
        generate_server_icon(), 
        Inches(nodes["central"]["x"] + 1.2), 
        Inches(nodes["central"]["y"] + 0.2), 
        width=Inches(0.8)
    )

    # 5. Place Internet Cloud (left of central office)
    cloud_x, cloud_y = 3.0, 1.8
    slide.shapes.add_picture(
        generate_cloud_icon(), 
        Inches(cloud_x), 
        Inches(cloud_y), 
        width=Inches(1.2)
    )
    
    # Label for Internet
    int_label_box = slide.shapes.add_textbox(Inches(cloud_x - 0.4), Inches(cloud_y + 0.8), Inches(2), Inches(0.5))
    int_tf = int_label_box.text_frame
    int_tf.text = "Internet"
    int_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    int_tf.paragraphs[0].font.size = Pt(14)

    cloud_center = (Inches(cloud_x) + Inches(0.6), Inches(cloud_y) + Inches(0.5))

    # ==========================================
    # Connectors (Topology Lines)
    # ==========================================
    def draw_connection(start_pt, end_pt):
        # Adding a straight connector
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, start_pt[0], start_pt[1], end_pt[0], end_pt[1])
        # Format line: Dark gray, 2pt
        connector.line.color.rgb = RGBColor(80, 80, 80)
        connector.line.width = Pt(2.0)
        # Push to back so it sits underneath the icons
        slide.shapes._spTree.insert(2, connector._element) # Index 2 keeps it above background but below most shapes

    # Connect Central Router to Branch 1 Router
    draw_connection(router_centers["central"], router_centers["branch1"])
    # Connect Central Router to Branch 2 Router
    draw_connection(router_centers["central"], router_centers["branch2"])
    # Connect Branch 1 Router to Branch 2 Router (Mesh link)
    draw_connection(router_centers["branch1"], router_centers["branch2"])
    # Connect Central Router to Internet Cloud
    draw_connection(router_centers["central"], cloud_center)

    prs.save(output_pptx_path)
    return output_pptx_path
