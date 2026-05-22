def create_slide(
    output_pptx_path: str,
    title_text: str = "PERFORMANCE",
    subtitle_text: str = "Review",
    bg_theme: str = "business meeting",
    primary_color: tuple = (18, 93, 168),   # Corporate Blue
    accent_color: tuple = (86, 43, 133),    # Deep Purple
    highlight_color: tuple = (0, 174, 239), # Cyan
    text_accent_color: tuple = (255, 192, 0), # Yellow/Gold
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Corporate Dynamic Wave Intersection" style.
    Generates a custom background using PIL with sweeping geometric curves.
    """
    import os
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageOps

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    width_px, height_px = 1920, 1080

    # === Layer 1: Background Image Generation via PIL ===
    
    # 1a. Fetch Background Photo
    bg_img = Image.new("RGBA", (width_px, height_px), (220, 220, 225, 255))
    try:
        # Use Unsplash Source API with the provided theme
        url = f"https://images.unsplash.com/photo-1600880292203-757bb62b4baf?q=80&w=1920&auto=format&fit=crop"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            fetched_img = Image.open(io.BytesIO(response.read())).convert("RGBA")
            # Resize and crop to fit 1920x1080 exactly
            bg_img = ImageOps.fit(fetched_img, (width_px, height_px), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Warning: Could not fetch image. Using solid background. Error: {e}")

    # 1b. Draw the "Waves"
    # We use a separate transparent overlay to draw the overlapping curved shapes
    overlay = Image.new("RGBA", (width_px, height_px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Note: Drawing massive ellipses off-canvas creates smooth, shallow curves on-canvas

    # Shape 1: Accent Wave (Purple sliver peeking out from behind)
    # Positioning creates a curve sweeping up from bottom-left to mid-right
    draw.ellipse([-400, 480, 2800, 3680], fill=accent_color + (255,))

    # Shape 2: Main Wave (Blue, holding the text)
    # Slightly lower and offset to let the purple edge show
    draw.ellipse([-300, 520, 2900, 3720], fill=primary_color + (255,))

    # Shape 3: Small highlight swoosh in the bottom left corner
    draw.ellipse([-400, 900, 300, 1600], fill=highlight_color + (255,))

    # Composite the waves over the photo
    final_bg = Image.alpha_composite(bg_img, overlay)
    
    # Save temporarily
    temp_bg_path = "temp_wave_bg.png"
    final_bg.save(temp_bg_path)

    # === Layer 2: Insert Background into PPTX ===
    slide.shapes.add_picture(temp_bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 3: Typography & Content ===
    
    # Position text box in the lower right quadrant over the blue wave
    left_margin = Inches(6.5)
    top_margin = Inches(4.2)
    width = Inches(6.0)
    height = Inches(2.5)
    
    tx_box = slide.shapes.add_textbox(left_margin, top_margin, width, height)
    tf = tx_box.text_frame
    tf.word_wrap = True

    # Main Title
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = 'Arial'
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.RIGHT

    # Subtitle
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = 'Arial'
    p2.font.size = Pt(48)
    p2.font.bold = False
    p2.font.color.rgb = RGBColor(*text_accent_color)
    p2.alignment = PP_ALIGN.RIGHT

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(temp_bg_path):
        os.remove(temp_bg_path)
        
    return output_pptx_path
