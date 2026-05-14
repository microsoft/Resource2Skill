def create_slide(
    output_pptx_path: str,
    title_text: str = "TRAVEL",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris.",
    theme_keywords: list = ["mountains", "ocean", "forest", "desert"],
    panel_color: tuple = (36, 34, 91, 255), # Dark slate blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Cinematic Horizontal Gallery Morph effect.
    Generates two slides to demonstrate the Morph transition.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw

    prs = Presentation()
    # Set 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Helper: Image Downloader ---
    def get_image(keyword, width, height):
        try:
            url = f"https://source.unsplash.com/random/{width}x{height}/?{keyword}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                img = Image.open(BytesIO(response.read())).convert("RGB")
                # Ensure exact size by cropping center
                img_ratio = img.width / img.height
                target_ratio = width / height
                if img_ratio > target_ratio:
                    new_w = int(img.height * target_ratio)
                    offset = (img.width - new_w) // 2
                    img = img.crop((offset, 0, offset + new_w, img.height))
                elif img_ratio < target_ratio:
                    new_h = int(img.width / target_ratio)
                    offset = (img.height - new_h) // 2
                    img = img.crop((0, offset, img.width, offset + new_h))
                return img.resize((width, height), Image.LANCZOS)
        except Exception:
            # Fallback: Solid grey rectangle with text
            img = Image.new("RGB", (width, height), (100, 100, 100))
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), keyword, fill=(255, 255, 255))
            return img

    # --- Setup Assets ---
    # We need 4 images for the gallery
    gallery_images = []
    print("Fetching images, this may take a moment...")
    for kw in theme_keywords[:4]:
        img = get_image(kw, 1920, 1080)
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        gallery_images.append(img_io)

    # --- Create Lower Panel with Cutout using PIL ---
    # We render this at high res (300dpi equivalent) to look sharp on slide
    dpi = 150
    w_px = int(13.333 * dpi)
    h_px = int(2.5 * dpi) # Panel is bottom 2.5 inches
    
    panel_img = Image.new("RGBA", (w_px, h_px), panel_color)
    alpha = Image.new("L", (w_px, h_px), 255)
    draw_alpha = ImageDraw.Draw(alpha)
    
    # Cutout dimensions
    cutout_center_x_in = 3.0 # Position play button 3 inches from left
    cutout_radius_in = 0.55
    cx_px = int(cutout_center_x_in * dpi)
    cy_px = 0 # Top edge of the panel
    r_px = int(cutout_radius_in * dpi)
    
    # Draw transparent circle on alpha mask
    draw_alpha.ellipse([cx_px - r_px, cy_px - r_px, cx_px + r_px, cy_px + r_px], fill=0)
    panel_img.putalpha(alpha)
    
    panel_io = BytesIO()
    panel_img.save(panel_io, format='PNG')

    # --- Define layout geometry ---
    hero_h = Inches(5.0) # Top section height
    panel_top = Inches(5.0)
    panel_h = Inches(2.5)
    
    thumb_w = Inches(2.0)
    thumb_h = Inches(1.125) # 16:9 ratio
    thumb_y = panel_top + Inches(0.8) # Padding inside panel
    thumb_gap = Inches(0.2)
    thumb_start_x = Inches(4.5) # Start gallery right of the play button

    # --- Helper: Apply Morph Transition ---
    def apply_morph_transition(slide):
        morph_xml = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow"><p:morph/></p:transition>'
        transition_el = parse_xml(morph_xml)
        # Insert transition into slide element (usually after timing/color mappings, safely at end before extLst)
        slide.element.insert(2, transition_el)

    # --- Build Slide 1 ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 1. Hero Image 1
    pic1 = slide1.shapes.add_picture(gallery_images[0], 0, 0, width=Inches(13.333), height=Inches(7.5))
    pic1.name = "Hero_Image"
    
    # 2. Text Content (Title & Subtitle)
    tx_box = slide1.shapes.add_textbox(0, Inches(1.5), Inches(13.333), Inches(2.0))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(120)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(255, 255, 255)

    sub_box = slide1.shapes.add_textbox(Inches(2.5), Inches(3.2), Inches(8.33), Inches(1.0))
    sub_tf = sub_box.text_frame
    sub_tf.word_wrap = True
    p2 = sub_tf.add_paragraph()
    p2.text = body_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(240, 240, 240)

    # 3. Lower UI Panel Overlay
    panel1 = slide1.shapes.add_picture(panel_io, 0, panel_top, width=Inches(13.333), height=panel_h)
    panel1.name = "UI_Panel"

    # 4. Play Button Group (Circle + Triangle)
    btn_r = Inches(0.4)
    btn_x = Inches(cutout_center_x_in) - btn_r
    btn_y = panel_top - btn_r
    
    btn_circle = slide1.shapes.add_shape(9, btn_x, btn_y, btn_r*2, btn_r*2) # 9 = msoShapeOval
    btn_circle.fill.solid()
    btn_circle.fill.fore_color.rgb = RGBColor(panel_color[0], panel_color[1], panel_color[2])
    btn_circle.line.color.rgb = RGBColor(255, 100, 100) # Accent border
    btn_circle.line.width = Pt(2)
    btn_circle.name = "PlayButton_BG"

    btn_tri_w = Inches(0.25)
    btn_tri_h = Inches(0.3)
    btn_tri = slide1.shapes.add_shape(7, btn_x + Inches(0.3), btn_y + Inches(0.25), btn_tri_w, btn_tri_h) # 7 = msoShapeIsoscelesTriangle
    btn_tri.rotation = 90 # Point right
    btn_tri.fill.solid()
    btn_tri.fill.fore_color.rgb = RGBColor(255, 100, 100)
    btn_tri.line.fill.background()
    btn_tri.name = "PlayButton_Icon"

    # 5. Thumbnail Gallery Slide 1
    for i, img_stream in enumerate(gallery_images):
        x_pos = thumb_start_x + (i * (thumb_w + thumb_gap))
        # Important: Name the shapes sequentially so Morph tracks them
        thumb = slide1.shapes.add_picture(img_stream, x_pos, thumb_y, width=thumb_w, height=thumb_h)
        thumb.name = f"Thumb_{i}"
        # Add white border
        thumb.line.color.rgb = RGBColor(255, 255, 255)
        thumb.line.width = Pt(1)


    # --- Build Slide 2 (The Morph Target) ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 1. Hero Image changes to Image 2
    pic2 = slide2.shapes.add_picture(gallery_images[1], 0, 0, width=Inches(13.333), height=Inches(7.5))
    pic2.name = "Hero_Image" # Same name ensures Morph crossfades
    
    # 2. Text remains
    tx_box2 = slide2.shapes.add_textbox(0, Inches(1.5), Inches(13.333), Inches(2.0))
    tf2 = tx_box2.text_frame
    p2 = tf2.add_paragraph()
    p2.text = title_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(120)
    p2.font.bold = True
    p2.font.name = "Arial"
    p2.font.color.rgb = RGBColor(255, 255, 255)

    sub_box2 = slide2.shapes.add_textbox(Inches(2.5), Inches(3.2), Inches(8.33), Inches(1.0))
    sub_tf2 = sub_box2.text_frame
    sub_tf2.word_wrap = True
    p22 = sub_tf2.add_paragraph()
    p22.text = "Now exploring: " + theme_keywords[1].capitalize() + ". " + body_text
    p22.alignment = PP_ALIGN.CENTER
    p22.font.size = Pt(14)
    p22.font.color.rgb = RGBColor(240, 240, 240)

    # 3. Lower UI Panel Overlay (same position)
    panel2 = slide2.shapes.add_picture(panel_io, 0, panel_top, width=Inches(13.333), height=panel_h)
    panel2.name = "UI_Panel"

    # 4. Play Button Group (same position)
    btn_circle2 = slide2.shapes.add_shape(9, btn_x, btn_y, btn_r*2, btn_r*2)
    btn_circle2.fill.solid()
    btn_circle2.fill.fore_color.rgb = RGBColor(panel_color[0], panel_color[1], panel_color[2])
    btn_circle2.line.color.rgb = RGBColor(255, 100, 100)
    btn_circle2.line.width = Pt(2)
    btn_circle2.name = "PlayButton_BG"

    btn_tri2 = slide2.shapes.add_shape(7, btn_x + Inches(0.3), btn_y + Inches(0.25), btn_tri_w, btn_tri_h)
    btn_tri2.rotation = 90
    btn_tri2.fill.solid()
    btn_tri2.fill.fore_color.rgb = RGBColor(255, 100, 100)
    btn_tri2.line.fill.background()
    btn_tri2.name = "PlayButton_Icon"

    # 5. Thumbnail Gallery Slide 2 - SHIFTED LEFT
    # We shift all thumbnails left by exactly one unit (width + gap)
    shift_amount = thumb_w + thumb_gap
    for i, img_stream in enumerate(gallery_images):
        x_pos = thumb_start_x + (i * (thumb_w + thumb_gap)) - shift_amount
        thumb2 = slide2.shapes.add_picture(img_stream, x_pos, thumb_y, width=thumb_w, height=thumb_h)
        thumb2.name = f"Thumb_{i}" # Important: Name matching Slide 1 triggers movement Morph
        thumb2.line.color.rgb = RGBColor(255, 255, 255)
        thumb2.line.width = Pt(1)

    # Inject Morph XML transition into Slide 2
    apply_morph_transition(slide2)

    prs.save(output_pptx_path)
    return output_pptx_path
