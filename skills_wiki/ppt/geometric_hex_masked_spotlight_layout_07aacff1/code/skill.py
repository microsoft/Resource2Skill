def create_slide(
    output_pptx_path: str,
    title_text: str = "EMPLOYEE SPOTLIGHT",
    employee_name: str = "CASEY SADLER",
    employee_title: str = "SENIOR MANAGER OF\nPROFESSIONAL DEVELOPMENT",
    avatar_url: str = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?crop=faces&fit=crop&w=600&h=600&q=80",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Geometric Hex-Masked Spotlight visual effect.
    """
    import io
    import math
    import urllib.request
    from lxml import etree
    from PIL import Image, ImageDraw
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_CONNECTOR

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide

    # --- Colors ---
    BG_COLOR = (94, 128, 157)       # Muted Slate Blue
    ACCENT_COLOR = (114, 211, 227)  # Bright Cyan
    WHITE = (255, 255, 255)

    # --- 1. Background Fill ---
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*BG_COLOR)

    # --- 2. PIL Image Processing (Hexagon Masking) ---
    border_size = 600
    avatar_size = 540

    try:
        req = urllib.request.Request(avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            base_img = Image.open(io.BytesIO(response.read())).convert("RGBA")
    except Exception:
        # Fallback if download fails
        base_img = Image.new("RGBA", (avatar_size, avatar_size), (200, 200, 200, 255))
        d = ImageDraw.Draw(base_img)
        d.text((avatar_size//3, avatar_size//2), "Avatar Placeholder", fill=(50,50,50,255))

    # Resize and crop to square
    base_img = base_img.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # Create inner hexagon mask for the photo
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    cx, cy = avatar_size/2, avatar_size/2
    r_img = avatar_size/2
    # Flat-topped hexagon vertices
    pts_img = [
        (cx + r_img * math.cos(math.radians(60*i)), cy + r_img * math.sin(math.radians(60*i))) 
        for i in range(6)
    ]
    draw_mask.polygon(pts_img, fill=255)
    base_img.putalpha(mask)

    # Create outer canvas with cyan hexagon border
    canvas = Image.new("RGBA", (border_size, border_size), (0, 0, 0, 0))
    draw_canvas = ImageDraw.Draw(canvas)
    cx_b, cy_b = border_size/2, border_size/2
    r_b = border_size/2
    pts_b = [
        (cx_b + r_b * math.cos(math.radians(60*i)), cy_b + r_b * math.sin(math.radians(60*i))) 
        for i in range(6)
    ]
    # Draw the cyan background/border hexagon
    draw_canvas.polygon(pts_b, fill=ACCENT_COLOR + (255,))

    # Paste the masked photo onto the cyan background (creating a perfect border)
    offset = (border_size - avatar_size) // 2
    canvas.paste(base_img, (offset, offset), base_img)

    # Save to BytesIO for insertion
    img_stream = io.BytesIO()
    canvas.save(img_stream, format="PNG")
    img_stream.seek(0)

    # --- 3. Insert Image & Accents into PPTX ---
    # Center coords on slide for the avatar
    slide_cx = 13.333 / 2
    slide_cy = 2.5
    img_display_size = 3.0  # inches
    
    img_left = slide_cx - (img_display_size / 2)
    img_top = slide_cy - (img_display_size / 2)

    # Draw radiating sunburst lines (background layer)
    radius_outer = 2.1  # inches from center
    radius_inner = 1.6  # inches from center
    for i in range(6):
        angle_rad = math.radians(60 * i)
        start_x = slide_cx + radius_inner * math.cos(angle_rad)
        start_y = slide_cy + radius_inner * math.sin(angle_rad)
        end_x = slide_cx + radius_outer * math.cos(angle_rad)
        end_y = slide_cy + radius_outer * math.sin(angle_rad)
        
        line = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            Inches(start_x), Inches(start_y),
            Inches(end_x), Inches(end_y)
        )
        line.line.color.rgb = RGBColor(*WHITE)
        line.line.width = Pt(3)

    # Insert the composite avatar image
    slide.shapes.add_picture(
        img_stream, 
        Inches(img_left), Inches(img_top), 
        width=Inches(img_display_size), height=Inches(img_display_size)
    )

    # --- 4. Typography & Layout ---
    # Employee Name
    name_top = img_top + img_display_size + 0.3
    tx_name = slide.shapes.add_textbox(
        Inches(1), Inches(name_top), Inches(11.333), Inches(0.8)
    )
    tf_name = tx_name.text_frame
    tf_name.text = employee_name.upper()
    tf_name.paragraphs[0].alignment = PP_ALIGN.CENTER
    font_name = tf_name.paragraphs[0].font
    font_name.name = 'Arial'
    font_name.size = Pt(44)
    font_name.bold = True
    font_name.color.rgb = RGBColor(*WHITE)

    # Employee Title
    title_top = name_top + 0.8
    tx_title = slide.shapes.add_textbox(
        Inches(1), Inches(title_top), Inches(11.333), Inches(1.0)
    )
    tf_title = tx_title.text_frame
    tf_title.text = employee_title.upper()
    tf_title.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf_title.word_wrap = True
    font_title = tf_title.paragraphs[0].font
    font_title.name = 'Arial'
    font_title.size = Pt(18)
    font_title.color.rgb = RGBColor(220, 230, 240)  # Slightly dimmed white

    # Bottom Callout / Title ("EMPLOYEE SPOTLIGHT")
    callout_top = 6.2
    tx_callout = slide.shapes.add_textbox(
        Inches(1), Inches(callout_top), Inches(11.333), Inches(1.0)
    )
    tf_callout = tx_callout.text_frame
    tf_callout.text = title_text.upper()
    tf_callout.paragraphs[0].alignment = PP_ALIGN.CENTER
    font_callout = tf_callout.paragraphs[0].font
    font_callout.name = 'Arial Black'
    font_callout.size = Pt(36)
    font_callout.color.rgb = RGBColor(*WHITE)

    # LXML Magic: Add drop shadow to the Bottom Callout text box
    spPr = tx_callout.element.spPr
    effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                 blurRad="38100", dist="38100", dir="2700000", algn="tl")
    srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
    etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="30000")

    # Save output
    prs.save(output_pptx_path)
    return output_pptx_path
