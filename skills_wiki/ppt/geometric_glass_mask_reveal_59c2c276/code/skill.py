def create_slide(
    output_pptx_path: str,
    title_text: str = "THANK\nYOU",
    bg_theme: str = "cityscape,architecture",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Geometric Glass-Mask Reveal' visual effect.
    """
    import os
    import math
    import requests
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls
    from PIL import Image, ImageDraw, ImageFilter

    # --- 1. Initialization ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    WIDTH, HEIGHT = 1920, 1080

    # --- 2. Image Download & Preparation ---
    def get_background_image(theme: str) -> Image.Image:
        try:
            # Using picsum for reliable high-res random imagery
            url = f"https://picsum.photos/1920/1080?{theme}"
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            img = Image.open(BytesIO(res.content)).convert("RGBA")
            return img.resize((WIDTH, HEIGHT), Image.LANCZOS)
        except Exception as e:
            print(f"Image download failed: {e}. Using fallback solid color.")
            return Image.new("RGBA", (WIDTH, HEIGHT), (20, 30, 50, 255))

    bg_img = get_background_image(bg_theme)

    # --- 3. Create Gradient Base for Mask ---
    color1 = (255, 180, 140)  # Peach/Orange
    color2 = (140, 180, 220)  # Light Blue
    gradient_img = Image.new("RGB", (WIDTH, HEIGHT), color1)
    top_img = Image.new("RGB", (WIDTH, HEIGHT), color2)
    grad_mask = Image.new("L", (WIDTH, HEIGHT))
    
    # Generate diagonal gradient data
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Diagonal gradient distribution
            val = int(255 * (x + y) / (WIDTH + HEIGHT))
            grad_mask.putpixel((x, y), val)
            
    gradient_img = Image.composite(gradient_img, top_img, grad_mask).convert("RGBA")
    
    # Add slight transparency to the overall gradient
    gradient_img.putalpha(240)

    # --- 4. Punching Transparent Geometric Holes ---
    # We draw black (0) on a white (255) mask to punch holes.
    alpha_mask = Image.new("L", (WIDTH, HEIGHT), 255)

    def draw_rotated_rrect_hole(mask: Image.Image, cx, cy, w, h, radius, angle):
        temp_size = int(max(w, h) * 1.5)
        # Create a local mask: 0 inside the shape, 255 outside
        shape_mask = Image.new("L", (temp_size, temp_size), 255)
        draw = ImageDraw.Draw(shape_mask)
        x0, y0 = (temp_size - w) / 2, (temp_size - h) / 2
        draw.rounded_rectangle([x0, y0, x0+w, y0+h], radius=radius, fill=0)
        # Rotate the shape
        shape_mask = shape_mask.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=255)
        
        # Paste the hole onto the main alpha_mask
        paste_x = int(cx - temp_size / 2)
        paste_y = int(cy - temp_size / 2)
        
        # We want to paste black (0) wherever shape_mask is black (0)
        # Inverting shape_mask so white represents the hole for the `paste` mask parameter
        inv_shape_mask = Image.eval(shape_mask, lambda p: 255 - p)
        black_patch = Image.new("L", (temp_size, temp_size), 0)
        mask.paste(black_patch, (paste_x, paste_y), mask=inv_shape_mask)

    # Define the geometry of the holes
    holes = [
        # Center huge diamond
        {"cx": 960, "cy": 540, "w": 550, "h": 550, "r": 60, "a": 45},
        # Top-Left diagonal
        {"cx": 580, "cy": 160, "w": 180, "h": 180, "r": 20, "a": 45},
        {"cx": 400, "cy": -20, "w": 120, "h": 120, "r": 15, "a": 45},
        # Bottom-Right diagonal
        {"cx": 1340, "cy": 920, "w": 250, "h": 250, "r": 30, "a": 45},
        {"cx": 1560, "cy": 1140, "w": 150, "h": 150, "r": 15, "a": 45},
        # Bottom-Left diagonal
        {"cx": 580, "cy": 920, "w": 200, "h": 200, "r": 25, "a": 45},
        {"cx": 380, "cy": 1120, "w": 130, "h": 130, "r": 15, "a": 45},
        # Top-Right diagonal
        {"cx": 1340, "cy": 160, "w": 200, "h": 200, "r": 25, "a": 45},
    ]

    # Draw all diamond holes
    for h in holes:
        draw_rotated_rrect_hole(alpha_mask, h["cx"], h["cy"], h["w"], h["h"], h["r"], h["a"])

    # Draw circle holes directly
    c_draw = ImageDraw.Draw(alpha_mask)
    circles = [
        {"cx": 350, "cy": 250, "r": 80},
        {"cx": 1550, "cy": 750, "r": 90},
    ]
    for c in circles:
        c_draw.ellipse([c["cx"]-c["r"], c["cy"]-c["r"], c["cx"]+c["r"], c["cy"]+c["r"]], fill=0)

    # Apply the hole mask to the gradient layer
    gradient_img.putalpha(alpha_mask)
    
    # Composite over background
    bg_img.paste(gradient_img, (0, 0), gradient_img)

    # --- 5. Draw Floating Outlines ---
    def draw_floating_outline(bg: Image.Image, cx, cy, w, h, radius, angle, color, width):
        temp_size = int(max(w, h) * 1.6)
        temp_img = Image.new("RGBA", (temp_size, temp_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp_img)
        x0, y0 = (temp_size - w) / 2, (temp_size - h) / 2
        
        if radius > 0:
            draw.rounded_rectangle([x0, y0, x0+w, y0+h], radius=radius, outline=color, width=width)
        else:
            # Circle
            draw.ellipse([x0, y0, x0+w, y0+h], outline=color, width=width)
            
        temp_img = temp_img.rotate(angle, resample=Image.BICUBIC, expand=False)
        paste_x, paste_y = int(cx - temp_size / 2), int(cy - temp_size / 2)
        bg.paste(temp_img, (paste_x, paste_y), temp_img)

    # Floating vector accents
    draw_floating_outline(bg_img, 960, 540, 620, 620, 70, 45, (255, 255, 0, 255), 8)   # Yellow diamond
    draw_floating_outline(bg_img, 960, 540, 650, 600, 80, 20, (255, 255, 255, 220), 4) # White skewed rectangle
    draw_floating_outline(bg_img, 960, 540, 700, 700, 0, 0, (0, 255, 200, 255), 5)     # Cyan circle
    
    # Save composite to file and insert into slide
    composite_path = "temp_composite_bg.png"
    bg_img.save(composite_path)
    slide.shapes.add_picture(composite_path, 0, 0, Inches(13.333), Inches(7.5))

    # --- 6. Typography & Styling (lxml Injection) ---
    tx_width = Inches(8)
    tx_height = Inches(3)
    tx_left = (prs.slide_width - tx_width) / 2
    tx_top = (prs.slide_height - tx_height) / 2

    textbox = slide.shapes.add_textbox(tx_left, tx_top, tx_width, tx_height)
    tf = textbox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = PP_ALIGN.CENTER
    
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = title_text
    
    # Text formatting
    for run in p.runs:
        font = run.font
        font.name = "Impact"  # Heavy display font
        font.size = Pt(85)
        font.bold = True
        font.color.rgb = RGBColor(255, 255, 255)
        
        # Inject Reflection and Drop Shadow via lxml
        rPr = run._r.get_or_add_rPr()
        effect_xml = f"""
        <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <!-- Drop Shadow -->
            <a:outerShdw blurRad="40000" dist="35000" dir="2700000" algn="tl" rotWithShape="0">
                <a:srgbClr val="000000">
                    <a:alpha val="60000"/>
                </a:srgbClr>
            </a:outerShdw>
            <!-- Floor Reflection -->
            <a:reflection blurRad="10000" stA="50000" endA="500" endPos="35000" dist="0" dir="5400000" sy="-100000" algn="bl" rotWithShape="0"/>
        </a:effectLst>
        """
        effect_element = parse_xml(effect_xml)
        rPr.append(effect_element)

    # Save and Cleanup
    prs.save(output_pptx_path)
    if os.path.exists(composite_path):
        os.remove(composite_path)
        
    return output_pptx_path
