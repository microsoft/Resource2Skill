def create_slide(
    output_pptx_path: str,
    title_text: str = "JOURNEY\nTHROUGH\nWOODS",
    body_text: str = "Embracing Nature in its glory, a train whistled to alert the forest's life!",
    bg_palette: str = "train,forest,dark",
    accent_color: tuple = (0, 191, 255), 
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Glassmorphism Reveal Panel effect.
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw, ImageFilter

    # --- Setup Dimensions & Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # High-res canvas for PIL (144 DPI mapping)
    # 13.333 * 144 = 1920, 7.5 * 144 = 1080
    dpi = 144
    canvas_w, canvas_h = 1920, 1080

    # Panel positioning in inches
    panel_left_in = 8.5
    panel_top_in = 1.0
    panel_width_in = 4.0
    panel_height_in = 5.5

    # Panel positioning in pixels
    box_left = int(panel_left_in * dpi)
    box_top = int(panel_top_in * dpi)
    box_right = int((panel_left_in + panel_width_in) * dpi)
    box_bottom = int((panel_top_in + panel_height_in) * dpi)
    box = (box_left, box_top, box_right, box_bottom)
    corner_radius = 40

    # --- Background Image Fetching / Fallback Generation ---
    bg_path = "temp_bg.png"
    glass_path = "temp_glass.png"
    
    try:
        # Fetch an image from Unsplash Source
        url = f"https://source.unsplash.com/random/1920x1080/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(bg_path, 'wb') as f:
                f.write(response.read())
        bg_image = Image.open(bg_path).convert("RGBA")
        # Ensure exact size
        bg_image = bg_image.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
    except Exception:
        # Fallback: Generate a rich gradient background with shapes
        bg_image = Image.new('RGBA', (canvas_w, canvas_h))
        draw = ImageDraw.Draw(bg_image)
        for y in range(canvas_h):
            r = int(20 + 20 * (y / canvas_h))
            g = int(30 + 40 * (y / canvas_h))
            b = int(40 + 60 * (y / canvas_h))
            draw.line([(0, y), (canvas_w, y)], fill=(r, g, b, 255))
        # Add abstract elements for the glass to blur
        draw.ellipse([200, 200, 700, 700], fill=(0, 150, 100, 255))
        draw.ellipse([1100, 300, 1600, 800], fill=(200, 100, 50, 255))

    # --- Process the Glass Panel Effect ---
    # 1. Crop and Blur
    glass_crop = bg_image.crop(box)
    glass_blurred = glass_crop.filter(ImageFilter.GaussianBlur(radius=30))
    panel_w, panel_h = glass_blurred.size

    # 2. Create the Rounded Corner Mask
    mask = Image.new('L', (panel_w, panel_h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, panel_w, panel_h), radius=corner_radius, fill=255)

    # Apply mask to the blurred section
    glass_panel = Image.new('RGBA', (panel_w, panel_h), (0,0,0,0))
    glass_panel.paste(glass_blurred, (0, 0), mask)

    # 3. Create Glass Tint/Reflection (Linear Gradient)
    shine = Image.new('RGBA', (panel_w, panel_h), (0,0,0,0))
    shine_draw = ImageDraw.Draw(shine)
    
    # We create a simple top-left to bottom-right fade effect manually
    for y in range(panel_h):
        for x in range(panel_w):
            diag = (x / panel_w + y / panel_h) / 2
            alpha = int(90 * (1 - diag)) # 90 down to 0
            shine.putpixel((x, y), (255, 255, 255, alpha))
            
    shine.putalpha(mask) # constrain tint to rounded rectangle shape
    
    # Composite the shine over the blurred background
    final_glass = Image.alpha_composite(glass_panel, shine)

    # 4. Add the defining glass edge (White, semi-transparent outline)
    edge = Image.new('RGBA', (panel_w, panel_h), (0,0,0,0))
    edge_draw = ImageDraw.Draw(edge)
    # Draw outline slightly inward to prevent clipping
    edge_draw.rounded_rectangle(
        (1, 1, panel_w - 2, panel_h - 2), 
        radius=corner_radius, 
        outline=(255, 255, 255, 140), 
        width=2
    )
    final_glass = Image.alpha_composite(final_glass, edge)

    # Save components
    bg_image.save(bg_path, format="PNG")
    final_glass.save(glass_path, format="PNG")

    # --- Assemble Presentation ---
    # Layer 1: The untouched background
    slide.shapes.add_picture(bg_path, 0, 0, width=Inches(13.333), height=Inches(7.5))

    # Layer 2: The Glass Panel
    slide.shapes.add_picture(
        glass_path, 
        left=Inches(panel_left_in), 
        top=Inches(panel_top_in), 
        width=Inches(panel_width_in), 
        height=Inches(panel_height_in)
    )

    # Layer 3: Typography inside the glass panel
    # Title Text
    title_box = slide.shapes.add_textbox(
        left=Inches(panel_left_in + 0.4), 
        top=Inches(panel_top_in + 0.5), 
        width=Inches(panel_width_in - 0.8), 
        height=Inches(2.0)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial" # Standard bold font
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255) # White text

    # Body Text
    body_box = slide.shapes.add_textbox(
        left=Inches(panel_left_in + 0.4), 
        top=Inches(panel_top_in + 3.0), 
        width=Inches(panel_width_in - 0.8), 
        height=Inches(2.0)
    )
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.name = "Arial"
    p_body.font.size = Pt(16)
    p_body.font.color.rgb = RGBColor(240, 240, 240)

    # Add a decorative vertical accent line inside the panel
    accent_line = slide.shapes.add_shape(
        9, # msoShapeRectangle
        left=Inches(panel_left_in + 0.4),
        top=Inches(panel_top_in + 2.7),
        width=Inches(0.5),
        height=Inches(0.04)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = RGBColor(255, 255, 255)
    accent_line.line.fill.background()

    # Save and cleanup
    prs.save(output_pptx_path)
    
    try:
        os.remove(bg_path)
        os.remove(glass_path)
    except OSError:
        pass

    return output_pptx_path
