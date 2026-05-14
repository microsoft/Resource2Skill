def create_slide(
    output_pptx_path: str,
    title_text: str = "圖 像\n佔 比 圖",
    body_text: str = "如何用 PPT 製作?",
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the Thematic Icon Proportion Chart visual effect.
    Uses PIL to synthesize custom icon masks and dynamically fill them based on data percentages.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_CONNECTOR
    from PIL import Image, ImageDraw

    # === Helper Functions for PIL Image Generation ===
    def get_heart_mask(size=(400, 400)):
        scale = 4  # supersample for anti-aliasing
        img = Image.new('L', (size[0]*scale, size[1]*scale), 0)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        r = int(w * 0.25)
        cx1, cx2 = int(w/2 - r), int(w/2 + r)
        cy = int(h * 0.3)
        draw.ellipse([cx1-r, cy-r, cx1+r, cy+r], fill=255)
        draw.ellipse([cx2-r, cy-r, cx2+r, cy+r], fill=255)
        draw.polygon([(cx1 - r*0.9, cy + r*0.4), (cx2 + r*0.9, cy + r*0.4), (w/2, h - int(h*0.1))], fill=255)
        draw.polygon([(cx1, cy), (cx2, cy), (w/2, h - int(h*0.1))], fill=255)
        draw.polygon([(w/2, cy-int(r*0.5)), (cx1, cy), (cx2, cy)], fill=255)
        return img.resize(size, Image.Resampling.LANCZOS)

    def get_drop_mask(size=(400, 400)):
        scale = 4
        img = Image.new('L', (size[0]*scale, size[1]*scale), 0)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        r = int(w * 0.3)
        cx, cy = int(w/2), int(h - r - h*0.1)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=255)
        top_pt = (w/2, int(h*0.1))
        draw.polygon([top_pt, (cx - r*0.95, cy - r*0.2), (cx + r*0.95, cy - r*0.2)], fill=255)
        return img.resize(size, Image.Resampling.LANCZOS)

    def get_lightning_mask(size=(400, 400)):
        scale = 4
        img = Image.new('L', (size[0]*scale, size[1]*scale), 0)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        pts = [
            (w*0.6, h*0.1), (w*0.2, h*0.55), (w*0.5, h*0.55),
            (w*0.4, h*0.9), (w*0.8, h*0.45), (w*0.5, h*0.45)
        ]
        draw.polygon(pts, fill=255)
        return img.resize(size, Image.Resampling.LANCZOS)

    def generate_filled_icon(icon_type, percentage, filename):
        size = (400, 400)
        if icon_type == "heart":
            mask = get_heart_mask(size)
        elif icon_type == "drop":
            mask = get_drop_mask(size)
        else:
            mask = get_lightning_mask(size)
            
        base_color = (0, 0, 0, 40)   # Empty state: Semi-transparent black
        fill_color = (255, 255, 255, 255) # Filled state: Solid white
        
        w, h = size
        color_img = Image.new('RGBA', (w, h), base_color)
        fill_img = Image.new('RGBA', (w, h), fill_color)

        # Calculate cutoff for percentage (bottom-up fill)
        cutoff = int(h * (1 - percentage / 100.0))

        if cutoff < h:
            fill_crop = fill_img.crop((0, cutoff, w, h))
            color_img.paste(fill_crop, (0, cutoff))

        final_img = color_img.copy()
        final_img.putalpha(mask)
        final_img.save(filename, "PNG")

    # === PPTX Generation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Colors
    bg_color = RGBColor(236, 195, 68)   # Mustard Yellow
    text_color = RGBColor(40, 40, 40)   # Dark Charcoal

    # Slide Background
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = bg_color

    # Main Title Left
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(4.5), Inches(2.5))
    tf = title_box.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.font.size = Pt(80)
    p.font.bold = True
    p.font.color.rgb = text_color
    if len(tf.paragraphs) > 1:
        tf.paragraphs[1].font.size = Pt(80)
        tf.paragraphs[1].font.bold = True
        tf.paragraphs[1].font.color.rgb = text_color

    # Subtitle Left
    sub_box = slide.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(4.5), Inches(1.0))
    tf_sub = sub_box.text_frame
    tf_sub.text = body_text
    p_sub = tf_sub.paragraphs[0]
    p_sub.font.size = Pt(28)
    p_sub.font.bold = True
    p_sub.font.color.rgb = text_color

    # Data Items (Right Side)
    data = [
        {"icon": "heart", "val": 80},
        {"icon": "drop", "val": 65},
        {"icon": "lightning", "val": 52}
    ]

    x_center_icon = 7.0
    x_center_text = 10.0
    y_starts = [1.0, 3.25, 5.5]
    icon_size = 1.5

    generated_files = []

    for i, item in enumerate(data):
        icon_file = f"temp_icon_{i}.png"
        generated_files.append(icon_file)
        
        # 1. Generate & Insert Graphic
        generate_filled_icon(item["icon"], item["val"], icon_file)
        slide.shapes.add_picture(
            icon_file, 
            Inches(x_center_icon - icon_size/2), 
            Inches(y_starts[i]), 
            width=Inches(icon_size), 
            height=Inches(icon_size)
        )
        
        # 2. Add Percentage Text
        val_str = f"{item['val']}%"
        txt_box = slide.shapes.add_textbox(
            Inches(x_center_text), 
            Inches(y_starts[i] + 0.1), 
            Inches(2.5), 
            Inches(1.0)
        )
        p_val = txt_box.text_frame.paragraphs[0]
        p_val.text = val_str
        p_val.font.size = Pt(48)
        p_val.font.bold = True
        p_val.font.color.rgb = text_color
        
        # 3. Add Connector Line
        # Line from right edge of icon to left edge of text
        line = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            Inches(x_center_icon + icon_size/2 + 0.2), Inches(y_starts[i] + icon_size/2),
            Inches(x_center_text - 0.2), Inches(y_starts[i] + icon_size/2)
        )
        line.line.color.rgb = text_color
        line.line.width = Pt(1.5)

    prs.save(output_pptx_path)

    # Cleanup temporary images
    for f in generated_files:
        if os.path.exists(f):
            os.remove(f)

    return output_pptx_path
