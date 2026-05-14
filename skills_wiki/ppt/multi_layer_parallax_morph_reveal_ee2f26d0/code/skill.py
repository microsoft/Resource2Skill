def create_slide(
    output_pptx_path: str,
    title_text: str = "EXPLORE",
    body_text: str = "Parallax Scrolling Effect\nBrought to life with Morph.",
    bg_palette: str = "mountains", 
    accent_color: tuple = (0, 191, 255), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Multi-Layer Parallax Morph Reveal visual effect.
    """
    import os
    import math
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Asset Generation 1: Background Image ---
    bg_path = "parallax_bg_temp.jpg"
    try:
        # Fetch an oversized high-res landscape
        req = urllib.request.Request(
            f"https://source.unsplash.com/featured/1600x1000/?{bg_palette},landscape",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(bg_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback: Create a gradient image if download fails
        img = Image.new('RGB', (1600, 1000), color=(25, 45, 65))
        draw = ImageDraw.Draw(img)
        for y in range(1000):
            r = int(25 + (20 * (y / 1000)))
            g = int(45 + (30 * (y / 1000)))
            b = int(65 + (40 * (y / 1000)))
            draw.line([(0, y), (1600, y)], fill=(r, g, b))
        img.save(bg_path)

    # --- Asset Generation 2: Wavy Foreground Overlay (PIL) ---
    overlay_path = "parallax_overlay_temp.png"
    w, h = 2000, 800
    overlay_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay_img)
    
    # Draw organic wave for the top edge
    points = [(0, h), (w, h)]
    for x in range(w, -1, -5):
        y = 150 + 40 * math.sin(x / 80.0) + 20 * math.cos(x / 200.0)
        points.append((x, y))
    
    # Dark slate with alpha transparency
    draw.polygon(points, fill=(15, 20, 25, 245))
    overlay_img.save(overlay_path)

    # ==========================================
    # SLIDE 1: THE HOOK (Initial State)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    
    # 1. Background (Oversized, positioned at 0,0)
    bg1 = slide1.shapes.add_picture(bg_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(8.5))
    bg1.name = "!!ParallaxBG" # Force morph matching

    # 2. Hero Title (Center)
    title1 = slide1.shapes.add_textbox(Inches(0), Inches(2.5), Inches(13.333), Inches(2))
    title1.name = "!!HeroTitle"
    tf1 = title1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = title_text
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(110)
    p1.font.bold = True
    p1.font.name = "Arial Black"
    p1.font.color.rgb = RGBColor(255, 255, 255)

    # 3. Wavy Overlay (Resting completely off-screen at bottom)
    over1 = slide1.shapes.add_picture(overlay_path, Inches(-0.5), Inches(7.5), width=Inches(14.5), height=Inches(5))
    over1.name = "!!WavyOverlay"

    # ==========================================
    # SLIDE 2: THE REVEAL (Parallax Shift State)
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)

    # 1. Background (Shifted UP slightly: -1 inch. Moves slowest)
    bg2 = slide2.shapes.add_picture(bg_path, Inches(0), Inches(-1.0), width=Inches(13.333), height=Inches(8.5))
    bg2.name = "!!ParallaxBG"

    # 2. Hero Title (Shifted UP massively: -2.5 inches. Moves faster to create depth)
    title2 = slide2.shapes.add_textbox(Inches(0), Inches(-2.5), Inches(13.333), Inches(2))
    title2.name = "!!HeroTitle"
    tf2 = title2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(110)
    p2.font.bold = True
    p2.font.name = "Arial Black"
    p2.font.color.rgb = RGBColor(255, 255, 255)

    # 3. Wavy Overlay (Shifted UP dramatically to cover bottom half. Moves fastest)
    over2 = slide2.shapes.add_picture(overlay_path, Inches(-0.5), Inches(3.5), width=Inches(14.5), height=Inches(5))
    over2.name = "!!WavyOverlay"

    # 4. New Content fading in on the overlay
    body_box = slide2.shapes.add_textbox(Inches(2), Inches(5.0), Inches(9.333), Inches(1.5))
    body_box.name = "BodyContent" # Doesn't need !! because it only exists on slide 2 (will fade in)
    tf_body = body_box.text_frame
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.alignment = PP_ALIGN.CENTER
    p_body.font.size = Pt(28)
    p_body.font.name = "Calibri"
    p_body.font.color.rgb = RGBColor(240, 240, 240)

    # --- Morph Transition XML Injection ---
    # Apply morph transition to Slide 2 using lxml
    p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
    p14_ns = "http://schemas.microsoft.com/office/powerpoint/2010/main"
    
    # Build transition element: <p:transition spd="slow"><p14:morph option="byObject"/></p:transition>
    transition = etree.Element(f"{{{p_ns}}}transition", spd="slow")
    etree.SubElement(transition, f"{{{p14_ns}}}morph", option="byObject")
    
    # Append to Slide 2's root element
    slide2.element.append(transition)

    # Cleanup temporary assets
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(overlay_path): os.remove(overlay_path)

    prs.save(output_pptx_path)
    return output_pptx_path
