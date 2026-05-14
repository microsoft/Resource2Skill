def create_slide(
    output_pptx_path: str,
    title_text: str = "Glassmorphism\nPowerPoint Effect",
    body_text: str = "Transform your slide backgrounds into modern, readable interfaces using localized gaussian blurs and semi-transparent overlays.",
    bg_palette: str = "modern office interior", 
    accent_color: tuple = (255, 255, 255), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Glassmorphism Panel effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageFilter, ImageDraw
    import requests
    import io
    from lxml import etree

    # 1. Setup Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # PPT standard DPI is 144. Therefore 13.333" x 7.5" = 1920 x 1080 pixels
    DPI = 144
    W_PX, H_PX = int(13.333 * DPI), int(7.5 * DPI)

    # 2. Fetch or Generate Background Image
    try:
        url = f"https://source.unsplash.com/1920x1080/?{bg_palette.replace(' ', ',')}"
        response = requests.get(url, timeout=10)
        bg_img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        bg_img = bg_img.resize((W_PX, H_PX), Image.Resampling.LANCZOS)
    except Exception:
        # Fallback: Gradient/Pattern if download fails
        bg_img = Image.new("RGBA", (W_PX, H_PX), (20, 40, 60, 255))
        draw = ImageDraw.Draw(bg_img)
        for i in range(0, W_PX, 50):
            draw.line([(i, 0), (0, H_PX - i)], fill=(40, 80, 120, 255), width=20)
            draw.line([(W_PX, i), (i, H_PX)], fill=(40, 80, 120, 255), width=20)

    # Save base background to memory and insert into slide
    bg_stream = io.BytesIO()
    bg_img.convert("RGB").save(bg_stream, format="PNG")
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    # 3. Define Glass Panels Layout (3 Columns)
    panel_width_in = 3.2
    panel_height_in = 4.5
    gap_in = 0.8
    start_x_in = (13.333 - (panel_width_in * 3 + gap_in * 2)) / 2
    start_y_in = 1.5

    panels_data = [
        {"title": "01", "subtitle": "Opacity", "x": start_x_in},
        {"title": "02", "subtitle": "Blur", "x": start_x_in + panel_width_in + gap_in},
        {"title": "03", "subtitle": "Shadow", "x": start_x_in + (panel_width_in + gap_in) * 2},
    ]

    # Glass settings
    blur_radius = 35
    tint_color = (255, 255, 255, 60) # Semi-transparent white
    border_color = (255, 255, 255, 150) # Stronger white border

    # 4. Generate and Insert Glass Panels
    for panel in panels_data:
        x_px = int(panel["x"] * DPI)
        y_px = int(start_y_in * DPI)
        w_px = int(panel_width_in * DPI)
        h_px = int(panel_height_in * DPI)

        # Crop exact region from background
        box = (x_px, y_px, x_px + w_px, y_px + h_px)
        crop = bg_img.crop(box)

        # Apply heavy blur
        glass_pane = crop.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        # Add Tint Overlay
        overlay = Image.new("RGBA", glass_pane.size, tint_color)
        glass_pane = Image.alpha_composite(glass_pane, overlay)

        # Add Edge Border (1px)
        draw = ImageDraw.Draw(glass_pane)
        draw.rectangle([(0, 0), (w_px-1, h_px-1)], outline=border_color, width=2)

        # Save panel to memory
        panel_stream = io.BytesIO()
        glass_pane.save(panel_stream, format="PNG")
        panel_stream.seek(0)

        # Insert panel exactly over the coordinates it was cropped from
        pic = slide.shapes.add_picture(
            panel_stream, 
            Inches(panel["x"]), Inches(start_y_in), 
            width=Inches(panel_width_in), height=Inches(panel_height_in)
        )

        # Add Drop Shadow via lxml XML injection
        spPr = pic._element.xpath('.//p:spPr')[0]
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                     blurRad="300000", dist="150000", dir="2700000", algn="b")
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
        etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="25000") # 25% opacity

        # 5. Add Text Content over the Panel
        # Large Number
        txBox_num = slide.shapes.add_textbox(Inches(panel["x"] + 0.3), Inches(start_y_in + 0.3), Inches(1), Inches(1))
        tf_num = txBox_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = panel["title"]
        p_num.font.size = Pt(24)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(50, 50, 50)

        # Title/Subtitle
        txBox_sub = slide.shapes.add_textbox(Inches(panel["x"] + 0.3), Inches(start_y_in + 3.0), Inches(panel_width_in - 0.6), Inches(1))
        tf_sub = txBox_sub.text_frame
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = panel["subtitle"]
        p_sub.font.size = Pt(32)
        p_sub.font.bold = True
        p_sub.font.color.rgb = RGBColor(30, 30, 30)

    # 6. Add Main Slide Title overlapping the background and panels
    title_box = slide.shapes.add_textbox(Inches(start_x_in), Inches(0.4), Inches(8), Inches(1))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text.replace('\n', ' ')
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255) # White title stands out on dark BG

    # Apply brief shadow to main text for readability
    spPr_txt = title_box._element.xpath('.//p:spPr')[0]
    effectLst_txt = etree.SubElement(spPr_txt, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    outerShdw_txt = etree.SubElement(effectLst_txt, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                 blurRad="100000", dist="0", dir="0")
    srgbClr_txt = etree.SubElement(outerShdw_txt, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
    etree.SubElement(srgbClr_txt, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="60000")

    prs.save(output_pptx_path)
    return output_pptx_path
