def create_slide(
    output_pptx_path: str,
    title_text: str = "AFRO-ASIAN\nLITERATURE",
    body_text: str = "About",
    bg_theme: str = "world map texture",
    core_theme: str = "african asian art painting",
    globe_theme: str = "earth globe satellite",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Thematic Collage Hero Slide' visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    import urllib.request
    import io
    import os

    # Setup presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Helper: Fetch image with fallback
    def fetch_image(keyword, fallback_color, size=(800, 600)):
        try:
            url = f"https://source.unsplash.com/featured/{size[0]}x{size[1]}?{urllib.parse.quote(keyword)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return Image.open(io.BytesIO(response.read())).convert("RGBA")
        except Exception:
            img = Image.new("RGBA", size, fallback_color)
            return img

    # --- Layer 1: Textured Map Background ---
    # Fetch, convert to grayscale, and tint with a sepia/brownish tone
    bg_img = fetch_image(bg_theme, (210, 180, 140, 255), size=(1280, 720))
    bg_gray = bg_img.convert("L").convert("RGBA")
    sepia_overlay = Image.new("RGBA", bg_gray.size, (160, 120, 80, 180))
    bg_composite = Image.alpha_composite(bg_gray, sepia_overlay)
    
    bg_path = "temp_bg.png"
    bg_composite.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # --- Layer 2: Central Thematic Rectangle ---
    # The focal point of the slide
    core_img = fetch_image(core_theme, (80, 100, 120, 255), size=(800, 450))
    # Add a slight dark vignette/overlay to make text readable
    overlay = Image.new("RGBA", core_img.size, (0, 0, 0, 90))
    core_composite = Image.alpha_composite(core_img, overlay)
    
    core_path = "temp_core.png"
    core_composite.save(core_path)
    
    core_width, core_height = Inches(8.5), Inches(4.5)
    core_left = (prs.slide_width - core_width) / 2
    core_top = Inches(2.2)
    slide.shapes.add_picture(core_path, core_left, core_top, core_width, core_height)

    # --- Layer 3: Overlapping Globe Element ---
    # Masking a square image into a perfect circle
    globe_size = 400
    globe_img = fetch_image(globe_theme, (40, 150, 100, 255), size=(globe_size, globe_size))
    
    # Create circular mask
    mask = Image.new("L", globe_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, globe_size, globe_size), fill=255)
    
    # Apply mask
    globe_circular = globe_img.copy()
    globe_circular.putalpha(mask)
    
    globe_path = "temp_globe.png"
    globe_circular.save(globe_path)
    
    globe_radius = Inches(2.2)
    globe_left = (prs.slide_width - globe_radius) / 2
    globe_top = core_top - (globe_radius / 1.6) # Overlaps the top edge of the core image
    slide.shapes.add_picture(globe_path, globe_left, globe_top, globe_radius, globe_radius)

    # --- Layer 4: Typography ---
    # Helper to create text with a simulated drop shadow for extreme legibility
    def add_shadowed_text(text, left, top, width, height, font_size, is_bold=True, is_title=False):
        # 1. Add Shadow
        shadow_box = slide.shapes.add_textbox(left + Inches(0.04), top + Inches(0.04), width, height)
        sp = shadow_box.text_frame.paragraphs[0]
        sp.text = text
        sp.alignment = PP_ALIGN.CENTER
        sp.font.size = font_size
        sp.font.bold = is_bold
        sp.font.name = "Georgia"
        sp.font.color.rgb = RGBColor(20, 20, 20)
        
        # 2. Add Main Text
        text_box = slide.shapes.add_textbox(left, top, width, height)
        p = text_box.text_frame.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.size = font_size
        p.font.bold = is_bold
        p.font.name = "Georgia"
        p.font.color.rgb = RGBColor(255, 255, 255) if is_title else RGBColor(240, 240, 240)

    # Subtitle ("About")
    add_shadowed_text(
        text=body_text,
        left=Inches(0), top=core_top + Inches(0.4),
        width=prs.slide_width, height=Inches(1.0),
        font_size=Pt(24), is_bold=False
    )

    # Main Title
    add_shadowed_text(
        text=title_text.upper(),
        left=Inches(0), top=core_top + Inches(1.2),
        width=prs.slide_width, height=Inches(2.0),
        font_size=Pt(54), is_bold=True, is_title=True
    )

    # Cleanup temp files
    prs.save(output_pptx_path)
    for p in [bg_path, core_path, globe_path]:
        if os.path.exists(p):
            os.remove(p)

    return output_pptx_path
