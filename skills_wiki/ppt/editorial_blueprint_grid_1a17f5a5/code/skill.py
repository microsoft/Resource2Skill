def create_slide(
    output_pptx_path: str,
    title_text: str = "Grid Systems\nIn Practice",
    body_text: str = "The concept of design is understood as a structured process. By utilizing grid systems, designers ensure that the arrangement of text, images, and negative space follows a predictable rhythm.\n\nConsistent spacing—from character tracking to paragraph leading—profoundly affects reading speed and comprehension. A well-aligned layout brings an inherent sense of order and rational beauty to the presentation.",
    bg_theme: str = "architecture,minimal",
    accent_color: tuple = (47, 185, 169),  # Teal from the video
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Editorial Blueprint Grid" visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw
    import urllib.request
    import io
    import os

    # Helper function to fetch and perfectly crop images to fit grid cells
    def fetch_and_crop_image(url: str, width_in: float, height_in: float, output_filename: str, dpi: int = 150) -> str:
        target_w, target_h = int(width_in * dpi), int(height_in * dpi)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img = Image.open(io.BytesIO(response.read())).convert('RGB')
                
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h

            if img_ratio > target_ratio:
                # Image is too wide, crop horizontally
                new_w = int(img.height * target_ratio)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))
            else:
                # Image is too tall, crop vertically
                new_h = int(img.width / target_ratio)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))
                
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        except Exception as e:
            # Fallback placeholder if network fails
            img = Image.new('RGB', (target_w, target_h), color=(210, 220, 210))
            draw = ImageDraw.Draw(img)
            draw.line((0, 0, img.width, img.height), fill=(190, 200, 190), width=3)
            draw.line((0, img.height, img.width, 0), fill=(190, 200, 190), width=3)
            
        img.save(output_filename, format='PNG')
        return output_filename

    # Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Colors
    c_bg = RGBColor(226, 235, 222)       # Light Sage Green
    c_accent = RGBColor(*accent_color)   # Teal
    c_dark = RGBColor(60, 60, 60)        # Dark Slate
    c_light = RGBColor(255, 255, 255)    # White

    # === Layer 1: Background ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = c_bg
    bg.line.fill.background()

    # === Grid Math (3 Columns x 2 Rows) ===
    margin = 1.0
    gutter = 0.4
    col_w = (13.333 - (2 * margin) - (2 * gutter)) / 3  # ~ 3.511 inches
    row_h = (7.5 - (2 * margin) - (1 * gutter)) / 2     # 2.55 inches

    # Coordinates
    x_col1 = margin
    x_col2 = margin + col_w + gutter
    x_col3 = margin + (col_w + gutter) * 2
    y_row1 = margin
    y_row2 = margin + row_h + gutter

    # === Layer 2: Content Population ===

    # Cell [Row 1, Col 1]: Title & Typography
    tx_box = slide.shapes.add_textbox(Inches(x_col1), Inches(y_row1), Inches(col_w), Inches(row_h))
    tf = tx_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "EDITORIAL DESIGN"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = c_accent
    p0.font.name = 'Arial'

    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = c_dark
    p1.font.name = 'Arial'
    p1.space_before = Pt(10)
    p1.line_spacing = 1.0

    p2 = tf.add_paragraph()
    p2.text = "Structuring information for maximum clarity, readability, and rational aesthetic appeal."
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(100, 100, 100)
    p2.font.name = 'Arial'
    p2.space_before = Pt(14)
    p2.line_spacing = 1.2

    # Cells [Row 1, Col 2 & 3]: Large Spanning Image
    w_span2 = (col_w * 2) + gutter
    img1_url = f"https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80"
    img1_path = fetch_and_crop_image(img1_url, w_span2, row_h, "temp_grid_1.png")
    slide.shapes.add_picture(img1_path, Inches(x_col2), Inches(y_row1), Inches(w_span2), Inches(row_h))

    # Cell [Row 2, Col 1]: Solid Accent Block
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x_col1), Inches(y_row2), Inches(col_w), Inches(row_h))
    accent.fill.solid()
    accent.fill.fore_color.rgb = c_accent
    accent.line.fill.background()

    # Accent Block Text (Oversized Number)
    num_box = slide.shapes.add_textbox(Inches(x_col1 + 0.15), Inches(y_row2 + 0.05), Inches(col_w - 0.3), Inches(1.0))
    p_num = num_box.text_frame.paragraphs[0]
    p_num.text = "01"
    p_num.font.size = Pt(64)
    p_num.font.bold = True
    # Calculate a lighter tint of the accent color for the number
    lighter_teal = RGBColor(min(255, accent_color[0]+60), min(255, accent_color[1]+60), min(255, accent_color[2]+60))
    p_num.font.color.rgb = lighter_teal
    p_num.font.name = 'Arial'

    # Accent Block Text (Heading & Description)
    acc_tx = slide.shapes.add_textbox(Inches(x_col1 + 0.2), Inches(y_row2 + 1.1), Inches(col_w - 0.4), Inches(1.2))
    acc_tf = acc_tx.text_frame
    acc_tf.word_wrap = True
    pa1 = acc_tf.paragraphs[0]
    pa1.text = "Alignment & Pacing"
    pa1.font.size = Pt(16)
    pa1.font.bold = True
    pa1.font.color.rgb = c_light
    pa1.font.name = 'Arial'

    pa2 = acc_tf.add_paragraph()
    pa2.text = "Elements must align strictly to the underlying grid to create visual unity and guide the reader's eye."
    pa2.font.size = Pt(11)
    pa2.font.color.rgb = c_light
    pa2.font.name = 'Arial'
    pa2.space_before = Pt(8)
    pa2.line_spacing = 1.3

    # Cell [Row 2, Col 2]: Single Square Image
    img2_url = f"https://images.unsplash.com/photo-1561089489-02ebfc1c9115?w=600&q=80"
    img2_path = fetch_and_crop_image(img2_url, col_w, row_h, "temp_grid_2.png")
    slide.shapes.add_picture(img2_path, Inches(x_col2), Inches(y_row2), Inches(col_w), Inches(row_h))

    # Cell [Row 2, Col 3]: Body Text Block
    body_box = slide.shapes.add_textbox(Inches(x_col3), Inches(y_row2), Inches(col_w), Inches(row_h))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True

    pb = tf_body.paragraphs[0]
    pb.text = body_text
    pb.font.size = Pt(11)
    pb.font.color.rgb = c_dark
    pb.font.name = 'Arial'
    pb.line_spacing = 1.4 # High line spacing as per tutorial recommendation

    # Clean up temp files
    if os.exists("temp_grid_1.png"): os.remove("temp_grid_1.png")
    if os.exists("temp_grid_2.png"): os.remove("temp_grid_2.png")

    prs.save(output_pptx_path)
    return output_pptx_path
